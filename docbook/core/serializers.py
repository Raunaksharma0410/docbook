from rest_framework import serializers
from .models import User, DoctorProfile, Appointment

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

        profile = getattr(doctor, "doctorprofile", None)
        if profile and not (profile.available_from <= time <= profile.available_to):
            raise serializers.ValidationError("Doctor not available at this time.")

        if Appointment.objects.filter(
            doctor=doctor, date=date, time=time, is_cancelled=False
        ).exists():
            raise serializers.ValidationError("Doctor already booked at this time.")

        return data