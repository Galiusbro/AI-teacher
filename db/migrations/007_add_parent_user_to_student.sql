-- UP
ALTER TABLE student ADD COLUMN parent_user_id UUID REFERENCES app_user(id) ON DELETE CASCADE;
ALTER TABLE student ALTER COLUMN user_id DROP NOT NULL;

-- Add index for better performance
CREATE INDEX idx_student_parent_user_id ON student(parent_user_id);

-- DOWN
-- ALTER TABLE student DROP COLUMN parent_user_id;
-- ALTER TABLE student ALTER COLUMN user_id SET NOT NULL;
-- DROP INDEX IF EXISTS idx_student_parent_user_id;
