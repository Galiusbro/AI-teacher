-- UP
BEGIN;

CREATE TABLE subject (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  locales JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE stage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code TEXT UNIQUE NOT NULL,  -- stage_primary | stage_lower_secondary | stage_upper_secondary | stage_advanced
  title TEXT NOT NULL,
  age_min INT NOT NULL,
  age_max INT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE stage_subject (
  stage_id UUID NOT NULL REFERENCES stage(id) ON DELETE CASCADE,
  subject_id UUID NOT NULL REFERENCES subject(id) ON DELETE CASCADE,
  PRIMARY KEY (stage_id, subject_id)
);

CREATE TABLE module (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subject_id UUID NOT NULL REFERENCES subject(id) ON DELETE CASCADE,
  stage_id UUID NOT NULL REFERENCES stage(id) ON DELETE CASCADE,
  code TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  recommended_hours INT,
  objectives_jsonb JSONB NOT NULL,
  lesson_policy_jsonb JSONB NOT NULL,
  assessment_blueprint_jsonb JSONB NOT NULL,
  version TEXT NOT NULL DEFAULT '1.0.0',
  status TEXT NOT NULL DEFAULT 'active', -- draft|active|archived
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE resource (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  kind TEXT NOT NULL CHECK (kind IN ('video','simulation','doc','dataset','image','link')),
  url TEXT NOT NULL,
  meta_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMIT;

-- DOWN
BEGIN;
DROP TABLE IF EXISTS resource;
DROP TABLE IF EXISTS module;
DROP TABLE IF EXISTS stage_subject;
DROP TABLE IF EXISTS stage;
DROP TABLE IF EXISTS subject;
COMMIT;
