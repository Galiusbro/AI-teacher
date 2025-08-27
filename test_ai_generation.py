#!/usr/bin/env python3
"""
Test script for AI lesson generation.
"""

import requests
import json
import os

BASE_URL = "http://localhost:3000"


def test_ai_lesson_generation():
    """Test AI lesson generation."""
    print("🤖 Testing AI lesson generation...")

    # Test concept lesson with AI
    print("  1. Generating concept lesson with AI...")
    response = requests.post(f"{BASE_URL}/api/lessons/generate",
                           json={
                               "module_code": "module_math_numbers_primary",
                               "lesson_type": "concept",
                               "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
                               "locale": "ru",
                               "use_ai": True
                           },
                           headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        print(f"    ❌ AI generation failed: {response.json()}")
        return

    lesson = response.json()
    print(f"    ✅ AI lesson generated: {lesson['id']}")
    print(f"    📝 Title: {lesson['title']}")
    print(f"    🎯 Generated with: {lesson.get('_generated_with', 'unknown')}")

    # Check lesson structure
    required_fields = ['id', 'type', 'title', 'locale', 'blocks']
    for field in required_fields:
        if field not in lesson:
            print(f"    ❌ Missing field: {field}")
            return

    if len(lesson['blocks']) == 0:
        print("    ❌ No blocks in lesson")
        return

    print(f"    📚 Blocks count: {len(lesson['blocks'])}")

    # Test guided lesson with AI
    print("  2. Generating guided lesson with AI...")
    response = requests.post(f"{BASE_URL}/api/lessons/generate",
                           json={
                               "module_code": "module_math_numbers_primary",
                               "lesson_type": "guided",
                               "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
                               "locale": "ru",
                               "use_ai": True
                           },
                           headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        guided_lesson = response.json()
        print(f"    ✅ Guided lesson generated: {guided_lesson['id']}")
    else:
        print(f"    ⚠️ Guided lesson generation failed: {response.json()}")

    print()


def test_template_vs_ai_comparison():
    """Compare template vs AI generation."""
    print("🔄 Comparing template vs AI generation...")

    # Template generation
    print("  1. Template generation...")
    response = requests.post(f"{BASE_URL}/api/lessons/generate",
                           json={
                               "module_code": "module_math_numbers_primary",
                               "lesson_type": "concept",
                               "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
                               "locale": "ru",
                               "use_ai": False
                           },
                           headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        template_lesson = response.json()
        print(f"    ✅ Template lesson: {template_lesson['id']}")
        print(f"    📝 Title: {template_lesson['title']}")
        print(f"    🎯 Generated with: {template_lesson.get('_generated_with', 'unknown')}")

    # AI generation (if available)
    print("  2. AI generation...")
    response = requests.post(f"{BASE_URL}/api/lessons/generate",
                           json={
                               "module_code": "module_math_numbers_primary",
                               "lesson_type": "concept",
                               "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
                               "locale": "ru",
                               "use_ai": True
                           },
                           headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        ai_lesson = response.json()
        print(f"    ✅ AI lesson: {ai_lesson['id']}")
        print(f"    📝 Title: {ai_lesson['title']}")
        print(f"    🎯 Generated with: {ai_lesson.get('_generated_with', 'unknown')}")

        # Compare block counts
        template_blocks = len(template_lesson.get('blocks', []))
        ai_blocks = len(ai_lesson.get('blocks', []))
        print(f"    📊 Template blocks: {template_blocks}, AI blocks: {ai_blocks}")

    else:
        print(f"    ⚠️ AI generation not available: {response.json()}")

    print()


def test_ai_availability():
    """Check if AI is available."""
    print("🔍 Checking AI availability...")

    # Try to generate with AI
    response = requests.post(f"{BASE_URL}/api/lessons/generate",
                           json={
                               "module_code": "module_math_numbers_primary",
                               "lesson_type": "concept",
                               "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
                               "locale": "ru",
                               "use_ai": True
                           },
                           headers={'Content-Type': 'application/json'})

    if response.status_code == 200:
        lesson = response.json()
        if lesson.get('_generated_with') == 'ai':
            print("    ✅ AI generation is available and working")
            return True
        else:
            print("    ⚠️ AI requested but template was used (AI not available)")
            return False
    else:
        error_msg = response.json().get('error', 'Unknown error')
        print(f"    ❌ AI generation failed: {error_msg}")
        return False


def main():
    """Run AI generation tests."""
    print("🧪 Ayaal Teacher AI Generation Tests")
    print("=" * 50)
    print()

    # Check AI availability first
    ai_available = test_ai_availability()
    print()

    if ai_available:
        test_ai_lesson_generation()
        test_template_vs_ai_comparison()
    else:
        print("⚠️ AI generation not available. Install groq package and set GROQ_API_KEY")
        print("💡 Continuing with template generation tests...")

    print("=" * 50)
    print("✅ AI generation tests completed!")


if __name__ == "__main__":
    main()
