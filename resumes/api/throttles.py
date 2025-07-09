from rest_framework.throttling import UserRateThrottle

class QuickBurstRateThrottle(UserRateThrottle):
    scope = 'quickburst'

class ResumeCreationThrottle(UserRateThrottle):
    scope = 'resume_create'    
