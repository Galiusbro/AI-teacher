отлично — ниже **чёткий ERD** для нашей системы ИИ-учителя. Он покрывает контент (curriculum→modules→уроки), пользователей (ученик/родитель/преподаватель), обучение (состояние/попытки/сабмиты), оценивание и подтверждение родителем. Делаю в двух слоях: **минимальный МVP** и **расширения**, чтобы было понятно, что можно добавить потом.

---

# 🗺️ Логическая модель (MVP)

```
Subject ──< StageSubject >── Stage
   │                         │
   │                         └──< Module >──┐
   │                                        │
   └────────────────────────────────────────┘

User ──1──│──1── Student
  │       │
  │       └──0..1── Parent (также User с ролью parent)
  │
  └──*── Enrollment ──*── Module

Module ──1──<─ LearningState ──1── Student
     │                │
     │                └──< Attempt
     │                         │
     │                         └──< Submission ──0..1── ParentSignoff
     │
     └──0..*── LessonTemplate  (кэш/фиксируемые уроки; иначе генерируем на лету)
```

---

# 📦 Сущности и ключевые поля

## 1) Контент

**Subject**

* `id (PK)`, `code UNIQUE`, `title`, `locales jsonb`
* Индексы: `code`, FTS по `title`

**Stage**

* `id (PK)`, `code UNIQUE` (`stage_primary|lower_secondary|upper_secondary|advanced`), `title`, `age_min`, `age_max`

**StageSubject** (связка многих-ко-многим)

* `stage_id (FK Stage)`, `subject_id (FK Subject)` — PK составной

**Module**

* `id (PK)`, `subject_id (FK)`, `stage_id (FK)`, `code UNIQUE`, `title`,
  `recommended_hours int`,
  `objectives_jsonb`, `lesson_policy_jsonb`, `assessment_blueprint_jsonb`,
  `version`, `status ('active','draft','archived')`,
  `created_at`, `updated_at`
* Индексы: `subject_id, stage_id`, GIN на `objectives_jsonb`

**LessonTemplate** (опционально; если фиксируем/кэшируем уроки)

* `id (PK text)` — например, `lesson_math_shapes_guided_01`
* `module_id (FK Module)`, `type ('concept','guided','independent','assessment',...)`,
  `schema_version`, `payload_jsonb` (валидный Lesson JSON по нашей схеме),
  `status`, `created_at`, `updated_at`
* Индексы: `module_id,type`, GIN на `payload_jsonb`

**Resource** (внешние источники/ссылки)

* `id (PK)`, `kind ('video','simulation','doc','dataset','image')`,
  `url`, `meta_jsonb`, `created_at`

---

## 2) Пользователи и роли

**User**

* `id (PK)`, `email UNIQUE`, `password_hash`, `role ('admin','teacher','student','parent')`,
  `locale`, `created_at`, `updated_at`

**Student**

* `id (PK)`, `user_id (FK User) UNIQUE`,
  `dob`, `grade_hint`, `settings_jsonb` (адаптивность/ДП)
* Индексы: `user_id`

**Parent**

* (вариант A) отдельная таблица: `id (PK)`, `user_id (FK User) UNIQUE`
* (вариант B) не делать таблицу, а хранить через `User.role='parent'` и связь с учеником в ParentLink

**ParentLink**

* `id (PK)`, `student_id (FK Student)`, `parent_user_id (FK User)`, `relation ('mother','father','guardian')`
* Уникальность: `(student_id, parent_user_id)`

**Teacher** (опционально)

* `id (PK)`, `user_id (FK User) UNIQUE`, `subjects jsonb`

**Enrollment** (запись ученика на предмет/стейдж/курс)

* `id (PK)`, `student_id (FK)`, `subject_id (FK)`, `stage_id (FK)`,
  `curriculum_version`, `started_at`, `status ('active','paused','completed')`
* Уникальность: `(student_id, subject_id, stage_id, curriculum_version)`

---

