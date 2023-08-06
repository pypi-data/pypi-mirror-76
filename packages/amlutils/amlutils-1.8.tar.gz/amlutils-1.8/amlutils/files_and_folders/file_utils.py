import shutil
import typing


def move_files(file_paths: typing.List[str], folder_path: str) -> None:
    """move files specified by their full paths to a destination folder

    Parameters
    ----------
    file_paths : typing.List[str]
        List of full paths of files that need to be moved
    folder_path : str
        Full path of destination folder where the files need to be moved
    """
    for fp in file_paths:
        shutil.move(fp, folder_path)


def copy_files(file_paths: typing.List[str], folder_path: str) -> None:
    """copy files specified by their full paths to a destination folder

    Parameters
    ----------
    file_paths : typing.List[str]
        List of full paths of files that need to be copied
    folder_path : str
        Full path of destination folder where the files need to be copied
    """
    for fp in file_paths:
        shutil.copy(fp, folder_path)
