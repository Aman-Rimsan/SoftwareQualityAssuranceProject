"""
FileHandler is responsible for all fixed-width file reading and writing
for the Back End. It parses the Master Bank Accounts File and the
Merged Transaction File, and writes both output files in the correct format.
"""


class FileHandler:
    """
    Handles all file I/O for the Back End system using fixed-width parsing
    as defined by the Banking System file format specifications.
    """

    def read_master_accounts(self, filename):
        """
        Reads the Old Master Bank Accounts File and returns a list of account dicts.
        Master file format (42 chars/line): NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT
        Stops reading at the END_OF_FILE sentinel line.
        Logs a fatal error and exits if the file cannot be read.
        """
        accounts = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    if "END_OF_FILE" in line:
                        break
                    if len(line.rstrip("\n")) < 42:
                        print(f"ERROR: Fatal - malformed line in master file '{filename}': {line.rstrip()}")
                        exit(1)

                    number = line[0:5].strip()
                    name = line[6:26].strip()
                    status = line[27]
                    balance = float(line[29:37])
                    transactions = int(line[38:42])

                    accounts.append({
                        "number": number,
                        "name": name,
                        "status": status,
                        "balance": balance,
                        "transactions": transactions,
                        "plan": "SP"  # default plan; updated via changeplan transactions
                    })
        except Exception as e:
            print(f"ERROR: Fatal - could not read master file '{filename}': {e}")
            exit(1)

        return accounts

    def read_transactions(self, filename):
        """
        Reads the Merged Bank Account Transaction File and returns a list of transaction dicts.
        Transaction format (40 chars/line): CC AAAAAAAAAAAAAAAAAAAA NNNNN PPPPPPPP MM
        Reads all lines including end-of-session (00) codes.
        Logs a fatal error and exits if the file cannot be read.
        """
        transactions = []
        try:
            with open(filename, "r") as file:
                for line in file:
                    line = line.rstrip("\n")
                    if len(line) < 2:
                        continue

                    code = line[0:2].strip()
                    name = line[3:23].strip() if len(line) > 3 else ""
                    number = line[24:29].strip() if len(line) > 24 else "00000"
                    amount = float(line[30:38]) if len(line) > 30 else 0.0
                    misc = line[39:41].strip() if len(line) > 39 else ""

                    transactions.append({
                        "code": code,
                        "name": name,
                        "number": number,
                        "amount": amount,
                        "misc": misc
                    })
        except Exception as e:
            print(f"ERROR: Fatal - could not read transaction file '{filename}': {e}")
            exit(1)

        return transactions

    def write_master_accounts(self, accounts, filename):
        """
        Writes the New Master Bank Accounts File in fixed-width format (42 chars/line).
        Format: NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP TTTT
        Appends the END_OF_FILE sentinel at the end.
        """
        with open(filename, "w") as file:
            for acc in accounts:
                line = self._format_master_line(acc)
                file.write(line + "\n")
            # Write END_OF_FILE sentinel
            file.write(f"{'00000'} {'END_OF_FILE'.ljust(20)} {'A'} {'00000.00'} {'0000'}\n")

    def write_current_accounts(self, accounts, filename):
        """
        Writes the New Current Bank Accounts File in fixed-width format (37 chars/line).
        Format: NNNNN AAAAAAAAAAAAAAAAAAAA S PPPPPPPP
        Appends the END_OF_FILE sentinel at the end.
        """
        with open(filename, "w") as file:
            for acc in accounts:
                line = self._format_current_line(acc)
                file.write(line + "\n")
            # Write END_OF_FILE sentinel
            file.write(f"{'00000'} {'END_OF_FILE'.ljust(20)} {'A'} {'00000.00'}\n")

    def _format_master_line(self, acc):
        """
        Formats a single account dict into a 42-character master file line.
        """
        number = str(acc["number"]).zfill(5)
        name = acc["name"].ljust(20)[:20]
        status = acc["status"]
        balance = f"{acc['balance']:08.2f}"
        transactions = str(acc["transactions"]).zfill(4)
        return f"{number} {name} {status} {balance} {transactions}"

    def _format_current_line(self, acc):
        """
        Formats a single account dict into a 37-character current accounts file line.
        """
        number = str(acc["number"]).zfill(5)
        name = acc["name"].ljust(20)[:20]
        status = acc["status"]
        balance = f"{acc['balance']:08.2f}"
        return f"{number} {name} {status} {balance}"