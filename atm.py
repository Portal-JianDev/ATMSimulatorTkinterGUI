from gui_components import LoginScreen, MenuScreen, RegisterScreen
from persistence import save_users

# Main class of the ATM application.
class ATM:
    def __init__(self, root, users):
        self.root = root
        self.users = users
        self.current_user = None

        self.current_screen = None
        self.show_login()

    # Shows the login screen.
    def show_login(self):
        self._clear_screen()
        self.current_screen = LoginScreen(self)

    # Shows the main menu screen.
    def show_menu(self):
        self._clear_screen()
        self.current_screen = MenuScreen(self)

    # Shows the registration screen.
    def show_register(self):
        self._clear_screen()
        self.current_screen = RegisterScreen(self)

    # Handles user login.
    def login(self, pin):
        for user in self.users:
            if user.pin == pin:
                self.current_user = user
                return True
        return False

    # Handles registration of new users.
    def register(self, name, pin):
        if any(user.pin == pin for user in self.users):
            return False
        from user import User
        new_user = User(name, pin)
        self.users.append(new_user)
        save_users(self.users)
        return True

    # Handles logout.
    def logout(self):
        save_users(self.users)
        self.current_user = None
        self.show_login()
        
    # Handles deposits.   
    def deposit(self, amount):
        if not self.current_user:
            raise ValueError("No hay un usuario conectado actualmente.")
        if amount <= 0:
            raise ValueError("El monto del depósito debe ser positivo.")
        self.current_user.deposit(amount)
        save_users(self.users)
           
    # Handles withdrawals.     
    def withdraw(self, amount):
        if not self.current_user:
            raise ValueError("No hay un usuario conectado actualmente.")
        if amount <= 0:
            raise ValueError("El monto del retiro debe ser positivo.")
        success = self.current_user.withdraw(amount)
        if success:
            save_users(self.users)
            return success
        raise ValueError("Fondos insuficientes para realizar el retiro.")

    # Clears the current screen's elements.
    def _clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()