# DocBook – Doctor Appointment Booking System

DocBook is a Django REST-based backend application that allows patients to book appointments with doctors.
The system provides authentication using JWT tokens and manages doctor profiles and appointment scheduling.

---

## 🚀 Features

* User registration (Patient / Doctor)
* JWT Authentication (Login & Token Refresh)
* Doctor profile management
* List available doctors
* Book appointments with doctors
* Cancel appointments
* View patient appointments
* Doctors can view their scheduled appointments
* Prevents double booking of doctors

---

## 🛠 Tech Stack

* **Backend:** Python, Django
* **API Framework:** Django REST Framework
* **Authentication:** JWT (SimpleJWT)
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **Media Handling:** Django Media Files

---

## 📂 Project Structure

```
docbook/
│
├── core/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│
├── templates/
│
├── media/
│
├── docbook/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
```

---

## 🔐 Authentication

The project uses **JWT Authentication** via `djangorestframework-simplejwt`.

Endpoints:

```
POST /api/token/
POST /api/token/refresh/
```

Use the returned **access token** in headers:

```
Authorization: Bearer <your_token>
```

---

## 📌 API Endpoints

### Register User

```
POST /api/register/
```

### Get Doctors

```
GET /api/doctors/
```

### Book Appointment

```
POST /api/appointments/book/
```

### View My Appointments

```
GET /api/appointments/
```

### Cancel Appointment

```
POST /api/appointments/<appointment_id>/cancel/
```

### Doctor Appointments

```
GET /api/doctor/appointments/
```

---

## ⚙️ Installation

Clone the repository:

```
git clone https://github.com/Raunaksharma0410/docbook.git
cd docbook
```

Create virtual environment:

```
python -m venv venv
```

Activate environment:

Windows:

```
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run migrations:

```
python manage.py migrate
```

Start server:

```
python manage.py runserver
```

---

## 👨‍💻 Author

Raunak Sharma
BCA Student | Python Backend Developer
