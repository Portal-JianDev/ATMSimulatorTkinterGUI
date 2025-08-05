import tkinter as tk
from tkinter import messagebox, simpledialog
import os

# GUI components and logic for the ATM application.
class LoginScreen:
    def __init__(self, atm):
        self.atm = atm
        self.root = atm.root

        tk.Label(self.root, text="¡Bienvenido!", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Ingrese su PIN:").pack()
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.pack()

        tk.Button(self.root, text="Iniciar sesión", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Registrarse", command=self.go_to_register).pack()
    
    # Login: validates the PIN and shows the menu if it's correct.
    def login(self):
        pin = self.pin_entry.get()
        if self.atm.login(pin):
            self.atm.show_menu()
        else:
            messagebox.showerror("Error", "PIN incorrecto")

    # Go to the registration screen.
    def go_to_register(self):
        self.atm.show_register()

# Registration screen for creating a new user account.
class RegisterScreen:
    def __init__(self, atm):
        self.atm = atm
        self.root = atm.root

        tk.Label(self.root, text="Registro de nuevo usuario", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Nombre:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        tk.Label(self.root, text="PIN (4 dígitos):").pack()
        self.pin_entry = tk.Entry(self.root, show="*")
        self.pin_entry.pack()

        tk.Button(self.root, text="Crear cuenta", command=self.register).pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.atm.show_login).pack()

    # Register a new user account.
    def register(self):
        name = self.name_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not name or not pin.isdigit() or len(pin) != 4:
            messagebox.showwarning("Datos inválidos", "Ingrese un nombre y un PIN de 4 dígitos.")
            return

        success = self.atm.register(name, pin)
        if success:
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.atm.show_login()
        else:
            messagebox.showerror("Error", "El PIN ya está en uso. Intente con otro.")

# Main menu screen after successful login.
class MenuScreen:
    def __init__(self, atm):
        self.atm = atm
        self.root = atm.root
        user = atm.current_user

        tk.Label(self.root, text=f"Hola, {user.name}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="Ver saldo", width=20, command=self.view_balance).pack(pady=5)
        tk.Button(self.root, text="Depositar", width=20, command=self.deposit).pack(pady=5)
        tk.Button(self.root, text="Retirar", width=20, command=self.withdraw).pack(pady=5)
        tk.Button(
            self.root, text="Ver transacciones", width=20, command=self.view_transactions
        ).pack(pady=5)
        tk.Button(self.root, text="Cerrar sesión", width=20, command=self.atm.logout).pack(pady=10)

    # Show the current balance of the user.
    def view_balance(self):
        balance = self.atm.current_user.balance
        messagebox.showinfo(
            "Saldo actual", f"Tu saldo es: ${balance:,.0f}".replace(",", ".")
        )

    # Deposit money into the user's account.
    def deposit(self):
        raw_input = simpledialog.askstring(
            "Depósito",
            "Ingrese el monto a depositar (mínimo $10.000, solo números sin puntos):",
        )
        if raw_input is None:
            return

        if not raw_input.isdigit():
            messagebox.showerror(
                "Entrada inválida", "Solo se permiten números enteros sin puntos ni caracteres especiales."
            )
            return

        amount = float(raw_input)
        if amount < 10000:
            messagebox.showwarning(
                "Monto demasiado bajo", "El monto mínimo de depósito es $10.000. Intenta con un valor mayor."
            )
            return

        self.atm.deposit(amount)
        messagebox.showinfo(
            "Éxito", f"Has depositado ${amount:,.0f}".replace(",", ".")
        )
   
    # Withdraw money from the user's account.
    def withdraw(self):
        raw_input = simpledialog.askstring(
            "Retiro",
            "Ingrese el monto a retirar (entre $10.000 y $50.000.000, solo números sin puntos):"
        )
        if raw_input is None:
            return

        if not raw_input.isdigit():
            messagebox.showerror(
                "Entrada inválida",
                "Solo se permiten números enteros sin puntos ni caracteres especiales."
            )
            return

        amount = float(raw_input)
        if amount < 10000:
            messagebox.showwarning(
                "Monto demasiado bajo",
                "El monto mínimo de retiro es $10.000."
            )
            return
        if amount > 50000000:
            messagebox.showwarning(
                "Monto excedido",
                "El monto máximo permitido para retiro es $50.000.000."
            )
            return

        try:
            success = self.atm.withdraw(amount)
            if success:
                messagebox.showinfo(
                    "Éxito",
                    f"Has retirado ${amount:,.0f}".replace(",", ".")
                )
        except ValueError as e:
            messagebox.showwarning("Fondos insuficientes", str(e))

    # View the user's last 10 transactions.
    def view_transactions(self):
        username = self.atm.current_user.name
        log_path = "data/transactions.log"

        if not os.path.exists(log_path):
            messagebox.showinfo("Transacciones", "No hay transacciones registradas.")
            return

        with open(log_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.startswith(username)]

        if not lines:
            messagebox.showinfo(
                "Transacciones", "No hay transacciones registradas para este usuario."
            )
        else:
            history = "\n".join(lines[-10:])  
            messagebox.showinfo("Últimas transacciones", history)