-- Создание диагностических вопросов для тестирования системы

-- Получаем UUIDы предметов и уровней
DO $$
DECLARE
    math_subject_id UUID;
    primary_stage_id UUID;
    question_id UUID;
BEGIN
    -- Находим предмет "Mathematics"
    SELECT id INTO math_subject_id FROM subject WHERE code = 'Mathematics';
    IF math_subject_id IS NULL THEN
        RAISE NOTICE 'Предмет Mathematics не найден, создаем его...';
        INSERT INTO subject (code, title, locales) VALUES
        ('Mathematics', 'Математика', '{"ru": "Математика", "en": "Mathematics"}')
        RETURNING id INTO math_subject_id;
    END IF;

    -- Находим уровень "stage_primary"
    SELECT id INTO primary_stage_id FROM stage WHERE code = 'stage_primary';
    IF primary_stage_id IS NULL THEN
        RAISE NOTICE 'Уровень stage_primary не найден, создаем его...';
        INSERT INTO stage (code, title, age_min, age_max) VALUES
        ('stage_primary', 'Начальная школа', 6, 11)
        RETURNING id INTO primary_stage_id;
    END IF;

    RAISE NOTICE 'Создаем диагностические вопросы для Mathematics...';

    -- Вопросы уровня beginner
    INSERT INTO diagnostic_question (
        subject_id, stage_id, difficulty_level, question_type,
        content_jsonb, correct_answer_jsonb, explanation_jsonb,
        time_limit_sec, points
    ) VALUES
    (
        math_subject_id, primary_stage_id, 'easy', 'mcq',
        '{
            "question": "Сколько будет 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "instruction": "Выберите правильный ответ"
        }'::jsonb,
        '{"correct_option": 1}'::jsonb,
        '{"explanation": "2 + 2 = 4, потому что 2 яблока + 2 яблока = 4 яблока"}'::jsonb,
        60, 1
    ),
    (
        math_subject_id, primary_stage_id, 'easy', 'mcq',
        '{
            "question": "Какое число больше: 5 или 3?",
            "options": ["3", "5", "они равны", "не знаю"],
            "instruction": "Выберите правильный ответ"
        }'::jsonb,
        '{"correct_option": 1}'::jsonb,
        '{"explanation": "5 больше чем 3, потому что 5 содержит 3 и ещё 2"}'::jsonb,
        60, 1
    ),
    (
        math_subject_id, primary_stage_id, 'easy', 'mcq',
        '{
            "question": "Сколько пальцев на одной руке?",
            "options": ["4", "5", "6", "10"],
            "instruction": "Выберите правильный ответ"
        }'::jsonb,
        '{"correct_option": 1}'::jsonb,
        '{"explanation": "На одной руке 5 пальцев: большой, указательный, средний, безымянный и мизинец"}'::jsonb,
        60, 1
    );

    -- Вопросы уровня elementary
    INSERT INTO diagnostic_question (
        subject_id, stage_id, difficulty_level, question_type,
        content_jsonb, correct_answer_jsonb, explanation_jsonb,
        time_limit_sec, points
    ) VALUES
    (
        math_subject_id, primary_stage_id, 'medium', 'mcq',
        '{
            "question": "Сколько будет 10 - 3?",
            "options": ["6", "7", "8", "13"],
            "instruction": "Выберите правильный ответ"
        }'::jsonb,
        '{"correct_option": 1}'::jsonb,
        '{"explanation": "10 - 3 = 7, потому что от 10 отнимаем 3 и получаем 7"}'::jsonb,
        90, 1
    ),
    (
        math_subject_id, primary_stage_id, 'medium', 'mcq',
        '{
            "question": "Сколько углов у треугольника?",
            "options": ["2", "3", "4", "5"],
            "instruction": "Выберите правильный ответ"
        }'::jsonb,
        '{"correct_option": 1}'::jsonb,
        '{"explanation": "Треугольник имеет 3 угла"}'::jsonb,
        90, 1
    ),
    (
        math_subject_id, primary_stage_id, 'medium', 'mcq',
        '{
            "question": "2 + 3 × 4 = ? (сначала умножение, потом сложение)",
            "options": ["20", "14", "24", "16"],
            "instruction": "Выберите правильный ответ"
        }'::jsonb,
        '{"correct_option": 1}'::jsonb,
        '{"explanation": "Сначала 3 × 4 = 12, потом 2 + 12 = 14"}'::jsonb,
        120, 2
    );

    -- Вопросы уровня intermediate
    INSERT INTO diagnostic_question (
        subject_id, stage_id, difficulty_level, question_type,
        content_jsonb, correct_answer_jsonb, explanation_jsonb,
        time_limit_sec, points
    ) VALUES
    (
        math_subject_id, primary_stage_id, 'hard', 'mcq',
        '{
            "question": "Найдите периметр прямоугольника со сторонами 6 см и 8 см",
            "options": ["14 см", "28 см", "48 см", "24 см"],
            "instruction": "Выберите правильный ответ"
        }'::jsonb,
        '{"correct_option": 1}'::jsonb,
        '{"explanation": "Периметр = 2 × (6 + 8) = 2 × 14 = 28 см"}'::jsonb,
        180, 2
    ),
    (
        math_subject_id, primary_stage_id, 'hard', 'mcq',
        '{
            "question": "Сколько будет 144 ÷ 12?",
            "options": ["10", "12", "14", "16"],
            "instruction": "Выберите правильный ответ"
        }'::jsonb,
        '{"correct_option": 1}'::jsonb,
        '{"explanation": "144 ÷ 12 = 12, потому что 12 × 12 = 144"}'::jsonb,
        180, 2
    ),
    (
        math_subject_id, primary_stage_id, 'hard', 'open_ended',
        '{
            "question": "У Марии 15 яблок. Она отдала 7 яблок друзьям. Сколько яблок у неё осталось?",
            "instruction": "Напишите число"
        }'::jsonb,
        '{"answer": "8"}'::jsonb,
        '{"explanation": "15 - 7 = 8 яблок осталось"}'::jsonb,
        180, 2
    );

    RAISE NOTICE 'Диагностические вопросы созданы успешно!';
END $$;
