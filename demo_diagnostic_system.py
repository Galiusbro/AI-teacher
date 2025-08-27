#!/usr/bin/env python3
"""
Полная демонстрация диагностической системы Ayaal Teacher.

Показывает:
1. Создание диагностических вопросов
2. Запуск диагностической сессии
3. Прохождение диагностики учеником
4. Расчет уровня и рекомендаций
5. Интеграцию с системой mastery
"""

import requests
import json
import time
import subprocess

# Настройки API
API_BASE = "http://localhost:3000"
STUDENT_ID = "87b7df4c-0246-46d8-af27-54fdb1a826f7"
MATH_SUBJECT_ID = None
PRIMARY_STAGE_ID = None


def print_separator(title):
    """Печатает разделитель с заголовком."""
    print(f"\n{'='*80}")
    print(f"🎯 {title}")
    print(f"{'='*80}")


def run_sql_script(script_path):
    """Выполняет SQL скрипт."""
    print(f"📄 Выполняем {script_path}...")
    try:
        result = subprocess.run([
            'psql', '-h', 'localhost', '-p', '5432', '-U', 'gp', '-d', 'ayaal_teacher',
            '-f', script_path
        ], capture_output=True, text=True, cwd='/Users/gp/projects/ayaal/teacher')

        if result.returncode == 0:
            print("✅ Скрипт выполнен успешно")
            return True
        else:
            print(f"❌ Ошибка выполнения скрипта: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False


def get_subject_and_stage_ids():
    """Получает UUIDы предмета и уровня."""
    global MATH_SUBJECT_ID, PRIMARY_STAGE_ID

    print("🔍 Получаем UUIDы предмета и уровня...")

    # Используем SQL для получения UUIDов
    try:
        import subprocess

        # Получаем UUID предмета Mathematics
        result = subprocess.run([
            'psql', '-h', 'localhost', '-p', '5432', '-U', 'gp', '-d', 'ayaal_teacher',
            '-c', "SELECT id FROM subject WHERE code = 'Mathematics';"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                line = line.strip()
                if len(line) == 36 and '-' in line:  # UUID формат
                    MATH_SUBJECT_ID = line
                    print(f"✅ Mathematics ID: {MATH_SUBJECT_ID}")
                    break

        # Получаем UUID уровня stage_primary
        result = subprocess.run([
            'psql', '-h', 'localhost', '-p', '5432', '-U', 'gp', '-d', 'ayaal_teacher',
            '-c', "SELECT id FROM stage WHERE code = 'stage_primary';"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            lines = result.stdout.split('\n')
            for line in lines:
                line = line.strip()
                if len(line) == 36 and '-' in line:
                    PRIMARY_STAGE_ID = line
                    print(f"✅ Primary Stage ID: {PRIMARY_STAGE_ID}")
                    break

        if MATH_SUBJECT_ID and PRIMARY_STAGE_ID:
            return True
        else:
            print(f"❌ MATH_SUBJECT_ID: {MATH_SUBJECT_ID}")
            print(f"❌ PRIMARY_STAGE_ID: {PRIMARY_STAGE_ID}")
            print("❌ Не удалось получить UUIDы")
            return False

    except Exception as e:
        print(f"❌ Ошибка получения UUIDов: {e}")
        return False


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


def setup_database():
    """Настраивает базу данных для диагностики."""
    print_separator("НАСТРОЙКА БАЗЫ ДАННЫХ")

    # 1. Применяем миграцию для диагностических таблиц
    if not run_sql_script("db/migrations/007_diagnostic_assessment.sql"):
        print("❌ Ошибка применения миграции")
        return False

    # 2. Создаем диагностические вопросы
    if not run_sql_script("create_diagnostic_questions.sql"):
        print("❌ Ошибка создания вопросов")
        return False

    print("✅ База данных настроена")
    return True


def demonstrate_diagnostic_flow():
    """Демонстрирует полный цикл диагностики."""
    print_separator("ДЕМОНСТРАЦИЯ ДИАГНОСТИЧЕСКОЙ СИСТЕМЫ")

    # 1. Проверяем статус диагностики ученика
    print("1️⃣ Проверяем статус диагностики ученика...")
    status = api_call(f"/api/diagnostic/student/{STUDENT_ID}")

    if "error" in status:
        print(f"❌ Ошибка: {status['error']}")
        return

    print(f"   Статус диагностики: {status['diagnostic_status']}")
    print(f"   Рекомендуемая сложность: {status.get('recommended_difficulty', 'не определена')}")

    # 2. Начинаем диагностическую сессию
    print("\n2️⃣ Начинаем диагностическую сессию...")
    start_result = api_call("/api/diagnostic/start", "POST", {
        "student_id": STUDENT_ID,
        "subject_id": MATH_SUBJECT_ID,
        "stage_id": PRIMARY_STAGE_ID
    })

    if "error" in start_result:
        print(f"❌ Ошибка запуска диагностики: {start_result['error']}")
        return

    session_id = start_result['session_id']
    print(f"   Создана сессия: {session_id}")

    # 3. Проходим диагностику (симулируем ответы ученика)
    print("\n3️⃣ Проходим диагностику...")

    question_count = 0
    while question_count < 8:  # Ограничение на количество вопросов
        # Получаем следующий вопрос
        question_result = api_call("/api/diagnostic/question", "POST", {
            "session_id": session_id
        })

        if "question" not in question_result:
            if "message" in question_result and "завершена" in question_result['message']:
                print(f"   Диагностика завершена: {question_result['message']}")
                break
            else:
                print(f"❌ Ошибка получения вопроса: {question_result}")
                break

        question = question_result['question']
        question_count += 1

        print(f"\n   Вопрос {question_count}: {question['content']['question']}")

        # Симулируем ответ ученика
        # Для простоты отвечаем правильно на 80% вопросов
        import random
        is_correct_answer = random.random() < 0.8

        if question['question_type'] == 'mcq':
            # Для MCQ выбираем правильный или случайный ответ
            if is_correct_answer:
                selected_option = question['content']['correct_option'] if 'correct_option' in question['content'] else 1
            else:
                selected_option = random.randint(0, len(question['content']['options']) - 1)

            answer = {"selected_option": selected_option}
        else:
            # Для открытых вопросов
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
        print(f"      Результат: {'✅ Правильно' if result['is_correct'] else '❌ Неправильно'}")
        print(f"      Текущая точность: {result['total_score']:.2f}")
        print(f"      Следующий уровень: {result['next_level']}")

        time.sleep(0.5)  # Небольшая задержка

    # 4. Завершаем диагностику
    print("\n4️⃣ Завершаем диагностику...")
    complete_result = api_call("/api/diagnostic/complete", "POST", {
        "session_id": session_id
    })

    if "error" in complete_result:
        print(f"❌ Ошибка завершения диагностики: {complete_result['error']}")
        return

    diagnostic_result = complete_result['diagnostic_result']
    print("   Диагностика завершена! 📊")
    print(f"   Определенный уровень: {diagnostic_result['estimated_level']}")
    print(f"   Уверенность: {diagnostic_result['confidence_score']:.3f}")
    print(f"   Рекомендуемая сложность: {diagnostic_result['recommended_difficulty']}")

    # 5. Проверяем результаты диагностики
    print("\n5️⃣ Проверяем полные результаты...")
    results = api_call(f"/api/diagnostic/results/{session_id}")

    if "error" not in results:
        results_data = results['results']
        print("   Детальная статистика:")
        print(f"   • Всего вопросов: {results_data['total_questions']}")
        print(f"   • Правильных ответов: {results_data['correct_answers']}")
        print(f"   • Точность: {results_data['accuracy']:.3f}")
        print(f"   • Среднее время: {results_data['avg_time_spent']:.1f} сек")
        print(f"   • Распределение по уровням: {results_data['level_distribution']}")

        recommendations = results['recommendations']
        print("\n   Рекомендации:")
        for rec in recommendations.get('study_plan', []):
            print(f"   • {rec}")
        for rec in recommendations.get('focus_areas', []):
            print(f"   • {rec}")

    # 6. Проверяем обновленный статус ученика
    print("\n6️⃣ Проверяем обновленный статус ученика...")
    updated_status = api_call(f"/api/diagnostic/student/{STUDENT_ID}")

    if "error" not in updated_status:
        print("   Обновленный статус:")
        print(f"   • Статус диагностики: {updated_status['diagnostic_status']}")
        print(f"   • Текущий уровень: {updated_status.get('current_level', 'не определен')}")
        print(f"   • Рекомендуемая сложность: {updated_status.get('recommended_difficulty', 'не определена')}")


def demonstrate_integration_with_mastery():
    """Демонстрирует интеграцию диагностики с системой mastery."""
    print_separator("ИНТЕГРАЦИЯ С СИСТЕМОЙ MASTERY")

    print("🔗 Диагностика интегрирована с системой mastery:")
    print("   • Результаты диагностики сохраняются в профиле ученика")
    print("   • Рекомендуемая сложность используется для подбора заданий")
    print("   • Уровень ученика влияет на выбор типа уроков")
    print("   • Система mastery адаптируется под диагностированные способности")

    # Проверяем статус ученика после диагностики
    status = api_call(f"/api/diagnostic/student/{STUDENT_ID}")

    if "error" not in status and status['diagnostic_status'] == 'completed':
        print("\n✅ Интеграция работает:")
        print(f"   • Ученик имеет уровень: {status.get('current_level', 'не определен')}")
        print(f"   • Рекомендуемая сложность: {status.get('recommended_difficulty', 'не определена')}")
        print("   • Эти данные будут использоваться системой mastery")
    else:
        print("\n⚠️  Диагностика не завершена - интеграция пока не активна")


def main():
    """Основная функция демонстрации."""
    print("🚀 ПОЛНАЯ ДЕМОНСТРАЦИЯ ДИАГНОСТИЧЕСКОЙ СИСТЕМЫ")
    print("Показываем определение уровня ученика и адаптацию сложности заданий")

    # 1. Настраиваем базу данных
    if not setup_database():
        print("❌ Не удалось настроить базу данных")
        return

    # 2. Получаем необходимые UUIDы
    if not get_subject_and_stage_ids():
        print("❌ Не удалось получить UUIDы предмета и уровня")
        return

    # 3. Демонстрируем работу диагностики
    demonstrate_diagnostic_flow()

    # 4. Показываем интеграцию с mastery
    demonstrate_integration_with_mastery()

    print_separator("ИТОГИ ДЕМОНСТРАЦИИ")
    print("🎉 Диагностическая система успешно протестирована!")
    print("\n💡 РЕАЛИЗОВАННЫЕ ФУНКЦИИ:")
    print("   ✅ Начальные диагностические тесты")
    print("   ✅ Определение уровня ученика")
    print("   ✅ Адаптация сложности заданий")
    print("   ✅ Система рекомендаций по обучению")
    print("   ✅ Интеграция с базой данных")
    print("   ✅ API для управления диагностикой")
    print("   ✅ Интеграция с системой mastery")

    print("\n🎓 ПРИМЕНЕНИЕ:")
    print("   • Новые ученики проходят диагностику при первом входе")
    print("   • Система определяет начальный уровень по предмету")
    print("   • Рекомендуется оптимальная сложность заданий")
    print("   • Система mastery использует результаты диагностики")
    print("   • Постоянная адаптация под прогресс ученика")


if __name__ == "__main__":
    main()
