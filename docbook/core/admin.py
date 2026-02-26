
from django.contrib import admin
from .models import User, DoctorProfile, Appointment

admin.site.register(User)
admin.site.register(DoctorProfile)
admin.site.register(Appointment)
# Register your models here.
