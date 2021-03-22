""" This program serves as a unit test for main.py to check if
the global string object called 'filename' in the DataSet class of
main.py exists and has length of 48895.

FileNotFoundError: should be raised if the file referred to by
'filename' does not exist.
DataSet.InvalidDataLength: should be raised if the length of
the file referred to by 'filename' is not 48895.
"""

import unittest
import main as cc


class TestCC(unittest.TestCase):

    def test_file_nonexistent(self):
        """ Test if the file referred to by 'filename' does not
        exist.
        """
        with self.assertRaises(FileNotFoundError):
            cc.filename = './nonexistent_file.csv'
            cc.DataSet().load_file()

    def test_length_of_data(self):
        """ Test if the length of the file referred to by 'filename'
        is not 48895.
        """
        with self.assertRaises(cc.DataSet.InvalidDataLength):
            cc.filename = './AB_NYC_2012.csv'
            cc.DataSet().load_file()


if __name__ == "__main__":
    unittest.main()