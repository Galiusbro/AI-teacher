#!/usr/bin/env python3
"""
Умная адаптивная диагностическая система Ayaal Teacher.

Ключевые особенности:
1. Адаптивная сложность с учетом возраста ученика
2. Психологическое профилирование через диалоговые вопросы
3. Индивидуальные траектории обучения
4. Генерация вопросов через шаблоны
5. Комплексная оценка компетентности по предметам
"""

import json
import os
import random
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import math

# Импорт AI генератора (опционально)
try:
    from ai_generator import generate_ai_concept_lesson
    AI_AVAILABLE = True
except (ImportError, ValueError):
    AI_AVAILABLE = False


class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class CognitiveDomain(Enum):
    REMEMBER = "remember"
    UNDERSTAND = "understand"
    APPLY = "apply"
    ANALYZE = "analyze"
    EVALUATE = "evaluate"
    CREATE = "create"


@dataclass
class StudentProfile:
    """Профиль ученика для персонализации диагностики."""
    student_id: str
    age: int
    subjects: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    psychological_profile: Dict[str, Any] = field(default_factory=dict)
    learning_history: List[Dict[str, Any]] = field(default_factory=list)
    current_difficulty: Dict[str, DifficultyLevel] = field(default_factory=dict)
    recommended_difficulty: Dict[str, str] = field(default_factory=dict)


@dataclass
class DiagnosticQuestion:
    """Структурированный диагностический вопрос."""
    id: str
    subject: str
    target_age: int
    difficulty_level: DifficultyLevel
    question_type: str
    cognitive_domain: CognitiveDomain
    content: Dict[str, Any]
    scoring: Dict[str, Any]
    adaptation_rules: Dict[str, Any]
    psychological_profile: Dict[str, Any]
    estimated_time_sec: int


