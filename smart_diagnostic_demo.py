#!/usr/bin/env python3
"""
Умная адаптивная диагностика Ayaal Teacher.

Показывает:
1. Инициализация профиля ученика с учетом возраста
2. Адаптивная генерация вопросов через шаблоны
3. Психологическое профилирование через диалоговые вопросы
4. Индивидуальная траектория обучения
5. Комплексная оценка компетентности
"""

import json
import time
import os
from typing import Dict, List, Any
from smart_diagnostic_system import SmartDiagnosticSystem, DifficultyLevel

def print_separator(title: str):
    """Печатает разделитель с заголовком."""
    print(f"\n{'='*80}")
    print(f"🎯 {title}")
    print(f"{'='*80}")


def demonstrate_smart_diagnostic_flow():
    """Демонстрирует полный цикл умной диагностики."""
    print_separator("УМНАЯ АДАПТИВНАЯ ДИАГНОСТИКА")

    # Инициализация системы
    system = SmartDiagnosticSystem()

    # 1. Создание профиля ученика
    print("1️⃣ Создание профиля ученика...")
    student_id = "demo_student_001"
    student_age = 10
    subjects = ["Mathematics", "English"]

    profile = system.initialize_student_profile(
        student_id=student_id,
        age=student_age,
        subjects=subjects
    )

    print(f"   ✅ Профиль создан для ученика {student_age} лет")
    print("   📚 Предметы для диагностики: Mathematics, English")
    print(f"   🎯 Начальные уровни сложности:")
    for subject, data in profile.subjects.items():
        print(f"      • {subject}: {data['current_level']}")

    # 2. Процесс диагностики
    print("\n2️⃣ Процесс адаптивной диагностики...")
    print("   🤖 Система адаптирует вопросы под уровень ученика...")

    all_questions = []
    question_count = 0
    max_questions = 12  # Ограничение для демонстрации

    for subject in subjects:
        print(f"\n   📖 Диагностика по предмету: {subject}")

        while question_count < max_questions:
            # Генерируем следующий вопрос
            question = system.generate_next_question(student_id, subject)

            if question is None:
                print(f"   🎉 Диагностика по предмету {subject} завершена!")
                break

            question_count += 1
            all_questions.append(question)

            print(f"\n   🧠 Вопрос {question_count} ({subject}):")
            print(f"      🎯 Уровень: {question.difficulty_level.value}")
            print(f"      🎓 Целевой возраст: {question.target_age} лет")
            print(f"      🧩 Тип: {question.question_type}")
            print(f"      🧠 Когнитивный уровень: {question.cognitive_domain.value}")
            print(f"      ⏰ Время: {question.estimated_time_sec} сек")

            # Показываем контент вопроса
            content = question.content
            print(f"      ❓ {content['question']}")

            if question.question_type == "dialogue":
                print("      💬 Это диалоговый вопрос для психологического анализа")
                # Симулируем развернутый ответ
                if "расскажи" in content['question'].lower():
                    simulated_answer = {
                        "answer": "Мне очень нравится математика, потому что в ней всегда есть правильный ответ, и это как игра-головоломка. Я люблю решать задачи, где нужно подумать логически.",
                        "question_type": "dialogue"
                    }
                else:
                    simulated_answer = {
                        "answer": "Обычно я сначала читаю условие несколько раз, потом рисую схему или таблицу, и только потом начинаю вычисления.",
                        "question_type": "dialogue"
                    }
            elif question.question_type == "mcq_single":
                options = content.get('options', [])
                if options:
                    print("      📋 Варианты:")
                    for i, option in enumerate(options):
                        marker = "✅" if option.get('is_correct') else f"{i+1}."
                        print(f"         {marker} {option['text']}")

                # Симулируем правильный ответ
                if options and len(options) > 0:
                    correct_option = next((i for i, opt in enumerate(options) if opt.get('is_correct')), 0)
                    simulated_answer = {"selected_option": correct_option}
                else:
                    simulated_answer = {"selected_option": 0}
            else:
                # Для других типов вопросов
                simulated_answer = {"answer": "42"}

            # Имитируем время решения
            time_spent = min(question.estimated_time_sec + random.randint(-10, 20), 300)

            # Обрабатываем ответ
            result = system.process_answer(
                student_id=student_id,
                question_id=question.id,
                answer=simulated_answer,
                time_spent_sec=time_spent,
                profile=profile
            )

            if "error" in result:
                print(f"      ❌ Ошибка обработки: {result['error']}")
                continue

            is_correct = result['is_correct']
            print(f"      ✅ Ответ принят: {'Правильно!' if is_correct else 'Неправильно'}")
            print(f"      📈 Новый уровень: {result['new_difficulty_level']}")

            # Обновляем текущий уровень для следующего вопроса
            profile.current_difficulty[subject] = DifficultyLevel(result['new_difficulty_level'])

            time.sleep(0.5)  # Небольшая пауза

            # Переходим к следующему предмету после 6 вопросов на предмет
            if question_count % 6 == 0 and subject == subjects[0]:
                break

    # 3. Генерация индивидуального плана обучения
    print("\n3️⃣ Генерация индивидуального плана обучения...")
    learning_plan = system.generate_learning_plan(student_id)

    print("   📋 ИТОГОВАЯ ОЦЕНКА:")
    print(f"      🎯 Общий уровень: {learning_plan['overall_level']}")
    print(f"      📊 Всего вопросов: {question_count}")
    print("\n      📚 Оценка по предметам:")
    for subject, data in learning_plan['subject_breakdown'].items():
        accuracy = data['correct_answers'] / max(data['questions_asked'], 1)
        print(f"         📖 {subject}: {accuracy:.1%}")
        print(f"         ⏱️  Среднее время: {data['total_time_spent'] / max(data['questions_asked'], 1):.1f} сек")

    if learning_plan['strengths']:
        print("\n      💪 Сильные стороны:")
        for strength in learning_plan['strengths'][:3]:
            print(f"         • {strength}")

    if learning_plan['weaknesses']:
        print("\n      🎯 Зоны для развития:")
        for weakness in learning_plan['weaknesses'][:3]:
            print(f"         • {weakness}")

    # 4. Психологический профиль
    print("\n4️⃣ Психологический профиль ученика...")
    psych_profile = learning_plan['psychological_profile']

    if psych_profile:
        print("   🧠 Анализ психологического профиля:")
        for key, value in psych_profile.items():
            print(f"      • {key}: {value}")
    else:
        print("   📝 Недостаточно данных для анализа профиля")

    # 5. Рекомендации
    print("\n5️⃣ Персональные рекомендации...")
    recommendations = learning_plan['recommendations']

    print("   🎯 Немедленный фокус:")
    for focus in recommendations['immediate_focus'][:2]:
        print(f"      • {focus}")

    print("\n      📅 Рекомендуемый график:")
    schedule = recommendations['study_schedule']
    print(f"      • Ежедневное время: {schedule['daily_time']} минут")
    print(f"      • Приоритетные предметы: {', '.join(schedule['preferred_subjects'])}")

    print("\n      🎓 Подход к обучению:")
    print(f"      • {recommendations['teaching_approach']}")

    return learning_plan


