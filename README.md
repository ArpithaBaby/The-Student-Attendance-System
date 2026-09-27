# SmartTrack - Student Attendance & Course Management System

A web-based Student Attendance and Academic Course Management Portal built using **Python, Flask, MySQL 8.0, SQLAlchemy, HTML5, and Bootstrap**.

Designed for colleges and academic departments to manage student enrollments, record class-wise daily attendance with real-time turnout meters, track course-level compliance, and flag exam shortage risks ($<75\%$).

---

## 🌟 Key Features

- **Department & Course-Wise Attendance Tracking**:
  - Separate branches: **CU**, **CS**, and **AI** (Semester 3).
  - Preconfigured subjects per branch (e.g., `COA`, `OOPS`, `FLAT`, `DBMS`, `DSA`, `ML`, etc.).
  - Tracks individual student attendance per subject and overall aggregate.
- **Dynamic Live Attendance Register (`/takeattendance`)**:
  - **Live Attendance Meter**: Automatically calculates Present, Absent, and Live Turnout % in real time as toggles are clicked.
  - **One-Click Batch Actions**: Mark All Present, Mark All Absent, or Invert Selections.
  - **Instant Search**: Real-time table filter to search students by name or roll number without page reloads.
- **Attendance Analytics & Shortage Alerts (`/viewattendance`)**:
  - Color-coded eligibility badges:
    - **Eligible ($\ge 75\%$)**: Green badge with checkmark.
    - **Shortage Warning ($< 75\%$)**: Crimson alert badge.
  - Date-specific register view to inspect daily class rolls.
- **Individual Student Performance Reports (`/attendance/student/<rollno>`)**:
  - Detailed card breakdown for each registered subject showing attended sessions, total sessions, and compliance progress bar.
  - Chronological history log of every attended/missed date.
- **Unified Admin Control Panel (`/admin`)**:
  - **Tab 1: Enroll Student**: Form for adding new students.
  - **Tab 2: Manage Courses**: Add, search, and delete subjects with branch filter pills.
  - **Tab 3: Branches / Departments**: Manage official degree branches with live student and course counters.
  - **Tab 4: Edit Student Records**: Directory with real-time search, Edit (`/edit/<id>`), and Delete actions.
- **Authentication & Security (`/login`)**:
  - Enforced login protection on all portal routes.
  - Default Administrator login: `admin` / `admin`.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Flask, Flask-SQLAlchemy, Flask-Login
- **Database**: MySQL 8.0 (connected via `mysql-connector-python`)
- **Frontend**: HTML5, CSS3, Bootstrap 4, FontAwesome, Google Font (Plus Jakarta Sans)

---

## 🚀 Team Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/ArpithaBaby/student-attendance-system.git
cd student-attendance-system
```

### 2. Set Up Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and enter your MySQL credentials:
```bash
cp .env.example .env
```
Inside `.env`:
```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=attendance
SECRET_KEY=key_student_management_secret
```

### 5. Initialize Database & Seed Data
Make sure your MySQL server is running, then run:
```bash
# Initialize tables and seed courses/students
python setup_courses_and_students.py
```

### 6. Run the Application
```bash
python main.py
```
Open your browser and navigate to:
```
http://localhost:5000
```
- **Default Username**: `admin`
- **Default Password**: `admin`

---

## 🧪 Running Automated Tests

Run the complete test suite:
```bash
python -m unittest test_system.py
```

---

## 📂 Project Structure

```
├── .env.example              # Template for database configuration
├── .gitignore                # Git ignore rules (prevents committing secrets)
├── README.md                 # Project documentation & team setup guide
├── init_db.py                # Database setup script
├── main.py                   # Core Flask application and routes
├── requirements.txt          # Python dependencies
├── setup_courses_and_students.py # Seeds branches, courses, and students
├── static/                   # CSS, vendor libraries, assets
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Base layout shell (sidebar, topbar, theme)
│   ├── index.html            # Dashboard overview
│   ├── take_attendance.html  # Live dynamic attendance marking
│   ├── view_attendance.html  # Attendance analytics & register
│   ├── student_attendance_detail.html # Individual student breakdown
│   ├── studentdetails.html   # Student directory roster
│   ├── admin.html            # Unified admin panel (4 tabs)
│   ├── edit.html             # Edit student record
│   ├── search.html           # Student & roll number search
│   ├── login.html            # Sign in page
│   └── signup.html           # Account registration
└── test_system.py            # Automated test suite
```

---

## 👥 Contributors
Developed for Student Attendance & Academic Course Management.
