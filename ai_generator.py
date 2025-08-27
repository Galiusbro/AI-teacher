#!/usr/bin/env python3
"""
AI-powered lesson generator using Groq API.
Generates educational content based on module data and student context.
"""

import os
import json
import re
from typing import Dict, List, Any, Optional
from groq import Groq
from cache_manager import get_cached_lesson, save_lesson_to_cache


class AILessonGenerator:
    """AI-powered lesson generator using Groq."""

    def __init__(self):
        """Initialize Groq client."""
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def generate_concept_lesson(self, module_data: Dict[str, Any], student_locale: str = 'ru') -> Dict[str, Any]:
        """Generate a concept lesson using AI."""

        # Check cache first
        module_code = module_data.get('code', 'unknown')
        cached_lesson = get_cached_lesson(module_code, 'concept', student_locale)
        if cached_lesson:
            print(f"Cache hit for {module_code} concept lesson")
            return cached_lesson

        # Extract module information
        subject = module_data.get('subject', 'General')
        title = module_data.get('title', 'Unknown Module')
        objectives = module_data.get('objectives_jsonb', [])

        # Prepare objectives text
        objectives_text = ""
        if isinstance(objectives, list):
            objectives_text = "\n".join([f"- {obj.get('description', '')}" for obj in objectives])

        # Create prompt for concept lesson
        prompt = f"""
Создай урок типа "concept" на русском языке для модуля "{title}" по предмету "{subject}".

Цели обучения:
{objectives_text}

Структура урока должна включать:
1. Теоретический блок (theory) - объяснение основных понятий
2. Пример (example) - практический пример применения
3. Интерактивный элемент (interactive) - тест или упражнение

Формат ответа должен быть строго JSON:
{{
  "id": "lesson_{module_data.get('code', 'unknown')}_concept_01",
  "type": "concept",
  "title": "Краткое название урока",
  "locale": "{student_locale}",
  "blocks": [
    {{
      "type": "theory",
      "content": {{
        "title": "Название раздела",
        "text": "Подробное объяснение..."
      }}
    }},
    {{
      "type": "example",
      "content": {{
        "title": "Пример",
        "text": "Описание примера..."
      }}
    }},
    {{
      "type": "interactive",
      "content": {{
        "type": "mcq",
        "question": "Вопрос для проверки понимания?",
        "options": ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
        "correct": 2,
        "explanation": "Пояснение правильного ответа..."
      }}
    }}
  ]
}}

Сделай урок интересным, понятным и соответствующим уровню ученика.
"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=2000,
            )

            response_text = chat_completion.choices[0].message.content

            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                lesson_data = json.loads(json_match.group())
                # Save to cache
                save_lesson_to_cache(module_code, 'concept', lesson_data, student_locale)
                return lesson_data
            else:
                # Fallback to manual parsing or basic structure
                fallback_lesson = self._create_fallback_concept_lesson(module_data, student_locale)
                save_lesson_to_cache(module_code, 'concept', fallback_lesson, student_locale)
                return fallback_lesson

        except Exception as e:
            print(f"AI generation error: {e}")
            fallback_lesson = self._create_fallback_concept_lesson(module_data, student_locale)
            save_lesson_to_cache(module_code, 'concept', fallback_lesson, student_locale)
            return fallback_lesson

    def generate_guided_lesson(self, module_data: Dict[str, Any], student_locale: str = 'ru') -> Dict[str, Any]:
        """Generate a guided lesson using AI."""

        # Check cache first
        module_code = module_data.get('code', 'unknown')
        cached_lesson = get_cached_lesson(module_code, 'guided', student_locale)
        if cached_lesson:
            print(f"Cache hit for {module_code} guided lesson")
            return cached_lesson

        subject = module_data.get('subject', 'General')
        title = module_data.get('title', 'Unknown Module')

        prompt = f"""
Создай урок типа "guided" на русском языке для модуля "{title}" по предмету "{subject}".

Guided урок должен включать:
1. Инструкцию (instruction) - объяснение задания
2. Интерактивный элемент (interactive) - практическое упражнение с подсказками

Формат ответа должен быть строго JSON:
{{
  "id": "lesson_{module_data.get('code', 'unknown')}_guided_01",
  "type": "guided",
  "title": "Название урока с подсказками",
  "locale": "{student_locale}",
  "blocks": [
    {{
      "type": "instruction",
      "content": {{
        "title": "Задание",
        "text": "Описание задания с пошаговыми инструкциями..."
      }}
    }},
    {{
      "type": "interactive",
      "content": {{
        "type": "drag_drop",
        "instruction": "Инструкция по выполнению упражнения",
        "items": [
          {{
            "number": "1",
            "objects": ["🍎", "🍎"]
          }},
          {{
            "number": "2",
            "objects": ["⭐", "⭐", "⭐"]
          }}
        ]
      }}
    }}
  ]
}}

