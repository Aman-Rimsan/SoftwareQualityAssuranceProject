class TransactionRecorder:
    def __init__(self):
        self.records = []

    def record(self, code, name = "", acc = "", amount = "00000.00", misc = "  "):
        code = str(code).zfill(2)
        name = name.ljust(20)[:20]
        acc = str(acc).zfill(5)
        amount = f"{float(amount):08.2f}"
        misc = misc.ljust(2)[:2]

        line = f"{code} {name} {acc} {amount} {misc}"
        self.records.append(line)

    def write_transaction_file(self, filename = "transaction_file.txt"):
        with open(filename, "w") as file:
            for line in self.records:
                file.write(line + "\n")

            session_end = f"00 {' '*20} {'00000'} {'00000.00'} {'  '}"
            file.write(session_end + "\n")

        self.records.clear()