#!/usr/bin/env python3
"""
ETL script to import curriculum modules from JSON files into PostgreSQL.
"""

import os
import sys
import json
import psycopg2
from psycopg2 import sql
import glob


def get_db_connection():
    """Get database connection from environment variables."""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'ayaal_teacher'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '')
    )


def get_subject_id(cursor, subject_code):
    """Get subject ID by code."""
    cursor.execute("SELECT id FROM subject WHERE code = %s", (subject_code,))
    result = cursor.fetchone()
    if not result:
        raise ValueError(f"Subject not found: {subject_code}")
    return result[0]


def get_stage_id(cursor, stage_code):
    """Get stage ID by code."""
    cursor.execute("SELECT id FROM stage WHERE code = %s", (stage_code,))
    result = cursor.fetchone()
    if not result:
        raise ValueError(f"Stage not found: {stage_code}")
    return result[0]


def transform_module_data(module_data):
    """Transform module JSON data to match database schema."""
    return {
        'code': module_data['id'],
        'title': module_data['title'],
        'recommended_hours': module_data.get('recommended_hours'),
        'objectives_jsonb': json.dumps(module_data.get('objectives', [])),
        'lesson_policy_jsonb': json.dumps(module_data.get('lesson_policy', {})),
        'assessment_blueprint_jsonb': json.dumps(module_data.get('assessment_blueprint', {})),
        'version': module_data.get('version', '1.0.0'),
        'status': 'active'
    }


def import_module(cursor, module_data, subject_id, stage_id):
    """Import a single module."""
    transformed = transform_module_data(module_data)

    cursor.execute("""
        INSERT INTO module (
            subject_id, stage_id, code, title, recommended_hours,
            objectives_jsonb, lesson_policy_jsonb, assessment_blueprint_jsonb,
            version, status
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (code) DO UPDATE SET
            title = EXCLUDED.title,
            recommended_hours = EXCLUDED.recommended_hours,
            objectives_jsonb = EXCLUDED.objectives_jsonb,
            lesson_policy_jsonb = EXCLUDED.lesson_policy_jsonb,
            assessment_blueprint_jsonb = EXCLUDED.assessment_blueprint_jsonb,
            version = EXCLUDED.version,
            status = EXCLUDED.status,
            updated_at = now()
    """, (
        subject_id, stage_id, transformed['code'], transformed['title'],
        transformed['recommended_hours'], transformed['objectives_jsonb'],
        transformed['lesson_policy_jsonb'], transformed['assessment_blueprint_jsonb'],
        transformed['version'], transformed['status']
    ))

    print(f"✓ Imported module: {transformed['code']}")


def process_module_file(cursor, file_path):
    """Process a single module JSON file."""
    print(f"Processing: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        modules_data = json.load(f)

    if not isinstance(modules_data, list):
        modules_data = [modules_data]

    for module_data in modules_data:
        try:
            # Map subject names to codes
            subject_name = module_data.get('subject', '')
            subject_code_map = {
                'Mathematics': 'Mathematics',
                'English': 'English',
                'Science': 'Science',
                'Biology': 'Biology',
                'Chemistry': 'Chemistry',
                'Physics': 'Physics',
                'ICT': 'ICT',
                'Computer Science': 'ComputerScience',
                'ComputerScience': 'ComputerScience',
                'Global Perspectives': 'GlobalPerspectives',
                'GlobalPerspectives': 'GlobalPerspectives',
                'Art': 'Art',
                'Business': 'Business',
                'Economics': 'Economics',
                'English Literature': 'EnglishLiterature',
                'EnglishLiterature': 'EnglishLiterature',
                'Further Mathematics': 'FurtherMathematics',
                'FurtherMathematics': 'FurtherMathematics',
                'Geography': 'Geography',
                'History': 'History',
                'Languages': 'Languages',
                'Music': 'Music',
                'Physical Education': 'PhysicalEducation',
                'PE': 'PhysicalEducation'
            }

            subject_code = subject_code_map.get(subject_name)
            if not subject_code:
                print(f"⚠️  Skipping module {module_data.get('id')} - unknown subject: {subject_name}")
                continue

            # Get IDs
            subject_id = get_subject_id(cursor, subject_code)
            stage_id = get_stage_id(cursor, module_data.get('stage', ''))

            # Import module
            import_module(cursor, module_data, subject_id, stage_id)

        except Exception as e:
            print(f"✗ Error importing module {module_data.get('id')}: {e}")
            continue


def main():
    """Main ETL function."""
    if len(sys.argv) != 2:
        print("Usage: python import_modules.py <modules_directory>")
        sys.exit(1)

    modules_dir = sys.argv[1]

    if not os.path.exists(modules_dir):
        print(f"Modules directory not found: {modules_dir}")
        sys.exit(1)

    # Get all JSON files in modules directory recursively
    module_files = glob.glob(os.path.join(modules_dir, "**", "*.json"), recursive=True)

    if not module_files:
        print(f"No module files found in {modules_dir}")
        sys.exit(1)

    print(f"Found {len(module_files)} module files:")
    for mf in module_files:
        print(f"  - {os.path.relpath(mf, modules_dir)}")

    # Connect to database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Process each module file
        total_modules = 0
        for module_file in module_files:
            process_module_file(cursor, module_file)
            conn.commit()  # Commit after each file

        print(f"\n✅ Import complete! Processed {len(module_files)} files.")

        # Show summary
        cursor.execute("SELECT COUNT(*) FROM module")
        module_count = cursor.fetchone()[0]
        print(f"📊 Total modules in database: {module_count}")

        cursor.execute("""
            SELECT s.title as subject, st.title as stage, COUNT(m.id) as modules
            FROM module m
            JOIN subject s ON m.subject_id = s.id
            JOIN stage st ON m.stage_id = st.id
            GROUP BY s.title, st.title
            ORDER BY s.title, st.title
        """)

        print("\n📋 Modules by subject and stage:")
        for row in cursor.fetchall():
            print(f"  {row[0]} - {row[1]}: {row[2]} modules")

    except Exception as e:
        print(f"❌ Import failed: {e}")
        if 'conn' in locals():
            conn.rollback()
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    main()
