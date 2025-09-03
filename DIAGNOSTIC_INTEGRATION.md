# Интеграция системы диагностики во фронтенд

## 🎯 Обзор

Система диагностики знаний ученика полностью интегрирована во фронтенд приложения. Студенты могут проходить адаптивную диагностику, получать персональные планы обучения и отслеживать свой прогресс.

## 🏗️ Архитектура интеграции

### Backend API Endpoints

Добавлены следующие API endpoints в `api.py`:

#### 1. `/api/diagnostic/start` (POST)
Запуск диагностической сессии для ученика.

**Параметры:**
```json
{
  "student_id": "string",
  "age": number,
  "subjects": ["Mathematics", "English", "Science"]
}
```

**Ответ:**
```json
{
  "student_id": "string",
  "age": number,
  "subjects": ["string"],
  "profile_created": true
}
```

#### 2. `/api/diagnostic/question` (POST)
Получение следующего диагностического вопроса.

**Параметры:**
```json
{
  "student_id": "string",
  "subject": "string"
}
```

**Ответ:**
```json
{
  "question": {
    "id": "string",
    "subject": "string",
    "difficulty_level": "beginner|elementary|intermediate|advanced|expert",
    "question_type": "dialogue|mcq_single|numeric|short_text",
    "content": {
      "question": "string",
      "options": ["string"],
      "correct_answer": "string"
    },
    "target_age": number
  }
}
```

#### 3. `/api/diagnostic/answer` (POST)
Отправка ответа на диагностический вопрос.

**Параметры:**
```json
{
  "student_id": "string",
  "question_id": "string",
  "answer": "string",
  "time_spent_sec": number
}
```

**Ответ:**
```json
{
  "result": {
    "is_correct": boolean,
    "confidence_score": number,
    "new_difficulty_level": "string"
  },
  "question_id": "string"
}
```

#### 4. `/api/diagnostic/plan/<student_id>` (GET)
Получение персонального плана обучения.

**Ответ:**
```json
{
  "student_id": "string",
  "plan": {
    "overall_level": "string",
    "subject_breakdown": {
      "subject": {
        "current_level": "string",
        "questions_asked": number,
        "correct_answers": number,
        "total_time_spent": number
      }
    },
    "strengths": ["string"],
    "weaknesses": ["string"],
    "psychological_profile": {
      "communication_style": "expressive|calm",
      "samples": ["string"]
    },
    "recommendations": {
      "immediate_focus": ["string"],
      "study_schedule": {
        "daily_time": number,
        "preferred_subjects": ["string"]
      },
      "teaching_approach": "creative|structured"
    }
  }
}
```

#### 5. `/api/diagnostic/export/<student_id>` (GET)
Экспорт данных диагностической сессии для сохранения в БД.

### Frontend Components

#### 1. `DiagnosticTest.tsx`
Основной компонент для прохождения диагностики.

**Функции:**
- Запуск диагностической сессии
- Отображение вопросов с таймером
- Обработка различных типов вопросов (диалоговые, MCQ, текстовые)
- Адаптивная навигация между предметами
- Отображение результатов в реальном времени

**Использование:**
```tsx
<DiagnosticTest
  studentId={user.user_id}
  age={12}
  subjects={['Mathematics', 'English', 'Science']}
  onComplete={handleDiagnosticComplete}
  onClose={() => setShowDiagnostic(false)}
/>
```

#### 2. `DiagnosticResults.tsx`
Компонент для отображения результатов диагностики.

**Функции:**
- Отображение общего уровня знаний
- Детализация по предметам
- Психологический профиль
- Рекомендации по обучению
- Визуализация прогресса

**Использование:**
```tsx
<DiagnosticResults
  plan={learningPlan}
  onClose={() => setShowResults(false)}
  onStartLearning={handleStartLearning}
/>
```

#### 3. `StudentDashboard.tsx`
Главная страница для студентов с интеграцией диагностики.

**Функции:**
- Проверка статуса диагностики
- Приветственный экран для новых студентов
- Отображение плана обучения
- Навигация к диагностике и обучению

## 🔄 Поток работы

### 1. Первый вход студента
1. Студент входит в систему
2. Система проверяет, проходил ли он диагностику
3. Если нет - показывается приветственный экран с предложением пройти диагностику

### 2. Прохождение диагностики
1. Студент нажимает "Начать диагностику"
2. Открывается модальное окно `DiagnosticTest`
3. Система генерирует адаптивные вопросы по предметам
4. Студент отвечает на вопросы с таймером
5. После каждого ответа показывается результат
6. По завершении генерируется персональный план

### 3. Отображение результатов
1. Показывается модальное окно `DiagnosticResults`
2. Отображается общий уровень, детали по предметам
3. Показывается психологический профиль
4. Предлагаются рекомендации по обучению

### 4. Работа с планом обучения
1. Студент возвращается на главную страницу
2. Отображается его персональный план
3. Показывается прогресс по предметам
4. Предлагается начать обучение

## 🎨 UI/UX Особенности

### Адаптивный дизайн
- Модальные окна с адаптивной высотой
- Responsive grid layout для результатов
- Мобильная оптимизация

### Визуальная обратная связь
- Цветовая кодировка уровней сложности
- Иконки для разных типов контента
- Прогресс-бары для отслеживания
- Анимации загрузки

### Интерактивность
- Таймер для каждого вопроса
- Автоматическое продвижение после ответа
- Возможность прервать тест
- Повторное прохождение диагностики

## 🧪 Тестирование

### API Endpoints
Все endpoints протестированы с помощью curl:

```bash
# Запуск диагностики
curl -X POST http://localhost:3000/api/diagnostic/start \
  -H "Content-Type: application/json" \
  -d '{"student_id": "test_student_001", "age": 12, "subjects": ["Mathematics", "English"]}'

# Получение вопроса
curl -X POST http://localhost:3000/api/diagnostic/question \
  -H "Content-Type: application/json" \
  -d '{"student_id": "test_student_001", "subject": "Mathematics"}'

# Отправка ответа
curl -X POST http://localhost:3000/api/diagnostic/answer \
  -H "Content-Type: application/json" \
  -d '{"student_id": "test_student_001", "question_id": "Mathematics_dialogue_0", "answer": "Мне нравится математика!", "time_spent_sec": 15}'

# Получение плана
curl -X GET http://localhost:3000/api/diagnostic/plan/test_student_001
```

### Frontend Components
- Все компоненты написаны на TypeScript
- Используется React hooks для управления состоянием
- Обработка ошибок и loading состояний
- Валидация данных

## 🚀 Запуск

### Backend
```bash
source venv/bin/activate
python api.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📱 Использование

1. Зарегистрируйтесь как студент
2. Войдите в систему
3. Нажмите "Начать диагностику"
4. Ответьте на вопросы
5. Просмотрите результаты
6. Начните обучение по персональному плану

## 🔧 Настройка

### Переменные окружения
- `VITE_API_URL` - URL API сервера (по умолчанию: http://localhost:3000/api)

### Кастомизация
- Предметы для диагностики можно изменить в `StudentDashboard.tsx`
- Возраст студента можно получать из профиля пользователя
- Стили можно настроить через Tailwind CSS классы

## 🎯 Результат

Система диагностики полностью интегрирована во фронтенд и готова к использованию. Студенты получают персонализированный опыт обучения на основе их уровня знаний и психологического профиля.
