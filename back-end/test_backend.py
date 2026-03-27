import unittest
import os
from back_end import BackEndSystem


# METHOD 1 TESTS
class TestReadTransactions(unittest.TestCase):

    def test_valid_transaction(self):
        backend = BackEndSystem("old.txt","transactions.txt","new.txt","current.txt")
        transactions = backend._read_transactions("transactions.txt")
        self.assertTrue(len(transactions) > 0)

    def test_empty_file(self):
        backend = BackEndSystem("old.txt","empty.txt","new.txt","current.txt")
        transactions = backend._read_transactions("empty.txt")
        self.assertEqual(len(transactions), 0)

    def test_missing_fields(self):
        backend = BackEndSystem("old.txt","partial.txt","new.txt","current.txt")
        transactions = backend._read_transactions("partial.txt")
        self.assertTrue(isinstance(transactions, list))


if __name__ == "__main__":
    unittest.main()
