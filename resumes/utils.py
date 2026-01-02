import PyPDF2
import docx
import re
import json
from typing import Dict, List, Any

class ResumeProcessor:
    def __init__(self):
        self.skills_keywords = [
            'python', 'java', 'javascript', 'react', 'django', 'flask', 'node.js',
            'html', 'css', 'sql', 'mongodb', 'postgresql', 'git', 'docker',
            'kubernetes', 'aws', 'azure', 'machine learning', 'data science',
            'artificial intelligence', 'tensorflow', 'pytorch', 'pandas', 'numpy'
        ]
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def extract_text_from_docx(self, file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    def extract_text(self, file_path: str, file_extension: str) -> str:
        if file_extension.lower() == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension.lower() in ['.docx', '.doc']:
            return self.extract_text_from_docx(file_path)
        else:
            return "Unsupported file format"
    
    def extract_skills(self, text: str) -> List[str]:
        found_skills = []
        text_lower = text.lower()
        for skill in self.skills_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        return found_skills
    
    def extract_experience(self, text: str) -> float:
        experience_patterns = [
            r'(\d+)\s*years?\s*of\s*experience',
            r'(\d+)\s*years?\s*experience',
            r'experience\s*:\s*(\d+)\s*years?',
            r'(\d+)\+\s*years?'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return float(matches[0])
        return 0.0
    
    def extract_education(self, text: str) -> List[str]:
        education_keywords = [
            'bachelor', 'master', 'phd', 'diploma', 'degree',
            'b.tech', 'm.tech', 'bca', 'mca', 'mba', 'b.sc', 'm.sc'
        ]
        
        found_education = []
        text_lower = text.lower()
        for edu in education_keywords:
            if edu in text_lower:
                found_education.append(edu)
        return found_education
    
    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'[\+]?[1-9]?[0-9]{7,15}'
        
        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        
        return {
            'emails': emails,
            'phones': phones
        }
    
    def process_resume(self, file_path: str, file_extension: str) -> Dict[str, Any]:
        text = self.extract_text(file_path, file_extension)
        
        return {
            'extracted_text': text,
            'skills': self.extract_skills(text),
            'experience_years': self.extract_experience(text),
            'education': self.extract_education(text),
            'contact_info': self.extract_contact_info(text)
        }