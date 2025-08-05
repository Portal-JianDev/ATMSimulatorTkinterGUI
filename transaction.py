import datetime
import os

# Class representing a transaction (deposit or withdrawal).
class Transaction:
    def __init__(self, type, amount, final_balance):
        self.type = type
        self.amount = amount
        self.final_balance = final_balance
        self.timestamp = datetime.datetime.now()

    # Text representation of the transaction for display or saving.
    def __str__(self):
        return (
            f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"{self.type} | ${self.amount:,.0f} | Saldo: ${self.final_balance:,.0f}"
        ).replace(",", ".")
    
    # Saves the transaction to a history log file.
    def save_to_file(self, username):
        os.makedirs("data", exist_ok=True)
        with open("data/transactions.log", "a", encoding="utf-8") as f:
            f.write(f"{username} | {self}\n")