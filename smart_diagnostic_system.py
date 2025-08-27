#!/usr/bin/env python3
"""Простая адаптивная система диагностики.

Используется в ``ai_self_diagnostic`` для демонстрации того, как вопросы
могут усложняться в зависимости от ответов ученика. Модуль не обращается
к внешним сервисам и опирается только на стандартную библиотеку.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Tuple


class DifficultyLevel(Enum):
    """Уровни сложности вопросов."""

    BEGINNER = "beginner"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


# Упорядоченный список уровней для удобной навигации
LEVELS: List[DifficultyLevel] = [
    DifficultyLevel.BEGINNER,
    DifficultyLevel.ELEMENTARY,
    DifficultyLevel.INTERMEDIATE,
    DifficultyLevel.ADVANCED,
    DifficultyLevel.EXPERT,
]


@dataclass
class Question:
    """Структура диагностического вопроса."""

    id: str
    subject: str
    difficulty_level: DifficultyLevel
    question_type: str
    content: Dict[str, Any]
    target_age: int


@dataclass
class SubjectProgress:
    """Состояние обучения по отдельному предмету."""

    current_level: DifficultyLevel = DifficultyLevel.BEGINNER
    questions_asked: int = 0
    correct_answers: int = 0
    total_time_spent: float = 0.0
    asked_dialogue: bool = False


@dataclass
class StudentProfile:
    """Профиль ученика в системе."""

    student_id: str
    age: int
    subjects: Dict[str, SubjectProgress]
    dialogue_answers: List[str] = field(default_factory=list)


class SmartDiagnosticSystem:
    """Адаптивная диагностика с простыми правилами."""

    def __init__(self):
        self.profiles: Dict[str, StudentProfile] = {}
        self.active_questions: Dict[Tuple[str, str], Question] = {}

    # ------------------------------------------------------------------
    # Внутренние утилиты
    def _level_index(self, level: DifficultyLevel) -> int:
        return LEVELS.index(level)

    def _index_to_level(self, idx: int) -> DifficultyLevel:
        idx = max(0, min(idx, len(LEVELS) - 1))
        return LEVELS[idx]

    # ------------------------------------------------------------------
    # Публичный API
    def initialize_student_profile(
        self, student_id: str, age: int, subjects: List[str]
    ) -> StudentProfile:
        """Создаёт профиль ученика."""

        profile = StudentProfile(
            student_id=student_id,
            age=age,
            subjects={s: SubjectProgress() for s in subjects},
        )
        self.profiles[student_id] = profile
        return profile

    def generate_next_question(self, student_id: str, subject: str) -> Optional[Question]:
        """Генерирует следующий вопрос для ученика."""

        profile = self.profiles.get(student_id)
        if not profile:
            raise ValueError("Unknown student_id")
        progress = profile.subjects.get(subject)
        if not progress:
            raise ValueError("Unknown subject")

        # Первая попытка — диалоговый вопрос для психологического портрета
        if not progress.asked_dialogue:
            progress.asked_dialogue = True
            q_id = f"{subject}_dialogue_{progress.questions_asked}"
            content = {
                "question": f"Расскажи, что тебе нравится в предмете {subject}?",
                "correct_answer": "диалоговый_ответ",
                "options": [],
            }
            question = Question(
                id=q_id,
                subject=subject,
                difficulty_level=progress.current_level,
                question_type="dialogue",
                content=content,
                target_age=profile.age,
            )
            self.active_questions[(student_id, q_id)] = question
            return question

        # Тестовый вопрос по предмету
        level_idx = self._level_index(progress.current_level)
        target_age = profile.age - 3 + level_idx
        q_id = f"{subject}_{progress.questions_asked}"

        if subject.lower().startswith("math"):
            # Детеминированные числа, чтобы тесты были стабильными
            a, b = 2 + level_idx, 3 + level_idx
            correct = a + b
            content = {
                "question": f"Сколько будет {a} + {b}?",
                "correct_answer": str(correct),
                "options": [
                    str(correct),
                    str(correct + 1),
                    str(correct - 1),
                    str(correct + 2),
                ],
            }
            qtype = "mcq_single"
        else:
            # Простой словарный вопрос по английскому
            words = ["cat", "dog", "sun", "book"]
            translations = {"cat": "кот", "dog": "собака", "sun": "солнце", "book": "книга"}
            word = words[level_idx % len(words)]
            content = {
                "question": f"Как по-английски '{translations[word]}'?",
                "correct_answer": word,
                "options": [word, "bad", "good", "run"],
            }
            qtype = "mcq_single"

        question = Question(
            id=q_id,
            subject=subject,
            difficulty_level=progress.current_level,
            question_type=qtype,
            content=content,
            target_age=target_age,
        )
        self.active_questions[(student_id, q_id)] = question
        return question

    def process_answer(
        self,
        student_id: str,
        question_id: str,
        answer: Dict[str, Any],
        time_spent_sec: float,
        profile: Optional[StudentProfile] = None,
    ) -> Dict[str, Any]:
        """Обрабатывает ответ ученика и адаптирует сложность."""

        profile = profile or self.profiles.get(student_id)
        if not profile:
            raise ValueError("Unknown student_id")
        question = self.active_questions.get((student_id, question_id))
        if not question:
            raise ValueError("Unknown question_id")

        progress = profile.subjects[question.subject]
        progress.questions_asked += 1
        progress.total_time_spent += time_spent_sec

        if question.question_type == "dialogue":
            is_correct = True
            profile.dialogue_answers.append(answer.get("answer", ""))
        else:
            user_answer = str(answer.get("answer", "")).strip().lower()
            correct = str(question.content.get("correct_answer", "")).strip().lower()
            is_correct = user_answer == correct
            if is_correct:
                progress.correct_answers += 1

        # Адаптация сложности
        idx = self._level_index(progress.current_level)
        idx = idx + 1 if is_correct else idx - 1
        new_level = self._index_to_level(idx)
        progress.current_level = new_level
        confidence = progress.correct_answers / max(progress.questions_asked, 1)

        return {
            "is_correct": is_correct,
            "confidence_score": round(confidence, 2),
            "new_difficulty_level": new_level.value,
        }

    def generate_learning_plan(self, student_id: str) -> Dict[str, Any]:
        """Формирует краткий план обучения."""

        profile = self.profiles.get(student_id)
        if not profile:
            raise ValueError("Unknown student_id")

        breakdown: Dict[str, Any] = {}
        level_sum = 0
        for subject, prog in profile.subjects.items():
            acc = prog.correct_answers / max(prog.questions_asked, 1)
            breakdown[subject] = {
                "current_level": prog.current_level.value,
                "questions_asked": prog.questions_asked,
                "correct_answers": prog.correct_answers,
                "total_time_spent": prog.total_time_spent,
            }
            level_sum += self._level_index(prog.current_level)

        avg_idx = round(level_sum / max(len(profile.subjects), 1))
        overall_level = self._index_to_level(avg_idx).value

        strengths = [
            f"{s} strong understanding"
            for s, p in profile.subjects.items()
            if p.questions_asked and (p.correct_answers / p.questions_asked) >= 0.8
        ]
        weaknesses = [
            f"{s} needs practice"
            for s, p in profile.subjects.items()
            if p.questions_asked and (p.correct_answers / p.questions_asked) < 0.5
        ]

        style = (
            "expressive"
            if any("!" in ans or ":)" in ans for ans in profile.dialogue_answers)
            else "calm"
        )

        recommendations = {
            "immediate_focus": [
                s
                for s, p in profile.subjects.items()
                if p.questions_asked and (p.correct_answers / p.questions_asked) < 0.6
            ],
            "study_schedule": {
                "daily_time": 45,
                "preferred_subjects": list(profile.subjects.keys()),
            },
            "teaching_approach": "creative" if style == "expressive" else "structured",
        }

        return {
            "overall_level": overall_level,
            "subject_breakdown": breakdown,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "psychological_profile": {
                "communication_style": style,
                "samples": profile.dialogue_answers[:3],
            },
            "recommendations": recommendations,
        }

    def export_session_record(self, student_id: str) -> Dict[str, Any]:
        """Подготовить данные диагностики для сохранения в БД."""
        profile = self.profiles.get(student_id)
        if not profile:
            raise ValueError("Unknown student_id")
        plan = self.generate_learning_plan(student_id)
        return {
            "student_id": student_id,
            "context": {"age": profile.age},
            "results": plan["subject_breakdown"],
            "persona": {
                "communication_style": plan["psychological_profile"]["communication_style"],
                "samples": plan["psychological_profile"]["samples"],
            },
        }
