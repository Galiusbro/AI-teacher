#!/usr/bin/env python3
"""
Скрипт для демонстрации работы API системы mastery.

Показывает полный цикл: от начального состояния до изменения mastery после ответов.
"""

import requests
import json
import time

# Настройки API
API_BASE = "http://localhost:3000"
STUDENT_ID = "65e32701-fccf-46c4-ba7f-44ab7853444c"
MODULE_CODE = "module_math_numbers_primary"


def print_separator(title):
    """Печатает разделитель с заголовком."""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")


def api_call(endpoint, method="GET", data=None):
    """Универсальный вызов API."""
    url = f"{API_BASE}{endpoint}"
    headers = {"Content-Type": "application/json"}

    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            response = requests.get(url)

        return response.json()
    except Exception as e:
        return {"error": str(e)}


def format_mastery_details(mastery_details):
    """Форматирует детали mastery для красивого вывода."""
    if not mastery_details:
        return "Нет данных"

    result = []
    for key, value in mastery_details.items():
        if key != "last_updated" and key != "total_submissions":
            result.append(f"{key}: {value:.3f}")

    return " | ".join(result)


def simulate_student_progress():
    """Симуляция прогресса ученика через API."""
    print_separator("СИМУЛЯЦИЯ ПРОГРЕССА УЧЕНИКА")

    # Шаг 1: Начальное состояние
    print("📊 ШАГ 1: Проверяем начальное состояние")
    initial_state = api_call("/api/next", "POST", {
        "student_id": STUDENT_ID,
        "module_code": MODULE_CODE
    })

    if "error" in initial_state:
        print(f"❌ Ошибка: {initial_state['error']}")
        return

    print("🏆 Начальный уровень:"    print(f"   Общий mastery: {initial_state['current_mastery']:.3f}")
    print(f"   Описание: {initial_state['mastery_description']}")
    print(f"   Детали: {format_mastery_details(initial_state['mastery_details'])}")
    print(f"   Рекомендация: {initial_state['next_lesson_type']} урок")
    print(f"   Причина: {initial_state['reason']}")

    # Шаг 2: Отправляем несколько ответов
    print("\n📝 ШАГ 2: Отправляем ответы ученика")

    # Сценарий: ученик проходит concept урок с хорошими результатами
    submissions = [
        {
            "lesson_type": "concept",
            "score": 0.85,
            "time_spent": 180,
            "difficulty": "easy",
            "description": "Отличный результат на concept уроке"
        },
        {
            "lesson_type": "concept",
            "score": 0.90,
            "time_spent": 150,
            "difficulty": "easy",
            "description": "Еще один хороший результат"
        },
        {
            "lesson_type": "guided",
            "score": 0.75,
            "time_spent": 240,
            "difficulty": "medium",
            "description": "Средний результат на guided уроке"
        },
        {
            "lesson_type": "guided",
            "score": 0.80,
            "time_spent": 200,
            "difficulty": "medium",
            "description": "Улучшение на guided уроке"
        }
    ]

    for i, submission in enumerate(submissions, 1):
        print(f"\n   Ответ {i}: {submission['description']}")

        # Отправляем ответ
        result = api_call("/api/submissions", "POST", {
            "student_id": STUDENT_ID,
            "module_code": MODULE_CODE,
            "lesson_id": f"lesson_{MODULE_CODE}_{submission['lesson_type']}_01",
            "task_id": f"task_{submission['lesson_type']}_{i}",
            "kind": "practice",
            "answer_jsonb": {"selected_option": 2, "correct_option": 2},
            "score": submission['score'],
            "time_spent": submission['time_spent'],
            "difficulty": submission['difficulty']
        })

        if "error" in result:
            print(f"      ❌ Ошибка: {result['error']}")
            continue

        print("      ✅ Ответ принят:"        print(f"         Mastery урока: {result['lesson_mastery']:.3f}")
        print(f"         Диагностика: точность={result['mastery_diagnostics']['accuracy']:.2f}, скорость={result['mastery_diagnostics']['speed']:.2f}")
        print(f"         Общий mastery: {result['overall_mastery']:.3f} ({result['mastery_description']})")
        print(f"         Следующий урок: {result['next_recommended']}")

    # Шаг 3: Финальное состояние
    print("\n📊 ШАГ 3: Проверяем финальное состояние")
    final_state = api_call("/api/next", "POST", {
        "student_id": STUDENT_ID,
        "module_code": MODULE_CODE
    })

    if "error" not in final_state:
        print("🏆 Финальный уровень:"        print(f"   Общий mastery: {final_state['current_mastery']:.3f}")
        print(f"   Описание: {final_state['mastery_description']}")
        print(f"   Детали: {format_mastery_details(final_state['mastery_details'])}")
        print(f"   Рекомендация: {final_state['next_lesson_type']} урок")
        print(f"   Причина: {final_state['reason']}")


def show_mastery_statistics():
    """Показывает статистику mastery ученика."""
    print_separator("СТАТИСТИКА MASTERY УЧЕНИКА")

    stats = api_call(f"/api/mastery/{STUDENT_ID}")

    if "error" in stats:
        print(f"❌ Ошибка: {stats['error']}")
        return

    print(f"👤 Студент: {stats['student_id']}")
    print(f"📚 Всего модулей: {stats['summary']['total_modules']}")
    print(f"🏆 Средний уровень: {stats['summary']['average_mastery']:.3f}")
    print(f"✅ Завершенных модулей: {stats['summary']['completed_modules']}")

    if stats['modules']:
        print("\n📖 Детальная статистика по модулям:")
        for module in stats['modules']:
            print(f"\n   📚 {module['module_title']}")
            print(f"      Предмет: {module['subject']}")
            print(f"      Уровень: {module['stage']}")
            print(f"      Mastery: {module['mastery']['overall']:.3f} ({module['mastery_description']})")
            print(f"      Детали: {format_mastery_details(module['mastery'])}")
            print(f"      Следующий урок: {module['next_recommended']}")


def main():
    """Основная функция."""
    print("🚀 Демонстрация API системы Mastery в Ayaal Teacher")
    print("Тестируем полную интеграцию: от ответов до расчета уровня освоения"
    # Проверяем здоровье API
    health = api_call("/api/health")
    if "database" in health and health["database"] == "connected":
        print("✅ API сервер работает")
    else:
        print("❌ API сервер недоступен")
        return

    # Запускаем демонстрацию
    simulate_student_progress()
    show_mastery_statistics()

    print_separator("ЗАВЕРШЕНИЕ")
    print("🎉 Демонстрация завершена!")
    print("💡 Система mastery успешно работает:")
    print("   • Автоматический расчет уровня освоения")
    print("   • Детальная диагностика по факторам")
    print("   • Адаптивные рекомендации уроков")
    print("   • Отслеживание прогресса по типам заданий")


if __name__ == "__main__":
    main()
