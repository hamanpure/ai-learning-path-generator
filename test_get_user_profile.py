#!/usr/bin/env python3
"""
Test script for the get_user_profile() function
Demonstrates various ways to create user profiles using the new function.
"""

from user_profile import get_user_profile, get_user_profile_from_dataframe
import pandas as pd

def test_dictionary_input():
    """Test get_user_profile() with dictionary input"""
    print("=== Test 1: Dictionary Input ===")
    try:
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
        print("✅ Profile created successfully!")
        print(f"Name: {profile.name}")
        print(f"Email: {profile.email}")
        print(f"Skills: {len(profile.current_skills)} skills")
        for skill in profile.current_skills:
            print(f"  - {skill.skill_name}: {skill.level.name} (confidence: {skill.confidence_score}/10)")
        print(f"Goals: {len(profile.learning_goals)} goals")
        for goal in profile.learning_goals:
            print(f"  - {goal.goal_name}: {goal.target_skill_level.name} (priority: {goal.priority})")
        print(f"Learning Style: {profile.preferred_learning_style}")
        print(f"Hours/week: {profile.time_commitment_hours_per_week}")
        print(f"Budget: ${profile.budget_usd}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid inputs"""
    print("\n=== Test 2: Error Handling ===")
    
    try:
        # Test with invalid data
        get_user_profile(
            name="",  # Invalid: empty name
            email="invalid-email",  # Invalid: no @ symbol
            current_skills_input=[],  # Invalid: empty skills
            learning_goals_input=[],  # Invalid: empty goals
            time_commitment_hours_per_week=0  # Invalid: zero hours
        )
        print("❌ Expected error but got success")
        return False
    except ValueError as e:
        print(f"✅ Error handling works: {str(e)[:80]}...")
        return True
    except Exception as e:
        print(f"❌ Unexpected error type: {type(e).__name__}: {e}")
        return False

def main():
    """Run tests"""
    print("🧪 Testing get_user_profile() Function")
    print("=" * 50)
    
    tests = [test_dictionary_input, test_error_handling]
    passed = sum(test() for test in tests)
    total = len(tests)
    
    print(f"\n{'='*50}")
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The get_user_profile() function works correctly.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.")

if __name__ == "__main__":
    main() 