from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Service)
class AdminService(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Specialist)
class AdminSpecialist(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Schedule)
class AdminSchedule(admin.ModelAdmin):
    list_display = ('date', 'time', 'specialist', 'services', 'user',)

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ('user',)
