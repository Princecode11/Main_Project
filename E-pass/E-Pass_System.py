import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os


class CurfewEPassSystem:
    def __init__(self):
        self.requests = []  # Store all e-pass requests
        self.admin_credentials = {"admin": "admin123"}  # Admin login details
        self.current_request_id = 1  # Auto-increment request ID
        self.data_file = "requests.json"  # File to save requests
        self.load_requests()  # Load requests from file on startup

    def load_requests(self):
        """Load requests from the JSON file."""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                data = json.load(file)
                self.requests = data.get("requests", [])
                self.current_request_id = data.get("current_request_id", 1)

    def save_requests(self):
        """Save requests to the JSON file."""
        data = {
            "requests": self.requests,
            "current_request_id": self.current_request_id,
        }
        with open(self.data_file, "w") as file:
            json.dump(data, file)

    def register_request(self, name, contact, id_proof, reason, attachment):
        request = {
            "request_id": self.current_request_id,
            "name": name,
            "contact": contact,
            "id_proof": id_proof,
            "reason": reason,
            "attachment": attachment,
            "status": "Pending",
            "e_pass_id": None,
            "appeal": None,
        }
        self.requests.append(request)
        self.current_request_id += 1
        self.save_requests()  # Save requests after adding a new one
        return f"Request submitted successfully! Your request ID is {request['request_id']}."

    def get_request_status(self, request_id):
        for request in self.requests:
            if request["request_id"] == request_id:
                status = f"Request ID: {request_id}\nStatus: {request['status']}\n"
                if request["status"] == "Approved":
                    status += f"E-Pass ID: {request['e_pass_id']}"
                elif request["status"] == "Denied":
                    status += f"\nAppeal: {request['appeal']}" if request["appeal"] else ""
                return status
        return "Request ID not found."

    def approve_request(self, request_id):
        for request in self.requests:
            if request["request_id"] == request_id:
                if request["status"] == "Pending":
                    request["status"] = "Approved"
                    request["e_pass_id"] = f"EP-{request_id:05}"
                    self.save_requests()  # Save requests after approval
                    return f"Request {request_id} approved. E-Pass ID: {request['e_pass_id']}"
                return "Request already processed."
        return "Request ID not found."

    def deny_request(self, request_id):
        for request in self.requests:
            if request["request_id"] == request_id:
                if request["status"] == "Pending":
                    request["status"] = "Denied"
                    self.save_requests()  # Save requests after denial
                    return f"Request {request_id} denied."
                return "Request already processed."
        return "Request ID not found."

    def delete_request(self, request_id):
        """Delete a request by request ID (only accessible by admin)."""
        for request in self.requests:
            if request["request_id"] == request_id:
                self.requests.remove(request)
                self.save_requests()  # Save after deletion
                return f"Request {request_id} deleted."
        return "Request ID not found."

    def delete_all_requests(self):
        """Delete all requests and reset the request ID to 1."""
        self.requests.clear()  # Clear all requests
        self.current_request_id = 1  # Reset the request ID counter
        self.save_requests()  # Save after clearing all requests
        return "All requests have been deleted, and the ID counter has been reset to 1."


