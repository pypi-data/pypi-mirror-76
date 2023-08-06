import tempfile
import unittest

# project imports
from amlutils import csv_utils


class TestCSVUtils(unittest.TestCase):

    def test_store_list_csv(self):
        data = [
            ["col1", "col2", "col3"],
            ["a", "a", 1],
            ["b", "b", 2],
            ["c", "c", 3],
        ]
        file_path = tempfile.NamedTemporaryFile(suffix=".csv").name
        csv_utils.store_list_to_csv(file_path, data)
        parsed_data = csv_utils.parse_csv_file(file_path, has_header=True)
        self.assertEqual([[str(i) for i in row] for row in data[1:]], parsed_data)

        parsed_data = csv_utils.parse_csv_file(file_path)
        self.assertEqual([[str(i) for i in row] for row in data], parsed_data)

    def test_store_dictionary(self):
        expected_data = [
            ["key_1", "key_2", "key_3"],
            ["a", "a", 1],
            ["b", "b", 2],
            ["c", "c", 3],
        ]
        data = [
            {"key_1": "a", "key_2": "a", "key_3": 1},
            {"key_1": "b", "key_2": "b", "key_3": 2},
            {"key_1": "c", "key_2": "c", "key_3": 3},
        ]
        file_path = tempfile.NamedTemporaryFile(suffix=".csv").name
        csv_utils.store_dictionary_to_csv(file_path, data)
        parsed_data = csv_utils.parse_csv_file(file_path)
        self.assertEqual([[str(i) for i in row] for row in expected_data], parsed_data)

        # test only for specific keys
        file_path = tempfile.NamedTemporaryFile(suffix=".csv").name
        csv_utils.store_dictionary_to_csv(file_path, data, headers=["key_1", "key_2"])
        parsed_data = csv_utils.parse_csv_file(file_path)
        self.assertEqual([[str(i) for i in row[:2]] for row in expected_data], parsed_data)


if __name__ == '__main__':
    unittest.main()
