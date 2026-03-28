import unittest
import os
from back_end import BackEndSystem


# METHOD 1 TESTS
class TestReadTransactions(unittest.TestCase):

    def test_valid_transaction(self):
        backend = BackEndSystem("old.txt","one_transaction.txt","new.txt","current.txt")
        transactions = backend._read_transactions("one_transaction.txt")
        self.assertTrue(len(transactions) > 0)

    def test_empty_file(self):
        backend = BackEndSystem("old.txt","empty.txt","new.txt","current.txt")
        transactions = backend._read_transactions("empty.txt")
        self.assertEqual(len(transactions), 0)

    def test_missing_fields(self):
        backend = BackEndSystem("old.txt","partial.txt","new.txt","current.txt")
        transactions = backend._read_transactions("partial.txt")
        self.assertTrue(isinstance(transactions, list))

    def test_exception_path(self):
        backend = BackEndSystem("old.txt","does_not_exist.txt","new.txt","current.txt")
        with self.assertRaises(SystemExit):
            backend._read_transactions("does_not_exist.txt")

    def test_short_line(self):
        backend = BackEndSystem("old.txt","short.txt","new.txt","current.txt")
        transactions = backend._read_transactions("short.txt")
        self.assertEqual(len(transactions), 0)


if __name__ == "__main__":
    unittest.main()
