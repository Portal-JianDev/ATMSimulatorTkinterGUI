import tkinter as tk
from atm import ATM
from persistence import load_users

def main():
    root = tk.Tk()
    root.title("Simulador Cajero Automático")
    root.geometry("400x300")
    
    users = load_users() 
    app = ATM(root, users) 
    
    root.mainloop()  

if __name__ == "__main__":
    main()