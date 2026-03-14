# DocBook

DocBook is a full-stack doctor appointment booking web application built with **Django, Django REST Framework, JavaScript, HTML, and CSS**.

The project allows patients to create an account, browse doctors, search and filter by specialization, book appointments, and manage their bookings. It also includes admin-side control for managing doctors and appointments.

This project was built to practice real backend development concepts such as authentication, API handling, booking validation, role-based logic, and deployment.

---

## Live Demo

Add your deployed link here:

`https://your-docbook-render-link.onrender.com`

---

## GitHub Repository

`https://github.com/Raunaksharma0410/docbook`

---

## Project Purpose

The main purpose of this project was to build a practical backend-focused web application based on a real-world use case.

Instead of building only a basic CRUD application, I wanted to work on a project that includes authentication, user roles, API-based booking flow, validation rules, appointment conflict handling, admin management, and deployment of a full Django project.

This project helped me understand how real systems manage user actions, business rules, and backend logic together.

---

## Features

### Patient Features
- User signup and login
- JWT-based authentication
- Browse all available doctors
- Search doctors by name or specialization
- Filter doctors by specialization
- View doctor details such as specialization, experience, bio, and available time
- Book appointments with doctors
- View booked appointments
- Cancel appointments

### Booking Validation Features
- A patient can book only **one appointment per day with the same doctor**
- A doctor cannot be booked twice in the same slot
- **15-minute slot blocking** is implemented so overlapping bookings are prevented
- Appointment booking is allowed only within the doctor’s available working hours

### Admin Features
- Admin can manage users
- Admin can manage doctor profiles
- Admin can view appointments
- Admin can cancel appointments in case of emergency or doctor unavailability

### UI Features
- Clean and responsive interface
- Mobile navbar support
- Doctor listing with a user-friendly card layout
- Booking modal for smoother user experience

---

## Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- Simple JWT

### Frontend
- HTML
- CSS
- JavaScript

### Database
- SQLite

### Deployment
- Render

### Version Control
- Git
- GitHub

---

## How It Works

### 1. User Registration and Login
Patients can create an account and log in securely. Authentication is handled using JWT tokens.

### 2. Doctor Listing
All doctor profiles are fetched from the backend and displayed on the frontend.

Each doctor card shows:
- doctor name
- specialization
- experience
- available time
- short bio

### 3. Search and Filter
Users can:
- search by doctor name
- search by specialization
- filter doctors using a specialization dropdown

This improves usability and makes doctor discovery easier.

### 4. Appointment Booking
Logged-in users can book appointments through a booking modal.

Before confirming a booking, the backend validates:
- whether the doctor is available in that time range
- whether the patient already has an appointment with the same doctor on the same day
- whether another booking already occupies that 15-minute slot

### 5. Appointment Management
Patients can view their appointments and cancel them if needed.

Admin can also cancel appointments from the admin panel.

---

## Main Business Logic Implemented

This project includes important real-world validation logic.

### One Appointment Per Doctor Per Patient Per Day
A patient cannot book multiple appointments with the same doctor on the same day.

### 15-Minute Appointment Slot Protection
If one appointment is booked at a time, the next overlapping slot is blocked for 15 minutes.

Example:
- If a doctor is booked at **10:00**
- Another patient cannot book at **10:05** or **10:10**
- The next safe slot becomes available after that blocked time window

### Doctor Working-Hour Validation
Appointments can only be booked inside the doctor’s available working hours.

This makes the booking system more realistic and professional.

---

## API Endpoints

### Authentication
- `POST /api/register/` → Register a new user
- `POST /api/token/` → Login and receive JWT token
- `POST /api/token/refresh/` → Refresh access token

### Doctors
- `GET /api/doctors/` → Fetch all doctors

### Appointments
- `POST /api/appointments/book/` → Book appointment
- `GET /api/appointments/` → Get logged-in patient appointments
- `POST /api/appointments/<id>/cancel/` → Cancel appointment

### Doctor Side
- `GET /api/doctor/appointments/` → Doctor can view own appointments

---

## Folder Structure

    docbook/
    │── core/
    │   │── migrations/
    │   │── static/
    │   │   │── core/
    │   │   │   │── css/
    │   │   │   │── js/
    │   │   │   │── img/
    │   │── templates/
    │   │   │── core/
    │   │── admin.py
    │   │── models.py
    │   │── serializers.py
    │   │── views.py
    │   │── urls.py
    │
    │── docbook/
    │   │── settings.py
    │   │── urls.py
    │   │── wsgi.py
    │
    │── manage.py
    │── requirements.txt
    │── README.md

---

## Installation and Setup

### 1. Clone the repository

    git clone https://github.com/Raunaksharma0410/docbook.git
    cd docbook

### 2. Create virtual environment

    python -m venv venv

### 3. Activate virtual environment

#### Windows

    venv\Scripts\activate

#### Mac/Linux

    source venv/bin/activate

### 4. Install dependencies

    pip install -r requirements.txt

### 5. Run migrations

    python manage.py makemigrations
    python manage.py migrate

### 6. Create superuser

    python manage.py createsuperuser

### 7. Run development server

    python manage.py runserver

---

## Admin Panel

The Django admin panel is used to:
- create and manage doctor profiles
- manage appointments
- cancel appointments manually
- manage users

Admin route:

`/admin/`

This makes it easy to handle platform data and simulate real application administration.

---

## Deployment

This project is deployed on **Render**.

The deployment includes:
- Django backend hosting
- static file handling
- environment setup
- production server execution

---

## What I Learned

While building DocBook, I improved my understanding of:
- Django project structure
- model relationships
- serializer validation
- JWT authentication
- API integration with frontend JavaScript
- booking conflict logic
- user role handling
- responsive frontend design
- deployment workflow with GitHub and Render

This project helped me move beyond basic syntax and understand how backend rules control real user actions in a practical web application.

---

## Why This Project Matters

DocBook is not just a basic CRUD project. It includes practical backend logic that reflects real-world system requirements.

This project shows my ability to:
- build a full-stack Django application
- design and consume APIs
- implement real validation rules
- connect frontend and backend properly
- manage authentication and user actions
- handle booking conflicts using backend logic
- deploy a working project

For me, this project was important because it gave me hands-on practice with both development and problem-solving in a realistic use case.

---

## Future Improvements

Planned improvements for this project:
- doctor dashboard
- next available slot calculation
- email notifications
- appointment status updates
- better profile images or avatar system
- PostgreSQL integration for persistent production database
- improved doctor-side appointment controls
- better UI polish and analytics

---

## Author

**Ronak**  
Aspiring Python Backend Developer  
BCA Student

GitHub: `https://github.com/Raunaksharma0410`

---

## License

This project is built for learning, practice, and portfolio purposes.

---



## Resume One-Line Description

**DocBook — A doctor appointment booking web application built with Django, DRF, JavaScript, and Render, featuring authentication, doctor filtering, appointment booking, 15-minute slot validation, and admin management.**
