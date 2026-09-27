import unittest
from main import app, db, Student, Course, AttendanceRecord, Department, User


class TestAttendanceSystem(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()

    def test_01_unauthenticated_redirect(self):
        """Unauthenticated user accessing root must be redirected to /login"""
        resp = self.client.get('/', follow_redirects=False)
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/login', resp.headers.get('Location', ''))

    def test_02_login(self):
        """Login with default admin credentials"""
        resp = self.client.post('/login', data={'email': 'admin', 'password': 'admin'}, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Academic & Attendance Dashboard', resp.data)

    def test_03_dashboard_metrics(self):
        """Dashboard renders key stats and department roster"""
        self.client.post('/login', data={'email': 'admin', 'password': 'admin'})
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Enrolled Students', resp.data)
        self.assertIn(b'Registered Subjects', resp.data)
        self.assertIn(b'Attendance Eligibility Standing', resp.data)

    def test_04_take_attendance_flow(self):
        """Take attendance page loads and submits attendance for CU Sem 3 COA"""
        self.client.post('/login', data={'email': 'admin', 'password': 'admin'})
        resp = self.client.get('/takeattendance?branch=CU&sem=3&course=COA')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Mark Class Attendance', resp.data)
        self.assertIn(b'TURNOUT', resp.data)

        # Mark attendance for U2509001
        with self.app.app_context():
            student = Student.query.filter_by(rollno='U2509001').first()
            self.assertIsNotNone(student)
            s_id = student.id

        post_data = {
            'date': '2026-09-24',
            'branch': 'CU',
            'sem': '3',
            'course': 'COA',
            'student_ids': [str(s_id)],
            f'status_{s_id}': 'Present'
        }
        post_resp = self.client.post('/takeattendance', data=post_data, follow_redirects=True)
        self.assertEqual(post_resp.status_code, 200)

        # Verify record in DB
        with self.app.app_context():
            rec = AttendanceRecord.query.filter_by(rollno='U2509001', course_code='COA', date='2026-09-24').first()
            self.assertIsNotNone(rec)
            self.assertEqual(rec.status, 'Present')

    def test_05_view_attendance_reports(self):
        """View attendance displays cumulative stats and filters"""
        self.client.post('/login', data={'email': 'admin', 'password': 'admin'})
        resp = self.client.get('/viewattendance?branch=CU&course=COA')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Attendance Analytics & Reports', resp.data)
        self.assertIn(b'Matching Students', resp.data)

    def test_06_search_by_name_and_roll(self):
        """Search student by both roll number and partial name"""
        self.client.post('/login', data={'email': 'admin', 'password': 'admin'})

        # By Roll
        r_roll = self.client.post('/search', data={'query': 'U2509001'})
        self.assertEqual(r_roll.status_code, 200)
        self.assertIn(b'U2509001', r_roll.data)

        # By Name
        r_name = self.client.post('/search', data={'query': 'Aamil'})
        self.assertEqual(r_name.status_code, 200)
        self.assertIn(b'Aamil', r_name.data)

    def test_07_individual_student_report(self):
        """Check student detailed subject-wise breakdown page"""
        self.client.post('/login', data={'email': 'admin', 'password': 'admin'})
        resp = self.client.get('/attendance/student/U2509001')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Student Performance Report', resp.data)
        self.assertIn(b'Subject-Wise Attendance Breakdown', resp.data)

    def test_08_admin_panel_tabs(self):
        """Check all admin tabs render without errors"""
        self.client.post('/login', data={'email': 'admin', 'password': 'admin'})
        for tab in ['student', 'courses', 'dept', 'manage']:
            resp = self.client.get(f'/admin?tab={tab}')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'Admin Control Panel', resp.data)


if __name__ == '__main__':
    unittest.main()
