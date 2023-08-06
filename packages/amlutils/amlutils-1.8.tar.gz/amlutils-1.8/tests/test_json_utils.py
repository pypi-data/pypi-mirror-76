import numpy as np
import tempfile
import unittest

# project imports
from amlutils import json_utils


class TestJsonUtils(unittest.TestCase):

    def test_store_json(self):
        json_data = [{str(key): str(key) for key in range(10)} for i in range(5)]
        file_path = tempfile.NamedTemporaryFile(suffix=".json").name
        json_utils.store_json_data(file_path, json_data)
        parsed_data = json_utils.parse_json_file(file_path)
        self.assertEqual(json_data, parsed_data)

    def test_store_json_with_numpy_data(self):
        json_data = {
            "np_array": np.array([1, 2, 3]),
            "np_int32": np.int32(4),
            "np_int64": np.int64(4),
        }
        file_path = tempfile.NamedTemporaryFile(suffix=".json").name
        json_utils.store_json_data(file_path, json_data)
        parsed_data = json_utils.parse_json_file(file_path)
        self.assertEqual({"np_array": [1, 2, 3], "np_int32": 4, "np_int64": 4}, parsed_data)


if __name__ == '__main__':
    unittest.main()
