import unittest

# project imports
from amlutils.collections import lists


class TestLists(unittest.TestCase):

    def test_flatten_list(self):
        list_of_lists = [[1, 3, 4], [3, 4, 5], [2, 6, 8]]
        flat_list = lists.flatten_list(list_of_lists)
        self.assertEqual(flat_list, [1, 3, 4, 3, 4, 5, 2, 6, 8])

    def test_chunks(self):
        iterable = range(17)
        counter = 0
        for chunk in lists.chunks_of_list(iterable, 4):
            if counter < 4:
                self.assertEqual(len(chunk), 4)
            else:
                self.assertEqual(len(chunk), 1)
            counter += 1


if __name__ == '__main__':
    unittest.main()
