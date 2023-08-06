import re
import typing


def atoi(text: str) -> typing.Union[int, str]:
    """returns numeric representation of text if possible else original text

    Parameters
    ----------
    text: str
        text whose numeric representation is needed

    Returns
    -------
    typing.Union[int, str]
        the integer representation of the number if possible else the original text
    """
    return int(text) if text.isdigit() else text


def get_natural_keys(text: str) -> typing.List[typing.Union[int, str]]:
    """list.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html

    Parameters
    ----------
    text: str
        text that needs to be transformed into its natural format

    Returns
    ------
    typing.List[typing.Union[int, str]]
        list of integers and strings based on placement of digits and characters
    """
    return [atoi(c) for c in re.split(r"(\d+)", text)]


def get_natural_sorted_list(input_list: typing.List[typing.Any]) -> typing.List[typing.Any]:
    """
    sort list of strings in natural order ["0","1","2","10"] instead of ["0","1","10","2"]

    Parameters
    ----------
    input_list: list of elements that need to be sorted

    Returns
    -------
    typing.List[typing.Any]
        sorted list of elements in natural order
    """
    temp_list = [str(elem) for elem in input_list]
    temp_list.sort(key=get_natural_keys)
    return temp_list
