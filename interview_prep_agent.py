#!/usr/bin/env python3
"""
AI Research Agent for Interview Preparation Roadmaps
A multi-agent system that generates comprehensive interview preparation roadmaps
"""

import google.generativeai as genai
import json
import re
import os
import glob
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system environment variables

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')  # Set via environment variable
DEMO_MODE = True  # Set to False when you have a real API key

# Data Models
class JobInput(BaseModel):
    company_name: str = Field(description="Name of the target company")
    role: str = Field(description="Job role/position title")
    job_description: str = Field(description="Complete job description text")

class InterviewRound(BaseModel):
    type: str = Field(description="Type of interview round")
    topics: List[str] = Field(description="List of topics covered in this round")
    duration: Optional[str] = Field(None, description="Expected duration")
    weight: Optional[str] = Field(None, description="Importance weight")

class Roadmap(BaseModel):
    company: str = Field(description="Company name")
    role: str = Field(description="Job role")
    difficulty: str = Field(description="Overall difficulty level")
    rounds: List[InterviewRound] = Field(description="List of interview rounds")
    recommended_order: List[str] = Field(description="Recommended preparation order")
    preparation_timeline: Optional[str] = Field(None, description="Timeline")
    key_skills: List[str] = Field(description="Most important skills")
    resources: Optional[Dict[str, List[str]]] = Field(None, description="Study resources")

class ExtractedSkills(BaseModel):
    technical_skills: List[str] = Field(description="Technical skills")
    soft_skills: List[str] = Field(description="Soft skills")
    tools_technologies: List[str] = Field(description="Tools and technologies")
    responsibilities: List[str] = Field(description="Key responsibilities")
    experience_level: str = Field(description="Required experience level")

class CompanyInsights(BaseModel):
    company_name: str = Field(description="Company name")
    company_type: str = Field(description="Type of company")
    typical_rounds: List[str] = Field(description="Typical interview rounds")
    difficulty_level: str = Field(description="General difficulty level")
    interview_focus: List[str] = Field(description="Interview focus areas")

