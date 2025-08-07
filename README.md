# 🎓 AI Learning Path Generator

An intelligent, personalized learning path generator that uses AI and machine learning to create customized educational roadmaps based on your current skills, goals, and constraints.

## 🚀 Live Demo

**Try it now:** [AI Learning Path Generator Demo](https://ai-learning-path-generator-ihndahrii5hz2yg2cu6kpq.streamlit.app/)

Experience the full application with interactive features, personalized learning paths, and beautiful visualizations!

## 🌟 Features

- **🎯 Personalized Recommendations**: AI-powered analysis of your skill profile
- **📚 Curated Resources**: Access to high-quality learning materials from top platforms
- **⏱️ Time Optimization**: Realistic time estimates based on your availability
- **💰 Budget Consideration**: Cost-effective learning path suggestions
- **📊 Progress Analytics**: Detailed insights and tracking capabilities
- **🎨 Interactive Web Interface**: Beautiful Streamlit-based UI
- **⌨️ Command Line Interface**: For developers and automation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd ai-learning-path-generator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

The web interface will open in your browser automatically!

## 🖥️ Usage Options

### 1. Web Interface (Recommended)
```bash
python main.py
```
- Interactive Streamlit web interface
- Visual charts and analytics
- Easy profile management
- Best for most users

### 2. Command Line Interface
```bash
python main.py --cli
```
- Text-based interface
- Quick profile setup
- Perfect for developers and automation

### 3. Demo Mode
```bash
python main.py --demo
```
- See a sample learning path
- No profile setup required
- Great for trying out the system

## 📁 Project Structure

```
ai-learning-path-generator/
│
├── main.py              # Entry point with CLI options
├── user_profile.py      # User profile and skill management
├── path_engine.py       # Core AI learning path generation
├── ui.py               # Streamlit web interface
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🛠️ Module Overview

### `main.py`
- **Entry point** for the application
- **Command line interface** with argument parsing
- **Streamlit launcher** for web interface
- **Demo mode** for quick testing

### `user_profile.py`
- **UserProfile** class for storing user information
- **SkillMapper** for analyzing skill gaps and readiness
- **UserInputHandler** for collecting and validating user data
- **Enums** for skill levels and learning goals

### `path_engine.py`
- **PathEngine** class - core AI recommendation engine
- **LearningResource** database management
- **Path optimization** algorithms
- **Analytics** and insights generation

### `ui.py`
- **LearningPathUI** class for Streamlit interface
- **Interactive forms** for profile setup
- **Visualization** with Plotly charts
- **Multi-page** navigation system

## 🎯 How It Works

### 1. Profile Analysis
The system analyzes your:
- **Current skills** and proficiency levels
- **Learning goals** and target achievements
- **Time availability** and constraints
- **Budget** considerations
- **Learning style** preferences

### 2. Intelligent Matching
Using machine learning algorithms:
- **Resource matching** based on skill requirements
- **Prerequisite checking** for learning dependencies
- **Difficulty progression** optimization
- **Quality filtering** using ratings and reviews

### 3. Path Optimization
The AI engine:
- **Sequences resources** for maximum learning effectiveness
- **Balances difficulty** with engagement
- **Considers time** and budget constraints
- **Provides confidence scores** for each recommendation

## 📊 Sample Data

The system includes sample learning resources covering:

- **Programming**: Python, JavaScript, Web Development
- **Data Science**: Machine Learning, Data Analysis, Statistics
- **AI/ML**: Deep Learning, Neural Networks
- **Databases**: SQL, NoSQL, Data Warehousing
- **Cloud Computing**: AWS, Azure, DevOps

Resources include courses from platforms like:
- Coursera
- Udemy
- edX
- Khan Academy
- Free tutorials and documentation

## 🔧 Customization

### Adding New Resources
Edit the `_initialize_resource_database()` method in `path_engine.py`:

```python
LearningResource(
    id="unique_id",
    title="Resource Title",
    description="Detailed description",
    resource_type=ResourceType.COURSE,
    difficulty=Difficulty.INTERMEDIATE,
    estimated_hours=40,
    skills_taught=["Skill1", "Skill2"],
    prerequisites=["PrereqSkill"],
    cost_usd=99.99,
    rating=4.5,
    provider="Platform Name"
)
```

### Adding New Skills
Modify the `skill_categories` in `user_profile.py`:

```python
self.skill_categories = {
    "Your Category": ["Skill1", "Skill2", "Skill3"],
    # ... existing categories
}
```

### Customizing Prerequisites
Update `_get_prerequisites()` in `user_profile.py`:

```python
prerequisites_map = {
    "Advanced Skill": ["Basic Skill", "Intermediate Skill"],
    # ... existing mappings
}
```

## 📈 Analytics Features

The system provides comprehensive analytics:

- **Path Comparison**: Compare different learning paths
- **Resource Distribution**: Analyze types and difficulty levels
- **Time vs Confidence**: Visualize learning efficiency
- **Cost Analysis**: Budget breakdown and optimization
- **Progress Tracking**: Monitor advancement through paths

## 🎨 Web Interface Features

### Home Page
- Welcome message and quick start options
- Sample statistics and popular skills
- Navigation to different sections

### Profile Setup
- **Personal Information**: Name, email, preferences
- **Current Skills**: Add/manage existing skills with proficiency levels
- **Learning Goals**: Define what you want to achieve
- **Constraints**: Set time and budget limitations

### Path Generation
- **Profile Summary**: Overview of your setup
- **One-click Generation**: Generate personalized paths
- **Detailed Paths**: Step-by-step learning recommendations
- **Resource Information**: Complete details for each learning step

### Analytics Dashboard
- **Overview Metrics**: Total hours, costs, confidence scores
- **Interactive Charts**: Plotly visualizations
- **Resource Analysis**: Distribution and breakdown
- **Detailed Insights**: Per-path analytics

## 🛡️ Error Handling

The system includes robust error handling:
- **Input validation** for all user data
- **Graceful failures** with helpful error messages
- **Fallback options** when resources are unavailable
- **Data consistency** checks throughout the pipeline

## 🔮 Future Enhancements

Planned features for future versions:
- **Real-time progress tracking** with learning platforms
- **Community features** for peer learning and reviews
- **Advanced AI models** using OpenAI GPT for better recommendations
- **Mobile app** for on-the-go learning management
- **Certification tracking** and achievement badges
- **Integration APIs** with popular learning platforms
- **Machine learning model improvements** based on user feedback

## 🤝 Contributing

This is an open-source project! Contributions are welcome:

1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

Areas where contributions are especially welcome:
- **New learning resources** and platforms
- **Additional skill categories** and prerequisites
- **UI/UX improvements** and new features
- **Algorithm optimizations** and ML enhancements
- **Documentation** and tutorials

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

Having issues or questions?

- **Check the documentation** in this README
- **Run the demo** to see example output
- **Try the CLI mode** for debugging
- **Review error messages** for specific guidance

For additional support:
- Open an issue on the repository

## 🏃‍♀️ Quick Examples

### Example 1: Web Interface
```bash
python main.py
# Opens browser with interactive interface
# Follow the guided setup process
```

### Example 2: Command Line
```bash
python main.py --cli
# Interactive CLI prompts:
# Enter your name: John Doe
# Enter your email: john@example.com
# Hours per week available: 10
# Budget: 500
# Skills: Python,INTERMEDIATE
# Goals: Machine Learning,ADVANCED,1,6
```

### Example 3: Quick Demo
```bash
python main.py --demo
# Shows sample learning path for AI/ML
# No setup required
```

## 📝 Sample Output

```
🎯 Path 1: Machine Learning (INTERMEDIATE)
   Duration: 3 months
   Total Hours: 80
   Cost: $129.98
   Confidence: 84.5%
   Steps: 4 resources

   📖 Learning Steps:
   1. Python for Everybody Specialization
      Type: Course
      Duration: 60 hours
      Cost: $0.00
   
   2. Machine Learning A-Z: Hands-On Python & R
      Type: Course
      Duration: 40 hours
      Cost: $89.99
   
   ... and 2 more steps
```

---

**Happy Learning! 🎓✨** 