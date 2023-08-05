import itertools

from typing import Callable, Iterable, Tuple


def chunk_iterator(n, iterable):
    """
    A function to split an iterable into multiple n-sized iterable.
    """
    it = iter(iterable)
    while True:
        chunk_it = itertools.islice(it, n)
        try:
            first_el = next(chunk_it)
        except StopIteration:
            return
        yield itertools.chain((first_el,), chunk_it)


def process_record(
        field: str or Iterable[str],
        func: Callable,
        record: dict,
        new_field: str or Iterable[str] = None,
        **kwargs
) -> dict:
    """
    This is the actual record processor which calls the function passed to a p function.

    Args:
        field: The record's input field(s) used as input to func.
        func: The function (originally passed to a p functions) to be applied to the record.
        record: The record to be modified.
        new_field: The record's output field(s) to be modified. (Default: None, field will be used instead)
        **kwargs: Additional arguments to be passed to func.

    Returns:
        A modified record.

    """
    if new_field is None:
        new_field = field
    res = func(record[field], **kwargs) if isinstance(field, str) else func(*[record[k] for k in field], **kwargs)
    if isinstance(res, Tuple):
        # assert len(new_field) == len(res)  # TODO: this is a bit clunky
        for f, r in zip(new_field, res):
            record[f] = r
    else:
        record[new_field] = res

    return record
