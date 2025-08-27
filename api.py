#!/usr/bin/env python3
"""
Simple Flask API for Ayaal Teacher learning flow.
"""

import os
import json
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import jsonschema
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Flask for proper UTF-8 handling
app = Flask(__name__,
           static_folder='templates',
           static_url_path='/static')
app.config['JSON_AS_ASCII'] = False  # Allow non-ASCII characters in JSON

from validation import (
    validate_api_request_generate_lesson,
    validate_api_request_next_lesson,
    validate_api_request_submission,
    validate_lesson_json,
    validate_database_integrity
)
from cache_manager import get_cache_stats, clear_lesson_cache
from mastery_calculator import (
    calculate_lesson_mastery_v2,
    update_learning_mastery_v2,
    next_lesson_recommendation_v2,
    get_mastery_description,
    MasteryCalculatorV2,
    MasteryConfig
)
from diagnostic_system import diagnostic_system

# Try to import AI generator
try:
    from ai_generator import (
        generate_ai_concept_lesson,
        generate_ai_guided_lesson,
        generate_ai_independent_lesson
    )
    AI_AVAILABLE = True
except ImportError:
    print("Warning: AI generator not available. Install groq package and set GROQ_API_KEY")
    AI_AVAILABLE = False


def get_db_connection():
    """Get database connection."""
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'ayaal_teacher'),
        user=os.getenv('DB_USER', 'gp'),
        password=os.getenv('DB_PASSWORD', '')
    )





def generate_concept_lesson(module_code, student_locale='ru'):
    """Generate a concept lesson (placeholder implementation)."""
    return {
        "id": f"lesson_{module_code}_concept_01",
        "type": "concept",
        "title": "Основы чисел и счёта",
        "locale": student_locale,
        "blocks": [
            {
                "type": "theory",
                "content": {
                    "title": "Что такое числа?",
                    "text": "Числа помогают нам считать предметы, измерять и решать задачи..."
                }
            },
            {
                "type": "example",
                "content": {
                    "title": "Пример",
                    "text": "У Маши 3 яблока, у Пети 2 яблока. Сколько всего яблок?"
                }
            },
            {
                "type": "interactive",
                "content": {
                    "type": "mcq",
                    "question": "Сколько будет 2 + 3?",
                    "options": ["3", "4", "5", "6"],
                    "correct": 2,
                    "explanation": "2 + 3 = 5, потому что..."
                }
            }
        ]
    }


def generate_guided_lesson(module_code, student_locale='ru'):
    """Generate a guided lesson (placeholder implementation)."""
    return {
        "id": f"lesson_{module_code}_guided_01",
        "type": "guided",
        "title": "Практика счёта с помощью",
        "locale": student_locale,
        "blocks": [
            {
                "type": "instruction",
                "content": {
                    "title": "Задание",
                    "text": "Посчитайте пальцы на руке вместе с учителем..."
                }
            },
            {
                "type": "interactive",
                "content": {
                    "type": "drag_drop",
                    "instruction": "Перетащите числа к правильному количеству предметов",
                    "items": [
                        {"number": "3", "objects": ["🍎", "🍎", "🍎"]},
                        {"number": "5", "objects": ["⭐", "⭐", "⭐", "⭐", "⭐"]}
                    ]
                }
            }
        ]
    }


@app.route('/')
def index():
    """Serve the main web interface."""
    return app.send_static_file('index.html')


