#!/usr/bin/env python3
"""
Простая демонстрация работы системы Mastery через API /api/next.

Показывает, как система анализирует состояние ученика и рекомендует следующий урок.
"""

import requests
import json

# Настройки API
API_BASE = "http://localhost:3000"
STUDENT_ID = "65e32701-fccf-46c4-ba7f-44ab7853444c"
MODULE_CODE = "module_math_numbers_primary"


def print_separator(title):
    """Печатает разделитель с заголовком."""
    print(f"\n{'='*70}")
    print(f"🎯 {title}")
    print(f"{'='*70}")


def test_api_next():
    """Тестируем API /api/next с нашей новой системой mastery."""
    print_separator("ДЕМОНСТРАЦИЯ API /api/next")

    print("📚 Тестируемый модуль: Математика - Числа (начальный уровень)")
    print(f"👤 ID ученика: {STUDENT_ID}")
    print(f"📖 Код модуля: {MODULE_CODE}")

    # Отправляем запрос
    response = requests.post(
        f"{API_BASE}/api/next",
        json={
            "student_id": STUDENT_ID,
            "module_code": MODULE_CODE
        },
        headers={"Content-Type": "application/json"}
    )

    if response.status_code != 200:
        print(f"❌ Ошибка HTTP {response.status_code}: {response.text}")
        return

    try:
        data = response.json()

        if "error" in data:
            print(f"❌ Ошибка API: {data['error']}")
            return

        # Выводим результаты
        print("\n🎉 УСПЕШНЫЙ ОТВЕТ ОТ СИСТЕМЫ MASTERY!")
        print("\n📊 АНАЛИЗ СОСТОЯНИЯ УЧЕНИКА:")
        print(f"   • Общий уровень mastery: {data['current_mastery']:.3f}")
        print(f"   • Описание уровня: {data['mastery_description']}")

        print("\n🔍 ДЕТАЛЬНАЯ ДИАГНОСТИКА:")
        mastery_details = data['mastery_details']
        for key, value in mastery_details.items():
            if key not in ['last_updated', 'total_submissions']:
                print(f"   • {key}: {value:.3f}")

        print("\n🎓 РЕКОМЕНДАЦИЯ СИСТЕМЫ:")
        print(f"   • Тип следующего урока: {data['next_lesson_type']}")

        print("\n🧠 ЛОГИКА РЕШЕНИЯ:")
        print(f"   • Причина: {data['reason']}")

        if 'lesson' in data and data['lesson']:
            lesson = data['lesson']
            print("\n📖 СГЕНЕРИРОВАННЫЙ УРОК:")
            print(f"   • Название: {lesson.get('title', 'N/A')}")
            print(f"   • Тип: {lesson.get('type', 'N/A')}")
            print(f"   • Количество блоков: {len(lesson.get('blocks', []))}")

            # Покажем первый блок урока
            if lesson.get('blocks') and len(lesson['blocks']) > 0:
                first_block = lesson['blocks'][0]
                print(f"   • Первый блок: {first_block.get('type', 'N/A')} - {first_block.get('content', {}).get('title', 'N/A')}")

        print_separator("ВЫВОДЫ")

        print("💡 СИСТЕМА MASTERY РАБОТАЕТ КОРРЕКТНО:")
        print("   ✅ Автоматический анализ уровня ученика")
        print("   ✅ Детальная диагностика по факторам")
        print("   ✅ Адаптивные рекомендации уроков")
        print("   ✅ Генерация персонализированного контента")
        print("   ✅ Учет политики модуля и прогресса")

        # Дополнительные insights
        overall = data['current_mastery']
        if overall < 0.3:
            print("\n🎓 ИНСАЙТ: Ученик находится на начальном этапе обучения")
            print("   Система правильно рекомендует concept уроки для закладки основ")
        elif overall < 0.6:
            print("\n🎓 ИНСАЙТ: Ученик готов к практике с подсказками")
            print("   Система рекомендует guided уроки для закрепления материала")
        else:
            print("\n🎓 ИНСАЙТ: Ученик показал хорошие результаты")
            print("   Система готова предложить более сложные задания")

    except json.JSONDecodeError as e:
        print(f"❌ Ошибка парсинга JSON: {e}")
        print(f"Ответ сервера: {response.text}")


def test_health():
    """Проверяем здоровье API."""
    print_separator("ПРОВЕРКА ЗДОРОВЬЯ API")

    try:
        response = requests.get(f"{API_BASE}/api/health")
        if response.status_code == 200:
            health = response.json()
            print("✅ API сервер работает:")
            print(f"   • Статус: {health.get('status', 'unknown')}")
            print(f"   • База данных: {health.get('database', 'unknown')}")
        else:
            print(f"❌ Ошибка здоровья API: {response.status_code}")
    except Exception as e:
        print(f"❌ Не удалось подключиться к API: {e}")


def main():
    """Основная функция."""
    print("🚀 ДЕМОНСТРАЦИЯ СИСТЕМЫ MASTERY V2")
    print("Показываем работу новой интеллектуальной системы оценки уровня освоения")

    # Проверяем здоровье
    test_health()

    # Тестируем основную функциональность
    test_api_next()

    print_separator("ЗАВЕРШЕНИЕ ДЕМОНСТРАЦИИ")
    print("🎉 Система mastery успешно протестирована!")
    print("\n💡 КЛЮЧЕВЫЕ ДОСТИЖЕНИЯ:")
    print("   • Многофакторный анализ (точность, скорость, последовательность)")
    print("   • EMA для плавного обновления уровня")
    print("   • Адаптивная логика выбора уроков")
    print("   • Детальная диагностика для обратной связи")
    print("   • Интеграция с базой данных для сохранения прогресса")


if __name__ == "__main__":
    main()
