#forms.py
from django import forms
from django.urls import reverse_lazy
from .models import Resume, Education, Experience, Skill, Project, Certification
import pycountry

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


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = [
            'title', 'full_name', 'email', 'phone', 'phone_country_code',
            'address', 'summary', 'github_url', 'linkedin_url',
            'country', 'state'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'e.g., Software Engineer'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': '123-456-7890'
            }),
            'phone_country_code': forms.Select(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
                'placeholder': 'Your address'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Brief summary about yourself'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'https://github.com/yourusername'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'https://linkedin.com/in/yourusername'
            }),
            'country': forms.Select(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'id': 'id_country'
            }),
            'state': forms.Select(attrs={
                'class': 'w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                'id': 'id_state'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set up country choices
        country_choices = [('', 'Select Country')]
        for country in pycountry.countries:
            country_choices.append((country.alpha_3, country.name))
        country_choices.sort(key=lambda x: x[1])
        self.fields['country'].widget.choices = country_choices
        
        # Set up phone country code choices
        phone_code_choices = [('', 'Country Code')]
        calling_codes = {
            'USA': '+1', 'CAN': '+1', 'GBR': '+44', 'DEU': '+49', 'FRA': '+33',
            'ITA': '+39', 'ESP': '+34', 'AUS': '+61', 'JPN': '+81', 'CHN': '+86',
            'IND': '+91', 'BRA': '+55', 'RUS': '+7', 'MEX': '+52', 'ARG': '+54',
            'NLD': '+31', 'BEL': '+32', 'CHE': '+41', 'AUT': '+43', 'SWE': '+46',
            'NOR': '+47', 'DNK': '+45', 'FIN': '+358', 'POL': '+48', 'CZE': '+420',
            'HUN': '+36', 'PRT': '+351', 'GRC': '+30', 'TUR': '+90', 'ZAF': '+27',
            'EGY': '+20', 'NGA': '+234', 'KEN': '+254', 'SGP': '+65', 'MYS': '+60',
            'THA': '+66', 'VNM': '+84', 'PHL': '+63', 'IDN': '+62', 'KOR': '+82',
            'TWN': '+886', 'HKG': '+852', 'MAC': '+853', 'ARE': '+971', 'SAU': '+966',
            'ISR': '+972', 'JOR': '+962', 'LBN': '+961', 'IRQ': '+964', 'IRN': '+98',
            'PAK': '+92', 'BGD': '+880', 'LKA': '+94', 'NPL': '+977', 'AFG': '+93',
            'UZB': '+998', 'KAZ': '+7', 'KGZ': '+996', 'TJK': '+992', 'TKM': '+993',
        }
        
        for country in pycountry.countries:
            code = calling_codes.get(country.alpha_3, '')
            if code:
                phone_code_choices.append((code, f"{code} ({country.name})"))
        
        phone_code_choices.sort(key=lambda x: x[1])
        self.fields['phone_country_code'].widget.choices = phone_code_choices
        
        # Initialize state field
        self.fields['state'].widget.choices = [('', 'Select State')]
        
        # If editing existing instance and has country, populate states
        if self.instance and self.instance.pk and self.instance.country:
            try:
                # Get states for the selected country
                state_choices = [('', 'Select State')]
                for subdivision in pycountry.subdivisions:
                    if subdivision.country_code == self.instance.country[:2]:  # Use first 2 chars for alpha-2
                        state_choices.append((subdivision.code, subdivision.name))
                state_choices.sort(key=lambda x: x[1])
                self.fields['state'].widget.choices = state_choices
            except:
                pass
        
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