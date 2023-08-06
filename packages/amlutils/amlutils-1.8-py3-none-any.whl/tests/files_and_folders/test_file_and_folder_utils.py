import os
import tempfile
import unittest

# project imports
from amlutils.files_and_folders import (
    file_utils,
    folder_utils,
)


class TestFileAndFolderUtils(unittest.TestCase):

    def _create_file(self, file_path, content):
        with open(file_path, "w") as f:
            f.write(content)

    def test_folder_utils(self):
        temp_folder = tempfile.mkdtemp()
        folder_to_create = os.path.join(temp_folder, "test_directory")

        self.assertFalse(os.path.exists(folder_to_create))
        folder_utils.make_folder_if_not_exists(folder_to_create)
        self.assertTrue(os.path.exists(folder_to_create))

        temp_file_to_create = os.path.join(folder_to_create, "temp_file.txt")
        self._create_file(temp_file_to_create, "TEMPORARY FILE")
        self.assertEqual(len(folder_utils.full_path_for_contents(folder_to_create)), 1)

        # check not deleting existing folder
        folder_utils.make_folder_if_not_exists(folder_to_create)
        self.assertEqual(len(folder_utils.full_path_for_contents(folder_to_create)), 1)

        # check create new folder
        folder_utils.make_folder_if_not_exists(folder_to_create, make_new=True)
        self.assertEqual(len(folder_utils.full_path_for_contents(folder_to_create)), 0)

        # check list folder with different extensions
        num_txt_files = 5
        num_csv_files = 3
        num_jpg_files = 2
        for i in range(num_jpg_files):
            self._create_file(os.path.join(folder_to_create, "{}.jpg".format(i)), "jpeg file")
        for i in range(num_txt_files):
            self._create_file(os.path.join(folder_to_create, "prefix_{}.txt".format(i)), "text file")
        for i in range(num_csv_files):
            self._create_file(os.path.join(folder_to_create, "prefix_{}.csv".format(i)), "csv file")

        self.assertEqual(len(folder_utils.full_path_for_contents(folder_to_create, suffix=".txt")), num_txt_files)
        self.assertEqual(len(folder_utils.full_path_for_contents(folder_to_create, suffix=".csv")), num_csv_files)
        self.assertEqual(
            len(folder_utils.full_path_for_contents(folder_to_create, prefix="prefix_")),
            num_txt_files + num_csv_files,
        )
        self.assertEqual(
            len(folder_utils.full_path_for_contents(folder_to_create, suffix=".csv", prefix="prefix_")),
            num_csv_files,
        )

    def test_file_utils(self):
        temp_folder = tempfile.mkdtemp()
        source_folder = os.path.join(temp_folder, "source_folder")
        destination_folder = os.path.join(temp_folder, "destination_folder")
        folder_utils.make_folder_if_not_exists(source_folder)
        folder_utils.make_folder_if_not_exists(destination_folder)

        files_to_create = 10
        for i in range(files_to_create):
            self._create_file(os.path.join(source_folder, "{}.txt".format(i)), "text file")
        all_files = folder_utils.full_path_for_contents(source_folder)
        files_to_move = all_files[:3]
        file_utils.move_files(files_to_move, destination_folder)
        moved_files = folder_utils.full_path_for_contents(destination_folder)
        files_in_source_folder = folder_utils.full_path_for_contents(source_folder)
        self.assertEqual(len(moved_files), len(files_to_move))
        self.assertEqual(len(files_in_source_folder), len(all_files) - len(files_to_move))

        file_utils.copy_files(files_in_source_folder, destination_folder)
        destination_files = folder_utils.full_path_for_contents(destination_folder)
        files_in_source_folder = folder_utils.full_path_for_contents(source_folder)
        self.assertEqual(len(destination_files), len(all_files))
        self.assertEqual(len(files_in_source_folder), len(all_files) - len(files_to_move))


if __name__ == '__main__':
    unittest.main()
