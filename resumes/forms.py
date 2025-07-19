#forms.py
from django import forms
from django.urls import reverse_lazy
from .models import Resume, Education, Experience, Skill, Project, Certification
import pycountry
from django_countries.widgets import CountrySelectWidget

CHENNAI_COLLEGES = [
    ('IIT Madras', 'IIT Madras'),
    ('Anna University', 'Anna University'),
    ('SRM Institute of Science and Technology', 'SRM IST'),
    ('VIT Chennai', 'VIT Chennai'),
    ('Sathyabama Institute of Science and Technology', 'Sathyabama'),
    ('Loyola College', 'Loyola College'),
    ('MCC', 'Madras Christian College'),
    ('CEG', 'College of Engineering, Guindy'),
    ('SSN', 'SSN College of Engineering'),
    ('Other', 'Other'),
]

# Define countries and states manually
COUNTRIES = [
    ('', 'Select Country'),
    ('India', 'India'),
    ('United States', 'United States'),
    ('Canada', 'Canada'),
    
]

STATES_BY_COUNTRY = {
    'India': [
        ('', 'Select State'),
        ('Delhi', 'Delhi'),
        ('Maharashtra', 'Maharashtra'),
        ('Karnataka', 'Karnataka'),
        ('Tamil Nadu', 'Tamil Nadu'),
    ],
    'United States': [
        ('', 'Select State'),
        ('California', 'California'),
        ('New York', 'New York'),
        ('Texas', 'Texas'),
        ('Florida', 'Florida'),
    ],
    'Canada': [
        ('', 'Select Province'),
        ('Ontario', 'Ontario'),
        ('Quebec', 'Quebec'),
        ('British Columbia', 'British Columbia'),
        ('Alberta', 'Alberta'),
    ],
}

PHONE_COUNTRY_CODES = [
    ('+1', 'USA (+1)'),
    ('+91', 'India (+91)'),
    ('+44', 'UK (+44)'),
    ('+61', 'Australia (+61)'),
    ('+81', 'Japan (+81)'),
    ('+49', 'Germany (+49)'),
    ('+33', 'France (+33)'),
    ('+86', 'China (+86)'),
    ('+971', 'UAE (+971)'),
    ('+65', 'Singapore (+65)'),
    ('+94', 'Sri Lanka (+94)'),
    ('+880', 'Bangladesh (+880)'),
    ('+92', 'Pakistan (+92)'),
    ('+7', 'Russia (+7)'),
    ('+82', 'South Korea (+82)'),
    ('+39', 'Italy (+39)'),
    ('+34', 'Spain (+34)'),
    ('+46', 'Sweden (+46)'),
    ('+41', 'Switzerland (+41)'),
    ('+27', 'South Africa (+27)'),
    ('+32', 'Belgium (+32)'),
    ('+31', 'Netherlands (+31)'),
    ('+966', 'Saudi Arabia (+966)'),
    ('+20', 'Egypt (+20)'),
    ('+351', 'Portugal (+351)'),
    ('+353', 'Ireland (+353)'),
    ('+52', 'Mexico (+52)'),
    ('+48', 'Poland (+48)'),
    ('+380', 'Ukraine (+380)'),
    ('+62', 'Indonesia (+62)'),
    ('+60', 'Malaysia (+60)'),
]


class ResumeForm(forms.ModelForm):
    phone_country_code = forms.ChoiceField(
        choices=PHONE_COUNTRY_CODES,
        initial='+1',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'style': 'width: 100px;'
        })
    )

    class Meta:
        model = Resume
        fields = [
            'title', 'full_name', 'email', 'phone_country_code','phone', 'address', 'summary', 'github_url', 
            'linkedin_url', 'country', 'state'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Software Engineer'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your.email@example.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '123-456-7890'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Your address'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Brief summary about yourself'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://github.com/yourusername'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://linkedin.com/in/yourusername'
            }),
            'country': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_country'
            }),
            'state': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_state'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up country choices
        self.fields['country'].choices = COUNTRIES
        
        # Initialize state field
        self.fields['state'].choices = [('', 'Select State')]
        
        # If editing existing instance and has country, populate states
        if self.instance and self.instance.pk and self.instance.country:
            states = STATES_BY_COUNTRY.get(self.instance.country, [])
            self.fields['state'].choices = states
        
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'branch', 'start_date', 'end_date', 'description', 'subjects', 'percentage', 'cgpa', 'is_current']
        widgets = {
            'institution': forms.Select(choices=CHENNAI_COLLEGES),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'subjects': forms.TextInput(attrs={'placeholder': 'Math, Physics, Chemistry'}),
            'percentage': forms.NumberInput(attrs={'step': '0.01'}),
            'cgpa': forms.NumberInput(attrs={'step': '0.01'}),
        }

class ExperienceForm(forms.ModelForm):
    """Form for work experience"""
    class Meta:
        model = Experience
        fields = ['company','position','location','start_date','end_date','description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date': forms.DateInput(attrs={'type':'date'}),
            'description': forms.Textarea(attrs={'rows':'3'}),
        }

class SkillForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input skill-input',
            'placeholder': 'Search or Add skills',
            'autocomplete': 'off'
            })
        )
    class Meta:
        model = Skill
        fields = ['name']

class ProjectForm(forms.ModelForm):
    """Form for projects"""
    class Meta:
        model = Project
        fields = ['title', 'description', 'technologies','url','start_date','end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type':'date'}),
            'end_date': forms.DateInput(attrs={'type':'date'}),
            'description': forms.Textarea(attrs={'rows':'3'}),
        }

class CertificationForm(forms.ModelForm):
    """Form for certifications"""
    class Meta: 
        model = Certification
        fields = ['name','organization','date_obtained','expiry_date','credential_id']
        widgets = {
            'date_obtained': forms.DateInput(attrs={'type':'date'}),
            'expiry_date': forms.DateInput(attrs={'type':'date'}),
        }       