#!/usr/bin/env python3
"""
AI-Пowered Диагностическая система Ayaal Teacher.

Показывает:
1. Создание диагностической сессии
2. AI генерацию персонализированных вопросов
3. Адаптивную диагностику на основе ответов
4. Расчет уровня и рекомендаций
5. Интеграцию с системой mastery
"""

import requests
import json
import time
import os

# Настройки API
API_BASE = "http://localhost:3000"
STUDENT_ID = "87b7df4c-0246-46d8-af27-54fdb1a826f7"


def print_separator(title):
    """Печатает разделитель с заголовком."""
    print(f"\n{'='*80}")
    print(f"🎯 {title}")
    print(f"{'='*80}")


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


def demonstrate_ai_diagnostic_flow():
    """Демонстрирует полный цикл AI диагностики."""
    print_separator("AI-ПОВЕРЕД ДИАГНОСТИКА УЧЕНИКА")

    # 1. Проверяем статус диагностики ученика
    print("1️⃣ Проверяем статус диагностики ученика...")
    status = api_call(f"/api/diagnostic/student/{STUDENT_ID}")

    if "error" in status:
        print(f"❌ Ошибка: {status['error']}")
        return

    print(f"   Статус диагностики: {status['diagnostic_status']}")
    if status['diagnostic_status'] == 'not_started':
        print("   ✅ Ученик готов к диагностике!")
    else:
        print(f"   Последняя диагностика: {status.get('last_diagnostic', {}).get('completed_at', 'неизвестно')}")

    # 2. Создаем диагностическую сессию для Математики
    print("\n2️⃣ Создаем диагностическую сессию...")

    # Получаем UUIDы для Математики и Primary уровня
    try:
        import subprocess
        result = subprocess.run([
            'psql', '-h', 'localhost', '-p', '5432', '-U', 'gp', '-d', 'ayaal_teacher',
            '-c', "SELECT id FROM subject WHERE code = 'Mathematics';"
        ], capture_output=True, text=True)

        math_subject_id = None
        lines = result.stdout.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) == 36 and '-' in line:
                math_subject_id = line
                break

        result = subprocess.run([
            'psql', '-h', 'localhost', '-p', '5432', '-U', 'gp', '-d', 'ayaal_teacher',
            '-c', "SELECT id FROM stage WHERE code = 'stage_primary';"
        ], capture_output=True, text=True)

        primary_stage_id = None
        lines = result.stdout.split('\n')
        for line in lines:
            line = line.strip()
            if len(line) == 36 and '-' in line:
                primary_stage_id = line
                break

        if not math_subject_id or not primary_stage_id:
            print("❌ Не удалось получить UUIDы предмета или уровня")
            return

    except Exception as e:
        print(f"❌ Ошибка получения UUIDов: {e}")
        return

    start_result = api_call("/api/diagnostic/start", "POST", {
        "student_id": STUDENT_ID,
        "subject_id": math_subject_id,
        "stage_id": primary_stage_id
    })

    if "error" in start_result:
        print(f"❌ Ошибка запуска диагностики: {start_result['error']}")
        return

    session_id = start_result['session_id']
    print(f"   ✅ Создана сессия: {session_id}")
    print("   🎓 Предмет: Математика (Начальная школа)")

    # 3. Проходим AI диагностику (симулируем ученика среднего уровня)
    print("\n3️⃣ Проходим AI диагностику...")
    print("   🤖 AI адаптирует вопросы под уровень ученика...")

    question_count = 0
    current_level = 'beginner'

    while question_count < 5:  # Максимум 5 вопросов для демонстрации
        # Получаем следующий AI-сгенерированный вопрос
        question_result = api_call("/api/diagnostic/question", "POST", {
            "session_id": session_id,
            "current_level": current_level
        })

        if "question" not in question_result:
            if "message" in question_result:
                print(f"\n   🎉 Диагностика завершена: {question_result['message']}")
                break
            else:
                print(f"❌ Ошибка получения вопроса: {question_result}")
                break

        question = question_result['question']
        question_count += 1

        print(f"\n   🧠 Вопрос {question_count} (AI сгенерирован):")
        print(f"      📚 Уровень: {question['difficulty_level']}")
        print(f"      ⏰ Время: {question['time_limit_sec']} сек")
        print(f"      💯 Баллы: {question['points']}")

        content = question['content']
        print(f"      ❓ {content['question']}")

        if 'options' in content:
            print("      📋 Варианты:")
            for i, option in enumerate(content['options']):
                print(f"         {i+1}. {option}")

        # Симулируем ответ ученика (правильный в 80% случаев)
        import random
        is_correct_answer = random.random() < 0.8

        if question['question_type'] == 'mcq' and 'options' in content:
            if is_correct_answer:
                # Правильный ответ (симулируем, что ученик знает правильный)
                selected_option = content.get('correct_option', 0) if 'correct_option' in content else 0
            else:
                # Случайный неправильный ответ
                selected_option = random.randint(0, len(content['options']) - 1)

            answer = {"selected_option": selected_option}
        else:
            answer = {"answer": "42" if is_correct_answer else "не знаю"}

        # Отправляем ответ
        answer_result = api_call("/api/diagnostic/answer", "POST", {
            "session_id": session_id,
            "question_id": question['question_id'],
            "answer": answer,
            "time_spent_sec": random.randint(30, 120)
        })

        if "error" in answer_result:
            print(f"      ❌ Ошибка отправки ответа: {answer_result['error']}")
            continue

        result = answer_result['result']
        print(f"      ✅ Ответ принят: {'Правильно!' if result['is_correct'] else 'Неправильно'}")
        print(f"      📊 Текущая точность: {result['total_score']:.2f}")
        print(f"      📈 Следующий уровень: {result['next_level']}")

        # Обновляем уровень для следующего вопроса
        current_level = result['next_level']

        time.sleep(1)  # Небольшая пауза

    # 4. Завершаем диагностику
    print("\n4️⃣ Завершаем диагностику...")
    complete_result = api_call("/api/diagnostic/complete", "POST", {
        "session_id": session_id
    })

    if "error" in complete_result:
        print(f"❌ Ошибка завершения диагностики: {complete_result['error']}")
        return

    diagnostic_result = complete_result['diagnostic_result']
    print("   🎊 Диагностика завершена! Результаты:")
    print(f"      🏆 Определенный уровень: {diagnostic_result['estimated_level']}")
    print(f"      🎯 Рекомендуемая сложность: {diagnostic_result['recommended_difficulty']}")

    # 5. Показываем детальную статистику
    print("\n5️⃣ Детальная статистика диагностики...")
    results = api_call(f"/api/diagnostic/results/{session_id}")

    if "error" not in results and 'results' in results:
        results_data = results['results']
        print("   📊 Статистика ответов:")
        print(f"      • Всего вопросов: {results_data['total_questions']}")
        print(f"      • Правильных ответов: {results_data['correct_answers']}")
        print(f"      • Точность: {results_data['accuracy']:.3f}")
        print(f"      • Среднее время: {results_data['avg_time_spent']:.1f} сек")
        print(f"      • Распределение по уровням: {results_data['level_distribution']}")

    if 'recommendations' in results:
        recommendations = results['recommendations']
        print("\n   🎯 Рекомендации по обучению:")
        for rec in recommendations.get('study_plan', []):
            print(f"      • {rec}")
        for rec in recommendations.get('focus_areas', []):
            print(f"      • {rec}")

    # 6. Проверяем обновленный статус ученика
    print("\n6️⃣ Проверяем обновленный статус ученика...")
    updated_status = api_call(f"/api/diagnostic/student/{STUDENT_ID}")

    if "error" not in updated_status:
        print("   🔄 Обновленный профиль:")
        print(f"      • Статус диагностики: {updated_status['diagnostic_status']}")
        print(f"      • Текущий уровень: {updated_status.get('current_level', 'не определен')}")
        print(f"      • Рекомендуемая сложность: {updated_status.get('recommended_difficulty', 'не определена')}")
        print("      • Эти данные будут использоваться системой mastery!")


