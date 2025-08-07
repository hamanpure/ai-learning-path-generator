"""
User Profile Module
Handles user input, skill assessment, and profile management for the AI Learning Path Generator.
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class SkillLevel(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

@dataclass
class UserSkill:
    """Represents a user's skill in a specific area"""
    skill_name: str
    level: SkillLevel
    years_experience: float
    confidence_score: int  # 1-10 scale

@dataclass
class LearningGoal:
    """Represents a user's learning objective"""
    goal_name: str
    target_skill_level: SkillLevel
    priority: int  # 1-5 scale
    timeline_months: int

@dataclass
class UserProfile:
    """Complete user profile including skills, goals, and preferences"""
    name: str
    email: str
    current_skills: List[UserSkill]
    learning_goals: List[LearningGoal]
    preferred_learning_style: str
    time_commitment_hours_per_week: int
    budget_usd: Optional[float] = None
    
class SkillMapper:
    """Maps and analyzes user skills and learning requirements"""
    
    def __init__(self):
        self.skill_categories = {
            "Programming": ["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
            "Data Science": ["Machine Learning", "Statistics", "Data Analysis", "Deep Learning"],
            "Web Development": ["Frontend", "Backend", "Full Stack", "DevOps"],
            "Cloud Computing": ["AWS", "Azure", "GCP", "Docker", "Kubernetes"],
            "Databases": ["SQL", "NoSQL", "Database Design", "Data Warehousing"],
            "Soft Skills": ["Leadership", "Communication", "Project Management"]
        }
    
    def assess_skill_gaps(self, user_profile: UserProfile) -> Dict[str, List[str]]:
        """Identify skill gaps based on user's current skills and goals"""
        current_skill_names = {skill.skill_name for skill in user_profile.current_skills}
        goal_skills = {goal.goal_name for goal in user_profile.learning_goals}
        
        skill_gaps = {}
        for category, skills in self.skill_categories.items():
            missing_skills = []
            for skill in skills:
                if skill in goal_skills and skill not in current_skill_names:
                    missing_skills.append(skill)
            if missing_skills:
                skill_gaps[category] = missing_skills
        
        return skill_gaps
    
    def calculate_readiness_score(self, user_profile: UserProfile, target_skill: str) -> float:
        """Calculate how ready a user is to learn a specific skill (0-1 scale)"""
        # Find prerequisite skills for the target skill
        prerequisites = self._get_prerequisites(target_skill)
        
        if not prerequisites:
            return 0.8  # No prerequisites needed
        
        readiness_scores = []
        for prereq in prerequisites:
            user_skill = self._find_user_skill(user_profile, prereq)
            if user_skill:
                # Convert skill level and confidence to readiness score
                level_score = user_skill.level.value / 4.0
                confidence_score = user_skill.confidence_score / 10.0
                readiness_scores.append((level_score + confidence_score) / 2)
            else:
                readiness_scores.append(0.0)  # Missing prerequisite
        
        return sum(readiness_scores) / len(readiness_scores) if readiness_scores else 0.0
    
    def _get_prerequisites(self, skill: str) -> List[str]:
        """Define prerequisite skills for various learning paths"""
        prerequisites_map = {
            "Machine Learning": ["Python", "Statistics", "Data Analysis"],
            "Deep Learning": ["Machine Learning", "Python", "Statistics"],
            "Backend": ["Programming fundamentals"],
            "Full Stack": ["Frontend", "Backend"],
            "DevOps": ["Backend", "Cloud Computing"],
            "Kubernetes": ["Docker", "Cloud Computing"],
            "Data Warehousing": ["SQL", "Database Design"]
        }
        return prerequisites_map.get(skill, [])
    
    def _find_user_skill(self, user_profile: UserProfile, skill_name: str) -> Optional[UserSkill]:
        """Find a specific skill in user's profile"""
        for skill in user_profile.current_skills:
            if skill.skill_name.lower() == skill_name.lower():
                return skill
        return None

class UserInputHandler:
    """Handles user input collection and validation"""
    
    def collect_basic_info(self) -> Tuple[str, str]:
        """Collect basic user information"""
        # This would typically be called from the UI
        # For now, return placeholder values
        return "User", "user@example.com"
    
    def collect_current_skills(self) -> List[UserSkill]:
        """Collect user's current skills and proficiency levels"""
        # In a real implementation, this would collect from UI
        # Returning sample data for demonstration
        return [
            UserSkill("Python", SkillLevel.INTERMEDIATE, 2.0, 7),
            UserSkill("SQL", SkillLevel.BEGINNER, 0.5, 5)
        ]
    
    def collect_learning_goals(self) -> List[LearningGoal]:
        """Collect user's learning objectives"""
        # Sample learning goals
        return [
            LearningGoal("Machine Learning", SkillLevel.INTERMEDIATE, 1, 6),
            LearningGoal("Data Analysis", SkillLevel.ADVANCED, 2, 4)
        ]
    
    def validate_profile(self, profile: UserProfile) -> Tuple[bool, List[str]]:
        """Validate user profile completeness and consistency"""
        errors = []
        
        if not profile.name or len(profile.name.strip()) == 0:
            errors.append("Name is required")
        
        if not profile.email or "@" not in profile.email:
            errors.append("Valid email is required")
        
        if not profile.current_skills:
            errors.append("At least one current skill must be specified")
        
        if not profile.learning_goals:
            errors.append("At least one learning goal must be specified")
        
        if profile.time_commitment_hours_per_week <= 0:
            errors.append("Time commitment must be positive")
        
        return len(errors) == 0, errors

def create_sample_profile() -> UserProfile:
    """Create a sample user profile for testing"""
    current_skills = [
        UserSkill("Python", SkillLevel.INTERMEDIATE, 2.0, 7),
        UserSkill("SQL", SkillLevel.BEGINNER, 0.5, 5),
        UserSkill("Statistics", SkillLevel.BEGINNER, 1.0, 4)
    ]
    
    learning_goals = [
        LearningGoal("Machine Learning", SkillLevel.INTERMEDIATE, 1, 6),
        LearningGoal("Data Analysis", SkillLevel.ADVANCED, 2, 4),
        LearningGoal("Deep Learning", SkillLevel.BEGINNER, 3, 12)
    ]
    
    return UserProfile(
        name="Alex Johnson",
        email="alex.johnson@example.com",
        current_skills=current_skills,
        learning_goals=learning_goals,
        preferred_learning_style="Visual and Hands-on",
        time_commitment_hours_per_week=10,
        budget_usd=500.0
    )

def get_user_profile(
    name: str = None,
    email: str = None,
    current_skills_input: List[Dict] = None,
    learning_goals_input: List[Dict] = None,
    preferred_learning_style: str = None,
    time_commitment_hours_per_week: int = None,
    budget_usd: float = None,
    interactive: bool = False
) -> UserProfile:
    """
    Comprehensive function to get user profile from various input sources.
    
    Args:
        name: User's full name
        email: User's email address
        current_skills_input: List of skill dictionaries with keys:
            - skill_name (str): Name of the skill
            - level (str): Skill level ('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT')
            - years_experience (float): Years of experience (optional, default 1.0)
            - confidence_score (int): Confidence level 1-10 (optional, default 5)
        learning_goals_input: List of goal dictionaries with keys:
            - goal_name (str): Name of the learning goal
            - target_level (str): Target skill level
            - priority (int): Priority 1-5 (optional, default 3)
            - timeline_months (int): Timeline in months (optional, default 6)
        preferred_learning_style: Learning style preference
            ('video', 'reading', 'hands-on', 'interactive', 'mixed')
        time_commitment_hours_per_week: Hours available per week
        budget_usd: Monthly budget in USD (optional)
        interactive: If True, prompt for missing information interactively
    
    Returns:
        UserProfile: Validated and structured user profile
    
    Example usage:
        # Using dictionaries
        profile = get_user_profile(
            name="John Doe",
            email="john@example.com",
            current_skills_input=[
                {"skill_name": "Python", "level": "INTERMEDIATE", "years_experience": 2.5, "confidence_score": 7},
                {"skill_name": "SQL", "level": "BEGINNER", "years_experience": 0.5, "confidence_score": 4}
            ],
            learning_goals_input=[
                {"goal_name": "Machine Learning", "target_level": "ADVANCED", "priority": 1, "timeline_months": 8},
                {"goal_name": "Data Analysis", "target_level": "INTERMEDIATE", "priority": 2, "timeline_months": 4}
            ],
            preferred_learning_style="hands-on",
            time_commitment_hours_per_week=12,
            budget_usd=300.0
        )
        
        # Using pandas DataFrame
        skills_df = pd.DataFrame([
            {"skill_name": "Python", "level": "INTERMEDIATE", "confidence_score": 7},
            {"skill_name": "JavaScript", "level": "BEGINNER", "confidence_score": 5}
        ])
        profile = get_user_profile_from_dataframe(
            name="Jane Smith",
            email="jane@example.com", 
            current_skills_df=skills_df,
            # ... other parameters
        )
    """
    
    # Handle interactive mode
    if interactive:
        return _get_user_profile_interactive()
    
    # Validate required inputs
    if not name or not email:
        raise ValueError("Name and email are required")
    
    if not current_skills_input or not learning_goals_input:
        raise ValueError("Current skills and learning goals are required")
    
    # Process current skills
    current_skills = []
    for skill_data in current_skills_input:
        try:
            skill_name = skill_data.get("skill_name", "").strip()
            level_str = skill_data.get("level", "BEGINNER").upper()
            years_exp = skill_data.get("years_experience", 1.0)
            confidence = skill_data.get("confidence_score", 5)
            
            if not skill_name:
                raise ValueError("Skill name cannot be empty")
            
            # Validate skill level
            if level_str not in [level.name for level in SkillLevel]:
                raise ValueError(f"Invalid skill level: {level_str}. Must be one of: {[l.name for l in SkillLevel]}")
            
            # Validate confidence score
            if not isinstance(confidence, (int, float)) or not 1 <= confidence <= 10:
                raise ValueError(f"Confidence score must be between 1 and 10, got: {confidence}")
            
            # Validate years of experience
            if not isinstance(years_exp, (int, float)) or years_exp < 0:
                raise ValueError(f"Years of experience must be non-negative, got: {years_exp}")
            
            skill = UserSkill(
                skill_name=skill_name,
                level=SkillLevel[level_str],
                years_experience=float(years_exp),
                confidence_score=int(confidence)
            )
            current_skills.append(skill)
            
        except Exception as e:
            raise ValueError(f"Error processing skill '{skill_data}': {str(e)}")
    
    # Process learning goals
    learning_goals = []
    for goal_data in learning_goals_input:
        try:
            goal_name = goal_data.get("goal_name", "").strip()
            target_level_str = goal_data.get("target_level", "INTERMEDIATE").upper()
            priority = goal_data.get("priority", 3)
            timeline = goal_data.get("timeline_months", 6)
            
            if not goal_name:
                raise ValueError("Goal name cannot be empty")
            
            # Validate target level
            if target_level_str not in [level.name for level in SkillLevel]:
                raise ValueError(f"Invalid target level: {target_level_str}")
            
            # Validate priority
            if not isinstance(priority, int) or not 1 <= priority <= 5:
                raise ValueError(f"Priority must be between 1 and 5, got: {priority}")
            
            # Validate timeline
            if not isinstance(timeline, int) or not 1 <= timeline <= 60:
                raise ValueError(f"Timeline must be between 1 and 60 months, got: {timeline}")
            
            goal = LearningGoal(
                goal_name=goal_name,
                target_skill_level=SkillLevel[target_level_str],
                priority=priority,
                timeline_months=timeline
            )
            learning_goals.append(goal)
            
        except Exception as e:
            raise ValueError(f"Error processing goal '{goal_data}': {str(e)}")
    
    # Validate learning style
    valid_styles = ["video", "reading", "hands-on", "interactive", "mixed", "visual and hands-on", "project-based"]
    if preferred_learning_style and preferred_learning_style.lower() not in [s.lower() for s in valid_styles]:
        raise ValueError(f"Invalid learning style. Must be one of: {valid_styles}")
    
    # Validate time commitment
    if time_commitment_hours_per_week is None or time_commitment_hours_per_week <= 0:
        raise ValueError("Time commitment must be a positive number")
    
    # Validate budget (optional)
    if budget_usd is not None and budget_usd < 0:
        raise ValueError("Budget must be non-negative")
    
    # Create user profile
    profile = UserProfile(
        name=name.strip(),
        email=email.strip().lower(),
        current_skills=current_skills,
        learning_goals=learning_goals,
        preferred_learning_style=preferred_learning_style or "mixed",
        time_commitment_hours_per_week=time_commitment_hours_per_week,
        budget_usd=budget_usd
    )
    
    # Final validation using existing validator
    input_handler = UserInputHandler()
    is_valid, errors = input_handler.validate_profile(profile)
    
    if not is_valid:
        raise ValueError(f"Profile validation failed: {'; '.join(errors)}")
    
    return profile

def get_user_profile_from_dataframe(
    name: str,
    email: str,
    current_skills_df: pd.DataFrame = None,
    learning_goals_df: pd.DataFrame = None,
    preferred_learning_style: str = None,
    time_commitment_hours_per_week: int = None,
    budget_usd: float = None
) -> UserProfile:
    """
    Create a user profile from pandas DataFrames.
    
    Args:
        name: User's full name
        email: User's email address
        current_skills_df: DataFrame with columns:
            - skill_name (str): Name of the skill
            - level (str): Skill level
            - years_experience (float, optional): Years of experience
            - confidence_score (int, optional): Confidence level 1-10
        learning_goals_df: DataFrame with columns:
            - goal_name (str): Name of the learning goal
            - target_level (str): Target skill level
            - priority (int, optional): Priority 1-5
            - timeline_months (int, optional): Timeline in months
        preferred_learning_style: Learning style preference
        time_commitment_hours_per_week: Hours available per week
        budget_usd: Monthly budget in USD (optional)
    
    Returns:
        UserProfile: Validated and structured user profile
    
    Example:
        skills_df = pd.DataFrame([
            {"skill_name": "Python", "level": "INTERMEDIATE", "confidence_score": 8},
            {"skill_name": "SQL", "level": "BEGINNER", "confidence_score": 5}
        ])
        
        goals_df = pd.DataFrame([
            {"goal_name": "Machine Learning", "target_level": "ADVANCED", "priority": 1},
            {"goal_name": "Data Visualization", "target_level": "INTERMEDIATE", "priority": 2}
        ])
        
        profile = get_user_profile_from_dataframe(
            name="Data Scientist",
            email="scientist@example.com",
            current_skills_df=skills_df,
            learning_goals_df=goals_df,
            preferred_learning_style="hands-on",
            time_commitment_hours_per_week=15,
            budget_usd=400.0
        )
    """
    
    # Convert DataFrames to dictionaries
    current_skills_input = None
    if current_skills_df is not None:
        # Fill missing values with defaults
        skills_df = current_skills_df.copy()
        if 'years_experience' not in skills_df.columns:
            skills_df['years_experience'] = 1.0
        if 'confidence_score' not in skills_df.columns:
            skills_df['confidence_score'] = 5
        
        skills_df['years_experience'] = skills_df['years_experience'].fillna(1.0)
        skills_df['confidence_score'] = skills_df['confidence_score'].fillna(5)
        
        current_skills_input = skills_df.to_dict('records')
    
    learning_goals_input = None
    if learning_goals_df is not None:
        # Fill missing values with defaults
        goals_df = learning_goals_df.copy()
        if 'priority' not in goals_df.columns:
            goals_df['priority'] = 3
        if 'timeline_months' not in goals_df.columns:
            goals_df['timeline_months'] = 6
        
        goals_df['priority'] = goals_df['priority'].fillna(3)
        goals_df['timeline_months'] = goals_df['timeline_months'].fillna(6)
        
        learning_goals_input = goals_df.to_dict('records')
    
    return get_user_profile(
        name=name,
        email=email,
        current_skills_input=current_skills_input,
        learning_goals_input=learning_goals_input,
        preferred_learning_style=preferred_learning_style,
        time_commitment_hours_per_week=time_commitment_hours_per_week,
        budget_usd=budget_usd
    )

def _get_user_profile_interactive() -> UserProfile:
    """
    Interactive function to collect user profile information via console input.
    
    Returns:
        UserProfile: Validated user profile from interactive input
    """
    print("🎓 AI Learning Path Generator - Profile Setup")
    print("=" * 50)
    
    # Collect basic information
    print("\n📝 Personal Information")
    name = input("Enter your full name: ").strip()
    email = input("Enter your email address: ").strip()
    
    # Collect time commitment
    while True:
        try:
            hours = int(input("Hours per week available for learning (1-40): "))
            if 1 <= hours <= 40:
                break
            else:
                print("❌ Please enter a number between 1 and 40")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Collect budget
    while True:
        try:
            budget_input = input("Monthly learning budget in USD (press Enter for no budget limit): ").strip()
            if not budget_input:
                budget = None
                break
            budget = float(budget_input)
            if budget >= 0:
                break
            else:
                print("❌ Budget must be non-negative")
        except ValueError:
            print("❌ Please enter a valid number or press Enter for no limit")
    
    # Collect learning style
    print("\n🎨 Learning Style Preferences:")
    styles = ["video", "reading", "hands-on", "interactive", "mixed"]
    for i, style in enumerate(styles, 1):
        print(f"  {i}. {style.title()}")
    
    while True:
        try:
            choice = int(input("Select your preferred learning style (1-5): "))
            if 1 <= choice <= len(styles):
                learning_style = styles[choice - 1]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(styles)}")
        except ValueError:
            print("❌ Please enter a valid number")
    
    # Collect current skills
    print(f"\n🛠️ Current Skills")
    print("Enter your current skills. For each skill, provide:")
    print("Format: skill_name,level,years_experience,confidence_score")
    print("Levels: BEGINNER, INTERMEDIATE, ADVANCED, EXPERT")
    print("Confidence: 1-10 scale")
    print("Example: Python,INTERMEDIATE,2.5,7")
    print("Type 'done' when finished")
    
    current_skills_input = []
    while True:
        skill_input = input("Skill: ").strip()
        if skill_input.lower() == 'done':
            break
        
        try:
            parts = skill_input.split(',')
            if len(parts) < 2:
                print("❌ Please provide at least skill name and level")
                continue
            
            skill_name = parts[0].strip()
            level = parts[1].strip().upper()
            years_exp = float(parts[2]) if len(parts) > 2 and parts[2].strip() else 1.0
            confidence = int(parts[3]) if len(parts) > 3 and parts[3].strip() else 5
            
            current_skills_input.append({
                "skill_name": skill_name,
                "level": level,
                "years_experience": years_exp,
                "confidence_score": confidence
            })
            print(f"✅ Added {skill_name} ({level})")
            
        except (ValueError, IndexError) as e:
            print(f"❌ Invalid format: {e}")
            print("Please use: skill_name,level[,years_experience,confidence_score]")
    
    if not current_skills_input:
        print("❌ At least one skill is required")
        return _get_user_profile_interactive()  # Retry
    
    # Collect learning goals
    print(f"\n🎯 Learning Goals")
    print("Enter your learning goals. For each goal, provide:")
    print("Format: goal_name,target_level,priority,timeline_months")
    print("Priority: 1-5 (1=highest priority)")
    print("Timeline: months to achieve the goal")
    print("Example: Machine Learning,ADVANCED,1,8")
    print("Type 'done' when finished")
    
    learning_goals_input = []
    while True:
        goal_input = input("Goal: ").strip()
        if goal_input.lower() == 'done':
            break
        
        try:
            parts = goal_input.split(',')
            if len(parts) < 2:
                print("❌ Please provide at least goal name and target level")
                continue
            
            goal_name = parts[0].strip()
            target_level = parts[1].strip().upper()
            priority = int(parts[2]) if len(parts) > 2 and parts[2].strip() else 3
            timeline = int(parts[3]) if len(parts) > 3 and parts[3].strip() else 6
            
            learning_goals_input.append({
                "goal_name": goal_name,
                "target_level": target_level,
                "priority": priority,
                "timeline_months": timeline
            })
            print(f"✅ Added goal: {goal_name} ({target_level})")
            
        except (ValueError, IndexError) as e:
            print(f"❌ Invalid format: {e}")
            print("Please use: goal_name,target_level[,priority,timeline_months]")
    
    if not learning_goals_input:
        print("❌ At least one learning goal is required")
        return _get_user_profile_interactive()  # Retry
    
    # Create and return profile
    try:
        profile = get_user_profile(
            name=name,
            email=email,
            current_skills_input=current_skills_input,
            learning_goals_input=learning_goals_input,
            preferred_learning_style=learning_style,
            time_commitment_hours_per_week=hours,
            budget_usd=budget
        )
        
        print("\n✅ Profile created successfully!")
        return profile
        
    except ValueError as e:
        print(f"\n❌ Profile creation failed: {e}")
        print("Please try again with valid inputs.")
        return _get_user_profile_interactive()  # Retry 