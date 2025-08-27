🔥 да, «PE» (Physical Education) как школьный предмет в Cambridge — это не только спорт, но и здоровье/фитнес, моторика, командная работа.
Понятно, что **мы не можем «ставить зачёт по бегу на 100м» онлайн**, зато можем:

* давать **упражнения с видео-демо** (можно подтягивать с YouTube или встроенных библиотек),
* задавать **мини-тренировки** (warm-up, core, stretching),
* просить **ученика загрузить видео** выполнения (телефон),
* анализировать базовые метрики (повторения, амплитуда, поза),
* подключать «здоровье и lifestyle» (питание, сон, техника безопасности),
* делать **теоретические блоки** (как тренировать сердечно-сосудистую систему, зачем растяжка).

---

# 📑 PE (Cambridge-style) — Curriculum JSON

```json
{
  "id": "curriculum_pe",
  "title": "Physical Education (Cambridge-style)",
  "subject": "PE",
  "stages": [
    {
      "id": "stage_primary",
      "title": "Primary",
      "age_range": [5,11],
      "modules": [
        { "id": "pe_motor_primary", "title": "Fundamental Motor Skills (running, jumping, throwing)", "recommended_hours": 30 },
        { "id": "pe_games_primary", "title": "Simple Games & Teamwork", "recommended_hours": 25 },
        { "id": "pe_health_primary", "title": "Healthy Habits (hydration, rest, hygiene)", "recommended_hours": 20 }
      ]
    },
    {
      "id": "stage_lower_secondary",
      "title": "Lower Secondary",
      "age_range": [11,14],
      "modules": [
        { "id": "pe_fitness_lower", "title": "Fitness Foundations (cardio, strength, flexibility)", "recommended_hours": 30 },
        { "id": "pe_games_lower", "title": "Team Sports & Cooperation", "recommended_hours": 30 },
        { "id": "pe_safety_lower", "title": "Injury Prevention & First Aid Basics", "recommended_hours": 20 },
        { "id": "pe_health_lower", "title": "Health, Nutrition and Lifestyle", "recommended_hours": 20 }
      ]
    },
    {
      "id": "stage_upper_secondary",
      "title": "Upper Secondary (IGCSE PE)",
      "age_range": [14,16],
      "modules": [
        { "id": "pe_anatomy_upper", "title": "Anatomy & Physiology for Sport", "recommended_hours": 40 },
        { "id": "pe_training_upper", "title": "Training Methods & Fitness Planning", "recommended_hours": 40 },
        { "id": "pe_psychology_upper", "title": "Psychology of Sport & Motivation", "recommended_hours": 30 },
        { "id": "pe_practical_upper", "title": "Practical Performance & Video Assessment", "recommended_hours": 40 }
      ]
    },
    {
      "id": "stage_advanced",
      "title": "Advanced (A Level PE)",
      "age_range": [16,19],
      "modules": [
        { "id": "pe_biomechanics_adv", "title": "Biomechanics & Movement Analysis", "recommended_hours": 40 },
        { "id": "pe_exercise_physiology_adv", "title": "Exercise Physiology", "recommended_hours": 40 },
        { "id": "pe_psychology_adv", "title": "Advanced Sports Psychology", "recommended_hours": 35 },
        { "id": "pe_performance_adv", "title": "Performance Analysis & Coaching", "recommended_hours": 45 },
        { "id": "pe_research_adv", "title": "Research Project (sports science)", "recommended_hours": 40 }
      ]
    }
  ]
}
```

---

# 🏃 Как реализовать онлайн-PE

### 🎥 Контент

* Урок = блок **видео (YouTube embed)** + текстовое объяснение.
* Можно прикреплять **короткие туториалы** (разминка, приседания, растяжка).

### 📲 Практика ученика

* **Upload video/photo** → ученик записывает, как делает упражнение (например, планка).
* **Анализ**:

  * базовая поза (углы тела — через pose estimation / OpenPose, Mediapipe),
  * количество повторений (jumping jacks, squats).
* **Фидбек**: «спина прямая», «руки слишком согнуты», «отличный ритм».

### 📑 Теория

* MCQ/квизы: «какие мышцы работают при приседании?», «зачем разминка?».
* Мини-эссе: «Как питание влияет на выносливость?».

### 🏆 Контроль

* «Fitness log» (прогресс по повторениям/времени).
* Родитель/опекун подтверждает: «да, ребёнок сделал тренировку».
* Итоговый зачёт: план тренировки + защита устно.

---

# 📘 Пример Lesson JSON (PE, приседания)

```json
{
  "id": "lesson_pe_squats_lower",
  "title": "Bodyweight Squats — Technique and Practice",
  "subject": "PE",
  "stage": "Lower Secondary",
  "module_id": "pe_fitness_lower",
  "objectives": ["learn_squat_form","improve_leg_strength","apply_reps_consistency"],
  "estimated_minutes": 30,
  "modules": [
    { "type": "intro", "blocks": [
      { "type": "text", "md": "Сегодня учимся правильной технике приседаний." }
    ]},
    { "type": "concept", "blocks": [
      { "type": "video", "url": "https://www.youtube.com/embed/aclHkVaku9U", "caption": "Правильная техника приседаний" },
      { "type": "text", "md": "Основное: спина прямая, колени не выходят за носки, пятки на полу." }
    ]},
    { "type": "guided_practice", "blocks": [
      { "type": "interactive", "question_id": "item_pe_squat_quiz1" }
    ]},
    { "type": "independent_practice", "blocks": [
      { "type": "assignment", "assignment_id": "hw_pe_squat_10",
        "prompt_md": "Сделайте **10 приседаний** и запишите видео. Загрузите файл.",
        "submit_modes": ["video"] }
    ]},
    { "type": "summary", "blocks": [
      { "type": "text", "md": "Приседания укрепляют ноги и корпус. Важно соблюдать технику." }
    ]}
  ]
}
```

---

# 🎯 Особенность PE онлайн

* **Видео YouTube** = офиц. источник (разминки, упражнения).
* **Практика** = загрузка **видео/фото** → автоматическая + экспертная оценка.
* **Теория** = MCQ, эссе.
* **Фокус** = здоровье + привычки, не соревнования.

---