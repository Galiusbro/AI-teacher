-- UP
BEGIN;

-- Таблица для начальной диагностики уровня ученика
CREATE TABLE diagnostic_session (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  subject_id UUID NOT NULL REFERENCES subject(id),
  stage_id UUID NOT NULL REFERENCES stage(id),
  status TEXT NOT NULL DEFAULT 'in_progress' CHECK (status IN ('in_progress','completed','abandoned')),
  estimated_level TEXT CHECK (estimated_level IN ('beginner','elementary','intermediate','advanced')),
  confidence_score NUMERIC CHECK (confidence_score >= 0 AND confidence_score <= 1),
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ,
  results_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb, -- детальные результаты диагностики
  recommendations_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb -- рекомендации по обучению
);

-- Таблица для диагностических вопросов/заданий
CREATE TABLE diagnostic_question (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id UUID NOT NULL REFERENCES subject(id),
  stage_id UUID NOT NULL REFERENCES stage(id),
  difficulty_level TEXT NOT NULL CHECK (difficulty_level IN ('beginner','elementary','intermediate','advanced')),
  question_type TEXT NOT NULL CHECK (question_type IN ('mcq','open_ended','interactive','problem_solving')),
  content_jsonb JSONB NOT NULL, -- текст вопроса, варианты ответов и т.д.
  correct_answer_jsonb JSONB NOT NULL, -- правильный ответ
  explanation_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb, -- объяснение
  time_limit_sec INTEGER, -- рекомендуемое время на ответ
  points INTEGER NOT NULL DEFAULT 1,
  active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Связь диагностических сессий с вопросами
CREATE TABLE diagnostic_response (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES diagnostic_session(id) ON DELETE CASCADE,
  question_id UUID NOT NULL REFERENCES diagnostic_question(id),
  student_answer_jsonb JSONB,
  is_correct BOOLEAN,
  time_spent_sec INTEGER,
  points_earned INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Расширяем таблицу student для хранения диагностической информации
ALTER TABLE student ADD COLUMN IF NOT EXISTS diagnostic_completed_at TIMESTAMPTZ;
ALTER TABLE student ADD COLUMN IF NOT EXISTS current_level TEXT CHECK (current_level IN ('beginner','elementary','intermediate','advanced'));
ALTER TABLE student ADD COLUMN IF NOT EXISTS recommended_difficulty TEXT DEFAULT 'medium' CHECK (recommended_difficulty IN ('easy','medium','hard','expert'));

-- Индексы для производительности
CREATE INDEX IF NOT EXISTS idx_diagnostic_session_student ON diagnostic_session(student_id);
CREATE INDEX IF NOT EXISTS idx_diagnostic_session_status ON diagnostic_session(status);
CREATE INDEX IF NOT EXISTS idx_diagnostic_question_subject_stage ON diagnostic_question(subject_id, stage_id);
CREATE INDEX IF NOT EXISTS idx_diagnostic_question_difficulty ON diagnostic_question(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_diagnostic_response_session ON diagnostic_response(session_id);

COMMIT;

-- DOWN
BEGIN;
DROP INDEX IF EXISTS idx_diagnostic_response_session;
DROP INDEX IF EXISTS idx_diagnostic_question_difficulty;
DROP INDEX IF EXISTS idx_diagnostic_question_subject_stage;
DROP INDEX IF EXISTS idx_diagnostic_session_status;
DROP INDEX IF EXISTS idx_diagnostic_session_student;

ALTER TABLE student DROP COLUMN IF EXISTS recommended_difficulty;
ALTER TABLE student DROP COLUMN IF EXISTS current_level;
ALTER TABLE student DROP COLUMN IF EXISTS diagnostic_completed_at;

DROP TABLE IF EXISTS diagnostic_response;
DROP TABLE IF EXISTS diagnostic_question;
DROP TABLE IF EXISTS diagnostic_session;
COMMIT;
