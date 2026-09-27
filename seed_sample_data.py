from main import app, db, Student, Department, AttendanceRecord, sync_legacy_attendance, get_student_attendance_stats
from datetime import date, timedelta

def seed_data():
    with app.app_context():
        # Add sample students if needed
        sample_students = [
            ("CS101", "Aarav Sharma", 5, "Male", "Computer Science", "aarav@college.edu", "9876543210", "Hostel A-101"),
            ("CS102", "Ananya Verma", 5, "Female", "Computer Science", "ananya@college.edu", "9876543211", "Green Glen Layout"),
            ("IS201", "Rohan Mehta", 5, "Male", "Information Science", "rohan@college.edu", "9876543212", "Hostel B-205"),
            ("EC301", "Priya Nair", 3, "Female", "Electronics & Communication", "priya@college.edu", "9876543213", "Whitefield"),
            ("ME401", "Vikram Patel", 3, "Male", "Mechanical", "vikram@college.edu", "9876543214", "Indiranagar")
        ]

        for roll, name, sem, gender, branch, email, phone, addr in sample_students:
            existing = Student.query.filter_by(rollno=roll).first()
            if not existing:
                s = Student(rollno=roll, sname=name, sem=sem, gender=gender, branch=branch, email=email, number=phone, address=addr)
                db.session.add(s)
        db.session.commit()

        # Seed 10 days of attendance
        today = date.today()
        students = Student.query.all()
        for i in range(10, 0, -1):
            att_date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            for s in students:
                existing = AttendanceRecord.query.filter_by(rollno=s.rollno, date=att_date).first()
                if not existing:
                    # Give different students different attendance profiles
                    if s.rollno == "CS101":
                        status = "Present" if i != 3 else "Absent" # 90%
                    elif s.rollno == "CS102":
                        status = "Present" if i not in (2, 5) else "Absent" # 80%
                    elif s.rollno == "IS201":
                        status = "Present" if i not in (1, 3, 6, 8) else "Absent" # 60% (Shortage)
                    elif s.rollno == "EC301":
                        status = "Present" # 100%
                    else:
                        status = "Present" if i % 2 == 0 else "Absent" # 50% (Shortage)
                    
                    db.session.add(AttendanceRecord(rollno=s.rollno, date=att_date, status=status))

        db.session.commit()

        # Sync legacy percentage
        for s in students:
            stats = get_student_attendance_stats(s.rollno)
            sync_legacy_attendance(s.rollno, stats['percentage'])

        print("Sample data seeded successfully!")

if __name__ == '__main__':
    seed_data()
