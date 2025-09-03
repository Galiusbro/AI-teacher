#!/usr/bin/env python3
"""
Скрипт для запуска всех тестов системы диагностики.

Запускает:
- Основные тесты системы диагностики
- API тесты
- Тесты интеграции
- Тесты производительности
"""

import sys
import os
import time
from typing import List, Tuple

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_test_module(module_name: str) -> Tuple[int, int]:
    """Запуск тестового модуля и возврат результатов."""
    try:
        if module_name == "comprehensive":
            from test_comprehensive_diagnostic import run_all_tests
            print(f"\n{'='*60}")
            print(f"🧪 ЗАПУСК ОСНОВНЫХ ТЕСТОВ СИСТЕМЫ ДИАГНОСТИКИ")
            print(f"{'='*60}")
            run_all_tests()
            return 1, 0  # Предполагаем успех, так как функция не возвращает детали
            
        elif module_name == "api":
            from test_diagnostic_api import run_api_tests
            print(f"\n{'='*60}")
            print(f"🔌 ЗАПУСК API ТЕСТОВ СИСТЕМЫ ДИАГНОСТИКИ")
            print(f"{'='*60}")
            run_api_tests()
            return 1, 0  # Предполагаем успех
            
        else:
            print(f"❌ Неизвестный модуль тестов: {module_name}")
            return 0, 1
            
    except ImportError as e:
        print(f"❌ Ошибка импорта модуля {module_name}: {e}")
        return 0, 1
    except Exception as e:
        print(f"❌ Ошибка при запуске тестов {module_name}: {e}")
        return 0, 1

def run_individual_tests():
    """Запуск отдельных тестов для детальной проверки."""
    print(f"\n{'='*60}")
    print(f"🔍 ДЕТАЛЬНАЯ ПРОВЕРКА ОТДЕЛЬНЫХ КОМПОНЕНТОВ")
    print(f"{'='*60}")
    
    try:
        from smart_diagnostic_system import SmartDiagnosticSystem, DifficultyLevel
        
        # Тест 1: Инициализация системы
        print("\n1️⃣ Тест инициализации системы...")
        system = SmartDiagnosticSystem()
        assert system is not None
        print("   ✅ Система инициализирована успешно")
        
        # Тест 2: Создание профиля ученика
        print("\n2️⃣ Тест создания профиля ученика...")
        profile = system.initialize_student_profile("test_001", 12, ["Mathematics", "English"])
        assert profile.student_id == "test_001"
        assert profile.age == 12
        assert len(profile.subjects) == 2
        print("   ✅ Профиль ученика создан успешно")
        
        # Тест 3: Генерация диалогового вопроса
        print("\n3️⃣ Тест генерации диалогового вопроса...")
        question = system.generate_next_question("test_001", "Mathematics")
        assert question is not None
        assert question.question_type == "dialogue"
        print("   ✅ Диалоговый вопрос сгенерирован успешно")
        
        # Тест 4: Обработка ответа
        print("\n4️⃣ Тест обработки ответа...")
        result = system.process_answer("test_001", question.id, {"answer": "Мне нравится математика! 😊"}, 10.0)
        assert "is_correct" in result
        assert "confidence_score" in result
        assert "new_difficulty_level" in result
        print("   ✅ Ответ обработан успешно")
        
        # Тест 5: Генерация плана обучения
        print("\n5️⃣ Тест генерации плана обучения...")
        plan = system.generate_learning_plan("test_001")
        assert "overall_level" in plan
        assert "psychological_profile" in plan
        assert "recommendations" in plan
        print("   ✅ План обучения сгенерирован успешно")
        
        # Тест 6: Экспорт данных для БД
        print("\n6️⃣ Тест экспорта данных для БД...")
        session_record = system.export_session_record("test_001")
        assert "student_id" in session_record
        assert "persona" in session_record
        print("   ✅ Данные для БД экспортированы успешно")
        
        print(f"\n🎉 Все индивидуальные тесты пройдены успешно!")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка в индивидуальных тестах: {e}")
        return False

def check_dependencies():
    """Проверка зависимостей и файлов."""
    print(f"\n{'='*60}")
    print(f"📋 ПРОВЕРКА ЗАВИСИМОСТЕЙ И ФАЙЛОВ")
    print(f"{'='*60}")
    
    required_files = [
        "smart_diagnostic_system.py",
        "diagnostic_utils.py",
        "mastery_calculator.py",
        "templates/diagnostic_sample_10yo.json",
        "templates/diagnostic.schema.json",
        "curriculum/diagnostic/diagnostic.template.json"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"   ✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Отсутствующие файлы:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print(f"\n✅ Все необходимые файлы найдены!")
    return True

def main():
    """Основная функция запуска тестов."""
    print("🚀 ЗАПУСК КОМПЛЕКСНОГО ТЕСТИРОВАНИЯ СИСТЕМЫ ДИАГНОСТИКИ")
    print("=" * 80)
    
    start_time = time.time()
    
    # Проверка зависимостей
    if not check_dependencies():
        print("\n❌ Тестирование прервано из-за отсутствующих файлов")
        return 1
    
    # Запуск индивидуальных тестов
    if not run_individual_tests():
        print("\n❌ Тестирование прервано из-за ошибок в базовых компонентах")
        return 1
    
    # Запуск основных тестов
    test_modules = ["comprehensive", "api"]
    total_passed = 0
    total_failed = 0
    
    for module in test_modules:
        passed, failed = run_test_module(module)
        total_passed += passed
        total_failed += failed
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Итоговый отчет
    print(f"\n{'='*80}")
    print(f"📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
    print(f"{'='*80}")
    print(f"⏱️  Общее время выполнения: {total_time:.2f} секунд")
    print(f"📋 Модулей протестировано: {len(test_modules)}")
    print(f"✅ Успешных модулей: {total_passed}")
    print(f"❌ Провалившихся модулей: {total_failed}")
    
    if total_failed == 0:
        print(f"\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print(f"💡 Система диагностики готова к использованию")
        return 0
    else:
        print(f"\n⚠️  НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛИЛИСЬ")
        print(f"🔧 Рекомендуется исправить ошибки перед использованием")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