class SmartDiagnosticSystem:
    """
    Умная адаптивная диагностическая система.

    Особенности:
    - Начинает с уровня на 2-3 года младше возраста ученика
    - Адаптирует сложность на основе ответов
    - Собирает психологический профиль
    - Создает индивидуальную траекторию обучения
    """

    def __init__(self, config_path: str = None):
        self.templates = self._load_templates()
        self.schemas = self._load_schemas()
        self.config = self._load_config(config_path)
        self.student_profiles: Dict[str, StudentProfile] = {}

    def _load_templates(self) -> Dict[str, Any]:
        """Загружает шаблоны диагностических вопросов."""
        template_path = "/Users/gp/projects/ayaal/teacher/curriculum/diagnostic/diagnostic.template.json"
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Шаблоны не найдены: {template_path}")
            return self._get_default_templates()

    def _load_schemas(self) -> Dict[str, Any]:
        """Загружает схемы диагностических вопросов."""
        schema_path = "/Users/gp/projects/ayaal/teacher/curriculum/diagnostic/diagnostic.schema.json"
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Схема не найдена: {schema_path}")
            return {}

    def _load_config(self, config_path: str = None) -> Dict[str, Any]:
        """Загружает конфигурацию системы."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)

        return {
            "adaptation": {
                "age_adjustment": -2,  # Начинаем на 2 года младше
                "correct_streak_threshold": 3,
                "incorrect_streak_threshold": 2,
                "max_age_advance": 3,
                "min_age_decline": -4
            },
            "psychological_profiling": {
                "dialogue_questions_count": 3,
                "personality_questions_count": 2
            },
            "subjects": {
                "Mathematics": {"weight": 1.0},
                "English": {"weight": 1.0},
                "Science": {"weight": 0.8}
            }
        }

    def _get_default_templates(self) -> Dict[str, Any]:
        """Возвращает базовые шаблоны при отсутствии файла."""
        return {
            "diagnostic_templates": {
                "mcq_single": {
                    "structure": {
                        "question_type": "mcq_single",
                        "content": {
                            "question": "{{QUESTION_TEXT}}",
                            "options": [
                                {"text": "{{CORRECT_ANSWER}}", "is_correct": true},
                                {"text": "{{DISTRACTOR_1}}"},
                                {"text": "{{DISTRACTOR_2}}"},
                                {"text": "{{DISTRACTOR_3}}"}
                            ]
                        }
                    }
                }
            }
        }

    def initialize_student_profile(self, student_id: str, age: int, subjects: List[str]) -> StudentProfile:
        """
        Инициализирует профиль ученика для диагностики.

        Args:
            student_id: ID ученика
            age: Возраст ученика
            subjects: Список предметов для диагностики

        Returns:
            StudentProfile: Инициализированный профиль
        """
        profile = StudentProfile(
            student_id=student_id,
            age=age
        )

        # Инициализируем стартовые уровни для каждого предмета
        for subject in subjects:
            start_level = self._calculate_starting_level(age, subject)
            profile.current_difficulty[subject] = start_level
            profile.recommended_difficulty[subject] = start_level.value

            profile.subjects[subject] = {
                "current_level": start_level.value,
                "questions_asked": 0,
                "correct_answers": 0,
                "total_time_spent": 0,
                "confidence_score": 0.5,
                "strengths": [],
                "weaknesses": []
            }

        self.student_profiles[student_id] = profile
        return profile

    def _calculate_starting_level(self, age: int, subject: str) -> DifficultyLevel:
        """
        Рассчитывает начальный уровень сложности для ученика.

        Начинаем на 2 года младше возраста ученика.
        """
        effective_age = max(5, age + self.config["adaptation"]["age_adjustment"])

        if effective_age <= 7:
            return DifficultyLevel.BEGINNER
        elif effective_age <= 9:
            return DifficultyLevel.ELEMENTARY
        elif effective_age <= 12:
            return DifficultyLevel.INTERMEDIATE
        elif effective_age <= 15:
            return DifficultyLevel.ADVANCED
        else:
            return DifficultyLevel.EXPERT

    def generate_next_question(self, student_id: str, subject: str) -> Optional[DiagnosticQuestion]:
        """
        Генерирует следующий вопрос для ученика по предмету.

        Args:
            student_id: ID ученика
            subject: Предмет для вопроса

        Returns:
            DiagnosticQuestion или None если диагностика завершена
        """
        if student_id not in self.student_profiles:
            raise ValueError(f"Профиль ученика {student_id} не найден")

        profile = self.student_profiles[student_id]
        subject_data = profile.subjects.get(subject)

        if not subject_data:
            raise ValueError(f"Предмет {subject} не найден в профиле ученика")

        # Проверяем, не пора ли завершить диагностику
        if subject_data["questions_asked"] >= 8:
            return None

        current_level = DifficultyLevel(subject_data["current_level"])
        target_age = self._calculate_target_age(profile.age, current_level)

        # Генерируем вопрос
        question = self._generate_question(subject, target_age, current_level, profile)

        # Обновляем статистику
        subject_data["questions_asked"] += 1

        return question

    def _calculate_target_age(self, student_age: int, difficulty_level: DifficultyLevel) -> int:
        """Рассчитывает целевой возраст для вопроса на основе уровня сложности."""
        level_ages = {
            DifficultyLevel.BEGINNER: 6,
            DifficultyLevel.ELEMENTARY: 8,
            DifficultyLevel.INTERMEDIATE: 11,
            DifficultyLevel.ADVANCED: 14,
            DifficultyLevel.EXPERT: 16
        }

        base_age = level_ages.get(difficulty_level, student_age)
        return max(5, min(18, base_age))

    def _generate_question(self, subject: str, target_age: int,
                          difficulty_level: DifficultyLevel, profile: StudentProfile) -> DiagnosticQuestion:
        """
        Генерирует вопрос на основе шаблонов и профиля ученика.
        """
        question_id = f"diag_{subject.lower()}_{int(datetime.now().timestamp())}_{random.randint(1000, 9999)}"

        # Выбираем тип вопроса
        question_type = self._select_question_type(subject, profile)

        # Выбираем когнитивный домен
        cognitive_domain = self._select_cognitive_domain(difficulty_level, profile)

        # Генерируем контент вопроса
        content = self._generate_question_content(
            subject, target_age, difficulty_level, question_type, profile
        )

        # Настраиваем систему оценивания
        scoring = self._setup_scoring(question_type, difficulty_level)

        # Правила адаптации
        adaptation_rules = self._setup_adaptation_rules(difficulty_level, profile)

        # Психологический профиль
        psychological_profile = self._setup_psychological_profile(question_type)

        return DiagnosticQuestion(
            id=question_id,
            subject=subject,
            target_age=target_age,
            difficulty_level=difficulty_level,
            question_type=question_type,
            cognitive_domain=cognitive_domain,
            content=content,
            scoring=scoring,
            adaptation_rules=adaptation_rules,
            psychological_profile=psychological_profile,
            estimated_time_sec=self._estimate_time(difficulty_level, question_type)
        )

    def _select_question_type(self, subject: str, profile: StudentProfile) -> str:
        """Выбирает тип вопроса на основе предмета и профиля ученика."""
        # Если у нас мало информации о психологическом профиле, задаем диалоговые вопросы
        dialogue_questions_asked = sum(
            1 for q in profile.learning_history
            if q.get("question_type") == "dialogue"
        )

        if dialogue_questions_asked < self.config["psychological_profiling"]["dialogue_questions_count"]:
            return "dialogue"

        # Иначе выбираем обычные вопросы
        question_types = {
            "Mathematics": ["mcq_single", "numeric", "problem_solving"],
            "English": ["mcq_single", "short_text", "dialogue"],
            "Science": ["mcq_single", "short_text", "problem_solving"]
        }

        available_types = question_types.get(subject, ["mcq_single"])
        return random.choice(available_types)

    def _select_cognitive_domain(self, difficulty_level: DifficultyLevel,
                                profile: StudentProfile) -> CognitiveDomain:
        """Выбирает когнитивный домен по Блуму."""
        level_domains = {
            DifficultyLevel.BEGINNER: [CognitiveDomain.REMEMBER, CognitiveDomain.UNDERSTAND],
            DifficultyLevel.ELEMENTARY: [CognitiveDomain.UNDERSTAND, CognitiveDomain.APPLY],
            DifficultyLevel.INTERMEDIATE: [CognitiveDomain.APPLY, CognitiveDomain.ANALYZE],
            DifficultyLevel.ADVANCED: [CognitiveDomain.ANALYZE, CognitiveDomain.EVALUATE],
            DifficultyLevel.EXPERT: [CognitiveDomain.EVALUATE, CognitiveDomain.CREATE]
        }

        available_domains = level_domains.get(difficulty_level, [CognitiveDomain.UNDERSTAND])
        return random.choice(available_domains)

    def _generate_question_content(self, subject: str, target_age: int,
                                  difficulty_level: DifficultyLevel, question_type: str,
                                  profile: StudentProfile) -> Dict[str, Any]:
        """
        Генерирует контент вопроса на основе AI или шаблонов.
        """
        if AI_AVAILABLE and os.getenv('GROQ_API_KEY'):
            return self._generate_ai_question_content(
                subject, target_age, difficulty_level, question_type, profile
            )
        else:
            return self._generate_template_question_content(
                subject, target_age, difficulty_level, question_type
            )

    def _generate_ai_question_content(self, subject: str, target_age: int,
                                     difficulty_level: DifficultyLevel, question_type: str,
                                     profile: StudentProfile) -> Dict[str, Any]:
        """
        Генерирует контент вопроса с помощью AI.
        """
        prompt = self._create_ai_question_prompt(
            subject, target_age, difficulty_level, question_type, profile
        )

        try:
            import groq
            client = groq.Groq(api_key=os.getenv('GROQ_API_KEY'))

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=500
            )

            response = chat_completion.choices[0].message.content
            return self._parse_ai_question_response(response, question_type)

        except Exception as e:
            print(f"AI generation error: {e}")
            return self._generate_template_question_content(
                subject, target_age, difficulty_level, question_type
            )

    def _create_ai_question_prompt(self, subject: str, target_age: int,
                                  difficulty_level: DifficultyLevel, question_type: str,
                                  profile: StudentProfile) -> str:
        """
        Создает промпт для AI генерации вопроса.
        """
        level_descriptions = {
            DifficultyLevel.BEGINNER: "начальный уровень, базовые понятия",
            DifficultyLevel.ELEMENTARY: "элементарный уровень, простые операции",
            DifficultyLevel.INTERMEDIATE: "средний уровень, применение знаний",
            DifficultyLevel.ADVANCED: "продвинутый уровень, сложные задачи",
            DifficultyLevel.EXPERT: "экспертный уровень, творческие задачи"
        }

        if question_type == "dialogue":
            return f"""