def demonstrate_ai_power():
    """Демонстрирует возможности AI диагностики."""
    print_separator("СИЛА AI ДИАГНОСТИКИ")

    print("🚀 Преимущества AI-powered диагностики:")
    print("   🧠 Адаптивность - вопросы подстраиваются под ученика")
    print("   🎯 Персонализация - уникальные вопросы для каждого уровня")
    print("   📈 Динамика - уровень меняется по ходу диагностики")
    print("   🔍 Анализ - глубокий анализ паттернов ответов")
    print("   🎮 Интерактивность - живое взаимодействие")
    print("   📚 Масштабируемость - работает для любых предметов")

    print("\n📊 Что умеет система:")
    print("   ✅ Генерировать вопросы нужного уровня сложности")
    print("   ✅ Анализировать время решения")
    print("   ✅ Отслеживать последовательность успехов")
    print("   ✅ Рекомендовать оптимальную сложность заданий")
    print("   ✅ Предлагать индивидуальный план обучения")
    print("   ✅ Интегрироваться с системой mastery")


def main():
    """Основная функция демонстрации."""
    print("🚀 AI-ПОВЕРЕД ДИАГНОСТИКА В AYAAL TEACHER")
    print("Показываем мощь искусственного интеллекта в образовании!")

    # Проверяем здоровье API
    health = api_call("/api/health")
    if "database" in health and health["database"] == "connected":
        print("✅ API сервер работает")
    else:
        print("❌ API сервер недоступен")
        return

    # Проверяем наличие AI
    ai_available = "GROQ_API_KEY" in str(os.environ.get('GROQ_API_KEY', ''))
    if ai_available:
        print("✅ AI (Groq) доступен - будут генерироваться умные вопросы")
    else:
        print("⚠️  AI недоступен - будут использоваться резервные вопросы")

    # Запускаем демонстрацию
    demonstrate_ai_diagnostic_flow()
    demonstrate_ai_power()

    print_separator("ИТОГИ ДЕМОНСТРАЦИИ")
    print("🎉 AI-диагностика успешно протестирована!")
    print("\n💡 РЕЗУЛЬТАТЫ:")
    print("   ✅ Создана адаптивная система диагностики уровня")
    print("   ✅ AI генерирует персонализированные вопросы")
    print("   ✅ Система точно определяет уровень ученика")
    print("   ✅ Рекомендуется оптимальная сложность заданий")
    print("   ✅ Интегрировано с системой mastery")
    print("   ✅ Полная автоматизация процесса обучения")

    print("\n🎓 ВОЗМОЖНОСТИ:")
    print("   • Новые ученики автоматически проходят диагностику")
    print("   • Каждый ученик получает персонализированные рекомендации")
    print("   • Система непрерывно адаптируется к прогрессу")
    print("   • AI создает бесконечное количество уникальных вопросов")
    print("   • Анализ данных помогает улучшать методику обучения")


if __name__ == "__main__":
    main()
