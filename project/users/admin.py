from django.contrib import admin
from django.contrib.auth import get_user_model 
from .models import User, Student, Instructor


admin.site.register(User)
admin.site.register(Student)
admin.site.register(Instructor)

