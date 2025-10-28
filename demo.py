#!/usr/bin/env python3
"""
Quick Demo Script for Interview Preparation Agent
Run this for a fast demonstration of the agent's capabilities
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from interview_prep_agent import InterviewPrepAgent, JobInput

def run_demo():
    """Run a quick demo with pre-configured examples"""
    
    print("🎯 AI Interview Preparation Roadmap Generator - DEMO")
    print("=" * 60)
    
    # Sample job descriptions
    examples = {
        "1": {
            "company": "Google",
            "role": "Software Engineer (SDE-1)",
            "jd": """
            Software Engineer - Google
            
            We are looking for a Software Engineer to join our team and help build the next generation of products.
            
            Requirements:
            - Bachelor's degree in Computer Science or equivalent
            - 1+ years of software development experience
            - Experience with Python, Java, or C++
            - Knowledge of data structures and algorithms
            - Experience with distributed systems
            - Strong problem-solving skills
            """
        },
        "2": {
            "company": "Microsoft", 
            "role": "Data Scientist",
            "jd": """
            Data Scientist - Microsoft Azure AI
            
            Join our Azure AI team to build intelligent solutions.
            
            Requirements:
            - PhD or Master's in Data Science, Statistics, or Computer Science
            - 3+ years of experience in machine learning
            - Proficiency in Python and R
            - Experience with TensorFlow, PyTorch, Scikit-learn
            - Strong knowledge of statistics
            - Experience with Azure, AWS, or GCP
            """
        },
        "3": {
            "company": "TechFlow",
            "role": "Full Stack Developer", 
            "jd": """
            Full Stack Developer - TechFlow (YC-backed startup)
            
            We're a fast-growing fintech startup looking for a talented developer.
            
            Requirements:
            - 2-4 years of full stack development experience
            - Strong proficiency in JavaScript/TypeScript
            - Experience with React and Node.js
            - Database experience with PostgreSQL
            - Understanding of RESTful APIs
            - AWS experience preferred
            """
        }
    }
    
    print("Choose an example to analyze:")
    for key, example in examples.items():
        print(f"{key}. {example['company']} - {example['role']}")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice not in examples:
        print("Invalid choice. Using Google example.")
        choice = "1"
    
    selected = examples[choice]
    
    print(f"\n🔍 Analyzing: {selected['role']} at {selected['company']}")
    print("=" * 60)
    
    # Initialize agent (will use demo mode if no API key)
    agent = InterviewPrepAgent("demo_mode")
    
    # Create job input
    job_input = JobInput(
        company_name=selected['company'],
        role=selected['role'],
        job_description=selected['jd']
    )
    
    # Generate roadmap
    roadmap = agent.generate_roadmap(job_input)
    
    # Display results
    agent.display_summary(roadmap)
    
    # Save results
    filename = f"demo_{selected['company'].lower().replace(' ', '_')}_roadmap.json"
    agent.save_roadmap(roadmap, filename)
    
    print(f"\n✅ Demo completed! Check {filename} for the full JSON output.")
    print("\n💡 To use with your own job descriptions:")
    print("   python3 interview_prep_agent.py")

if __name__ == "__main__":
    run_demo()