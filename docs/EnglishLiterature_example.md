Отличный выбор 🙌
**English Literature** в Cambridge — это отдельный предмет, который идёт в **Upper Secondary (IGCSE)** и **Advanced (A Level)**.
Он отличается от «English Language»: тут главное не грамматика, а **анализ художественных текстов, понимание авторских приёмов и интерпретация смысла**.

---

# 📑 English Literature (Cambridge-style) — Curriculum JSON

```json
{
  "id": "curriculum_english_literature",
  "title": "English Literature (Cambridge-style)",
  "subject": "EnglishLiterature",
  "stages": [
    {
      "id": "stage_upper_secondary",
      "title": "Upper Secondary (IGCSE English Literature)",
      "age_range": [14,16],
      "modules": [
        { "id": "lit_poetry_igcse", "title": "Poetry Analysis (themes, imagery, rhythm)", "recommended_hours": 40 },
        { "id": "lit_prose_igcse", "title": "Prose (novels, short stories)", "recommended_hours": 40 },
        { "id": "lit_drama_igcse", "title": "Drama (Shakespeare + modern plays)", "recommended_hours": 45 },
        { "id": "lit_comparison_igcse", "title": "Comparative Reading (texts across genres)", "recommended_hours": 35 },
        { "id": "lit_essay_igcse", "title": "Essay Writing and Interpretation", "recommended_hours": 40 }
      ]
    },
    {
      "id": "stage_advanced",
      "title": "Advanced (AS/A Level English Literature)",
      "age_range": [16,19],
      "modules": [
        { "id": "lit_poetry_adv", "title": "Advanced Poetry (forms, schools, comparative study)", "recommended_hours": 50 },
        { "id": "lit_drama_adv", "title": "Advanced Drama (classical to modern, performance context)", "recommended_hours": 50 },
        { "id": "lit_prose_adv", "title": "Advanced Prose (novels, narrative techniques, critical theories)", "recommended_hours": 50 },
        { "id": "lit_comparison_adv", "title": "Comparative & Contextual Studies (literary movements, culture)", "recommended_hours": 50 },
        { "id": "lit_coursework_adv", "title": "Independent Coursework / Research Essay", "recommended_hours": 45 }
      ]
    }
  ]
}
```

---

# 📘 Человеческое объяснение

### 🔵 IGCSE (14–16)

* **Поэзия**: разбор образов, ритма, тем.
* **Проза**: романы, рассказы (характеры, сюжет, стиль).
* **Драма**: Шекспир + современные пьесы.
* **Сравнительное чтение**: сопоставление текстов.
* **Эссе**: развитие аргументированной письменной речи.

### 🔴 A Level (16–19)

* **Поэзия**: углублённый анализ школ и эпох (метафизики, романтики, модернисты).
* **Драма**: от античных трагедий до постмодернистских пьес.
* **Проза**: стили, нарративные техники, литературная критика.
* **Сравнительные исследования**: межкультурные и межжанровые связи.
* **Курсовая**: самостоятельное исследование, часто \~3000 слов.

---

# 🧩 Как учить онлайн

* **Текстовые блоки**: отрывки стихов, прозы, пьес.
* **Интерактив**: выдели метафору, найди ключевой мотив.
* **Аудио/видео**: чтение стихотворения или постановка пьесы.
* **Эссе**: загрузка текста → ИИ проверяет структуру, аргументацию, цитаты.
* **Дискуссия**: устный ответ (видео) → подтверждение родителем/опекуном.
* **Сравнение текстов**: интерактивные таблицы (темы, персонажи, стили).

---

# 🧪 Пример Lesson JSON (IGCSE English Literature — Poetry)

```json
{
  "id": "lesson_lit_poetry_igcse_1",
  "title": "Introduction to Poetry Analysis",
  "subject": "EnglishLiterature",
  "stage": "Upper Secondary",
  "module_id": "lit_poetry_igcse",
  "objectives": ["identify_imagery","analyze_theme","comment_on_form"],
  "estimated_minutes": 60,
  "modules": [
    { "type": "intro", "blocks": [
      { "type": "text", "md": "Сегодня разбираем, как понимать **поэзию**: тему, образы, форму." }
    ]},
    { "type": "concept", "blocks": [
      { "type": "quote", "md": "\"Shall I compare thee to a summer’s day?\" – W. Shakespeare" },
      { "type": "text", "md": "Здесь мы видим **метафору**: сравнение возлюбленной с летним днём." }
    ]},
    { "type": "guided_practice", "blocks": [
      { "type": "interactive", "question_id": "item_lit_poetry_quiz1" }
    ]},
    { "type": "independent_practice", "blocks": [
      { "type": "assignment", "assignment_id": "hw_lit_poetry_sonnet",
        "prompt_md": "Выберите короткое стихотворение (14–20 строк). Напишите эссе (150–200 слов): тема, образы, форма. Загрузите документ.",
        "submit_modes": ["doc"]
      }
    ]},
    { "type": "summary", "blocks": [
      { "type": "text", "md": "Поэзия = сочетание темы, образов и формы. Это три ключа анализа." }
    ]}
  ]
}
```

---

# 🧪 Пример Quiz Item (Poetry)

```json
{
  "id": "item_lit_poetry_quiz1",
  "version": "1.0.0",
  "subject": "EnglishLiterature",
  "stage": "Upper Secondary",
  "objective": "identify_imagery",
  "bloom": "understand",
  "question": {
    "type": "mcq",
    "prompt_md": "Что означает образ «Shall I compare thee to a summer’s day?»",
    "options": [
      { "id": "A", "text": "Сравнение красоты с чем-то мимолётным" },
      { "id": "B", "text": "Точный прогноз погоды" },
      { "id": "C", "text": "Научное описание климата" }
    ],
    "answer": "A"
  },
  "scoring": { "points": 1 },
  "difficulty": 0.3
}
```

---

⚡️ Итого:

* **English Literature** = анализ текстов, а не язык.
* На **IGCSE** — стихи, проза, драма, эссе.
* На **A Level** — сложный анализ, критика, исследовательская работа.
* Онлайн-курс = чтение текстов, эссе, устные дискуссии, проекты.

---

👉 Хочешь, я сделаю так же для **Art & Design (Advanced)** в расширенном виде — с примерами проектов и оценочной рубрикой (как в Cambridge A Level Art)?
