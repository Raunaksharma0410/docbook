from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    available_from = models.TimeField()
    available_to = models.TimeField()
    bio = models.TextField(blank=True, null=True)  # ✅ optional
    experience_years = models.PositiveIntegerField(default=0)  # ✅ optional
    profile_picture = models.ImageField(upload_to="doctors/", blank=True, null=True)  # ✅ optional

    def __str__(self):
        return f"Dr. {self.user.username} ({self.specialization})"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments_as_doctor")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments_as_patient")
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.patient.username} with Dr. {self.doctor.username} on {self.date} at {self.time}"