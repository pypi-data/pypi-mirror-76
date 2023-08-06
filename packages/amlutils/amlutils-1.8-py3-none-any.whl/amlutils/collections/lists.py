import typing


def flatten_list(list_of_lists: typing.List[typing.List[typing.Any]]) -> typing.List[typing.Any]:
    """flatten a 2 level deep nested list into a single list

    Parameters
    ----------
    list_of_lists:  typing.List[typing.List[typing.Any]]
        2 level nested list

    Returns
    -------
    typing.List[typing.Any]
        the unrolled list
    """
    return [item for sublist in list_of_lists for item in sublist]


def chunks_of_list(iterable: typing.List[typing.Any], chunk_size: int):
    """generate fixed sized list out of given list

    Parameters
    ----------
    iterable: typing.List[typing.Any]
        iterable which needs to be broken down into fixed size chunks
    chunk_size: int
        desired size to divide the iterable into, all chunks except for the last one will be of this size

    Returns
    -------
        Generator[typing.List]
            Fixed size chunks of the original list
    """
    length = len(iterable)
    for ndx in range(0, length, chunk_size):
        yield iterable[ndx:min(ndx + chunk_size, length)]
