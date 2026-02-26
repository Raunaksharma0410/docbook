from django.urls import path
from .views import (
    intro_page, login_page, doctors_page, appointments_page,
    list_doctors, book_appointment, my_appointments, cancel_appointment,
    register, signup_page, doctor_appointments   # ✅ added doctor_appointments
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 🔹 Frontend pages
    path('', intro_page, name='intro_page'),
    path('login/', login_page, name='login_page'),
    path('doctors/', doctors_page, name='doctors_page'),
    path('appointments/', appointments_page, name='appointments_page'),
    path("signup/", signup_page, name="signup_page"),

    # 🔹 JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🔹 API endpoints
    path('api/doctors/', list_doctors, name='list_doctors'),
    path('api/appointments/book/', book_appointment, name='book_appointment'),
    path('api/appointments/', my_appointments, name='my_appointments'),
    path('api/appointments/<int:appointment_id>/cancel/', cancel_appointment, name='cancel_appointment'),
    path('api/register/', register, name='register'),
    path('api/doctor/appointments/', doctor_appointments, name='doctor_appointments'),
]