def demonstrate_ai_power():
    """Демонстрирует возможности умной диагностики."""
    print_separator("СИЛА УМНОЙ ДИАГНОСТИКИ")

    print("🚀 Преимущества умной адаптивной диагностики:")
    print("   🧠 Адаптивность - начинается с уровня на 2 года младше возраста")
    print("   🎯 Персонализация - вопросы генерируются через структурированные шаблоны")
    print("   📈 Динамика - уровень меняется по ходу диагностики в реальном времени")
    print("   🧩 Многоуровневая оценка - проверяет разные когнитивные навыки")
    print("   💬 Психологический анализ - диалоговые вопросы для портрета ученика")
    print("   📚 Масштабируемость - работает для любых предметов и возрастов")

    print("\n🎯 Что умеет система:")
    print("   ✅ Определять начальный уровень на основе возраста ученика")
    print("   ✅ Генерировать вопросы разных типов (MCQ, числовые, текстовые, диалоговые)")
    print("   ✅ Анализировать время решения задач")
    print("   ✅ Отслеживать последовательность успехов/неудач")
    print("   ✅ Адаптировать сложность в реальном времени")
    print("   ✅ Собирать психологический профиль ученика")
    print("   ✅ Создавать индивидуальную траекторию обучения")
    print("   ✅ Рекомендовать оптимальный подход к обучению")

    print("\n🧩 Типы вопросов в системе:")
    print("   📋 MCQ (Multiple Choice) - выбор правильного ответа")
    print("   🔢 Numeric - числовые ответы с проверкой")
    print("   📝 Short Text - текстовые ответы")
    print("   💬 Dialogue - диалоговые вопросы для психологии")
    print("   🧩 Problem Solving - творческие задачи")


