#!/usr/bin/env python3
"""
Validation module for Ayaal Teacher API.
Provides comprehensive validation for API inputs, lessons, and data integrity.
"""

import re
import json
from typing import Dict, List, Any, Tuple, Optional


class ValidationError(Exception):
    """Custom validation error."""
    pass


def validate_uuid(uuid_str: str) -> bool:
    """Validate UUID format."""
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(uuid_pattern, uuid_str))


def validate_email(email: str) -> bool:
    """Validate email format."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))


def validate_module_code(module_code: str) -> bool:
    """Validate module code format."""
    # Should start with 'module_' and contain only valid characters
    return module_code.startswith('module_') and bool(re.match(r'^module_[a-zA-Z0-9_]+$', module_code))


def validate_lesson_type(lesson_type: str) -> bool:
    """Validate lesson type."""
    valid_types = ['concept', 'guided', 'independent', 'assessment', 'revision', 'project', 'lab']
    return lesson_type in valid_types


def validate_locale(locale: str) -> bool:
    """Validate locale format."""
    return bool(re.match(r'^[a-z]{2}(-[A-Z]{2})?$', locale))


def validate_api_request_generate_lesson(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate request for lesson generation."""
    try:
        required_fields = ['module_code', 'lesson_type', 'student_id']

        # Check required fields
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"

        # Validate module_code
        if not validate_module_code(data['module_code']):
            return False, f"Invalid module_code format: {data['module_code']}"

        # Validate lesson_type
        if not validate_lesson_type(data['lesson_type']):
            return False, f"Invalid lesson_type: {data['lesson_type']}"

        # Validate student_id (UUID)
        if not validate_uuid(data['student_id']):
            return False, f"Invalid student_id format: {data['student_id']}"

        # Validate optional locale
        if 'locale' in data and not validate_locale(data['locale']):
            return False, f"Invalid locale format: {data['locale']}"

        return True, "Valid"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_api_request_next_lesson(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate request for next lesson."""
    try:
        required_fields = ['student_id', 'module_code']

        # Check required fields
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"

        # Validate module_code
        if not validate_module_code(data['module_code']):
            return False, f"Invalid module_code format: {data['module_code']}"

        # Validate student_id (UUID)
        if not validate_uuid(data['student_id']):
            return False, f"Invalid student_id format: {data['student_id']}"

        return True, "Valid"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_api_request_submission(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate request for submission."""
    try:
        required_fields = ['student_id', 'module_code', 'lesson_id', 'task_id', 'kind']

        # Check required fields
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"

        # Validate module_code
        if not validate_module_code(data['module_code']):
            return False, f"Invalid module_code format: {data['module_code']}"

        # Validate student_id (UUID)
        if not validate_uuid(data['student_id']):
            return False, f"Invalid student_id format: {data['student_id']}"

        # Validate kind
        valid_kinds = ['practice', 'homework', 'project', 'lab', 'assessment']
        if data['kind'] not in valid_kinds:
            return False, f"Invalid kind: {data['kind']}. Must be one of: {valid_kinds}"

        # Validate score if provided
        if 'score' in data:
            try:
                score = float(data['score'])
                if not (0.0 <= score <= 1.0):
                    return False, f"Score must be between 0.0 and 1.0, got: {score}"
            except (ValueError, TypeError):
                return False, f"Invalid score format: {data['score']}"

        # Validate answer_jsonb if provided
        if 'answer_jsonb' in data:
            try:
                json.dumps(data['answer_jsonb'])  # Check if JSON serializable
            except (TypeError, ValueError):
                return False, "answer_jsonb must be JSON serializable"

        return True, "Valid"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_lesson_json(lesson_data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate lesson JSON structure."""
    try:
        # Required fields for our simplified lessons
        required_fields = ['id', 'type', 'title', 'locale', 'blocks']
        for field in required_fields:
            if field not in lesson_data:
                return False, f"Missing required field: {field}"

        # Validate lesson type
        if not validate_lesson_type(lesson_data['type']):
            return False, f"Invalid lesson type: {lesson_data['type']}"

        # Validate locale
        if not validate_locale(lesson_data['locale']):
            return False, f"Invalid locale format: {lesson_data['locale']}"

        # Validate blocks
        if not isinstance(lesson_data['blocks'], list):
            return False, "Blocks must be a list"

        if len(lesson_data['blocks']) == 0:
            return False, "Lesson must have at least one block"

        valid_block_types = ['theory', 'example', 'instruction', 'interactive']

        for i, block in enumerate(lesson_data['blocks']):
            if not isinstance(block, dict):
                return False, f"Block {i} must be an object"

            if 'type' not in block:
                return False, f"Block {i} missing 'type' field"

            if 'content' not in block:
                return False, f"Block {i} missing 'content' field"

            if block['type'] not in valid_block_types:
                return False, f"Block {i} has invalid type: {block['type']}. Must be one of: {valid_block_types}"

            # Validate content based on type
            if block['type'] == 'interactive':
                if not isinstance(block['content'], dict):
                    return False, f"Block {i} interactive content must be an object"
                if 'type' not in block['content']:
                    return False, f"Block {i} interactive content missing 'type' field"

        return True, "Valid"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_module_data(module_data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate module data structure."""
    try:
        required_fields = ['id', 'subject', 'stage', 'title', 'objectives_jsonb', 'lesson_policy_jsonb', 'assessment_blueprint_jsonb']

        for field in required_fields:
            if field not in module_data:
                return False, f"Missing required field: {field}"

        # Validate JSONB fields
        jsonb_fields = ['objectives_jsonb', 'lesson_policy_jsonb', 'assessment_blueprint_jsonb']
        for field in jsonb_fields:
            try:
                json.loads(module_data[field])
            except (json.JSONDecodeError, TypeError):
                return False, f"Invalid JSON in field {field}"

        # Validate recommended_hours if provided
        if 'recommended_hours' in module_data:
            try:
                hours = int(module_data['recommended_hours'])
                if hours <= 0:
                    return False, f"recommended_hours must be positive, got: {hours}"
            except (ValueError, TypeError):
                return False, f"Invalid recommended_hours format: {module_data['recommended_hours']}"

        return True, "Valid"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_learning_state_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validate learning state data."""
    try:
        # Validate mastery JSONB
        if 'mastery_jsonb' in data:
            try:
                mastery = json.loads(data['mastery_jsonb'])
                if not isinstance(mastery, dict):
                    return False, "mastery_jsonb must be a JSON object"
            except (json.JSONDecodeError, TypeError):
                return False, "Invalid JSON in mastery_jsonb"

        # Validate counters JSONB
        if 'counters_jsonb' in data:
            try:
                counters = json.loads(data['counters_jsonb'])
                if not isinstance(counters, dict):
                    return False, "counters_jsonb must be a JSON object"
            except (json.JSONDecodeError, TypeError):
                return False, "Invalid JSON in counters_jsonb"

        # Validate current_lesson_type
        if 'current_lesson_type' in data and not validate_lesson_type(data['current_lesson_type']):
            return False, f"Invalid current_lesson_type: {data['current_lesson_type']}"

        return True, "Valid"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_database_integrity(conn) -> Dict[str, str]:
    """Validate database integrity and return report."""
    report = {}

    try:
        with conn.cursor() as cur:
            # Check for orphaned records
            cur.execute("""
                SELECT COUNT(*) FROM learning_state ls
                LEFT JOIN student s ON ls.student_id = s.id
                WHERE s.id IS NULL
            """)
            orphaned_learning_states = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*) FROM learning_state ls
                LEFT JOIN module m ON ls.module_id = m.id
                WHERE m.id IS NULL
            """)
            orphaned_modules = cur.fetchone()[0]

            cur.execute("""
                SELECT COUNT(*) FROM submission s
                LEFT JOIN module m ON s.module_id = m.id
                WHERE m.id IS NULL
            """)
            orphaned_submissions = cur.fetchone()[0]

            # Check for invalid JSONB (simplified check)
            cur.execute("""
                SELECT COUNT(*) FROM module
                WHERE objectives_jsonb::text = '{}'::text
                   OR lesson_policy_jsonb::text = '{}'::text
                   OR assessment_blueprint_jsonb::text = '{}'::text
            """)
            invalid_jsonb = cur.fetchone()[0]

            report = {
                "orphaned_learning_states": orphaned_learning_states,
                "orphaned_modules_in_learning_state": orphaned_modules,
                "orphaned_submissions": orphaned_submissions,
                "invalid_jsonb_modules": invalid_jsonb
            }

    except Exception as e:
        report["error"] = str(e)

    return report
