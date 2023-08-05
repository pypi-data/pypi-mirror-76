import ray
import psutil
import math
import logging

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
                    **{k: (ray.get(v) if isinstance(v, ray._raylet.ObjectID) else v) for k, v in kwargs.items()}
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
        chunksize: int or None = None,
        n_pipes: int or None = None,
) -> Iterator[dict]:
    """
    A multi-threaded parallel pipe (or ppipe) which pipes records through it in parallel. Note that each record is still
    handled by a chain of p functions in sequence.

    You can think of a ppipe as a set of multiple parallel pipes.

    Args:
        records: An iterator of dictionaries. We call these dictionaries "records" throughout chunkyp.
        *funcs: A list of p functions to be applied to the records.
        chunksize: The number of records to pass to each one of the parallel pipes.
        n_pipes: The number of pipes to launch. (Default: #logical_cores - 1)
    Returns:
        A generator of the resulting records modified by the p functions.
    """

    if not ray.is_initialized():
        raise Exception("ray is not running!")

    if n_pipes is None:
        n_pipes = psutil.cpu_count(logical=True) - 1 # number of logical cores (threads) on system

    iter_len = len(records) if hasattr(records, '__len__') else None

    if iter_len and chunksize > iter_len:
        chunksize = iter_len
        logging.info(f'reducing batch_size to {chunksize}')

    def _ppipe(
        records: Iterator[dict],
        *funcs
    ):
        result = records
        for f in funcs:
            result = f[1](records=result)  # f[1] selects _pp: the parallel p function
        return result

    ray_pipe = ray.remote(_ppipe)

    # fill up memory with outer loop
    batches = chunk_iterator(n=chunksize, iterable=records)

    for batch in batches:
        chunks = chunk_iterator(n=math.ceil(chunksize / n_pipes), iterable=batch)

        # parallelize with inner loop
        for chunk in chunks:

            futures = ray_pipe.remote(chunk, *funcs)
            results = ray.get(futures)

            for r in results:
                yield r