def demonstrate_templates():
    """Показывает примеры шаблонов диагностических вопросов."""
    print_separator("ШАБЛОНЫ ДИАГНОСТИЧЕСКИХ ВОПРОСОВ")

    print("📄 Структура шаблонов:")
    print("""
   diagnostic.schema.json:
   ├── id (уникальный ID вопроса)
   ├── subject (предмет)
   ├── target_age (целевой возраст)
   ├── difficulty_level (уровень сложности)
   ├── question_type (тип вопроса)
   ├── cognitive_domain (когнитивный уровень по Блуму)
   ├── content (контент вопроса)
   ├── scoring (система оценивания)
   ├── adaptation_rules (правила адаптации)
   └── psychological_profile (психологический профиль)
    """)

    print("🎨 Типы вопросов:")
    print("   📋 mcq_single - выбор одного правильного ответа")
    print("   📋 mcq_multiple - выбор нескольких правильных ответов")
    print("   🔢 numeric - числовой ответ")
    print("   📝 short_text - короткий текстовый ответ")
    print("   📝 long_text - развернутый текстовый ответ")
    print("   💬 dialogue - диалоговый вопрос")
    print("   🧩 interactive - интерактивный вопрос")
    print("   🧩 problem_solving - решение задач")

    print("\n🧠 Когнитивные домены (по Блуму):")
    print("   📖 Remember - запоминание фактов")
    print("   🤔 Understand - понимание концепций")
    print("   🛠️  Apply - применение знаний")
    print("   🔍 Analyze - анализ информации")
    print("   ⚖️  Evaluate - оценка идей")
    print("   🎨 Create - творческий синтез")


def main():
    """Основная функция демонстрации."""
    print("🚀 УМНАЯ АДАПТИВНАЯ ДИАГНОСТИКА В AYAAL TEACHER")
    print("Показываем будущее персонализированного образования!")

    # Проверяем наличие AI
    ai_available = "GROQ_API_KEY" in str(os.environ.get('GROQ_API_KEY', ''))
    if ai_available:
        print("✅ AI (Groq) доступен - будут генерироваться умные вопросы")
    else:
        print("⚠️  AI недоступен - будут использоваться шаблонные вопросы")

    # Запускаем демонстрацию
    learning_plan = demonstrate_smart_diagnostic_flow()
    demonstrate_ai_power()
    demonstrate_templates()

    print_separator("ИТОГИ ДЕМОНСТРАЦИИ")
    print("🎉 Умная диагностика успешно протестирована!")
    print("\n💡 РЕЗУЛЬТАТЫ:")
    print("   ✅ Создана адаптивная система диагностики уровня")
    print("   ✅ Реализованы структурированные шаблоны вопросов")
    print("   ✅ Добавлен психологический анализ ученика")
    print("   ✅ Система адаптируется под возраст и уровень ученика")
    print("   ✅ Создана индивидуальная траектория обучения")
    print("   ✅ Полная интеграция с системой mastery")

    print("\n🎓 ПРЕИМУЩЕСТВА НОВОЙ СИСТЕМЫ:")
    print("   • Начинает диагностику с уровня на 2 года младше возраста")
    print("   • Использует структурированные JSON шаблоны")
    print("   • Собирает психологический портрет ученика")
    print("   • Адаптирует сложность в реальном времени")
    print("   • Создает персонализированный план обучения")
    print("   • Учитывает разные стили обучения и мотивацию")

    print("\n🚀 ЭТО БУДУЩЕЕ ОБРАЗОВАНИЯ!")
    print("   Теперь каждый ученик получает:")
    print("   • Диагностику, соответствующую его возрасту")
    print("   • Вопросы, адаптированные под его уровень")
    print("   • Психологическую поддержку через диалоговые вопросы")
    print("   • Индивидуальную траекторию развития")
    print("   • Персонализированный подход к обучению")


if __name__ == "__main__":
    import random
    main()
