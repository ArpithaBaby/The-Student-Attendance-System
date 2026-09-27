import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'student')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_NAME = os.getenv('DB_NAME', 'attendance')

def init_database():
    print(f"Connecting to MySQL server at {DB_HOST}:{DB_PORT} as {DB_USER}...")
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"Database `{DB_NAME}` verified/created.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Warning connecting with mysql.connector: {e}")

    # Use Flask app context to create all tables
    from main import app, db, Department, Test, Student, User, AttendanceRecord, sync_legacy_attendance, get_student_attendance_stats
    with app.app_context():
        db.create_all()
        print("SQLAlchemy tables created successfully in database:", DB_NAME)

        # Seed default admin user
        if User.query.count() == 0:
            db.session.add(User(username='admin', email='admin@college.edu', password='admin'))
            db.session.commit()
            print("Default admin user created: admin@college.edu / admin")

        # Connect directly to sync existing students from `students` table if present
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT,
                database=DB_NAME
            )
            cursor = conn.cursor()

            # Import departments from courses if courses table exists
            cursor.execute("SHOW TABLES LIKE 'courses';")
            if cursor.fetchone():
                cursor.execute("""
                INSERT IGNORE INTO `department` (`branch`)
                SELECT DISTINCT `name` FROM `courses` WHERE `name` IS NOT NULL AND `name` != '';
                """)
                conn.commit()

            # Seed default departments if still empty
            if Department.query.count() == 0:
                for d in ["Computer Science", "Information Science", "Electronics & Communication", "Mechanical"]:
                    db.session.add(Department(branch=d))
                db.session.commit()

            # Import existing 14 students from `students` table if present
            cursor.execute("SHOW TABLES LIKE 'students';")
            if cursor.fetchone():
                cursor.execute("""
                INSERT IGNORE INTO `student` (`rollno`, `sname`, `sem`, `gender`, `branch`, `email`, `number`, `address`)
                SELECT 
                    s.student_id,
                    s.name,
                    5,
                    'Not Specified',
                    COALESCE(c.name, 'Computer Science'),
                    CONCAT(LOWER(REPLACE(s.name, ' ', '.')), '@uni.edu'),
                    '9876543210',
                    'Campus Hostel'
                FROM `students` s
                LEFT JOIN `courses` c ON s.course_id = c.id;
                """)
                conn.commit()
                print("Imported existing students from `students` table into `student`.")

            cursor.close()
            conn.close()
        except Exception as se:
            print(f"Notice while syncing students: {se}")

        # Insert test entry for /test route verification
        if Test.query.count() == 0:
            db.session.add(Test(name="Database Connection Test", email="test@attendance.local"))
            db.session.commit()

        # Seed initial attendance for any students who have 0 attendance records
        from datetime import date, timedelta
        students = Student.query.all()
        today = date.today()
        seeded_any = False

        for s in students:
            rec_count = AttendanceRecord.query.filter_by(rollno=s.rollno).count()
            if rec_count == 0:
                seeded_any = True
                # Seed 8 past days of attendance
                for day_offset in range(8, 0, -1):
                    att_date = (today - timedelta(days=day_offset)).strftime('%Y-%m-%d')
                    # Make most students eligible (>=75%) and a couple with shortage for demonstration
                    if s.rollno in ('ST-2045', 'ST-3004'):
                        status = 'Present' if day_offset % 3 == 0 else 'Absent'  # ~33% shortage
                    elif s.rollno in ('ST-2048', 'ST-3002'):
                        status = 'Present' if day_offset not in (1, 4) else 'Absent' # 75%
                    else:
                        status = 'Present' if day_offset != 3 else 'Absent'  # 87.5% eligible
                    
                    db.session.add(AttendanceRecord(rollno=s.rollno, date=att_date, status=status))

        if seeded_any:
            db.session.commit()
            for s in students:
                stats = get_student_attendance_stats(s.rollno)
                sync_legacy_attendance(s.rollno, stats['percentage'])
            print("Initial attendance records generated.")

    print(f"\nDatabase initialization complete! Connected to `{DB_NAME}` database.")

if __name__ == '__main__':
    init_database()
