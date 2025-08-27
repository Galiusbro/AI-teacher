-- UP
BEGIN;

CREATE TABLE diagnostic_session (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  context_jsonb JSONB NOT NULL,
  results_jsonb JSONB,
  persona_jsonb JSONB,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE diagnostic_item_result (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL REFERENCES diagnostic_session(id) ON DELETE CASCADE,
  item_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  level INT NOT NULL,
  answer_jsonb JSONB NOT NULL,
  is_correct BOOLEAN,
  time_spent_sec INT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE persona_profile (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL UNIQUE REFERENCES student(id) ON DELETE CASCADE,
  traits_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb,
  style_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb,
  interests_jsonb JSONB NOT NULL DEFAULT '[]'::jsonb,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMIT;

-- DOWN
BEGIN;
DROP TABLE IF EXISTS persona_profile;
DROP TABLE IF EXISTS diagnostic_item_result;
DROP TABLE IF EXISTS diagnostic_session;
COMMIT;
