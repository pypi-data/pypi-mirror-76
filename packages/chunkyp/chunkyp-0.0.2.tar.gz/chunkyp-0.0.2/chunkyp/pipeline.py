import ray
import psutil
import math
import logging
import types

from typing import Iterator, Callable, List
from .utils import chunk_iterator, process_record

logging.basicConfig()
logging.root.setLevel(logging.INFO)


def p(
        in_field: str or List[str],
        func: Callable,
        out_field: str or List[str] = None,
        **kwargs
) -> (Callable, Callable):
    """
    Wraps any function with the record fields it will touch and returns either its sequential or parallel form.

    Args:
        in_field: A record's field the passed function changes. Can be a string or an iterable if the function requires
        multiple fields.
        func: A function which takes in a record's field and outputs something.
        out_field: A record's field to which the function's output will be written to. If a function outputs a tuple,
        new_field should be a list of the same length. (Default: None, functions outputs will instead be written to
        field)
        **kwargs: Additional arguments passed to the functions.

    Returns:
        A tuple of two functions (_p, __p) which are used by chunkyp to run the funcs in the single-thread or
        as part of the parallel mode.
    """
    kwargs = {k: (ray.get(v) if isinstance(v, ray._raylet.ObjectID) else v) for k, v in kwargs.items()}

    def _p(records):
        for record in records:
            yield process_record(in_field, func, record, out_field, **kwargs)

    def _pp(records):
        processed = []
        for record in records:
            processed.append(
                process_record(
                    in_field,
                    func,
                    record,
                    out_field,
                    **kwargs
                )
            )
        return processed

    return _p, _pp


def pipe(
        records: Iterator[dict],
        *funcs: p,
) -> Iterator[dict]:
    """
    A single-threaded pipe which pipes records through it in sequence.

    Args:
        records: An iterator of dictionaries. We call these dictionaries "records" throughout chunkyp.
        *funcs: A list of p functions to be applied to the records.

    Returns:
        A generator of the resulting records modified by the p functions.
    """

    result = records
    for f in funcs:
        result = f[0](records=result)  # f[0] selects _p: the sequential p function
    return result


def ppipe(
        records: Iterator[dict],
        *funcs,
        records_in_memory: int or None = None,
        processes: int or None = None,
) -> Iterator[dict]:
    """
    A multi-threaded parallel pipe (or ppipe) which pipes records through it in parallel. Note that each record is still
    handled by a chain of p functions in sequence.

    You can think of a ppipe as a set of multiple parallel pipes.

    Args:
        records: An iterator of dictionaries. We call these dictionaries "records" throughout chunkyp.
        *funcs: A list of p functions to be applied to the records.
        records_in_memory: The number of records to pass to each one of the parallel pipes.
        processes: The number of pipes to launch in parallel. (Default: #logical_cores - 1)
    Returns:
        A generator of the resulting records modified by the p functions.
    """

    # initialize ray if user hasn't already
    if not ray.is_initialized():
        logging.warning('Ray is not running. Starting ray!')
        ray.init()

    # define a ray_pipe which wraps a _ppipe functions which actually handles the records
    def _ppipe(
            records: Iterator[dict],
            *funcs
    ):
        result = records
        for f in funcs:
            result = f[1](records=result)  # f[1] selects _pp: the parallel p function
        return result
    ray_pipe = ray.remote(_ppipe)

    # set number of processes if user hasn't already
    if processes is None:
        processes = psutil.cpu_count(logical=True) - 1  # number of logical cores (threads) on system

    # if records_in_memory is not set AND the a record generator is passed - uwind it into a list
    if records_in_memory is None and isinstance(records, types.GeneratorType):
        records = list(records)

    # prepare batches
    if records_in_memory is None:
        batches = [records]
    else:
        batches = chunk_iterator(n=records_in_memory, iterable=records)

    print('chunksize', records_in_memory)

    for batch in batches:
        batch = list(batch)  # read into memory

        print('batch_len:', len(batch))

        # chunk so we can parallelize
        chunks = chunk_iterator(n=math.ceil(len(batch) / processes), iterable=batch)

        futures = [ray_pipe.remote(list(chunk), *funcs) for chunk in chunks]
        results = ray.get(futures)

        for result in results:
            for record in result:
                yield record
