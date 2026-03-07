"""
Back End Banking System
-----------------------
Reads the Old Master Bank Accounts File and the Merged Bank Account Transaction File,
applies all transactions, deducts per-transaction fees, and writes the New Master
Bank Accounts File and New Current Bank Accounts File.

Usage:
    python back_end.py <old_master_file> <merged_transaction_file> <new_master_file> <new_current_file>
    
    eg with file structure: winpty python back_end.py old_master.txt ../front-end/source-code/transaction_output.txt new_master.txt new_current.txt

Inputs:
    old_master_file          - Old Master Bank Accounts File (42 chars/line)
    merged_transaction_file  - Merged Bank Account Transaction File (40 chars/line)

Outputs:
    new_master_file          - New Master Bank Accounts File (42 chars/line, sorted by account number)
    new_current_file         - New Current Bank Accounts File (37 chars/line)
"""

import sys
from file_handler import FileHandler
from account_manager import AccountManager


class BackEndSystem:
    """
    Primary orchestrator for the Back End pipeline.
    Coordinates reading inputs, processing transactions, and writing outputs.
    """

    def __init__(self, old_master_file, transaction_file, new_master_file, new_current_file):
        """
        Stores the four file paths needed for the back end pipeline.
        """
        self.old_master_file = old_master_file
        self.transaction_file = transaction_file
        self.new_master_file = new_master_file
        self.new_current_file = new_current_file

    def run(self):
        """
        Executes the full pipeline: load accounts, apply all transactions,
        sort accounts, then write both output files.
        """
        file_handler = FileHandler()

        # Step 1: Load old master accounts
        accounts = file_handler.read_master_accounts(self.old_master_file)

        # Step 2: Load all transactions from merged file
        transactions = file_handler.read_transactions(self.transaction_file)

        # Step 3: Apply transactions and enforce constraints
        manager = AccountManager(accounts)
        manager.apply_all_transactions(transactions)

        # Step 4: Sort accounts by account number (required by spec)
        manager.accounts.sort(key=lambda acc: acc["number"])

        # Step 5: Write both output files
        file_handler.write_master_accounts(manager.accounts, self.new_master_file)
        file_handler.write_current_accounts(manager.accounts, self.new_current_file)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python back_end.py <old_master> <merged_transactions> <new_master> <new_current>")
        sys.exit(1)

    system = BackEndSystem(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    system.run()