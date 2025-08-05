from transaction import Transaction
import os

class User: 
    def __init__(self, name, pin, balance=0.0):
        self._name = name
        self._pin = pin
        self._balance = balance
        self._transactions = []
        
    def deposit(self, amount):
        self._balance += amount
        self._add_transaction("DEPÓSITO", amount)
            
    def withdraw(self, amount):
        if amount > self._balance:
            print("Fondos insuficientes para retirar.")
            return False
        self._balance -= amount
        self._add_transaction("RETIRO", -amount)
        return True
        
    def _add_transaction(self, type, amount):
        t = Transaction(type, amount, self._balance)
        self._transactions.append(t)
        t.save_to_file(self._name)
            
    def to_dict(self):
        return {
            "name": self._name,
            "pin": self._pin,
            "balance": self._balance
        }
        
    @property
    def pin(self):
        return self._pin

    @property
    def name(self):
        return self._name

    @property
    def balance(self):
        return self._balance
    
    @property
    def transactions(self):
        return self._transactions

    def get_transaction_history(self):
        log_path = "data/transactions.log"
        if not os.path.exists(log_path):
            return []

        with open(log_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.startswith(self._name)]