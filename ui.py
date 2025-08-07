"""
Streamlit User Interface
Interactive web interface for the AI Learning Path Generator.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from user_profile import (
    UserProfile, UserSkill, LearningGoal, SkillLevel, 
    SkillMapper, UserInputHandler, create_sample_profile
)
from path_engine import PathEngine, LearningPath, ResourceType, Difficulty

class LearningPathUI:
    """Main UI class for the learning path generator"""
    
    def __init__(self):
        # Check for OpenAI API key in session state or secrets
        openai_key = None
        try:
            if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
                openai_key = st.secrets['OPENAI_API_KEY']
        except Exception:
            # Secrets file not found or accessible, continue without it
            pass
        
        if not openai_key and 'openai_api_key' in st.session_state:
            openai_key = st.session_state.openai_api_key
        
        self.path_engine = PathEngine(openai_api_key=openai_key)
        self.skill_mapper = SkillMapper()
        self.input_handler = UserInputHandler()
        
        # Initialize session state
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = None
        if 'learning_paths' not in st.session_state:
            st.session_state.learning_paths = []
        if 'current_skills' not in st.session_state:
            st.session_state.current_skills = []
        if 'learning_goals' not in st.session_state:
            st.session_state.learning_goals = []
    
    def run(self):
        """Main function to run the Streamlit app"""
        st.set_page_config(
            page_title="AI Learning Path Generator",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🎓 AI Learning Path Generator")
        st.markdown("""
        **Create personalized learning paths based on your current skills and goals!**
        
        This AI-powered tool analyzes your skill profile and generates optimized learning paths 
        to help you achieve your professional development objectives.
        """)
        
        # Initialize current page in session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "🏠 Home"
        
        # Sidebar navigation
        page = st.sidebar.selectbox(
            "Navigation",
            ["🏠 Home", "👤 Profile Setup", "🎯 Generate Paths", "📊 Analytics", "ℹ️ About"],
            index=["🏠 Home", "👤 Profile Setup", "🎯 Generate Paths", "📊 Analytics", "ℹ️ About"].index(st.session_state.current_page)
        )
        
        # Update current page
        st.session_state.current_page = page
        
        # AI Configuration (optional)
        with st.sidebar.expander("🤖 AI Configuration", expanded=False):
            st.markdown("**🆓 FREE AI Integration Active!**")
            st.info("✅ Using Together AI (Llama 3.3 70B) for FREE resource generation")
            
            st.markdown("---")
            st.markdown("**Optional: OpenAI API Key**")
            st.markdown("Add your OpenAI key for additional AI models:")
            api_key_input = st.text_input(
                "OpenAI API Key", 
                type="password",
                value=st.session_state.get('openai_api_key', ''),
                help="Optional: Your OpenAI API key. We already use free AI for resource generation!"
            )
            if api_key_input != st.session_state.get('openai_api_key', ''):
                st.session_state.openai_api_key = api_key_input
                # Reinitialize path engine with new API key
                self.path_engine = PathEngine(openai_api_key=api_key_input)
                st.success("OpenAI API key added as backup!")
            
            if not api_key_input:
                st.markdown("🎉 **No worries!** Your app works perfectly with free AI.")
        
        if page == "🏠 Home":
            self.show_home_page()
        elif page == "👤 Profile Setup":
            self.show_profile_setup()
        elif page == "🎯 Generate Paths":
            self.show_path_generation()
        elif page == "📊 Analytics":
            self.show_analytics()
        elif page == "ℹ️ About":
            self.show_about_page()
    
    def show_home_page(self):
        """Display the home page"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.header("Welcome to Your Personalized Learning Journey! 🚀")
            
            st.markdown("""
            ### How it works:
            1. **Set up your profile** - Tell us about your current skills and experience
            2. **Define your goals** - What do you want to learn or achieve?
            3. **Get your path** - Receive a personalized learning roadmap
            4. **Track progress** - Monitor your advancement and adjust as needed
            
            ### Features:
            - 🎯 **Personalized recommendations** based on your skill level
            - 📚 **Curated resources** from top learning platforms
            - ⏱️ **Time estimation** based on your availability
            - 💰 **Budget consideration** for cost-effective learning
            - 📈 **Progress tracking** and analytics
            """)
            
            # Quick start buttons
            st.markdown("### Quick Start")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🆕 Create New Profile", type="primary"):
                    # Clear all profile-related session state
                    st.session_state.user_profile = None
                    st.session_state.current_skills = []
                    st.session_state.learning_goals = []
                    st.session_state.learning_paths = []
                    st.session_state.current_page = "👤 Profile Setup"
                    st.rerun()
            with col_b:
                if st.button("📋 Load Sample Profile"):
                    st.session_state.user_profile = create_sample_profile()
                    st.success("Sample profile loaded! Go to 'Generate Paths' to see recommendations.")
        
        with col2:
            st.header("Quick Stats")
            
            # Show some sample statistics
            stats_data = {
                "Learning Resources": 500,
                "Skill Categories": 6,
                "Average Path Length": "3-5 months",
                "Success Rate": "87%"
            }
            
            for stat, value in stats_data.items():
                st.metric(stat, value)
            
            # Show sample skills
            st.subheader("Popular Skills")
            popular_skills = [
                "Machine Learning", "Python", "Data Analysis",
                "Web Development", "Cloud Computing", "SQL"
            ]
            for skill in popular_skills:
                st.write(f"• {skill}")
    
    def show_profile_setup(self):
        """Display profile setup interface"""
        st.header("👤 Profile Setup")
        
        # Personal Information
        st.subheader("Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", value="Alex Johnson" if st.session_state.user_profile else "")
            email = st.text_input("Email", value="alex.johnson@example.com" if st.session_state.user_profile else "")
        
        with col2:
            learning_style = st.selectbox(
                "Preferred Learning Style",
                ["Visual and Hands-on", "Reading and Theory", "Interactive", "Project-based"],
                index=0
            )
            time_commitment = st.slider("Hours per week available for learning", 1, 40, 10)
        
        budget = st.number_input("Monthly learning budget (USD)", min_value=0.0, value=500.0, step=50.0)
        
        # Current Skills
        st.subheader("Current Skills")
        st.markdown("Add your existing skills and rate your proficiency level:")
        
        # Skills input
        if 'current_skills' not in st.session_state:
            st.session_state.current_skills = []
        
        # Add new skill form
        with st.expander("➕ Add New Skill"):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                skill_name = st.text_input("Skill Name", key="new_skill_name")
            with col2:
                skill_level = st.selectbox("Level", [l.name for l in SkillLevel], key="new_skill_level")
            with col3:
                years_exp = st.number_input("Years Experience", min_value=0.0, max_value=50.0, 
                                          step=0.5, key="new_skill_years")
            with col4:
                confidence = st.slider("Confidence (1-10)", 1, 10, 5, key="new_skill_confidence")
            
            if st.button("Add Skill"):
                if skill_name:
                    new_skill = UserSkill(
                        skill_name=skill_name,
                        level=SkillLevel[skill_level],
                        years_experience=years_exp,
                        confidence_score=confidence
                    )
                    st.session_state.current_skills.append(new_skill)
                    st.success(f"Added {skill_name} to your skills!")
                    st.rerun()
        
        # Display current skills
        if st.session_state.current_skills:
            st.markdown("**Your Current Skills:**")
            skills_df = pd.DataFrame([
                {
                    "Skill": skill.skill_name,
                    "Level": skill.level.name,
                    "Years": skill.years_experience,
                    "Confidence": skill.confidence_score
                }
                for skill in st.session_state.current_skills
            ])
            st.dataframe(skills_df, use_container_width=True)
            
            if st.button("🗑️ Clear All Skills"):
                st.session_state.current_skills = []
                st.rerun()
        
        # Learning Goals
        st.subheader("Learning Goals")
        st.markdown("What do you want to learn or achieve?")
        
        if 'learning_goals' not in st.session_state:
            st.session_state.learning_goals = []
        
        # Add new goal form
        with st.expander("🎯 Add New Learning Goal"):
            col1, col2, col3, col4 = st.columns([3, 2, 1, 2])
            
            with col1:
                goal_name = st.text_input("Goal/Skill to Learn", key="new_goal_name")
            with col2:
                target_level = st.selectbox("Target Level", [l.name for l in SkillLevel], key="new_goal_level")
            with col3:
                priority = st.slider("Priority (1-5)", 1, 5, 3, key="new_goal_priority")
            with col4:
                timeline = st.number_input("Timeline (months)", min_value=1, max_value=24, 
                                         value=6, key="new_goal_timeline")
            
            if st.button("Add Goal"):
                if goal_name:
                    new_goal = LearningGoal(
                        goal_name=goal_name,
                        target_skill_level=SkillLevel[target_level],
                        priority=priority,
                        timeline_months=timeline
                    )
                    st.session_state.learning_goals.append(new_goal)
                    st.success(f"Added {goal_name} to your learning goals!")
                    st.rerun()
        
        # Display learning goals
        if st.session_state.learning_goals:
            st.markdown("**Your Learning Goals:**")
            goals_df = pd.DataFrame([
                {
                    "Goal": goal.goal_name,
                    "Target Level": goal.target_skill_level.name,
                    "Priority": goal.priority,
                    "Timeline (months)": goal.timeline_months
                }
                for goal in st.session_state.learning_goals
            ])
            st.dataframe(goals_df, use_container_width=True)
            
            if st.button("🗑️ Clear All Goals"):
                st.session_state.learning_goals = []
                st.rerun()
        
        # Save Profile
        st.subheader("Save Profile")
        if st.button("💾 Save Profile", type="primary"):
            if name and email and st.session_state.current_skills and st.session_state.learning_goals:
                profile = UserProfile(
                    name=name,
                    email=email,
                    current_skills=st.session_state.current_skills,
                    learning_goals=st.session_state.learning_goals,
                    preferred_learning_style=learning_style,
                    time_commitment_hours_per_week=time_commitment,
                    budget_usd=budget
                )
                
                # Validate profile
                is_valid, errors = self.input_handler.validate_profile(profile)
                
                if is_valid:
                    st.session_state.user_profile = profile
                    st.success("✅ Profile saved successfully! You can now generate learning paths.")
                else:
                    st.error("❌ Profile validation failed:")
                    for error in errors:
                        st.write(f"• {error}")
            else:
                st.warning("⚠️ Please fill in all required fields (name, email, skills, and goals).")
    
    def show_path_generation(self):
        """Display learning path generation interface"""
        st.header("🎯 Generate Learning Paths")
        
        if not st.session_state.user_profile:
            st.warning("⚠️ Please set up your profile first before generating learning paths.")
            if st.button("Go to Profile Setup"):
                st.rerun()
            return
        
        profile = st.session_state.user_profile
        
        # Display user summary
        with st.expander("👤 Your Profile Summary", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Skills", len(profile.current_skills))
                st.metric("Learning Goals", len(profile.learning_goals))
            with col2:
                st.metric("Weekly Time Commitment", f"{profile.time_commitment_hours_per_week} hours")
                st.metric("Budget", f"${profile.budget_usd}")
            with col3:
                st.write("**Skills:**")
                for skill in profile.current_skills[:3]:
                    st.write(f"• {skill.skill_name} ({skill.level.name})")
                if len(profile.current_skills) > 3:
                    st.write(f"... and {len(profile.current_skills) - 3} more")
        
        # Generate paths button
        if st.button("🚀 Generate Learning Paths", type="primary"):
            with st.spinner("Generating personalized learning paths..."):
                try:
                    paths = self.path_engine.generate_multiple_paths(profile)
                    st.session_state.learning_paths = paths
                    st.success(f"✅ Generated {len(paths)} learning path(s)!")
                except Exception as e:
                    st.error(f"❌ Error generating paths: {str(e)}")
        
        # Display generated paths
        if st.session_state.learning_paths:
            st.subheader("📚 Your Personalized Learning Paths")
            
            for i, path in enumerate(st.session_state.learning_paths):
                with st.expander(f"🎯 Path {i+1}: {path.goal_skill} ({path.target_level.name})", expanded=i==0):
                    self.display_learning_path(path)
    
    def display_learning_path(self, path: LearningPath):
        """Display a single learning path"""
        # Path overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Hours", path.total_estimated_hours)
        with col2:
            st.metric("Estimated Duration", f"{path.estimated_completion_months} months")
        with col3:
            st.metric("Total Cost", f"${path.total_cost_usd:.2f}")
        with col4:
            st.metric("Confidence Score", f"{path.confidence_score:.1%}")
        
        # Display skill tree path
        if hasattr(path, 'skill_tree_path') and path.skill_tree_path:
            st.markdown("### 🗺️ Learning Path Overview")
            st.write(" → ".join(path.skill_tree_path))
            st.markdown("---")
        
        # Learning modules and steps
        st.markdown("### 📚 Learning Modules")
        
        if not hasattr(path, 'modules') or not path.modules:
            st.warning("No learning modules found for this path.")
            return
            
        for module_idx, module in enumerate(path.modules, 1):
            # Safely get module name
            module_name = getattr(module, 'module_name', f'Module {module_idx}')
            try:
                # Use container instead of nested expander
                st.markdown(f"#### 📖 Module {module_idx}: {module_name}")
                
                # Module overview
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Module Hours", getattr(module, 'estimated_hours', 0))
                with col2:
                    difficulty = getattr(module, 'difficulty', None)
                    difficulty_name = difficulty.name if difficulty and hasattr(difficulty, 'name') else 'Unknown'
                    st.metric("Difficulty", difficulty_name)
                with col3:
                    steps = getattr(module, 'steps', [])
                    st.metric("Steps", len(steps))
                
                # Module details
                description = getattr(module, 'description', 'No description available')
                st.markdown(f"**Description:** {description}")
                
                skills_taught = getattr(module, 'skills_taught', [])
                if skills_taught:
                    st.markdown(f"**Skills Taught:** {', '.join(skills_taught)}")
                
                prerequisites = getattr(module, 'prerequisites', [])
                if prerequisites:
                    st.markdown(f"**Prerequisites:** {', '.join(prerequisites)}")
                
                # Module steps
                st.markdown("##### 📝 Learning Steps")
                
                for step in steps:
                    resource = getattr(step, 'resource', None)
                    if resource:
                        with st.container():
                            title = getattr(resource, 'title', 'Untitled Resource')
                            description = getattr(resource, 'description', 'No description available')
                            step_number = getattr(step, 'step_number', 1)
                            
                            st.markdown(f"""
                            **Step {step_number}: {title}**
                            
                            📝 *{description}*
                            """)
                            
                            # Resource details in columns
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                resource_type = getattr(resource, 'resource_type', None)
                                type_name = resource_type.name if resource_type and hasattr(resource_type, 'name') else 'Unknown'
                                st.write(f"**Type:** {type_name}")
                            with col2:
                                hours = getattr(resource, 'estimated_hours', 0)
                                st.write(f"**Duration:** {hours}h")
                            with col3:
                                cost = getattr(resource, 'cost_usd', 0)
                                st.write(f"**Cost:** ${cost:.2f}")
                            with col4:
                                rating = getattr(resource, 'rating', 0)
                                st.write(f"**Rating:** {rating:.1f}/5")
                            
                            # Resource link
                            url = getattr(resource, 'url', None)
                            if url and url.startswith('http'):
                                st.markdown(f"🔗 [Access Resource]({url})")
                            else:
                                st.info("🔗 Resource link will be generated using AI")
                            
                            st.markdown("---")
                
                # Add separator between modules
                st.markdown("---")
                
            except Exception as e:
                st.error(f"Error displaying module {module_idx}: {str(e)}")
                continue
    
    def show_analytics(self):
        """Display analytics and insights"""
        st.header("📊 Learning Path Analytics")
        
        if not st.session_state.learning_paths:
            st.warning("⚠️ No learning paths generated yet. Please generate paths first.")
            return
        
        paths = st.session_state.learning_paths
        
        # Overall analytics
        st.subheader("📈 Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_paths = len(paths)
            st.metric("Total Paths", total_paths)
        with col2:
            total_hours = sum(path.total_estimated_hours for path in paths)
            st.metric("Total Learning Hours", total_hours)
        with col3:
            total_cost = sum(path.total_cost_usd for path in paths)
            st.metric("Total Investment", f"${total_cost:.2f}")
        with col4:
            avg_confidence = sum(path.confidence_score for path in paths) / len(paths)
            st.metric("Average Confidence", f"{avg_confidence:.1%}")
        
        # Path comparison chart
        st.subheader("📊 Path Comparison")
        
        # Prepare data for visualization
        path_data = []
        for path in paths:
            # Calculate total resources across all modules
            total_resources = sum(len(module.steps) for module in path.modules)
            path_data.append({
                'Goal': path.goal_skill,
                'Hours': path.total_estimated_hours,
                'Months': path.estimated_completion_months,
                'Cost': path.total_cost_usd,
                'Confidence': path.confidence_score,
                'Resources': total_resources,
                'Modules': len(path.modules)
            })
        
        df = pd.DataFrame(path_data)
        
        # Create visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Time vs Confidence scatter plot
            fig = px.scatter(df, x='Hours', y='Confidence', 
                           size='Cost', color='Goal',
                           title='Learning Time vs Confidence',
                           labels={'Hours': 'Total Hours', 'Confidence': 'Confidence Score'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Cost breakdown
            fig = px.bar(df, x='Goal', y='Cost',
                        title='Learning Path Costs',
                        labels={'Cost': 'Cost (USD)', 'Goal': 'Learning Goal'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Resource type distribution
        st.subheader("📚 Resource Analysis")
        
        # Aggregate resource types across all paths
        resource_types = {}
        difficulty_levels = {}
        
        for path in paths:
            for module in path.modules:
                for step in module.steps:
                    resource_type = step.resource.resource_type.value
                    difficulty = step.resource.difficulty.name
                    
                    resource_types[resource_type] = resource_types.get(resource_type, 0) + 1
                    difficulty_levels[difficulty] = difficulty_levels.get(difficulty, 0) + 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Resource types pie chart
            if resource_types:
                fig = px.pie(values=list(resource_types.values()), 
                           names=list(resource_types.keys()),
                           title='Resource Types Distribution')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Difficulty levels bar chart
            if difficulty_levels:
                fig = px.bar(x=list(difficulty_levels.keys()), 
                           y=list(difficulty_levels.values()),
                           title='Difficulty Levels Distribution',
                           labels={'x': 'Difficulty Level', 'y': 'Number of Resources'})
                st.plotly_chart(fig, use_container_width=True)
        
        # Detailed path analytics
        st.subheader("🔍 Detailed Path Analytics")
        
        selected_path = st.selectbox("Select a path for detailed analysis:", 
                                   [f"{path.goal_skill} ({path.target_level.name})" for path in paths])
        
        if selected_path:
            path_index = next(i for i, path in enumerate(paths) 
                            if f"{path.goal_skill} ({path.target_level.name})" == selected_path)
            path = paths[path_index]
            
            analytics = self.path_engine.get_path_analytics(path)
            
            # Display analytics
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Path Metrics:**")
                st.write(f"• Total Resources: {analytics['total_resources']}")
                st.write(f"• Average Rating: {analytics['avg_resource_rating']:.1f}/5")
                st.write(f"• Free Resources: {analytics['free_resources_count']}")
                st.write(f"• Weekly Hours: {analytics['estimated_weekly_hours']:.1f}")
            
            with col2:
                st.write("**Resource Breakdown:**")
                for resource_type, count in analytics['resource_types'].items():
                    if count > 0:
                        st.write(f"• {resource_type.title()}: {count}")
    
    def show_about_page(self):
        """Display about page"""
        st.header("ℹ️ About AI Learning Path Generator")
        
        st.markdown("""
        ### 🎯 Mission
        To democratize personalized learning by providing AI-powered, data-driven learning path recommendations 
        that adapt to individual skills, goals, and constraints.
        
        ### 🤖 How It Works
        
        **1. Profile Analysis**
        - Analyzes your current skills and experience levels
        - Evaluates your learning goals and priorities
        - Considers your time and budget constraints
        
        **2. Intelligent Matching**
        - Uses machine learning algorithms to match you with relevant resources
        - Considers prerequisites and skill dependencies
        - Optimizes for your learning style and preferences
        
        **3. Path Optimization**
        - Sequences learning resources for maximum effectiveness
        - Balances difficulty progression with engagement
        - Provides time and cost estimates
        
        ### 🛠️ Technology Stack
        - **Frontend:** Streamlit for interactive web interface
        - **Backend:** Python with scikit-learn for ML algorithms
        - **Data Processing:** Pandas and NumPy for data manipulation
        - **Visualization:** Plotly and Matplotlib for charts
        - **AI Integration:** OpenAI API for enhanced recommendations
        
        ### 📊 Features
        - ✅ Personalized learning path generation
        - ✅ Skill gap analysis
        - ✅ Resource recommendation engine
        - ✅ Progress tracking and analytics
        - ✅ Budget and time optimization
        - ✅ Multi-goal path planning
        
        ### 🔮 Future Enhancements
        - Integration with learning platforms for progress tracking
        - Community features for peer learning
        - Advanced AI models for better personalization
        - Mobile app for on-the-go learning
        - Certification and achievement tracking
        
        ### 👥 Contributing
        This is an open-source project. Contributions are welcome!
        
        ### 📞 Support
        For questions or support, please contact: support@learningpathgen.ai
        """)

def main():
    """Main function to run the Streamlit app"""
    app = LearningPathUI()
    app.run()

if __name__ == "__main__":
    main() 