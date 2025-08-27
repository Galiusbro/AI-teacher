классная идея — давай упакуем её в понятную систему: что именно строим, какие данные храним (JSON-схемы), как работает ИИ, какие экраны в веб-интерфейсе и как всё это стыкуется с «кембриджской» логикой (диагностика → план → уроки → контрольная → следующий цикл).

# Видение и принципы

* **Мастерство по объектам знаний**, а не «общая оценка по предмету»: математика ≠ геометрия ≠ алгебра. Прокачиваем отдельные цели (learning objectives) из Cambridge (Primary / Lower Secondary / IGCSE).
* **Диагностика → персональный план (месяц/триместр)** с проверкой в конце периода и возможностью **досрочного зачёта** по блокам, если уже есть мастерство.
* **«Рецепты, не готовые блюда»**: при докладах ИИ даёт структуру, вопросы к источникам, ссылки и чек-листы, но не пишет работу за ученика.
* **Ответственный (родитель/опекун)** подтверждает зачёт **паролем** + журнал аудита.
* **Контент — в JSON**, чтобы веб мог «без кода» рендерить тексты, формулы, графики, тесты, загрузки фото и т.д.

---

# Роли и доступы

* **Student**: проходит диагностику/уроки, сдаёт ответы (текст/фото), инициирует досрочный зачёт.
* **Guardian**: видит прогресс, подтверждает зачёты/контрольные, оставляет отзыв (под паролем).
* **Educator/Reviewer (опционально)**: верифицирует граничные случаи, добавляет задания.
* **Admin**: настраивает предметы, цели, весовые коэффициенты, пороги, Academic integrity политики.

---

# Потоки (flows)

## 1) Онбординг и диагностика

1. Ученик выбирает предметы (или **базовый набор**).
2. Система запускает **адаптивный диагностический тест**: от простого к сложному по каждому «objective».
3. Модель «знаниеслежения» (см. ниже) выводит стартовый уровень по каждому objective.

## 2) План на месяц/триместр

* План строится по приоритетам: (a) пробелы с высокой связностью-пререквизитами, (b) важность по Cambridge, (c) дедлайны (например, к IGCSE).
* Каждая неделя = 2-4 микроцели + 1 закрепляющее задание.

## 3) Урок → задание в тетради → проверка

* ИИ рендерит **материал урока** (объяснение, примеры, формулы) + **задание**, ученик решает в тетради.
* Ответ отправляется как **текст или фото**. Визуальный модуль извлекает шаги, указывает, где ошибка, и показывает верный ход.

## 4) Досрочный зачёт

* Если по objective **mastery ≥ порога** (например, 0.85), система предлагает **skip** блока и контрольный квиз для подтверждения.

## 5) Контрольная

* В конце периода — микс задач по всем objectives периода.
* После проверки — **план на следующий промежуток**.

## 6) Подтверждение ответственным

* Родитель видит краткий отчёт, ставит галочку «принято» и **подтверждает паролем**, отзыв сохраняется в журнале.

---

# Модель знаний и формулы

**Мастерство по objective** храним как `p ∈ [0,1]`. Обновляем после каждого ответа.
Простой логит-апдейт (альтернатива BKT/DKT), где `θ` — сложность, `β` — базовая способность:

* Вероятность правильного:  $\hat{y} = \sigma(β - θ)$
* Обновление мастерства (онлайн-логит):
  $β_{t+1} = β_t + η \cdot (y - \hat{y})$,
  где $y ∈ \{0,1\}$, $η$ — темп.
* Маппим $β$ в `p` сигмоидой: $p = \sigma(β)$

**Решение для реальной школы**: начнём с простого онлайн-логита (понятно и стабильно), затем можно включить **BKT** или **DKT** (LSTM-модель) для более точного прогнозирования.

**Пороги**:

* Досрочный зачёт по objective: `p ≥ 0.85`
* Готов к контрольной (блок): среднее по objectives блока `≥ 0.8` и **нет «красных» пререквизитов**.

---

# Cambridge-слои (пример математики)