class InterviewPrepAgent:
    """Main AI agent for generating interview preparation roadmaps"""
    
    def __init__(self, api_key: str, demo_mode: bool = False):
        self.demo_mode = demo_mode
        
        if not demo_mode:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
            print("🔧 Running in DEMO MODE - using predefined responses")
        
        # Company profiles database
        self.company_profiles = {
            "google": {"type": "FAANG", "difficulty": "Hard", "focus": ["Algorithms", "System Design"]},
            "meta": {"type": "FAANG", "difficulty": "Hard", "focus": ["Algorithms", "System Design"]},
            "facebook": {"type": "FAANG", "difficulty": "Hard", "focus": ["Algorithms", "System Design"]},
            "amazon": {"type": "FAANG", "difficulty": "Hard", "focus": ["Algorithms", "Leadership"]},
            "apple": {"type": "FAANG", "difficulty": "Hard", "focus": ["Algorithms", "Product"]},
            "netflix": {"type": "FAANG", "difficulty": "Hard", "focus": ["Algorithms", "Culture"]},
            "microsoft": {"type": "Big Tech", "difficulty": "Hard", "focus": ["Algorithms", "System Design"]},
            "uber": {"type": "Big Tech", "difficulty": "Hard", "focus": ["Algorithms", "Problem Solving"]},
            "startup": {"type": "Startup", "difficulty": "Medium", "focus": ["Full Stack", "Adaptability"]},
        }
        
        # Skill mapping for topic extraction
        self.skill_mapping = {
            "REST APIs": "Backend Development",
            "Data Structures": "DSA",
            "Algorithms": "DSA",
            "System Design": "System Design",
            "Machine Learning": "AI/ML",
            "React": "Frontend Development",
            "Node.js": "Backend Development",
            "SQL": "Database Management",
            "AWS": "Cloud Computing",
            "Docker": "DevOps"
        }

    def parse_job_description(self, job_description: str, role: str) -> ExtractedSkills:
        """Parse job description to extract skills and requirements"""
        
        if self.demo_mode:
            return self._demo_parse_skills(job_description, role)
        
        prompt = f"""
        Analyze this job description for {role} and extract information in JSON format:

        {job_description}

        Extract:
        {{
            "technical_skills": [list of technical skills],
            "soft_skills": [list of soft skills],
            "tools_technologies": [list of tools/technologies],
            "responsibilities": [list of key responsibilities],
            "experience_level": "Entry/Mid/Senior/Principal"
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            
            if json_match:
                parsed_data = json.loads(json_match.group())
                return ExtractedSkills(**parsed_data)
            else:
                return self._create_default_skills(role)
                
        except Exception as e:
            print(f"Error parsing job description: {e}")
            return self._create_default_skills(role)

    def research_company(self, company_name: str, role: str) -> CompanyInsights:
        """Research company interview process"""
        
        company_key = company_name.lower().replace(" ", "")
        company_profile = None
        
        # Check database
        for key, profile in self.company_profiles.items():
            if key in company_key:
                company_profile = profile
                break
        
        if not company_profile:
            company_profile = {"type": "Unknown", "difficulty": "Medium", "focus": ["Technical Skills"]}
        
        return CompanyInsights(
            company_name=company_name,
            company_type=company_profile["type"],
            typical_rounds=["Screening", "Technical", "System Design", "Behavioral", "Manager"],
            difficulty_level=company_profile["difficulty"],
            interview_focus=company_profile["focus"]
        )

    def generate_roadmap(self, job_input: JobInput) -> Roadmap:
        """Generate comprehensive preparation roadmap"""
        
        print(f"🚀 Analyzing {job_input.role} at {job_input.company_name}...")
        
        # Step 1: Parse job description
        extracted_skills = self.parse_job_description(job_input.job_description, job_input.role)
        print(f"✅ Extracted {len(extracted_skills.technical_skills)} technical skills")
        
        # Step 2: Research company
        company_insights = self.research_company(job_input.company_name, job_input.role)
        print(f"✅ Identified {company_insights.company_type} company")
        
        # Step 3: Generate interview rounds
        rounds = self._generate_rounds(extracted_skills, company_insights)
        
        # Step 4: Create preparation order
        prep_order = self._generate_prep_order(extracted_skills, company_insights, job_input.role)
        
        # Step 5: Estimate timeline
        timeline = self._estimate_timeline(company_insights.difficulty_level, extracted_skills.experience_level)
        
        # Step 6: Generate resources
        resources = self._generate_resources()
        
        # Step 7: Identify key skills
        key_skills = extracted_skills.technical_skills[:3] + company_insights.interview_focus[:2]
        
        return Roadmap(
            company=job_input.company_name,
            role=job_input.role,
            difficulty=company_insights.difficulty_level,
            rounds=rounds,
            recommended_order=prep_order,
            preparation_timeline=timeline,
            key_skills=list(set(key_skills)),
            resources=resources
        )

    def _generate_rounds(self, skills: ExtractedSkills, company: CompanyInsights) -> List[InterviewRound]:
        """Generate interview rounds based on company and skills"""
        
        rounds = []
        
        if company.company_type in ["FAANG", "Big Tech"]:
            rounds = [
                InterviewRound(type="Phone Screening", topics=["Resume", "Basic Technical"], duration="30 min"),
                InterviewRound(type="Coding Round 1", topics=["Arrays", "Strings", "Hash Maps"], duration="45 min"),
                InterviewRound(type="Coding Round 2", topics=["Dynamic Programming", "Graphs"], duration="45 min"),
                InterviewRound(type="System Design", topics=["Scalability", "Database Design"], duration="60 min"),
                InterviewRound(type="Behavioral", topics=["Leadership", "Teamwork"], duration="30 min")
            ]
        else:
            rounds = [
                InterviewRound(type="Initial Screening", topics=["Background", "Interest"], duration="30 min"),
                InterviewRound(type="Technical Interview", topics=["Problem Solving", "Code Review"], duration="60 min"),
                InterviewRound(type="Manager Round", topics=["Experience", "Culture Fit"], duration="45 min")
            ]
        
        return rounds

    def _generate_prep_order(self, skills: ExtractedSkills, company: CompanyInsights, role: str) -> List[str]:
        """Generate recommended preparation order"""
        
        order = ["DSA Fundamentals"]
        
        if "data" in role.lower():
            order.extend(["Statistics", "SQL", "Machine Learning"])
        elif "frontend" in role.lower():
            order.extend(["JavaScript", "React", "CSS"])
        else:
            order.extend(["System Design", "Backend Development"])
        
        if company.company_type in ["FAANG", "Big Tech"]:
            order.extend(["Advanced Algorithms", "System Design"])
        
        order.extend(["Behavioral Preparation", "Mock Interviews"])
        
        return order[:6]

    def _estimate_timeline(self, difficulty: str, experience: str) -> str:
        """Estimate preparation timeline"""
        
        base_weeks = {"Easy": 4, "Medium": 8, "Hard": 12}
        multiplier = {"Entry": 1.5, "Mid": 1.0, "Senior": 0.8}.get(experience, 1.0)
        
        weeks = int(base_weeks.get(difficulty, 8) * multiplier)
        return f"{weeks} weeks"

    def _generate_resources(self) -> Dict[str, List[str]]:
        """Generate study resources"""
        
        return {
            "DSA": ["LeetCode", "Cracking the Coding Interview"],
            "System Design": ["System Design Interview by Alex Xu"],
            "Behavioral": ["STAR method preparation", "Company research"]
        }

    def _create_default_skills(self, role: str) -> ExtractedSkills:
        """Create default skills when parsing fails"""
        
        return ExtractedSkills(
            technical_skills=["Programming", "Problem Solving"],
            soft_skills=["Communication", "Teamwork"],
            tools_technologies=["Development Tools"],
            responsibilities=["Software Development"],
            experience_level="Mid"
        )
    
    def _demo_parse_skills(self, job_description: str, role: str) -> ExtractedSkills:
        """Demo mode parsing using keyword matching"""
        
        jd_lower = job_description.lower()
        
        # Extract technical skills based on keywords
        tech_skills = []
        for keyword in ["python", "java", "javascript", "react", "node.js", "sql", "aws", "docker", "kubernetes", "machine learning", "data structures", "algorithms"]:
            if keyword in jd_lower:
                tech_skills.append(keyword.title())
        
        # Default skills if none found
        if not tech_skills:
            tech_skills = ["Programming", "Problem Solving", "Software Development"]
        
        # Determine experience level
        experience = "Entry"
        if "senior" in role.lower() or "lead" in role.lower():
            experience = "Senior"
        elif any(term in jd_lower for term in ["3+ years", "4+ years", "5+ years"]):
            experience = "Mid"
        
        return ExtractedSkills(
            technical_skills=tech_skills,
            soft_skills=["Communication", "Teamwork", "Problem Solving", "Leadership"],
            tools_technologies=tech_skills,
            responsibilities=["Software Development", "Code Review", "System Design"],
            experience_level=experience
        )

    def save_roadmap(self, roadmap: Roadmap, filename: str = None) -> str:
        """Save roadmap to JSON file"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"roadmap_{roadmap.company}_{roadmap.role}_{timestamp}.json"
            filename = filename.replace(" ", "_").replace("/", "_")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(roadmap.model_dump(), f, indent=2, ensure_ascii=False)
        
        print(f"💾 Roadmap saved to: {filename}")
        return filename

    def display_summary(self, roadmap: Roadmap):
        """Display formatted roadmap summary"""
        
        print(f"\n🎯 INTERVIEW PREPARATION ROADMAP")
        print(f"{'='*50}")
        print(f"Company: {roadmap.company}")
        print(f"Role: {roadmap.role}")
        print(f"Difficulty: {roadmap.difficulty}")
        print(f"Timeline: {roadmap.preparation_timeline}")
        
        print(f"\n📊 INTERVIEW ROUNDS ({len(roadmap.rounds)} rounds)")
        for i, round_info in enumerate(roadmap.rounds, 1):
            print(f"{i}. {round_info.type}")
            print(f"   Topics: {', '.join(round_info.topics)}")
            if round_info.duration:
                print(f"   Duration: {round_info.duration}")
        
        print(f"\n🎯 KEY SKILLS: {', '.join(roadmap.key_skills)}")
        print(f"\n📈 PREP ORDER: {' → '.join(roadmap.recommended_order)}")

