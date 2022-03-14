from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, get_object_or_404
from datetime import datetime, date
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
from django.contrib import messages
import logging
from django.utils.timezone import now
import re
from django.contrib.auth.decorators import login_required


from university.models import Department, Course, Section


from .models import User, Student, Instructor
from .choices import country_choices, generate_code


# from .models import Profile


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def index(request):
    return render(request, 'users/index.html')
    

def studentSignUpView(request):
    """
        student signup view
    """
    computer = 'computer'
    physics = 'physics'
    economics = 'economics'
    art = 'art'
    # departments = [computer, physics, economics, art]
    departments = Department.objects.values_list('dept_name', flat=True)
    context = {
        "departments": departments
    }

    if request.method == 'POST':
        # Get form values

        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        email = request.POST['email']
        
        # if (!request.POST['tot_cred']):
        #     tot_cred = request.POST['tot_cred']
        # else:
        #     tot_cred = 0
            
        dept_name_value = request.POST.get('dept_name', computer)
        dept_name = Department.objects.get(dept_name=dept_name_value)
        
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if password match
        if password == password2:
            # Check email
            
            User = get_user_model()
            # Check Email
            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email is being used.')
                return redirect('student_signup', context)
            else:
                user = User.objects.create_user(
                                            password=password,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name,
                                            is_promoted=False,
                                            is_student=True,
                                            is_instructor=False)
                user.save()
                
                student = Student.objects.create(
                    user=user,
                    # tot_cred=tot_cred,
                    dept_name=dept_name
                )
                student.save()
                
                return redirect('signup')
                
        else:
            messages.error(request, 'Passwords doesnt match!')
            return redirect('student_signup', context)
    else:
        return render(request, 'users/student_signup.html', context)


def instructorSignUpView(request):
    """
        instructor signup view
    """
    computer = 'computer'
    physics = 'physics'
    economics = 'economics'
    art = 'art'
    departments = [computer, physics, economics, art]
    departments = Department.objects.values_list('dept_name', flat=True)
    context = {
        "departments": departments
    }
    

    if request.method == 'POST':
        # Get form values

        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        email = request.POST['email']
        
        salary = int(request.POST.get('salary', 0))
        dept_name_value = request.POST.get('dept_name', computer)
        dept_name = Department.objects.get(dept_name=dept_name_value)
        
        
        
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if password match
        if password == password2:
            # Check email
            
            User = get_user_model()
            # Check Email
            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email is being used.')
                return redirect('instructor_signup', context)
            else:
                user = User.objects.create_user(
                                            password=password,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name,
                                            is_promoted=False,
                                            is_student=False,
                                            is_instructor=True)
                user.save()
                
                instructor = Instructor.objects.create(
                    user=user,
                    salary=salary,
                    dept_name=dept_name
                )
                instructor.save()
                
                return redirect('signup')
                
        else:
            messages.error(request, 'Passwords doesnt match!')
            return redirect('instructor_signup', context)
    else:
        return render(request, 'users/instructor_signup.html', context)


def signUpView(request):
    return render(request, 'users/login.html')
  
