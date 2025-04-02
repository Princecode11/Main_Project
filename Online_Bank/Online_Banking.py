import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


# Define Account class
class Account:
    def __init__(self, acc_no, name, address, phone, amt=0.0):
        self.acc_no = acc_no
        self.name = name
        self.address = address
        self.phone = phone
        self.amt = amt

    def to_dict(self):
        return {
            "acc_no": self.acc_no,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "amt": self.amt
        }

    @staticmethod
    def from_dict(data):
        return Account(data['acc_no'], data['name'], data['address'], data['phone'], data['amt'])


# File to store account data
data_file = "accounts.json"


# Load data from the JSON file
def load_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            data = json.load(file)
            return [Account.from_dict(acc) for acc in data]
    return []


# Save data to the JSON file
def save_data(accounts):
    with open(data_file, "w") as file:
        json.dump([acc.to_dict() for acc in accounts], file, indent=4)


# Function to switch the view
def switch_view(view):
    for widget in content_frame.winfo_children():
        widget.destroy()
    view()


# Function to create a new account
def create_account():
    def save_account():
        acc_no = acc_no_entry.get()
        name = name_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()
        amt = float(amt_entry.get())

        accounts = load_data()
        if any(acc.acc_no == acc_no for acc in accounts):
            messagebox.showwarning("Account Exists", "This account number already exists.")
            return

        new_account = Account(acc_no, name, address, phone, amt)
        accounts.append(new_account)
        save_data(accounts)
        messagebox.showinfo("Success", "Account created successfully.")

    tk.Label(content_frame, text="Create Account", font=("Arial", 16), fg="white", bg="#1a1a2e").pack()
    tk.Label(content_frame, text="Account Number:", fg="white", bg="#1a1a2e").pack()
    acc_no_entry = tk.Entry(content_frame, bg="black", fg="white")
    acc_no_entry.pack()
    tk.Label(content_frame, text="Name:", fg="white", bg="#1a1a2e").pack()
    name_entry = tk.Entry(content_frame, bg="black", fg="white")
    name_entry.pack()
    tk.Label(content_frame, text="Address:", fg="white", bg="#1a1a2e").pack()
    address_entry = tk.Entry(content_frame, bg="black", fg="white")
    address_entry.pack()
    tk.Label(content_frame, text="Phone:", fg="white", bg="#1a1a2e").pack()
    phone_entry = tk.Entry(content_frame, bg="black", fg="white")
    phone_entry.pack()
    tk.Label(content_frame, text="Initial Deposit:", fg="white", bg="#1a1a2e").pack()
    amt_entry = tk.Entry(content_frame, bg="black", fg="white")
    amt_entry.pack()
    tk.Button(content_frame, text="Save", command=save_account, bg="#e94560", fg="white").pack()


# Function to view accounts
def view_accounts():
    tk.Label(content_frame, text="Accounts List", font=("Arial", 16), fg="white", bg="#1a1a2e").pack()
    accounts = load_data()
    if not accounts:
        tk.Label(content_frame, text="No accounts found.", fg="white", bg="#1a1a2e").pack()
        return
    for acc in accounts:
        tk.Label(content_frame, text=f"{acc.acc_no} - {acc.name} - ${acc.amt}", fg="white", bg="#1a1a2e").pack()


# Function to edit an account
def edit_account():
    def save_changes():
        acc_no = acc_no_entry.get()
        accounts = load_data()
        account = next((acc for acc in accounts if acc.acc_no == acc_no), None)

        if account:
            account.address = address_var.get()
            account.phone = phone_var.get()
            save_data(accounts)
            messagebox.showinfo("Success", "Account updated successfully.")
        else:
            messagebox.showwarning("Error", "Account not found.")

    tk.Label(content_frame, text="Edit Account", font=("Arial", 16), fg="white", bg="#1a1a2e").pack()
    tk.Label(content_frame, text="Enter Account Number:", fg="white", bg="#1a1a2e").pack()
    acc_no_entry = tk.Entry(content_frame, bg="black", fg="white")
    acc_no_entry.pack()
    tk.Label(content_frame, text="New Address:", fg="white", bg="#1a1a2e").pack()
    address_var = tk.StringVar()
    address_entry = tk.Entry(content_frame, textvariable=address_var, bg="black", fg="white")
    address_entry.pack()
    tk.Label(content_frame, text="New Phone:", fg="white", bg="#1a1a2e").pack()
    phone_var = tk.StringVar()
    phone_entry = tk.Entry(content_frame, textvariable=phone_var, bg="black", fg="white")
    phone_entry.pack()
    tk.Button(content_frame, text="Save Changes", command=save_changes, bg="#e94560", fg="white").pack()


