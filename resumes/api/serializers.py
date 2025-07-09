from rest_framework import serializers
from resumes.models import Certification, Education, Experience, Project, Resume, Skill

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution', 'degree', 'branch', 'start_date', 'end_date', 'cgpa', 'percentage', 'description']

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'company', 'position', 'location', 'start_date', 'end_date', 'description']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'level']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'technologies', 'url', 'start_date', 'end_date']

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'name', 'organization', 'date_obtained', 'expiry_date', 'credential_id']

class ResumeSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, read_only=True, source='education_set')
    experiences = ExperienceSerializer(many=True, read_only=True, source='experience_set')
    skills = SkillSerializer(many=True, read_only=True, source='skill_set')
    projects = ProjectSerializer(many=True, read_only=True, source='project_set')
    certifications = CertificationSerializer(many=True, read_only=True, source='certification_set')

    class Meta:
        model = Resume
        fields = [
            'id', 'title', 'full_name', 'email', 'phone', 'address', 'summary',
            'template', 'created_at', 'updated_at',
            'education', 'experiences', 'skills', 'projects', 'certifications'
        ]
        read_only_fields = ['created_at', 'updated_at']
