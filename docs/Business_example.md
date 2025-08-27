Отличный выбор 🙌
**Business Studies** в Cambridge идёт как отдельный предмет на **Upper Secondary (IGCSE)** и **Advanced (A Level)**.
Он ближе к практике: как работает бизнес, маркетинг, финансы, управление людьми.

---

# 📑 Business (Cambridge-style) — Curriculum JSON

```json
{
  "id": "curriculum_business",
  "title": "Business Studies (Cambridge-style)",
  "subject": "Business",
  "stages": [
    {
      "id": "stage_upper_secondary",
      "title": "Upper Secondary (IGCSE Business Studies)",
      "age_range": [14,16],
      "modules": [
        { "id": "bus_intro", "title": "Business Activity and Objectives", "recommended_hours": 25 },
        { "id": "bus_org", "title": "Types of Business Organisation", "recommended_hours": 30 },
        { "id": "bus_people", "title": "People in Business (motivation, HR)", "recommended_hours": 30 },
        { "id": "bus_marketing", "title": "Marketing (market research, 4Ps, strategy)", "recommended_hours": 35 },
        { "id": "bus_operations", "title": "Operations Management (production, quality)", "recommended_hours": 30 },
        { "id": "bus_finance", "title": "Financial Information and Decisions", "recommended_hours": 35 },
        { "id": "bus_external", "title": "External Influences on Business", "recommended_hours": 30 }
      ]
    },
    {
      "id": "stage_advanced",
      "title": "Advanced (A Level Business)",
      "age_range": [16,19],
      "modules": [
        { "id": "bus_strategy_adv", "title": "Business Strategy and Objectives", "recommended_hours": 40 },
        { "id": "bus_marketing_adv", "title": "Marketing Strategy and Analytics", "recommended_hours": 40 },
        { "id": "bus_hr_adv", "title": "Human Resource Management and Leadership", "recommended_hours": 40 },
        { "id": "bus_ops_adv", "title": "Operations and Global Supply Chains", "recommended_hours": 40 },
        { "id": "bus_finance_adv", "title": "Corporate Finance and Investment Decisions", "recommended_hours": 50 },
        { "id": "bus_global_adv", "title": "Global Business and International Trade", "recommended_hours": 40 },
        { "id": "bus_research_adv", "title": "Case Studies, Data Response & Research Project", "recommended_hours": 50 }
      ]
    }
  ]
}
```

---

# 📘 Как учить Business онлайн

### 🟡 IGCSE (14–16)

* **Основы бизнеса**: цели, типы (индивидуальное предприятие, компания, корпорация).
* **Кейсы**: «почему компания А выбрала стратегию X».
* **Задания**:

  * Составить бизнес-план (мини).
  * Рассчитать прибыль, рентабельность.
  * Сделать SWOT-анализ.
* **Проверка**:

  * Автоматически — числовые задачи.
  * ИИ/тьютор — эссе и презентации.

### 🔴 A Level (16–19)

* **Управление и стратегия**: лидерство, мотивация, HR.
* **Маркетинг**: аналитика, сегментация, позиционирование.
* **Финансы**: инвестиции, NPV, cash flow.
* **Мировой бизнес**: глобальные цепочки поставок, международная торговля.
* **Итог**: проект — «бизнес-план стартапа», защита перед группой/опекуном.

---

# 🧩 Пример Lesson JSON (IGCSE Business — Marketing Mix)

```json
{
  "id": "lesson_bus_marketing_1",
  "title": "Introduction to the Marketing Mix (4Ps)",
  "subject": "Business",
  "stage": "Upper Secondary",
  "module_id": "bus_marketing",
  "objectives": ["define_product","explain_price","understand_promotion","explain_place"],
  "estimated_minutes": 45,
  "modules": [
    { "type": "intro", "blocks": [
      { "type": "text", "md": "Сегодня узнаем, что такое **Marketing Mix (4Ps)**: Product, Price, Promotion, Place." }
    ]},
    { "type": "concept", "blocks": [
      { "type": "image", "url": "https://cdn.example/marketing_mix.png", "alt": "Marketing Mix" },
      { "type": "text", "md": "**Product** — товар/услуга. **Price** — цена. **Promotion** — продвижение. **Place** — каналы продаж." }
    ]},
    { "type": "guided_practice", "blocks": [
      { "type": "interactive", "question_id": "item_bus_mix_quiz1" }
    ]},
    { "type": "independent_practice", "blocks": [
      { "type": "assignment", "assignment_id": "hw_bus_mix_case",
        "prompt_md": "Выберите **известный бренд** и проанализируйте его маркетинг по 4Ps. Загрузите эссе (1 стр.) или видео-презентацию.",
        "submit_modes": ["doc","video"]
      }
    ]},
    { "type": "summary", "blocks": [
      { "type": "text", "md": "Маркетинг-микс = основа стратегий бизнеса. Все 4Ps взаимосвязаны." }
    ]}
  ]
}
```

---

# 🧪 Пример Quiz Item (Business)

```json
{
  "id": "item_bus_mix_quiz1",
  "version": "1.0.0",
  "subject": "Business",
  "stage": "Upper Secondary",
  "objective": "define_product",
  "bloom": "remember",
  "question": {
    "type": "mcq",
    "prompt_md": "Что относится к элементу **Promotion** в маркетинг-миксе?",
    "options": [
      { "id": "A", "text": "Цена товара" },
      { "id": "B", "text": "Реклама и PR" },
      { "id": "C", "text": "Точка продаж (магазин)" }
    ],
    "answer": "B"
  },
  "scoring": { "points": 1 },
  "difficulty": 0.2
}
```

---

⚡️ **Business Studies** онлайн = сочетание:

* теория + кейсы,
* интерактив (графики, таблицы),
* эссе и бизнес-планы (с подтверждением родителем/опекуном).

---
