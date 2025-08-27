отлично — вот **как связать meta-curriculum (оглавление школы)** и **предметные curriculum JSON** так, чтобы система автоматически подхватывала нужные планы и не путалась на переходах (например, Science → Biology/Chemistry/Physics). Я дам рабочие схемы + пример резолвера.

---

# 1) Регистр предметов (Subject Registry)

Одна «карточка» на предмет/кластер с устойчивым кодом. Нужен, чтобы meta-curriculum не зависел от локализаций.

```json
{
  "id": "subject_registry",
  "version": "1.0.0",
  "subjects": [
    { "code": "Mathematics", "kind": "single", "titles": {"en":"Mathematics","ru":"Математика"} },
    { "code": "English", "kind": "single", "titles": {"en":"English","ru":"Английский"} },
    { "code": "Science", "kind": "cluster", "titles": {"en":"Science","ru":"Естествознание"},
      "cluster_children": ["Biology","Chemistry","Physics"] },
    { "code": "Biology", "kind": "single", "titles": {"en":"Biology","ru":"Биология"} },
    { "code": "Chemistry", "kind": "single", "titles": {"en":"Chemistry","ru":"Химия"} },
    { "code": "Physics", "kind": "single", "titles": {"en":"Physics","ru":"Физика"} },
    { "code": "ICT", "kind": "single", "titles": {"en":"ICT","ru":"ИКТ"} },
    { "code": "ComputerScience", "kind": "single", "titles": {"en":"Computer Science","ru":"Информатика"} },
    { "code": "GlobalPerspectives", "kind": "single", "titles": {"en":"Global Perspectives","ru":"Глобальные перспективы"} }
  ]
}
```

---

# 2) Meta-curriculum (Оглавление школы) + «правила развилки»

Meta-curriculum описывает **какие предметы доступны на каждой ступени**, а также **как разворачивать кластеры** (например, Science → Biology, Chemistry, Physics на старших ступенях).

```json
{
  "id": "curriculum_cambridge_like",
  "title": "Cambridge-style International Curriculum",
  "languages": ["en","ru","es","zh"],
  "stages": [
    {
      "id": "stage_primary",
      "title": "Primary",
      "age_range": [5,11],
      "subjects": ["Mathematics","English","Science","ICT","GlobalPerspectives","Art","Music","PE"],
      "cluster_rules": {
        "Science": { "mode": "integrated", "map_to": "curriculum_science_integrated" }
      }
    },
    {
      "id": "stage_lower_secondary",
      "title": "Lower Secondary",
      "age_range": [11,14],
      "subjects": ["Mathematics","English","Science","Geography","History","ICT","Art","Music","PE","Languages"],
      "cluster_rules": {
        "Science": { "mode": "integrated", "map_to": "curriculum_science_integrated" }
      }
    },
    {
      "id": "stage_upper_secondary",
      "title": "Upper Secondary (IGCSE)",
      "age_range": [14,16],
      "subjects": ["Mathematics","English","Physics","Chemistry","Biology","Geography","History","Economics","Business","ICT","GlobalPerspectives","Languages","Art"],
      "cluster_rules": {
        "Science": { "mode": "separate", "map_to_children": ["curriculum_biology","curriculum_chemistry","curriculum_physics"] }
      }
    },
    {
      "id": "stage_advanced",
      "title": "Advanced (AS/A level)",
      "age_range": [16,19],
      "subjects": ["Mathematics","FurtherMathematics","EnglishLiterature","Physics","Chemistry","Biology","Geography","History","Economics","Business","ComputerScience","GlobalPerspectives","ArtAndDesign","Languages"],
      "cluster_rules": {
        "Science": { "mode": "separate", "map_to_children": ["curriculum_biology","curriculum_chemistry","curriculum_physics"] }
      }
    }
  ]
}
```

**Идея:**

* На Primary/Lower Secondary `Science` резолвится в **единый** `curriculum_science_integrated`.
* На Upper/Advanced `Science` **не показываем как предмет** — вместо него отображаем **отдельные** `Biology`, `Chemistry`, `Physics` (каждый со своим curriculum).

---

# 3) Индекс куррикулумов (Curriculum Index)

Где физически лежат файлы предметных программ.

```json
{
  "id": "curriculum_index",
  "entries": [
    { "curriculum_id": "curriculum_math", "subject_code": "Mathematics", "stages": ["stage_primary","stage_lower_secondary","stage_upper_secondary","stage_advanced"], "url": "store://curriculum/math.json", "version": "1.0.0" },
    { "curriculum_id": "curriculum_english", "subject_code": "English", "stages": ["stage_primary","stage_lower_secondary","stage_upper_secondary","stage_advanced"], "url": "store://curriculum/english.json", "version": "1.0.0" },
    { "curriculum_id": "curriculum_science_integrated", "subject_code": "Science", "stages": ["stage_primary","stage_lower_secondary"], "url": "store://curriculum/science_integrated.json", "version": "1.0.0" },
    { "curriculum_id": "curriculum_biology", "subject_code": "Biology", "stages": ["stage_upper_secondary","stage_advanced"], "url": "store://curriculum/biology.json", "version": "1.0.0" },
    { "curriculum_id": "curriculum_chemistry", "subject_code": "Chemistry", "stages": ["stage_upper_secondary","stage_advanced"], "url": "store://curriculum/chemistry.json", "version": "1.0.0" },
    { "curriculum_id": "curriculum_physics", "subject_code": "Physics", "stages": ["stage_upper_secondary","stage_advanced"], "url": "store://curriculum/physics.json", "version": "1.0.0" },
    { "curriculum_id": "curriculum_ict", "subject_code": "ICT", "stages": ["stage_primary","stage_lower_secondary","stage_upper_secondary"], "url": "store://curriculum/ict.json", "version": "1.0.0" },
    { "curriculum_id": "curriculum_computer_science", "subject_code": "ComputerScience", "stages": ["stage_lower_secondary","stage_upper_secondary","stage_advanced"], "url": "store://curriculum/compsci.json", "version": "1.0.0" },
    { "curriculum_id": "curriculum_global_perspectives", "subject_code": "GlobalPerspectives", "stages": ["stage_lower_secondary","stage_upper_secondary","stage_advanced"], "url": "store://curriculum/global_perspectives.json", "version": "1.0.0" }
  ]
}
```

