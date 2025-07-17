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
                'placeholder': 'e.g. Backend Developer',
                'class': 'block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
            }),
            'summary': forms.Textarea(attrs={
                'rows': 4,
                'class': 'block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
            }),
            'github_url': forms.URLInput(attrs={
                'placeholder': 'https://github.com/username',
                'class': 'block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'placeholder': 'https://linkedin.com/in/username',
                'class': 'block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
            }),
            'phone_country_code': forms.Select(
                choices=[('', 'Select Code')] + [
                    (c.alpha_2, f"{c.name} (+{c.numeric})") for c in pycountry.countries
                ],
                attrs={
                    'class': 'block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
                }
            ),
            'country': forms.Select(
                choices=[('', 'Select Country')] + [
                    (c.alpha_2, c.name) for c in pycountry.countries
                ],
                attrs={
                    'id': 'id_country',
                    'class': 'block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                }
            ),
            'state': forms.Select(
                choices=[('', 'Select State')],
                attrs={
                    'id': 'id_state',
                    'disabled': True,
                    'class': 'block w-full px-3 py-2.5 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically populate state dropdown if editing existing resume
        if self.instance and self.instance.country:
            try:
                subdivisions = pycountry.subdivisions.get(country_code=self.instance.country.upper())
                self.fields['state'].widget.choices = [('', 'Select State')] + [
                    (s.code, s.name) for s in subdivisions
                ]
                self.fields['state'].widget.attrs.pop('disabled', None)
            except Exception:
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