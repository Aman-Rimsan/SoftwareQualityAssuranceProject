"""
AccountManager applies all banking transactions to the loaded account list.
It enforces business constraints, deducts per-transaction fees based on account
plan (SP or NP), and logs all constraint violations to the terminal.
"""


class AccountManager:
    """
    Manages the list of bank accounts during Back End processing.
    Routes each transaction code to its handler and enforces constraints.
    """

    STUDENT_FEE = 0.05      # fee per transaction for student plan accounts
    NON_STUDENT_FEE = 0.10  # fee per transaction for non-student plan accounts

    # Maps 2-digit transaction codes to handler method names
    TRANSACTION_HANDLERS = {
        "01": "apply_withdrawal",
        "02": "apply_transfer",
        "03": "apply_paybill",
        "04": "apply_deposit",
        "05": "apply_create",
        "06": "apply_delete",
        "07": "apply_disable",
        "08": "apply_changeplan",
    }

    def __init__(self, accounts):
        """
        Stores the accounts list that will be modified during transaction processing.
        """
        self.accounts = accounts

    def find_account(self, number):
        """
        Returns the account dict matching the given account number, or None if not found.
        """
        for acc in self.accounts:
            if acc["number"] == number:
                return acc
        return None

    def log_error(self, msg):
        """
        Prints a constraint violation or fatal error to the terminal in the required format.
        """
        print(f"ERROR: {msg}")

    def deduct_fee(self, account):
        """
        Deducts the transaction fee from the account based on its plan type.
        SP (student plan): $0.05 per transaction.
        NP (non-student plan): $0.10 per transaction.
        Logs an error if the fee would cause a negative balance.
        """
        fee = self.STUDENT_FEE if account["plan"] == "SP" else self.NON_STUDENT_FEE
        if round(account["balance"] - fee, 2) < 0:
            self.log_error(
                f"Fee deduction of ${fee:.2f} would cause negative balance "
                f"on account {account['number']} ({account['name']}). Fee skipped."
            )
            return
        account["balance"] = round(account["balance"] - fee, 2)
        account["transactions"] += 1

    def apply_all_transactions(self, transactions):
        """
        Iterates through the full transaction list and routes each to its handler.
        Skips end-of-session (00) codes. Logs unknown codes as errors.
        """
        for t in transactions:
            code = t["code"]
            if code == "00":
                continue  # end-of-session marker, nothing to process

            handler_name = self.TRANSACTION_HANDLERS.get(code)
            if handler_name is None:
                self.log_error(f"Unknown transaction code '{code}'. Transaction skipped: {t}")
                continue

            handler = getattr(self, handler_name)
            handler(t)

    def apply_withdrawal(self, t):
        """
        Deducts the transaction amount from the account balance.
        Logs an error if the account is not found or balance would go negative.
        """
        acc = self.find_account(t["number"])
        if acc is None:
            self.log_error(f"Withdrawal failed: account {t['number']} not found. Transaction: {t}")
            return
        if round(acc["balance"] - t["amount"], 2) < 0:
            self.log_error(
                f"Withdrawal failed: would cause negative balance on account "
                f"{t['number']}. Amount: ${t['amount']:.2f}. Transaction: {t}"
            )
            return
        acc["balance"] = round(acc["balance"] - t["amount"], 2)
        self.deduct_fee(acc)

    def apply_transfer(self, t):
        """
        Deducts the transfer amount from the source account.
        Note: the current transaction format does not store the destination account number,
        so only the source account deduction is applied. This is a known format limitation.
        Logs an error if the source account is not found or balance would go negative.
        """
        from_acc = self.find_account(t["number"])
        if from_acc is None:
            self.log_error(f"Transfer failed: source account {t['number']} not found. Transaction: {t}")
            return
        if round(from_acc["balance"] - t["amount"], 2) < 0:
            self.log_error(
                f"Transfer failed: would cause negative balance on account "
                f"{t['number']}. Amount: ${t['amount']:.2f}. Transaction: {t}"
            )
            return
        from_acc["balance"] = round(from_acc["balance"] - t["amount"], 2)
        self.deduct_fee(from_acc)

    def apply_paybill(self, t):
        """
        Deducts the bill payment amount from the account balance.
        Logs an error if the account is not found or balance would go negative.
        """
        acc = self.find_account(t["number"])
        if acc is None:
            self.log_error(f"Paybill failed: account {t['number']} not found. Transaction: {t}")
            return
        if round(acc["balance"] - t["amount"], 2) < 0:
            self.log_error(
                f"Paybill failed: would cause negative balance on account "
                f"{t['number']}. Amount: ${t['amount']:.2f}. Transaction: {t}"
            )
            return
        acc["balance"] = round(acc["balance"] - t["amount"], 2)
        self.deduct_fee(acc)

    def apply_deposit(self, t):
        """
        Adds the deposited amount to the account balance.
        Logs an error if the account is not found.
        """
        acc = self.find_account(t["number"])
        if acc is None:
            self.log_error(f"Deposit failed: account {t['number']} not found. Transaction: {t}")
            return
        acc["balance"] = round(acc["balance"] + t["amount"], 2)
        self.deduct_fee(acc)

    def apply_create(self, t):
        """
        Creates a new account and adds it to the accounts list.
        Logs an error if the account number already exists (constraint violation).
        """
        if self.find_account(t["number"]) is not None:
            self.log_error(
                f"Create failed: account number {t['number']} already exists. Transaction: {t}"
            )
            return
        new_acc = {
            "number": t["number"],
            "name": t["name"],
            "status": "A",
            "balance": t["amount"],
            "transactions": 0,
            "plan": "SP"  # all new accounts start on the student plan
        }
        self.accounts.append(new_acc)

    def apply_delete(self, t):
        """
        Removes the specified account from the accounts list.
        Logs an error if the account is not found.
        """
        acc = self.find_account(t["number"])
        if acc is None:
            self.log_error(f"Delete failed: account {t['number']} not found. Transaction: {t}")
            return
        self.accounts.remove(acc)

    def apply_disable(self, t):
        """
        Sets the account status to disabled (D), preventing further transactions.
        Logs an error if the account is not found.
        """
        acc = self.find_account(t["number"])
        if acc is None:
            self.log_error(f"Disable failed: account {t['number']} not found. Transaction: {t}")
            return
        acc["status"] = "D"
        self.deduct_fee(acc)

    def apply_changeplan(self, t):
        """
        Toggles the account plan between SP (student) and NP (non-student).
        Logs an error if the account is not found.
        """
        acc = self.find_account(t["number"])
        if acc is None:
            self.log_error(f"Changeplan failed: account {t['number']} not found. Transaction: {t}")
            return
        acc["plan"] = "NP" if acc["plan"] == "SP" else "SP"
        self.deduct_fee(acc)