"""
Back End Banking System
-----------------------
Reads the Old Master Bank Accounts File and the Merged Bank Account Transaction File,
applies all transactions, deducts per-transaction fees, and writes the New Master
Bank Accounts File and New Current Bank Accounts File.

Usage:
    winpty python back_end.py <old_master_file> <merged_transaction_file> <new_master_file> <new_current_file>

    eg with file struct: winpty python back_end.py old_master.txt ../front-end/source-code/transaction_output.txt new_master.txt new_current.txt

    check if fees are working correctly by doing: cat new_master.txt

    eg 2: log in as standard, pick bob with account number 55555, withdraw 5, deposit 5. Switch back to back-end file struct and input cat new_master.txt, the original value in old_master.txt is 

    original:
    11111 amanulla rimsan      A 01500.00 0000 SP
    22222 john smith           A 00500.00 0000 SP
    33333 amanulla rimsan      A 01500.00 0000 SP
    44444 bob                  A 00100.00 0000 SP
    55555 bob                  A 00200.00 0000 SP
    00000 END_OF_FILE          A 00000.00 0000 NP

    after doing example input on bob: 
    00000 END_OF_FILE          A 00000.00 0000 NP
    11111 amanulla rimsan      A 01500.00 0000 SP
    22222 john smith           A 00500.00 0000 SP
    33333 amanulla rimsan      A 01500.00 0000 SP
    44444 bob                  A 00100.00 0000 SP
    55555 bob                  A 00199.90 0002 SP <---- Fee applied, so backend is working
    00000 END_OF_FILE          A 00000.00 0000 NP

Inputs:
    old_master_file          - Old Master Bank Accounts File (45 chars/line)
    merged_transaction_file  - Merged Bank Account Transaction File (40 chars/line)

Outputs:
    new_master_file          - New Master Bank Accounts File (45 chars/line, sorted by account number)
    new_current_file         - New Current Bank Accounts File (39 chars/line)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from read import read_old_bank_accounts
from write import write_new_current_accounts
from print_error import log_constraint_error
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
        # Step 1: Load accounts
        accounts = read_old_bank_accounts(self.old_master_file)

        #Remove ALL existing END_OF_FILE entries
        accounts = [acc for acc in accounts if acc["account_number"] != "00000"]

        # Step 2: Read transactions
        transactions = self._read_transactions(self.transaction_file)

        # Step 3: Apply transactions
        manager = AccountManager(accounts)
        manager.apply_all_transactions(transactions)

        # Step 4: Sort
        manager.accounts.sort(key=lambda acc: acc["account_number"].zfill(5))

        # Step 5: Write files (ONLY this adds END_OF_FILE)
        # Remove ANY leftover END_OF_FILE before writing
        manager.accounts = [
            acc for acc in manager.accounts if acc["account_number"] != "00000"
        ]
        self._write_master_accounts(manager.accounts, self.new_master_file)
        write_new_current_accounts(manager.accounts, self.new_current_file)

    def _read_transactions(self, filename):
        """
        Reads the Merged Bank Account Transaction File and returns a list of transaction dicts.
        Transaction format (40 chars/line): CC AAAAAAAAAAAAAAAAAAAA NNNNN PPPPPPPP MM
        Logs a fatal error and exits if the file cannot be read.
        """
        transactions = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.rstrip("\n")

                    if len(line) < 40:
                        continue

                    code = line[0:2].strip()
                    name = line[3:23].strip()
                    number = line[24:29].strip()

                    try:
                        amount = float(line[30:38])
                    except:
                        amount = 0.0

                    misc = line[39:41].strip()

                    transactions.append({
                        "code": code,
                        "name": name,
                        "account_number": number,
                        "amount": amount,
                        "misc": misc
                    })

        except Exception as e:
            log_constraint_error(str(e), filename, fatal=True)
            exit(1)

        return transactions

    def _write_master_accounts(self, accounts, filename):
        """
        Writes the New Master Bank Accounts File in fixed-width format (45 chars/line).
        Format: NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT SP/NP
        Appends the END_OF_FILE sentinel at the end.
        """
        with open(filename, "w") as file:
            for acc in accounts:
                number = acc["account_number"].zfill(5)
                name = acc["name"].ljust(20)[:20]
                status = acc["status"]
                balance = f"{acc['balance']:08.2f}"
                transactions = str(acc["total_transactions"]).zfill(4)
                plan = acc.get("plan", "SP")
                file.write(f"{number} {name} {status} {balance} {transactions} {plan}\n")

            file.write("00000 END_OF_FILE          A 00000.00 0000 NP\n")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python back_end.py <old_master> <merged_transactions> <new_master> <new_current>")
        sys.exit(1)

    system = BackEndSystem(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    system.run()