* **Strands**: Number, Algebra, Geometry, Measure, Data (и Problem solving как сквозная).
* **Objective code** (пример): `M.LS.Geometry.7.3` — «Углы, параллельные прямые, сумма углов треугольника» (условный код, можно синхронизировать с реальными кодами Cambridge для вашего издания).

---

# JSON: единый формат контента/уроков

## 1) Урок (Lesson JSON)

```json
{
  "id": "lesson_M_Geometry_Angles_v1",
  "subject": "Mathematics",
  "strand": "Geometry",
  "stage": "LowerSecondary-7",
  "objectives": ["M.LS.Geometry.7.3"],
  "title": "Углы и параллельные прямые",
  "duration_min": 35,
  "prerequisites": ["M.LS.Number.6.1"],
  "blocks": [
    {"type": "heading", "text": "Что такое углы?"},
    {"type": "text", "md": "Угол — это фигура, образованная двумя лучами с общим началом..."},
    {"type": "formula", "latex": "\\alpha+\\beta+\\gamma=180^{\\circ}"},
    {
      "type": "image",
      "alt": "Параллельные прямые и секущая",
      "url": "https://cdn.example/geom/parallel_transversal.png"
    },
    {
      "type": "example",
      "md": "Найдите углы, если известен один из внутренних накрест лежащих — 35°."
    },
    {
      "type": "interactive",
      "question_id": "q1",
      "question_type": "numeric",
      "prompt": "Чему равен накрест лежащий угол к 35°?",
      "validation": {"type": "equals", "value": 35},
      "objective": "M.LS.Geometry.7.3",
      "difficulty": 0.3
    },
    {
      "type": "assignment",
      "id": "hw1",
      "submit_modes": ["text", "photo"],
      "prompt_md": "В тетради решите 3 задачи из файла «Angles_01.pdf». Загрузите фото решения."
    },
    {
      "type": "chart",
      "chart_type": "line",
      "title": "Прогресс по углам",
      "series": [
        {"name": "mastery", "data": [[1,0.4],[2,0.55],[3,0.7]]}
      ],
      "x_label": "шаг урока",
      "y_label": "вероятность мастерства"
    }
  ],
  "resources": [
    {"type": "link", "title": "Краткий конспект", "url": "https://school.example/notes/angles"},
    {"type": "link", "title": "Видеоурок", "url": "https://video.example/angles"}
  ],
  "assessment": {
    "items": ["item_geom_ang_01", "item_geom_ang_02"]
  }
}
```

## 2) Тестовый элемент (Assessment Item JSON)

```json
{
  "id": "item_geom_ang_01",
  "subject": "Mathematics",
  "objective": "M.LS.Geometry.7.3",
  "bloom": "apply",
  "question": {
    "type": "mcq",
    "prompt_md": "Найдите значение угла **x** (см. рисунок).",
    "image": "https://cdn.example/tasks/triangles_02.png",
    "options": [
      {"id": "A", "text": "45°"},
      {"id": "B", "text": "60°"},
      {"id": "C", "text": "75°"},
      {"id": "D", "text": "120°"}
    ],
    "answer": "C"
  },
  "scoring": {"points": 1, "partial": false},
  "difficulty": 0.5,
  "hints": [
    "Сумма углов треугольника — 180°.",
    "Равнобедренный? Проверьте стороны."
  ]
}
```

## 3) План на период (Plan JSON)

```json
{
  "id": "plan_2025_T1_student_123",
  "period": "trimester",
  "start_date": "2025-09-01",
  "end_date": "2025-11-30",
  "subjects": [
    {
      "subject": "Mathematics",
      "goals": [
        {"objective": "M.LS.Geometry.7.3", "target_p": 0.85},
        {"objective": "M.LS.Number.7.1", "target_p": 0.85}
      ],
      "weeks": [
        {
          "week_index": 1,
          "lessons": ["lesson_M_Geometry_Angles_v1", "lesson_M_Number_Fractions_v2"],
          "checks": ["quiz_geo_w1"],
          "skip_candidates": ["M.LS.Number.7.1"]  // если p уже высокое
        }
      ]
    }
  ]
}
```