class EPassGUI:
    def __init__(self, root):
        self.system = CurfewEPassSystem()
        self.root = root
        self.root.title("Curfew E-Pass System")
        self.root.geometry("600x500")
        self.create_home_screen()

    def clear_window(self):
        """Clears the current window for the next screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_home_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Curfew E-Pass System", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self.root, text="Request E-Pass", command=self.create_request_screen).pack(pady=5)
        tk.Button(self.root, text="Check Request Status", command=self.create_status_screen).pack(pady=5)
        tk.Button(self.root, text="Admin Login", command=self.admin_login_screen).pack(pady=5)

    def create_request_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Request E-Pass", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Name:").pack(pady=5)
        name_entry = tk.Entry(self.root)
        name_entry.pack()

        tk.Label(self.root, text="Contact:").pack(pady=5)
        contact_entry = tk.Entry(self.root)
        contact_entry.pack()

        tk.Label(self.root, text="ID Proof:").pack(pady=5)
        id_proof_entry = tk.Entry(self.root)
        id_proof_entry.pack()

        tk.Label(self.root, text="Reason:").pack(pady=5)
        reason_entry = tk.Entry(self.root)
        reason_entry.pack()

        tk.Label(self.root, text="Attachment (optional):").pack(pady=5)

        def select_file():
            file_path = filedialog.askopenfilename(title="Select a file")
            attachment_label.config(text=file_path)

        attachment_label = tk.Label(self.root, text="No file selected.")
        attachment_label.pack(pady=5)

        tk.Button(self.root, text="Browse", command=select_file).pack(pady=5)

        def submit_request():
            name = name_entry.get()
            contact = contact_entry.get()
            id_proof = id_proof_entry.get()
            reason = reason_entry.get()
            attachment = attachment_label.cget("text")
            if name and contact and id_proof and reason:
                message = self.system.register_request(name, contact, id_proof, reason, attachment)
                messagebox.showinfo("Success", message)
                self.create_home_screen()
            else:
                messagebox.showerror("Error", "All fields except attachment are required!")

        tk.Button(self.root, text="Submit", command=submit_request).pack(pady=10)

    def create_status_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Check Request Status", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Enter Request ID:").pack(pady=5)
        request_id_entry = tk.Entry(self.root)
        request_id_entry.pack()

        def check_status():
            try:
                request_id = int(request_id_entry.get())
                message = self.system.get_request_status(request_id)
                messagebox.showinfo("Status", message)
            except ValueError:
                messagebox.showerror("Error", "Invalid Request ID!")

        tk.Button(self.root, text="Check Status", command=check_status).pack(pady=10)

    def admin_login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Admin Login", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Username:").pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password:").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if username in self.system.admin_credentials and self.system.admin_credentials[username] == password:
                self.create_admin_screen()
            else:
                messagebox.showerror("Error", "Invalid credentials!")

        tk.Button(self.root, text="Login", command=login).pack(pady=10)

    def create_admin_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Admin Panel", font=("Arial", 16, "bold")).pack(pady=10)

        if not self.system.requests:
            tk.Label(self.root, text="No requests found.").pack()
        else:
            for request in self.system.requests:
                details = (
                    f"ID: {request['request_id']} | Name: {request['name']} | Status: {request['status']}\n"
                    f"Reason: {request['reason']} | Attachment: {request['attachment']}"
                )
                tk.Label(self.root, text=details, justify="left", wraplength=500).pack(anchor="w", padx=10, pady=5)

                if request["attachment"] and os.path.exists(request["attachment"]):
                    def open_file(filepath=request["attachment"]):
                        try:
                            os.startfile(filepath)
                        except Exception as e:
                            messagebox.showerror("Error", f"Could not open file: {e}")

                    tk.Button(self.root, text="Open Attachment", command=open_file).pack(pady=5, anchor="w", padx=20)

            tk.Label(self.root, text="Enter Request ID to Process:").pack(pady=5)
            request_id_entry = tk.Entry(self.root)
            request_id_entry.pack()

            def approve():
                try:
                    request_id = int(request_id_entry.get())
                    message = self.system.approve_request(request_id)
                    messagebox.showinfo("Result", message)
                    self.create_admin_screen()
                except ValueError:
                    messagebox.showerror("Error", "Invalid Request ID!")

            def deny():
                try:
                    request_id = int(request_id_entry.get())
                    message = self.system.deny_request(request_id)
                    messagebox.showinfo("Result", message)
                    self.create_admin_screen()
                except ValueError:
                    messagebox.showerror("Error", "Invalid Request ID!")

            def delete():
                try:
                    request_id = int(request_id_entry.get())
                    message = self.system.delete_request(request_id)
                    messagebox.showinfo("Result", message)
                    self.create_admin_screen()
                except ValueError:
                    messagebox.showerror("Error", "Invalid Request ID!")

            def delete_all():
                message = self.system.delete_all_requests()
                messagebox.showinfo("Result", message)
                self.create_admin_screen()

            tk.Button(self.root, text="Approve", command=approve).pack(pady=5)
            tk.Button(self.root, text="Deny", command=deny).pack(pady=5)
            tk.Button(self.root, text="Delete", command=delete).pack(pady=5)
            tk.Button(self.root, text="Delete All Requests", command=delete_all).pack(pady=5)

        tk.Button(self.root, text="Back", command=self.create_home_screen).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = EPassGUI(root)
    root.mainloop()