Создай диалоговый вопрос для диагностики психологического профиля ученика {target_age} лет.

Цель: определить стиль общения, мотивацию, предпочтения в обучении.

Вопрос должен быть открытым, побуждающим к развернутому ответу.

Пример хорошего вопроса: "Расскажи о том, как ты обычно учишь новые слова в английском языке. Что тебе помогает лучше запомнить?"

Верни только текст вопроса.
"""
        else:
            return f"""
Создай диагностический вопрос по предмету "{subject}" для ребенка {target_age} лет.
Уровень сложности: {level_descriptions[difficulty_level]}
Тип вопроса: {question_type}

Требования:
1. Вопрос должен соответствовать возрасту и уровню сложности
2. Должен проверять фундаментальные знания по предмету
3. Должен иметь однозначный правильный ответ

{"Для MCQ вопроса верни 4 варианта ответа, где первый - правильный." if question_type == "mcq_single" else ""}
{"Для числового вопроса верни только число." if question_type == "numeric" else ""}
{"Для текстового вопроса верни ожидаемый ответ." if question_type == "short_text" else ""}

Формат ответа: JSON с полями "question" и "correct_answer"
"""

    def _parse_ai_question_response(self, response: str, question_type: str) -> Dict[str, Any]:
        """Парсит ответ AI и преобразует в структуру вопроса."""
        try:
            # Ищем JSON в ответе
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return {
                    "question": data.get("question", response.strip()),
                    "correct_answer": data.get("correct_answer"),
                    "options": data.get("options", [])
                }
        except:
            pass

        # Если не удалось распарсить, возвращаем простой формат
        return {
            "question": response.strip(),
            "correct_answer": "AI generated answer",
            "options": []
        }

    def _generate_template_question_content(self, subject: str, target_age: int,
                                           difficulty_level: DifficultyLevel,
                                           question_type: str) -> Dict[str, Any]:
        """
        Генерирует контент вопроса на основе шаблонов.
        """
        template = self.templates["diagnostic_templates"].get(question_type, {})
        structure = template.get("structure", {})

        if subject == "Mathematics":
            return self._generate_math_question(target_age, difficulty_level, question_type)
        elif subject == "English":
            return self._generate_english_question(target_age, difficulty_level, question_type)
        else:
            return self._generate_general_question(subject, target_age, difficulty_level, question_type)

    def _generate_math_question(self, target_age: int, difficulty_level: DifficultyLevel,
                               question_type: str) -> Dict[str, Any]:
        """Генерирует математический вопрос."""
        if question_type == "mcq_single":
            if difficulty_level == DifficultyLevel.BEGINNER:
                a, b = random.randint(1, 10), random.randint(1, 10)
                correct = a + b
                return {
                    "question": f"Сколько будет {a} + {b}?",
                    "options": [
                        {"text": str(correct), "is_correct": True},
                        {"text": str(correct + 1)},
                        {"text": str(correct - 1)},
                        {"text": str(correct + 2)}
                    ]
                }
            elif difficulty_level == DifficultyLevel.ELEMENTARY:
                a, b = random.randint(10, 50), random.randint(10, 50)
                operation = random.choice(['+', '-', '*'])
                if operation == '+':
                    correct = a + b
                    question = f"Сколько будет {a} + {b}?"
                elif operation == '-':
                    correct = a - b
                    question = f"Сколько будет {a} - {b}?"
                else:
                    a, b = random.randint(2, 12), random.randint(2, 10)
                    correct = a * b
                    question = f"Сколько будет {a} × {b}?"

                return {
                    "question": question,
                    "options": [
                        {"text": str(correct), "is_correct": True},
                        {"text": str(correct + random.randint(1, 5))},
                        {"text": str(correct - random.randint(1, 5))},
                        {"text": str(correct + random.randint(6, 10))}
                    ]
                }

        elif question_type == "numeric":
            a, b = random.randint(5, 20), random.randint(5, 20)
            correct = a * b
            return {
                "question": f"Вычисли {a} × {b}",
                "correct_answer": correct
            }

        return {"question": "Математический вопрос", "correct_answer": 42}

    def _generate_english_question(self, target_age: int, difficulty_level: DifficultyLevel,
                                  question_type: str) -> Dict[str, Any]:
        """Генерирует вопрос по английскому языку."""
        if question_type == "dialogue":
            questions = [
                "Расскажи о своем любимом английском слове. Почему оно тебе нравится?",
                "Как ты обычно запоминаешь новые английские слова?",
                "Что тебе больше нравится в английском: читать, писать или говорить?"
            ]
            return {
                "question": random.choice(questions),
                "instructions": "Ответь свободно, как ты думаешь"
            }

        elif question_type == "mcq_single":
            vocab_words = {
                "apple": ["фрукт", "машина", "животное", "цветок"],
                "house": ["дом", "машина", "дерево", "река"],
                "school": ["школа", "магазин", "парк", "библиотека"]
            }
            word, options = random.choice(list(vocab_words.items()))
            return {
                "question": f"Что означает слово '{word}'?",
                "options": [
                    {"text": options[0], "is_correct": True},
                    {"text": options[1]},
                    {"text": options[2]},
                    {"text": options[3]}
                ]
            }

        return {"question": "Английский вопрос", "correct_answer": "answer"}

    def _generate_general_question(self, subject: str, target_age: int,
                                  difficulty_level: DifficultyLevel, question_type: str) -> Dict[str, Any]:
        """Генерирует общий вопрос."""
        return {
            "question": f"Диагностический вопрос по предмету {subject} для {target_age} лет",
            "correct_answer": "зависит_от_предмета"
        }

    def _setup_scoring(self, question_type: str, difficulty_level: DifficultyLevel) -> Dict[str, Any]:
        """Настраивает систему оценивания для вопроса."""
        base_points = {
            DifficultyLevel.BEGINNER: 1,
            DifficultyLevel.ELEMENTARY: 1,
            DifficultyLevel.INTERMEDIATE: 2,
            DifficultyLevel.ADVANCED: 2,
            DifficultyLevel.EXPERT: 3
        }

        points = base_points.get(difficulty_level, 1)

        if question_type == "dialogue":
            return {
                "max_points": 1,
                "auto_grade": False,
                "evaluation_criteria": ["содержательность", "открытость", "мотивация"]
            }
        elif question_type == "problem_solving":
            return {
                "max_points": points,
                "auto_grade": False,
                "partial_credit": True,
                "criteria": ["правильность", "ход_мыслей", "творческий_подход"]
            }
        else:
            return {
                "max_points": points,
                "auto_grade": True,
                "partial_credit": False
            }

    def _setup_adaptation_rules(self, difficulty_level: DifficultyLevel,
                               profile: StudentProfile) -> Dict[str, Any]:
        """Настраивает правила адаптации сложности."""
        return {
            "correct_streak_threshold": self.config["adaptation"]["correct_streak_threshold"],
            "incorrect_streak_threshold": self.config["adaptation"]["incorrect_streak_threshold"],
            "difficulty_increase_on_correct": True,
            "difficulty_decrease_on_incorrect": True,
            "age_adjustment_range": {
                "min": profile.age + self.config["adaptation"]["min_age_decline"],
                "max": profile.age + self.config["adaptation"]["max_age_advance"]
            }
        }

    def _setup_psychological_profile(self, question_type: str) -> Dict[str, Any]:
        """Настраивает психологический профиль для вопроса."""
        if question_type == "dialogue":
            return {
                "communication_style": "to_be_analyzed",
                "learning_style": "to_be_analyzed",
                "motivation_type": "to_be_analyzed",
                "personality_traits": "to_be_analyzed"
            }
        else:
            return {
                "cognitive_style": "logical_analytical",
                "response_pattern": "direct_answer"
            }

    def _estimate_time(self, difficulty_level: DifficultyLevel, question_type: str) -> int:
        """Оценивает время на ответ."""
        base_times = {
            DifficultyLevel.BEGINNER: 30,
            DifficultyLevel.ELEMENTARY: 45,
            DifficultyLevel.INTERMEDIATE: 60,
            DifficultyLevel.ADVANCED: 90,
            DifficultyLevel.EXPERT: 120
        }

        base_time = base_times.get(difficulty_level, 60)

        if question_type == "dialogue":
            return base_time * 2
        elif question_type == "problem_solving":
            return base_time * 3
        else:
            return base_time

    def process_answer(self, student_id: str, question_id: str, answer: Dict[str, Any],
                      time_spent_sec: int, profile: StudentProfile) -> Dict[str, Any]:
        """
        Обрабатывает ответ ученика и адаптирует сложность.

        Returns:
            Результат обработки ответа
        """
        subject_data = None
        for subj_data in profile.subjects.values():
            subject_data = subj_data
            break

        if not subject_data:
            return {"error": "Данные по предмету не найдены"}

        # Оцениваем ответ
        is_correct = self._evaluate_answer(answer, subject_data)

        # Обновляем статистику
        subject_data["correct_answers"] += 1 if is_correct else 0
        subject_data["total_time_spent"] += time_spent_sec

        # Адаптируем сложность
        new_level = self._adapt_difficulty(
            profile, list(profile.subjects.keys())[0], is_correct, time_spent_sec
        )

        # Анализируем психологический профиль
        if answer.get("question_type") == "dialogue":
            self._analyze_psychological_profile(profile, answer)

        return {
            "is_correct": is_correct,
            "new_difficulty_level": new_level.value,
            "confidence_score": subject_data["confidence_score"],
            "next_question_recommended": True
        }

    def _evaluate_answer(self, answer: Dict[str, Any], subject_data: Dict[str, Any]) -> bool:
        """Оценивает правильность ответа."""
        # Простая заглушка - в реальности нужна более сложная логика
        if "selected_option" in answer:
            return answer["selected_option"] == 0  # Предполагаем, что первый вариант правильный
        elif "answer" in answer:
            return len(str(answer["answer"]).strip()) > 0
        return False

    def _adapt_difficulty(self, profile: StudentProfile, subject: str,
                         is_correct: bool, time_spent_sec: int) -> DifficultyLevel:
        """
        Адаптирует уровень сложности на основе ответа ученика.
        """
        current_level = DifficultyLevel(profile.current_difficulty[subject])
        subject_data = profile.subjects[subject]

        # Простая логика адаптации
        levels = list(DifficultyLevel)
        current_index = levels.index(current_level)

        new_index = current_index  # По умолчанию сохраняем текущий уровень

        if is_correct:
            subject_data["correct_streak"] = subject_data.get("correct_streak", 0) + 1
            if subject_data["correct_streak"] >= 3:
                new_index = min(current_index + 1, len(levels) - 1)
                subject_data["correct_streak"] = 0
        else:
            subject_data["incorrect_streak"] = subject_data.get("incorrect_streak", 0) + 1
            if subject_data["incorrect_streak"] >= 2:
                new_index = max(current_index - 1, 0)
                subject_data["incorrect_streak"] = 0
            # Если неправильный ответ, но streak < 2, сохраняем текущий уровень

        new_level = levels[new_index]
        profile.current_difficulty[subject] = new_level
        subject_data["current_level"] = new_level.value

        return new_level

    def _analyze_psychological_profile(self, profile: StudentProfile, answer: Dict[str, Any]):
        """
        Анализирует психологический профиль на основе диалогового ответа.
        """
        response_text = str(answer.get("answer", "")).lower()

        # Простой анализ стиля общения
        if any(word in response_text for word in ["думаю", "считаю", "мне кажется"]):
            profile.psychological_profile["communication_style"] = "analytical"
        elif any(word in response_text for word in ["круто", "классно", "здорово"]):
            profile.psychological_profile["communication_style"] = "enthusiastic"
        else:
            profile.psychological_profile["communication_style"] = "neutral"

        # Анализ мотивации
        if any(word in response_text for word in ["хочу", "мечтаю", "стремлюсь"]):
            profile.psychological_profile["motivation_type"] = "achievement"
        elif any(word in response_text for word in ["интересно", "узнать", "понять"]):
            profile.psychological_profile["motivation_type"] = "mastery"

    def generate_learning_plan(self, student_id: str) -> Dict[str, Any]:
        """
        Генерирует индивидуальный план обучения на основе диагностики.
        """
        if student_id not in self.student_profiles:
            raise ValueError(f"Профиль ученика {student_id} не найден")

        profile = self.student_profiles[student_id]

        # Анализируем сильные и слабые стороны
        strengths = []
        weaknesses = []

        for subject, data in profile.subjects.items():
            accuracy = data["correct_answers"] / max(data["questions_asked"], 1)
            avg_time = data["total_time_spent"] / max(data["questions_asked"], 1)

            if accuracy > 0.8:
                strengths.append(f"Высокая точность в {subject}")
            elif accuracy < 0.6:
                weaknesses.append(f"Низкая точность в {subject}")

            if avg_time < 45:
                strengths.append(f"Быстрое решение задач в {subject}")
            elif avg_time > 90:
                weaknesses.append(f"Медленное решение задач в {subject}")

        # Создаем план обучения
        learning_plan = {
            "student_id": student_id,
            "age": profile.age,
            "assessment_date": datetime.now().isoformat(),
            "overall_level": "intermediate",  # Заглушка
            "subject_breakdown": profile.subjects,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "psychological_profile": profile.psychological_profile,
            "recommendations": {
                "immediate_focus": weaknesses[:2],
                "long_term_goals": strengths,
                "study_schedule": {
                    "daily_time": 45,
                    "preferred_subjects": [subj for subj, data in profile.subjects.items()
                                         if data["correct_answers"] / max(data["questions_asked"], 1) > 0.7]
                },
                "teaching_approach": self._recommend_teaching_approach(profile)
            }
        }

        return learning_plan

    def _recommend_teaching_approach(self, profile: StudentProfile) -> str:
        """Рекомендует подход к обучению на основе профиля."""
        comm_style = profile.psychological_profile.get("communication_style", "neutral")

        if comm_style == "analytical":
            return "структурированный подход с объяснением логики"
        elif comm_style == "enthusiastic":
            return "игровой подход с элементами соревнования"
        else:
            return "сбалансированный подход с визуальными материалами"


# Глобальный экземпляр умной диагностической системы
smart_diagnostic_system = SmartDiagnosticSystem()