# Function to delete an account
def delete_account():
    def delete():
        acc_no = acc_no_entry.get()
        accounts = load_data()
        accounts = [acc for acc in accounts if acc.acc_no != acc_no]
        save_data(accounts)
        messagebox.showinfo("Success", "Account deleted successfully.")

    tk.Label(content_frame, text="Delete Account", font=("Arial", 16), fg="white", bg="#1a1a2e").pack()
    tk.Label(content_frame, text="Enter Account Number:", fg="white", bg="#1a1a2e").pack()
    acc_no_entry = tk.Entry(content_frame, bg="black", fg="white")
    acc_no_entry.pack()
    tk.Button(content_frame, text="Delete", command=delete, bg="#e94560", fg="white").pack()


# Function to deposit/withdraw
def transact():
    def process_transaction():
        acc_no = acc_no_entry.get()
        amount = float(amount_entry.get())
        accounts = load_data()
        account = next((acc for acc in accounts if acc.acc_no == acc_no), None)

        if account:
            if trans_choice.get() == 1:
                account.amt += amount
            elif trans_choice.get() == 2 and account.amt >= amount:
                account.amt -= amount
            else:
                messagebox.showwarning("Error", "Insufficient funds.")
                return
            save_data(accounts)
            messagebox.showinfo("Success", "Transaction successful.")
        else:
            messagebox.showwarning("Error", "Account not found.")

    tk.Label(content_frame, text="Deposit/Withdraw", font=("Arial", 16), fg="white", bg="#1a1a2e").pack()
    tk.Label(content_frame, text="Enter Account Number:", fg="white", bg="#1a1a2e").pack()
    acc_no_entry = tk.Entry(content_frame, bg="black", fg="white")
    acc_no_entry.pack()
    tk.Label(content_frame, text="Transaction Amount:", fg="white", bg="#1a1a2e").pack()
    amount_entry = tk.Entry(content_frame, bg="black", fg="white")
    amount_entry.pack()
    trans_choice = tk.IntVar()
    tk.Radiobutton(content_frame, text="Deposit", variable=trans_choice, value=1, fg="white", bg="#1a1a2e").pack()
    tk.Radiobutton(content_frame, text="Withdraw", variable=trans_choice, value=2, fg="white", bg="#1a1a2e").pack()
    tk.Button(content_frame, text="Process", command=process_transaction, bg="#e94560", fg="white").pack()



# Main window setup
window = tk.Tk()
window.title("Bank Account Management System")
window.geometry("900x600")
window.configure(bg="#1a1a2e")

header = tk.Label(window, text="Bank Account Management System", font=("Arial", 20, "bold"), bg="#0f3460", fg="white",
                  pady=10)
header.pack(fill=tk.X)

frame = tk.Frame(window, bg="#1a1a2e")
frame.pack(side=tk.LEFT, fill=tk.Y)

content_frame = tk.Frame(window, bg="#1a1a2e")
content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

buttons = [
    ("Create Account", lambda: switch_view(create_account)),
    ("View Accounts", lambda: switch_view(view_accounts)),
    ("Edit Account", lambda: switch_view(edit_account)),
    ("Delete Account", lambda: switch_view(delete_account)),
    ("Deposit/Withdraw", lambda: switch_view(transact))
]

for text, command in buttons:
    tk.Button(frame, text=text, command=command, font=("Arial", 14), bg="#e94560", fg="white", padx=20, pady=10,
              borderwidth=0, width=20).pack(pady=10)

window.mainloop()