def interactive_mode(agent):
    """Interactive mode for custom job analysis"""
    
    print("\n🎯 INTERACTIVE JOB ANALYSIS MODE")
    print("="*50)
    
    while True:
        print("\nEnter job details (or 'quit' to exit):")
        
        # Get user input
        company_name = input("🏢 Company Name: ").strip()
        if company_name.lower() == 'quit':
            break
            
        role = input("💼 Job Role: ").strip()
        if role.lower() == 'quit':
            break
            
        print("📋 Job Description (press Enter twice when done):")
        job_description_lines = []
        while True:
            line = input()
            if line == "":
                if job_description_lines and job_description_lines[-1] == "":
                    break
                job_description_lines.append("")
            else:
                job_description_lines.append(line)
        
        job_description = "\n".join(job_description_lines).strip()
        
        if not job_description:
            print("❌ Job description cannot be empty!")
            continue
        
        # Create job input
        job_input = JobInput(
            company_name=company_name,
            role=role,
            job_description=job_description
        )
        
        # Generate roadmap
        print(f"\n🚀 Analyzing {role} position at {company_name}...")
        roadmap = agent.generate_roadmap(job_input)
        
        # Display and save
        agent.display_summary(roadmap)
        filename = agent.save_roadmap(roadmap)
        
        # Ask if user wants to continue
        print(f"\n✅ Analysis complete! Roadmap saved as {filename}")
        continue_choice = input("\n🔄 Analyze another job? (y/n): ").strip().lower()
        if continue_choice not in ['y', 'yes']:
            break

