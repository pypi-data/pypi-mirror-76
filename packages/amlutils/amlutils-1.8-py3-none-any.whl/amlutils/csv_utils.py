import csv
import logging
import sys
import typing


csv.field_size_limit(sys.maxsize)


def store_list_to_csv(
    file_path: str,
    data: typing.List[typing.List[typing.Any]],
    delimiter: typing.Optional[str] = ",",
    quotechar: typing.Optional[str] = "|",
) -> None:
    """stores a list of data to a csv file

    Parameters
    ----------
    file_path : str
        full path to csv file to be created
    data : typing.List[typing.List[typing.Any]]
        List of lists that needs to be stored as csv
    delimiter : typing.Optional[str], optional
        delimiter to be used for creating columns, by default ","
    quotechar : typing.Optional[str], optional
        how to quote the delimiter if it is part of data, by default "|"
    """
    num_rows = 0
    with open(file_path, "w") as csv_file:
        csv_writer = csv.writer(
            csv_file,
            delimiter=delimiter,
            quotechar=quotechar,
            quoting=csv.QUOTE_MINIMAL,
        )
        for row in data:
            csv_writer.writerow(row)
            num_rows += 1
    logging.info("Number of lines written {}".format(num_rows))


def store_dictionary_to_csv(
    file_path: str,
    data: typing.List[typing.Dict[str, typing.Any]],
    headers: typing.Optional[typing.List[str]] = None,
    delimiter: typing.Optional[str] = ",",
    quotechar: typing.Optional[str] = "|",
) -> None:
    """stores a list of dictionaries to a csv file

    Parameters
    ----------
    file_path : str
        full path to csv file to be created
    data : typing.List[typing.Dict[str, typing.Any]]
        list of dictionaries, where each key of the dictionary indicates columns
    headers : typing.Optional[typing.List[str]], optional
        if provided will use only these keys from dictionaries to create csv
        if None will use all keys from first dictionary in the list, by default None
    delimiter : typing.Optional[str], optional
        delimiter to be used for creating columns, by default ","
    quotechar : typing.Optional[str], optional
        character to be used to escape the delimiter if its a part of the data, by default "|"
    """
    if headers is None or headers == []:
        headers = data[0].keys()
    final_data = []
    for row in data:
        final_data.append({key: value for key, value in row.items() if key in headers})
    with open(file_path, "w") as csv_file:
        csv_writer = csv.DictWriter(
            csv_file,
            fieldnames=headers,
            delimiter=delimiter,
            quotechar=quotechar,
            quoting=csv.QUOTE_MINIMAL,
        )
        csv_writer.writeheader()
        csv_writer.writerows(final_data)


def parse_csv_file(
    file_path: str,
    has_header: typing.Optional[bool] = False,
    column_id: typing.Optional[int] = None,
    delimiter: typing.Optional[str] = ",",
    quotechar: typing.Optional[str] = "|",
    encoding: typing.Optional[str] = "utf-8",
) -> typing.Union[typing.List[typing.List[typing.Any]], typing.List[typing.Any]]:
    """parse a csv file and return data

    Parameters
    ----------
    file_path : str
        full path to csv file that needs to be parsed
    has_header : typing.Optional[bool], optional
        whether the first row of the file are headers
        If true the first row will be skipped in returned data, by default False
    column_id : typing.Optional[int], optional
        if only need data of a specific column from the csv file, by default None
    delimiter : typing.Optional[str], optional
        what is the delimiter used to indicate columns in csv file, by default ","
    quotechar : typing.Optional[str], optional
        what is the quotechar used to escape delimiter, by default "|"
    encoding: typing.Optional[str], optional
        what encoding mode should be used for opening the file, by default "utf-8"

    Returns
    -------
    typing.Union[typing.List[typing.List[typing.Any]], typing.List[typing.Any]]
        either returns a List of Lists of the data from the csv file,
        OR returns a List of data indicating only one column as specified by column_id
    """
    data = []
    with open(file_path, "r", encoding=encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter, quotechar=quotechar)
        for row in csv_reader:
            if has_header:
                # skip header row
                has_header = False
                continue
            if column_id is not None:
                data.append(row[column_id])
            else:
                data.append(row)
    return data
