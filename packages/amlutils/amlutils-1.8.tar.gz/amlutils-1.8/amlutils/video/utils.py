import cv2
import logging
import os
import numpy as np
import typing

from multiprocessing.pool import ThreadPool

from amlutils.files_and_folders import folder_utils


class ExtractionInfo:
    def __init__(
        self,
        video_path: str,
        extraction_folder: str,
        sample_rate: typing.Optional[int] = 1,
        frame_suffix: typing.Optional[str] = "_frame_{}_sec.jpg",
    ) -> None:
        """ExtractionInfo to store information about frames to be extracted from video

        Parameters
        ----------
        video_path : str
            full path to video from which frames need to be extracted
        extraction_folder : str
            full path to folder where extracted frames should be saved
        sample_rate : typing.Optional[int], optional
            how many frames per second to extract, by default 1
            sample_rate > 1 -> multiple samples per second
            sample_rate < 1 -> one sample for multiple second
        frame_suffix : typing.Optional[str], optional
            prefix to append to extracted frames for storing them to images, by default "_frame_{}_sec.jpg"
        """
        self.video_path = video_path
        self.extraction_folder = extraction_folder
        self.sample_rate = sample_rate
        self.frame_suffix = frame_suffix


def extract_frames_from_video(extraction_info: ExtractionInfo) -> None:
    """Extract frames from video as specified in extraction_info

    Parameters
    ----------
    extraction_info : ExtractionInfo
        extraction info controlling, extraction metadata

    Raises
    ------
    ValueError
        extraction_info.sample_rate has to be greater than 0
    """
    video_path = extraction_info.video_path
    file_name = os.path.basename(video_path)
    folder_utils.make_folder_if_not_exists(extraction_info.extraction_folder)
    base_output_file_name = os.path.join(extraction_info.extraction_folder, file_name).rsplit(".", 1)[0]
    base_output_file_name = base_output_file_name + extraction_info.frame_suffix

    if extraction_info.sample_rate <= 0:
        raise ValueError("Sample Rate has to be greater 0")

    if os.path.exists(base_output_file_name.format(0)):
        # if the first extracted frame for a video exists consider it processed
        logging.info("Video({}) already processed".format(video_path))
        return

    count = 0
    vidcap = cv2.VideoCapture(video_path)
    success = True
    while success:
        second_to_sample_at = (count * 1000 / extraction_info.sample_rate)
        vidcap.set(cv2.CAP_PROP_POS_MSEC, second_to_sample_at)
        success, image = vidcap.read()
        if not success:
            # no new frames to process
            logging.info("Processed video file: {}".format(video_path))
            return

        cv2.imwrite(base_output_file_name.format(count), image)
        count = count + 1


def extract_frames_from_videos(
    videos_folder: str,
    extraction_folder: str,
    videos_extension: typing.Optional[str] = ".mp4",
    sample_rate: typing.Optional[int] = 1,
    num_processes: typing.Optional[int] = 8,
    frame_suffix: typing.Optional[str] = "_frame_{}_sec.jpg",
) -> None:
    """[summary]

    Parameters
    ----------
    videos_folder : str
        [description]
    extraction_folder : str
        [description]
    videos_extension : typing.Optional[str], optional
        [description], by default ".mp4"
    sample_rate : typing.Optional[int], optional
        [description], by default 1
    num_processes : typing.Optional[int], optional
        [description], by default 8
    """
    video_paths = folder_utils.full_path_for_contents(videos_folder, suffix=videos_extension)
    folder_utils.make_folder_if_not_exists(extraction_folder)

    extraction_info_list = [
        ExtractionInfo(video_path, extraction_folder, sample_rate, frame_suffix) for video_path in video_paths
    ]
    tp = ThreadPool(num_processes)
    _ = tp.map(extract_frames_from_video, extraction_info_list)
    tp.close()


def write_to_video(
    cv2_image_list: typing.List[np.ndarray],
    output_video_file_path: str,
    video_fps: int,
    width: typing.Optional[int] = None,
    height: typing.Optional[int] = None,
) -> None:
    """create a video out of a list of images represented as np.ndarray,

    Parameters
    ----------
    cv2_image_list: typing.List[np.ndarray]
        List of images represented as np.ndarray generally obtained from cv2.imread()
    output_video_file_path: str
        full path to where video should be stored
    video_fps: int
        number of images to use per second of video from the list
    width: typing.Optional[int], optional
        expected width of video. If is 0 or None width will be taken from first image of list
    height: typing.Optional[int], optional
        expected height of video. If is 0 or None height will be taken from first image of list, by default None
    """
    if len(cv2_image_list[0].shape) != 3:
        logging.error("Frames to be written need to be a 3 dimesional numpy array found {}".format(
            len(cv2_image_list[0].shape))
        )
        return
    img_height, img_width = cv2_image_list[0].shape[:2]
    if not width:
        width = img_width
    if not height:
        height = img_height

    out = cv2.VideoWriter(
        output_video_file_path,
        cv2.VideoWriter_fourcc(*"MP4V"),
        int(video_fps),
        (width, height),
    )
    for image in cv2_image_list:
        out.write(image)
    out.release
