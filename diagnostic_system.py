#!/usr/bin/env python3
"""
Диагностическая система для определения уровня ученика.

Функции:
- Проведение начальной диагностики для новых учеников
- Оценка текущего уровня по предмету
- Рекомендации по сложности заданий
- Адаптация контента под уровень ученика
"""

import json
import uuid
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

from mastery_calculator import MasteryCalculatorV2, get_mastery_description

# Импорт AI генератора (опционально)
try:
    from ai_generator import generate_ai_concept_lesson
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


@dataclass
class DiagnosticConfig:
    """Конфигурация диагностической системы."""
    # Количество вопросов для диагностики
    questions_per_level: int = 5
    # Максимальное время на ответ (сек)
    max_time_per_question: int = 300
    # Минимальный процент правильных ответов для прохождения уровня
    min_score_threshold: float = 0.6
    # Уровни сложности
    levels: List[str] = None

    def __post_init__(self):
        if self.levels is None:
            self.levels = ['beginner', 'elementary', 'intermediate', 'advanced']


class DiagnosticSystem:
    """Система диагностики уровня ученика."""

    def __init__(self, config: Optional[DiagnosticConfig] = None):
        self.config = config or DiagnosticConfig()
        self.mastery_calc = MasteryCalculatorV2()

    def start_diagnostic_session(
        self,
        db_connection,
        student_id: str,
        subject_id: str,
        stage_id: str
    ) -> str:
        """
        Начинает новую диагностическую сессию.

        Returns:
            session_id: UUID созданной сессии
        """
        session_id = str(uuid.uuid4())

        with db_connection.cursor() as cur:
            cur.execute("""
                INSERT INTO diagnostic_session (
                    id, student_id, subject_id, stage_id, status
                ) VALUES (%s, %s, %s, %s, 'in_progress')
            """, (session_id, student_id, subject_id, stage_id))

        return session_id

    def get_next_diagnostic_question(
        self,
        db_connection,
        session_id: str,
        current_level: str = None,
        answered_questions: List[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Генерирует следующий вопрос для диагностики с помощью AI.

        Returns:
            question_data: словарь с данными вопроса или None если диагностика завершена
        """
        with db_connection.cursor() as cur:
            # Получаем информацию о сессии и предмете
            cur.execute("""
                SELECT ds.subject_id, ds.stage_id, s.title as subject_title,
                       st.title as stage_title, COUNT(dr.id) as answered_questions
                FROM diagnostic_session ds
                JOIN subject s ON ds.subject_id = s.id
                JOIN stage st ON ds.stage_id = st.id
                LEFT JOIN diagnostic_response dr ON ds.id = dr.session_id
                WHERE ds.id = %s
                GROUP BY ds.id, ds.subject_id, ds.stage_id, s.title, st.title
            """, (session_id,))

            session_data = cur.fetchone()
            if not session_data:
                return None

            subject_id, stage_id, subject_title, stage_title, answered_count = session_data

            # Если это уже 5+ вопрос - завершаем диагностику
            if answered_count >= 5:
                return None

            # Определяем уровень для вопроса
            if current_level is None:
                question_level = self.config.levels[0]  # Начинаем с beginner
            else:
                question_level = current_level

            # Генерируем вопрос с помощью AI
            question_data = self._generate_ai_question(
                subject_title, stage_title, question_level, answered_questions or []
            )

            if not question_data:
                return None

            # Сохраняем вопрос в базе для отслеживания
            cur.execute("""
                INSERT INTO diagnostic_question (
                    subject_id, stage_id, difficulty_level, question_type,
                    content_jsonb, correct_answer_jsonb, explanation_jsonb,
                    time_limit_sec, points, active
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, false)
                RETURNING id
            """, (
                subject_id, stage_id, question_level, question_data['type'],
                json.dumps(question_data['content']),
                json.dumps(question_data['correct_answer']),
                json.dumps(question_data.get('explanation', {})),
                question_data.get('time_limit', 120),
                question_data.get('points', 1)
            ))

            question_id = cur.fetchone()[0]

            return {
                'question_id': question_id,
                'content': question_data['content'],
                'question_type': question_data['type'],
                'time_limit_sec': question_data.get('time_limit', 120),
                'points': question_data.get('points', 1),
                'difficulty_level': question_level,
                'ai_generated': True
            }

    def submit_diagnostic_answer(
        self,
        db_connection,
        session_id: str,
        question_id: str,
        student_answer: Dict[str, Any],
        time_spent_sec: int
    ) -> Dict[str, Any]:
        """
        Обрабатывает ответ ученика на диагностический вопрос.

        Returns:
            result: информация о результате ответа
        """
        with db_connection.cursor() as cur:
            # Получаем правильный ответ
            cur.execute("""
                SELECT correct_answer_jsonb, points, difficulty_level
                FROM diagnostic_question
                WHERE id = %s
            """, (question_id,))

            question_data = cur.fetchone()
            if not question_data:
                return {'error': 'Question not found'}

            correct_answer, max_points, difficulty_level = question_data

            # Проверяем ответ (простая проверка для MCQ)
            is_correct = self._check_answer(student_answer, correct_answer)
            points_earned = max_points if is_correct else 0

            # Сохраняем ответ
            cur.execute("""
                INSERT INTO diagnostic_response (
                    session_id, question_id, student_answer_jsonb,
                    is_correct, time_spent_sec, points_earned
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                session_id, question_id, json.dumps(student_answer),
                is_correct, time_spent_sec, points_earned
            ))

            # Получаем статистику по сессии
            cur.execute("""
                SELECT
                    COUNT(*) as total_questions,
                    SUM(CASE WHEN is_correct THEN 1 ELSE 0 END) as correct_answers,
                    AVG(time_spent_sec) as avg_time,
                    SUM(points_earned) as total_points,
                    MAX(points_earned) as max_points_possible
                FROM diagnostic_response
                WHERE session_id = %s
            """, (session_id,))

            stats = cur.fetchone()
            total_questions, correct_answers, avg_time, total_points, max_points_possible = stats

            # Рассчитываем процент правильных ответов
            accuracy = correct_answers / total_questions if total_questions > 0 else 0

            # Определяем следующий уровень сложности
            next_level = self._determine_next_level(difficulty_level, accuracy, total_questions)

            return {
                'is_correct': is_correct,
                'points_earned': points_earned,
                'total_score': accuracy,
                'next_level': next_level,
                'completed_questions': total_questions,
                'avg_time_spent': float(avg_time or 0)
            }

    def complete_diagnostic_session(
        self,
        db_connection,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Завершает диагностическую сессию и рассчитывает итоговый уровень.

        Returns:
            diagnostic_result: результаты диагностики
        """
        with db_connection.cursor() as cur:
            # Получаем все ответы из сессии
            cur.execute("""
                SELECT
                    dr.is_correct,
                    dr.time_spent_sec,
                    dr.points_earned,
                    dq.difficulty_level,
                    dq.points as max_points
                FROM diagnostic_response dr
                JOIN diagnostic_question dq ON dr.question_id = dq.id
                WHERE dr.session_id = %s
                ORDER BY dr.created_at
            """, (session_id,))

            responses = cur.fetchall()

            if not responses:
                return {'error': 'No responses found in session'}

            # Анализируем результаты
            total_questions = len(responses)
            correct_answers = sum(1 for r in responses if r[0])
            total_points = sum(r[2] for r in responses)
            avg_time = sum(r[1] for r in responses) / total_questions

            # Распределение по уровням сложности
            level_distribution = {}
            for response in responses:
                level = response[3]
                level_distribution[level] = level_distribution.get(level, 0) + 1

            # Определяем уровень ученика
            estimated_level, confidence = self._calculate_student_level(responses)
            recommended_difficulty = self._calculate_recommended_difficulty(estimated_level, confidence)

            # Сохраняем результаты
            results = {
                'total_questions': total_questions,
                'correct_answers': correct_answers,
                'accuracy': correct_answers / total_questions,
                'total_points': total_points,
                'avg_time_spent': avg_time,
                'level_distribution': level_distribution,
                'estimated_level': estimated_level,
                'confidence_score': confidence,
                'recommended_difficulty': recommended_difficulty
            }

            recommendations = self._generate_recommendations(results)

            cur.execute("""
                UPDATE diagnostic_session
                SET status = 'completed',
                    completed_at = now(),
                    estimated_level = %s,
                    confidence_score = %s,
                    results_jsonb = %s,
                    recommendations_jsonb = %s
                WHERE id = %s
            """, (
                estimated_level,
                confidence,
                json.dumps(results),
                json.dumps(recommendations),
                session_id
            ))

            # Обновляем информацию в таблице student
            cur.execute("""
                SELECT student_id FROM diagnostic_session WHERE id = %s
            """, (session_id,))

            student_id = cur.fetchone()[0]

            cur.execute("""
                UPDATE student
                SET diagnostic_completed_at = now(),
                    current_level = %s,
                    recommended_difficulty = %s
                WHERE id = %s
            """, (estimated_level, recommended_difficulty, student_id))

            return {
                'session_id': session_id,
                'estimated_level': estimated_level,
                'confidence_score': confidence,
                'recommended_difficulty': recommended_difficulty,
                'results': results,
                'recommendations': recommendations
            }

    def _check_answer(self, student_answer: Dict, correct_answer: Dict) -> bool:
        """Проверяет правильность ответа ученика."""
        # Простая проверка для MCQ вопросов
        if 'selected_option' in student_answer and 'correct_option' in correct_answer:
            return student_answer['selected_option'] == correct_answer['correct_option']

        # Для более сложных типов вопросов нужна дополнительная логика
        return False

    def _determine_next_level(self, current_level: str, accuracy: float, questions_count: int) -> str:
        """Определяет следующий уровень сложности для вопроса."""
        if accuracy >= self.config.min_score_threshold and questions_count >= self.config.questions_per_level:
            # Ученик справляется - повышаем уровень
            current_index = self.config.levels.index(current_level) if current_level in self.config.levels else 0
            next_index = min(current_index + 1, len(self.config.levels) - 1)
            return self.config.levels[next_index]
        else:
            # Продолжаем на текущем уровне
            return current_level

    def _calculate_student_level(self, responses: List[Tuple]) -> Tuple[str, float]:
        """Рассчитывает уровень ученика на основе всех ответов."""
        if not responses:
            return 'beginner', 0.0

        # Анализируем успешность по уровням
        level_performance = {}
        for response in responses:
            is_correct, time_spent, points, level, max_points = response
            if level not in level_performance:
                level_performance[level] = {'correct': 0, 'total': 0, 'avg_time': []}

            level_performance[level]['total'] += 1
            level_performance[level]['avg_time'].append(time_spent)
            if is_correct:
                level_performance[level]['correct'] += 1

        # Находим самый высокий уровень, с которым ученик справляется
        best_level = 'beginner'
        confidence = 0.0

        for level in reversed(self.config.levels):
            if level in level_performance:
                perf = level_performance[level]
                accuracy = perf['correct'] / perf['total']
                avg_time = sum(perf['avg_time']) / len(perf['avg_time'])

                if accuracy >= 0.7:  # Хорошо справляется с уровнем
                    best_level = level
                    confidence = accuracy
                    break
                elif accuracy >= 0.5:  # Средне справляется
                    best_level = level
                    confidence = accuracy * 0.8
                    break

        return best_level, confidence

    def _calculate_recommended_difficulty(self, estimated_level: str, confidence: float) -> str:
        """Определяет рекомендуемую сложность заданий."""
        level_mapping = {
            'beginner': 'easy',
            'elementary': 'easy',
            'intermediate': 'medium',
            'advanced': 'hard'
        }

        base_difficulty = level_mapping.get(estimated_level, 'medium')

        # Корректируем сложность в зависимости от уверенности
        if confidence < 0.5:
            # Низкая уверенность - понижаем сложность
            difficulty_levels = ['easy', 'medium', 'hard', 'expert']
            current_index = difficulty_levels.index(base_difficulty)
            adjusted_index = max(0, current_index - 1)
            return difficulty_levels[adjusted_index]
        elif confidence > 0.8:
            # Высокая уверенность - можем повысить сложность
            difficulty_levels = ['easy', 'medium', 'hard', 'expert']
            current_index = difficulty_levels.index(base_difficulty)
            adjusted_index = min(len(difficulty_levels) - 1, current_index + 1)
            return difficulty_levels[adjusted_index]

        return base_difficulty

    def _generate_recommendations(self, results: Dict) -> Dict[str, Any]:
        """Генерирует рекомендации по обучению на основе результатов диагностики."""
        estimated_level = results['estimated_level']
        accuracy = results['accuracy']
        avg_time = results['avg_time_spent']

        recommendations = {
            'study_plan': [],
            'focus_areas': [],
            'estimated_completion_time': '',
            'suggested_learning_path': []
        }

        # Рекомендации по плану обучения
        if accuracy < 0.5:
            recommendations['study_plan'].append("Рекомендуется начать с основ и постепенно повышать сложность")
            recommendations['focus_areas'].append("Базовые понятия и навыки")
        elif accuracy < 0.7:
            recommendations['study_plan'].append("Нужна дополнительная практика по сложным темам")
            recommendations['focus_areas'].append("Практические задания и закрепление материала")
        else:
            recommendations['study_plan'].append("Можно переходить к более сложным темам")
            recommendations['focus_areas'].append("Расширение знаний и углубленное изучение")

        # Временные рекомендации
        if avg_time > 180:  # Более 3 минут в среднем
            recommendations['study_plan'].append("Рекомендуется больше времени на размышления")
        elif avg_time < 30:  # Менее 30 секунд
            recommendations['study_plan'].append("Возможно, задания кажутся слишком простыми")

        # Путь обучения
        level_order = ['beginner', 'elementary', 'intermediate', 'advanced']
        current_index = level_order.index(estimated_level) if estimated_level in level_order else 0

        for i in range(current_index, len(level_order)):
            recommendations['suggested_learning_path'].append({
                'level': level_order[i],
                'status': 'completed' if i < current_index else ('current' if i == current_index else 'upcoming')
            })

        return recommendations

    def _generate_ai_question(
        self,
        subject_title: str,
        stage_title: str,
        difficulty_level: str,
        previous_answers: List[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Генерирует диагностический вопрос с помощью AI.

        Args:
            subject_title: Название предмета (например, "Математика")
            stage_title: Название уровня (например, "Начальная школа")
            difficulty_level: Уровень сложности ('beginner', 'elementary', 'intermediate', 'advanced')
            previous_answers: Предыдущие ответы ученика для адаптации

        Returns:
            question_data: Структура вопроса или None при ошибке
        """
        if not AI_AVAILABLE:
            # Fallback: генерируем простой вопрос без AI
            return self._generate_fallback_question(subject_title, difficulty_level)

        try:
            # Получаем API ключ для AI
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                return self._generate_fallback_question(subject_title, difficulty_level)

            # Создаем промпт для генерации диагностического вопроса
            prompt = self._create_diagnostic_prompt(
                subject_title, stage_title, difficulty_level, previous_answers
            )

            # Используем AI для генерации вопроса
            from groq import Groq
            client = Groq(api_key=api_key)

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational diagnostic system. Generate questions to assess student's knowledge level."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=800
            )

            response_text = chat_completion.choices[0].message.content

            # Парсим JSON из ответа AI
            return self._parse_ai_question_response(response_text, difficulty_level)

        except Exception as e:
            print(f"AI generation error: {e}")
            return self._generate_fallback_question(subject_title, difficulty_level)

    def _create_diagnostic_prompt(
        self,
        subject_title: str,
        stage_title: str,
        difficulty_level: str,
        previous_answers: List[Dict] = None
    ) -> str:
        """Создает промпт для AI генерации диагностического вопроса."""

        level_descriptions = {
            'beginner': 'начальный уровень, базовые понятия',
            'elementary': 'элементарный уровень, простые операции',
            'intermediate': 'средний уровень, применение знаний',
            'advanced': 'продвинутый уровень, сложные задачи'
        }

        prompt = f"""
Создай диагностический вопрос по предмету "{subject_title}" для уровня "{stage_title}".
Уровень сложности: {level_descriptions.get(difficulty_level, difficulty_level)}

Требования к вопросу:
1. Вопрос должен проверять фундаментальные знания по предмету
2. Уровень сложности должен соответствовать указанному уровню
3. Вопрос должен иметь однозначный правильный ответ
4. Дай подробное объяснение правильного ответа

Формат ответа (ТОЛЬКО JSON):
{{
  "type": "mcq",
  "content": {{
    "question": "Текст вопроса",
    "options": ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
    "instruction": "Выберите правильный ответ"
  }},
  "correct_answer": {{
    "correct_option": 0
  }},
  "explanation": {{
    "explanation": "Подробное объяснение правильного ответа"
  }},
  "time_limit": 120,
  "points": 1
}}
"""

        if previous_answers:
            prompt += f"\n\nУченик уже ответил на {len(previous_answers)} вопросов. " \
                     f"Последний ответ был {'правильным' if previous_answers[-1].get('is_correct') else 'неправильным'}."

        return prompt

    def _parse_ai_question_response(self, response_text: str, difficulty_level: str) -> Optional[Dict[str, Any]]:
        """Парсит ответ AI и преобразует в структуру вопроса."""
        try:
            # Ищем JSON в ответе
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                question_data = json.loads(json_match.group())

                # Валидируем структуру
                if 'content' in question_data and 'correct_answer' in question_data:
                    question_data['type'] = question_data.get('type', 'mcq')
                    question_data['time_limit'] = question_data.get('time_limit', 120)
                    question_data['points'] = question_data.get('points', 1)
                    return question_data

        except json.JSONDecodeError:
            pass

        # Если не удалось распарсить, возвращаем fallback
        return None

    def _generate_fallback_question(self, subject_title: str, difficulty_level: str) -> Dict[str, Any]:
        """Генерирует простой вопрос без AI (fallback)."""

        if subject_title.lower().startswith('мат'):
            # Математические вопросы
            if difficulty_level == 'beginner':
                return {
                    'type': 'mcq',
                    'content': {
                        'question': 'Сколько будет 2 + 2?',
                        'options': ['3', '4', '5', '6'],
                        'instruction': 'Выберите правильный ответ'
                    },
                    'correct_answer': {'correct_option': 1},
                    'explanation': {'explanation': '2 + 2 = 4'},
                    'time_limit': 60,
                    'points': 1
                }
            elif difficulty_level == 'elementary':
                return {
                    'type': 'mcq',
                    'content': {
                        'question': 'Сколько будет 10 - 3?',
                        'options': ['6', '7', '8', '13'],
                        'instruction': 'Выберите правильный ответ'
                    },
                    'correct_answer': {'correct_option': 1},
                    'explanation': {'explanation': '10 - 3 = 7'},
                    'time_limit': 90,
                    'points': 1
                }
            else:
                return {
                    'type': 'mcq',
                    'content': {
                        'question': 'Найдите периметр прямоугольника со сторонами 6 см и 8 см',
                        'options': ['14 см', '28 см', '48 см', '24 см'],
                        'instruction': 'Выберите правильный ответ'
                    },
                    'correct_answer': {'correct_option': 1},
                    'explanation': {'explanation': 'Периметр = 2 × (6 + 8) = 28 см'},
                    'time_limit': 180,
                    'points': 2
                }
        else:
            # Общие вопросы для других предметов
            return {
                'type': 'mcq',
                'content': {
                    'question': f'Это диагностический вопрос по предмету {subject_title}',
                    'options': ['Вариант 1', 'Вариант 2', 'Вариант 3', 'Вариант 4'],
                    'instruction': 'Выберите правильный ответ'
                },
                'correct_answer': {'correct_option': 0},
                'explanation': {'explanation': 'Это тестовый вопрос'},
                'time_limit': 120,
                'points': 1
            }


# Глобальный экземпляр системы диагностики
diagnostic_system = DiagnosticSystem()
