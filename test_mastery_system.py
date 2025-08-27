#!/usr/bin/env python3
"""
Тест системы расчета mastery.

Запуск: python test_mastery_system.py
"""

import json
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

from mastery_calculator import (
    MasteryCalculatorV2,
    calculate_lesson_mastery_v2,
    update_learning_mastery_v2,
    next_lesson_recommendation_v2,
    get_mastery_description
)


def test_mastery_calculator():
    """Тест калькулятора mastery."""
    print("🧮 Тестирование калькулятора mastery...")

    calculator = MasteryCalculatorV2()

    # Тестовые данные
    submissions_history = [
        {
            'score': 0.8,
            'created_at': '2024-01-01T10:00:00Z',
            'lesson_type': 'concept'
        },
        {
            'score': 0.9,
            'created_at': '2024-01-02T10:00:00Z',
            'lesson_type': 'guided'
        },
        {
            'score': 0.7,
            'created_at': '2024-01-03T10:00:00Z',
            'lesson_type': 'guided'
        }
    ]

    # Тест расчета mastery для разных сценариев
    scenarios = [
        {
            'lesson_type': 'concept',
            'time_spent': 250,  # 4 минуты - быстро
            'score': 0.9,       # Отличный результат
            'difficulty': 'medium',
            'expected_mastery': 0.8  # Высокий уровень
        },
        {
            'lesson_type': 'guided',
            'time_spent': 700,  # 11 минут - долго
            'score': 0.6,       # Средний результат
            'difficulty': 'hard',
            'expected_mastery': 0.4  # Средний уровень
        },
        {
            'lesson_type': 'independent',
            'time_spent': 1200, # 20 минут - очень долго
            'score': 0.3,       # Плохой результат
            'difficulty': 'easy',
            'expected_mastery': 0.2  # Низкий уровень
        }
    ]

    for i, scenario in enumerate(scenarios):
        mastery, diagnostics = calculator.lesson_mastery(
            submissions_history,
            scenario['lesson_type'],
            scenario['time_spent'],
            scenario['score'],
            scenario['difficulty']
        )

        print(f"  Тест {i+1}: {scenario['lesson_type']} урок")
        print(f"    Время: {scenario['time_spent']} сек, Оценка: {scenario['score']}")
        print(f"    Полученный mastery: {mastery:.3f}")
        print(f"    Диагностика: {diagnostics}")
        print()


def test_mastery_update():
    """Тест обновления состояния mastery."""
    print("📊 Тестирование обновления mastery...")

    # Начальное состояние
    initial_mastery = {
        'overall': 0.0,
        'concept': 0.0,
        'guided': 0.0,
        'independent': 0.0,
        'assessment': 0.0
    }

    # Симуляция нескольких ответов
    updates = [
        ('concept', 0.8, 5),
        ('guided', 0.7, 6),
        ('guided', 0.9, 7),
        ('independent', 0.6, 8)
    ]

    current_mastery = initial_mastery.copy()

    for lesson_type, lesson_mastery, submissions_count in updates:
        current_mastery = update_learning_mastery_v2(
            current_mastery, lesson_type, lesson_mastery, submissions_count
        )

        print(f"  После {lesson_type} урока:")
        print(f"    Общий mastery: {current_mastery['overall']}")
        print(f"    Детали: {current_mastery}")
        print()


def test_next_lesson_recommendation():
    """Тест рекомендации следующего урока."""
    print("🎯 Тестирование рекомендации следующего урока...")

    test_cases = [
        {
            'mastery': {'overall': 0.2, 'concept': 0.3, 'guided': 0.0},
            'name': 'Начинающий ученик'
        },
        {
            'mastery': {'overall': 0.5, 'concept': 0.9, 'guided': 0.6},
            'name': 'Средний уровень'
        },
        {
            'mastery': {'overall': 0.8, 'concept': 0.9, 'guided': 0.9, 'independent': 0.7},
            'name': 'Продвинутый ученик'
        }
    ]

    for case in test_cases:
        next_type, reason = next_lesson_recommendation_v2(
            case['mastery'], {}, {}  # Пустая политика и счетчики
        )

        description = get_mastery_description(case['mastery']['overall'])

        print(f"  {case['name']}:")
        print(f"    Mastery: {case['mastery']['overall']} ({description})")
        print(f"    Рекомендуемый урок: {next_type}")
        print(f"    Причина: {reason}")
        print()


def test_api_integration():
    """Тест интеграции с API (если сервер запущен)."""
    print("🌐 Тестирование API интеграции...")

    if not HAS_REQUESTS:
        print("  ⚠️  Модуль requests не установлен - пропускаем API тест")
        return

    try:
        # Проверка здоровья API
        response = requests.get('http://localhost:3000/api/health', timeout=2)
        if response.status_code == 200:
            print("  ✅ API сервер запущен")

            # Тест получения статистики mastery
            test_student_id = "95ef01b7-ebfd-4320-a41b-9550e88551b5"
            response = requests.get(f'http://localhost:3000/api/mastery/{test_student_id}', timeout=5)

            if response.status_code == 200:
                data = response.json()
                print("  ✅ API mastery работает")
                print(f"    Модулей: {data['summary']['total_modules']}")
                print(f"    Средний mastery: {data['summary']['average_mastery']:.3f}")
            else:
                print(f"  ⚠️  API mastery вернул код: {response.status_code}")
        else:
            print("  ❌ API сервер не запущен")

    except requests.exceptions.RequestException:
        print("  ❌ API сервер не доступен")


def main():
    """Основная функция тестирования."""
    print("🚀 Запуск тестов системы mastery\n")

    test_mastery_calculator()
    test_mastery_update()
    test_next_lesson_recommendation()
    test_api_integration()

    print("✅ Все тесты завершены!")


if __name__ == "__main__":
    main()