## 3) Обучение и оценивание

**LearningState** (состояние по модулю для ученика)

* `id (PK)`, `student_id (FK)`, `module_id (FK)`,
  `current_lesson_type`,
  `mastery_jsonb` (например: `{"overall":0.72,"concept":0.9,"guided":0.65,"independent":0.55}`),
  `counters_jsonb` (например: `{"concept":2,"guided":1,"independent":0,"assessment":0}`),
  `next_recommended`, `updated_at`
* Уникальность: `(student_id, module_id)`
* Индексы: `student_id,module_id`, GIN на `mastery_jsonb`

**Attempt** (попытка прохождения интерактива/квиза)

* `id (PK)`, `student_id (FK)`, `module_id (FK)`,
  `lesson_id TEXT NULL` (если урок кэшировался), `interactive_id TEXT`,
  `payload_jsonb` (ответы/события/телеметрия), `score NUMERIC`, `created_at`
* Индексы: `student_id,module_id,created_at`, GIN на `payload_jsonb`

**Submission** (сабмит задания/домашки/экзамена)

* `id (PK)`, `student_id (FK)`, `module_id (FK)`,
  `lesson_id TEXT NULL`, `task_id TEXT`,
  `kind ('practice','homework','project','lab','assessment')`,
  `answer_jsonb` (structured), `artifacts jsonb` (ссылки на файлы в S3),
  `score NUMERIC`, `rubric_jsonb`, `graded_by (FK User NULL)`, `created_at`
* Индексы: `student_id,module_id,kind`, GIN на `answer_jsonb`

**ParentSignoff** (подтверждение родителя)

* `id (PK)`, `submission_id (FK Submission) UNIQUE`,
  `parent_user_id (FK User)`, `signed_at`, `method ('pin','oauth','link')`, `meta_jsonb`

**AuditLog**

* `id (PK)`, `actor_user_id (FK User)`, `action`, `entity`, `entity_id`,
  `diff_jsonb`, `created_at`
* Индексы: `actor_user_id,entity,created_at`

---

# 🧠 Поток данных (как это живёт)

1. **Контент**: Subject/Stage/Module занесены в БД (структурные поля + `jsonb` с objectives/policy).
2. **Генерация урока**:

   * `/api/lessons/generate`: вход `module_id`, `type`, `student_profile` → на выход **Lesson JSON** (валидный по схеме).
   * По желанию — кешируем в `LessonTemplate`.
3. **Прохождение урока**:

   * UI рисует `interactives` → ответы уходят в `Attempt` и/или `Submission`.
4. **Оценка и маршрут**:

   * Сервис обновляет `LearningState.mastery_jsonb` и `counters_jsonb`.
   * По `lesson_policy_jsonb` определяет `next_recommended`.
   * Если `assessment.proctoring.parent_signoff_required=true` → создаётся запись `ParentSignoff`.

---

# 🧩 Мини-SQL (PostgreSQL) — MVP таблицы

