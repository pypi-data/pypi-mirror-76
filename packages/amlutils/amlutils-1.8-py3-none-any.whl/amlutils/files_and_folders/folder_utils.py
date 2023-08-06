import glob
import logging
import os
import shutil
import typing


def full_path_for_contents(
    folder_path: str,
    suffix: typing.Optional[str] = None,
    prefix: typing.Optional[str] = None,
) -> typing.List[str]:
    """Returns full paths of all files in the folder, does not traverse sub folders

    Parameters
    ----------
    folder_path: str
        full path to folder whose contents are needed
    suffix: typing.Optional[str], optional
        if specified only return files ending in suffix from folder, by default None
    prefix: typing.Optional[str], optional
        if specified only return files beginning with prefix from folder, by default None

    Returns
    -------
    List of full path of files contained in the folder
    """
    glob_string = ""
    if suffix:
        glob_string = "*{}".format(suffix)
    if prefix:
        glob_string = "{}*{}".format(prefix, glob_string)
    if glob_string:
        folder_path = os.path.join(folder_path, glob_string)
    else:
        folder_path = os.path.join(folder_path, "*")
    logging.info("Looking for all files matching: {}".format(folder_path))
    return glob.glob(folder_path)


def delete_folder(folder_path: str, empty: typing.Optional[bool] = True) -> None:
    """Delete specified folder

    Parameters
    ----------
    folder_path : str
        full path to folder that needs to be deleted
    empty : typing.Optional[bool], optional
        if False, delete folder even if its not empty
        if True will not delete a folder that has contents, by default True
    """
    if empty:
        files = full_path_for_contents(folder_path)
        if len(files) > 0:
            logging.warning("Folder({}) is non empty, has {} files. NOT DELETING".format(folder_path, len(files)))
            return
        else:
            os.rmdir(folder_path)
            return

    shutil.rmtree(folder_path)


def make_folder_if_not_exists(folder_path: str, make_new: typing.Optional[bool] = False) -> None:
    """Make folder and sub folders for the given folder path

    Parameters
    ----------
    folder_path : str
        full path of folder that needs to be created
    make_new : typing.Optional[bool], optional
        if True, delete the existing folder and all its contents and create new folder, by default False
    """
    if os.path.exists(folder_path):
        logging.info("Folder({}) already exists".format(folder_path))
        if not make_new:
            return

        # delete existing folder and contents and re-create folder
        delete_folder(folder_path, empty=False)

    os.makedirs(folder_path)
