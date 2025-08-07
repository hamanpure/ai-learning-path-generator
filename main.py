#!/usr/bin/env python3
"""
AI Learning Path Generator
Main entry point for the application.

This application generates personalized learning paths based on user skills,
goals, and preferences using AI and machine learning algorithms.

Usage:
    python main.py                    # Run Streamlit web interface
    python main.py --demo            # Run with sample data
    python main.py --cli             # Run command line interface
    python main.py --generate-sample # Generate and display sample learning path
"""

import argparse
import sys
import os
from typing import List

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user_profile import (
    UserProfile, UserSkill, LearningGoal, SkillLevel,
    SkillMapper, UserInputHandler, create_sample_profile
)
from path_engine import PathEngine, LearningPath
from ui import LearningPathUI

def run_streamlit_app():
    """Launch the Streamlit web interface"""
    print("🚀 Starting AI Learning Path Generator Web Interface...")
    print("📊 Open your browser and navigate to the URL shown below.")
    print("🔄 Use Ctrl+C to stop the application.")
    print("-" * 50)
    
    # Import and run streamlit
    try:
        import streamlit.web.cli as stcli
        import streamlit as st
        
        # Run the Streamlit app
        sys.argv = ["streamlit", "run", __file__, "--", "--streamlit"]
        stcli.main()
    except ImportError:
        print("❌ Streamlit not installed. Please install it using:")
        print("   pip install streamlit")
        sys.exit(1)

def run_cli_interface():
    """Run command line interface for the learning path generator"""
    print("🎓 AI Learning Path Generator - CLI Mode")
    print("=" * 50)
    
    # Initialize components
    input_handler = UserInputHandler()
    path_engine = PathEngine()
    
    try:
        # Collect user information
        print("\n📝 Let's set up your learning profile...")
        
        # Basic info
        name = input("Enter your name: ").strip()
        email = input("Enter your email: ").strip()
        
        if not name or not email:
            print("❌ Name and email are required.")
            return
        
        # Time commitment
        try:
            hours_per_week = int(input("Hours per week available for learning (1-40): "))
            if not 1 <= hours_per_week <= 40:
                raise ValueError()
        except ValueError:
            print("❌ Please enter a valid number between 1 and 40.")
            return
        
        # Budget
        try:
            budget = float(input("Monthly learning budget in USD (0 for free resources only): "))
            if budget < 0:
                raise ValueError()
        except ValueError:
            print("❌ Please enter a valid budget amount.")
            return
        
        # Current skills
        print("\n🛠️ Enter your current skills:")
        print("Format: skill_name,level (where level is BEGINNER, INTERMEDIATE, ADVANCED, or EXPERT)")
        print("Example: Python,INTERMEDIATE")
        print("Type 'done' when finished.")
        
        current_skills = []
        while True:
            skill_input = input("Skill: ").strip()
            if skill_input.lower() == 'done':
                break
            
            try:
                skill_name, level_str = skill_input.split(',')
                skill_name = skill_name.strip()
                level_str = level_str.strip().upper()
                
                level = SkillLevel[level_str]
                
                # Default values for CLI
                skill = UserSkill(
                    skill_name=skill_name,
                    level=level,
                    years_experience=1.0,  # Default
                    confidence_score=7     # Default
                )
                current_skills.append(skill)
                print(f"✅ Added {skill_name} ({level.name})")
                
            except (ValueError, KeyError):
                print("❌ Invalid format. Please use: skill_name,LEVEL")
                continue
        
        if not current_skills:
            print("❌ At least one skill is required.")
            return
        
        # Learning goals
        print("\n🎯 Enter your learning goals:")
        print("Format: goal_name,target_level,priority,timeline_months")
        print("Example: Machine Learning,INTERMEDIATE,1,6")
        print("Type 'done' when finished.")
        
        learning_goals = []
        while True:
            goal_input = input("Goal: ").strip()
            if goal_input.lower() == 'done':
                break
            
            try:
                parts = goal_input.split(',')
                if len(parts) != 4:
                    raise ValueError()
                
                goal_name = parts[0].strip()
                target_level = SkillLevel[parts[1].strip().upper()]
                priority = int(parts[2].strip())
                timeline = int(parts[3].strip())
                
                if not 1 <= priority <= 5:
                    raise ValueError("Priority must be 1-5")
                if not 1 <= timeline <= 24:
                    raise ValueError("Timeline must be 1-24 months")
                
                goal = LearningGoal(
                    goal_name=goal_name,
                    target_skill_level=target_level,
                    priority=priority,
                    timeline_months=timeline
                )
                learning_goals.append(goal)
                print(f"✅ Added goal: {goal_name} ({target_level.name})")
                
            except (ValueError, KeyError) as e:
                print(f"❌ Invalid format: {e}")
                print("Please use: goal_name,target_level,priority(1-5),timeline_months(1-24)")
                continue
        
        if not learning_goals:
            print("❌ At least one learning goal is required.")
            return
        
        # Create user profile
        profile = UserProfile(
            name=name,
            email=email,
            current_skills=current_skills,
            learning_goals=learning_goals,
            preferred_learning_style="Mixed",
            time_commitment_hours_per_week=hours_per_week,
            budget_usd=budget if budget > 0 else None
        )
        
        # Generate learning paths
        print("\n🤖 Generating personalized learning paths...")
        paths = path_engine.generate_multiple_paths(profile)
        
        # Display results
        print(f"\n📚 Generated {len(paths)} learning path(s):")
        print("=" * 50)
        
        for i, path in enumerate(paths, 1):
            print(f"\n🎯 Path {i}: {path.goal_skill} ({path.target_level.name})")
            print(f"   Duration: {path.estimated_completion_months} months")
            print(f"   Total Hours: {path.total_estimated_hours}")
            print(f"   Cost: ${path.total_cost_usd:.2f}")
            print(f"   Confidence: {path.confidence_score:.1%}")
            total_resources = sum(len(module.steps) for module in path.modules)
            print(f"   Modules: {len(path.modules)}, Total Resources: {total_resources}")
            
            print("\n   📚 Learning Modules:")
            for module_idx, module in enumerate(path.modules[:2], 1):  # Show first 2 modules
                print(f"   Module {module_idx}: {module.module_name}")
                print(f"      Description: {module.description}")
                print(f"      Hours: {module.estimated_hours}")
                print(f"      Steps: {len(module.steps)}")
                if module.steps:
                    print(f"      First Step: {module.steps[0].resource.title}")
            
            if len(path.modules) > 2:
                print(f"   ... and {len(path.modules) - 2} more modules")
        
        print("\n🎉 Learning paths generated successfully!")
        print("💡 Run with --streamlit flag for a better visual experience.")
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

