from rest_framework import generics, permissions
from resumes.models import Certification, Education, Experience, Project, Resume, Skill
from resumes.api.serializers import (CertificationSerializer, EducationSerializer, ExperienceSerializer, ProjectSerializer, ResumeSerializer, SkillSerializer)
from rest_framework import status
from rest_framework.response import Response
from .throttles import QuickBurstRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from resumes.api.throttles import ResumeCreationThrottle
from drf_yasg.utils import swagger_auto_schema


class IsOwner(permissions.BasePermission):
   def has_object_permission(self, request, view, obj):
        print(f"Permission check - User: {request.user}, Object: {obj}")
        
        if hasattr(obj, 'user'):
            print(f"Object user: {obj.user}")
            return obj.user == request.user
            
        if hasattr(obj, 'resume'):
            print(f"Resume user: {obj.resume.user}")
            return obj.resume.user == request.user
            
        print("Object has neither user nor resume attribute")
        return False

class TestThrottleView(generics.ListAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = []    

# ------------------ Resume Views ------------------

class ResumeListCreateView(generics.ListCreateAPIView):
    """
    get:
    Returns all resumes belonging to the authorized user.

    post:
    Creates a new resume for the authenticated user.

    Throttle: Limited to 5 creations per hour (configured in throttles.py)
    """
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_throttles(self):
        if self.request.method == 'POST':
            return [ResumeCreationThrottle()]
        return [UserRateThrottle(), AnonRateThrottle()]    

    @swagger_auto_schema(
        operation_description="List all resumes",
        responses={200: ResumeSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        print(f"Authenticated user: {request.user} (ID: {request.user.id})")
        print(f"Resumes for user: {Resume.objects.filter(user=request.user).count()}")
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
            operation_description="Create a resume",
            request_body=ResumeSerializer,
            responses={
                201: ResumeSerializer(),
                400: "Bad request",
                401: "Unauthorized"
            }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class ResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

# ------------------ Education Views ------------------

class EducationListCreateView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        resume_id = self.kwargs.get('resume_id')
        return Education.objects.filter(resume_id=resume_id, resume__user=self.request.user)

    def perform_create(self, serializer):
        resume = Resume.objects.get(pk=self.kwargs['resume_id'], user=self.request.user)
        serializer.save(resume=resume)

class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Education data deleted successfully!"}, status=status.HTTP_200_OK)


# ------------------ Experience Views ------------------

class ExperienceListCreateView(generics.ListCreateAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        resume_id = self.kwargs.get('resume_id')
        return Experience.objects.filter(resume_id=resume_id, resume__user=self.request.user)

    def perform_create(self, serializer):
        resume = Resume.objects.get(pk=self.kwargs['resume_id'], user=self.request.user)
        serializer.save(resume=resume)

class ExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Experience data deleted successfully!"}, status=status.HTTP_200_OK)

# ------------------ Skill Views ------------------

class SkillListCreateView(generics.ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        resume_id = self.kwargs.get('resume_id')
        return Skill.objects.filter(resume_id=resume_id, resume__user=self.request.user)

    def perform_create(self, serializer):
        resume = Resume.objects.get(pk=self.kwargs['resume_id'], user=self.request.user)
        serializer.save(resume=resume)

class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Skill deleted successfully!"}, status=status.HTTP_200_OK)

# ------------------ Project Views ------------------

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        resume_id = self.kwargs.get('resume_id')
        return Project.objects.filter(resume_id=resume_id, resume__user=self.request.user)

    def perform_create(self, serializer):
        resume = Resume.objects.get(pk=self.kwargs['resume_id'], user=self.request.user)
        serializer.save(resume=resume)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
   
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Project data deleted successfully!"}, status=status.HTTP_200_OK)

# ------------------ Certification Views ------------------

class CertificationListCreateView(generics.ListCreateAPIView):
    serializer_class = CertificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        resume_id = self.kwargs.get('resume_id')
        return Certification.objects.filter(resume_id=resume_id, resume__user=self.request.user)

    def perform_create(self, serializer):
        resume = Resume.objects.get(pk=self.kwargs['resume_id'], user=self.request.user)
        serializer.save(resume=resume)

class CertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
   
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Certification data deleted successfully!"}, status=status.HTTP_200_OK)

