import pandas as pd
import string
import os
import sys
import re


class SimpleBank:
    def __init__(self) -> None:
        self.file_name = "record.csv"
        self.rule = "^(0|\+?[1-9][0-9]*)$"
        # If there is no CSV file, create
        try:
            self.data = pd.read_csv(self.file_name).to_dict(orient="records")
        except FileNotFoundError:
            self.data = pd.DataFrame([{"account": None, "balance": None}]).dropna()
            self.data.to_csv(self.file_name, index=False)
            self.data = self.data.to_dict(orient="records")
        self.data: dict = {_["account"]: _["balance"] for _ in self.data}
        self.account = None

    @staticmethod
    def clear():
        """
        Clear command line
        """
        os.system("cls" if os.name == "nt" else "clear")

    def amount_verification(self, slogan: str):
        number = input(slogan)
        match = re.match(self.rule, number)
        while match is None:
            number = input(slogan)
            match = re.match(self.rule, number)
        return int(match.group())

    def update_balance(self, account, balance, op):
        if "deposit" == op:
            self.data[account] += balance
        elif "withdraw" == op:
            self.data[account] -= balance
        else:
            raise RuntimeError("System Error")

    def account_info(self):
        print(
            "Current account: {}\nCurrent balance: {}".format(
                self.account, self.data[self.account]
            )
        )

    def create_account(self):
        self.clear()
        self.rule = "^(0|\+?[1-9][0-9]*)$"
        self.account = input("Enter Account: ")
        while self.account in self.data:
            print("Account Has Been Registered")
            self.account = input("Enter Account: ")
        starting_balance = self.amount_verification(slogan="Enter Starting Balance: ")
        self.data[self.account] = starting_balance
        self.clear()
        self.account_info()
        self.save()
        self.operation()

    def login_account(self):
        self.clear()
        all_account = list(self.data.keys())
        target = input("Enter Account: ")
        while target not in all_account:
            print("No Such Account Found")
            target = input("Enter Account: ")
        self.account = target
        self.clear()
        self.account_info()
        self.operation()

    def operation(self):
        self.clear()
        self.account_info()
        select = input(
            "Enter deposit -- 1, withdraw -- 2 transfer -- 3, exit the system for others\n"
        )
        if select not in ("1", "2", "3"):
            sys.exit()
        if "1" == select:
            self.deposit()
        elif "2" == select:
            self.withdraw()
        elif "3" == select:
            self.transfer()
        else:
            raise RuntimeError("System Error")

    def deposit(self):
        self.clear()
        self.account_info()
        amount = self.amount_verification("Enter Deposit Amount: ")
        self.update_balance(self.account, amount, op="deposit")
        self.save()
        self.operation()

    def withdraw(self):
        self.clear()
        self.account_info()
        amount = self.amount_verification("Enter Withdraw Amount: ")
        while self.data[self.account] < amount:
            print("Not Allowed To Overdraft")
            amount = self.amount_verification("Enter Withdraw Amount: ")
        self.update_balance(self.account, amount, op="withdraw")
        self.save()
        self.operation()

    def transfer(self):
        self.clear()
        self.account_info()
        all_account = list(self.data.keys())
        amount = self.amount_verification("Enter Transfer Amount: ")
        while self.data[self.account] < amount:
            print("Not Allowed To Overdraft")
            amount = self.amount_verification("Enter Transfer Amount: ")
        target = input("Enter Payee Account: ")
        while target not in all_account:
            print("No Such Account Found")
            target = input("Enter Payee Account: ")
        self.update_balance(self.account, amount, op="withdraw")
        self.update_balance(target, amount, op="deposit")
        self.save()
        self.operation()

    def save(self):
        """
        Save to CSV file to records system state
        """
        pack = [{"account": k, "balance": v} for k, v in self.data.items()]
        pd.DataFrame(pack).to_csv(self.file_name, index=False)

    def run(self):
        select = 0
        print("Add an account -- 1 Login an account -- 2")
        while select not in (1, 2):
            select = input("1 or 2\n")
            if select not in string.digits:
                continue
            select = int(select)
        # Add an account
        if 1 == select:
            self.create_account()
        # Login an account
        elif 2 == select:
            self.login_account()
        else:
            raise RuntimeError("System Error")


def main():
    simple_bank = SimpleBank()
    simple_bank.run()

if "__main__" == __name__:
    main()
