from django.contrib import messages 
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.http import HttpResponse
from requests import request
from .models import Resume, Education, Experience, Skill, Project, Certification
from .forms import (ResumeForm, EducationForm, ExperienceForm, ProjectForm, CertificationForm)
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q


def get_states(request, country):
    """AJAX endpoint for state dropdown"""
    states = {
        'India': ['Delhi', 'Maharashtra', 'Karnataka'],
        'United States': ['California', 'New York', 'Texas'],
        'Canada': ['Ontario', 'Quebec', 'British Columbia']
    }
    return JsonResponse({'states': states.get(country, [])})


@login_required
def resume_list(request):
    """View to display all resumes belonging to the logged in user"""
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resumes/resume_list.html',{'resumes':resumes})
    

@login_required
def create_resume(request):
    """View to create a new resume"""
    # Initialize both forms right at the start
    resume_form = ResumeForm(request.POST or None)
    
    # Define formsets here
    EducationFormSet = inlineformset_factory(
        Resume, Education, form=EducationForm, extra=1, can_delete=False # Set can_delete to True for removal
    )

    ExperienceFormSet = inlineformset_factory(
        Resume, Experience, form=ExperienceForm, extra=1, can_delete=False
    )

    ProjectFormSet = inlineformset_factory(
        Resume, Project, form=ProjectForm, extra=1, can_delete=False
    )

    CertificationFormSet = inlineformset_factory(
        Resume, Certification, form=CertificationForm, extra=1, can_delete=False
    )

    if request.method == 'POST':
        # Initialize main form and formsets with POST data
        # Important: Initialize formsets with a new, unsaved Resume instance
        # This prevents the formset data from being associated with an existing (or newly created) object prematurely
        education_formset = EducationFormSet(
            request.POST, prefix='education'
        )
        experience_formset = ExperienceFormSet(
            request.POST, prefix='experience'
        )
        project_formset = ProjectFormSet(
            request.POST, prefix='project'
        )
        certification_formset = CertificationFormSet(
            request.POST, prefix='certification'
        )

        # Check if the main form and ALL formsets are valid
        if (resume_form.is_valid() and
            education_formset.is_valid() and
            experience_formset.is_valid() and
            project_formset.is_valid() and
            certification_formset.is_valid()):

            # Save the main resume form ONLY AFTER validation
            resume_instance = resume_form.save(commit=False)
            resume_instance.user = request.user
            resume_instance.save()

            # Now save the formsets, linking them to the newly saved resume_instance
            education_formset.instance = resume_instance
            education_formset.save()

            experience_formset.instance = resume_instance
            experience_formset.save()

            project_formset.instance = resume_instance
            project_formset.save()

            certification_formset.instance = resume_instance
            certification_formset.save()

           #Handle skills
            skill_entries = request.POST.get('skills', '').split(',')
            skill_ids = [entry.strip() for entry in skill_entries if entry.strip()]
            
            final_skill_ids = []
            for skill_id in skill_ids:
               if skill_id.startswith('new_'):
                    skill_name = skill_id[4:]
                    skill, created = Skill.objects.get_or_create(
                        name=skill_name,
                        defaults={'level': 'Intermediate', 'category': 'other'}
                    )
                    final_skill_ids.append(skill.id)
               else:
                    final_skill_ids.append(int(skill_id))
            
            resume_instance.skills.set(final_skill_ids)

            messages.success(request, 'Resume created successfully!')
            return redirect('edit_resume', pk=resume_instance.pk) # Redirect to edit the created resume

        # If validation fails, the forms and formsets will contain errors
        # The rendering logic below will display the forms with errors

    else: # GET request - initialize empty forms
        # Initialize formsets with no instance for a new resume
        education_formset = EducationFormSet(prefix='education')
        experience_formset = ExperienceFormSet(prefix='experience')
        project_formset = ProjectFormSet(prefix='project')
        certification_formset = CertificationFormSet(prefix='certification')
    
    categories = [
        ('programming', 'Programming Languages'),
        ('framework', 'Frameworks & Libraries'),
        ('frontend', 'Frontend Technologies'),
        ('database', 'Databases'),
        ('devops', 'DevOps & Cloud')
    ]
    
    categories = Skill.CATEGORY_CHOICES

    skills_by_category = {}
    for category in categories:
        skills =Skill.objects.filter(category=category[0]).order_by('name')
        skills_by_category[category[0]] = list(skills)

    context = {
        'resume_form': resume_form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'project_formset': project_formset,
        'certification_formset': certification_formset,
        'skills': [],
        'skill_categories': categories,
        'skills_by_category': skills_by_category,
    }
    return render(request, 'resumes/resume_form.html', context)

