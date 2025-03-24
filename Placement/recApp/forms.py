from django import forms
from .models import Company, Placement

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'place', 'district', 'contact_number', 'email','website']

from django import forms
from .models import Placement
from datetime import date

class PlacementForm(forms.ModelForm):
    class Meta:
        model = Placement
        fields = ['title', 'company', 'location', 'email', 'position', 'job_description', 'date_of_drive','recruitment_type', 'last_date_to_apply', 'salary_package','application_link']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default date to today's date for both fields
        self.fields['date_of_drive'].initial = date.today()  # Default to today's date for date_of_drive
        self.fields['last_date_to_apply'].initial = date.today()  # Default to today's date for last_date_to_apply

        # Modify salary package field label to mention CTC
        self.fields['salary_package'].label = "Salary Package (CTC) in LPA"

     # 👉 Add salary_package validation
    def clean_salary_package(self):
        salary = self.cleaned_data.get('salary_package')
        if salary is not None and salary < 0:
            raise forms.ValidationError("Salary package cannot be negative.")
        return salary

from django import forms
from django.contrib.auth.models import User
from .models import Student

from django import forms
from django.contrib.auth.models import User

class StudentSignupForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=True, label="Student Name")
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], required=True)
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    
    email = forms.EmailField(max_length=254, required=True, label="Email Address")
    contact_number = forms.CharField(max_length=15, required=True)
    department = forms.ChoiceField(choices=[
        ('MCA', 'MCA'), 
        ('MBA', 'MBA'), 
        ('MMH', 'MMH'), 
        ('MSW', 'MSW'), 
        ('BBA', 'BBA'), 
        ('B.COM', 'B.COM')
    ], required=True)
    
    username = forms.CharField(max_length=150, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Password")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Please provide a different email.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        return password

from django import forms
from .models import Student
from datetime import datetime
import re

class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'gender', 'date_of_birth', 'contact_number', 'email', 'department',
            
            'sslc_percentage', 'sslc_year', 'hsc_percentage', 'hsc_year', 'ug_percentage', 'ug_year',
            'pg_percentage', 'pg_year', 'resume', 'image', 'skills'
        ]
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'type': 'date'}),
            'resume': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            
        }

    def clean_sslc_percentage(self):
        sslc_percentage = self.cleaned_data.get('sslc_percentage')
        if sslc_percentage is not None and (sslc_percentage < 0 or sslc_percentage > 100):
            raise forms.ValidationError("SSLC percentage must be between 0 and 100.")
        return sslc_percentage

    def clean_hsc_percentage(self):
        hsc_percentage = self.cleaned_data.get('hsc_percentage')
        if hsc_percentage is not None and (hsc_percentage < 0 or hsc_percentage > 100):
            raise forms.ValidationError("HSC percentage must be between 0 and 100.")
        return hsc_percentage

    def clean_ug_percentage(self):
        ug_percentage = self.cleaned_data.get('ug_percentage')
        if ug_percentage is not None and (ug_percentage < 0 or ug_percentage > 100):
            raise forms.ValidationError("UG percentage must be between 0 and 100.")
        return ug_percentage

    def clean_pg_percentage(self):
        pg_percentage = self.cleaned_data.get('pg_percentage')
        if pg_percentage is not None and (pg_percentage < 0 or pg_percentage > 100):
            raise forms.ValidationError("PG percentage must be between 0 and 100.")
        return pg_percentage

    def clean_sslc_year(self):
        sslc_year = self.cleaned_data.get('sslc_year')
        if sslc_year is not None:
            current_year = datetime.now().year
            if sslc_year < 1900 or sslc_year > current_year:
                raise forms.ValidationError(f"SSLC year must be between 1900 and {current_year}.")
        return sslc_year

    def clean_hsc_year(self):
        hsc_year = self.cleaned_data.get('hsc_year')
        if hsc_year is not None:
            current_year = datetime.now().year
            if hsc_year < 1900 or hsc_year > current_year:
                raise forms.ValidationError(f"HSC year must be between 1900 and {current_year}.")
        return hsc_year

    def clean_ug_year(self):
        ug_year = self.cleaned_data.get('ug_year')
        if ug_year is not None:
            current_year = datetime.now().year
            if ug_year < 1900 or ug_year > current_year:
                raise forms.ValidationError(f"UG year must be between 1900 and {current_year}.")
        return ug_year

    def clean_pg_year(self):
        pg_year = self.cleaned_data.get('pg_year')
        if pg_year is not None:
            current_year = datetime.now().year
            if pg_year < 1900 or pg_year > current_year:
                raise forms.ValidationError(f"PG year must be between 1900 and {current_year}.")
        return pg_year

   

from django import forms

class ApplicantFilterForm(forms.Form):
    ug_percentage_min = forms.DecimalField(required=False, label="Minimum UG %", max_digits=5, decimal_places=2)
    pg_percentage_min = forms.DecimalField(required=False, label="Minimum PG %", max_digits=5, decimal_places=2)
    

from django import forms
from .models import PlacedStudent

class PlacedStudentForm(forms.ModelForm):
    class Meta:
        model = PlacedStudent
        fields = ['name', 'department', 'company', 'position', 'contact_number', 'email', 'placed_year']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')

        if PlacedStudent.objects.filter(name=name, email=email).exists():
            raise forms.ValidationError(f"A student with the name '{name}' and email '{email}' is already placed.")

        return cleaned_data


from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your name',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'form-control'
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'placeholder': 'Enter the subject',
        'class': 'form-control'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Enter your message',
        'class': 'form-control',
        'rows': 5
    }))


from django import forms
from .models import StudentPlacementRequest

class StudentPlacementRequestForm(forms.ModelForm):
    class Meta:
        model = StudentPlacementRequest
        exclude = ['status', 'student']  # Students shouldn't set the status
