from django.http import HttpResponse
from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request,'index.html')

def aboutus(request):
    return render(request,'about.html')



def coordinator_dashboard(request):
    return render(request, 'pdashboard.html')


def add_company(request):
    if request.method == "POST":
        name = request.POST.get('name')
        place = request.POST.get('place')
        street = request.POST.get('street')
        pincode = request.POST.get('pincode')
        district = request.POST.get('district')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')

        # Save company details to database
        company = Company(
            name=name,
            place=place,
            street=street,
            pincode=pincode,
            district=district,
            contact_number=contact_number,
            email=email
        )
        company.save()
        
        return redirect('displaycompany')  # Redirect to display company page

    return render(request, 'addcompany.html')
from django.shortcuts import render, redirect
from .models import Company
from django.http import HttpResponse

# Display all companies
def display_company(request):
    companies = Company.objects.all()  # Fetch all companies from database
    return render(request, 'displaycompany.html', {'companies': companies})

# Delete a company
def delete_company(request, company_id):
    try:
        company = Company.objects.get(id=company_id)
        company.delete()
        return redirect('displaycompany')  # Redirect back to the company list page
    except Company.DoesNotExist:
        return HttpResponse("Company not found", status=404)



from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import PlacementForm

def add_placement(request):
    if request.method == "POST":
        form = PlacementForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('displayplacement')  # Redirect to placement display page
    else:
        form = PlacementForm()

    return render(request, 'addplacement.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Placement, PlacementApplication

def display_placements(request):
    placements = Placement.objects.all()
    return render(request, 'displayplacement.html', {'placements': placements})

def view_applicants(request, placement_id):
    # Fetch the specific placement
    placement = get_object_or_404(Placement, id=placement_id)
    # Fetch all applications for this placement
    applications = PlacementApplication.objects.filter(placement=placement)
    # Extract student details
    applicants = [
        {"name": application.student.first_name, "email": application.student.email}
        for application in applications
    ]
    return render(request, 'view_applicants.html', {
        'placement': placement,
        'applicants': applicants,
    })


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import StudentSignupForm
from .models import Student

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import StudentSignupForm
from django.db import IntegrityError  

def studentsignup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            try:
                # Check for unique email
                if User.objects.filter(email=form.cleaned_data.get('email')).exists():
                    form.add_error('email', 'This email is already registered. Please use a different email.')
                    return render(request, 'signup.html', {'form': form})

                # Create user
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    email=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password')
                )

                # Save additional student details
                Student.objects.create(
                    user=user,
                    name=form.cleaned_data.get('name'),
                    gender=form.cleaned_data.get('gender'),
                    date_of_birth=form.cleaned_data.get('date_of_birth'),
                    contact_number=form.cleaned_data.get('contact_number'),
                    email=form.cleaned_data.get('email'),
                    department=form.cleaned_data.get('department'),
                )

                # Send success email
                subject = "Welcome to Marian Placement Platform!"
                message = f"Hello {user.username},\n\nThank you for registering with us. Your account has been successfully created."
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


                return redirect('student_login')  # Redirect to login page after successful signup

            except IntegrityError as e:
                form.add_error(None, 'An error occurred while creating your account. Please try again.')

    else:
        form = StudentSignupForm()

    return render(request, 'signup.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth.models import User

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_superuser:
                # Redirect to the displayplacement page if the user is a superuser
                return redirect('displayplacement')
            else:
                # Redirect to the updateprofile page if the user is a student
                return redirect('updateprofile')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

from django.shortcuts import render

def student_dashboard(request):
    return render(request, 'student.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentProfileUpdateForm
from .models import Student
from django.contrib.auth.decorators import login_required
@login_required
def update_profile(request):
    student = Student.objects.get(user=request.user)

    if request.method == 'POST':
        form = StudentProfileUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('applied_placements')  # Redirect to dashboard after updating
    else:
        form = StudentProfileUpdateForm(instance=student)

    return render(request, 'updateprofile.html', {'form': form})

from .models import Placement, PlacementApplication
from django.contrib.auth.decorators import login_required

from datetime import date
from django.shortcuts import render
from .models import Placement, PlacementApplication

def student_placements_view(request):
    # Fetch placements and applied placements
    placements = Placement.objects.all()
    applied_placements = PlacementApplication.objects.filter(student=request.user)

    # Add the current date to the context
    context = {
        'placements': placements,
        'applied_placements': applied_placements,
        'current_date': date.today(),  # Pass the current date to the template
    }

    return render(request, 'studentplacements.html', context)

@login_required
def apply_for_placement(request, placement_id):
    placement = Placement.objects.get(id=placement_id)

    # Check if the student already applied
    if not PlacementApplication.objects.filter(student=request.user, placement=placement).exists():
        PlacementApplication.objects.create(student=request.user, placement=placement)
        messages.success(request, "You have successfully applied for this placement!")
    else:
        messages.error(request, "You have already applied for this placement.")

    return redirect('studentplacements')
from django.shortcuts import render, get_object_or_404
from .models import Placement, PlacementApplication, Student
from .forms import ApplicantFilterForm

def view_applicants(request, placement_id):
    # Fetch the placement
    placement = get_object_or_404(Placement, id=placement_id)

    # Fetch all applications for the placement
    applications = PlacementApplication.objects.filter(placement=placement)

    # Filter applicants based on form input
    applicants = []
    
    # Initialize the filter form
    filter_form = ApplicantFilterForm(request.GET)
    
    if filter_form.is_valid():
        ug_percentage_min = filter_form.cleaned_data.get('ug_percentage_min')
        pg_percentage_min = filter_form.cleaned_data.get('pg_percentage_min')
        ug_percentage_max = filter_form.cleaned_data.get('ug_percentage_max')
        pg_percentage_max = filter_form.cleaned_data.get('pg_percentage_max')
        
        # Apply filters if the form data is provided
        for application in applications:
            student_profile = Student.objects.filter(user=application.student).first()
            if student_profile:
                if (
                    (ug_percentage_min is None or student_profile.ug_percentage >= ug_percentage_min) and
                    (pg_percentage_min is None or student_profile.pg_percentage >= pg_percentage_min) and
                    (ug_percentage_max is None or student_profile.ug_percentage <= ug_percentage_max) and
                    (pg_percentage_max is None or student_profile.pg_percentage <= pg_percentage_max)
                ):
                    applicants.append({
                        'name': student_profile.name,
                        'gender': student_profile.gender,
                        'date_of_birth': student_profile.date_of_birth,
                        'contact_number': student_profile.contact_number,
                        'email': student_profile.email,
                        'sslc_percentage': student_profile.sslc_percentage,
                        'sslc_year': student_profile.sslc_year,
                        'hsc_percentage': student_profile.hsc_percentage,
                        'hsc_year': student_profile.hsc_year,
                        'ug_percentage': student_profile.ug_percentage,
                        'ug_year': student_profile.ug_year,
                        'pg_percentage': student_profile.pg_percentage,
                        'pg_year': student_profile.pg_year,
                        'skills': student_profile.skills,
                        'resume': student_profile.resume,
                        'image': student_profile.image,
                    })

    # Render the template with placement and applicants data
    return render(request, 'view_applicants.html', {
        'placement': placement,
        'applicants': applicants,
        'filter_form': filter_form,
    })



from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Placement, PlacementApplication


# View for applied placements
def applied_placements(request):
    applied_placements = PlacementApplication.objects.filter(student=request.user)

    context = {
        'applied_placements': applied_placements,
        'now': timezone.now()  # Pass current time to the template for comparison
    }
    return render(request, 'applied_placements.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import PlacementApplication

# View for canceling the placement application
def cancel_application(request, application_id):
    application = get_object_or_404(PlacementApplication, id=application_id)

    # Check if the application was made within 1 day
    if application.application_date >= timezone.now() - timedelta(days=1):
        # Delete the application
        application.delete()
        messages.success(request, "Your application has been successfully canceled.")
    else:
        messages.error(request, "You cannot cancel your application after 24 hours.")
    
    return redirect('studentplacements')

from django.shortcuts import render
from .models import Student

def student_profiles(request):
    students = Student.objects.all()  # Fetch all student profiles
    return render(request, 'student_profiles.html', {'students': students})


import pandas as pd
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Placement, PlacementApplication, Student
from .forms import ApplicantFilterForm

def export_filtered_applicants_to_excel(request, placement_id):
    # Fetch the placement
    placement = get_object_or_404(Placement, id=placement_id)

    # Fetch all applications for the placement
    applications = PlacementApplication.objects.filter(placement=placement)

    # Initialize filter criteria from the form or GET parameters
    filter_form = ApplicantFilterForm(request.GET)

    applicants = []
    if filter_form.is_valid():
        ug_percentage_min = filter_form.cleaned_data.get('ug_percentage_min')
        pg_percentage_min = filter_form.cleaned_data.get('pg_percentage_min')
        ug_percentage_max = filter_form.cleaned_data.get('ug_percentage_max')
        pg_percentage_max = filter_form.cleaned_data.get('pg_percentage_max')

        # Apply filters and collect the filtered applicants
        for application in applications:
            student_profile = Student.objects.filter(user=application.student).first()
            if student_profile:
                if (
                    (ug_percentage_min is None or student_profile.ug_percentage >= ug_percentage_min) and
                    (pg_percentage_min is None or student_profile.pg_percentage >= pg_percentage_min) and
                    (ug_percentage_max is None or student_profile.ug_percentage <= ug_percentage_max) and
                    (pg_percentage_max is None or student_profile.pg_percentage <= pg_percentage_max)
                ):
                    applicants.append({
                        'name': student_profile.name,
                        'gender': student_profile.gender,
                        'date_of_birth': student_profile.date_of_birth,
                        'contact_number': student_profile.contact_number,
                        'email': student_profile.email,
                        'sslc_percentage': student_profile.sslc_percentage,
                        'sslc_year': student_profile.sslc_year,
                        'hsc_percentage': student_profile.hsc_percentage,
                        'hsc_year': student_profile.hsc_year,
                        'ug_percentage': student_profile.ug_percentage,
                        'ug_year': student_profile.ug_year,
                        'pg_percentage': student_profile.pg_percentage,
                        'pg_year': student_profile.pg_year,
                        'skills': student_profile.skills,
                        'resume': student_profile.resume.url if student_profile.resume else 'No Resume',
                        'image': student_profile.image.url if student_profile.image else 'No Image',
                    })

    # Create a pandas DataFrame from the filtered applicants list
    df = pd.DataFrame(applicants)

    # Create the HTTP response to serve the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=filtered_applicants_{placement.title}.xlsx'

    # Write the DataFrame to the Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

from django.shortcuts import render, redirect
from .forms import PlacedStudentForm
from .models import PlacedStudent
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def add_placed_student(request):
    if request.method == 'POST':
        form = PlacedStudentForm(request.POST)
        if form.is_valid():
            # Get form data
            student_name = form.cleaned_data['name']
            student_email = form.cleaned_data['email']
            department = form.cleaned_data['department']
            company = form.cleaned_data['company']
            position = form.cleaned_data['position']
            contact_number = form.cleaned_data['contact_number']
            placed_year = form.cleaned_data['placed_year']

            # Check if the student already exists based on name and email
            existing_student = PlacedStudent.objects.filter(name=student_name, email=student_email).exists()

            if existing_student:
                # If student already exists, show message and don't save
                messages.warning(request, f"{student_name} is already placed in the system.")
            else:
                # Save the new placed student
                new_placed_student = form.save()

               
                messages.success(request, f"{student_name} has been successfully added to the placed students list.")

                return redirect('display_placed_students')  # Redirect to display page after successful addition

    else:
        form = PlacedStudentForm()

    return render(request, 'add_placed_student.html', {'form': form})


from django.shortcuts import render
from .models import PlacedStudent
import csv
from django.http import HttpResponse
import csv
from django.http import HttpResponse

def display_placed_students(request):
    # Get filter parameters
    department_filter = request.GET.get('department')
    placed_year_filter = request.GET.get('placed_year')

    # Get all placed students
    placed_students = PlacedStudent.objects.all()

    # Apply filters if provided
    if department_filter:
        placed_students = placed_students.filter(department=department_filter)
    if placed_year_filter:
        placed_students = placed_students.filter(placed_year=placed_year_filter)

    context = {
        'placed_students': placed_students,
        'department_filter': department_filter,
        'placed_year_filter': placed_year_filter
    }

    # Check if the "Download CSV" button was clicked
    if request.GET.get('download_csv'):
        return download_csv(PlacedStudent.objects.all())  # Ensure all students are included

    return render(request, 'display_placed_students.html', context)

def download_csv(placed_students):
    # Prepare the response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=placed_students.csv'
    
    # Create a CSV writer object
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow(['Name', 'Department', 'Company', 'Position', 'Contact Number', 'Email', 'Placed Year'])
    
    # Write the data rows
    for student in placed_students:
        writer.writerow([student.name, student.department, student.company.name, student.position,
                         student.contact_number, student.email, student.placed_year])
    
    return response
from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse

def placements_by_year(request):
    # Prepare data for both charts
    placed_by_year = PlacedStudent.objects.values('placed_year').annotate(count=Count('id'))
    data_by_year = {entry['placed_year']: entry['count'] for entry in placed_by_year}

    placed_by_dept_year = PlacedStudent.objects.values('placed_year', 'department').annotate(count=Count('id'))
    data_by_dept_year = {}
    for entry in placed_by_dept_year:
        year = entry['placed_year']
        dept = entry['department']
        count = entry['count']
        if year not in data_by_dept_year:
            data_by_dept_year[year] = {}
        data_by_dept_year[year][dept] = count

    context = {
        'data_by_year': data_by_year,
        'data_by_dept_year': data_by_dept_year,
    }
    return render(request, 'placements_by_year.html', context)

# API to fetch updated chart data based on the selected year
def get_chart_data(request):
    year = int(request.GET.get('year', 0))

    # Data for students placed in the selected year
    placed_students_in_year = PlacedStudent.objects.filter(placed_year=year).values('department').annotate(count=Count('id'))
    dept_data = {entry['department']: entry['count'] for entry in placed_students_in_year}

    return JsonResponse({
        'year': year,
        'dept_data': dept_data,
    })


from django.contrib.auth import logout
from django.shortcuts import redirect

def student_logout(request):
    logout(request)  # Log the user out
    return redirect('home')  # Redirect to the login page



from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate reset token
                token = default_token_generator.make_token(user)
                
                # Ensure user.pk is encoded as a string
                uid = urlsafe_base64_encode(str(user.pk).encode())

                # Send email with reset link
                domain = get_current_site(request).domain
                reset_link = f"http://{domain}/reset/{uid}/{token}/"
                message = render_to_string('password_reset_email.html', {'reset_link': reset_link})
                send_mail("Password Reset Request", message, 'aleeshasibi26@gmail.com', [email])
                
                return redirect('password_reset_done')
            except User.DoesNotExist:
                messages.error(request, "No user found with that email address.")
    
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset_request.html', {'form': form})




from django.shortcuts import render

def password_reset_done(request):
    return render(request, 'password_reset_done.html')


from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('password_reset_complete')
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect('password_reset')


from django.shortcuts import render

def password_reset_complete(request):
    return render(request, 'login.html')

from django.shortcuts import render
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract the cleaned data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send the email (example: sending to an admin email)
            send_mail(
                subject=f"Contact Us: {subject}",
                message=f"Message from {name} ({email}):\n\n{message}",
                from_email=email,
                recipient_list=[settings.EMAIL_HOST_USER],  # Add admin email here
            )
            
            # Optionally, you can add a success message
            return render(request, 'contact.html', {'form': form, 'success': True})

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
