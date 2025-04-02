import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import matplotlib.pyplot as plt

# JSON Database File
DATA_FILE = "finance_data.json"


def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"transactions": [], "budget": {}}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


data = load_data()


class FinanceManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.root.geometry("600x600")

        self.dark_mode = False  # Dark mode flag

        # Title Label
        ttk.Label(root, text="Personal Finance Manager", font=("Arial", 16, "bold")).pack(pady=10)

        # Amount Input
        ttk.Label(root, text="Amount:").pack()
        self.amount_entry = ttk.Entry(root)
        self.amount_entry.pack(pady=5)

        # Category Input
        ttk.Label(root, text="Category:").pack()
        self.category_entry = ttk.Entry(root)
        self.category_entry.pack(pady=5)

        # Date Input
        ttk.Label(root, text="Date:").pack()
        self.date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

        # Type Selection
        self.type_var = tk.StringVar()
        ttk.Radiobutton(root, text="Income", variable=self.type_var, value="Income").pack()
        ttk.Radiobutton(root, text="Expense", variable=self.type_var, value="Expense").pack()

        # Add Transaction Button
        ttk.Button(root, text="Add Transaction", command=self.add_transaction).pack(pady=10)

        # Budget Alert Button
        ttk.Button(root, text="Set Category Budget", command=self.set_budget).pack(pady=5)

        # Balance and Chart Buttons
        ttk.Button(root, text="Show Balance", command=self.show_balance).pack(pady=5)
        ttk.Button(root, text="Show Expense Chart", command=self.show_chart).pack(pady=5)
        ttk.Button(root, text="Export to CSV", command=self.export_csv).pack(pady=5)
        ttk.Button(root, text="Toggle Dark Mode", command=self.toggle_dark_mode).pack(pady=5)

        # Delete and Edit Buttons
        ttk.Button(root, text="Delete Transaction", command=self.delete_transaction).pack(pady=5)
        ttk.Button(root, text="Edit Transaction", command=self.edit_transaction).pack(pady=5)

        # Transactions List
        self.transactions_list = tk.Listbox(root, height=10)
        self.transactions_list.pack(pady=10, fill=tk.BOTH, expand=True)
        self.load_transactions()

    def add_transaction(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        trans_type = self.type_var.get()
        date = self.date_entry.get()

        if not amount or not category or not trans_type:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        try:
            amount = float(amount)
            data["transactions"].append({"amount": amount, "category": category, "type": trans_type, "date": date})
            save_data(data)
            self.transactions_list.insert(tk.END, f"{trans_type}: {category} - {amount:,.0f} Rwf on {date}")
            self.check_budget_alert(category)
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount!")

    def show_balance(self):
        income = sum(t["amount"] for t in data["transactions"] if t["type"] == "Income")
        expense = sum(t["amount"] for t in data["transactions"] if t["type"] == "Expense")
        balance = income - expense
        messagebox.showinfo("Balance", f"Total Income: {income:,.0f} Rwf\nTotal Expense: {expense:,.0f} Rwf\nBalance: {balance:,.0f} Rwf")

    def show_chart(self):
        expenses = [t for t in data["transactions"] if t["type"] == "Expense"]
        if not expenses:
            messagebox.showinfo("No Data", "No expense data to display!")
            return

        categories = {}
        for t in expenses:
            categories[t["category"]] = categories.get(t["category"], 0) + t["amount"]

        plt.figure(figsize=(6, 4))
        plt.bar(categories.keys(), categories.values(), color="red")
        plt.xlabel("Categories")
        plt.ylabel("Amount Spent (Rwf)")
        plt.title("Expenses by Category")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def export_csv(self):
        import csv
        with open("transactions.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Category", "Amount (Rwf)", "Date"])
            for t in data["transactions"]:
                writer.writerow([t["type"], t["category"], t["amount"], t["date"]])
        messagebox.showinfo("Export Successful", "Transactions exported to transactions.csv")

    def set_budget(self):
        category = self.category_entry.get()
        budget = self.amount_entry.get()

        if not category or not budget:
            messagebox.showwarning("Warning", "Enter category and budget amount!")
            return

        try:
            data["budget"][category] = float(budget)
            save_data(data)
            messagebox.showinfo("Success", f"Budget set for {category}: {float(budget):,.0f} Rwf")
        except ValueError:
            messagebox.showerror("Error", "Invalid budget amount!")

    def check_budget_alert(self, category):
        if category in data["budget"]:
            total_spent = sum(
                t["amount"] for t in data["transactions"] if t["category"] == category and t["type"] == "Expense")
            if total_spent > data["budget"][category]:
                messagebox.showwarning("Budget Exceeded", f"You have exceeded the budget for {category}!")

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.root.configure(bg="black" if self.dark_mode else "white")

    def load_transactions(self):
        self.transactions_list.delete(0, tk.END)
        for trans in data["transactions"]:
            self.transactions_list.insert(tk.END,
                                          f"{trans['type']}: {trans['category']} - {trans['amount']:,.0f} Rwf on {trans['date']}")

    def delete_transaction(self):
        try:
            selected_index = self.transactions_list.curselection()[0]
            selected_transaction = data["transactions"][selected_index]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this transaction?\n{selected_transaction}")
            if confirm:
                del data["transactions"][selected_index]
                save_data(data)
                self.load_transactions()
                messagebox.showinfo("Success", "Transaction deleted successfully.")
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a transaction to delete.")

    def edit_transaction(self):
        try:
            selected_index = self.transactions_list.curselection()[0]
            selected_transaction = data["transactions"][selected_index]

            # Pre-fill current transaction data
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, selected_transaction["amount"])

            self.category_entry.delete(0, tk.END)
            self.category_entry.insert(0, selected_transaction["category"])

            self.date_entry.set_date(selected_transaction["date"])
            self.type_var.set(selected_transaction["type"])

            # Remove the old transaction and wait for new input
            def save_edited_transaction():
                amount = self.amount_entry.get()
                category = self.category_entry.get()
                trans_type = self.type_var.get()
                date = self.date_entry.get()

                if not amount or not category or not trans_type:
                    messagebox.showwarning("Warning", "Please fill all fields!")
                    return

                try:
                    amount = float(amount)
                    data["transactions"][selected_index] = {"amount": amount, "category": category, "type": trans_type, "date": date}
                    save_data(data)
                    self.load_transactions()
                    messagebox.showinfo("Success", "Transaction edited successfully.")
                except ValueError:
                    messagebox.showerror("Error", "Invalid amount!")

            # Save edited transaction
            edit_button = ttk.Button(self.root, text="Save Edited Transaction", command=save_edited_transaction)
            edit_button.pack(pady=5)

        except IndexError:
            messagebox.showwarning("No Selection", "Please select a transaction to edit.")


# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceManager(root)
    root.mainloop()