## 4) Ответ ученика (Submission) и фидбек

```json
{
  "submission_id": "sub_987",
  "student_id": "stu_123",
  "question_id": "hw1",
  "mode": "photo",
  "uploaded_at": "2025-09-10T12:05:00+07:00",
  "artifacts": [{"type": "image", "url": "https://uploads/.../sub_987.jpg"}],
  "analysis": {
    "ocr_math": [
      {"step": 1, "expr": "α+β+γ=180°"},
      {"step": 2, "expr": "α=35°, β=35°"}
    ],
    "errors": [
      {
        "at_step": 2,
        "type": "concept",
        "message": "β не обязательно равен 35°, проверьте тип углов."
      }
    ]
  },
  "auto_score": {"points": 0.5, "max": 1},
  "feedback_md": "Верно определили сумму углов, но спутали пары накрест лежащих.",
  "mastery_update": [
    {"objective": "M.LS.Geometry.7.3", "delta": 0.08}
  ]
}
```

## 5) Подтверждение родителем (Approval)

```json
{
  "approval_id": "appr_445",
  "student_id": "stu_123",
  "period": "2025_T1",
  "artifact": "final_exam_math",
  "status": "approved",
  "guardian_id": "par_77",
  "approved_at": "2025-11-30T19:40:00+07:00",
  "audit": {
    "ip": "1.2.3.4",
    "user_agent": "Chrome/...",
    "method": "password",
    "signature_hash": "sha256:..."
  },
  "review_comment": "Выступил уверенно, решения объяснял."
}
```

---

# API (REST, черновик)

* `POST /diagnostics/start` → `{ subjects: ["Mathematics","English"] }` → `diagnostic_session_id`
* `GET /diagnostics/next?session_id=...` → следующий адаптивный `AssessmentItem JSON`
* `POST /diagnostics/answer` → `{session_id,item_id,answer}` → `{correct, mastery_updates}`
* `POST /plan/generate` → `{student_id, horizon:"trimester"}` → `Plan JSON`
* `GET /lessons/:lesson_id` → `Lesson JSON`
* `POST /submit` → `Submission JSON` (текст/фото)
* `POST /grade` → автооценивание + `mastery_update`
* `POST /exam/request-early-pass` → триаж по objective/блоку
* `POST /guardian/approve` → `{artifact, password}` → `Approval JSON`
* `POST /report/assist` → вход: тема + требования → выход: **план доклада** (outline), источники, чек-лист (без готового текста)
* `POST /report/check` → проверка цитирований, структуры, антиплагиат-score

---

# Веб-интерфейс: ключевые экраны

1. **Диагностика**: прогресс-бар по предметам; вопросы от лёгких к сложным; индикатор «затрагиваемые темы».
2. **Дашборд ученика**: карта целей (objective heatmap), графики мастерства, кнопка «досрочно сдать блок».
3. **Урок**: рендер JSON-блоков (текст, формулы, графики, задания), кнопки «ответ текстом» / «загрузить фото».
4. **Проверка решения**: подсветка ошибочных шагов, совет «как правильно».
5. **Доклад**: мастер-помощник (outline → источники → черновик тезисов → чек-лист защиты).
6. **Панель родителя**: сводка успехов, кнопка «подтвердить», поле пароля, история подтверждений.
7. **Отчёты**: освоение по предметам/целям, попытки, среднее время, стабильность.

---

# Мини-рендер JSON-урока (React + TS, фрагмент)

