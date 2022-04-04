from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (PasswordChangeView, PasswordChangeDoneView, 
                                        PasswordResetView, PasswordResetDoneView,
                                        PasswordResetConfirmView, PasswordResetCompleteView)

from . import views


urlpatterns = [
    path('signup/', views.signUpView, name='signup'),
    path('signup/student/', views.studentSignUpView, name='student_signup'),
    path('signup/instructor/', views.instructorSignUpView, name='instructor_signup'),



    path('login', views.mylogin, name='log_in'),
    path('register', views.register, name='register'),
    path('log_out', views.mylogout, name='log_out'),
    
    path('student/courses', views.student_view_department_courses, name='student_view_department_courses'),
    path('instructor/courses', views.instructor_view_department_courses, name='instructor_view_department_courses'),
    
    path('student/courses/register', views.student_register_course, name='student_register_course'),
    path('instructor/courses/register', views.instructor_register_course, name='instructor_register_course'),
    
    
    path('instructor/section/marks', views.instructor_enter_marks, name='instructor_enter_marks'),
    path('instructor/section/marks/teach/<teach_id>', views.instructor_enter_marks_teach, name='instructor_enter_marks_teach'),
    path('instructor/section/mark/take/<take_id>', views.instructor_enter_mark_take, name='instructor_enter_mark_take'),
    
    path('student/sections', views.student_view_registered_section, name='student_view_registered_section'),
    path('student/grades', views.student_view_grades, name='student_view_grades'),
    
    
    
    
]