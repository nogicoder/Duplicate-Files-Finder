from find_duplicate_files import *
from subprocess import run, PIPE
from os.path import getsize
from os import chdir
import unittest


class MainTest(unittest.TestCase):

    def setUp(self):
        """
        Setting up the test directory and expected result
        The generate_duplicate_files2.py will create an expected
        test directory.
        """
        run('python3 generate_duplicate_files2.py', shell=True)
        self.sample_list = [
                  '/home/mbach/mbach/duplicates/file1',
                  '/home/mbach/mbach/duplicates/file2']
        self.file_path_names = [
                  '/home/mbach/mbach/duplicates/dir4/test2x',
                  '/home/mbach/mbach/duplicates/dir5/test2xx',
                  '/home/mbach/mbach/duplicates/dir5/dir6/test3',
                  '/home/mbach/mbach/duplicates/dir1/test1',
                  '/home/mbach/mbach/duplicates/dir1/dir2/test1x',
                  '/home/mbach/mbach/duplicates/dir1/dir2/dir3/test2']
        self.result = [
                  ["/home/mbach/mbach/duplicates/dir1/test1",
                   "/home/mbach/mbach/duplicates/dir1/dir2/test1x"],
                  ["/home/mbach/mbach/duplicates/dir4/test2x",
                   "/home/mbach/mbach/duplicates/dir5/test2xx",
                   "/home/mbach/mbach/duplicates/dir1/dir2/dir3/test2"]]

    def tearDown(self):
        """
        Remove the test files after each test
        """
        run('rm -rf duplicates/', shell=True)

    def test_get_file_paths(self):
        """
        Test if each file has its correct absolute path and is added to
        the list.
        """
        root = 'duplicates/'
        file_list = ['file1', 'file2']
        files = get_file_paths(root, file_list)
        self.assertEqual(files, self.sample_list)

    def test_scan_files(self):
        """
        Test if all the files is included in the return result.
        """
        root = 'duplicates/'
        files = sorted(scan_files(root))
        for file in self.file_path_names:
            self.assertIn(file, files)

    def test_create_size_dict(self):
        """
        Test if the empty file is not included in the result.
        """
        size_dict = create_size_dict(self.file_path_names)
        empty_file = '/home/mbach/mbach/duplicates/dir5/dir6/emptyfile.txt'
        self.assertNotIn(empty_file, size_dict.values())

    def test_group_files_by_size1(self):
        """
        Test if the list has at least 2 items.
        """
        size_list = group_files_by_size(self.file_path_names)
        for list in size_list:
            self.assertTrue(len(list) > 2)

    def test_group_files_by_size2(self):
        """
        Test if every file in a group has the same size.
        """
        size_list = group_files_by_size(self.file_path_names)
        for list in size_list:
            size = getsize(list[0])
            for file in list:
                self.assertEqual(size, getsize(file))

    def test_get_file_checksum(self):
        """
        Test if the hash is returned in 2 cases:
        + Return the right hash
        + Return None if file is not readable
        """
        empty_file = '/home/mbach/mbach/duplicates/dir5/dir6/emptyfile.txt'
        file_hash = get_file_checksum(empty_file)
        hash = 'd41d8cd98f00b204e9800998ecf8427e'
        self.assertEqual(file_hash, hash)
        no_read_file = open('no_read.txt', 'w+')
        run('chmod -r no_read.txt', shell=True)
        file_hash2 = get_file_checksum('no_read.txt')
        self.assertEqual(file_hash2, None)
        run('rm -rf no_read.txt', shell=True)

    def test_create_hash_dict(self):
        """
        Test if the empty file is not in the dict's values.
        """
        temp = self.file_path_names
        empty_file = '/home/mbach/mbach/duplicates/dir5/dir6/emptyfile.txt'
        temp.append(empty_file)
        hash_dict = create_hash_dict(temp)
        self.assertNotIn(empty_file, hash_dict.values())

    def test_group_files_by_checksum(self):
        """
        Test if each item in a list has the same checksum.
        """
        hash_list = group_files_by_checksum(self.file_path_names)
        for list in hash_list:
            hash = get_file_checksum(list[0])
            for file in list:
                self.assertEqual(hash, get_file_checksum(file))

    def test_find_duplicate_files(self):
        """
        Test if the final result is the same as the expected result
        by comparing items inside each list.
        """
        groups = find_duplicate_files(self.file_path_names)
        test_result = []
        for list1 in groups:
            for file1 in list1:
                test_result.append(file1)
        expect_result = []
        for list2 in self.result:
            for file2 in list2:
                expect_result.append(file2)
        self.assertEqual(sorted(test_result), sorted(expect_result))


if __name__ == '__main__':
    unittest.main()