def demo_samples_mode(agent):
    """Demo mode with multiple sample job descriptions"""
    
    print("\n🎭 DEMO MODE - Testing with Sample Job Descriptions")
    print("="*60)
    
    # Sample job descriptions
    samples = [
        {
            "company": "Google",
            "role": "Software Engineer (SDE-1)",
            "description": """
Software Engineer - Google

We are looking for a Software Engineer to join our team and help build the next generation of products.

Responsibilities:
- Design, develop, test, deploy, maintain and improve software
- Work with large-scale distributed systems
- Write efficient code following best practices
- Collaborate with cross-functional teams

Requirements:
- Bachelor's degree in Computer Science or equivalent
- 1+ years of software development experience
- Experience with data structures and algorithms
- Knowledge of Python, Java, C++, or Go
- Experience with system design and architecture
- Knowledge of web technologies (HTTP, REST APIs, JSON)
- Experience with databases (SQL, NoSQL)
- Strong problem-solving skills
            """
        },
        {
            "company": "Microsoft",
            "role": "Data Scientist",
            "description": """
Data Scientist - Microsoft Azure AI

Join our Azure AI team to build intelligent solutions with AI and machine learning.

Responsibilities:
- Develop machine learning models and algorithms
- Analyze large datasets to extract insights
- Design and implement data pipelines
- Conduct statistical analysis and A/B testing
- Present findings to stakeholders

Requirements:
- PhD or Master's in Data Science, Statistics, or Computer Science
- 3+ years of experience in machine learning
- Proficiency in Python and R
- Experience with ML frameworks (TensorFlow, PyTorch, Scikit-learn)
- Strong knowledge of statistics
- Experience with big data technologies (Spark, Hadoop)
- Knowledge of cloud platforms (Azure preferred)
- Strong communication skills
            """
        },
        {
            "company": "TechFlow (Startup)",
            "role": "Full Stack Developer",
            "description": """
Full Stack Developer - TechFlow (YC-backed startup)

Fast-growing fintech startup building the future of financial technology.

Responsibilities:
- Build and maintain web application using modern technologies
- Work on both frontend and backend development
- Implement new features from concept to deployment
- Optimize application performance
- Collaborate with designers and product managers

Tech Stack:
- Frontend: React, TypeScript, Tailwind CSS
- Backend: Node.js, Express, PostgreSQL
- Infrastructure: AWS, Docker, Kubernetes

Requirements:
- 2-4 years of full stack development experience
- Strong proficiency in JavaScript/TypeScript
- Experience with React and modern frontend development
- Backend development experience with Node.js
- Database experience with SQL databases
- Understanding of RESTful APIs and microservices
- Experience with cloud platforms (AWS preferred)
            """
        }
    ]
    
    for i, sample in enumerate(samples, 1):
        print(f"\n🧪 Test {i}: {sample['company']} - {sample['role']}")
        print("-" * 60)
        
        job_input = JobInput(
            company_name=sample["company"],
            role=sample["role"],
            job_description=sample["description"]
        )
        
        roadmap = agent.generate_roadmap(job_input)
        agent.display_summary(roadmap)
        agent.save_roadmap(roadmap)
        
        if i < len(samples):
            input("\n⏳ Press Enter to continue to next test...")

