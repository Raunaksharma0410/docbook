from rest_framework import serializers
from .models import User, DoctorProfile, Appointment
from datetime import datetime, timedelta


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_doctor', 'is_patient']


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            'id', 'user', 'specialization',
            'available_from', 'available_to',
            'bio', 'experience_years', 'profile_picture'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_doctor=True),
        write_only=True,
        source='doctor'
    )
    doctor = serializers.SerializerMethodField()
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor_id', 'doctor', 'patient',
            'date', 'time', 'status', 'created_at', 'is_cancelled'
        ]

    def get_doctor(self, obj):
        profile = getattr(obj.doctor, "doctorprofile", None)
        if profile:
            return DoctorProfileSerializer(profile).data
        return {"id": obj.doctor.id, "username": obj.doctor.username}

    def validate(self, data):

        doctor = data['doctor']
        time = data['time']
        date = data['date']
        patient = self.context['request'].user

        profile = getattr(doctor, "doctorprofile", None)

        # Doctor working hours
        if profile and not (profile.available_from <= time <= profile.available_to):
            raise serializers.ValidationError("Doctor not available at this time.")

        # Patient can only book one appointment per doctor per day
        if Appointment.objects.filter(
                patient=patient,
                doctor=doctor,
                date=date,
                is_cancelled=False
        ).exists():
            raise serializers.ValidationError(
                "You already have an appointment with this doctor today."
            )

        # 15 minute slot blocking
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

            if appointment_start < existing_end and appointment_end > existing_start:
                raise serializers.ValidationError(
                    "This slot is already booked. Please select another time."
                )

        return data