#!/usr/bin/env python3
"""
Демонстрация работы системы mastery в Ayaal Teacher.

Показывает полный цикл: от ответа ученика до обновления прогресса.
"""

import json
from mastery_calculator import (
    MasteryCalculatorV2,
    calculate_lesson_mastery_v2,
    update_learning_mastery_v2,
    next_lesson_recommendation_v2,
    get_mastery_description
)


def simulate_student_progress():
    """Симуляция прогресса ученика по модулю математики."""
    print("🎓 Демонстрация прогресса ученика по модулю 'Математика - Числа'\n")

    # Инициализация состояния
    current_mastery = {
        'overall': 0.0,
        'concept': 0.0,
        'guided': 0.0,
        'independent': 0.0,
        'assessment': 0.0,
        'last_updated': '2024-01-01T09:00:00Z',
        'total_submissions': 0
    }

    # Симуляция уроков и ответов ученика
    lessons_scenario = [
        {
            'lesson_type': 'concept',
            'lesson_name': 'Что такое числа?',
            'time_spent': 180,  # 3 минуты
            'score': 0.85,      # Отличный результат
            'difficulty': 'easy',
            'description': 'Ученик быстро понял основы'
        },
        {
            'lesson_type': 'guided',
            'lesson_name': 'Сложение однозначных чисел',
            'time_spent': 420,  # 7 минут
            'score': 0.75,      # Хороший результат
            'difficulty': 'medium',
            'description': 'Немного времени на размышления'
        },
        {
            'lesson_type': 'guided',
            'lesson_name': 'Вычитание в пределах 10',
            'time_spent': 600,  # 10 минут
            'score': 0.65,      # Средний результат
            'difficulty': 'medium',
            'description': 'Были трудности с некоторыми примерами'
        },
        {
            'lesson_type': 'independent',
            'lesson_name': 'Самостоятельное решение примеров',
            'time_spent': 480,  # 8 минут
            'score': 0.80,      # Очень хороший результат
            'difficulty': 'medium',
            'description': 'Ученик справился самостоятельно!'
        }
    ]

    # История предыдущих ответов (пустая в начале)
    submissions_history = []

    for i, lesson in enumerate(lessons_scenario, 1):
        print(f"📚 Урок {i}: {lesson['lesson_name']}")
        print(f"   Тип: {lesson['lesson_type']}")
        print(f"   Время: {lesson['time_spent']} сек ({lesson['time_spent']//60} мин)")
        print(f"   Оценка: {lesson['score']:.0%}")
        print(f"   Сложность: {lesson['difficulty']}")
        print(f"   Описание: {lesson['description']}")

        # Рассчитываем mastery для этого урока
        lesson_mastery, diagnostics = calculate_lesson_mastery_v2(
            submissions_history,
            lesson['lesson_type'],
            lesson['time_spent'],
            lesson['score'],
            lesson['difficulty']
        )

        # Обновляем общее состояние mastery
        current_mastery = update_learning_mastery_v2(
            current_mastery,
            lesson['lesson_type'],
            lesson_mastery,
            len(submissions_history) + 1
        )

        # Добавляем этот ответ в историю
        submissions_history.append({
            'score': lesson['score'],
            'created_at': f'2024-01-{i:02d}T10:00:00Z',
            'lesson_type': lesson['lesson_type']
        })

        # Определяем следующий рекомендуемый урок
        next_lesson, recommendation_reason = next_lesson_recommendation_v2(current_mastery, {}, {})

        # Описание текущего уровня
        mastery_desc = get_mastery_description(current_mastery['overall'])

        print("\n🎯 Результаты:")
        print(f"   Mastery урока: {lesson_mastery:.3f}")
        print(f"   Диагностика: точность={diagnostics['accuracy']:.2f}, скорость={diagnostics['speed']:.2f}, последовательность={diagnostics['consistency']:.2f}")
        print(f"   Общий mastery: {current_mastery['overall']:.3f} ({mastery_desc})")
        print(f"   Рекомендуемый следующий урок: {next_lesson}")
        print(f"   Причина рекомендации: {recommendation_reason}")
        print(f"   Детали по типам: Concept: {current_mastery['concept']:.2f}, Guided: {current_mastery['guided']:.2f}, Independent: {current_mastery['independent']:.2f}")
        print("   ───────────────────────────────────")
        print()


def show_mastery_levels():
    """Показать все уровни mastery с описаниями."""
    print("🏆 Уровни освоения (Mastery Levels):\n")

    test_scores = [0.1, 0.3, 0.5, 0.7, 0.85, 0.95]

    for score in test_scores:
        description = get_mastery_description(score)
        level = "🔴 Начинающий" if score < 0.4 else "🟡 Новичок" if score < 0.6 else "🟢 Средний" if score < 0.8 else "🔵 Продвинутый" if score < 0.9 else "🏆 Мастер"
        print(f"   {score:.1f} - {description} ({level})")

    print()


def demonstrate_adaptive_learning():
    """Демонстрация адаптивного обучения."""
    print("🧠 Адаптивное обучение - как система подстраивается:\n")

    scenarios = [
        {
            'student_type': 'Быстрый ученик',
            'mastery': {'overall': 0.9, 'concept': 0.95, 'guided': 0.9, 'independent': 0.85},
            'description': 'Ученик быстро схватывает материал'
        },
        {
            'student_type': 'Нуждается в поддержке',
            'mastery': {'overall': 0.4, 'concept': 0.6, 'guided': 0.3, 'independent': 0.2},
            'description': 'Ученику нужна дополнительная помощь'
        },
        {
            'student_type': 'Смешанный тип',
            'mastery': {'overall': 0.7, 'concept': 0.9, 'guided': 0.8, 'independent': 0.5},
            'description': 'Теорию понимает, но практика вызывает трудности'
        }
    ]

    for scenario in scenarios:
        next_lesson, reason = next_lesson_recommendation_v2(scenario['mastery'], {}, {})
        mastery_desc = get_mastery_description(scenario['mastery']['overall'])

        print(f"👤 {scenario['student_type']}:")
        print(f"   Общий уровень: {scenario['mastery']['overall']:.1f} ({mastery_desc})")
        print(f"   Ситуация: {scenario['description']}")
        print(f"   Рекомендация: {next_lesson} урок")
        print(f"   Причина: {reason}")
        print()


def main():
    """Основная демонстрация."""
    print("🚀 Демонстрация системы Mastery в Ayaal Teacher\n")
    print("=" * 60)

    show_mastery_levels()
    simulate_student_progress()
    demonstrate_adaptive_learning()

    print("🎉 Демонстрация завершена!")
    print("\n💡 Ключевые особенности системы:")
    print("   • Многофакторный расчет (точность, скорость, последовательность, сложность)")
    print("   • Адаптивные рекомендации следующего урока")
    print("   • Отслеживание прогресса по типам уроков")
    print("   • Мотивационные уровни и описания")
    print("   • Интеграция с базой данных для сохранения прогресса")


if __name__ == "__main__":
    main()
