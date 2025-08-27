Отличный выбор 🙌
**Economics** в Cambridge — предмет для **Upper Secondary (IGCSE)** и **Advanced (A Level)**.
На Primary/Lower Secondary экономики как отдельного курса нет (она частично входит в «Global Perspectives» или «Business Studies»), но с 14 лет появляется отдельный предмет.

Я сделаю curriculum JSON для Economics, а потом — поясню, как его реально можно учить онлайн (задания, кейсы, анализ данных).

---

# 📑 Economics (Cambridge-style) — Curriculum JSON

```json
{
  "id": "curriculum_economics",
  "title": "Economics (Cambridge-style)",
  "subject": "Economics",
  "stages": [
    {
      "id": "stage_upper_secondary",
      "title": "Upper Secondary (IGCSE Economics)",
      "age_range": [14,16],
      "modules": [
        { "id": "econ_basic_concepts", "title": "Basic Economic Concepts (scarcity, choice, opportunity cost)", "recommended_hours": 25 },
        { "id": "econ_demand_supply", "title": "Demand and Supply", "recommended_hours": 30 },
        { "id": "econ_market", "title": "The Market System (price, competition, elasticity)", "recommended_hours": 35 },
        { "id": "econ_production", "title": "Production and Costs", "recommended_hours": 30 },
        { "id": "econ_labor", "title": "Labour and Employment", "recommended_hours": 25 },
        { "id": "econ_government", "title": "Government and the Economy (tax, spending, policy)", "recommended_hours": 35 },
        { "id": "econ_international", "title": "International Trade and Globalisation", "recommended_hours": 40 }
      ]
    },
    {
      "id": "stage_advanced",
      "title": "Advanced (A Level Economics)",
      "age_range": [16,19],
      "modules": [
        { "id": "econ_micro", "title": "Microeconomics (demand/supply, elasticity, market structures)", "recommended_hours": 60 },
        { "id": "econ_macro", "title": "Macroeconomics (inflation, growth, unemployment)", "recommended_hours": 60 },
        { "id": "econ_government_adv", "title": "Government Policies (fiscal, monetary, supply-side)", "recommended_hours": 50 },
        { "id": "econ_international_adv", "title": "International Economics (trade, exchange rates, globalization)", "recommended_hours": 50 },
        { "id": "econ_development", "title": "Development Economics (inequality, poverty, sustainability)", "recommended_hours": 45 },
        { "id": "econ_research", "title": "Case Studies, Data Response & Research Project", "recommended_hours": 45 }
      ]
    }
  ]
}
```

---

# 📘 Как учить Economics онлайн

### 🟡 IGCSE (14–16)

* **Теория**: графики (спрос/предложение), elasticity, налоги.
* **Задания**:

  * нарисовать график (встроенный инструмент или загрузка фото из тетради);
  * решить задачи (подсчитать эластичность, стоимость, излишки);
  * написать мини-эссе: «Что будет, если государство введёт налог на сахар?»
* **Проверка**:

  * Автоматическая проверка числовых задач.
  * Анализ эссе по структуре (введение–аргументы–вывод).

### 🔴 A Level (16–19)

* **Кейсы**: реальные данные (ВВП, инфляция, курс валют).
* **Графики**: студент строит модель, объясняет сдвиги.
* **Дискуссии/эссе**: «Преимущества и недостатки протекционизма».
* **Исследование**: взять страну → собрать данные → сделать выводы.
* **Защита**: устное выступление (видео) + подтверждение родителя/учителя.

---

# 🧩 Пример Lesson JSON (IGCSE Economics — спрос и предложение)

```json
{
  "id": "lesson_econ_demand_supply_1",
  "title": "Introduction to Demand and Supply",
  "subject": "Economics",
  "stage": "Upper Secondary",
  "module_id": "econ_demand_supply",
  "objectives": ["explain_demand","explain_supply","draw_basic_curves"],
  "estimated_minutes": 45,
  "modules": [
    { "type": "intro", "blocks": [
      { "type": "text", "md": "Сегодня мы узнаем, что такое спрос и предложение и как они определяют цену." }
    ]},
    { "type": "concept", "blocks": [
      { "type": "image", "url": "https://cdn.example/demand_supply.png", "alt": "Спрос и предложение" },
      { "type": "text", "md": "Спрос = количество, которое покупатели готовы купить. Предложение = количество, которое продавцы готовы продать." }
    ]},
    { "type": "guided_practice", "blocks": [
      { "type": "interactive", "question_id": "item_econ_ds_quiz1" }
    ]},
    { "type": "independent_practice", "blocks": [
      { "type": "assignment", "assignment_id": "hw_econ_ds_graph",
        "prompt_md": "Нарисуйте график спроса и предложения для яблок. Укажите точку равновесия. Загрузите фото или постройте в редакторе.",
        "submit_modes": ["photo","editor"]
      }
    ]},
    { "type": "summary", "blocks": [
      { "type": "text", "md": "Цена устанавливается в точке равновесия — там, где спрос = предложению." }
    ]}
  ]
}
```

---

# 🧪 Пример Quiz Item (Economics)

```json
{
  "id": "item_econ_ds_quiz1",
  "version": "1.0.0",
  "subject": "Economics",
  "stage": "Upper Secondary",
  "objective": "explain_demand",
  "bloom": "understand",
  "question": {
    "type": "mcq",
    "prompt_md": "Если цена товара растёт, то спрос обычно…",
    "options": [
      { "id": "A", "text": "Растёт" },
      { "id": "B", "text": "Падает" },
      { "id": "C", "text": "Не меняется" }
    ],
    "answer": "B"
  },
  "scoring": { "points": 1 },
  "difficulty": 0.2
}
```

---

⚡️ Экономика отлично подходит для онлайн-обучения, потому что:

* легко использовать **данные и графики**,
* много **эссе и кейсов**, которые можно проверять ИИ,
* есть баланс **автоматической проверки** (задачи, графики) и **soft skills** (аргументация, устная защита).

---
