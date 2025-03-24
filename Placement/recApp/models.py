from django.db import models

# Create your models here.
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    district = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Placement(models.Model):
    title = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default=1)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    position = models.CharField(max_length=50)
    job_description = models.TextField()
    date_of_drive = models.DateField(null=True, blank=True,verbose_name="Drive Date")
    salary_package = models.DecimalField(max_digits=10, decimal_places=2)
    last_date_to_apply = models.DateField(null=True, blank=True)
    application_link = models.URLField(max_length=200, null=True, blank=True)
    recruitment_type = models.CharField(max_length=50, default="Offline") 

    def __str__(self):
        return f"{self.title} - {self.company.name}"

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, RegexValidator

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Unknown")
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    department = models.CharField(max_length=100, choices=[
        ('MCA', 'MCA'), ('MBA', 'MBA'), ('MMH', 'MMH'),
        ('MSW', 'MSW'), ('BBA', 'BBA'), ('B.COM', 'B.COM')
    ])

    # Academic year in the format 'YYYY-YYYY'
    academic_year = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{4}-\d{4}$', message="Enter a valid academic year range, e.g., 2023-2025")],
        null=True, blank=True
    )

    sslc_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sslc_year = models.IntegerField(null=True, blank=True)
    hsc_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hsc_year = models.IntegerField(null=True, blank=True)
    ug_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ug_year = models.IntegerField(null=True, blank=True)
    pg_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    pg_year = models.IntegerField(null=True, blank=True)

    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])], null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    is_placed = models.BooleanField(default=False)  # Field to track placement status

    def __str__(self):
        return f"{self.user.username} - {self.department}"


from django.contrib.auth.models import User  # Assuming students use Django's User model

class PlacementApplication(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    placement = models.ForeignKey(Placement, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.placement.title}"


class PlacedStudent(models.Model):

    name = models.CharField(max_length=100, verbose_name="Student Name", null=True, blank=True)

    department = models.CharField(
    max_length=100, 
    choices=[
        ('MCA', 'MCA'), 
        ('MBA', 'MBA'), 
        ('MMH', 'MMH'), 
        ('MSW', 'MSW'), 
        ('BBA', 'BBA'), 
        ('B.COM', 'B.COM')
    ],
    null=True, 
    blank=True
)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    email = models.EmailField(null=True, blank=True)

    placed_year = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.company.name}"

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class StudentPlacementRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    department = models.CharField(
        max_length=100,
        choices=[('MCA', 'MCA'), ('MBA', 'MBA'), ('MMH', 'MMH'),
                 ('MSW', 'MSW'), ('BBA', 'BBA'), ('B.COM', 'B.COM')]
    )
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField()
    placed_year = models.IntegerField()
    offer_letter = models.FileField(upload_to='offer_letters/', 
                                    validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])], 
                                    null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.name} - {self.company} ({self.status})"
