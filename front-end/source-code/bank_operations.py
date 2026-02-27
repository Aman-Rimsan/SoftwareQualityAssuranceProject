"""
The BankOperations class contains the core logic for all banking transactions.
It interacts with the account list to modify balances and uses the 
TransactionRecorder to log every successful action.
"""
class BankOperations:
    def __init__(self, accounts, recorder):
        """
        Initialization method that links the operations to the current accounts list
        and the session's transaction recorder.
        """
        self.accounts = accounts
        self.recorder = recorder
        self.pending_deposits = {}
        self.new_accounts = []

    def find_account(self, name, number):
        """
        Helper method to locate an account dictionary within the accounts list
        based on a matching name and account number. Returns None if not found.
        """
        for acc in self.accounts:
            if acc["name"] == name and acc["number"] == number:
                return acc
        return None
    
    def withdraw(self, name):
        """
        Deducts a specified amount from an active account.
        Logs the transaction with code '01'.
        """
        max_withdrawal = 500
        if name == None:
            name = input("Account holder name: ").strip().lower()
            max_withdrawal = 100000
        number = input("Account number: ").strip()
        amount = float(input("Enter amount to withdraw: "))
        if amount > max_withdrawal:
            print("Withdrawal amount too high!")
            return
        acc = self.find_account(name, number)
        if acc == None:
            print("Invalid account!")
        
        if acc and acc["status"] == "A":
            if amount > acc["balance"]:
                print("Insufficient funds!")
                return
            acc["balance"] -= amount
            self.recorder.record("01", name, number, amount)

    def deposit(self, name):
        """
        Adds a specified amount to an active account balance.
        Logs the transaction with code '04'.
        """
        if name == None:
            name = input("Account holder name: ").strip().lower()
        number = input("Account number: ").strip()
        amount = float(input("Enter amount to deposit: "))
        acc = self.find_account(name, number)
        if acc == None:
            print("Invalid account!")

        if acc and acc["status"] == "A":
            if number not in self.pending_deposits:
                self.pending_deposits[number] = 0
            self.pending_deposits[number] += amount

            self.recorder.record("04", name, number, amount)
    
    def add_pending_deposits(self):
        for acc in self.accounts:
            number = acc["number"]
            if number in self.pending_deposits:
                acc["balance"] += self.pending_deposits[number]

        self.pending_deposits.clear()

    def transfer(self, name):
        """
        Moves funds between two accounts belonging to the same user.
        Logs the transaction with code '02' and includes the target account.
        """
        max_transfer = 1000
        if name == None:
            name = input("Account holder name: ").strip().lower()
            max_transfer = 100000
        from_number = input("Account number to get transfer money: ").strip()
        to_number = input("Account number to send transfer to: ").strip()
        amount = float(input("Enter amount to transfer: "))
        if amount > max_transfer:
            print("Transfer amount too high!")
            return
        from_acc = self.find_account(name, from_number)
        if from_acc == None:
            print("Invalid 'from' account!")
        to_acc = self.find_account(name, to_number)
        if to_acc == None:
            print("Invalid 'to' account!")

        if from_acc and from_acc["status"] == "A" and to_acc and to_acc["status"] == "A":
            if amount > from_acc["balance"]:
                print("Insufficient funds!")
                return
            to_acc["balance"] += amount
            from_acc["balance"] -= amount
            self.recorder.record("02", name, from_number, amount)

    def paybill(self, name):
        """
        Deducts funds to pay a bill to a specific company (EC, CQ, or FI).
        Logs the transaction with code '03'.
        """
        max_request = 2000
        if name == None:
            name = input("Account holder name: ").strip().lower()
            max_request = 100000
        number = input("Account number: ").strip()
        payee = input("Company (EC/CQ/FI): ").strip().upper()
        amount = float(input("Enter amount to pay: "))
        acc = self.find_account(name, number)
        if amount > max_request:
            print("Pay request too high!")
            return

        if payee not in ["EC", "CQ", "FI"]:
            print("Invalid payee!")
            return
        if acc == None:
            print("Invalid account!")

        if acc and acc["status"] == "A":
            if amount > acc["balance"]:
                print("Insufficient funds!")
                return
            acc["balance"] -= amount
            self.recorder.record("03", name, number, amount, payee)

    def create(self):
        """
        Admin-only: Adds a new account to the system with an initial balance.
        Logs the creation with code '05'.
        """
        name = input("Account holder name: ").strip().lower()
        number = input("Account number: ").strip()
        amount = float(input("Initial balance: "))

        for acc in self.accounts:
            num = acc["number"]
            if number == num:
                print("Account number already exists!")
                return

        if len(name) > 20:
            print("Account name is too long!")
            return

        if amount > 99999.99 or amount < 0.00:
            print("Starting balance must be between $99,999.99 and $0.00!")
            return
        
        self.new_accounts.append({"number": number, "name": name, "status": "A", "balance": amount})

        self.recorder.record("05", name, number, amount)

    def add_new_accounts(self):
        for acc in self.new_accounts:
            self.accounts.append(acc)

    def delete(self):
        """
        Admin-only: Removes an existing account from the system list.
        Logs the deletion with code '06'.
        """
        name = input("Account holder name: ").strip().lower()
        number = input("Account number: ").strip()
        acc = self.find_account(name, number)
        if acc == None:
            print("Invalid account!")

        if acc:
            self.accounts.remove(acc)
            self.recorder.record("06", name, number)

    def disable(self):
        """
        Admin-only: Changes an account status to 'Disabled', preventing further transactions.
        Logs the status change with code '07'.
        """
        name = input("Account holder name: ").strip().lower()
        number = input("Account number: ").strip()
        acc = self.find_account(name, number)
        if acc == None:
            print("Invalid account!")

        if acc:
            acc["status"] = "D"
            self.recorder.record("07", name, number)

    def changeplan(self):
        """
        Admin-only: Updates the account's payment plan type from SP (student plan) to NP (non-student plan).
        Logs the change with code '08'.
        """
        name = input("Account holder name: ").strip().lower()
        number = input("Account number: ").strip()
        acc = self.find_account(name, number)

        if acc:
            self.recorder.record("08", name, number)