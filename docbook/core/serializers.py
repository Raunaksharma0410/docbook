from rest_framework import serializers
from .models import User, DoctorProfile, Appointment
from datetime import datetime, timedelta


# ------------------------------------------------------
# USER SERIALIZER
# Used to return basic user information in API responses
# ------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_doctor', 'is_patient']


# ------------------------------------------------------
# DOCTOR PROFILE SERIALIZER
# Combines doctor profile data with basic user information
# ------------------------------------------------------
class DoctorProfileSerializer(serializers.ModelSerializer):

    # Nested serializer to include doctor user details
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            'id',
            'user',
            'specialization',
            'available_from',
            'available_to',
            'bio',
            'experience_years',
            'profile_picture'
        ]


# ------------------------------------------------------
# APPOINTMENT SERIALIZER
# Handles appointment creation, validation and response
# ------------------------------------------------------
class AppointmentSerializer(serializers.ModelSerializer):

    # Accept doctor id from frontend when booking appointment
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_doctor=True),
        write_only=True,
        source='doctor'
    )

    # Return doctor details using custom serializer method
    doctor = serializers.SerializerMethodField()

    # Patient information is read-only (taken from logged-in user)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id',
            'doctor_id',
            'doctor',
            'patient',
            'date',
            'time',
            'status',
            'created_at',
            'is_cancelled'
        ]

    # ------------------------------------------------------
    # Returns doctor profile information in appointment response
    # ------------------------------------------------------
    def get_doctor(self, obj):
        profile = getattr(obj.doctor, "doctorprofile", None)

        if profile:
            return DoctorProfileSerializer(profile).data

        return {
            "id": obj.doctor.id,
            "username": obj.doctor.username
        }

    # ------------------------------------------------------
    # APPOINTMENT VALIDATION LOGIC
    # Prevents invalid bookings before saving appointment
    # ------------------------------------------------------
    def validate(self, data):

        doctor = data['doctor']
        time = data['time']
        date = data['date']

        # Logged in user becomes the patient
        patient = self.context['request'].user

        # Get doctor profile if exists
        profile = getattr(doctor, "doctorprofile", None)

        # ------------------------------------------------------
        # 1️⃣ Doctor availability validation
        # Ensures booking time is inside doctor's working hours
        # ------------------------------------------------------
        if profile and not (profile.available_from <= time <= profile.available_to):
            raise serializers.ValidationError(
                "Doctor not available at this time."
            )

        # ------------------------------------------------------
        # 2️⃣ Prevent same patient booking same doctor twice in one day
        # ------------------------------------------------------
        if Appointment.objects.filter(
                patient=patient,
                doctor=doctor,
                date=date,
                is_cancelled=False
        ).exists():

            raise serializers.ValidationError(
                "You already have an appointment with this doctor today."
            )

        # ------------------------------------------------------
        # 3️⃣ 15-minute slot blocking logic
        # Prevents overlapping appointments
        # ------------------------------------------------------
        appointment_start = datetime.combine(date, time)
        appointment_end = appointment_start + timedelta(minutes=15)

        existing_appointments = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            is_cancelled=False
        )

        for appt in existing_appointments:

            existing_start = datetime.combine(date, appt.time)
            existing_end = existing_start + timedelta(minutes=15)

            # Check if appointment overlaps existing slot
            if appointment_start < existing_end and appointment_end > existing_start:
                raise serializers.ValidationError(
                    "This slot is already booked. Please select another time."
                )

        return data