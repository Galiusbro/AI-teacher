#!/usr/bin/env python3
"""
Demo script for AI lesson generation.
Shows how to use AI generation without running the full API server.
"""

import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Try to import AI generator functions
try:
    from ai_generator import generate_ai_concept_lesson, generate_ai_guided_lesson
    AI_AVAILABLE = True
except ValueError:
    # GROQ_API_KEY not set
    AI_AVAILABLE = False
except ImportError:
    AI_AVAILABLE = False

from validation import validate_lesson_json


def demo_module_data():
    """Example module data for demonstration."""
    return {
        'code': 'module_demo_science_primary',
        'title': 'Изучение природы для малышей',
        'subject': 'Science',
        'stage': 'stage_primary',
        'objectives_jsonb': json.dumps([
            {"code": "SCI.NAT.P.1", "description": "Распознавать растения и животных", "bloom": "remember"},
            {"code": "SCI.NAT.P.2", "description": "Понимать основные части растений", "bloom": "understand"},
            {"code": "SCI.NAT.P.3", "description": "Наблюдать за природой и делать простые выводы", "bloom": "apply"}
        ]),
        'lesson_policy_jsonb': json.dumps({
            "default_lesson_minutes": 25,
            "min_lessons": 4,
            "max_lessons": 6,
            "mix": {"concept": 0.4, "guided": 0.4, "independent": 0.2}
        }),
        'assessment_blueprint_jsonb': json.dumps({
            "formative": ["observation_tasks", "simple_quiz"],
            "summative": ["nature_walk", "drawing_task"],
            "required_artifacts": ["photo", "drawing"]
        })
    }


def demo_ai_generation():
    """Demonstrate AI lesson generation."""
    print("🤖 Ayaal Teacher AI Generation Demo")
    print("=" * 50)
    print()

    # Check if AI is available
    if not AI_AVAILABLE:
        print("❌ AI generation not available")
        if not os.environ.get("GROQ_API_KEY"):
            print("Reason: GROQ_API_KEY not found in environment variables")
            print("Please set it with: export GROQ_API_KEY='your_key_here'")
            print()
            print("Getting a key from Groq:")
            print("1. Go to https://console.groq.com/")
            print("2. Create account")
            print("3. Generate API key")
            print("4. Set environment variable")
        else:
            print("Reason: groq package not installed or other import error")
        print()
        print("📚 For now, let's show what AI generation would produce:")
        show_ai_generation_example()
        return

    module_data = demo_module_data()

    print("📚 Module Information:")
    print(f"   Title: {module_data['title']}")
    print(f"   Subject: {module_data['subject']}")
    print(f"   Code: {module_data['code']}")
    print()

    # Generate concept lesson
    print("🎯 Generating Concept Lesson...")
    print("-" * 30)

    try:
        concept_lesson = generate_ai_concept_lesson(module_data, 'ru')

        # Validate the generated lesson
        is_valid, message = validate_lesson_json(concept_lesson)

        print(f"✅ Lesson generated successfully!")
        print(f"📝 Title: {concept_lesson['title']}")
        print(f"🔍 Validation: {'✅ Passed' if is_valid else f'❌ Failed: {message}'}")
        print(f"📚 Blocks: {len(concept_lesson.get('blocks', []))}")
        print()

        # Show lesson structure
        print("📖 Lesson Structure:")
        for i, block in enumerate(concept_lesson.get('blocks', []), 1):
            print(f"   {i}. {block['type'].upper()}: {block['content'].get('title', 'No title')}")

        print()
        print("📄 Full Lesson JSON:")
        print(json.dumps(concept_lesson, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ Error generating concept lesson: {e}")
        print("This might be due to:")
        print("- Invalid GROQ_API_KEY")
        print("- Network issues")
        print("- API rate limits")
        print("- Model unavailability")

    print()
    print("=" * 50)
    print("🎉 Demo completed!")


def show_ai_generation_example():
    """Show an example of what AI generation would produce."""
    example_lesson = {
        "id": "lesson_module_demo_science_primary_concept_01",
        "type": "concept",
        "title": "Знакомство с природой",
        "locale": "ru",
        "_generated_with": "ai_example",
        "blocks": [
            {
                "type": "theory",
                "content": {
                    "title": "Что такое природа?",
                    "text": "Природа - это весь живой мир вокруг нас: растения, животные, земля, вода и воздух. Давайте узнаем, как растения растут и что им нужно для жизни."
                }
            },
            {
                "type": "example",
                "content": {
                    "title": "Пример растения",
                    "text": "Посмотрите на цветок в горшке. У него есть корни, стебель, листья и цветы. Корни впитывают воду из земли, листья ловят солнечный свет."
                }
            },
            {
                "type": "interactive",
                "content": {
                    "type": "mcq",
                    "question": "Что нужно растению, чтобы жить?",
                    "options": ["Только вода", "Вода и солнце", "Вода, солнце и земля", "Только солнце"],
                    "correct": 2,
                    "explanation": "Растению нужна вода для питья, солнце для энергии и земля для опоры корней."
                }
            }
        ]
    }

    print("🎯 Example AI-Generated Concept Lesson:")
    print("-" * 40)
    print(f"📝 Title: {example_lesson['title']}")
    print(f"📚 Blocks: {len(example_lesson['blocks'])}")
    print()

    print("📖 Lesson Structure:")
    for i, block in enumerate(example_lesson['blocks'], 1):
        print(f"   {i}. {block['type'].upper()}: {block['content'].get('title', 'No title')}")

    print()
    print("💡 Key AI Generation Features:")
    print("   ✨ Natural, conversational language")
    print("   ✨ Personalized content based on module objectives")
    print("   ✨ Age-appropriate examples and activities")
    print("   ✨ Interactive elements with explanations")
    print("   ✨ Culturally relevant content")
    print()

    # Validate the example
    is_valid, message = validate_lesson_json(example_lesson)
    print(f"🔍 Validation: {'✅ Passed' if is_valid else f'❌ Failed: {message}'}")
    print()

    print("🚀 To try real AI generation:")
    print("1. Get GROQ API key from https://console.groq.com/")
    print("2. Set environment variable: export GROQ_API_KEY='your_key'")
    print("3. Run this demo again")
    print()


def compare_template_vs_ai():
    """Compare template vs AI generation quality."""
    print("🔄 Comparing Template vs AI Generation")
    print("=" * 50)
    print()

    module_data = demo_module_data()

    # This would require having both template and AI generators
    # For now, just show the concept
    print("📋 Comparison Matrix:")
    print("Feature              | Template Generation | AI Generation")
    print("---------------------|---------------------|--------------")
    print("Content Variety      | 🔶 Fixed templates   | ✅ Dynamic")
    print("Personalization      | 🔶 Limited          | ✅ High")
    print("Language Quality     | 🔶 Template-based   | ✅ Natural")
    print("Adaptability         | 🔶 Static           | ✅ Flexible")
    print("Maintenance          | 🔶 Manual updates   | ✅ Auto")
    print("Cost                 | ✅ Free             | ⚠️ API calls")
    print("Speed                | ✅ Instant          | 🔶 API delay")
    print("Reliability          | ✅ 100%             | ⚠️ API dependent")
    print()

    print("🎯 Best Use Cases:")
    print("Template Generation:")
    print("- Well-established curriculum")
    print("- Consistent quality requirements")
    print("- Offline functionality")
    print("- Cost-sensitive environments")
    print()
    print("AI Generation:")
    print("- New content creation")
    print("- Personalized learning")
    print("- Experimental modules")
    print("- Content scaling")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--compare":
        compare_template_vs_ai()
    else:
        demo_ai_generation()
