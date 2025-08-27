#!/usr/bin/env python3
"""
Test script for validation functionality.
"""

import requests
import json

BASE_URL = "http://localhost:3000"


def test_health():
    """Test health endpoint."""
    print("🩺 Testing /api/health...")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_database_validation():
    """Test database validation."""
    print("🗄️ Testing /api/validate/database...")
    response = requests.get(f"{BASE_URL}/api/validate/database")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_lesson_validation_valid():
    """Test lesson validation with valid data."""
    print("✅ Testing /api/validate/lesson (valid data)...")
    valid_lesson = {
        "id": "test_lesson_valid",
        "type": "concept",
        "title": "Test Lesson",
        "locale": "ru",
        "blocks": [
            {
                "type": "theory",
                "content": {"title": "Test", "text": "Test content"}
            },
            {
                "type": "interactive",
                "content": {"type": "mcq", "question": "Test?"}
            }
        ]
    }

    response = requests.post(f"{BASE_URL}/api/validate/lesson",
                           json=valid_lesson,
                           headers={'Content-Type': 'application/json'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_lesson_validation_invalid():
    """Test lesson validation with invalid data."""
    print("❌ Testing /api/validate/lesson (invalid data)...")

    # Test cases for invalid data
    invalid_cases = [
        {
            "name": "Missing required field",
            "data": {"type": "concept", "title": "Test"}
        },
        {
            "name": "Invalid lesson type",
            "data": {
                "id": "test",
                "type": "invalid_type",
                "title": "Test",
                "locale": "ru",
                "blocks": []
            }
        },
        {
            "name": "Empty blocks",
            "data": {
                "id": "test",
                "type": "concept",
                "title": "Test",
                "locale": "ru",
                "blocks": []
            }
        },
        {
            "name": "Invalid locale",
            "data": {
                "id": "test",
                "type": "concept",
                "title": "Test",
                "locale": "invalid",
                "blocks": [{"type": "theory", "content": {"text": "test"}}]
            }
        }
    ]

    for case in invalid_cases:
        print(f"  Testing: {case['name']}")
        response = requests.post(f"{BASE_URL}/api/validate/lesson",
                               json=case['data'],
                               headers={'Content-Type': 'application/json'})
        print(f"    Status: {response.status_code}")
        print(f"    Response: {response.json()}")
        print()


def test_api_validation_invalid():
    """Test API request validation."""
    print("🚫 Testing API request validation...")

    # Test invalid module code
    print("  Testing invalid module code...")
    response = requests.post(f"{BASE_URL}/api/lessons/generate",
                           json={
                               "module_code": "invalid_module",
                               "lesson_type": "concept",
                               "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5"
                           },
                           headers={'Content-Type': 'application/json'})
    print(f"    Status: {response.status_code}")
    print(f"    Response: {response.json()}")

    # Test invalid lesson type
    print("  Testing invalid lesson type...")
    response = requests.post(f"{BASE_URL}/api/lessons/generate",
                           json={
                               "module_code": "module_math_numbers_primary",
                               "lesson_type": "invalid_type",
                               "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5"
                           },
                           headers={'Content-Type': 'application/json'})
    print(f"    Status: {response.status_code}")
    print(f"    Response: {response.json()}")

    # Test invalid UUID
    print("  Testing invalid UUID...")
    response = requests.post(f"{BASE_URL}/api/lessons/generate",
                           json={
                               "module_code": "module_math_numbers_primary",
                               "lesson_type": "concept",
                               "student_id": "invalid-uuid"
                           },
                           headers={'Content-Type': 'application/json'})
    print(f"    Status: {response.status_code}")
    print(f"    Response: {response.json()}")
    print()


def test_full_workflow():
    """Test complete workflow with validation."""
    print("🔄 Testing full workflow...")

    # 1. Generate lesson
    print("  1. Generating lesson...")
    response = requests.post(f"{BASE_URL}/api/lessons/generate",
                           json={
                               "module_code": "module_math_numbers_primary",
                               "lesson_type": "concept",
                               "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
                               "locale": "ru"
                           },
                           headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        print(f"    ❌ Failed to generate lesson: {response.json()}")
        return

    lesson = response.json()
    print(f"    ✅ Lesson generated: {lesson['id']}")

    # 2. Validate generated lesson
    print("  2. Validating generated lesson...")
    response = requests.post(f"{BASE_URL}/api/validate/lesson",
                           json=lesson,
                           headers={'Content-Type': 'application/json'})

    if response.status_code != 200 or not response.json()['valid']:
        print(f"    ❌ Lesson validation failed: {response.json()}")
        return

    print("    ✅ Lesson is valid")

    # 3. Get next lesson recommendation
    print("  3. Getting next lesson...")
    response = requests.post(f"{BASE_URL}/api/next",
                           json={
                               "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
                               "module_code": "module_math_numbers_primary"
                           },
                           headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        print(f"    ❌ Failed to get next lesson: {response.json()}")
        return

    next_data = response.json()
    print(f"    ✅ Next lesson type: {next_data['next_lesson_type']}")
    print(f"    Reason: {next_data['reason']}")

    # 4. Submit answer
    print("  4. Submitting answer...")
    response = requests.post(f"{BASE_URL}/api/submissions",
                           json={
                               "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
                               "module_code": "module_math_numbers_primary",
                               "lesson_id": lesson['id'],
                               "task_id": "task_practice_1",
                               "kind": "practice",
                               "answer_jsonb": {"mcq_correct": 4, "mcq_total": 5},
                               "score": 0.8
                           },
                           headers={'Content-Type': 'application/json'})

    if response.status_code != 200:
        print(f"    ❌ Failed to submit answer: {response.json()}")
        return

    print("    ✅ Answer submitted successfully")
    print()


def main():
    """Run all validation tests."""
    print("🧪 Ayaal Teacher API Validation Tests")
    print("=" * 50)
    print()

    test_health()
    test_database_validation()
    test_lesson_validation_valid()
    test_lesson_validation_invalid()
    test_api_validation_invalid()
    test_full_workflow()

    print("=" * 50)
    print("✅ All validation tests completed!")


if __name__ == "__main__":
    main()
