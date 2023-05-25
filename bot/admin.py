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
    list_display = ('date', 'timeslot', 'specialist', 'services', 'user',)


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('name', 'phone')
