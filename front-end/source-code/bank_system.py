"""
Bank System Description:
------------------------
This program is intended to simulate a banking system that processes account transactions.
The program reads from an accounts.txt file and stores account values for the user to use.
Users can log in as a standard user to use standard features like withdrawal, transfer, paybill, and deposit,
while admin users can use privileged features like create, delete, disable, and changeplan.

Input:
------
An accounts.txt file is passed in as a command-line argument.
This file contains all the formatted current bank accounts in the system.
The file ends with an END_OF_FILE string to indicate that all accounts have been read.

Output:
-------
A transaction_file.txt is made at the end of each logout.
This file has records of all the transactions that were made in the session after logging in.
The file ends with a 00 code to indicate there are no more transactions recorded.

How to run the program:
-------------------
To run the program, you'll have to paste this in the terminal:
python bank_system.py accounts.txt
"""
import sys

from bank_operations import BankOperations
from transaction_recorder import TransactionRecorder
"""
The BankSystem class is the primary class that initiates the system and presents a menu to the user.
It reads and stores current accounts in the banking system from a txt file.
Starts the system by asking for a login type (Standard/Admin).
Shows all standard options to standard users and privileged options to admins.
"""
class BankSystem:
    def __init__(self, filename):
        """
        Initialization method that takes in a filename.
        Creates an empty list to store accounts.
        Calls load_accounts to populate empty list with accounts in filename.
        """
        self.accounts = []
        self.load_accounts(filename)

    def load_accounts(self, filename):
        """
        Reads account data from a text file and populates the accounts list.
        Uses fixed-width slicing based on the rubrics file format specification.
        """
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
        """
        The main entry point for the session. Initializes the recorder and operations,
        then enters a loop to handle user login or program termination.
        """
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
        """
        Displays the banking menu based on the user's login mode.
        Routes user input to the specific BankOperations methods and handles session logout.
        """
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