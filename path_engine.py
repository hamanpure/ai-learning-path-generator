"""
Learning Path Engine
Core logic for generating personalized AI learning paths based on user profiles and goals.

This module implements intelligent learning path generation using predefined skill trees,
resource matching algorithms, and comprehensive analytics.
"""

import pandas as pd
import numpy as np
import logging
import requests
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import json
from user_profile import UserProfile, UserSkill, LearningGoal, SkillLevel, SkillMapper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResourceType(Enum):
    """Types of learning resources available"""
    COURSE = "course"
    BOOK = "book"
    TUTORIAL = "tutorial"
    PROJECT = "project"
    CERTIFICATION = "certification"
    DOCUMENTATION = "documentation"
    VIDEO = "video"
    ARTICLE = "article"
    INTERACTIVE = "interactive"

class Difficulty(Enum):
    """Difficulty levels for learning resources"""
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

@dataclass
class LearningResource:
    """Represents a learning resource in the knowledge base"""
    id: str
    title: str
    description: str
    resource_type: ResourceType
    difficulty: Difficulty
    estimated_hours: int
    skills_taught: List[str]
    prerequisites: List[str]
    cost_usd: float
    rating: float
    url: Optional[str] = None
    provider: Optional[str] = None
    tags: Optional[List[str]] = None

@dataclass
class LearningStep:
    """Represents a single step in a learning path"""
    step_number: int
    resource: LearningResource
    estimated_completion_weeks: int
    priority_score: float
    readiness_score: float
    module_name: str
    prerequisites_met: bool = True

@dataclass
class LearningModule:
    """Represents a learning module containing multiple steps"""
    module_id: str
    module_name: str
    description: str
    skills_taught: List[str]
    prerequisites: List[str]
    estimated_hours: int
    steps: List[LearningStep]
    difficulty: Difficulty

@dataclass
class LearningPath:
    """Complete learning path for achieving specific goals"""
    path_id: str
    user_id: str
    goal_skill: str
    target_level: SkillLevel
    modules: List[LearningModule]
    total_estimated_hours: int
    total_cost_usd: float
    estimated_completion_months: int
    confidence_score: float
    skill_tree_path: List[str]

