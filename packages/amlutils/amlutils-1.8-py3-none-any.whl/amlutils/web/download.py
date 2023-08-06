import logging
import os
import requests
import typing

from multiprocessing import Pool

import amlutils.files_and_folders as file_utils


class DownloadDataInfo:
    def __init__(self, url: str, download_folder: str, overwrite_existing: bool) -> None:
        """Information needed to download data from url

        Parameters
        ----------
        url : str
            Url of file that needs to be downloaded
        download_folder : str
            full path to folder where the downloaded files need to be saved
        """
        self.url = url
        self.download_folder = download_folder
        self.overwrite_existing = overwrite_existing


def download_data_from_url(download_info: DownloadDataInfo) -> None:
    """Download data from url and store to folder

    Parameters
    ----------
    download_info : DownloadDataInfo
        download information containing url and destination folder
    """
    file_utils.make_folder_if_not_exists(download_info.download_folder)

    file_name = download_info.url.split("/")[-1]
    if not file_name:
        logging.error("Could not determine file name from {} NOT DOWNLOADING".format(download_info.url))
        return

    store_file_path = os.path.join(download_info.download_folder, file_name)
    if os.path.exists(store_file_path) and not download_info.overwrite_existing:
        logging.warning("File {} already exists, NOT OVERWRITING".format(store_file_path))
        return

    logging.info("Downloading file {}".format(file_name))
    response = requests.get(download_info.url, stream=True)
    with open(store_file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
    logging.info("Download completed: {}".format(file_name))


def download_data_from_urls(
    urls_list: typing.List[str],
    download_folder: str,
    num_processes: typing.Optional[int] = 4,
    overwrite_existing: typing.Optional[bool] = False,
) -> None:
    """[summary]

    Parameters
    ----------
    urls_list : typing.List[str]
        List of urls for data that need to be downloaded
    download_folder : str
        Destination folder where downloaded data need to be stored
    num_processes : typing.Optional[int], optional
        Number of processes to use to download data, by default 8
    """
    file_utils.make_folder_if_not_exists(download_folder)

    download_info = [DownloadDataInfo(url, download_folder, overwrite_existing) for url in urls_list]
    with Pool(num_processes) as p:
        p.map(download_data_from_url, download_info)