def generate_sample_path():
    """Generate and display a sample learning path"""
    print("🎓 AI Learning Path Generator - Sample Generation")
    print("=" * 50)
    
    # Create sample profile
    print("👤 Using sample user profile...")
    profile = create_sample_profile()
    
    print(f"Name: {profile.name}")
    print(f"Skills: {', '.join(skill.skill_name for skill in profile.current_skills)}")
    print(f"Goals: {', '.join(goal.goal_name for goal in profile.learning_goals)}")
    print(f"Time Commitment: {profile.time_commitment_hours_per_week} hours/week")
    print(f"Budget: ${profile.budget_usd}")
    
    # Generate paths
    print("\n🤖 Generating learning paths...")
    path_engine = PathEngine()
    paths = path_engine.generate_multiple_paths(profile)
    
    # Display first path in detail
    if paths:
        path = paths[0]
        print(f"\n📚 Sample Learning Path: {path.goal_skill}")
        print("=" * 50)
        print(f"🎯 Target Level: {path.target_level.name}")
        print(f"⏱️ Duration: {path.estimated_completion_months} months")
        print(f"📊 Total Hours: {path.total_estimated_hours}")
        print(f"💰 Total Cost: ${path.total_cost_usd:.2f}")
        print(f"🎯 Confidence: {path.confidence_score:.1%}")
        
        print("\n📚 Learning Modules:")
        for module_idx, module in enumerate(path.modules, 1):
            print(f"\n📖 Module {module_idx}: {module.module_name}")
            print(f"   📝 {module.description}")
            print(f"   🎯 Skills: {', '.join(module.skills_taught)}")
            print(f"   ⏱️ Module Hours: {module.estimated_hours}")
            print(f"   📊 Difficulty: {module.difficulty.name}")
            
            print(f"\n   📋 Learning Steps:")
            for step in module.steps:
                resource = step.resource
                print(f"   {step.step_number}. {resource.title}")
                print(f"      📝 {resource.description}")
                print(f"      🏷️ Type: {resource.resource_type.value.title()}")
                print(f"      ⏱️ Time: {resource.estimated_hours} hours")
                print(f"      💰 Cost: ${resource.cost_usd:.2f}")
                print(f"      ⭐ Rating: {resource.rating}/5")
                if resource.provider:
                    print(f"      🏢 Provider: {resource.provider}")
                if resource.prerequisites:
                    print(f"      📋 Prerequisites: {', '.join(resource.prerequisites)}")
                print()
    
    print("\n✨ Sample generation complete!")

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(
        description="AI Learning Path Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Launch web interface
  python main.py --cli             # Run command line interface
  python main.py --demo            # Generate sample learning path
  python main.py --streamlit       # Force web interface (same as default)
        """
    )
    
    parser.add_argument(
        '--cli', 
        action='store_true',
        help='Run in command line interface mode'
    )
    
    parser.add_argument(
        '--demo', 
        action='store_true',
        help='Generate and display a sample learning path'
    )
    
    parser.add_argument(
        '--streamlit', 
        action='store_true',
        help='Run Streamlit web interface (default)'
    )
    
    args = parser.parse_args()
    
    # Check if running from streamlit
    if len(sys.argv) > 1 and sys.argv[-1] == '--streamlit':
        # This is called by streamlit, run the UI
        app = LearningPathUI()
        app.run()
        return
    
    # Handle command line arguments
    if args.cli:
        run_cli_interface()
    elif args.demo:
        generate_sample_path()
    else:
        # Default: run Streamlit interface
        run_streamlit_app()

if __name__ == "__main__":
    main() 