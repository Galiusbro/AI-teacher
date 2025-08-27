-- UP
BEGIN;

-- опциональный кэш заранее сгенерированных уроков
CREATE TABLE lesson_template (
  id TEXT PRIMARY KEY, -- например: 'lesson_math_shapes_guided_01'
  module_id UUID NOT NULL REFERENCES module(id) ON DELETE CASCADE,
  type TEXT NOT NULL CHECK (type IN ('concept','guided','independent','assessment','revision','project','lab')),
  schema_version TEXT NOT NULL DEFAULT '1.0.0',
  payload_jsonb JSONB NOT NULL, -- валидный Lesson JSON по нашей схеме
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- состояние ученика в рамках модуля
CREATE TABLE learning_state (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  module_id UUID NOT NULL REFERENCES module(id) ON DELETE CASCADE,
  current_lesson_type TEXT CHECK (current_lesson_type IN ('concept','guided','independent','assessment','revision','project','lab')),
  mastery_jsonb JSONB NOT NULL DEFAULT '{"overall":0}'::jsonb, -- {"overall":0.72,"concept":0.9,...}
  counters_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb,          -- {"concept":2,"guided":1,...}
  next_recommended TEXT,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (student_id, module_id)
);

-- попытки (интерактивы/квизы)
CREATE TABLE attempt (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  module_id UUID NOT NULL REFERENCES module(id) ON DELETE CASCADE,
  lesson_id TEXT,       -- если использовали lesson_template
  interactive_id TEXT,  -- локальный id виджета
  payload_jsonb JSONB NOT NULL, -- ответы/телеметрия
  score NUMERIC,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- сабмиты заданий/домашки/экзаменов
CREATE TABLE submission (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  module_id UUID NOT NULL REFERENCES module(id) ON DELETE CASCADE,
  lesson_id TEXT,
  task_id TEXT,
  kind TEXT NOT NULL CHECK (kind IN ('practice','homework','project','lab','assessment')),
  answer_jsonb JSONB NOT NULL,
  artifacts JSONB,      -- ссылки на S3: {"files":[{"url":"s3://...","type":"photo"}]}
  score NUMERIC,
  rubric_jsonb JSONB,
  graded_by UUID REFERENCES app_user(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- подтверждение родителя
CREATE TABLE parent_signoff (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  submission_id UUID NOT NULL UNIQUE REFERENCES submission(id) ON DELETE CASCADE,
  parent_user_id UUID NOT NULL REFERENCES app_user(id),
  signed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  method TEXT NOT NULL CHECK (method IN ('pin','oauth','link')),
  meta_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb
);

-- аудит
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_user_id UUID REFERENCES app_user(id),
  action TEXT NOT NULL,
  entity TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  diff_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMIT;

-- DOWN
BEGIN;
DROP TABLE IF EXISTS audit_log;
DROP TABLE IF EXISTS parent_signoff;
DROP TABLE IF EXISTS submission;
DROP TABLE IF EXISTS attempt;
DROP TABLE IF EXISTS learning_state;
DROP TABLE IF EXISTS lesson_template;
COMMIT;
