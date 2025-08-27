-- UP
BEGIN;

CREATE TABLE app_user (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('admin','teacher','student','parent')),
  locale TEXT NOT NULL DEFAULT 'en',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE student (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL UNIQUE REFERENCES app_user(id) ON DELETE CASCADE,
  dob DATE,
  grade_hint TEXT,
  settings_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb
);

-- связь «родитель—ученик»
CREATE TABLE parent_link (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  parent_user_id UUID NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
  relation TEXT,
  UNIQUE (student_id, parent_user_id)
);

CREATE TABLE enrollment (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  subject_id UUID NOT NULL REFERENCES subject(id),
  stage_id UUID NOT NULL REFERENCES stage(id),
  curriculum_version TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active', -- active|paused|completed
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (student_id, subject_id, stage_id, curriculum_version)
);

COMMIT;

-- DOWN
BEGIN;
DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS parent_link;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS app_user;
COMMIT;