class SkillTree:
    """Defines skill progression trees and dependencies"""
    
    def __init__(self):
        self.skill_trees = {
            "Data Science": {
                "Python Fundamentals": {
                    "skills": ["Python", "Programming Basics"],
                    "prerequisites": [],
                    "next": ["Data Analysis Basics", "Statistics Fundamentals"]
                },
                "Statistics Fundamentals": {
                    "skills": ["Statistics", "Probability"],
                    "prerequisites": [],
                    "next": ["Data Analysis Basics"]
                },
                "Data Analysis Basics": {
                    "skills": ["Data Analysis", "Pandas", "NumPy"],
                    "prerequisites": ["Python Fundamentals"],
                    "next": ["Data Visualization", "Machine Learning Basics"]
                },
                "Data Visualization": {
                    "skills": ["Data Visualization", "Matplotlib", "Seaborn"],
                    "prerequisites": ["Data Analysis Basics"],
                    "next": ["Machine Learning Basics", "Advanced Analytics"]
                },
                "Machine Learning Basics": {
                    "skills": ["Machine Learning", "Scikit-learn"],
                    "prerequisites": ["Data Analysis Basics", "Statistics Fundamentals"],
                    "next": ["Deep Learning", "MLOps", "Advanced ML"]
                },
                "Deep Learning": {
                    "skills": ["Deep Learning", "Neural Networks", "TensorFlow", "PyTorch"],
                    "prerequisites": ["Machine Learning Basics"],
                    "next": ["Computer Vision", "NLP", "ML Engineering"]
                },
                "MLOps": {
                    "skills": ["MLOps", "Model Deployment", "Docker", "Cloud Platforms"],
                    "prerequisites": ["Machine Learning Basics"],
                    "next": ["ML Engineering", "Production ML"]
                }
            },
            "Web Development": {
                "HTML/CSS Fundamentals": {
                    "skills": ["HTML", "CSS", "Web Design"],
                    "prerequisites": [],
                    "next": ["JavaScript Basics", "Responsive Design"]
                },
                "JavaScript Basics": {
                    "skills": ["JavaScript", "DOM Manipulation"],
                    "prerequisites": ["HTML/CSS Fundamentals"],
                    "next": ["Frontend Frameworks", "Backend Development"]
                },
                "Frontend Frameworks": {
                    "skills": ["React", "Vue.js", "Angular"],
                    "prerequisites": ["JavaScript Basics"],
                    "next": ["Full Stack Development", "Advanced Frontend"]
                },
                "Backend Development": {
                    "skills": ["Node.js", "Python Flask", "APIs"],
                    "prerequisites": ["JavaScript Basics"],
                    "next": ["Database Design", "Full Stack Development"]
                },
                "Database Design": {
                    "skills": ["SQL", "Database Design", "MongoDB"],
                    "prerequisites": ["Backend Development"],
                    "next": ["Full Stack Development", "DevOps"]
                },
                "Full Stack Development": {
                    "skills": ["Full Stack", "System Architecture"],
                    "prerequisites": ["Frontend Frameworks", "Backend Development", "Database Design"],
                    "next": ["DevOps", "Microservices"]
                },
                "DevOps": {
                    "skills": ["DevOps", "CI/CD", "Docker", "Kubernetes"],
                    "prerequisites": ["Full Stack Development"],
                    "next": ["Cloud Architecture", "Site Reliability"]
                }
            },
            "Cloud Computing": {
                "Cloud Basics": {
                    "skills": ["Cloud Computing", "AWS Basics", "Azure Basics"],
                    "prerequisites": [],
                    "next": ["Infrastructure as Code", "Cloud Security"]
                },
                "Infrastructure as Code": {
                    "skills": ["Terraform", "CloudFormation", "Infrastructure"],
                    "prerequisites": ["Cloud Basics"],
                    "next": ["Container Orchestration", "Cloud Architecture"]
                },
                "Container Orchestration": {
                    "skills": ["Docker", "Kubernetes", "Container Management"],
                    "prerequisites": ["Cloud Basics"],
                    "next": ["Microservices", "Service Mesh"]
                },
                "Cloud Security": {
                    "skills": ["Cloud Security", "IAM", "Security Best Practices"],
                    "prerequisites": ["Cloud Basics"],
                    "next": ["Advanced Security", "Compliance"]
                }
            }
        }
    
    def get_learning_path_for_goal(self, goal_skill: str, current_skills: List[str]) -> List[str]:
        """
        Generate a learning path based on skill trees.
        
        Args:
            goal_skill: Target skill to achieve
            current_skills: List of current user skills
            
        Returns:
            List of module names in recommended order
        """
        try:
            # Find which tree contains the goal skill
            target_tree = None
            target_module = None
            
            for tree_name, modules in self.skill_trees.items():
                for module_name, module_info in modules.items():
                    if goal_skill in module_info["skills"]:
                        target_tree = tree_name
                        target_module = module_name
                        break
                if target_tree:
                    break
            
            if not target_tree:
                logger.warning(f"No skill tree found for goal: {goal_skill}")
                return [f"Custom Learning Path for {goal_skill}"]
            
            # Build path using BFS to find optimal route
            path = self._build_path_to_module(target_tree, target_module, current_skills)
            logger.info(f"Generated path for {goal_skill}: {path}")
            return path
            
        except Exception as e:
            logger.error(f"Error generating learning path for {goal_skill}: {str(e)}")
            return [f"Basic {goal_skill} Learning"]
    
    def _build_path_to_module(self, tree_name: str, target_module: str, current_skills: List[str]) -> List[str]:
        """Build learning path using dependency analysis"""
        try:
            tree = self.skill_trees[tree_name]
            visited = set()
            path = []
            
            def add_prerequisites(module_name: str):
                if module_name in visited or module_name not in tree:
                    return
                
                visited.add(module_name)
                module_info = tree[module_name]
                
                # Check if user already has required skills
                has_skills = any(skill in current_skills for skill in module_info["skills"])
                if has_skills:
                    return
                
                # Add prerequisites first
                for prereq in module_info.get("prerequisites", []):
                    add_prerequisites(prereq)
                
                # Add current module
                if module_name not in path:
                    path.append(module_name)
            
            add_prerequisites(target_module)
            return path if path else [target_module]
            
        except Exception as e:
            logger.error(f"Error building path to {target_module}: {str(e)}")
            return [target_module]

