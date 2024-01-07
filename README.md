# Django Human Resource Service Application

## Features of this Project

### A. Admin Users Can
1. See Overall Summary Charts of Staff Performance, Managers Perfomrances, Departments, Positions, Leave, etc.
2. Manage Staffs (Add, Update and Delete)
3. Manage Managers (Add, Update and Delete)
4. Manage Departments (Add, Update and Delete)
5. Manage Positions (Add, Update and Delete)
6. Manage Contracts (Add, Update and Delete)
7. View Staff Attendance
8. Review and Reply Manager/Staff Feedback
9. Review (Approve/Reject) Manager/Staff Leave

### B. Managers Can
1. See the Overall Summary Charts related to their staff, their positions, leave status, etc.
2. Take/Update Staff Attendance
3. Add/Update Points/bonus
4. Apply for Leave
5. Send Feedback to HR

### C. Staffs Can
1. See the Overall Summary Charts related to their attendance, their positions, leave status, etc.
2. View Attendance
3. View Points/bonus
4. Apply for Leave
5. Send Feedback to HR/managers


## How to Install and Run this project?

### Pre-Requisites:
1. Install Git Version Control
[ https://git-scm.com/ ]

2. Install Python Latest Version
[ https://www.python.org/downloads/ ]

3. Install Pip (Package Manager)
[ https://pip.pypa.io/en/stable/installing/ ]


### Installation
**1. Create a Folder where you want to save the project**

**2. Create a Virtual Environment and Activate**

Install Virtual Environment First
```
$  pip install virtualenv
```

Create Virtual Environment

For Windows
```
$  python -m venv venv
```
For Mac
```
$  python3 -m venv venv
```

Activate Virtual Environment

For Windows
```
$  source venv/scripts/activate
```

For Mac
```
$  source venv/bin/activate
```

**3. Clone this project**
```
$  git clone https://github.com/Wilco619/HR-Service-Application.git
```

Then, Enter the project
```
$  cd HR-Service-Application
```

**4. Install Requirements from 'requirements.txt'**
```python
$  pip install -r requirements.txt
```

**5. Add the hosts**

- Got to settings.py file 
- Then, On allowed hosts, Add [‘*’]. 
```python
ALLOWED_HOSTS = ['*']
```
*No need to change on Mac.*


**6. Now Run Server**

Command for PC:
```python
$ python manage.py runserver
```

Command for Mac:
```python
$ python3 manage.py runserver
```

**7. Login Credentials**

Create Super User (HR)
```
$  python manage.py createsuperuser
```
Then Add Email, Username and Password

