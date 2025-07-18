from django.db import models
from django.contrib.auth.models import User
import pycountry
from django_countries.fields import CountryField

class Skill(models.Model):
    """Model to store skills"""
    CATEGORY_CHOICES = [
        ('programming', 'Programming Languages'),
        ('framework', 'Frameworks & Libraries'),
        ('frontend', 'Frontend Technologies'),
        ('backend', 'Backend Technologies'),
        ('database', 'Databases'),
        ('devops', 'DevOps & Cloud'),
        ('mobile', 'Mobile Development'),
        ('testing', 'Testing'),
        ('tools', 'Development Tools'),
    ]

    name = models.CharField(max_length=50, unique=True, db_index=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)
    popularity = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']
       
    def __str__(self):
        return self.name
    
class Resume(models.Model):
    """Model to store basic resume info"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100, verbose_name="Job Title", help_text="e.g., Backend Developer, Frontend Engineer")
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    phone_country_code = models.CharField(max_length=5, default='+1')
    portfolio_url = models.URLField(blank=True, null=True)
    country = CountryField(blank_label='(Select Country)')
    state = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    
    TEMPLATE_CHOICES = [
    ('classic', 'Classic'),
    ('modern', 'Modern'),
    ('creative', 'Creative'),
    ('professional', 'Professional'),
    ('ats', 'ATS-Friendly'),
    ('elegant', 'Elegant'),
]

    template = models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='classic')

    class Meta:
        ordering = ['-updated_at'] 

    def get_country_name(self):
        try:
            return pycountry.countries.get(alpha_2=self.country).name
        except:
            return None

    @property
    def skills_list(self):
        return list(self.skills.values_list('name', flat=True))    

class Education(models.Model):
    """Model to store education info"""
    DEGREE_CHOICES = [
        # School Education
        ('HIGH_SCHOOL', 'High School'),
        ('SSC', 'Secondary School Certificate'),
        ('HSC', 'Higher Secondary Certificate'),
        ('DIPLOMA', 'Diploma'),
        
        # Undergraduate Degrees
        ('BTECH', 'Bachelor of Technology'),
        ('BE', 'Bachelor of Engineering'),
        ('BSC', 'Bachelor of Science'),
        ('BCOM', 'Bachelor of Commerce'),
        ('BA', 'Bachelor of Arts'),
        ('BBA', 'Bachelor of Business Administration'),
        ('BCA', 'Bachelor of Computer Applications'),
        ('BARCH', 'Bachelor of Architecture'),
        ('LLB', 'Bachelor of Laws'),
        
        # Postgraduate Degrees
        ('MTECH', 'Master of Technology'),
        ('ME', 'Master of Engineering'),
        ('MSC', 'Master of Science'),
        ('MCOM', 'Master of Commerce'),
        ('MA', 'Master of Arts'),
        ('MBA', 'Master of Business Administration'),
        ('MCA', 'Master of Computer Applications'),
        ('MARCH', 'Master of Architecture'),
        ('LLM', 'Master of Laws'),
        ('PHD', 'Doctor of Philosophy'),
    ]

    BRANCH_CHOICES = [
        # School Branches
        ('SCIENCE', 'Science'),
        ('COMMERCE', 'Commerce'),
        ('ARTS', 'Arts'),
        
        # Engineering & Technology
        ('CS', 'Computer Science & Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics & Communication'),
        ('EEE', 'Electrical & Electronics'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('CHEM', 'Chemical Engineering'),
        ('AERO', 'Aeronautical Engineering'),
        ('AUTO', 'Automobile Engineering'),
        
        # Computer Applications
        ('COMP_APP', 'Computer Applications'),
        ('SOFT_DEV', 'Software Development'),
        ('DATA_SCI', 'Data Science'),
        ('AI', 'Artificial Intelligence'),
        ('CYBER', 'Cyber Security'),
        
        # Science
        ('PHYSICS', 'Physics'),
        ('CHEMISTRY', 'Chemistry'),
        ('MATHS', 'Mathematics'),
        ('STATS', 'Statistics'),
        ('BIOTECH', 'Biotechnology'),
        
        # Commerce & Management
        ('ACCOUNT', 'Accountancy'),
        ('FINANCE', 'Finance'),
        ('MARKETING', 'Marketing'),
        ('HR', 'Human Resources'),
        ('ECO', 'Economics'),
        
        # Arts & Humanities
        ('ENGLISH', 'English'),
        ('HISTORY', 'History'),
        ('PSYCH', 'Psychology'),
        ('SOCIO', 'Sociology'),
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,related_name='education')
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100, choices=DEGREE_CHOICES)
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES,null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True) 
    subjects = models.TextField(blank=True, help_text="Comma rated list of major subjects")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    cgpa = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.get_degree_display()} in {self.get_branch_display()} from {self.institution}"

    def get_subjects_list(self):
        return [s.strip() for s in self.subjects.split(',') if s.strip()] 
    
    class Meta:
        ordering = ['-end_date', '-start_date']

class Experience(models.Model): 
    """Model to store work experience information."""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experiences')
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    class Meta:
        ordering = ['-end_date', '-start_date']


    
class Project(models.Model):
    """Model to store projects"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-end_date', '-start_date']

class Certification(models.Model):
    """Model to store certificate"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='certifications')
    name = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    date_obtained = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date_obtained']