```sql
CREATE TABLE subject (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  locales JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE stage (
  id UUID PRIMARY KEY,
  code TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  age_min INT NOT NULL,
  age_max INT NOT NULL
);

CREATE TABLE stage_subject (
  stage_id UUID NOT NULL REFERENCES stage(id) ON DELETE CASCADE,
  subject_id UUID NOT NULL REFERENCES subject(id) ON DELETE CASCADE,
  PRIMARY KEY (stage_id, subject_id)
);

CREATE TABLE module (
  id UUID PRIMARY KEY,
  subject_id UUID NOT NULL REFERENCES subject(id) ON DELETE CASCADE,
  stage_id UUID NOT NULL REFERENCES stage(id) ON DELETE CASCADE,
  code TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  recommended_hours INT,
  objectives_jsonb JSONB NOT NULL,
  lesson_policy_jsonb JSONB NOT NULL,
  assessment_blueprint_jsonb JSONB NOT NULL,
  version TEXT NOT NULL DEFAULT '1.0.0',
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE app_user (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('admin','teacher','student','parent')),
  locale TEXT DEFAULT 'en',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE student (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL UNIQUE REFERENCES app_user(id) ON DELETE CASCADE,
  dob DATE,
  grade_hint TEXT,
  settings_jsonb JSONB DEFAULT '{}'::jsonb
);

CREATE TABLE parent_link (
  id UUID PRIMARY KEY,
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  parent_user_id UUID NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
  relation TEXT,
  UNIQUE (student_id, parent_user_id)
);

CREATE TABLE enrollment (
  id UUID PRIMARY KEY,
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  subject_id UUID NOT NULL REFERENCES subject(id),
  stage_id UUID NOT NULL REFERENCES stage(id),
  curriculum_version TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  started_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (student_id, subject_id, stage_id, curriculum_version)
);

CREATE TABLE learning_state (
  id UUID PRIMARY KEY,
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  module_id UUID NOT NULL REFERENCES module(id) ON DELETE CASCADE,
  current_lesson_type TEXT CHECK (current_lesson_type IN ('concept','guided','independent','assessment','revision','project','lab')),
  mastery_jsonb JSONB NOT NULL DEFAULT '{"overall":0}'::jsonb,
  counters_jsonb JSONB NOT NULL DEFAULT '{}'::jsonb,
  next_recommended TEXT,
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (student_id, module_id)
);

CREATE TABLE attempt (
  id UUID PRIMARY KEY,
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  module_id UUID NOT NULL REFERENCES module(id) ON DELETE CASCADE,
  lesson_id TEXT,
  interactive_id TEXT,
  payload_jsonb JSONB NOT NULL,
  score NUMERIC,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE submission (
  id UUID PRIMARY KEY,
  student_id UUID NOT NULL REFERENCES student(id) ON DELETE CASCADE,
  module_id UUID NOT NULL REFERENCES module(id) ON DELETE CASCADE,
  lesson_id TEXT,
  task_id TEXT,
  kind TEXT NOT NULL CHECK (kind IN ('practice','homework','project','lab','assessment')),
  answer_jsonb JSONB NOT NULL,
  artifacts JSONB,        -- ссылки на файлы (S3)
  score NUMERIC,
  rubric_jsonb JSONB,
  graded_by UUID REFERENCES app_user(id),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE parent_signoff (
  id UUID PRIMARY KEY,
  submission_id UUID NOT NULL UNIQUE REFERENCES submission(id) ON DELETE CASCADE,
  parent_user_id UUID NOT NULL REFERENCES app_user(id),
  signed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  method TEXT NOT NULL CHECK (method IN ('pin','oauth','link')),
  meta_jsonb JSONB
);

CREATE TABLE audit_log (
  id UUID PRIMARY KEY,
  actor_user_id UUID REFERENCES app_user(id),
  action TEXT NOT NULL,
  entity TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  diff_jsonb JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

> Плюс GIN-индексы:

```sql
CREATE INDEX module_objectives_gin ON module USING GIN (objectives_jsonb);
CREATE INDEX learning_state_mastery_gin ON learning_state USING GIN (mastery_jsonb);
CREATE INDEX attempt_payload_gin ON attempt USING GIN (payload_jsonb);
CREATE INDEX submission_answer_gin ON submission USING GIN (answer_jsonb);
```

---

# 🔧 Что дальше (практика)

1. Утверждаем ERD (можно сразу так и пилить).
2. Пишем миграции и сидируем **Subject / Stage / Module** из твоих готовых JSON.
3. Добавляем эндпоинты:

   * `POST /api/lessons/generate` → отдаёт Lesson JSON по `module_id + type + профилю`.
   * `POST /api/next` → читает `LearningState` и возвращает следующий тип + Lesson JSON.
   * `POST /api/submissions` → сохраняет ответы/артефакты, триггерит апдейт `LearningState`.
4. Подключаем S3/CDN для медиа.

