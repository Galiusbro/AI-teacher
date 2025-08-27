-- UP
CREATE INDEX IF NOT EXISTS idx_module_subject_stage ON module (subject_id, stage_id);
CREATE INDEX IF NOT EXISTS idx_module_objectives_gin ON module USING GIN (objectives_jsonb);
CREATE INDEX IF NOT EXISTS idx_module_policy_gin ON module USING GIN (lesson_policy_jsonb);
CREATE INDEX IF NOT EXISTS idx_module_assess_gin ON module USING GIN (assessment_blueprint_jsonb);

CREATE INDEX IF NOT EXISTS idx_enrollment_student ON enrollment (student_id);
CREATE INDEX IF NOT EXISTS idx_enrollment_subject_stage ON enrollment (subject_id, stage_id);

CREATE INDEX IF NOT EXISTS idx_learning_state_student_module ON learning_state (student_id, module_id);
CREATE INDEX IF NOT EXISTS idx_learning_state_mastery_gin ON learning_state USING GIN (mastery_jsonb);
CREATE INDEX IF NOT EXISTS idx_learning_state_counters_gin ON learning_state USING GIN (counters_jsonb);

CREATE INDEX IF NOT EXISTS idx_attempt_student_time ON attempt (student_id, created_at);
CREATE INDEX IF NOT EXISTS idx_attempt_payload_gin ON attempt USING GIN (payload_jsonb);

CREATE INDEX IF NOT EXISTS idx_submission_student_kind ON submission (student_id, kind);
CREATE INDEX IF NOT EXISTS idx_submission_answer_gin ON submission USING GIN (answer_jsonb);

CREATE INDEX IF NOT EXISTS idx_audit_entity_time ON audit_log (entity, created_at);

-- DOWN
DROP INDEX IF EXISTS idx_audit_entity_time;
DROP INDEX IF EXISTS idx_submission_answer_gin;
DROP INDEX IF EXISTS idx_submission_student_kind;
DROP INDEX IF EXISTS idx_attempt_payload_gin;
DROP INDEX IF EXISTS idx_attempt_student_time;
DROP INDEX IF EXISTS idx_learning_state_counters_gin;
DROP INDEX IF EXISTS idx_learning_state_mastery_gin;
DROP INDEX IF EXISTS idx_learning_state_student_module;
DROP INDEX IF EXISTS idx_enrollment_subject_stage;
DROP INDEX IF EXISTS idx_enrollment_student;
DROP INDEX IF EXISTS idx_module_assess_gin;
DROP INDEX IF EXISTS idx_module_policy_gin;
DROP INDEX IF EXISTS idx_module_objectives_gin;
DROP INDEX IF EXISTS idx_module_subject_stage;
