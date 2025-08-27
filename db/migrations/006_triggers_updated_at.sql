-- UP
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_subject_updated BEFORE UPDATE ON subject
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_stage_updated BEFORE UPDATE ON stage
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_module_updated BEFORE UPDATE ON module
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_lesson_template_updated BEFORE UPDATE ON lesson_template
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- DOWN
DROP TRIGGER IF EXISTS trg_lesson_template_updated ON lesson_template;
DROP TRIGGER IF EXISTS trg_module_updated ON module;
DROP TRIGGER IF EXISTS trg_stage_updated ON stage;
DROP TRIGGER IF EXISTS trg_subject_updated ON subject;
DROP FUNCTION IF EXISTS set_updated_at;
