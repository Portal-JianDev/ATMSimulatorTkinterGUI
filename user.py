from transaction import Transaction
import os

# Class representing a user of the ATM.
class User: 
    def __init__(self, name, pin, balance=0.0):
        self._name = name
        self._pin = pin
        self._balance = balance
        self._transactions = []
    
    # Makes a deposit and records the transaction.
    def deposit(self, amount):
        self._balance += amount
        self._add_transaction("DEPÓSITO", amount)
    
    # Makes a withdrawal if there are sufficient funds and records the transaction.
    def withdraw(self, amount):
        if amount > self._balance:
            print("Fondos insuficientes para retirar.")
            return False
        self._balance -= amount
        self._add_transaction("RETIRO", -amount)
        return True
        
    # Adds a transaction to the list and saves it to the file.
    def _add_transaction(self, type, amount):
        t = Transaction(type, amount, self._balance)
        self._transactions.append(t)
        t.save_to_file(self._name)
     
    # Converts the user to a dictionary to save in JSON.        
    def to_dict(self):
        return {
            "name": self._name,
            "pin": self._pin,
            "balance": self._balance
        }
      
    # Property to access the PIN.    
    @property
    def pin(self):
        return self._pin

    # Property to access the name.
    @property
    def name(self):
        return self._name

    # Property to access the balance.
    @property
    def balance(self):
        return self._balance
    
    # Property to access the transactions of the current session.
    @property
    def transactions(self):
        return self._transactions

    # Gets the complete transaction history from the file.
    def get_transaction_history(self):
        log_path = "data/transactions.log"
        if not os.path.exists(log_path):
            return []

        with open(log_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.startswith(self._name)]