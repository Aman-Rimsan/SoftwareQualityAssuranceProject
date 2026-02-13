class BankOperations:
    def __init__(self, accounts, recorder):
        self.accounts = accounts
        self.recorder = recorder

    def find_account(self, name, number):
        for acc in self.accounts:
            if acc["name"] == name and acc["number"] == number:
                return acc
        return None
    
    def withdraw(self, name):
        if name == None:
            name = input("Account holder name: ")
        number = input("Account number: ")
        amount = float(input("Enter amount to withdraw: "))
        acc = self.find_account(name, number)

        if acc and acc["status"] == "A":
            acc["balance"] -= amount
            self.recorder.record("01", name, number, amount)

    def deposit(self, name):
        if name == None:
            name = input("Account holder name: ")
        number = input("Account number: ")
        amount = float(input("Enter amount to deposit: "))
        acc = self.find_account(name, number)

        if acc and acc["status"] == "A":
            acc["balance"] += amount
            self.recorder.record("04", name, number, amount)

    def transfer(self, name):
        if name == None:
            name = input("Account holder name: ")
        from_number = input("Account number to get transfer money: ")
        to_number = input("Account number to send transfer to: ")
        amount = float(input("Enter amount to transfer: "))

        from_acc = self.find_account(name, from_number)
        to_acc = self.find_account(name, to_number)

        if from_acc and from_acc["status"] == "A" and to_acc and to_acc["status"] == "A":
            to_acc["balance"] += amount
            from_acc["balance"] -= amount
            self.recorder.record("02", name, name, from_number, amount, to_number)

    def paybill(self, name):
        if name == None:
            name = input("Account holder name: ")
        number = input("Account number: ")
        payee = input("Company (EC/CQ/FI): ")
        amount = float(input("Enter amount to pay: "))
        acc = self.find_account(name, number)

        if acc and acc["status"] == "A":
            acc["balance"] -= amount
            self.recorder.record("03", name, number, amount, payee)

    def create(self):
        name = input("Account holder name: ")
        number = input("Account number: ")
        amount = float(input("Initial balance: "))

        self.accounts.append({"number": number, "name": name, "status": "A", "balance": amount})

        self.recorder.record("05", name, number, amount)

    def delete(self):
        name = input("Account holder name: ")
        number = input("Account number: ")
        acc = self.find_account(name, number)

        if acc:
            self.accounts.remove(acc)
            self.recorder.record("06", name, number)

    def disable(self):
        name = input("Account holder name: ")
        number = input("Account number: ")
        acc = self.find_account(name, number)

        if acc:
            acc["status"] = "D"
            self.recorder.record("07", name, number)

    def changeplan(self):
        name = input("Account holder name: ")
        number = input("Account number: ")

        self.recorder.record("08", name, number)