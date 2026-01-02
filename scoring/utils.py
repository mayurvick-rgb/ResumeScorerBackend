import re
from typing import Dict, List
from resumes.models import Resume, ResumeAnalysis
from jobs.models import JobPost
from .models import ScoreAnalytics

class ATSScorer:
    def __init__(self):
        self.weights = {
            'ats_score': 0.3,
            'skill_match': 0.4,
            'experience': 0.3
        }
    
    def calculate_ats_score(self, resume_text: str, job_description: str) -> float:
        """Calculate ATS compatibility score based on keyword matching"""
        resume_words = set(resume_text.lower().split())
        job_words = set(job_description.lower().split())
        
        # Remove common words
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        resume_words -= common_words
        job_words -= common_words
        
        if not job_words:
            return 0.0
        
        matching_words = resume_words.intersection(job_words)
        score = (len(matching_words) / len(job_words)) * 100
        return min(score, 100.0)
    
    def calculate_skill_match(self, resume_skills: List[str], required_skills: List[str]) -> Dict:
        """Calculate skill matching score"""
        if not required_skills:
            return {'score': 0.0, 'missing_skills': []}
        
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        matched_skills = []
        missing_skills = []
        
        for skill in required_skills_lower:
            if any(skill in resume_skill for resume_skill in resume_skills_lower):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        score = (len(matched_skills) / len(required_skills_lower)) * 100
        return {
            'score': score,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills
        }
    
    def calculate_experience_score(self, resume_experience: float, required_experience: str) -> float:
        """Calculate experience matching score"""
        # Extract years from requirement string
        years_match = re.findall(r'(\d+)', required_experience)
        if not years_match:
            return 50.0  # Default score if can't parse
        
        required_years = int(years_match[0])
        
        if resume_experience >= required_years:
            return 100.0
        elif resume_experience >= required_years * 0.8:
            return 80.0
        elif resume_experience >= required_years * 0.6:
            return 60.0
        elif resume_experience >= required_years * 0.4:
            return 40.0
        else:
            return 20.0
    
    def calculate_overall_score(self, resume: Resume, job_post: JobPost) -> Dict:
        """Calculate overall ATS score for resume-job combination"""
        try:
            analysis = ResumeAnalysis.objects.get(resume=resume)
        except ResumeAnalysis.DoesNotExist:
            return {'error': 'Resume analysis not found'}
        
        # Calculate individual scores
        ats_score = self.calculate_ats_score(
            analysis.extracted_text, 
            job_post.description + ' ' + job_post.requirements
        )
        
        skill_match_data = self.calculate_skill_match(
            analysis.skills, 
            job_post.skills_required
        )
        
        experience_score = self.calculate_experience_score(
            analysis.experience_years,
            job_post.experience_required
        )
        
        # Calculate weighted overall score
        overall_score = (
            ats_score * self.weights['ats_score'] +
            skill_match_data['score'] * self.weights['skill_match'] +
            experience_score * self.weights['experience']
        )
        
        # Generate recommendations
        recommendations = self.generate_recommendations(
            ats_score, skill_match_data, experience_score
        )
        
        return {
            'ats_score': round(ats_score, 2),
            'skill_match_score': round(skill_match_data['score'], 2),
            'experience_score': round(experience_score, 2),
            'overall_score': round(overall_score, 2),
            'missing_skills': skill_match_data['missing_skills'],
            'recommendations': recommendations
        }
    
    def generate_recommendations(self, ats_score: float, skill_data: Dict, exp_score: float) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if ats_score < 60:
            recommendations.append("Optimize your resume with more relevant keywords from the job description")
        
        if skill_data['score'] < 70:
            recommendations.append(f"Consider learning these missing skills: {', '.join(skill_data['missing_skills'][:3])}")
        
        if exp_score < 60:
            recommendations.append("Highlight relevant projects and internships to demonstrate experience")
        
        if not recommendations:
            recommendations.append("Great match! Consider applying to this position")
        
        return recommendations
    
    def update_analytics(self, resume: Resume):
        """Update or create analytics for resume"""
        from .models import ResumeScore
        
        scores = ResumeScore.objects.filter(resume=resume)
        
        if not scores.exists():
            return
        
        total_applications = scores.count()
        average_score = sum(score.overall_score for score in scores) / total_applications
        
        # Get top matching roles
        top_roles = scores.order_by('-overall_score')[:5]
        top_matching_roles = [
            {
                'title': score.job_post.title,
                'company': score.job_post.company,
                'score': score.overall_score
            }
            for score in top_roles
        ]
        
        # Analyze skill gaps
        all_missing_skills = []
        for score in scores:
            all_missing_skills.extend(score.missing_skills)
        
        skill_frequency = {}
        for skill in all_missing_skills:
            skill_frequency[skill] = skill_frequency.get(skill, 0) + 1
        
        skill_gaps = [
            {'skill': skill, 'frequency': freq}
            for skill, freq in sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        # Generate improvement suggestions
        improvement_suggestions = [
            "Focus on learning the most frequently missing skills",
            "Tailor your resume keywords for better ATS compatibility",
            "Highlight relevant experience and projects more prominently"
        ]
        
        analytics, created = ScoreAnalytics.objects.update_or_create(
            resume=resume,
            defaults={
                'total_applications': total_applications,
                'average_score': round(average_score, 2),
                'top_matching_roles': top_matching_roles,
                'skill_gaps': skill_gaps,
                'improvement_suggestions': improvement_suggestions
            }
        )