Сделай урок с поддержкой и подсказками для ученика.
"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1500,
            )

            response_text = chat_completion.choices[0].message.content

            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                lesson_data = json.loads(json_match.group())
                # Save to cache
                save_lesson_to_cache(module_code, 'guided', lesson_data, student_locale)
                return lesson_data
            else:
                fallback_lesson = self._create_fallback_guided_lesson(module_data, student_locale)
                save_lesson_to_cache(module_code, 'guided', fallback_lesson, student_locale)
                return fallback_lesson

        except Exception as e:
            print(f"AI generation error: {e}")
            fallback_lesson = self._create_fallback_guided_lesson(module_data, student_locale)
            save_lesson_to_cache(module_code, 'guided', fallback_lesson, student_locale)
            return fallback_lesson

    def generate_independent_lesson(self, module_data: Dict[str, Any], student_locale: str = 'ru') -> Dict[str, Any]:
        """Generate an independent lesson using AI."""

        # Check cache first
        module_code = module_data.get('code', 'unknown')
        cached_lesson = get_cached_lesson(module_code, 'independent', student_locale)
        if cached_lesson:
            print(f"Cache hit for {module_code} independent lesson")
            return cached_lesson

        subject = module_data.get('subject', 'General')
        title = module_data.get('title', 'Unknown Module')

        prompt = f"""
Создай урок типа "independent" на русском языке для модуля "{title}" по предмету "{subject}".

Independent урок должен включать:
1. Задание для самостоятельной работы
2. Интерактивные элементы для практики

Формат ответа должен быть строго JSON:
{{
  "id": "lesson_{module_data.get('code', 'unknown')}_independent_01",
  "type": "independent",
  "title": "Самостоятельная работа",
  "locale": "{student_locale}",
  "blocks": [
    {{
      "type": "instruction",
      "content": {{
        "title": "Самостоятельное задание",
        "text": "Описание задания для самостоятельного выполнения..."
      }}
    }},
    {{
      "type": "interactive",
      "content": {{
        "type": "practice",
        "instruction": "Практические задания",
        "tasks": [
          {{
            "id": "task_1",
            "question": "Вопрос для самостоятельного решения?",
            "hint": "Подсказка для трудных случаев..."
          }}
        ]
      }}
    }}
  ]
}}

Сделай урок для развития самостоятельности.
"""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=1500,
            )

            response_text = chat_completion.choices[0].message.content

            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                lesson_data = json.loads(json_match.group())
                # Save to cache
                save_lesson_to_cache(module_code, 'independent', lesson_data, student_locale)
                return lesson_data
            else:
                fallback_lesson = self._create_fallback_independent_lesson(module_data, student_locale)
                save_lesson_to_cache(module_code, 'independent', fallback_lesson, student_locale)
                return fallback_lesson

        except Exception as e:
            print(f"AI generation error: {e}")
            fallback_lesson = self._create_fallback_independent_lesson(module_data, student_locale)
            save_lesson_to_cache(module_code, 'independent', fallback_lesson, student_locale)
            return fallback_lesson

    def _create_fallback_concept_lesson(self, module_data: Dict[str, Any], locale: str) -> Dict[str, Any]:
        """Create a basic concept lesson when AI fails."""
        return {
            "id": f"lesson_{module_data.get('code', 'unknown')}_concept_01",
            "type": "concept",
            "title": f"Основы: {module_data.get('title', 'Unknown')}",
            "locale": locale,
            "blocks": [
                {
                    "type": "theory",
                    "content": {
                        "title": "Теоретическая основа",
                        "text": f"Изучаем основы модуля {module_data.get('title', 'Unknown')}."
                    }
                },
                {
                    "type": "example",
                    "content": {
                        "title": "Пример",
                        "text": "Практический пример применения изученного материала."
                    }
                },
                {
                    "type": "interactive",
                    "content": {
                        "type": "mcq",
                        "question": "Проверьте понимание материала",
                        "options": ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
                        "correct": 0,
                        "explanation": "Это тестовый вопрос для проверки понимания."
                    }
                }
            ]
        }

    def _create_fallback_guided_lesson(self, module_data: Dict[str, Any], locale: str) -> Dict[str, Any]:
        """Create a basic guided lesson when AI fails."""
        return {
            "id": f"lesson_{module_data.get('code', 'unknown')}_guided_01",
            "type": "guided",
            "title": f"Практика с подсказками: {module_data.get('title', 'Unknown')}",
            "locale": locale,
            "blocks": [
                {
                    "type": "instruction",
                    "content": {
                        "title": "Задание с поддержкой",
                        "text": "Выполните задание, используя подсказки и инструкции."
                    }
                },
                {
                    "type": "interactive",
                    "content": {
                        "type": "guided_practice",
                        "instruction": "Следуйте инструкциям для выполнения задания",
                        "steps": [
                            {"step": 1, "instruction": "Первый шаг"},
                            {"step": 2, "instruction": "Второй шаг"}
                        ]
                    }
                }
            ]
        }

    def _create_fallback_independent_lesson(self, module_data: Dict[str, Any], locale: str) -> Dict[str, Any]:
        """Create a basic independent lesson when AI fails."""
        return {
            "id": f"lesson_{module_data.get('code', 'unknown')}_independent_01",
            "type": "independent",
            "title": f"Самостоятельная работа: {module_data.get('title', 'Unknown')}",
            "locale": locale,
            "blocks": [
                {
                    "type": "instruction",
                    "content": {
                        "title": "Самостоятельное задание",
                        "text": "Выполните задание самостоятельно, используя приобретенные знания."
                    }
                },
                {
                    "type": "interactive",
                    "content": {
                        "type": "practice",
                        "instruction": "Самостоятельные упражнения",
                        "tasks": [
                            {
                                "id": "task_1",
                                "question": "Самостоятельное задание",
                                "hint": "Используйте изученный материал"
                            }
                        ]
                    }
                }
            ]
        }


# Global instance for use in API
ai_generator = AILessonGenerator()


def generate_ai_concept_lesson(module_data: Dict[str, Any], locale: str = 'ru') -> Dict[str, Any]:
    """Generate concept lesson using AI."""
    return ai_generator.generate_concept_lesson(module_data, locale)


def generate_ai_guided_lesson(module_data: Dict[str, Any], locale: str = 'ru') -> Dict[str, Any]:
    """Generate guided lesson using AI."""
    return ai_generator.generate_guided_lesson(module_data, locale)


def generate_ai_independent_lesson(module_data: Dict[str, Any], locale: str = 'ru') -> Dict[str, Any]:
    """Generate independent lesson using AI."""
    return ai_generator.generate_independent_lesson(module_data, locale)
