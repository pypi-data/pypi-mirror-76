import cv2
import numpy as np
import os
import tempfile
import unittest

# project imports
import amlutils.video.utils as video_utils


class TestVideoUtis(unittest.TestCase):

    def test_video_write_read(self):
        num_video_frames = 60
        frame_height, frame_width, channels = (300, 300, 3)
        video_frames = [
            np.random.randint(low=0, high=255, size=(frame_height, frame_width, channels), dtype=np.uint8)
            for i in range(num_video_frames)
        ]
        file_path = tempfile.NamedTemporaryFile(suffix=".mp4").name
        video_utils.write_to_video(video_frames, file_path, video_fps=6)

        cv2_video = cv2.VideoCapture(file_path)
        self.assertEqual(int(cv2_video.get(cv2.CAP_PROP_FPS)), 6)
        self.assertEqual(int(cv2_video.get(cv2.CAP_PROP_FRAME_COUNT)), num_video_frames)

        extraction_directory = tempfile.mkdtemp()
        extraction_info = video_utils.ExtractionInfo(file_path, extraction_directory, 1)
        video_utils.extract_frames_from_video(extraction_info)
        extracted_frame_paths = os.listdir(extraction_directory)
        self.assertEqual(len(extracted_frame_paths), 10)    # 10 second video length at 1 fps


if __name__ == '__main__':
    unittest.main()