class ResourceFetcher:
    """Fetches and manages learning resources from various sources"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key
        self.cache = {}
    
    def fetch_resources(self, topic: str, difficulty: str = "intermediate", 
                       resource_type: str = "mixed") -> List[Dict[str, Any]]:
        """
        Fetch top learning resources for a given topic.
        
        Args:
            topic: Learning topic/skill
            difficulty: Difficulty level (beginner, intermediate, advanced)
            resource_type: Type of resource preferred
            
        Returns:
            List of resource dictionaries with links, descriptions, and metadata
        """
        try:
            cache_key = f"{topic}_{difficulty}_{resource_type}"
            if cache_key in self.cache:
                logger.info(f"Returning cached resources for {topic}")
                return self.cache[cache_key]
            
            # Try multiple resource fetching methods
            resources = []
            
            # Method 1: Use predefined curated resources
            curated = self._get_curated_resources(topic, difficulty)
            resources.extend(curated)
            
            # Method 2: Use web scraping/API if available
            if len(resources) < 3:
                scraped = self._scrape_resources(topic, difficulty)
                resources.extend(scraped)
            
            # Method 3: Use OpenAI if API key is available
            if len(resources) < 3 and self.openai_api_key:
                ai_generated = self._get_ai_resources(topic, difficulty)
                resources.extend(ai_generated)
            
            # Filter and rank resources
            resources = self._rank_and_filter_resources(resources, topic)[:3]
            
            # Cache results
            self.cache[cache_key] = resources
            logger.info(f"Fetched {len(resources)} resources for {topic}")
            return resources
            
        except Exception as e:
            logger.error(f"Error fetching resources for {topic}: {str(e)}")
            return self._get_fallback_resources(topic)
    
    def _get_curated_resources(self, topic: str, difficulty: str) -> List[Dict[str, Any]]:
        """Get curated resources from predefined database"""
        curated_db = {
            "Python": [
                {
                    "title": "Python for Everybody Specialization",
                    "description": "Complete Python programming course from University of Michigan",
                    "url": "https://www.coursera.org/specializations/python",
                    "provider": "Coursera",
                    "type": "course",
                    "difficulty": "beginner",
                    "rating": 4.8,
                    "estimated_hours": 60
                },
                {
                    "title": "Automate the Boring Stuff with Python",
                    "description": "Practical Python programming for total beginners",
                    "url": "https://automatetheboringstuff.com/",
                    "provider": "Free Book",
                    "type": "book",
                    "difficulty": "beginner",
                    "rating": 4.7,
                    "estimated_hours": 40
                }
            ],
            "Machine Learning": [
                {
                    "title": "Machine Learning Course by Andrew Ng",
                    "description": "Comprehensive introduction to machine learning",
                    "url": "https://www.coursera.org/learn/machine-learning",
                    "provider": "Coursera",
                    "type": "course",
                    "difficulty": "intermediate",
                    "rating": 4.9,
                    "estimated_hours": 60
                },
                {
                    "title": "Hands-On Machine Learning",
                    "description": "Practical machine learning with Python and Scikit-learn",
                    "url": "https://github.com/ageron/handson-ml2",
                    "provider": "GitHub",
                    "type": "tutorial",
                    "difficulty": "intermediate",
                    "rating": 4.8,
                    "estimated_hours": 80
                }
            ],
            "Data Analysis": [
                {
                    "title": "Python for Data Analysis",
                    "description": "Data wrangling with Pandas, NumPy, and IPython",
                    "url": "https://wesmckinney.com/pages/book.html",
                    "provider": "O'Reilly",
                    "type": "book",
                    "difficulty": "intermediate",
                    "rating": 4.6,
                    "estimated_hours": 50
                }
            ]
        }
        
        topic_resources = curated_db.get(topic, [])
        return [r for r in topic_resources if r["difficulty"] == difficulty or difficulty == "mixed"]
    
    def _scrape_resources(self, topic: str, difficulty: str) -> List[Dict[str, Any]]:
        """Scrape resources from educational platforms (mock implementation)"""
        # In a real implementation, this would scrape from educational platforms
        # For now, return mock data
        mock_resources = [
            {
                "title": f"Complete {topic} Tutorial",
                "description": f"Comprehensive {topic} learning resource",
                "url": f"https://example.com/{topic.lower().replace(' ', '-')}",
                "provider": "Educational Platform",
                "type": "tutorial",
                "difficulty": difficulty,
                "rating": 4.5,
                "estimated_hours": 30
            }
        ]
        return mock_resources
    
    def _get_ai_resources(self, topic: str, difficulty: str) -> List[Dict[str, Any]]:
        """Use OpenAI to generate resource recommendations (mock implementation)"""
        # In a real implementation, this would call OpenAI API
        # For now, return mock AI-generated resources
        ai_resources = [
            {
                "title": f"AI-Recommended {topic} Course",
                "description": f"AI-curated learning path for {topic}",
                "url": f"https://ai-learning.com/{topic.lower()}",
                "provider": "AI Learning Platform",
                "type": "course",
                "difficulty": difficulty,
                "rating": 4.4,
                "estimated_hours": 25
            }
        ]
        return ai_resources
    
    def _rank_and_filter_resources(self, resources: List[Dict[str, Any]], topic: str) -> List[Dict[str, Any]]:
        """Rank and filter resources based on quality metrics"""
        # Remove duplicates
        seen_urls = set()
        unique_resources = []
        for resource in resources:
            if resource.get("url") not in seen_urls:
                seen_urls.add(resource.get("url"))
                unique_resources.append(resource)
        
        # Sort by rating and relevance
        scored_resources = []
        for resource in unique_resources:
            score = resource.get("rating", 0) * 0.7
            if topic.lower() in resource.get("title", "").lower():
                score += 1.0
            if topic.lower() in resource.get("description", "").lower():
                score += 0.5
            scored_resources.append((score, resource))
        
        # Sort by score descending
        scored_resources.sort(key=lambda x: x[0], reverse=True)
        return [resource for score, resource in scored_resources]
    
    def _get_fallback_resources(self, topic: str) -> List[Dict[str, Any]]:
        """Provide fallback resources when other methods fail"""
        return [
            {
                "title": f"Learn {topic} - Getting Started",
                "description": f"Basic introduction to {topic}",
                "url": f"https://www.google.com/search?q=learn+{topic.replace(' ', '+')}",
                "provider": "Web Search",
                "type": "mixed",
                "difficulty": "beginner",
                "rating": 4.0,
                "estimated_hours": 20
            },
            {
                "title": f"{topic} Documentation",
                "description": f"Official documentation and guides for {topic}",
                "url": f"https://docs.python.org/3/",
                "provider": "Official Docs",
                "type": "documentation",
                "difficulty": "intermediate",
                "rating": 4.2,
                "estimated_hours": 15
            }
        ]

class PathEngine:
    """Main engine for generating personalized learning paths"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.skill_mapper = SkillMapper()
        self.skill_tree = SkillTree()
        self.resource_fetcher = ResourceFetcher(openai_api_key)
        self.resource_db = self._initialize_resource_database()
        logger.info("PathEngine initialized successfully")
    
    def generate_learning_path(self, profile: UserProfile, goal: LearningGoal) -> LearningPath:
        """
        Generate a comprehensive learning path for a specific goal.
        
        Args:
            profile: User profile containing skills and preferences
            goal: Learning goal to achieve
            
        Returns:
            Complete learning path with modules and steps
        """
        try:
            logger.info(f"Generating learning path for {goal.goal_name} (target: {goal.target_skill_level.name})")
            
            # Get current skills as strings
            current_skill_names = [skill.skill_name for skill in profile.current_skills]
            
            # Get skill tree path
            skill_path = self.skill_tree.get_learning_path_for_goal(
                goal.goal_name, current_skill_names
            )
            
            # Generate modules for each step in the path
            modules = []
            total_hours = 0
            total_cost = 0.0
            
            for i, module_name in enumerate(skill_path):
                module = self._create_learning_module(
                    module_name, goal, profile, i + 1
                )
                modules.append(module)
                total_hours += module.estimated_hours
                total_cost += sum(step.resource.cost_usd for step in module.steps)
            
            # Calculate completion time
            estimated_months = max(1, total_hours // (profile.time_commitment_hours_per_week * 4))
            
            # Calculate confidence score
            readiness_score = self.skill_mapper.calculate_readiness_score(profile, goal.goal_name)
            confidence_score = self._calculate_path_confidence(modules, readiness_score)
            
            path = LearningPath(
                path_id=f"path_{goal.goal_name}_{profile.name}_{int(time.time())}",
                user_id=profile.email,
                goal_skill=goal.goal_name,
                target_level=goal.target_skill_level,
                modules=modules,
                total_estimated_hours=total_hours,
                total_cost_usd=total_cost,
                estimated_completion_months=estimated_months,
                confidence_score=confidence_score,
                skill_tree_path=skill_path
            )
            
            logger.info(f"Generated learning path with {len(modules)} modules, {total_hours} hours")
            return path
            
        except Exception as e:
            logger.error(f"Error generating learning path: {str(e)}")
            # Return a basic fallback path
            return self._create_fallback_path(profile, goal)
    
    def _create_learning_module(self, module_name: str, goal: LearningGoal, 
                              profile: UserProfile, module_number: int) -> LearningModule:
        """Create a learning module with relevant resources"""
        try:
            # Get skills for this module from skill tree
            module_skills = self._get_module_skills(module_name)
            
            # Fetch resources for the main skill
            primary_skill = module_skills[0] if module_skills else module_name
            difficulty_map = {
                SkillLevel.BEGINNER: "beginner",
                SkillLevel.INTERMEDIATE: "intermediate", 
                SkillLevel.ADVANCED: "advanced",
                SkillLevel.EXPERT: "expert"
            }
            difficulty = difficulty_map.get(goal.target_skill_level, "intermediate")
            
            # Get resources from fetcher and database
            fetched_resources = self.resource_fetcher.fetch_resources(primary_skill, difficulty)
            db_resources = self._find_relevant_resources(primary_skill, goal.target_skill_level)
            
            # Combine and create learning steps
            all_resources = self._combine_resources(fetched_resources, db_resources)
            steps = []
            
            for i, resource_data in enumerate(all_resources[:3]):  # Limit to 3 resources per module
                if isinstance(resource_data, dict):
                    resource = self._dict_to_learning_resource(resource_data, f"{module_name}_{i}")
                else:
                    resource = resource_data
                
                estimated_weeks = max(1, resource.estimated_hours // profile.time_commitment_hours_per_week)
                readiness_score = self.skill_mapper.calculate_readiness_score(profile, primary_skill)
                
                step = LearningStep(
                    step_number=i + 1,
                    resource=resource,
                    estimated_completion_weeks=estimated_weeks,
                    priority_score=self._calculate_resource_priority(resource, profile, goal),
                    readiness_score=readiness_score,
                    module_name=module_name,
                    prerequisites_met=self._check_prerequisites_met(resource, profile)
                )
                steps.append(step)
            
            # Calculate module metrics
            module_hours = sum(step.resource.estimated_hours for step in steps)
            module_difficulty = self._determine_module_difficulty(steps)
            
            module = LearningModule(
                module_id=f"module_{module_number}_{module_name.replace(' ', '_')}",
                module_name=module_name,
                description=f"Learn {', '.join(module_skills)} through hands-on practice and projects",
                skills_taught=module_skills,
                prerequisites=self._get_module_prerequisites(module_name),
                estimated_hours=module_hours,
                steps=steps,
                difficulty=module_difficulty
            )
            
            logger.info(f"Created module '{module_name}' with {len(steps)} steps")
            return module
            
        except Exception as e:
            logger.error(f"Error creating module {module_name}: {str(e)}")
            return self._create_fallback_module(module_name, module_number)
    
    def _get_module_skills(self, module_name: str) -> List[str]:
        """Get skills taught by a specific module"""
        for tree_name, modules in self.skill_tree.skill_trees.items():
            if module_name in modules:
                return modules[module_name]["skills"]
        return [module_name]  # Fallback
    
    def _get_module_prerequisites(self, module_name: str) -> List[str]:
        """Get prerequisites for a specific module"""
        for tree_name, modules in self.skill_tree.skill_trees.items():
            if module_name in modules:
                return modules[module_name]["prerequisites"]
        return []  # Fallback
    
    def _dict_to_learning_resource(self, resource_dict: Dict[str, Any], resource_id: str) -> LearningResource:
        """Convert dictionary to LearningResource object"""
        try:
            # Map resource type
            type_mapping = {
                "course": ResourceType.COURSE,
                "book": ResourceType.BOOK,
                "tutorial": ResourceType.TUTORIAL,
                "video": ResourceType.VIDEO,
                "article": ResourceType.ARTICLE,
                "mixed": ResourceType.TUTORIAL
            }
            
            # Map difficulty
            difficulty_mapping = {
                "beginner": Difficulty.BEGINNER,
                "intermediate": Difficulty.INTERMEDIATE,
                "advanced": Difficulty.ADVANCED,
                "expert": Difficulty.EXPERT
            }
            
            resource_type = type_mapping.get(resource_dict.get("type", "tutorial"), ResourceType.TUTORIAL)
            difficulty = difficulty_mapping.get(resource_dict.get("difficulty", "intermediate"), Difficulty.INTERMEDIATE)
            
            return LearningResource(
                id=resource_id,
                title=resource_dict.get("title", "Learning Resource"),
                description=resource_dict.get("description", ""),
                resource_type=resource_type,
                difficulty=difficulty,
                estimated_hours=resource_dict.get("estimated_hours", 20),
                skills_taught=[resource_dict.get("topic", "General")],
                prerequisites=[],
                cost_usd=resource_dict.get("cost", 0.0),
                rating=resource_dict.get("rating", 4.0),
                url=resource_dict.get("url"),
                provider=resource_dict.get("provider", "Unknown")
            )
        except Exception as e:
            logger.error(f"Error converting dict to LearningResource: {str(e)}")
            return self._create_fallback_resource(resource_id)
    
    def _combine_resources(self, fetched: List[Dict], db_resources: List[LearningResource]) -> List:
        """Combine fetched and database resources"""
        combined = []
        combined.extend(fetched)
        combined.extend(db_resources)
        return combined
    
    def _determine_module_difficulty(self, steps: List[LearningStep]) -> Difficulty:
        """Determine overall module difficulty based on steps"""
        if not steps:
            return Difficulty.INTERMEDIATE
        
        difficulties = [step.resource.difficulty.value for step in steps]
        avg_difficulty = sum(difficulties) / len(difficulties)
        
        if avg_difficulty <= 1.5:
            return Difficulty.BEGINNER
        elif avg_difficulty <= 2.5:
            return Difficulty.INTERMEDIATE
        elif avg_difficulty <= 3.5:
            return Difficulty.ADVANCED
        else:
            return Difficulty.EXPERT
    
    def _create_fallback_path(self, profile: UserProfile, goal: LearningGoal) -> LearningPath:
        """Create a basic fallback learning path"""
        logger.warning("Creating fallback learning path")
        
        fallback_module = self._create_fallback_module(f"Learn {goal.goal_name}", 1)
        
        return LearningPath(
            path_id=f"fallback_{goal.goal_name}_{int(time.time())}",
            user_id=profile.email,
            goal_skill=goal.goal_name,
            target_level=goal.target_skill_level,
            modules=[fallback_module],
            total_estimated_hours=fallback_module.estimated_hours,
            total_cost_usd=0.0,
            estimated_completion_months=2,
            confidence_score=0.5,
            skill_tree_path=[goal.goal_name]
        )
    
    def _create_fallback_module(self, module_name: str, module_number: int) -> LearningModule:
        """Create a basic fallback module"""
        fallback_resource = self._create_fallback_resource(f"fallback_{module_number}")
        
        step = LearningStep(
            step_number=1,
            resource=fallback_resource,
            estimated_completion_weeks=2,
            priority_score=3.0,
            readiness_score=0.7,
            module_name=module_name
        )
        
        return LearningModule(
            module_id=f"fallback_module_{module_number}",
            module_name=module_name,
            description=f"Basic learning module for {module_name}",
            skills_taught=[module_name],
            prerequisites=[],
            estimated_hours=20,
            steps=[step],
            difficulty=Difficulty.INTERMEDIATE
        )
    
    def _create_fallback_resource(self, resource_id: str) -> LearningResource:
        """Create a basic fallback resource"""
        return LearningResource(
            id=resource_id,
            title="Basic Learning Resource",
            description="Foundational learning material",
            resource_type=ResourceType.TUTORIAL,
            difficulty=Difficulty.INTERMEDIATE,
            estimated_hours=20,
            skills_taught=["General Skills"],
            prerequisites=[],
            cost_usd=0.0,
            rating=4.0,
            provider="Generic"
        )
    
    def generate_multiple_paths(self, user_profile: UserProfile) -> List[LearningPath]:
        """Generate learning paths for all user goals"""
        try:
            paths = []
            logger.info(f"Generating {len(user_profile.learning_goals)} learning paths")
            
            for goal in user_profile.learning_goals:
                try:
                    path = self.generate_learning_path(user_profile, goal)
                    paths.append(path)
                except Exception as e:
                    logger.error(f"Error generating path for {goal.goal_name}: {str(e)}")
                    # Continue with other goals
            
            # Sort paths by priority and confidence
            paths.sort(key=lambda p: (
                -next(g.priority for g in user_profile.learning_goals if g.goal_name == p.goal_skill),
                -p.confidence_score
            ))
            
            logger.info(f"Successfully generated {len(paths)} learning paths")
            return paths
            
        except Exception as e:
            logger.error(f"Error generating multiple paths: {str(e)}")
            return []
    
    def _find_relevant_resources(self, skill: str, target_level: SkillLevel) -> List[LearningResource]:
        """Find resources relevant to learning a specific skill"""
        relevant_resources = []
        
        for resource in self.resource_db:
            # Check if resource teaches the target skill
            if skill.lower() in [s.lower() for s in resource.skills_taught]:
                # Check if difficulty is appropriate
                if resource.difficulty.value <= target_level.value + 1:  # Allow slightly higher difficulty
                    relevant_resources.append(resource)
        
        return relevant_resources
    
    def _calculate_resource_priority(self, resource: LearningResource, 
                                   user_profile: UserProfile, goal: LearningGoal) -> float:
        """Calculate priority score for a resource"""
        try:
            score = 0.0
            
            # Base score from rating
            score += resource.rating * 2
            
            # Difficulty appropriateness
            level_diff = abs(resource.difficulty.value - goal.target_skill_level.value)
            score += max(0, 5 - level_diff)
            
            # Cost efficiency
            if resource.cost_usd == 0:
                score += 3  # Bonus for free resources
            elif user_profile.budget_usd:
                cost_ratio = resource.cost_usd / user_profile.budget_usd
                score += max(0, 3 - cost_ratio * 3)
            
            # Time efficiency
            hours_per_week = user_profile.time_commitment_hours_per_week
            if resource.estimated_hours <= hours_per_week * 4:  # Completable in a month
                score += 2
            
            # Resource type preference
            type_scores = {
                ResourceType.PROJECT: 3,  # Hands-on learning
                ResourceType.COURSE: 2,
                ResourceType.TUTORIAL: 2,
                ResourceType.VIDEO: 1.5,
                ResourceType.CERTIFICATION: 1,
                ResourceType.BOOK: 1,
                ResourceType.DOCUMENTATION: 0.5
            }
            score += type_scores.get(resource.resource_type, 1)
            
            return score
            
        except Exception as e:
            logger.error(f"Error calculating resource priority: {str(e)}")
            return 3.0  # Default score
    
    def _check_prerequisites_met(self, resource: LearningResource, user_profile: UserProfile) -> bool:
        """Check if user meets resource prerequisites"""
        try:
            user_skills = {skill.skill_name.lower() for skill in user_profile.current_skills}
            
            for prereq in resource.prerequisites:
                if prereq.lower() not in user_skills:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking prerequisites: {str(e)}")
            return True  # Assume met if error
    
    def _calculate_path_confidence(self, modules: List[LearningModule], readiness_score: float) -> float:
        """Calculate confidence score for the learning path"""
        try:
            if not modules:
                return 0.0
            
            # Average resource rating across all steps
            all_steps = [step for module in modules for step in module.steps]
            if not all_steps:
                return 0.0
            
            avg_rating = sum(step.resource.rating for step in all_steps) / len(all_steps)
            rating_score = avg_rating / 5.0
            
            # Readiness contribution
            readiness_contribution = readiness_score
            
            # Path completeness (number of quality modules)
            completeness_score = min(1.0, len(modules) / 3.0)
            
            # Prerequisites coverage
            prereqs_met = sum(1 for step in all_steps if step.prerequisites_met) / len(all_steps)
            
            # Combine scores
            confidence = (
                rating_score * 0.3 + 
                readiness_contribution * 0.3 + 
                completeness_score * 0.2 + 
                prereqs_met * 0.2
            )
            
            return min(1.0, confidence)
            
        except Exception as e:
            logger.error(f"Error calculating path confidence: {str(e)}")
            return 0.5  # Default confidence
    
    def _initialize_resource_database(self) -> List[LearningResource]:
        """Initialize the learning resource database with enhanced resources"""
        resources = [
            LearningResource(
                id="ml_course_1",
                title="Machine Learning A-Z: Hands-On Python & R",
                description="Complete machine learning course with practical projects",
                resource_type=ResourceType.COURSE,
                difficulty=Difficulty.INTERMEDIATE,
                estimated_hours=40,
                skills_taught=["Machine Learning", "Python", "Data Analysis"],
                prerequisites=["Python", "Statistics"],
                cost_usd=89.99,
                rating=4.5,
                provider="Udemy",
                tags=["hands-on", "practical", "comprehensive"]
            ),
            LearningResource(
                id="python_basics",
                title="Python for Everybody Specialization",
                description="Learn Python programming fundamentals",
                resource_type=ResourceType.COURSE,
                difficulty=Difficulty.BEGINNER,
                estimated_hours=60,
                skills_taught=["Python"],
                prerequisites=[],
                cost_usd=0,
                rating=4.8,
                provider="Coursera",
                tags=["beginner-friendly", "university", "free"]
            ),
            LearningResource(
                id="data_analysis_project",
                title="Exploratory Data Analysis with Pandas",
                description="Hands-on project for data analysis skills",
                resource_type=ResourceType.PROJECT,
                difficulty=Difficulty.INTERMEDIATE,
                estimated_hours=20,
                skills_taught=["Data Analysis", "Python"],
                prerequisites=["Python"],
                cost_usd=0,
                rating=4.3,
                tags=["project-based", "pandas", "free"]
            ),
            LearningResource(
                id="deep_learning_spec",
                title="Deep Learning Specialization",
                description="Comprehensive deep learning course by Andrew Ng",
                resource_type=ResourceType.COURSE,
                difficulty=Difficulty.ADVANCED,
                estimated_hours=120,
                skills_taught=["Deep Learning", "Machine Learning", "Python"],
                prerequisites=["Machine Learning", "Python", "Statistics"],
                cost_usd=39.99,
                rating=4.9,
                provider="Coursera",
                tags=["andrew-ng", "comprehensive", "theory"]
            ),
            LearningResource(
                id="sql_tutorial",
                title="SQL Tutorial for Data Analysis",
                description="Complete SQL guide for data professionals",
                resource_type=ResourceType.TUTORIAL,
                difficulty=Difficulty.BEGINNER,
                estimated_hours=25,
                skills_taught=["SQL", "Data Analysis"],
                prerequisites=[],
                cost_usd=0,
                rating=4.4,
                tags=["sql", "databases", "free"]
            ),
            # Add more resources for web development
            LearningResource(
                id="react_course",
                title="Complete React Developer Course",
                description="Learn React from basics to advanced concepts",
                resource_type=ResourceType.COURSE,
                difficulty=Difficulty.INTERMEDIATE,
                estimated_hours=45,
                skills_taught=["React", "JavaScript", "Frontend"],
                prerequisites=["JavaScript", "HTML", "CSS"],
                cost_usd=69.99,
                rating=4.6,
                provider="Udemy",
                tags=["react", "frontend", "modern"]
            ),
            LearningResource(
                id="js_fundamentals",
                title="JavaScript: The Complete Guide",
                description="Master JavaScript from beginner to advanced",
                resource_type=ResourceType.COURSE,
                difficulty=Difficulty.BEGINNER,
                estimated_hours=50,
                skills_taught=["JavaScript", "Web Development"],
                prerequisites=["HTML", "CSS"],
                cost_usd=49.99,
                rating=4.7,
                provider="Udemy",
                tags=["javascript", "fundamentals", "comprehensive"]
            )
        ]
        
        logger.info(f"Initialized resource database with {len(resources)} resources")
        return resources
    
    def get_path_analytics(self, path: LearningPath) -> Dict[str, Any]:
        """Generate comprehensive analytics for a learning path"""
        try:
            all_steps = [step for module in path.modules for step in module.steps]
            
            analytics = {
                "total_modules": len(path.modules),
                "total_resources": len(all_steps),
                "resource_types": self._analyze_resource_types(all_steps),
                "difficulty_distribution": self._analyze_difficulty_distribution(path.modules),
                "avg_resource_rating": sum(step.resource.rating for step in all_steps) / len(all_steps) if all_steps else 0,
                "free_resources_count": sum(1 for step in all_steps if step.resource.cost_usd == 0),
                "estimated_weekly_hours": path.total_estimated_hours / (path.estimated_completion_months * 4.33),
                "skill_tree_path": path.skill_tree_path,
                "confidence_breakdown": self._analyze_confidence_factors(path),
                "cost_breakdown": self._analyze_cost_breakdown(all_steps),
                "time_breakdown": self._analyze_time_breakdown(path.modules)
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error generating path analytics: {str(e)}")
            return {}
    
    def _analyze_resource_types(self, steps: List[LearningStep]) -> Dict[str, int]:
        """Analyze distribution of resource types"""
        type_counts = {}
        for step in steps:
            resource_type = step.resource.resource_type.value
            type_counts[resource_type] = type_counts.get(resource_type, 0) + 1
        return type_counts
    
    def _analyze_difficulty_distribution(self, modules: List[LearningModule]) -> Dict[str, int]:
        """Analyze distribution of difficulty levels"""
        difficulty_counts = {}
        for module in modules:
            difficulty = module.difficulty.name
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        return difficulty_counts
    
    def _analyze_confidence_factors(self, path: LearningPath) -> Dict[str, float]:
        """Analyze factors contributing to confidence score"""
        all_steps = [step for module in path.modules for step in module.steps]
        
        if not all_steps:
            return {}
        
        return {
            "avg_readiness": sum(step.readiness_score for step in all_steps) / len(all_steps),
            "avg_priority": sum(step.priority_score for step in all_steps) / len(all_steps),
            "prerequisites_coverage": sum(1 for step in all_steps if step.prerequisites_met) / len(all_steps)
        }
    
    def _analyze_cost_breakdown(self, steps: List[LearningStep]) -> Dict[str, float]:
        """Analyze cost breakdown by resource type"""
        cost_by_type = {}
        for step in steps:
            resource_type = step.resource.resource_type.value
            cost_by_type[resource_type] = cost_by_type.get(resource_type, 0) + step.resource.cost_usd
        return cost_by_type
    
    def _analyze_time_breakdown(self, modules: List[LearningModule]) -> Dict[str, int]:
        """Analyze time breakdown by module"""
        time_by_module = {}
        for module in modules:
            time_by_module[module.module_name] = module.estimated_hours
        return time_by_module 