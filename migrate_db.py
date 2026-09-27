import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'student')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_NAME = os.getenv('DB_NAME', 'attendance')

def run_migration():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        database=DB_NAME
    )
    cur = conn.cursor()

    # 1. User table enhancements: role, branch, sem, assigned_course
    cur.execute("SHOW COLUMNS FROM `user` LIKE 'role';")
    if not cur.fetchone():
        print("Adding role, branch, sem, assigned_course to user table...")
        cur.execute("ALTER TABLE `user` ADD COLUMN `role` VARCHAR(20) NOT NULL DEFAULT 'faculty';")
        cur.execute("ALTER TABLE `user` ADD COLUMN `branch` VARCHAR(50) NULL;")
        cur.execute("ALTER TABLE `user` ADD COLUMN `sem` INT NULL;")
        cur.execute("ALTER TABLE `user` ADD COLUMN `assigned_course` VARCHAR(50) NULL;")
        cur.execute("UPDATE `user` SET `role` = 'admin' WHERE `username` = 'admin';")
        conn.commit()
        print("Updated user table.")
    else:
        print("User table already has role.")

    # 2. Student table enhancements: status (Active / Dropped Out)
    cur.execute("SHOW COLUMNS FROM `student` LIKE 'status';")
    if not cur.fetchone():
        print("Adding status to student table...")
        cur.execute("ALTER TABLE `student` ADD COLUMN `status` VARCHAR(20) NOT NULL DEFAULT 'Active';")
        conn.commit()
        print("Updated student table.")
    else:
        print("Student table already has status.")

    # 3. AttendanceRecord enhancements: student_id, slot
    cur.execute("SHOW COLUMNS FROM `attendance_record` LIKE 'student_id';")
    if not cur.fetchone():
        print("Adding student_id to attendance_record...")
        cur.execute("ALTER TABLE `attendance_record` ADD COLUMN `student_id` INT NULL;")
        cur.execute("UPDATE `attendance_record` a JOIN `student` s ON a.rollno = s.rollno SET a.student_id = s.id;")
        conn.commit()
        print("Added student_id and backfilled.")
    else:
        print("attendance_record already has student_id.")

    cur.execute("SHOW COLUMNS FROM `attendance_record` LIKE 'slot';")
    if not cur.fetchone():
        print("Adding slot to attendance_record...")
        cur.execute("ALTER TABLE `attendance_record` ADD COLUMN `slot` VARCHAR(30) NOT NULL DEFAULT 'Period 1';")
        conn.commit()
        print("Added slot to attendance_record.")
    else:
        print("attendance_record already has slot.")

    cur.close()
    conn.close()
    print("Database migration completed successfully!")

if __name__ == '__main__':
    run_migration()
