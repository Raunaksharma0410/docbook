from django.contrib import admin
from .models import User, DoctorProfile, Appointment


# ----------------------------
# User Admin
# ----------------------------
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_doctor", "is_patient")
    list_filter = ("is_doctor", "is_patient")
    search_fields = ("username", "email")


# ----------------------------
# Doctor Profile Admin
# ----------------------------
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "specialization", "experience_years")
    search_fields = ("user__username", "specialization")


# ----------------------------
# Appointment Admin
# ----------------------------
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "doctor",
        "patient",
        "date",
        "time",
        "status",
        "is_cancelled",
    )

    list_filter = ("status", "date", "doctor")

    search_fields = ("doctor__username", "patient__username")

    actions = ["cancel_appointments"]

    def cancel_appointments(self, request, queryset):
        queryset.update(status="cancelled", is_cancelled=True)

    cancel_appointments.short_description = "Cancel selected appointments"