```tsx
type Block =
  | { type: "heading"; text: string }
  | { type: "text"; md: string }
  | { type: "formula"; latex: string }
  | { type: "image"; alt: string; url: string }
  | { type: "interactive"; question_id: string; question_type: "numeric"|"mcq"|"open"; prompt: string; validation?: any }
  | { type: "assignment"; id: string; submit_modes: ("text"|"photo")[]; prompt_md: string }
  | { type: "chart"; chart_type: "line"|"bar"; title: string; series: {name:string; data:[number,number][]}[]; x_label?: string; y_label?: string };

function LessonRenderer({ blocks }: { blocks: Block[] }) {
  return (
    <div className="lesson">
      {blocks.map((b, i) => {
        switch (b.type) {
          case "heading": return <h2 key={i}>{b.text}</h2>;
          case "text": return <Markdown key={i} source={b.md} />;
          case "formula": return <Katex key={i} latex={b.latex} />;
          case "image": return <img key={i} src={b.url} alt={b.alt} />;
          case "chart": return <Chart key={i} spec={b} />;
          case "interactive": return <Interactive key={i} block={b} />;
          case "assignment": return <Assignment key={i} block={b} />;
          default: return null;
        }
      })}
    </div>
  );
}
```

*(Предполагаем компоненты `Markdown`, `Katex`, `Chart`, `Interactive`, `Assignment`.)*

---

# Анализ фото решения (pipeline)

1. **OCR/Math parse**: извлекаем формулы и структурируем по шагам.
2. **Сопоставление со «скелетом решения»** для этого задания.
3. **Семантическая проверка**: равенства, преобразования, переходы.
4. **Пояснения**: показываем, где именно сломан вывод, и «правильный путь».
5. **Обновление мастерства**: взвешенно (частичные баллы → небольшие апдейты).

---

# Доклады: «рецепт, не блюдо»

* `POST /report/assist` возвращает JSON:

  * `outline`: пункты плана с вопросами-подсказками.
  * `sources`: 5–8 ссылок (надежные/разные типы).
  * `checklist`: критерии оценки (структура, аргументы, цитирование, оформление).
* `POST /report/check`:

  * метрики: покрытие пунктов, логические дыры, доля цитируемого, формат ссылок, опечатки.
* На экране — **репетиция защиты**: ученик озвучивает тезисы (кнопка «тренировка речи»), родитель слушает и подтверждает.

---

# Безопасность и античитинг

* Подтверждение: пароль родителя + журнал (время, IP, подпись).
* Рандомизация вариантов, таймеры, «контрольные» без подсказок.
* Для докладов — **ссылки обязательны**, антиплагиат-скор, устная защита перед взрослым.

---

# База данных (упрощённо)

* `students(id, profile, settings)`
* `guardians(id, hashed_password, contacts)`
* `subjects(id, title)`
* `objectives(id, subject_id, code, title, prerequisites[])`
* `lessons(id, subject_id, json)`
* `items(id, json, objective_id, difficulty)`
* `plans(id, student_id, period_json)`
* `submissions(id, student_id, ref, json, score)`
* `mastery(student_id, objective_id, beta, p, updated_at)`
* `approvals(id, student_id, artifact, guardian_id, audit_json)`

---

# Что включить в MVP (8–10 недель)

1. Диагностика (адаптивная логика) по 1–2 предметам.
2. Генерация плана на месяц.
3. Рендер JSON-урока + интерактив + загрузка фото.
4. Автопроверка базовых типов: numeric, MCQ, короткий ответ; подсветка ошибок по фото (первый релиз — OCR + простые правила).
5. Досрочный зачёт по objective.
6. Контрольная и апдейт плана.
7. Кабинет родителя с паролем и журналом.
8. Дашборд прогресса (heatmap целей, график мастерства).

---

# Что нужно от тебя для старта

* Перечень **предметов и уровней** (например: *Mathematics Lower Secondary 7–8, English Reading/Writing*).
* Черновой список **objectives** (можем подготовить и отдать в JSON).
* Макеты 3–4 **уроков** с блоками (по образцу выше) — я помогу превратить в JSON.
* Политики порогов (пока: досрочно `0.85`, контрольная `0.8`).

Хочешь, я сразу соберу:

1. JSON-словарь целей по первому предмету,
2. 2 диагностических микротеста,
3. 1 урок с заданиями и проверкой,
4. шаблон дашборда прогресса (данные в JSON)?
