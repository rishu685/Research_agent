# AI Research Agent for Interview Preparation Roadmaps

An intelligent multi-agent system that analyzes job descriptions and generates comprehensive interview preparation roadmaps using Google's Gemini API.

## 🎯 Overview

This AI agent takes a company name, role, and job description as input and produces a structured preparation roadmap including:
- Interview rounds with specific topics
- Difficulty assessment
- Recommended preparation order
- Timeline estimation
- Study resources
- Company-specific insights

## 🚀 Quick Demo

```bash
# Clone the repository
git clone https://github.com/rishu685/Research_agent.git
cd Research_agent

# Install dependencies
pip install -r requirements.txt

# Run the interactive script
python3 interview_prep_agent.py
```

**Live Demo**: Run the script and select from pre-loaded examples or input your own job description!

## 🏗️ Architecture

### Multi-Agent System Design
```
Job Description → JD Parser Agent → Interview Process Agent → Roadmap Builder Agent → JSON Output
```

1. **Job Description Parser Agent**: Extracts skills, tools, and responsibilities using NLP
2. **Company Interview Process Research Agent**: Analyzes company interview patterns and difficulty
3. **Roadmap Generation Agent**: Combines insights to create structured preparation plans
4. **Multi-Agent Orchestrator**: Coordinates the workflow with error handling

## 🚀 Features

- ✅ **Intelligent Skill Extraction**: Maps JD keywords to relevant interview topics
- ✅ **Company Database**: Pre-configured insights for FAANG, Big Tech, and Startups
- ✅ **AI-Powered Research**: Uses Gemini API for unknown companies
- ✅ **Structured JSON Output**: Standardized format for easy integration
- ✅ **Multi-Round Planning**: Covers screening, technical, system design, and behavioral rounds
- ✅ **Resource Recommendations**: Curated study materials for each topic
- ✅ **Timeline Estimation**: Realistic preparation duration based on difficulty and experience
- ✅ **Error Handling**: Robust fallback mechanisms

## 📋 Requirements

### Dependencies
```bash
pip install google-generativeai langchain requests beautifulsoup4 pydantic typing-extensions
```

### API Setup
- Google Gemini API key (replace `YOUR_GEMINI_API_KEY_HERE` in the notebook)

## 💻 Usage

### Basic Usage
```python
# Initialize the agent
prep_agent = InterviewPrepAgent()

# Generate roadmap
roadmap = prep_agent.generate_preparation_roadmap(
    company_name="Google",
    role="Software Engineer",
    job_description="Your job description here..."
)

# Display results
prep_agent.display_roadmap_summary(roadmap)

# Save to JSON
prep_agent.save_roadmap_to_file(roadmap)
```

### Custom Analysis
```python
# Use the helper function
roadmap = analyze_custom_job(
    company_name="Amazon", 
    role="SDE-2", 
    job_description="Your JD text..."
)
```

## 🎨 How It Works

### 1. Skill Extraction
The JD Parser Agent uses advanced NLP to:
- Extract technical skills (programming languages, frameworks, tools)
- Identify soft skills (communication, leadership, teamwork)
- Map skills to interview topics using predefined mappings
- Determine experience level requirements

**Example Mapping:**
- "REST APIs" → "Backend Development"
- "Data Structures" → "DSA"
- "Machine Learning" → "AI/ML"

### 2. Company Research
The Research Agent analyzes companies using:
- **Pre-built Database**: FAANG, Big Tech, Fintech profiles
- **AI Analysis**: For unknown companies using Gemini API
- **Interview Pattern Recognition**: Typical rounds, difficulty, focus areas

**Company Types:**
- **FAANG**: Hard difficulty, 5-6 rounds, focus on algorithms + system design
- **Startup**: Medium difficulty, 3-4 rounds, focus on adaptability + full-stack
- **Enterprise**: Medium difficulty, standard process, focus on integration

### 3. Roadmap Generation
Combines extracted data to create:
- **Interview Rounds**: Type, topics, duration, weight
- **Preparation Order**: Optimized learning sequence
- **Timeline**: Based on difficulty and experience level
- **Resources**: Curated study materials

## 📊 Example Outputs

### Sample 1: Google Software Engineer (SDE-1)
**Input**: FAANG company, algorithms-focused role
```json
{
  "company": "Google",
  "role": "Software Engineer",
  "difficulty": "Hard",
  "rounds": [
    {
      "type": "Phone Screening",
      "topics": ["Resume", "Basic Technical"],
      "duration": "30 min"
    },
    {
      "type": "Coding Round 1", 
      "topics": ["Arrays", "Strings", "Hash Maps"],
      "duration": "45 min"
    },
    {
      "type": "System Design",
      "topics": ["Scalability", "Database Design"],
      "duration": "60 min"
    }
  ],
  "recommended_order": ["DSA Fundamentals", "System Design", "Behavioral"],
  "preparation_timeline": "18 weeks",
  "key_skills": ["Data Structures", "Algorithms", "System Design"]
}
```

