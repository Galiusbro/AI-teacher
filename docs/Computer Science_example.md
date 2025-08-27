Супер 🙌
**Computer Science** в Cambridge идёт на **Lower Secondary (11–14, основы), Upper Secondary (IGCSE)** и **Advanced (A Level)**.
Мы уже делали ICT отдельно, а здесь именно «CS» — программирование, алгоритмы, системы, теория.

---

# 📑 Computer Science (Cambridge-style) — Curriculum JSON

```json
{
  "id": "curriculum_computer_science",
  "title": "Computer Science (Cambridge-style)",
  "subject": "ComputerScience",
  "stages": [
    {
      "id": "stage_lower_secondary",
      "title": "Lower Secondary (Foundations of Computing)",
      "age_range": [11,14],
      "modules": [
        { "id": "cs_thinking_lower", "title": "Computational Thinking (patterns, logic, decomposition)", "recommended_hours": 30 },
        { "id": "cs_programming_lower", "title": "Introduction to Programming (variables, loops, conditionals)", "recommended_hours": 40 },
        { "id": "cs_data_lower", "title": "Data & Representation (binary, text, images)", "recommended_hours": 25 },
        { "id": "cs_systems_lower", "title": "Computer Systems (hardware, OS basics, networking intro)", "recommended_hours": 30 },
        { "id": "cs_project_lower", "title": "Mini Project (design–code–test)", "recommended_hours": 25 }
      ]
    },
    {
      "id": "stage_upper_secondary",
      "title": "Upper Secondary (IGCSE Computer Science)",
      "age_range": [14,16],
      "modules": [
        { "id": "cs_theory_igcse", "title": "Theory of Computer Science (CPU, memory, networking, security)", "recommended_hours": 45 },
        { "id": "cs_programming_igcse", "title": "Programming (procedural, subroutines, arrays, files)", "recommended_hours": 60 },
        { "id": "cs_algorithms_igcse", "title": "Algorithms (search, sort, pseudocode, flowcharts)", "recommended_hours": 40 },
        { "id": "cs_datarep_igcse", "title": "Data Representation (binary, hex, compression, encryption)", "recommended_hours": 35 },
        { "id": "cs_databases_igcse", "title": "Databases (concepts, queries, simple SQL)", "recommended_hours": 25 },
        { "id": "cs_project_igcse", "title": "Programming Project (requirements → design → code → test)", "recommended_hours": 35 }
      ]
    },
    {
      "id": "stage_advanced",
      "title": "Advanced (AS/A Level Computer Science)",
      "age_range": [16,19],
      "modules": [
        { "id": "cs_programming_adv", "title": "Advanced Programming (OO, recursion, modularity)", "recommended_hours": 55 },
        { "id": "cs_structures_adv", "title": "Data Structures & Algorithms (linked lists, trees, graphs, complexity)", "recommended_hours": 55 },
        { "id": "cs_systems_adv", "title": "Computer Architecture & Operating Systems", "recommended_hours": 50 },
        { "id": "cs_networks_adv", "title": "Networks & Security (protocols, cryptography basics)", "recommended_hours": 45 },
        { "id": "cs_databases_adv", "title": "Databases (relational, normalization, advanced SQL)", "recommended_hours": 40 },
        { "id": "cs_ai_adv", "title": "Foundations of AI & Data Science (search, logic, ML intro)", "recommended_hours": 35 },
        { "id": "cs_project_adv", "title": "Capstone Project (design–implement–evaluate)", "recommended_hours": 50 }
      ]
    }
  ]
}
```

---

# 📘 Объяснение по уровням

### 🟡 Lower Secondary (11–14)

* Учим **мыслить как программист** (разбивать задачу, находить паттерны).
* Простое программирование (Scratch, Python-базовый синтаксис).
* Первое знакомство с данными и системами.
* Мини-проект (простая игра, чат-бот, калькулятор).

### 🔵 IGCSE (14–16)

* Теория: устройства, CPU, сеть, безопасность.
* Программирование: процедуры, массивы, файлы.
* Алгоритмы: сортировки, поиск, flowcharts.
* Работа с данными: числа, текст, кодировка, сжатие, криптография.
* Курсовая: небольшой программный продукт.

### 🔴 A Level (16–19)

* Продвинутое программирование (ООП, рекурсия).
* Алгоритмы и структуры данных (деревья, графы, сложность).
* Архитектура компьютера, ОС, ассемблерные вставки.
* Сети, криптография, протоколы.
* Базы данных и транзакции.
* Основы AI и data science.
* Итоговый проект (например, веб-приложение, база данных, система управления).

---

# 🧩 Как учить онлайн

* **Кодинг**: встроенный редактор Python/JavaScript + автопроверка тестов.
* **Алгоритмы**: визуализации (сортировка, поиск, графы).
* **Теория**: карточки, квизы, короткие видео.
* **Практика**: загрузка кода (репозиторий или файл) → автоматическая проверка.
* **Проекты**: шаги → постановка задачи, дизайн, код, тест → защита перед учителем/родителем.

---

# 🧪 Пример Lesson JSON (IGCSE CS — Алгоритмы)

```json
{
  "id": "lesson_cs_algo_igcse_1",
  "title": "Introduction to Algorithms (Search and Sort)",
  "subject": "ComputerScience",
  "stage": "Upper Secondary",
  "module_id": "cs_algorithms_igcse",
  "objectives": ["define_algorithm","explain_search_sort","draw_flowchart"],
  "estimated_minutes": 60,
  "modules": [
    { "type": "intro", "blocks": [
      { "type": "text", "md": "Сегодня учимся что такое **алгоритм** и как работают поиск и сортировка." }
    ]},
    { "type": "concept", "blocks": [
      { "type": "code", "lang": "python", "content": "def linear_search(arr, target):\n    for i in range(len(arr)):\n        if arr[i] == target:\n            return i\n    return -1" },
      { "type": "text", "md": "Пример: линейный поиск. Работает за O(n)." }
    ]},
    { "type": "guided_practice", "blocks": [
      { "type": "interactive", "question_id": "item_cs_algo_quiz1" }
    ]},
    { "type": "independent_practice", "blocks": [
      { "type": "assignment", "assignment_id": "hw_cs_algo_sort",
        "prompt_md": "Реализуйте сортировку вставками (Insertion Sort) на Python или JS. Загрузите код.",
        "submit_modes": ["code"]
      }
    ]},
    { "type": "summary", "blocks": [
      { "type": "text", "md": "Алгоритм = пошаговое решение. У поиска и сортировок важна **сложность**." }
    ]}
  ]
}
```

---

# 🧪 Пример Quiz Item (CS)

```json
{
  "id": "item_cs_algo_quiz1",
  "version": "1.0.0",
  "subject": "ComputerScience",
  "stage": "Upper Secondary",
  "objective": "define_algorithm",
  "bloom": "understand",
  "question": {
    "type": "mcq",
    "prompt_md": "Какой алгоритм поиска быстрее при **отсортированном массиве**?",
    "options": [
      { "id": "A", "text": "Линейный поиск" },
      { "id": "B", "text": "Бинарный поиск" },
      { "id": "C", "text": "Оба одинаково" }
    ],
    "answer": "B"
  },
  "scoring": { "points": 1 },
  "difficulty": 0.3
}
```

---

⚡️ Итог:

* **Computer Science** = теория + практика кодинга.
* На IGCSE → основы алгоритмов и программирования.
* На A Level → структуры данных, архитектура, сети, AI.
* Отлично интегрируется в твою систему: код → автопроверка, теория → квизы, проект → защита.

---
