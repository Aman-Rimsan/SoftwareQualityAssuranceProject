"""
The TransactionRecorder class handles the logging of all banking activities.
It maintains an internal list of transaction strings and writes them to a 
formatted text file upon logout.
"""
class TransactionRecorder:
    def __init__(self):
        """
        Initialization method that creates an empty list to store formatted 
        transaction strings for the duration of the session.
        """
        self.records = []

    def record(self, code, name = "", acc = "", amount = "00000.00", misc = "  "):
        """
        Formats and stores a single transaction line. 
        Uses padding and specific widths to match the banking system requirements:
        - code: 2-digit transaction code
        - name: 20-character account holder name
        - acc: 5-digit account number
        - amount: 8-character string (00000.00 format)
        - misc: 2-character miscellaneous field
        """
        code = str(code).zfill(2)
        name = name.ljust(20)[:20]
        acc = str(acc).zfill(5)
        amount = f"{float(amount):08.2f}"
        misc = misc.ljust(2)[:2]

        line = f"{code} {name} {acc} {amount} {misc}"
        self.records.append(line)

    def write_transaction_file(self, filename = "transaction_file.txt"):
        """
        Writes all recorded transactions to a text file (default: transaction_file.txt).
        Adds a '00' terminal code at the end of the file to signify the end of the session.
        Clears the internal records list after writing.
        """
        with open(filename, "w") as file:
            for line in self.records:
                file.write(line + "\n")

            session_end = f"00 {' '*20} {'00000'} {'00000.00'} {'  '}"
            file.write(session_end + "\n")

        self.records.clear()