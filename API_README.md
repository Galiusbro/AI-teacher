# Ayaal Teacher API

Простой REST API для образовательной платформы Ayaal Teacher.

## 🚀 Запуск

```bash
# Активировать виртуальное окружение
source venv/bin/activate

# Запустить API (порт 3000)
python api.py

# Или указать другой порт
PORT=5000 python api.py
```

## 📚 API Эндпоинты

### 1. Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### 2. Database Validation
```http
GET /api/validate/database
```

**Response:**
```json
{
  "status": "valid",
  "message": "Database integrity is valid",
  "report": {
    "orphaned_learning_states": 0,
    "orphaned_modules_in_learning_state": 0,
    "orphaned_submissions": 0,
    "invalid_jsonb_modules": 0
  }
}
```

### 3. Lesson Validation
```http
POST /api/validate/lesson
```

**Request:**
```json
{
  "id": "lesson_id",
  "type": "concept",
  "title": "Lesson Title",
  "locale": "ru",
  "blocks": [...]
}
```

**Response:**
```json
{
  "valid": true,
  "message": "Valid"
}
```

### 4. Генерация урока
```http
POST /api/lessons/generate
```

**Request:**
```json
{
  "module_code": "module_math_numbers_primary",
  "lesson_type": "concept",
  "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
  "locale": "ru",
  "use_ai": false
}
```

**Параметры:**
- `use_ai` (boolean, optional) - использовать AI генерацию (требует GROQ_API_KEY)

**Response:**
```json
{
  "id": "lesson_module_math_numbers_primary_concept_01",
  "type": "concept",
  "title": "Основы чисел и счёта",
  "locale": "ru",
  "_generated_with": "ai",
  "blocks": [
    {
      "type": "theory",
      "content": {
        "title": "Что такое числа?",
        "text": "Числа помогают нам считать предметы, измерять и решать задачи..."
      }
    },
    {
      "type": "example",
      "content": {
        "title": "Пример",
        "text": "У Маши 3 яблока, у Пети 2 яблока. Сколько всего яблок?"
      }
    },
    {
      "type": "interactive",
      "content": {
        "type": "mcq",
        "question": "Сколько будет 2 + 3?",
        "options": ["3", "4", "5", "6"],
        "correct": 2,
        "explanation": "2 + 3 = 5, потому что..."
      }
    }
  ]
}
```

**Метаданные:**
- `_generated_with`: `"ai"` или `"template"` - метод генерации

### 5. Следующий урок
```http
POST /api/next
```

**Request:**
```json
{
  "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
  "module_code": "module_math_numbers_primary"
}
```

**Response:**
```json
{
  "next_lesson_type": "concept",
  "reason": "Низкий уровень освоения - начать с основ",
  "lesson": { /* Lesson JSON */ },
  "current_mastery": 0.0
}
```

### 6. Отправка ответа
```http
POST /api/submissions
```

**Request:**
```json
{
  "student_id": "95ef01b7-ebfd-4320-a41b-9550e88551b5",
  "module_code": "module_math_numbers_primary",
  "lesson_id": "lesson_module_math_numbers_primary_concept_01",
  "task_id": "task_practice_1",
  "kind": "practice",
  "answer_jsonb": {"mcq_correct": 4, "mcq_total": 5},
  "score": 0.8,
  "interactive_id": "mcq_2_plus_3"
}
```

**Response:**
```json
{
  "success": true,
  "submission_id": "6ddf5f7e-c05c-488c-a4be-dca216730618",
  "created_at": "2025-08-27T02:16:43.221292+07:00"
}
```

## 🗄️ База данных

API работает с PostgreSQL базой данных `ayaal_teacher`. Основные таблицы:

- `app_user` - пользователи
- `student` - ученики
- `module` - учебные модули
- `learning_state` - состояние обучения
- `submission` - отправленные ответы
- `attempt` - попытки выполнения интерактивов

## 🔧 Настройка

### Переменные окружения:
- `DB_HOST` - хост PostgreSQL (по умолчанию: localhost)
- `DB_PORT` - порт PostgreSQL (по умолчанию: 5432)
- `DB_NAME` - имя базы данных (по умолчанию: ayaal_teacher)
- `DB_USER` - пользователь БД (по умолчанию: gp)
- `DB_PASSWORD` - пароль БД (по умолчанию: пустой)
- `PORT` - порт для Flask API (по умолчанию: 3000)

### AI Генерация (опционально):
- `GROQ_API_KEY` - API ключ для Groq (требуется для AI генерации)

### Тестовые данные:
- **Студент:** student@example.com
- **ID студента:** 95ef01b7-ebfd-4320-a41b-9550e88551b5
- **Тестовый модуль:** module_math_numbers_primary

## 🧪 Тестирование

### Основные эндпоинты
```bash
# Health check
curl http://localhost:3000/api/health

# Генерация урока (шаблон)
curl -X POST http://localhost:3000/api/lessons/generate \
  -H "Content-Type: application/json" \
  -d '{"module_code":"module_math_numbers_primary","lesson_type":"concept","student_id":"95ef01b7-ebfd-4320-a41b-9550e88551b5","locale":"ru","use_ai":false}'

# Генерация урока (AI)
curl -X POST http://localhost:3000/api/lessons/generate \
  -H "Content-Type: application/json" \
  -d '{"module_code":"module_math_numbers_primary","lesson_type":"concept","student_id":"95ef01b7-ebfd-4320-a41b-9550e88551b5","locale":"ru","use_ai":true}'

# Следующий урок
curl -X POST http://localhost:3000/api/next \
  -H "Content-Type: application/json" \
  -d '{"student_id":"95ef01b7-ebfd-4320-a41b-9550e88551b5","module_code":"module_math_numbers_primary"}'

# Отправка ответа
curl -X POST http://localhost:3000/api/submissions \
  -H "Content-Type: application/json" \
  -d '{"student_id":"95ef01b7-ebfd-4320-a41b-9550e88551b5","module_code":"module_math_numbers_primary","lesson_id":"lesson_concept_01","task_id":"task_1","kind":"practice","answer_jsonb":{"correct":true},"score":1.0}'
```

### Валидация
```bash
# Проверка целостности базы данных
curl http://localhost:3000/api/validate/database

# Валидация структуры урока
curl -X POST http://localhost:3000/api/validate/lesson \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test_lesson",
    "type": "concept",
    "title": "Test Lesson",
    "locale": "ru",
    "blocks": [
      {"type": "theory", "content": {"title": "Test", "text": "Test content"}}
    ]
  }'

# Комплексное тестирование валидации
python test_validation.py

# Комплексное тестирование AI генерации
python test_ai_generation.py
```

## 📊 Проверка данных

```sql
-- Количество модулей по предметам
SELECT s.title, COUNT(*) FROM module m JOIN subject s ON m.subject_id=s.id GROUP BY s.title ORDER BY 2 DESC;

-- Состояние обучения студента
SELECT m.code, ls.mastery_jsonb, ls.counters_jsonb FROM learning_state ls JOIN module m ON ls.module_id=m.id;

-- Отправленные ответы
SELECT COUNT(*) FROM submission;
SELECT COUNT(*) FROM attempt;
```