@login_required
def edit_resume(request, pk):
    """View to edit an existing resume"""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)       
    
    #Create formsets
    EducationFormSet = inlineformset_factory(
        Resume,Education, form=EducationForm, extra=1, can_delete=True
    )

    ExperienceFormSet = inlineformset_factory(
        Resume, Experience, form=ExperienceForm, extra=1, can_delete=True
    )

    ProjectFormSet = inlineformset_factory(
        Resume, Project,form=ProjectForm, extra=1, can_delete=True
    )
    
    CertificationFormSet = inlineformset_factory(
        Resume, Certification, form=CertificationForm, extra=1,can_delete=True
    )
    
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST, instance=resume)
        education_formset = EducationFormSet(request.POST, instance=resume, prefix='education')
        experience_formset = ExperienceFormSet(request.POST, instance=resume, prefix='experience')
        project_formset = ProjectFormSet(request.POST, instance=resume, prefix='project')
        certification_formset = CertificationFormSet(request.POST, instance=resume, prefix='certification')

        if (resume_form.is_valid() and 
            education_formset.is_valid() and 
            experience_formset.is_valid() and 
            project_formset.is_valid() and
            certification_formset.is_valid()):

            resume_form.save()
            education_formset.save()
            experience_formset.save()
            project_formset.save()
            certification_formset.save()
            # Handle skills from the new dropdown system
            skill_entries = request.POST.get('skills', '').split(',')
            skill_ids = [entry.strip() for entry in skill_entries if entry.strip()]
            
            # Filter out temporary IDs (new_ prefix) if any
            final_skill_ids = []
            for skill_id in skill_ids:
                if skill_id.startswith('new_'):
                    skill_name = skill_id[4:]
                    skill, created = Skill.objects.get_or_create(
                        name=skill_name,
                        defaults={'level': 'Intermediate', 'category': 'other'}
                    )
                    final_skill_ids.append(skill.id)
                else:
                    final_skill_ids.append(int(skill_id))
            
            resume.skills.set(final_skill_ids)
            
            messages.success(request, 'Resume updated successfully!')
            return redirect('preview_resume', pk=resume.pk)
    else:
        resume_form = ResumeForm(instance=resume)
        education_formset = EducationFormSet(instance=resume, prefix='education')
        experience_formset = ExperienceFormSet(instance=resume, prefix='experience')
        project_formset = ProjectFormSet(instance=resume, prefix='project')
        certification_formset = CertificationFormSet(instance=resume, prefix='certification')
    
    # Get skills organized by category for the dropdowns
    categories = [
        ('programming', 'Programming Languages'),
        ('framework', 'Frameworks & Libraries'),
        ('frontend', 'Frontend Technologies'),
        ('database', 'Databases'),
        ('devops', 'DevOps & Cloud')
    ]
    
    skills_by_category = {}
    for category in categories:
        skills = Skill.objects.filter(category=category[0]).order_by('name')
        skills_by_category[category[0]] = list(skills)

    context = {
        'resume_form':resume_form,
        'education_formset':education_formset,
        'experience_formset': experience_formset,
        'project_formset': project_formset,
        'certification_formset': certification_formset,
        'resume': resume,
        'skills': resume.skills.all(),
        'skill_categories': categories,
        'skills_by_category': skills_by_category,
    }    
    return render(request, 'resumes/resume_form.html', context)

@login_required
def resume_detail(request, pk):
    """View to display a single resume"""
    resume = get_object_or_404(Resume, pk=pk,user=request.user)
    return render(request, 'resumes/preview_resume.html',{'resume':resume})

@login_required
def delete_resume(request, pk):
    """View to delete a resume"""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted successfully!')
        return redirect('resume_list')
    return render(request, 'resumes/resume_confirm_delete.html',{'resume':resume})

@login_required
def preview_resume(request, pk):
    """View to preview a resume"""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, 'resumes/preview_resume.html',{  
        'resume': resume,
        'template': resume.template or 'classic',
        'download': False 
    })
    
@login_required
def download_resume_pdf(request, pk):
    """view to download a resume as HTML"""
    resume = get_object_or_404(Resume,pk=pk,user=request.user)
    context = {
        'resume':resume, 
        'template': resume.template or 'classic',
        'download': True
    }
    html_string = render_to_string(
        'resumes/preview_resume.html',
        context=context,
        request=request
        )

    pdf_options = {
        'pag-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': 'UTF-8',
        'quiet': ''
    }
    
    #convert HTML to pdf
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()

    #create pdf response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_resume.pdf"'
    return response

@login_required
def choose_template(request, pk):
    """View to choose the template"""
    resume = get_object_or_404(Resume, pk=pk, user=request.user)

    if request.method == 'POST':
        template = request.POST.get('template')
        if template in dict(Resume.TEMPLATE_CHOICES):
            resume.template = template
            resume.save()
         # Save the user's template choice
            messages.success(request, f'Template {template.title()} selected!')
            return redirect('preview_resume',pk=resume.pk)
        else:
            messages.error(request, 'Invalid template selected.')
    return render(request,'resumes/choose_template.html',{'resume':resume, 'template_choices': Resume.TEMPLATE_CHOICES})    

def coming_soon(request):
    return render(request, 'resumes/coming_soon.html')
