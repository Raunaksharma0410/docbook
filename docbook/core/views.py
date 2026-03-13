from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

from .models import DoctorProfile, Appointment, User
from .serializers import DoctorProfileSerializer, AppointmentSerializer


# ------------------------------------------------------
# PAGE RENDERING
# ------------------------------------------------------
def intro_page(request):
    return render(request, 'core/intro.html')

def login_page(request):
    return render(request, 'core/login.html')

def doctors_page(request):
    return render(request, 'core/doctors.html')

def appointments_page(request):
    return render(request, 'core/appointments.html')

def signup_page(request):
    return render(request, "core/signup.html")


# ------------------------------------------------------
# API: LIST DOCTORS
# ------------------------------------------------------
@api_view(['GET'])
def list_doctors(request):
    doctors = DoctorProfile.objects.select_related('user').all()
    serializer = DoctorProfileSerializer(doctors, many=True)
    return Response(serializer.data)


# ------------------------------------------------------
# API: BOOK APPOINTMENT
# ------------------------------------------------------
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    serializer = AppointmentSerializer(
        data=request.data,
        context={"request": request}
    )

    if serializer.is_valid():
        appt = serializer.save(patient=request.user)
        return Response(AppointmentSerializer(appt).data, status=201)

    return Response(serializer.errors, status=400)


# ------------------------------------------------------
# API: MY APPOINTMENTS (patient)
# ------------------------------------------------------
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def my_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


# ------------------------------------------------------
# API: CANCEL APPOINTMENT
# ------------------------------------------------------
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient=request.user
    )
    appointment.is_cancelled = True
    appointment.status = "cancelled"
    appointment.save()

    return Response({"message": "Cancelled"}, status=200)


# ------------------------------------------------------
# API: REGISTER USER  (Signup)
# ------------------------------------------------------
@csrf_exempt
@api_view(['POST'])
@permission_classes([])
def register(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password),
        is_patient=True,
        is_doctor=False,
    )

    return Response({"message": "Account created successfully"}, status=201)


# ------------------------------------------------------
# API: Doctor's Appointments
# ------------------------------------------------------
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def doctor_appointments(request):

    if not request.user.is_doctor:
        return Response({"error": "Only doctors can view this"}, status=403)

    appointments = Appointment.objects.filter(doctor=request.user)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)
