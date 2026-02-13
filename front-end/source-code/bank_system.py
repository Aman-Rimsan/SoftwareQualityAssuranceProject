import sys

from bank_operations import BankOperations
from transaction_recorder import TransactionRecorder

class BankSystem:
    def __init__(self, filename):
        self.accounts = []
        self.load_accounts(filename)

    def load_accounts(self, filename):
        with open(filename, "r") as file:
            for line in file:
                if "END_OF_FILE" in line:
                    break

                number = line[0:5]
                name = line[6:26].strip()
                status = line[27]
                balance = float(line[29:37])

                self.accounts.append({"number": number, "name": name, "status": status, "balance": balance})
        print(self.accounts)

    def start_system(self):
        recorder = TransactionRecorder()
        operations = BankOperations(self.accounts, recorder)

        while True:
            print("\n1. Login")
            print("2. Exit")
            option = input("Option number: ")

            if option == "2":
                break

            if option == "1":
                mode = input("Login type (Standard/Admin): ").lower()

                if mode == "standard":
                    account_name = input("Account Holder Name: ")
                else:
                    account_name = None

                self.operations_menu(mode, account_name, operations, recorder)

    def operations_menu(self, mode, account_name, operations, recorder):
        while True:
            print("\n--- Menu ---")
            print("1. Withdraw")
            print("2. Transfer")
            print("3. Paybill")
            print("4. Deposit")
            if mode == "admin":
                print("5. Create")
                print("6. Delete")
                print("7. Disable")
                print("8. Changeplan")
            print("9. Logout")

            option = input("Enter option number: ")
            
            if option == "9":
                recorder.write_transaction_file()
                print("Logged out.\n")
                return
            
            if option == "1":
                operations.withdraw(account_name)

            elif option == "2":
                operations.transfer(account_name)

            elif option == "3":
                operations.paybill(account_name)

            elif option == "4":
                operations.deposit(account_name)

            elif mode == "admin":
                if option == "5":
                    operations.create()

                if option == "6":
                    operations.delete()

                if option == "7":
                    operations.disable()

                if option == "8":
                    operations.changeplan()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bank_system.py accounts.txt")
        sys.exit()

    system = BankSystem(sys.argv[1])
    system.start_system()