@app.route('/api/lessons/generate', methods=['POST'])
def generate_lesson():
    """Generate a lesson for a module."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate input data
        is_valid, message = validate_api_request_generate_lesson(data)
        if not is_valid:
            return jsonify({"error": f"Invalid request: {message}"}), 400

        module_code = data.get('module_code')
        lesson_type = data.get('lesson_type')
        student_id = data.get('student_id')
        locale = data.get('locale', 'ru')
        use_ai = data.get('use_ai', False)  # New parameter to enable AI generation

        # Get module data from database
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT m.code, m.title, s.title as subject, st.title as stage,
                       m.objectives_jsonb, m.lesson_policy_jsonb, m.assessment_blueprint_jsonb,
                       m.recommended_hours
                FROM module m
                JOIN subject s ON m.subject_id = s.id
                JOIN stage st ON m.stage_id = st.id
                WHERE m.code = %s
            """, (module_code,))

            module_data = cur.fetchone()
            if not module_data:
                return jsonify({"error": f"Module {module_code} not found"}), 404

        conn.close()

        # Generate lesson based on type and AI preference
        if use_ai and AI_AVAILABLE:
            # Use AI generation
            if lesson_type == 'concept':
                lesson = generate_ai_concept_lesson(dict(module_data), locale)
            elif lesson_type == 'guided':
                lesson = generate_ai_guided_lesson(dict(module_data), locale)
            elif lesson_type == 'independent':
                lesson = generate_ai_independent_lesson(dict(module_data), locale)
            else:
                lesson = {
                    "id": f"lesson_{module_code}_{lesson_type}_01",
                    "type": lesson_type,
                    "title": f"AI Generated {lesson_type.title()} lesson for {module_data['title']}",
                    "locale": locale,
                    "blocks": []
                }
        else:
            # Use traditional generation
            if lesson_type == 'concept':
                lesson = generate_concept_lesson(module_code, locale)
            elif lesson_type == 'guided':
                lesson = generate_guided_lesson(module_code, locale)
            else:
                lesson = {
                    "id": f"lesson_{module_code}_{lesson_type}_01",
                    "type": lesson_type,
                    "title": f"{lesson_type.title()} lesson for {module_code}",
                    "locale": locale,
                    "blocks": []
                }

        # Validate generated lesson
        is_valid, message = validate_lesson_json(lesson)
        if is_valid:
            # Add metadata about generation method
            lesson['_generated_with'] = 'ai' if use_ai and AI_AVAILABLE else 'template'
            return jsonify(lesson)
        else:
            return jsonify({"error": f"Generated lesson validation failed: {message}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/submissions', methods=['POST'])
def create_submission():
    """Create a submission for a task and update mastery."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate input data
        is_valid, message = validate_api_request_submission(data)
        if not is_valid:
            return jsonify({"error": f"Invalid request: {message}"}), 400

        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get module_id and student_id
            cur.execute("""
                SELECT m.id as module_id, s.id as student_id, m.lesson_policy_jsonb
                FROM module m, student s
                JOIN app_user u ON s.user_id = u.id
                WHERE m.code = %s AND u.id = %s
                LIMIT 1
            """, (data['module_code'], data['student_id']))

            ids = cur.fetchone()
            if not ids:
                return jsonify({"error": "Module or student not found"}), 404

            # Отладка: проверим, что получили
            if not all(key in ids for key in ['module_id', 'student_id']):
                return jsonify({"error": f"Invalid data structure: {ids}"}), 500

            # Insert submission
            cur.execute("""
                INSERT INTO submission (
                    student_id, module_id, lesson_id, task_id, kind,
                    answer_jsonb, artifacts, score
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, created_at
            """, (
                ids['student_id'], ids['module_id'], data['lesson_id'], data['task_id'],
                data['kind'], json.dumps(data.get('answer_jsonb', {})),
                json.dumps(data.get('artifacts', {})), data.get('score')
            ))

            submission = cur.fetchone()

            # Also create attempt record if it's an interactive task
            if data.get('interactive_id'):
                cur.execute("""
                    INSERT INTO attempt (
                        student_id, module_id, lesson_id, interactive_id,
                        payload_jsonb, score
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    ids['student_id'], ids['module_id'], data['lesson_id'],
                    data['interactive_id'], json.dumps(data.get('answer_jsonb', {})),
                    data.get('score')
                ))

            # Получить историю ответов для расчета mastery
            cur.execute("""
                SELECT
                    s.score,
                    s.created_at,
                    s.lesson_id,
                    CASE
                        WHEN s.lesson_id LIKE '%concept%' THEN 'concept'
                        WHEN s.lesson_id LIKE '%guided%' THEN 'guided'
                        WHEN s.lesson_id LIKE '%independent%' THEN 'independent'
                        WHEN s.lesson_id LIKE '%assessment%' THEN 'assessment'
                        ELSE 'unknown'
                    END as lesson_type
                FROM submission s
                WHERE s.student_id = %s AND s.module_id = %s
                ORDER BY s.created_at DESC
                LIMIT 20
            """, (ids['student_id'], ids['module_id']))

            submissions_history = cur.fetchall()

            # Определить тип урока из lesson_id
            lesson_id = data.get('lesson_id', '')
            if 'concept' in lesson_id:
                lesson_type = 'concept'
            elif 'guided' in lesson_id:
                lesson_type = 'guided'
            elif 'independent' in lesson_id:
                lesson_type = 'independent'
            elif 'assessment' in lesson_id:
                lesson_type = 'assessment'
            else:
                lesson_type = 'unknown'

            # Рассчитать mastery для этого урока
            time_spent = data.get('time_spent', 300)  # По умолчанию 5 минут
            score = data.get('score', 0.0)
            difficulty = data.get('difficulty', 'medium')

            lesson_mastery, mastery_diagnostics = calculate_lesson_mastery_v2(
                submissions_history, lesson_type, time_spent, score, difficulty
            )

            # Получить текущее состояние learning_state
            cur.execute("""
                SELECT mastery_jsonb, counters_jsonb
                FROM learning_state
                WHERE student_id = %s AND module_id = %s
            """, (ids['student_id'], ids['module_id']))

            learning_state = cur.fetchone()

            current_mastery = {}
            current_counters = {}

            if learning_state:
                current_mastery = learning_state['mastery_jsonb'] or {}
                current_counters = learning_state['counters_jsonb'] or {}
            else:
                # Создать новое состояние обучения
                current_mastery = {}
                current_counters = {}

            # Обновить mastery
            updated_mastery = update_learning_mastery_v2(
                current_mastery, lesson_type, lesson_mastery, len(submissions_history)
            )

            # Обновить счетчики
            if lesson_type in current_counters:
                current_counters[lesson_type] += 1
            else:
                current_counters[lesson_type] = 1

            # Определить следующий рекомендуемый урок
            lesson_policy_mix = ids['lesson_policy_jsonb'] or {}
            next_lesson_type, recommendation_reason = next_lesson_recommendation_v2(
                updated_mastery, lesson_policy_mix, current_counters
            )

            # Обновить или создать learning_state
            if learning_state:
                cur.execute("""
                    UPDATE learning_state
                    SET mastery_jsonb = %s, counters_jsonb = %s,
                        next_recommended = %s, updated_at = now()
                    WHERE student_id = %s AND module_id = %s
                """, (
                    json.dumps(updated_mastery), json.dumps(current_counters),
                    next_lesson_type, ids['student_id'], ids['module_id']
                ))
            else:
                cur.execute("""
                    INSERT INTO learning_state (
                        student_id, module_id, current_lesson_type,
                        mastery_jsonb, counters_jsonb, next_recommended
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    ids['student_id'], ids['module_id'], lesson_type,
                    json.dumps(updated_mastery), json.dumps(current_counters),
                    next_lesson_type
                ))

            conn.commit()

        # Получить описание уровня освоения
        mastery_description = get_mastery_description(updated_mastery.get('overall', 0))

        return jsonify({
            "success": True,
            "submission_id": str(submission['id']),
            "created_at": submission['created_at'].isoformat(),
            "lesson_mastery": lesson_mastery,
            "mastery_diagnostics": mastery_diagnostics,
            "overall_mastery": updated_mastery.get('overall', 0),
            "mastery_description": mastery_description,
            "next_recommended": next_lesson_type,
            "recommendation_reason": recommendation_reason,
            "mastery_details": updated_mastery
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/next', methods=['POST'])
def get_next_lesson():
    """Get next recommended lesson for a student."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate input data
        is_valid, message = validate_api_request_next_lesson(data)
        if not is_valid:
            return jsonify({"error": f"Invalid request: {message}"}), 400

        student_id = data.get('student_id')
        module_code = data.get('module_code')

        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get learning state
            cur.execute("""
                SELECT ls.*, m.code as module_code,
                       ls.mastery_jsonb->>'overall' as overall_mastery,
                       ls.mastery_jsonb->>'concept' as concept_mastery,
                       ls.mastery_jsonb->>'guided' as guided_mastery,
                       ls.mastery_jsonb->>'independent' as independent_mastery
                FROM learning_state ls
                JOIN module m ON ls.module_id = m.id
                JOIN student s ON ls.student_id = s.id
                JOIN app_user u ON s.user_id = u.id
                WHERE u.id = %s AND m.code = %s
            """, (student_id, module_code))

            ls = cur.fetchone()
            if not ls:
                # Создать новое состояние обучения если не существует
                cur.execute("""
                    SELECT m.id as module_id, s.id as student_id, m.lesson_policy_jsonb
                    FROM module m
                    CROSS JOIN student s
                    JOIN app_user u ON s.user_id = u.id
                    WHERE m.code = %s AND u.id = %s
                """, (module_code, student_id))

                module_data = cur.fetchone()
                if not module_data:
                    return jsonify({"error": "Module or student not found"}), 404

                # Создать начальное состояние
                initial_mastery = {
                    'overall': 0.0,
                    'concept': 0.0,
                    'guided': 0.0,
                    'independent': 0.0,
                    'assessment': 0.0,
                    'last_updated': datetime.now().isoformat(),
                    'total_submissions': 0
                }

                cur.execute("""
                    INSERT INTO learning_state (
                        student_id, module_id, current_lesson_type,
                        mastery_jsonb, counters_jsonb, next_recommended
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING *
                """, (
                    module_data['student_id'], module_data['module_id'], 'concept',
                    json.dumps(initial_mastery), json.dumps({}), 'concept'
                ))

                ls = cur.fetchone()
                lesson_policy = module_data['lesson_policy_jsonb'] or {}
            else:
                lesson_policy = ls.get('lesson_policy_jsonb') or {}

            # Использовать новую систему расчета следующего урока
            current_mastery = ls['mastery_jsonb'] or {}
            current_counters = ls['counters_jsonb'] or {}

            # Преобразовать lesson_policy в нужный формат
            lesson_policy_dict = lesson_policy if isinstance(lesson_policy, dict) else {}

            next_type, reason = next_lesson_recommendation_v2(
                current_mastery, lesson_policy_dict, current_counters
            )

            # Общий уровень освоения для обратной совместимости
            overall_mastery = current_mastery.get('overall', 0)

            # Generate lesson
            lesson = None
            if next_type == 'concept':
                lesson = generate_concept_lesson(module_code)
            elif next_type == 'guided':
                lesson = generate_guided_lesson(module_code)

            # Update learning state
            cur.execute("""
                UPDATE learning_state
                SET next_recommended = %s, updated_at = now()
                WHERE id = %s
            """, (next_type, ls['id']))

            conn.commit()

        # Получить описание уровня освоения
        mastery_description = get_mastery_description(overall_mastery)

        return jsonify({
            "next_lesson_type": next_type,
            "reason": reason,
            "lesson": lesson,
            "current_mastery": overall_mastery,
            "mastery_description": mastery_description,
            "mastery_details": current_mastery
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/mastery/<student_id>', methods=['GET'])
def get_student_mastery(student_id):
    """Get mastery statistics for a student."""
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Получить все состояния обучения ученика
            cur.execute("""
                SELECT
                    ls.mastery_jsonb,
                    ls.counters_jsonb,
                    ls.next_recommended,
                    ls.updated_at,
                    m.code as module_code,
                    m.title as module_title,
                    s.title as subject_title,
                    st.title as stage_title
                FROM learning_state ls
                JOIN module m ON ls.module_id = m.id
                JOIN subject s ON m.subject_id = s.id
                JOIN stage st ON m.stage_id = st.id
                JOIN student stud ON ls.student_id = stud.id
                JOIN app_user u ON stud.user_id = u.id
                WHERE u.id = %s
                ORDER BY ls.updated_at DESC
            """, (student_id,))

            learning_states = cur.fetchall()

            if not learning_states:
                return jsonify({
                    "student_id": student_id,
                    "modules": [],
                    "summary": {
                        "total_modules": 0,
                        "average_mastery": 0,
                        "completed_modules": 0
                    }
                })

            # Обработать данные
            modules_data = []
            total_mastery = 0
            completed_modules = 0

            for state in learning_states:
                mastery = state['mastery_jsonb'] or {}
                overall_mastery = mastery.get('overall', 0)
                total_mastery += overall_mastery

                if overall_mastery >= 0.8:  # Считаем завершенным
                    completed_modules += 1

                mastery_description = get_mastery_description(overall_mastery)

                modules_data.append({
                    "module_code": state['module_code'],
                    "module_title": state['module_title'],
                    "subject": state['subject_title'],
                    "stage": state['stage_title'],
                    "mastery": mastery,
                    "mastery_description": mastery_description,
                    "counters": state['counters_jsonb'] or {},
                    "next_recommended": state['next_recommended'],
                    "last_updated": state['updated_at'].isoformat() if state['updated_at'] else None
                })

            summary = {
                "total_modules": len(modules_data),
                "average_mastery": round(total_mastery / len(modules_data), 3),
                "completed_modules": completed_modules
            }

        return jsonify({
            "student_id": student_id,
            "modules": modules_data,
            "summary": summary
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route('/api/validate/database', methods=['GET'])
def validate_database():
    """Validate database integrity."""
    try:
        conn = get_db_connection()
        report = validate_database_integrity(conn)
        conn.close()

        if "error" in report:
            return jsonify({"status": "error", "message": report["error"]}), 500

        # Check if there are any issues
        issues = {k: v for k, v in report.items() if v > 0}

        if issues:
            return jsonify({
                "status": "issues_found",
                "message": "Database integrity issues detected",
                "issues": issues,
                "full_report": report
            }), 200
        else:
            return jsonify({
                "status": "valid",
                "message": "Database integrity is valid",
                "report": report
            }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/validate/lesson', methods=['POST'])
def validate_lesson_endpoint():
    """Validate lesson JSON structure."""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        is_valid, message = validate_lesson_json(data)

        return jsonify({
            "valid": is_valid,
            "message": message
        }), 200 if is_valid else 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/cache/stats', methods=['GET'])
def get_cache_stats_endpoint():
    """Get cache statistics."""
    try:
        stats = get_cache_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache_endpoint():
    """Clear lesson cache."""
    try:
        stats_before = get_cache_stats()
        clear_lesson_cache()
        stats_after = get_cache_stats()

        return jsonify({
            "message": "Cache cleared successfully",
            "stats_before": stats_before,
            "stats_after": stats_after
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/modules', methods=['GET'])
def get_modules_endpoint():
    """Get list of available modules."""
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    m.code,
                    m.title,
                    s.title as subject,
                    st.title as stage,
                    CONCAT(s.title, ' - ', m.title, ' (', st.title, ')') as display_name
                FROM module m
                JOIN subject s ON m.subject_id = s.id
                JOIN stage st ON m.stage_id = st.id
                ORDER BY s.title, m.title
            """)

            modules = cur.fetchall()
            conn.close()

            return jsonify({
                "modules": modules,
                "total": len(modules)
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- Диагностические API эндпоинты ----------

@app.route('/api/diagnostic/start', methods=['POST'])
def start_diagnostic():
    """Начинает новую диагностическую сессию для ученика."""
    try:
        data = request.get_json()

        if not data or 'student_id' not in data or 'subject_id' not in data or 'stage_id' not in data:
            return jsonify({"error": "Missing required fields: student_id, subject_id, stage_id"}), 400

        student_id = data['student_id']
        subject_id = data['subject_id']
        stage_id = data['stage_id']

        conn = get_db_connection()
        with conn.cursor() as cur:
            # Проверяем, что ученик существует
            cur.execute("SELECT id FROM student WHERE id = %s", (student_id,))
            if not cur.fetchone():
                return jsonify({"error": "Student not found"}), 404

            # Проверяем, что предмет и уровень существуют
            cur.execute("SELECT id FROM subject WHERE id = %s", (subject_id,))
            if not cur.fetchone():
                return jsonify({"error": "Subject not found"}), 404

            cur.execute("SELECT id FROM stage WHERE id = %s", (stage_id,))
            if not cur.fetchone():
                return jsonify({"error": "Stage not found"}), 404

            # Создаем диагностическую сессию
            session_id = diagnostic_system.start_diagnostic_session(
                conn, student_id, subject_id, stage_id
            )

            conn.commit()

        return jsonify({
            "success": True,
            "session_id": session_id,
            "message": "Диагностическая сессия начата",
            "next_action": "Получите следующий вопрос через /api/diagnostic/question"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/diagnostic/question', methods=['POST'])
def get_diagnostic_question():
    """Получает следующий вопрос для диагностики."""
    try:
        data = request.get_json()

        if not data or 'session_id' not in data:
            return jsonify({"error": "Missing required field: session_id"}), 400

        session_id = data['session_id']
        current_level = data.get('current_level')

        conn = get_db_connection()
        question = diagnostic_system.get_next_diagnostic_question(
            conn, session_id, current_level
        )

        if question is None:
            return jsonify({
                "message": "Диагностика завершена - все вопросы отвечены",
                "next_action": "Завершите диагностику через /api/diagnostic/complete",
                "session_id": session_id
            })

        return jsonify({
            "success": True,
            "question": question
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/diagnostic/answer', methods=['POST'])
def submit_diagnostic_answer():
    """Обрабатывает ответ ученика на диагностический вопрос."""
    try:
        data = request.get_json()

        required_fields = ['session_id', 'question_id', 'answer', 'time_spent_sec']
        if not all(field in data for field in required_fields):
            return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

        session_id = data['session_id']
        question_id = data['question_id']
        answer = data['answer']
        time_spent_sec = data['time_spent_sec']

        conn = get_db_connection()
        result = diagnostic_system.submit_diagnostic_answer(
            conn, session_id, question_id, answer, time_spent_sec
        )

        if 'error' in result:
            return jsonify(result), 400

        conn.commit()

        return jsonify({
            "success": True,
            "result": result,
            "next_action": "Получите следующий вопрос через /api/diagnostic/question"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/diagnostic/complete', methods=['POST'])
def complete_diagnostic():
    """Завершает диагностическую сессию и рассчитывает результаты."""
    try:
        data = request.get_json()

        if not data or 'session_id' not in data:
            return jsonify({"error": "Missing required field: session_id"}), 400

        session_id = data['session_id']

        conn = get_db_connection()
        result = diagnostic_system.complete_diagnostic_session(conn, session_id)

        if 'error' in result:
            return jsonify(result), 400

        conn.commit()

        return jsonify({
            "success": True,
            "diagnostic_result": result,
            "message": "Диагностика завершена! Результаты сохранены."
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/diagnostic/results/<session_id>', methods=['GET'])
def get_diagnostic_results(session_id):
    """Получает результаты диагностической сессии."""
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    ds.*,
                    s.email as student_email,
                    subj.title as subject_title,
                    st.title as stage_title
                FROM diagnostic_session ds
                JOIN student stud ON ds.student_id = stud.id
                JOIN app_user s ON stud.user_id = s.id
                JOIN subject subj ON ds.subject_id = subj.id
                JOIN stage st ON ds.stage_id = st.id
                WHERE ds.id = %s
            """, (session_id,))

            session = cur.fetchone()
            if not session:
                return jsonify({"error": "Diagnostic session not found"}), 404

            return jsonify({
                "session": dict(session),
                "results": session['results_jsonb'],
                "recommendations": session['recommendations_jsonb']
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/diagnostic/student/<student_id>', methods=['GET'])
def get_student_diagnostic_status(student_id):
    """Получает статус диагностики для ученика."""
    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Получаем информацию о студенте
            cur.execute("""
                SELECT
                    s.*,
                    u.email,
                    CASE
                        WHEN s.diagnostic_completed_at IS NOT NULL THEN 'completed'
                        WHEN EXISTS (
                            SELECT 1 FROM diagnostic_session ds
                            WHERE ds.student_id = s.id AND ds.status = 'in_progress'
                        ) THEN 'in_progress'
                        ELSE 'not_started'
                    END as diagnostic_status
                FROM student s
                JOIN app_user u ON s.user_id = u.id
                WHERE s.id = %s
            """, (student_id,))

            student = cur.fetchone()
            if not student:
                return jsonify({"error": "Student not found"}), 404

            result = dict(student)

            # Если диагностика завершена, получаем последнюю сессию
            if result['diagnostic_status'] == 'completed':
                cur.execute("""
                    SELECT * FROM diagnostic_session
                    WHERE student_id = %s AND status = 'completed'
                    ORDER BY completed_at DESC
                    LIMIT 1
                """, (student_id,))

                last_session = cur.fetchone()
                if last_session:
                    result['last_diagnostic'] = dict(last_session)

            return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(debug=True, host='0.0.0.0', port=port)
