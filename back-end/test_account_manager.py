import unittest
from account_manager import AccountManager

# METHOD 2 TESTS
class TestApplyAllTransactions(unittest.TestCase):

    def setUp(self):
        self.accounts = [
            {
                "number": "55555",
                "name": "bob",
                "status": "A",
                "balance": 200.00,
                "transactions": 0,
                "plan": "SP"
            }
        ]
        self.manager = AccountManager(self.accounts)

    def test_no_transactions(self):
        transactions = []
        self.manager.apply_all_transactions(transactions)
        self.assertEqual(self.accounts[0]["balance"], 200.00)

    def test_end_session_transaction(self):
        transactions = [{"code": "00"}]
        self.manager.apply_all_transactions(transactions)
        self.assertEqual(self.accounts[0]["balance"], 200.00)

    def test_invalid_transaction(self):
        transactions = [{"code": "99"}]
        self.manager.apply_all_transactions(transactions)
        self.assertEqual(self.accounts[0]["balance"], 200.00)

    def test_valid_transaction(self):
        transactions = [{"code": "04", "number": "55555", "amount": 10.00}]
        self.manager.apply_all_transactions(transactions)
        self.assertTrue(self.accounts[0]["balance"] > 200.00)


if __name__ == "__main__":
    unittest.main()
