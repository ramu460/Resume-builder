# management/commands/populate_skills.py
from django.core.management.base import BaseCommand
from resumes.models import Skill

class Command(BaseCommand):
    help = 'Populates the database with common tech skills'

    def handle(self, *args, **options):
        skills_data = [
            # Programming Languages
            {'name': 'Python', 'category': 'programming'},
            {'name': 'JavaScript', 'category': 'programming'},
            {'name': 'Java', 'category': 'programming'},
            {'name': 'C#', 'category': 'programming'},
            {'name': 'C++', 'category': 'programming'},
            {'name': 'TypeScript', 'category': 'programming'},
            {'name': 'Go', 'category': 'programming'},
            {'name': 'Ruby', 'category': 'programming'},
            {'name': 'Swift', 'category': 'programming'},
            {'name': 'Kotlin', 'category': 'programming'},
            {'name': 'Rust', 'category': 'programming'},
            
            # Frameworks
            {'name': 'Django', 'category': 'framework'},
            {'name': 'Flask', 'category': 'framework'},
            {'name': 'React', 'category': 'framework'},
            {'name': 'Angular', 'category': 'framework'},
            {'name': 'Vue.js', 'category': 'framework'},
            {'name': 'Spring', 'category': 'framework'},
            {'name': 'Express.js', 'category': 'framework'},
            {'name': 'Ruby on Rails', 'category': 'framework'},
            {'name': '.NET Core', 'category': 'framework'},
            
            # Frontend
            {'name': 'HTML5', 'category': 'frontend'},
            {'name': 'CSS3', 'category': 'frontend'},
            {'name': 'SASS', 'category': 'frontend'},
            {'name': 'Bootstrap', 'category': 'frontend'},
            
            # Databases
            {'name': 'PostgreSQL', 'category': 'database'},
            {'name': 'MySQL', 'category': 'database'},
            {'name': 'MongoDB', 'category': 'database'},
            {'name': 'Redis', 'category': 'database'},
            
            # DevOps
            {'name': 'Docker', 'category': 'devops'},
            {'name': 'Kubernetes', 'category': 'devops'},
            {'name': 'AWS', 'category': 'devops'},
            {'name': 'Azure', 'category': 'devops'},
        ]

        for skill in skills_data:

            obj, created = Skill.objects.get_or_create(
                name=skill['name'],
                defaults={
                    'category': skill['category'],
                    'level': 'Intermediate'
            }
        )
        
            if not created and obj.category != skill['category']:
               obj.category = skill['category']
               obj.save()
               self.stdout.write(self.style.SUCCESS(f'Updated category for {obj.name}'))
            elif created:
               self.stdout.write(self.style.SUCCESS(f'Created new skill: {obj.name}'))
            else:
               self.stdout.write(self.style.WARNING(f'Skipped existing skill: {obj.name}'))        
       
        self.stdout.write(self.style.SUCCESS('Successfully populated skills'))