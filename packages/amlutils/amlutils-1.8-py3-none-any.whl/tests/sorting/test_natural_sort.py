import unittest

# project imports
from amlutils.sorting import natural_sort


class TestNaturalSort(unittest.TestCase):

    def test_atoi(self):
        string = "101"
        result = natural_sort.atoi(string)
        self.assertEqual(result, int(string))
        self.assertIsInstance(result, int)
        string = "number101"
        self.assertIsInstance(string, str)
        self.assertEqual(string, string)

    def test_natural_keys(self):
        string = "101_filename.jpeg"
        natural_keys = natural_sort.get_natural_keys(string)
        self.assertEqual(
            natural_keys,
            ["", 101, "_filename.jpeg"],
        )
        string = "fileprefix101_filename.jpeg"
        natural_keys = natural_sort.get_natural_keys(string)
        self.assertEqual(
            natural_keys,
            ["fileprefix", 101, "_filename.jpeg"],
        )

    def test_get_natural_sorted_list(self):
        list_of_strings = ["0", "1", "2", "10"]
        self.assertEqual(sorted(list_of_strings), ["0", "1", "10", "2"])

        self.assertEqual(natural_sort.get_natural_sorted_list(list_of_strings), ["0", "1", "2", "10"])


if __name__ == '__main__':
    unittest.main()
