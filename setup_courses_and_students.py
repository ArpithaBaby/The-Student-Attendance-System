import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'student')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_NAME = os.getenv('DB_NAME', 'attendance')

def setup_courses_and_students():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        database=DB_NAME
    )
    cur = conn.cursor()

    # 1. Add course_code to attendance_record if not present
    cur.execute("DESCRIBE attendance_record;")
    cols = [c[0] for c in cur.fetchall()]
    if 'course_code' not in cols:
        print("Adding course_code column to attendance_record...")
        cur.execute("ALTER TABLE attendance_record ADD COLUMN course_code VARCHAR(50) DEFAULT 'GENERAL';")
        cur.execute("CREATE INDEX idx_att_course ON attendance_record(course_code);")
        conn.commit()

    # 2. Create course table if not exists
    cur.execute("""
    CREATE TABLE IF NOT EXISTS `course` (
        `id` INT AUTO_INCREMENT PRIMARY KEY,
        `course_code` VARCHAR(50) NOT NULL,
        `course_name` VARCHAR(100) NOT NULL,
        `branch` VARCHAR(50) NOT NULL,
        `sem` INT NOT NULL DEFAULT 3,
        UNIQUE KEY `uniq_course_branch_sem` (`course_code`, `branch`, `sem`)
    );
    """)
    conn.commit()

    # 3. Setup Departments / Branches: CU, CS, AI
    branches = ['CU', 'CS', 'AI']
    for b in branches:
        cur.execute("INSERT IGNORE INTO `department` (`branch`) VALUES (%s);", (b,))
    conn.commit()
    print("Departments CU, CS, AI ensured.")

    # 4. Populate Courses for CU, CS, AI (Sem 3)
    courses = [
        # CU
        ('COA', 'Computer Organization & Architecture', 'CU', 3),
        ('OOPS', 'Object-Oriented Programming', 'CU', 3),
        ('FLAT', 'Formal Languages & Automata Theory', 'CU', 3),
        ('DBMS', 'Database Management Systems', 'CU', 3),
        # CS
        ('DSA', 'Data Structures & Algorithms', 'CS', 3),
        ('DBMS', 'Database Management Systems', 'CS', 3),
        ('OS', 'Operating Systems', 'CS', 3),
        ('CN', 'Computer Networks', 'CS', 3),
        ('COA', 'Computer Organization & Architecture', 'CS', 3),
        # AI
        ('ML', 'Machine Learning', 'AI', 3),
        ('MATH', 'Mathematics & Linear Algebra for AI', 'AI', 3),
        ('PYTHON', 'Python for Data Science & AI', 'AI', 3),
        ('DSA', 'Data Structures & Algorithms', 'AI', 3),
        ('DBMS', 'Database Management Systems', 'AI', 3),
    ]

    for code, name, branch, sem in courses:
        cur.execute("""
        INSERT INTO `course` (`course_code`, `course_name`, `branch`, `sem`)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE `course_name` = VALUES(`course_name`);
        """, (code, name, branch, sem))
    conn.commit()
    print("Courses for CU, CS, and AI populated.")

    # 5. Populate the 20 Students from user's list
    user_students = [
        ('U2509001', 'AAMIL MOHAMMED T S'),
        ('U2509002', 'ABHIRAMI MANOJ NAIR'),
        ('U2509003', 'ADITI GAURI VINOD'),
        ('U2509004', 'AJAYKRISHNA EDATHATTU BIJU'),
        ('U2509005', 'AKSHAY P M'),
        ('U2509006', 'ALEENA B JOHN'),
        ('U2509007', 'ALFRED VARGHESE JAMES'),
        ('U2509008', 'ALLEN BENSON'),
        ('U2509009', 'AMANDA BIJU MANGALY'),
        ('U2509010', 'ANANYA JENNY'),
        ('U2509011', 'ANNU MARIAM GEORGE'),
        ('U2509012', 'ARJUN G'),
        ('U2509013', 'ARPITHA MARY BABY'),
        ('U2509014', 'ARSHA MARIYA TOMY'),
        ('U2509015', 'ASHWIN SUNIL KAMBIL'),
        ('U2509016', 'ASWANTH BOBISH'),
        ('U2509017', 'AUSTN JOHN JOBY'),
        ('U2509018', 'AYAAN YOUSUF'),
        ('U2509019', 'BADRA RAGEND'),
        ('U2509020', 'BHAVIN JOHN BENNY'),
    ]

    for roll, name in user_students:
        email = f"{roll.lower()}@college.edu"
        cur.execute("""
        INSERT INTO `student` (`rollno`, `sname`, `sem`, `gender`, `branch`, `email`, `number`, `address`)
        VALUES (%s, %s, 3, 'Not Specified', 'CU', %s, '9876543210', 'Campus Hostel')
        ON DUPLICATE KEY UPDATE `sname` = VALUES(`sname`), `branch` = 'CU', `sem` = 3;
        """, (roll, name, email))
    conn.commit()
    print("User students (U2509001 - U2509020) enrolled successfully in CU, Semester 3.")

    # 6. Seed sample subject-wise attendance for these 20 students so they have initial data
    from datetime import date, timedelta
    today = date.today()
    cu_subjects = ['COA', 'OOPS', 'FLAT', 'DBMS']

    # For each subject, record 5 sessions over the past 2 weeks
    for subj_idx, subj in enumerate(cu_subjects):
        for session_offset in range(1, 6):
            sess_date = (today - timedelta(days=(session_offset * 2) + subj_idx)).strftime('%Y-%m-%d')
            for s_idx, (roll, _) in enumerate(user_students):
                # Pattern: give different students realistic attendance
                if s_idx in (4, 11, 19): # A few students with shortage in some subjects
                    status = 'Present' if (s_idx + session_offset) % 3 == 0 else 'Absent'
                else:
                    status = 'Present' if (s_idx + session_offset) % 5 != 0 else 'Absent'
                
                cur.execute("""
                INSERT INTO `attendance_record` (`rollno`, `course_code`, `date`, `status`)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE `status` = VALUES(`status`);
                """, (roll, subj, sess_date, status))

    conn.commit()
    print("Subject-wise attendance records generated for CU subjects (COA, OOPS, FLAT, DBMS).")

    cur.close()
    conn.close()

if __name__ == '__main__':
    setup_courses_and_students()
