-- Создание тестовых данных для демонстрации системы mastery

-- 1. Создаем тестового пользователя
INSERT INTO app_user (email, password_hash, role, locale)
VALUES ('test_student@example.com', '$2b$12$dummy.hash.for.testing', 'student', 'ru')
ON CONFLICT (email) DO NOTHING;

-- 2. Создаем студента
INSERT INTO student (user_id, grade_hint)
SELECT id, 'Year 5' FROM app_user WHERE email = 'test_student@example.com'
ON CONFLICT DO NOTHING;

-- 3. Найдем существующий модуль математики (или создадим тестовый)
DO $$
DECLARE
    student_uuid UUID;
    module_uuid UUID;
    module_code TEXT := 'module_math_numbers_primary';
BEGIN
    -- Получаем UUID студента
    SELECT s.id INTO student_uuid FROM student s
    JOIN app_user u ON s.user_id = u.id
    WHERE u.email = 'test_student@example.com';

    -- Проверяем, существует ли модуль математики
    SELECT id INTO module_uuid FROM module WHERE code = module_code;

    -- Если модуль не существует, создаем его
    IF module_uuid IS NULL THEN
        INSERT INTO module (
            subject_id,
            stage_id,
            code,
            title,
            recommended_hours,
            objectives_jsonb,
            lesson_policy_jsonb,
            assessment_blueprint_jsonb
        )
        SELECT
            subj.id,
            st.id,
            module_code,
            'Числа и счет',
            10,
            '{"objectives": ["Понимать понятие числа", "Уметь считать до 100"]}'::jsonb,
            '{"concept": 0.3, "guided": 0.3, "independent": 0.25, "assessment": 0.15}'::jsonb,
            '{"assessment": ["Тест на знание чисел"]}'::jsonb
        FROM subject subj
        CROSS JOIN stage st
        WHERE subj.code = 'Mathematics'
        AND st.code = 'stage_primary'
        RETURNING id INTO module_uuid;
    END IF;

    -- Создаем начальное состояние обучения
    INSERT INTO learning_state (
        student_id,
        module_id,
        current_lesson_type,
        mastery_jsonb,
        counters_jsonb,
        next_recommended
    ) VALUES (
        student_uuid,
        module_uuid,
        'concept',
        '{"overall": 0.0, "concept": 0.0, "guided": 0.0, "independent": 0.0, "assessment": 0.0}'::jsonb,
        '{"concept": 0, "guided": 0, "independent": 0, "assessment": 0}'::jsonb,
        'concept'
    ) ON CONFLICT (student_id, module_id) DO NOTHING;

    RAISE NOTICE 'Тестовые данные созданы. Student UUID: %, Module UUID: %', student_uuid, module_uuid;
END $$;
