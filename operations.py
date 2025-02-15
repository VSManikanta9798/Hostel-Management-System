from database import get_db_connection
from models import Room, Bed, Student

# Display hostel status
def display_hostel_status():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM rooms')
    total_rooms = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM beds WHERE status = "Filled"')
    occupied_beds = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM beds WHERE status = "Vacant"')
    vacant_beds = cursor.fetchone()[0]
    conn.close()
    print("\n--- Hostel Status ---")
    print(f"Total Rooms: {total_rooms}")
    print(f"Occupied Beds: {occupied_beds}")
    print(f"Vacant Beds: {vacant_beds}")

# View existing student details
def view_student_details():
    roll_number = input("Enter the student's roll number: ")
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
    if student:
        print("\n--- Student Details ---")
        print(f"Roll Number: {student[1]}")
        print(f"Name: {student[2]} {student[3]}")
        print(f"Gender: {student[4]}")
        print(f"Room Type: {student[22]}")
        print(f"Floor: {student[23]}")
        print(f"Room Number: {student[21]}")
        print(f"Bed Number: {student[24]}")
        print(f"Contact: {student[10]}")
    else:
        print("Student not found!")

# Register a new student
def register_new_student():
    print("\n--- New Student Registration ---")
    # Step 1: Select room type, floor, room, and bed
    room_type = input("Enter room type (AC/Non-AC): ").strip().lower()
    floor_number = int(input("Enter floor number: "))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT rooms.id, rooms.room_number, COUNT(beds.id) AS vacant_beds
        FROM rooms
        LEFT JOIN beds ON rooms.id = beds.room_id AND beds.status = "Vacant"
        WHERE rooms.room_type = ? AND rooms.floor_number = ?
        GROUP BY rooms.id
    ''', (room_type, floor_number))
    rooms = cursor.fetchall()
    if not rooms:
        print("No rooms available on this floor!")
        return
    print("\nAvailable Rooms:")
    for room in rooms:
        print(f"Room {room[1]} - Vacant Beds: {room[2]}")
    room_id = int(input("Enter room ID: "))
    cursor.execute('SELECT * FROM beds WHERE room_id = ? AND status = "Vacant"', (room_id,))
    beds = cursor.fetchall()
    if not beds:
        print("No vacant beds in this room!")
        return
    print("\nAvailable Beds:")
    for bed in beds:
        print(f"Bed {bed[1]} - ID: {bed[0]}")
    bed_id = int(input("Enter bed ID: "))
    # Step 2: Enter student details
    print("\nEnter Student Details:")
    student = Student(
        input("Roll Number: "),
        input("First Name: "),
        input("Last Name: "),
        input("Gender: "),
        input("Nationality: "),
        input("Blood Group: "),
        input("Date of Birth (YYYY-MM-DD): "),
        int(input("Age: ")),
        input("Father/Guardian Name: "),
        input("Student Contact Number: "),
        input("Guardian Contact Number: "),
        input("Emergency Contact Number: "),
        input("Personal Email: "),
        input("College Email: "),
        input("Full Address: "),
        input("Pincode: "),
        input("Specialization: "),
        int(input("Year of Study: ")),
        input("Department/Branch: "),
        input("Course: "),
        bed_id
    )
    student.save()
    cursor.execute('UPDATE beds SET status = "Filled" WHERE id = ?', (bed_id,))
    conn.commit()
    conn.close()
    print("\nStudent registered successfully!")