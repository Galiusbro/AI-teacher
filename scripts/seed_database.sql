-- Seed script for basic curriculum data
-- Run this after applying all migrations

BEGIN;

-- Insert stages
INSERT INTO stage (code, title, age_min, age_max) VALUES
  ('stage_primary', 'Primary', 5, 11),
  ('stage_lower_secondary', 'Lower Secondary', 11, 14),
  ('stage_upper_secondary', 'Upper Secondary (IGCSE)', 14, 16),
  ('stage_advanced', 'Advanced (AS/A Level)', 16, 19)
ON CONFLICT (code) DO NOTHING;

-- Insert subjects
INSERT INTO subject (code, title, locales) VALUES
  ('Mathematics', 'Mathematics', '{"en":"Mathematics","ru":"Математика"}'),
  ('English', 'English', '{"en":"English","ru":"Английский"}'),
  ('Science', 'Science', '{"en":"Science","ru":"Естествознание"}'),
  ('Biology', 'Biology', '{"en":"Biology","ru":"Биология"}'),
  ('Chemistry', 'Chemistry', '{"en":"Chemistry","ru":"Химия"}'),
  ('Physics', 'Physics', '{"en":"Physics","ru":"Физика"}'),
  ('ICT', 'ICT', '{"en":"ICT","ru":"ИКТ"}'),
  ('ComputerScience', 'Computer Science', '{"en":"Computer Science","ru":"Информатика"}'),
  ('GlobalPerspectives', 'Global Perspectives', '{"en":"Global Perspectives","ru":"Глобальные перспективы"}'),
  ('Art', 'Art', '{"en":"Art","ru":"Искусство"}'),
  ('Business', 'Business', '{"en":"Business","ru":"Бизнес"}'),
  ('Economics', 'Economics', '{"en":"Economics","ru":"Экономика"}'),
  ('EnglishLiterature', 'English Literature', '{"en":"English Literature","ru":"Английская литература"}'),
  ('FurtherMathematics', 'Further Mathematics', '{"en":"Further Mathematics","ru":"Дополнительная математика"}'),
  ('Geography', 'Geography', '{"en":"Geography","ru":"География"}'),
  ('History', 'History', '{"en":"History","ru":"История"}'),
  ('Languages', 'Languages', '{"en":"Languages","ru":"Иностранные языки"}'),
  ('Music', 'Music', '{"en":"Music","ru":"Музыка"}'),
  ('PhysicalEducation', 'Physical Education', '{"en":"Physical Education","ru":"Физическая культура"}')
ON CONFLICT (code) DO NOTHING;

-- Create stage-subject relationships
-- All subjects are available for all stages, but some might be more relevant for certain stages
INSERT INTO stage_subject (stage_id, subject_id)
SELECT s.id, sub.id
FROM stage s
CROSS JOIN subject sub
ON CONFLICT (stage_id, subject_id) DO NOTHING;

COMMIT;

-- Verification query
SELECT
  st.title as stage,
  sub.title as subject,
  sub.code as subject_code
FROM stage st
JOIN stage_subject ss ON ss.stage_id = st.id
JOIN subject sub ON ss.subject_id = sub.id
ORDER BY st.age_min, sub.title;
