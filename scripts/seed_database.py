#!/usr/bin/env python3
"""
Скрипт для загрузки базовых справочных данных в базу данных.

Загружает:
- subjects (предметы)
- stages (уровни обучения)
- stage_subject связи
"""

import os
import psycopg2
import json
from psycopg2.extras import RealDictCursor

# Настройки подключения к БД
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'ayaal_teacher'),
    'user': os.getenv('DB_USER', 'gp'),
    'password': os.getenv('DB_PASSWORD', '')
}


def get_db_connection():
    """Получает подключение к базе данных."""
    return psycopg2.connect(**DB_CONFIG)


def load_subject_registry():
    """Загружает предметы из subject_registry.json."""
    try:
        with open('curriculum/subject_registry.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Файл curriculum/subject_registry.json не найден")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка парсинга JSON: {e}")
        return None


def seed_subjects_and_stages(conn):
    """Загружает базовые предметы и уровни обучения."""
    print("🌱 Загружаем базовые справочники...")
    
    with conn.cursor() as cur:
        # 1. Загружаем уровни обучения (stages)
        print("📚 Создаем уровни обучения...")
        stages = [
            ('stage_primary', 'Primary', 'Начальная школа (1-4 классы)'),
            ('stage_lower_secondary', 'Lower Secondary', 'Средняя школа (5-7 классы)'),
            ('stage_upper_secondary', 'Upper Secondary', 'Старшая школа (8-11 классы)'),
            ('stage_advanced', 'Advanced', 'Продвинутый уровень (A-Level, IB)')
        ]
        
        for code, title_en, title_ru in stages:
            # Определяем возрастные границы для каждого уровня
            age_ranges = {
                'stage_primary': (6, 10),
                'stage_lower_secondary': (11, 13),
                'stage_upper_secondary': (14, 17),
                'stage_advanced': (16, 19)
            }
            age_min, age_max = age_ranges.get(code, (6, 19))
            
            cur.execute("""
                INSERT INTO stage (code, title, age_min, age_max)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (code) DO UPDATE SET
                    title = EXCLUDED.title,
                    age_min = EXCLUDED.age_min,
                    age_max = EXCLUDED.age_max
            """, (code, title_en, age_min, age_max))
        
        print(f"   ✅ Создано {len(stages)} уровней обучения")
        
        # 2. Загружаем предметы из subject_registry.json
        print("📖 Загружаем предметы...")
        subject_registry = load_subject_registry()
        
        if subject_registry and 'subjects' in subject_registry:
            subjects = subject_registry['subjects']
            
            for subject in subjects:
                code = subject['code']
                titles = subject.get('titles', {})
                title_en = titles.get('en', code)
                title_ru = titles.get('ru', code)
                
                # Создаем locales JSONB с русским названием
                locales = {
                    "ru": {"title": title_ru},
                    "en": {"title": title_en}
                }
                
                cur.execute("""
                    INSERT INTO subject (code, title, locales)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (code) DO UPDATE SET
                        title = EXCLUDED.title,
                        locales = EXCLUDED.locales
                """, (code, title_en, json.dumps(locales)))
            
            print(f"   ✅ Загружено {len(subjects)} предметов")
        else:
            print("   ⚠️  subject_registry.json не найден или пуст, используем базовые предметы")
            
            # Базовые предметы если JSON не найден
            basic_subjects = [
                ('Mathematics', 'Mathematics', 'Математика', 'Математические науки'),
                ('English', 'English', 'Английский язык', 'Английский язык и литература'),
                ('Science', 'Science', 'Естествознание', 'Естественные науки'),
                ('History', 'History', 'История', 'Исторические науки'),
                ('Geography', 'Geography', 'География', 'Географические науки')
            ]
            
            for code, title, title_ru, description in basic_subjects:
                # Создаем locales JSONB с русским названием
                locales = {
                    "ru": {"title": title_ru},
                    "en": {"title": title}
                }
                
                cur.execute("""
                    INSERT INTO subject (code, title, locales)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (code) DO UPDATE SET
                        title = EXCLUDED.title,
                        locales = EXCLUDED.locales
                """, (code, title, json.dumps(locales)))
            
            print(f"   ✅ Создано {len(basic_subjects)} базовых предметов")
        
        # 3. Создаем связи stage_subject для всех комбинаций
        print("🔗 Создаем связи предмет-уровень...")
        cur.execute("SELECT id FROM stage")
        stage_ids = [row[0] for row in cur.fetchall()]
        
        cur.execute("SELECT id FROM subject")
        subject_ids = [row[0] for row in cur.fetchall()]
        
        connections_created = 0
        for stage_id in stage_ids:
            for subject_id in subject_ids:
                cur.execute("""
                    INSERT INTO stage_subject (stage_id, subject_id)
                    VALUES (%s, %s)
                    ON CONFLICT (stage_id, subject_id) DO NOTHING
                """, (stage_id, subject_id))
                if cur.rowcount > 0:
                    connections_created += 1
        
        print(f"   ✅ Создано {connections_created} связей предмет-уровень")
        
        conn.commit()
        print("✅ Базовые справочники успешно загружены!")


def verify_seeding(conn):
    """Проверяет, что данные загружены корректно."""
    print("\n🔍 Проверяем загруженные данные...")
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Проверяем stages
        cur.execute("SELECT COUNT(*) as count FROM stage")
        stage_count = cur.fetchone()['count']
        print(f"   📚 Уровней обучения: {stage_count}")
        
        # Проверяем subjects
        cur.execute("SELECT COUNT(*) as count FROM subject")
        subject_count = cur.fetchone()['count']
        print(f"   📖 Предметов: {subject_count}")
        
        # Проверяем связи
        cur.execute("SELECT COUNT(*) as count FROM stage_subject")
        connection_count = cur.fetchone()['count']
        print(f"   🔗 Связей предмет-уровень: {connection_count}")
        
        # Показываем примеры
        print("\n📚 Примеры уровней:")
        cur.execute("SELECT code, title, age_min, age_max FROM stage LIMIT 3")
        for row in cur.fetchall():
            print(f"   • {row['code']}: {row['title']} (возраст {row['age_min']}-{row['age_max']})")
        
        print("\n📖 Примеры предметов:")
        cur.execute("SELECT code, title, locales FROM subject LIMIT 5")
        for row in cur.fetchall():
            locales = row['locales']
            ru_title = locales.get('ru', {}).get('title', 'N/A') if locales else 'N/A'
            print(f"   • {row['code']}: {row['title']} (RU: {ru_title})")


def main():
    """Основная функция."""
    print("🚀 Загрузка базовых справочников в базу данных Ayaal Teacher")
    print("=" * 60)
    
    try:
        # Подключаемся к БД
        print("🔌 Подключаемся к базе данных...")
        conn = get_db_connection()
        print("✅ Подключение установлено")
        
        # Загружаем данные
        seed_subjects_and_stages(conn)
        
        # Проверяем результат
        verify_seeding(conn)
        
        print("\n🎉 Загрузка завершена успешно!")
        print("Теперь можно импортировать модули через import_modules.py")
        
    except psycopg2.Error as e:
        print(f"❌ Ошибка базы данных: {e}")
        return 1
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return 1
    finally:
        if 'conn' in locals():
            conn.close()
            print("🔌 Соединение с БД закрыто")
    
    return 0


if __name__ == "__main__":
    exit(main())
