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


# METHOD 2 TESTS
class TestBackendRun(unittest.TestCase):

    def test_run_no_transactions(self):
        backend = BackEndSystem("old_master.txt","empty.txt","new_master.txt","new_current.txt")
        backend.run()
        self.assertTrue(os.path.exists("new_master.txt"))

    def test_run_single_transaction(self):
        backend = BackEndSystem("old_master.txt","one_transaction.txt","new_master.txt","new_current.txt")
        backend.run()
        self.assertTrue(os.path.exists("new_master.txt"))

    def test_run_multiple_transactions(self):
        backend = BackEndSystem("old_master.txt","many_transactions.txt","new_master.txt","new_current.txt")
        backend.run()
        self.assertTrue(os.path.exists("new_master.txt"))

    def test_invalid_transaction(self):
        backend = BackEndSystem("old_master.txt","invalid_transaction.txt","new_master.txt","new_current.txt")
        backend.run()
        self.assertTrue(os.path.exists("new_master.txt"))


if __name__ == "__main__":
    unittest.main()
