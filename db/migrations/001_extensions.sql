-- UP
CREATE EXTENSION IF NOT EXISTS pgcrypto;   -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- на всякий (не обязателен)

-- DOWN
-- Расширения обычно не удаляют в down, но если нужно:
-- DROP EXTENSION IF EXISTS "uuid-ossp";
-- DROP EXTENSION IF EXISTS pgcrypto;