### Sample 2: Microsoft Data Scientist
**Input**: Big Tech company, ML/AI specialization
```json
{
  "company": "Microsoft",
  "role": "Data Scientist", 
  "difficulty": "Hard",
  "rounds": [
    {
      "type": "Technical Assessment",
      "topics": ["Machine Learning", "Statistics", "Python"],
      "duration": "60 min"
    },
    {
      "type": "Case Study",
      "topics": ["Business Problem Solving", "Data Analysis"],
      "duration": "90 min"
    }
  ],
  "recommended_order": ["Statistics", "Machine Learning", "Python", "System Design"],
  "preparation_timeline": "14 weeks",
  "key_skills": ["Machine Learning", "Statistics", "Python"]
}
```

### Sample 3: Startup Full Stack Developer
**Input**: Early-stage company, versatility-focused
```json
{
  "company": "TechFlow (Startup)",
  "role": "Full Stack Developer",
  "difficulty": "Medium", 
  "rounds": [
    {
      "type": "Technical Assessment",
      "topics": ["JavaScript", "React", "Node.js"],
      "duration": "60 min"
    },
    {
      "type": "Practical Coding",
      "topics": ["Live Coding", "API Integration"],
      "duration": "75 min"
    }
  ],
  "recommended_order": ["JavaScript", "React", "Node.js", "System Architecture"],
  "preparation_timeline": "8 weeks",
  "key_skills": ["JavaScript", "React", "Full Stack Development"]
}
```

**📁 Complete examples available in `/examples/` directory**

## 🧪 Testing & Validation

The notebook includes comprehensive testing with sample job descriptions:

1. **Google SDE-1**: FAANG company, algorithms-focused
2. **Microsoft Data Scientist**: Big Tech, ML/AI focused  
3. **TechFlow Full Stack**: Startup, versatility-focused

Each test demonstrates different:
- Company types and difficulties
- Interview round structures
- Skill requirements and mappings
- Preparation strategies

## 🎯 Customization

### Adding New Companies
```python
company_profiles = {
    "your_company": {
        "type": "Enterprise", 
        "difficulty": "Medium",
        "focus": ["Domain Knowledge", "Problem Solving"]
    }
}
```

### Extending Skill Mappings
```python
skill_mapping = {
    "Your Technology": "Your Topic Category",
    "GraphQL": "Backend Development",
    "Kubernetes": "DevOps"
}
```

### Custom Round Types
```python
rounds = [
    {
        "type": "Design Challenge",
        "topics": ["UX/UI Design", "Product Thinking"],
        "duration": "90 min",
        "weight": "High"
    }
]
```

## 📈 Performance & Scalability

- **Response Time**: ~10-30 seconds per analysis
- **API Efficiency**: Optimized prompts to minimize token usage
- **Error Handling**: Graceful fallbacks when API calls fail
- **Extensibility**: Modular design for easy feature additions

## 🔧 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure Gemini API key is correctly configured
2. **JSON Parsing Error**: Agent includes fallback parsing mechanisms
3. **Unknown Company**: AI research will classify and analyze automatically
4. **Empty Job Description**: Agent will create role-based defaults

### Debug Mode
```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🚀 Future Enhancements

- [ ] Web search integration for real-time company research

## � Security & API Key Management

### Proper API Key Setup
1. **Never commit API keys** to version control
2. **Use environment variables**:
   ```bash
   export GEMINI_API_KEY="your_key_here"
   ```
3. **Or use .env file** (automatically gitignored):
   ```bash
   echo "GEMINI_API_KEY=your_key_here" > .env
   ```

### If You Accidentally Exposed an API Key
1. **Immediately regenerate** your API key at [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Update your local environment** with the new key
3. **Check GitHub Security tab** for any alerts

### Safe Development Practices
- ✅ Use `.env` files for local development
- ✅ Set environment variables in production
- ✅ Add sensitive files to `.gitignore`
- ❌ Never hardcode API keys in source code

- [ ] Web search integration for real-time company research
- [ ] Multiple LLM support (OpenAI, Claude, etc.)
- [ ] Advanced skill extraction using domain-specific models
- [ ] Interactive web interface
- [ ] Integration with job boards APIs
- [ ] Personalized recommendations based on user background

## 📝 Contributing

1. Fork the repository
2. Add new features or improvements
3. Test with various job descriptions
4. Submit pull request with examples

## 📄 License

MIT License - Feel free to use and modify for your projects.

## 🙏 Acknowledgments

- Google Gemini API for intelligent analysis
- Pydantic for robust data validation
- The open-source community for inspiration

---

**Built with ❤️ for helping job seekers prepare more effectively for technical interviews.**