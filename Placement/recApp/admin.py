from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Company,Placement,Student

# Customizing the admin interface for the Company model
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'place', 'district', 'pincode', 'contact_number', 'email')  # Fields to display in the admin list view
    search_fields = ('name', 'place', 'district', 'email')  # Fields to enable search functionality
    list_filter = ('district',)  # Fields to enable filtering options
    ordering = ('name',)  # Default ordering by company name
    fieldsets = (
        (None, {
            'fields': ('name', 'place', 'street', 'pincode', 'district', 'contact_number', 'email')
        }),
    )


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'position', 'date_of_drive', 'salary_package')  # Customize columns
    list_filter = ('company', 'date_of_drive')  # Add filter optionsfrom django.contrib import admin



# Customizing the admin interface for the Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'contact_number', 'email')  # Display essential student details
    search_fields = ('name', 'department', 'email', 'contact_number')  # Search by name, department, email, or contact number
    list_filter = ('department', 'gender')  # Filter by department and gender
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'name', 'gender', 'date_of_birth', 'contact_number', 'email')
        }),
        ('Educational Details', {
            'fields': ('department', 'sslc_percentage', 'sslc_year', 
                       'hsc_percentage', 'hsc_year', 'ug_percentage', 'ug_year', 
                       'pg_percentage', 'pg_year')
        }),
        ('Other Details', {
            'fields': ('skills', 'resume', 'image')
        }),
    )
    ordering = ('name',)  # Default ordering by student name





from .models import Company, Placement, Student, PlacementApplication, Notification, PlacedStudent

# Customizing the admin interface for the PlacedStudent model
@admin.register(PlacedStudent)
class PlacedStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'company', 'position', 'placed_year')  # Display details of placed students
    search_fields = ('name', 'department', 'company__name')  # Enable search by name, department, or company
    list_filter = ('department', 'placed_year', 'company')  # Add filters for department, year, and company
    ordering = ('-placed_year',)  # Default ordering by the latest placement year