def main():
    """Enhanced main function with multiple modes"""
    
    print("🎯 AI Interview Preparation Roadmap Generator")
    print("="*50)
    
    # Initialize agent
    try:
        agent = InterviewPrepAgent(GEMINI_API_KEY)
        print("✅ AI Agent initialized successfully!")
        
        while True:
            print("\n🎮 Choose Mode:")
            print("1. � Interactive Mode (Analyze custom job descriptions)")
            print("2. 🧪 Quick Test (Sample Google SDE job)")
            print("3. 🎭 Demo Mode (Multiple sample jobs)")
            print("4. 📊 Show JSON Output (Latest roadmap)")
            print("5. 🚪 Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                interactive_mode(agent)
            elif choice == "2":
                # Quick test with Google SDE
                print("\n🧪 Quick Test: Google SDE-1 Analysis")
                print("-" * 40)
                
                job_input = JobInput(
                    company_name="Google",
                    role="Software Engineer (SDE-1)",
                    job_description="""
Software Engineer - Google

We are looking for a Software Engineer to join our team and help build the next generation of products.

Requirements:
- Bachelor's degree in Computer Science or equivalent
- 1+ years of software development experience  
- Experience with data structures and algorithms
- Knowledge of Python, Java, C++, or Go
- Experience with system design and architecture
- Strong problem-solving skills
                    """
                )
                
                roadmap = agent.generate_roadmap(job_input)
                agent.display_summary(roadmap)
                agent.save_roadmap(roadmap)
                
            elif choice == "3":
                demo_samples_mode(agent)
            elif choice == "4":
                # Show latest JSON file
                import glob
                json_files = glob.glob("roadmap_*.json")
                if json_files:
                    latest_file = max(json_files, key=lambda x: os.path.getctime(x))
                    print(f"\n📄 Latest Roadmap JSON: {latest_file}")
                    print("-" * 50)
                    with open(latest_file, 'r') as f:
                        content = json.load(f)
                        print(json.dumps(content, indent=2))
                else:
                    print("❌ No roadmap files found! Generate a roadmap first.")
                    
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1, 2, 3, 4, or 5.")
                
    except Exception as e:
        print(f"❌ Error initializing AI agent: {e}")
        print("💡 Please check your Gemini API key and internet connection.")
        print("🔧 You can still run in demo mode by modifying the API key check.")

if __name__ == "__main__":
    main()