def register(request):
    logger = logging.getLogger(__name__)

    
    

    context = {
        'country_choices': country_choices
    }


    if request.method == 'POST':
        # Get form values
        title = request.POST.get('title')

        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        company = request.POST['company']
        address = request.POST['address']

        zipcode = request.POST['zipcode']
        city = request.POST['city']

        country = request.POST['country']
        
        website = request.POST.get('website')

        tel = request.POST['tel']
        mobile = request.POST['mobile']

        fax = request.POST['fax']

        # username = request.POST['username']
        email = request.POST['email']

        password = request.POST['password']
        password2 = request.POST['password2']

        # full_name = request.POST.get('full_name', 'enter your name')  # ['full_name']

        # Check if password match
        if password == password2:
            # Check email
            
            User = get_user_model()
            # Check Email
            if User.objects.filter(email=email).exists():
                logger.error('Something went wrong!')
                messages.error(request, 'That email is being used.')
                return redirect('register', context)
            else:

                # Check the zipcode
                # if len(zipcode) < 5 or  len(zipcode) > 12: 
                #     messages.error(request, 'Wrong Zipcode format. ( 5 - 12 characters)')
                #     return redirect('register')
                # else:
                #     # Check the phone number
                #     if len(phoneNumber) > 17 or len(phoneNumber) < 12:
                #         messages.error(request, 'Wrong Phonenumber format. +X-XXX-XXX-XXXX or XXX-XXX-XXX-XXXX')
                #         return redirect('register')
                #     else:
                # phoneNumber[0] != '+' or 
                if tel[0] not in  ['0', '1', '2',   
                                                                            '3', '4', '5',
                                                                            '6', '7', '8',
                                                                            '9']:
                    messages.error(request, 'Wrong Phonenumber format. it should contains only digits.')
                    return redirect('register', context)

                else:

                    user_id = generate_code(country)
                    # print('user_id: ', user_id)



                    user = User.objects.create_user(
                                            password=password,
                                            email=email,
                                            first_name=first_name,
                                            last_name=last_name,
                                            user_id=user_id,
                                            title=title,
                                            company=company,
                                            address=address,
                                            zipcode=zipcode,
                                            city=city,
                                            country=country,
                                            website=website,
                                            tel=tel,
                                            mobile=mobile,
                                            fax=fax,
                                            is_promoted=False,
                                            previous_visit=datetime.now(),
                                            current_visit=datetime.now())
                                                    
                    ''' Begin reCAPTCHA validation '''
                    recaptcha_response = request.POST.get('g-recaptcha-response')
                    url = 'https://www.google.com/recaptcha/api/siteverify'
                    values = {
                            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY_REGISTER,
                            'response': recaptcha_response
                        }
                    data = urllib.parse.urlencode(values).encode()
                    req =  urllib.request.Request(url, data=data)
                    response = urllib.request.urlopen(req)
                    result = json.loads(response.read().decode())
                    ''' End reCAPTCHA validation '''
                    

                # # Login after register
                # # auth.login(request, user)
                # # messages.success(request, 'You are now logged in')
                # # return redirect('index')
                if result['success']:
                    user.save()
                    admin_list = User.objects.filter(is_superuser__icontains=True)
                    admin_emails = []
                    for u in admin_list:
                        admin_emails.append(u.email)
                    message = user.get_info()
                    send_mail(
                            'New Registration',
                            'A new user has been registered with following information.\n' + str(message) + '\nSign into the admin panel for more info.\n'  ,
                            'hw.fbuser@gmail.com',
                            admin_emails,
                            fail_silently=False)
                    # logger.error('Something went wrong!')
                    return redirect('log_in')
                else:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                    return redirect('register', context)
                        
                
                

        else:
            messages.error(request, 'Passwords doesnt match!')
            return redirect('register', context)
    else:
        return render(request, 'users/register.html', context)

   
def mylogin(request):
    # logger = logging.getLogger(__name__)
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
            messages.success(request, 'You are now logged in')
            # return redirect('dashboard')
            return redirect('index')
            # return render(request, 'users/my_products.html')
        else:
            # logger.error('Something went wrong!')
            messages.error(request, 'Invalid credentials.')
            # return redirect('log_in')
            return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html')


def mylogout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')
    else:
        # pass
        messages.error(request, 'Unknown error!!!')
        return redirect('index')

@login_required
def student_view_department_courses(request):
    try:
        this_user = Student.objects.get(user=request.user)
        print("\n\n\n\nstudent found\n\n\n\n")
    except:
        print("\n\n\n\n\nno student found!\n\n\n\n")
    
    
    
    queryset = Course.objects.filter(dept_name=this_user.dept_name)
    
  

    context = {
        "courses": queryset,
    }
    return render(request, 'users/student_view_department_courses.html', context)

@login_required
def instructor_view_department_courses(request):
    
    try:
        this_user = Instructor.objects.get(user=request.user)
        # print("\n\n\n\nstudent found\n\n\n\n")
    except:
        print("\n\n\n\n\nno instructor found!\n\n\n\n")
    
    
    
    queryset = Course.objects.filter(dept_name=this_user.dept_name)
    
    
    context = {
        "courses": queryset,
    }
    return render(request, 'users/student_view_department_courses.html', context)


@login_required
def student_register_course(request):
    
    try:
        this_user = Student.objects.get(user=request.user)
        # print("\n\n\n\nstudent found\n\n\n{}\n".format(this_user.dept_name))
    except:
        pass
        # print("\n\n\n\n\nno instructor found!\n\n\n\n")
    
    
    student_courses = Course.objects.filter(dept_name=this_user.dept_name)
    ids = []
    for item in student_courses:
        # print(item.courseid)
        ids.append(item.courseid)
    # print(ids)
    queryset = Section.objects.filter(courseid__in=ids)
    
    
    context = {
        "this_user_department": this_user.dept_name,
        "sections": queryset,
    }
    
    return render(request, 'users/student_register_course.html', context)
