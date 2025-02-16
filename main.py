import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from ttkthemes import ThemedStyle
from database import init_db, get_db_connection
from operations import display_hostel_status, view_student_details, register_new_student
from operations import *

# Initialize the database
init_db()

class HostelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏠 Hostel Management System")
        self.root.state('zoomed')  # Maximize window
        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")  # Modern theme: "arc", "equilux", "radiance"

        # Custom Colors and Fonts
        self.primary_color = "#2C3E50"
        self.secondary_color = "#3498DB"
        self.font_title = Font(family="Helvetica", size=20, weight="bold")
        self.font_body = Font(family="Arial", size=12)

        # Header
        header_frame = ttk.Frame(self.root, style="Header.TFrame")
        header_frame.pack(fill=tk.X, padx=20, pady=20)
        ttk.Label(
            header_frame,
            text="🏠 Hostel Management System",
            font=self.font_title,
            foreground=self.primary_color
        ).pack(side=tk.LEFT)

        # Main Menu
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.main_menu = ttk.Combobox(
            main_frame,
            values=[
                "📊 View Hostel Status",
                "👤 View Student Details",
                "➕ Register New Student",
                "⚙️ Initialize Hostel Structure",
                "🚪 Exit"
            ],
            state="readonly",
            font=self.font_body,
            width=30
        )
        self.main_menu.pack(pady=20)
        self.main_menu.current(0)
        self.main_menu.bind("<<ComboboxSelected>>", self.handle_menu_selection)

    def handle_menu_selection(self, event):
        choice = self.main_menu.get()
        if "Status" in choice:
            self.show_hostel_status()
        elif "Details" in choice:
            self.show_student_details_form()
        elif "Register" in choice:
            self.show_registration_form()
        elif "Initialize" in choice:
            self.initialize_hostel_structure()
        elif "Exit" in choice:
            self.root.destroy()

    def show_hostel_status(self):
        status_window = tk.Toplevel(self.root)
        status_window.title("📊 Hostel Status")
        status_window.grab_set()

        # Fetch data
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM rooms')
        total_rooms = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM beds WHERE status = "Filled"')
        occupied_beds = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM beds WHERE status = "Vacant"')
        vacant_beds = cursor.fetchone()[0]
        conn.close()

        # Status Cards
        cards_frame = ttk.Frame(status_window)
        cards_frame.pack(pady=20)

        cards = [
            ("Total Rooms", total_rooms, "#3498DB"),
            ("Occupied Beds", occupied_beds, "#E74C3C"),
            ("Vacant Beds", vacant_beds, "#2ECC71")
        ]

        for i, (title, value, color) in enumerate(cards):
            card = ttk.Frame(cards_frame, style="Card.TFrame")
            card.grid(row=0, column=i, padx=10, pady=10)
            ttk.Label(card, text=title, font=self.font_body, foreground=color).pack(pady=5)
            ttk.Label(card, text=value, font=("Helvetica", 24, "bold"), foreground=color).pack(pady=5)
            ttk.Button(status_window, text="Back", command=status_window.destroy, style="Accent.TButton").pack(pady=10)

    def show_student_details_form(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("🔍 Search Student")
        search_window.grab_set()

        ttk.Label(search_window, text="Enter Roll Number:", font=self.font_body).pack(pady=10)
        roll_entry = ttk.Entry(search_window, font=self.font_body, width=25)
        roll_entry.pack(pady=5)
        
        ttk.Button(
            search_window,
            text="Search",
            command=lambda: self.display_student_details(roll_entry.get()),
            style="Accent.TButton"
        ).pack(pady=10)

    def display_student_details(self, roll_number):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT students.*, rooms.room_number, rooms.room_type, rooms.floor_number, beds.bed_number
            FROM students
            JOIN beds ON students.bed_id = beds.id
            JOIN rooms ON beds.room_id = rooms.id
            WHERE students.roll_number = ?
        ''', (roll_number,))
        student = cursor.fetchone()
        conn.close()

        if not student:
            messagebox.showerror("Error", "❌ Student not found!")
            return

        details_window = tk.Toplevel(self.root)
        details_window.title("👤 Student Details")
        details_window.grab_set()

        # Student Info Table
        tree = ttk.Treeview(details_window, columns=("Field", "Value"), show="headings", height=20)
        tree.heading("Field", text="Field")
        tree.heading("Value", text="Value")
        tree.column("Field", width=200, anchor=tk.W)
        tree.column("Value", width=300, anchor=tk.W)

        fields = [
            "Roll Number", "First Name", "Last Name", "Gender", "Nationality",
            "Blood Group", "Date of Birth", "Age", "Father/Guardian Name",
            "Student Contact", "Guardian Contact", "Emergency Contact",
            "Personal Email", "College Email", "Address", "Pincode",
            "Specialization", "Year of Study", "Department", "Course",
            "Room Number", "Room Type", "Floor", "Bed"
        ]

        for i, field in enumerate(fields):
            value = student[i+1] if i < 20 else student[21 + (i-20)]
            tree.insert("", tk.END, values=(field, value))

        tree.pack(padx=10, pady=10)

    def initialize_hostel_structure(self):
        confirm = messagebox.askyesno(
            "Confirm", 
            "⚠️ This will delete existing data and initialize the hostel structure. Continue?"
        )
        if confirm:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students")
            cursor.execute("DELETE FROM beds")
            cursor.execute("DELETE FROM rooms")
            conn.commit()
            conn.close()
            initialize_hostel_structure()
            messagebox.showinfo("Success", "✅ Hostel structure initialized!")

    def show_registration_form(self):
        reg_window = tk.Toplevel(self.root)
        reg_window.title("➕ New Student Registration")
        reg_window.grab_set()
        
        # Add a canvas and scrollbar
        canvas = tk.Canvas(reg_window)
        scrollbar = ttk.Scrollbar(reg_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Registration Steps
        steps_frame = ttk.Frame(reg_window)
        steps_frame.pack(pady=10)

        ttk.Label(steps_frame, text="1. Room Type:", font=self.font_body).grid(row=0, column=0, padx=10)
        self.room_type_var = tk.StringVar()
        room_type_combo = ttk.Combobox(
            steps_frame, 
            textvariable=self.room_type_var, 
            values=["AC", "Non-AC"], 
            state="readonly",
            width=15
        )
        room_type_combo.grid(row=0, column=1, padx=10)
        room_type_combo.bind("<<ComboboxSelected>>", lambda e: self.update_floors(steps_frame))
        
        # Add Save, Reset, and Back buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=lambda: self.save_student(reg_window), style="Accent.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_form, style="Accent.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=reg_window.destroy, style="Accent.TButton").pack(side="left", padx=5)

    def update_floors(self, window):
        ttk.Label(window, text="2. Floor:", font=self.font_body).grid(row=1, column=0, padx=10, pady=10)
        floors = ["Ground Floor", "1st Floor", "2nd Floor"] if self.room_type_var.get() == "AC" else ["3rd Floor", "4th Floor", "5th Floor"]
        self.floor_var = tk.StringVar()
        floor_combo = ttk.Combobox(
            window, 
            textvariable=self.floor_var, 
            values=floors, 
            state="readonly",
            width=15
        )
        floor_combo.grid(row=1, column=1, padx=10)
        floor_combo.bind("<<ComboboxSelected>>", lambda e: self.update_rooms(window))

    def update_rooms(self, window):
        ttk.Label(window, text="3. Room:", font=self.font_body).grid(row=2, column=0, padx=10, pady=10)
        rooms = get_available_rooms(self.floor_var.get(), self.room_type_var.get())
        self.room_var = tk.StringVar()
        room_combo = ttk.Combobox(
            window, 
            textvariable=self.room_var, 
            values=[r[1] for r in rooms], 
            state="readonly",
            width=15
        )
        room_combo.grid(row=2, column=1, padx=10)
        self.room_ids = {r[1]: r[0] for r in rooms}
        room_combo.bind("<<ComboboxSelected>>", lambda e: self.update_beds(window))

    def update_beds(self, window):
        ttk.Label(window, text="4. Bed:", font=self.font_body).grid(row=3, column=0, padx=10, pady=10)
        room_id = self.room_ids[self.room_var.get()]
        beds = get_available_beds(room_id)
        self.bed_var = tk.StringVar()
        bed_combo = ttk.Combobox(
            window, 
            textvariable=self.bed_var, 
            values=[b[1] for b in beds], 
            state="readonly",
            width=15
        )
        bed_combo.grid(row=3, column=1, padx=10)
        self.bed_ids = {b[1]: b[0] for b in beds}
        bed_combo.bind("<<ComboboxSelected>>", lambda e: self.show_student_form(window))

    def show_student_form(self, window):
        form_window = tk.Toplevel(self.root)
        form_window.title("📝 Student Details")
        form_window.grab_set()

        fields = [
            "Roll Number", "First Name", "Last Name", "Gender", "Nationality",
            "Blood Group", "Date of Birth", "Age", "Father/Guardian Name",
            "Student Contact", "Guardian Contact", "Emergency Contact",
            "Personal Email", "College Email", "Address", "Pincode",
            "Specialization", "Year of Study", "Department", "Course"
        ]

        self.entries = {}
        for i, field in enumerate(fields):
            ttk.Label(form_window, text=field + ":", font=self.font_body).grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
            entry = ttk.Entry(form_window, font=self.font_body, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        ttk.Button(
            form_window,
            text="Submit",
            command=lambda: self.save_student(form_window),
            style="Accent.TButton"
        ).grid(row=len(fields), column=1, pady=20)

    def save_student(self, window):
        data = {field: entry.get() for field, entry in self.entries.items()}
        bed_id = self.bed_ids[self.bed_var.get()]

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO students (
                    roll_number, first_name, last_name, gender, nationality, blood_group,
                    date_of_birth, age, father_guardian_name, student_contact_number,
                    guardian_contact_number, emergency_contact_number, personal_email,
                    college_email, full_address, pincode, specialization, year_of_study,
                    department, course, bed_id
             ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          ''', (
                data["Roll Number"], data["First Name"], data["Last Name"],
                data["Gender"], data["Nationality"], data["Blood Group"],
                data["Date of Birth"], data["Age"], data["Father/Guardian Name"],
                data["Student Contact"], data["Guardian Contact"], data["Emergency Contact"],
                data["Personal Email"], data["College Email"], data["Address"],
                data["Pincode"], data["Specialization"], data["Year of Study"],
                data["Department"], data["Course"], bed_id
            ))
            cursor.execute('UPDATE beds SET status = "Filled" WHERE id = ?', (bed_id,))
            conn.commit()
            messagebox.showinfo("Success", "✅ Student registered successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"❌ Registration failed: {str(e)}")
        finally:
            conn.close()

def reset_form(self):
    for entry in self.entries.values():
        entry.delete(0, tk.END)  # Clear all entry fields

if __name__ == "__main__":
    root = tk.Tk()
    app = HostelManagementApp(root)
    root.mainloop()


# Main menu
def main_menu():
    while True:
        print("\n--- Hostel Management System ---")
        print("1. View Hostel Status")
        print("2. View Existing Student Details")
        print("3. Register New Student")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            display_hostel_status()
        elif choice == '2':
            view_student_details()
        elif choice == '3':
            register_new_student()
        elif choice == '4':
            break
        else:
            print("Invalid choice!")

# Run the application
if __name__ == '__main__':
    main_menu()  