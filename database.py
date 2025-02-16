import sqlite3

# Database file path
DATABASE = 'C:/Users/Administrator/Downloads/Hostel Management/data/hostel.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create rooms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL,
            room_type TEXT NOT NULL,
            floor_number TEXT NOT NULL,
            total_beds INTEGER NOT NULL
        )
    ''')

    # Create beds table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS beds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bed_number TEXT NOT NULL,
            room_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Vacant',
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    ''')

    # Create students table
    cursor.execute('''
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

    conn.commit()
    conn.close()

# Get a database connection
def get_db_connection():
    return sqlite3.connect(DATABASE)