---

# 4) Алгоритм резолвера (псевдокод)

Преобразует «я на такой-то ступени, хочу такие предметы» → в **список конкретных curriculum-файлов**.

```pseudo
function resolveCurricula(meta, registry, index, stage_id, selected_subject_codes):
  stage = meta.stages.find(s => s.id == stage_id)

  # 1) Подменяем кластеры по правилам
  effective_subjects = []
  for code in selected_subject_codes:
    rule = stage.cluster_rules[code] if exists
    if rule and rule.mode == "integrated":
       # остаётся один curriculum (например, integrated Science)
       effective_subjects.append({ code: code, mode: "integrated" })
    elif rule and rule.mode == "separate":
       # заменяем кластер Science на Biology, Chemistry, Physics
       children = registry.subjects.find(s => s.code == "Science").cluster_children
       for ch in children:
         effective_subjects.append({ code: ch, mode: "single" })
    else:
       effective_subjects.append({ code: code, mode: "single" })

  # 2) Подбираем curriculum из индекса
  curricula = []
  for subj in effective_subjects:
    entries = index.entries.filter(e => e.subject_code == subj.code && stage_id in e.stages)
    if entries not empty:
      curricula.push(entries[0]) # по умолчанию актуальная версия
    else:
      warn("No curriculum found for", subj.code, stage_id)

  return curricula
```

**Пример входа:**
`stage_id = "stage_upper_secondary"`, `selected = ["Mathematics","English","Science","ICT"]`
→ Результат: `["curriculum_math","curriculum_english","curriculum_biology","curriculum_chemistry","curriculum_physics","curriculum_ict"]`

---

# 5) Как уроки «заводятся» из предметного curriculum

Каждый предметный curriculum хранит **modules** c `recommended_hours`. Генератор уроков берёт модуль и дробит его на уроки по политике (например, 1 урок ≈ 45–60 минут):

```json
{
  "curriculum_id": "curriculum_math",
  "module": { "id": "math_quadratics_upper", "title": "Quadratic Equations", "recommended_hours": 40 },
  "lesson_policy": { "default_lesson_minutes": 60, "min_lessons": 6, "max_lessons": 12 },
  "generated_lessons": [
    {"id":"lesson_quad_01","allocated_minutes":60,"objectives":["recognize/form"],"module_id":"math_quadratics_upper"},
    {"id":"lesson_quad_02","allocated_minutes":60,"objectives":["formula_basics"],"module_id":"math_quadratics_upper"},
    {"id":"lesson_quad_03","allocated_minutes":60,"objectives":["formula_edge_cases"],"module_id":"math_quadratics_upper"},
    {"id":"lesson_quad_04","allocated_minutes":60,"objectives":["graphs_intro"],"module_id":"math_quadratics_upper"},
    {"id":"lesson_quad_05","allocated_minutes":60,"objectives":["graphs_practice"],"module_id":"math_quadratics_upper"},
    {"id":"lesson_quad_06","allocated_minutes":60,"objectives":["vieta_intro"],"module_id":"math_quadratics_upper"},
    {"id":"lesson_quad_07","allocated_minutes":60,"objectives":["vieta_problems"],"module_id":"math_quadratics_upper"}
  ],
  "hours_covered": 7
}
```

> Политика может наращивать уроки до покрытия `recommended_hours`, вплоть до добавления «практикумов», «повторения» и «контрольных».

---

# 6) Рекомендованный формат ссылок между уровнями

* **Meta → Subject Registry**: по `subjects[]` с кодами.
* **Meta → Subject Curricula**: через `cluster_rules` и `curriculum_index`.
* **Subject Curriculum → Modules → Lessons**: `module_id` и `lesson_id`, плюс `objectives[]` (LO codes).
* **Версионирование**: у каждого curriculum и lesson есть `version`, в планах храним «пригвождённые» версии.

---

# 7) Пример: студент 15 лет (Upper Secondary), выбрал Mathematics, English, Science, ICT

1. Резолвер читает meta и registry.
2. На этой ступени `Science` → `Biology+Chemistry+Physics`.
3. Из `curriculum_index` вытаскиваем: `curriculum_math`, `curriculum_english`, `curriculum_biology`, `curriculum_chemistry`, `curriculum_physics`, `curriculum_ict`.
4. Планировщик раздаёт недели и генерирует уроки из модулей согласно `recommended_hours`.

---

Если хочешь, упакую это в **единый контракт JSON Schema (draft-07)** + отдам минимальные **эндпойнты** (`/resolve`, `/plan/generate`) с примерами запрос/ответ, чтобы разработчики могли сразу внедрять.
