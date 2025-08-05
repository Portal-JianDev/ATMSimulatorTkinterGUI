import tkinter as tk
from atm import ATM
from persistence import load_users

# Main function of the application.
def main():
    root = tk.Tk()
    root.title("Simulador Cajero Automático")
    root.geometry("400x300")
    
    # Load saved users from the JSON file.
    users = load_users() 
    app = ATM(root, users) 
    
    root.mainloop()  

# Execute the main function if this file is the entry point.
if __name__ == "__main__":
    main()