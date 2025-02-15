from operations import display_hostel_status, view_student_details, register_new_student

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