import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import tkinter.font as font  # Import the font module

class AttendanceRegisterGUI:
    SCHOOL_NAME = "INES RUHENGELI"
    DEPARTMENT = "Department of Computer Science, SWE"
    OPTION = "Agile Software Development "
    LECTURER = "Lecturer: Dr. NTEZIRIZA NKERABAHIZI Josbert"
    CURRENT_DATE = "Date: " + str(datetime.now().date())

    def __init__(self, master):
        self.master = master
        master.title("Attendance Register PRINCE")
        master.configure(bg='green')

        # Define font style
        title_font = font.Font(size=20, weight='bold')
        label_font = font.Font(size=14)

        # Create a frame for the title
        title_frame = tk.Frame(master, bg='green')
        title_frame.pack(side=tk.TOP, pady=(10, 0))

        tk.Label(title_frame, text="ATTENDANCE SOFTWARE", bg='green', fg='white', font=title_font).pack()

        # Create a frame for the school information
        header_frame = tk.Frame(master, bg='green')
        header_frame.pack(side=tk.TOP)

        tk.Label(header_frame, text=self.SCHOOL_NAME, bg='green', fg='white', font=label_font).pack()
        tk.Label(header_frame, text=self.DEPARTMENT, bg='green', fg='white', font=label_font).pack()
        tk.Label(header_frame, text=self.OPTION, bg='green', fg='white', font=label_font).pack()
        tk.Label(header_frame, text=self.CURRENT_DATE, bg='green', fg='white', font=label_font).pack()
        tk.Label(header_frame, text=self.LECTURER, bg='green', fg='white', font=label_font).pack()

        # Create the table
        self.table = ttk.Treeview(master, columns=("No.", "Student No.", "First Name", "Surname", "Present"), show='headings')
        self.table.heading("No.", text="No.")
        self.table.heading("Student No.", text="Student No.")
        self.table.heading("First Name", text="First Name")
        self.table.heading("Surname", text="Surname")
        self.table.heading("Present", text="Present")
        self.table.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a panel for input
        input_frame = tk.Frame(master, bg='green')
        input_frame.pack(side=tk.BOTTOM)

        tk.Label(input_frame, text="Student No.: ", bg='green', fg='white').grid(row=0, column=0)
        self.student_no_field = tk.Entry(input_frame)
        self.student_no_field.grid(row=0, column=1)

        tk.Label(input_frame, text="First Name: ", bg='green', fg='white').grid(row=1, column=0)
        self.first_name_field = tk.Entry(input_frame)
        self.first_name_field.grid(row=1, column=1)

        tk.Label(input_frame, text="Surname: ", bg='green', fg='white').grid(row=2, column=0)
        self.surname_field = tk.Entry(input_frame)
        self.surname_field.grid(row=2, column=1)

        # Add buttons
        button_frame = tk.Frame(input_frame, bg='green')
        button_frame.grid(row=3, columnspan=2)

        self.mark_attendance_button = tk.Button(button_frame, text="Mark Attendance", command=self.mark_attendance, bg='blue', fg='white')
        self.mark_attendance_button.pack(side=tk.LEFT)

        self.add_student_button = tk.Button(button_frame, text="Add Student", command=self.add_student, bg='blue', fg='white')
        self.add_student_button.pack(side=tk.LEFT)

        self.delete_student_button = tk.Button(button_frame, text="Delete Student", command=self.delete_student, bg='blue', fg='white')
        self.delete_student_button.pack(side=tk.LEFT)

        # Populate the table with sample data
        self.students = self.get_sample_students()
        for student in self.students:
            self.table.insert("", "end", values=(student['no'], student['student_no'], student['first_name'], student['surname'], 0))

    def get_sample_students(self):
        return [
            {'no': 1, 'student_no': 2165, 'first_name': "Theophile", 'surname': "HAGENIMANA"},
            {'no': 2, 'student_no': 2265, 'first_name': "Prince", 'surname': "NDUNGUTSE"},
            {'no': 3, 'student_no': 2145, 'first_name': "Henry", 'surname': "ALLISON"},
            {'no': 4, 'student_no': 2355, 'first_name': "Alva Victor", 'surname': "RUGERO"},
            {'no': 5, 'student_no': 2169, 'first_name': "ADUT GAI", 'surname': "CHOL"},
            {'no': 6, 'student_no': 2175, 'first_name': "HARMON", 'surname': "Elvis"},
            {'no': 7, 'student_no': 21610, 'first_name': "Rachel", 'surname': "MUKESHIMANA"},
            {'no': 8, 'student_no': 22611, 'first_name': "Patrick", 'surname': "NDANGIJIMANA"},
            {'no': 9, 'student_no': 21412, 'first_name': "Roger", 'surname': "MUHIRE"},
            {'no': 10, 'student_no': 235523, 'first_name': "Faiza", 'surname': "MUTESI"},
            {'no': 11, 'student_no': 21690, 'first_name': "Eric", 'surname': "TUYISENGE"},
            {'no': 12, 'student_no': 21752, 'first_name': "UWAJENEZA", 'surname': "Magnifique"},
            # ... more students
        ]

    def find_student_row(self, student_no):
        for i, student in enumerate(self.students):
            if student['student_no'] == student_no:
                return i
        return -1

    def mark_attendance(self):
        try:
            student_no = int(self.student_no_field.get())
            row = self.find_student_row(student_no)
            if row >= 0:
                self.table.item(self.table.get_children()[row], values=(self.students[row]['no'], student_no, self.students[row]['first_name'], self.students[row]['surname'], 1))
            else:
                messagebox.showerror("Error", "Student not found.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid student number.")

    def add_student(self):
        try:
            new_student_no = int(self.student_no_field.get())
            first_name = self.first_name_field.get().strip()
            surname = self.surname_field.get().strip()

            if first_name and surname and self.find_student_row(new_student_no) == -1:
                new_row = len(self.students) + 1
                self.students.append({'no': new_row, 'student_no': new_student_no, 'first_name': first_name, 'surname': surname})
                self.table.insert("", "end", values=(new_row, new_student_no, first_name, surname, 0))
                messagebox.showinfo("Success", "Student added successfully.")
            else:
                messagebox.showerror("Error", "Invalid input or student number already exists.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid student number.")

    def delete_student(self):
        try:
            student_no_to_delete = int(self.student_no_field.get())
            row = self.find_student_row(student_no_to_delete)
            if row >= 0:
                self.table.delete(self.table.get_children()[row])
                del self.students[row]
                self.update_student_numbers()
                messagebox.showinfo("Success", "Student deleted successfully.")
            else:
                messagebox.showerror("Error", "Student not found.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid student number.")

    def update_student_numbers(self):
        for index, student in enumerate(self.students):
            student['no'] = index + 1
            self.table.item(self.table.get_children()[index], values=(student['no'], student['student_no'], student['first_name'], student['surname'], student.get('present', 0)))

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceRegisterGUI(root)
    root.mainloop()