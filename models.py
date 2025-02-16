from database import get_db_connection

class Room:
    def __init__(self, room_number, room_type, floor_number, total_beds):
        self.room_number = room_number
        self.room_type = room_type
        self.floor_number = floor_number
        self.total_beds = total_beds

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO rooms (room_number, room_type, floor_number, total_beds)
            VALUES (?, ?, ?, ?)
        ''', (self.room_number, self.room_type, self.floor_number, self.total_beds))
        conn.commit()
        conn.close()

class Bed:
    def __init__(self, bed_number, room_id, status='Vacant'):
        self.bed_number = bed_number
        self.room_id = room_id
        self.status = status

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO beds (bed_number, room_id, status)
            VALUES (?, ?, ?)
        ''', (self.bed_number, self.room_id, self.status))
        conn.commit()
        conn.close()

class Student:
    def __init__(self, roll_number, first_name, last_name, gender, nationality, blood_group, date_of_birth, age, father_guardian_name, student_contact_number, guardian_contact_number, emergency_contact_number, personal_email, college_email, full_address, pincode, specialization, year_of_study, department, course, bed_id):
        self.roll_number = roll_number
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.nationality = nationality
        self.blood_group = blood_group
        self.date_of_birth = date_of_birth
        self.age = age
        self.father_guardian_name = father_guardian_name
        self.student_contact_number = student_contact_number
        self.guardian_contact_number = guardian_contact_number
        self.emergency_contact_number = emergency_contact_number
        self.personal_email = personal_email
        self.college_email = college_email
        self.full_address = full_address
        self.pincode = pincode
        self.specialization = specialization
        self.year_of_study = year_of_study
        self.department = department
        self.course = course
        self.bed_id = bed_id

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO students (
                roll_number, first_name, last_name, gender, nationality, blood_group,
                date_of_birth, age, father_guardian_name, student_contact_number,
                guardian_contact_number, emergency_contact_number, personal_email,
                college_email, full_address, pincode, specialization, year_of_study,
                department, course, bed_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.roll_number, self.first_name, self.last_name, self.gender, self.nationality, self.blood_group,
            self.date_of_birth, self.age, self.father_guardian_name, self.student_contact_number,
            self.guardian_contact_number, self.emergency_contact_number, self.personal_email,
            self.college_email, self.full_address, self.pincode, self.specialization, self.year_of_study,
            self.department, self.course, self.bed_id
        ))
        conn.commit()
        conn.close()