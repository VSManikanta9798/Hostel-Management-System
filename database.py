import sqlite3
import os

DATABASE = 'c:/Users/Administrator/Downloads/Hostel Management System/data/hostel.db'

def get_db_connection():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        create_tables(conn)
    else:
        conn = sqlite3.connect(DATABASE)
        create_tables(conn)  # Ensure tables are created if they don't exist
    return conn

def create_tables(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT NOT NULL,
                room_type TEXT NOT NULL,
                floor_number INTEGER NOT NULL,
                total_beds INTEGER NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS beds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bed_number TEXT NOT NULL,
                room_id INTEGER NOT NULL,
                status TEXT DEFAULT 'Vacant',
                FOREIGN KEY (room_id) REFERENCES rooms(id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_number TEXT NOT NULL UNIQUE,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                nationality TEXT NOT NULL,
                blood_group TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                age INTEGER NOT NULL,
                father_guardian_name TEXT NOT NULL,
                student_contact_number TEXT NOT NULL,
                guardian_contact_number TEXT NOT NULL,
                emergency_contact_number TEXT NOT NULL,
                personal_email TEXT NOT NULL,
                college_email TEXT NOT NULL,
                full_address TEXT NOT NULL,
                pincode TEXT NOT NULL,
                specialization TEXT NOT NULL,
                year_of_study INTEGER NOT NULL,
                department TEXT NOT NULL,
                course TEXT NOT NULL,
                bed_id INTEGER NOT NULL,
                FOREIGN KEY (bed_id) REFERENCES beds(id)
            )
        ''')

if __name__ == "__main__":
    # Ensure the data directory exists
    data_directory = os.path.dirname(DATABASE)
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    conn = get_db_connection()
    conn.close()