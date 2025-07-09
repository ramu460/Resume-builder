def get_skills_for_title(job_title):
    """
    Returns a list of recommended skills based on job title
    """
    # This is a placeholder implementation
    # In a real-world scenario, you would use a more sophisticated approach
    # like fetching from an API or using a pre-defined mapping
    
    job_title = job_title.lower()
    
    skill_mapping = {
        'developer': ['Python', 'JavaScript', 'Git', 'SQL', 'HTML', 'CSS'],
        'web developer': ['JavaScript', 'HTML', 'CSS', 'React', 'Node.js', 'MySQL'],
        'frontend developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Vue.js', 'TypeScript'],
        'backend developer': ['Python', 'Java', 'Node.js', 'SQL', 'MongoDB', 'Django'],
        'data scientist': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics', 'Pandas'],
        'data analyst': ['SQL', 'Excel', 'Python', 'Tableau', 'Power BI', 'Data Visualization'],
        'ui designer': ['Figma', 'Sketch', 'Adobe XD', 'UI/UX', 'Wireframing', 'Prototyping'],
        'ux designer': ['User Research', 'Wireframing', 'Prototyping', 'Figma', 'Adobe XD', 'User Testing'],
        'product manager': ['Agile', 'JIRA', 'Product Strategy', 'User Stories', 'Roadmapping', 'Stakeholder Management'],
        'project manager': ['Agile', 'Scrum', 'JIRA', 'MS Project', 'Risk Management', 'Budgeting'],
    }
    
    # Try to find an exact match first
    if job_title in skill_mapping:
        return skill_mapping[job_title]
    
    # If no exact match, look for partial matches
    for key, skills in skill_mapping.items():
        if key in job_title or job_title in key:
            return skills
    
    # Default skills for unknown job titles
    return ['Python', 'JavaScript', 'SQL', 'Communication', 'Problem Solving', 'Teamwork']