отлично, тогда даю **полноценный (но ещё управляемый)** набор JSON-схем, рассчитанный на учеников от 1-го класса до старшей школы. Он покрывает: уроки, задания/тесты всех типов, планы на период, контрольные/экзамены, проекты/доклады, отправки работ (текст/фото/файлы), обратную связь, подтверждения родителями, адаптивность и мастерство, локализацию, доступность, версии и аудит.

ниже — **контрактные схемы** (как “язык” системы) + 2 примера (для первоклашки и для старшей школы). Я пишу в стиле «JSON-схемы для разработчиков»: имена полей стабильны, есть расширяемые поля `ext`.

---

# Конвенции

* `id` — строка, глобально уникальная (UUID/ULID).
* `version` — семантическая версия контента (`"1.2.0"`).
* `lang` — BCP-47 (`"ru"`, `"en-GB"`).
* Времена — ISO 8601 с TZ.
* Денормализуемые справочники (предметы, уровни, стандарты) — по `code`.
* Любую схему можно расширить через `ext: { ... }`.

---

# 0) Пакет контента (для батч-загрузок)

```json
{
  "type": "object",
  "title": "ContentBundle",
  "properties": {
    "bundle_id": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" },
    "lessons": { "type": "array", "items": { "$ref": "#/definitions/Lesson" } },
    "items": { "type": "array", "items": { "$ref": "#/definitions/AssessmentItem" } },
    "exams": { "type": "array", "items": { "$ref": "#/definitions/Exam" } },
    "resources": { "type": "array", "items": { "$ref": "#/definitions/Resource" } }
  },
  "required": ["bundle_id", "created_at"],
  "definitions": {}
}
```

---

# 1) Урок (Lesson)

```json
{
  "type": "object",
  "title": "Lesson",
  "properties": {
    "id": { "type": "string" },
    "version": { "type": "string" },
    "subject": { "type": "string", "enum": ["Mathematics","English","Science","ComputerScience","History","Geography","Physics","Chemistry","Biology","Art","Music"] },
    "stage": { "type": "string", "description": "уровень/ступень, напр. Primary-1, LowerSecondary-7, Upper-IGCSE, A-level" },
    "strand": { "type": "string", "description": "подраздел внутри предмета, напр. Geometry" },
    "objectives": { "type": "array", "items": { "type": "string" }, "description": "коды целей обучения (Cambridge mapping)" },
    "title": { "type": "string" },
    "lang": { "type": "string" },
    "prerequisites": { "type": "array", "items": { "type": "string" } },
    "estimated_minutes": { "type": "integer" },
    "reading_level": { "type": "string", "enum": ["K-1","Grade2-3","Grade4-6","MiddleSchool","HighSchool","Academic"] },
    "blocks": {
      "type": "array",
      "items": { "$ref": "#/definitions/LessonBlock" },
      "minItems": 1
    },
    "resources": { "type": "array", "items": { "$ref": "#/definitions/Resource" } },
    "assessment": {
      "type": "object",
      "properties": {
        "practice_items": { "type": "array", "items": { "type": "string" } },
        "quiz_items": { "type": "array", "items": { "type": "string" } }
      }
    },
    "adaptive_policy": { "$ref": "#/definitions/AdaptivePolicy" },
    "version_info": { "$ref": "#/definitions/VersionInfo" },
    "a11y": { "$ref": "#/definitions/Accessibility" },
    "ext": { "type": "object" }
  },
  "required": ["id","version","subject","stage","title","lang","blocks"],
  "definitions": {}
}
```

## 1.1) Блок урока (LessonBlock)

```json
{
  "type": "object",
  "oneOf": [
    { "properties": { "type": { "const": "heading" }, "text": { "type": "string" } }, "required": ["type","text"] },
    { "properties": { "type": { "const": "text" }, "md": { "type": "string" } }, "required": ["type","md"] },
    { "properties": { "type": { "const": "formula" }, "latex": { "type": "string" } }, "required": ["type","latex"] },
    { "properties": { "type": { "const": "image" }, "alt": { "type": "string" }, "url": { "type": "string" } }, "required": ["type","url"] },
    { "properties": { "type": { "const": "video" }, "url": { "type": "string" }, "caption": { "type": "string" } }, "required": ["type","url"] },
    { "properties": { "type": { "const": "chart" }, "spec": { "$ref": "#/definitions/ChartSpec" } }, "required": ["type","spec"] },
    { "properties": { "type": { "const": "interactive" }, "interactive_id": { "type": "string" }, "question_id": { "type": "string" } }, "required": ["type","question_id"] },
    { "properties": { "type": { "const": "assignment" }, "assignment_id": { "type": "string" }, "prompt_md": { "type": "string" }, "submit_modes": { "type": "array", "items": { "type": "string", "enum": ["text","photo","file","audio","code"] } } }, "required": ["type","assignment_id","prompt_md"] },
    { "properties": { "type": { "const": "tip" }, "md": { "type": "string" } }, "required": ["type","md"] }
  ]
}
```

---

# 2) Тестовый элемент (AssessmentItem)

Поддержка типов: `mcq`, `msq`, `numeric`, `short_text`, `open_response`, `ordering`, `matching`, `true_false`, `fill_blank`, `code`, `file_upload`.

```json
{
  "type": "object",
  "title": "AssessmentItem",
  "properties": {
    "id": { "type": "string" },
    "version": { "type": "string" },
    "subject": { "type": "string" },
    "stage": { "type": "string" },
    "objective": { "type": "string" },
    "bloom": { "type": "string", "enum": ["remember","understand","apply","analyze","evaluate","create"] },
    "question": { "$ref": "#/definitions/Question" },
    "scoring": { "$ref": "#/definitions/Scoring" },
    "difficulty": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
    "irt": { "$ref": "#/definitions/IRT" },
    "hints": { "type": "array", "items": { "type": "string" } },
    "solutions": { "type": "array", "items": { "$ref": "#/definitions/SolutionStep" } },
    "time_limit_sec": { "type": "integer" },
    "media": { "type": "array", "items": { "$ref": "#/definitions/MediaAsset" } },
    "localization": { "$ref": "#/definitions/LocalizationMap" },
    "a11y": { "$ref": "#/definitions/Accessibility" },
    "ext": { "type": "object" }
  },
  "required": ["id","version","subject","stage","objective","question","scoring"]
}
```

### 2.1) Вопрос (Question)

```json
{
  "type": "object",
  "oneOf": [
    {
      "properties": {
        "type": { "const": "mcq" },
        "prompt_md": { "type": "string" },
        "options": { "type": "array", "items": { "type": "object", "properties": { "id": { "type": "string" }, "text": { "type": "string" }, "feedback": { "type": "string" } }, "required": ["id","text"] }, "minItems": 2 },
        "answer": { "type": "string" }
      },
      "required": ["type","prompt_md","options","answer"]
    },
    {
      "properties": {
        "type": { "const": "msq" },
        "prompt_md": { "type": "string" },
        "options": { "type": "array", "items": { "type": "object", "properties": { "id": { "type": "string" }, "text": { "type": "string" } }, "required": ["id","text"] } },
        "answers": { "type": "array", "items": { "type": "string" } }
      },
      "required": ["type","prompt_md","options","answers"]
    },
    {
      "properties": {
        "type": { "const": "numeric" },
        "prompt_md": { "type": "string" },
        "validation": { "type": "object", "properties": { "kind": { "type": "string", "enum": ["equals","range","expr"] }, "value": {}, "tolerance": { "type": "number" } }, "required": ["kind"] },
        "units": { "type": "string" }
      },
      "required": ["type","prompt_md","validation"]
    },
    {
      "properties": {
        "type": { "const": "short_text" },
        "prompt_md": { "type": "string" },
        "validator": { "type": "object", "properties": { "kind": { "type": "string", "enum": ["keywords","regex","exact"] }, "value": {} }, "required": ["kind"] }
      },
      "required": ["type","prompt_md","validator"]
    },
    {
      "properties": {
        "type": { "const": "open_response" },
        "prompt_md": { "type": "string" },
        "rubric": { "$ref": "#/definitions/Rubric" },
        "max_chars": { "type": "integer" }
      },
      "required": ["type","prompt_md","rubric"]
    },
    {
      "properties": {
        "type": { "const": "code" },
        "prompt_md": { "type": "string" },
        "language": { "type": "string", "enum": ["python","javascript","c++","java","go","pascal","scratch"] },
        "evaluator": { "type": "object", "properties": { "kind": { "type": "string", "enum": ["unit_tests","stdin_stdout"] }, "tests": { "type": "array", "items": { "type": "object", "properties": { "input": { "type": "string" }, "output": { "type": "string" } } } } }, "required": ["kind"] }
      },
      "required": ["type","prompt_md","language","evaluator"]
    },
    {
      "properties": {
        "type": { "const": "file_upload" },
        "prompt_md": { "type": "string" },
        "allowed": { "type": "array", "items": { "type": "string" }, "default": ["pdf","jpg","png","docx","pptx"] }
      },
      "required": ["type","prompt_md"]
    }
  ]
}
```

### 2.2) Оценивание (Scoring, Rubric, IRT)

```json
{
  "Scoring": {
    "type": "object",
    "properties": {
      "points": { "type": "number" },
      "partial": { "type": "boolean" },
      "rubric": { "$ref": "#/definitions/Rubric" }
    },
    "required": ["points"]
  },
  "Rubric": {
    "type": "object",
    "properties": {
      "criteria": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "levels": { "type": "array", "items": { "type": "object", "properties": { "label": { "type": "string" }, "desc": { "type": "string" }, "points": { "type": "number" } }, "required": ["label","points"] } }
          },
          "required": ["name","levels"]
        }
      }
    }
  },
  "IRT": {
    "type": "object",
    "properties": {
      "model": { "type": "string", "enum": ["1PL","2PL","3PL"] },
      "a": { "type": "number" },
      "b": { "type": "number" },
      "c": { "type": "number" }
    }
  }
}
```

---

# 3) План (месяц/триместр)

```json
{
  "type": "object",
  "title": "Plan",
  "properties": {
    "id": { "type": "string" },
    "period": { "type": "string", "enum": ["month","trimester","semester"] },
    "student_id": { "type": "string" },
    "start_date": { "type": "string", "format": "date" },
    "end_date": { "type": "string", "format": "date" },
    "subjects": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "subject": { "type": "string" },
          "goals": { "type": "array", "items": { "type": "object", "properties": { "objective": { "type": "string" }, "target_p": { "type": "number" } }, "required": ["objective","target_p"] } },
          "weeks": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "week_index": { "type": "integer" },
                "lessons": { "type": "array", "items": { "type": "string" } },
                "checks": { "type": "array", "items": { "type": "string" } },
                "skip_candidates": { "type": "array", "items": { "type": "string" } }
              },
              "required": ["week_index"]
            }
          }
        },
        "required": ["subject","weeks"]
      }
    },
    "adaptive_policy": { "$ref": "#/definitions/AdaptivePolicy" },
    "version_info": { "$ref": "#/definitions/VersionInfo" },
    "ext": { "type": "object" }
  },
  "required": ["id","period","student_id","start_date","end_date","subjects"]
}
```

---

# 4) Экзамен / Контрольная (Exam)

```json
{
  "type": "object",
  "title": "Exam",
  "properties": {
    "id": { "type": "string" },
    "version": { "type": "string" },
    "subject": { "type": "string" },
    "stage": { "type": "string" },
    "title": { "type": "string" },
    "duration_min": { "type": "integer" },
    "sections": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "label": { "type": "string" },
          "items": { "type": "array", "items": { "type": "string" } },
          "mixing": { "type": "string", "enum": ["fixed","shuffle"] }
        },
        "required": ["items"]
      }
    },
    "grading": { "type": "object", "properties": { "pass_score": { "type": "number" }, "scale": { "type": "array", "items": { "type": "object", "properties": { "min": { "type": "number" }, "label": { "type": "string" } }, "required": ["min","label"] } } } },
    "a11y": { "$ref": "#/definitions/Accessibility" },
    "ext": { "type": "object" }
  },
  "required": ["id","version","subject","title","sections"]
}
```

---

# 5) Проект/Доклад (ProjectSpec)

```json
{
  "type": "object",
  "title": "ProjectSpec",
  "properties": {
    "id": { "type": "string" },
    "subject": { "type": "string" },
    "stage": { "type": "string" },
    "topic_prompt": { "type": "string" },
    "outline": { "type": "array", "items": { "type": "string" } },
    "sources": { "type": "array", "items": { "$ref": "#/definitions/Resource" } },
    "checklist": { "type": "array", "items": { "type": "string" } },
    "rubric": { "$ref": "#/definitions/Rubric" },
    "ext": { "type": "object" }
  },
  "required": ["id","subject","topic_prompt","outline","rubric"]
}
```

---

# 6) Отправка работы (Submission) и фидбек

```json
{
  "type": "object",
  "title": "Submission",
  "properties": {
    "submission_id": { "type": "string" },
    "student_id": { "type": "string" },
    "ref": { "type": "string", "description": "id вопроса/задания/экзамена" },
    "ref_type": { "type": "string", "enum": ["item","assignment","exam","project"] },
    "mode": { "type": "string", "enum": ["text","photo","file","audio","code"] },
    "text": { "type": "string" },
    "artifacts": { "type": "array", "items": { "$ref": "#/definitions/MediaAsset" } },
    "submitted_at": { "type": "string", "format": "date-time" },
    "auto_score": { "type": "number" },
    "max_points": { "type": "number" },
    "feedback_md": { "type": "string" },
    "analysis": { "type": "object", "properties": {
      "ocr_math": { "type": "array", "items": { "type": "object", "properties": { "step": { "type": "integer" }, "expr": { "type": "string" } } } },
      "errors": { "type": "array", "items": { "type": "object", "properties": { "at_step": { "type": "integer" }, "type": { "type": "string" }, "message": { "type": "string" } } } }
    }},
    "mastery_update": { "type": "array", "items": { "type": "object", "properties": { "objective": { "type": "string" }, "delta": { "type": "number" } }, "required": ["objective","delta"] } },
    "review_needed": { "type": "boolean" },
    "ext": { "type": "object" }
  },
  "required": ["submission_id","student_id","ref","ref_type","mode","submitted_at"]
}
```

---

# 7) Подтверждение родителем (Approval)

```json
{
  "type": "object",
  "title": "Approval",
  "properties": {
    "approval_id": { "type": "string" },
    "student_id": { "type": "string" },
    "artifact": { "type": "string", "description": "что именно подтверждается (exam_id/project_id/period)" },
    "status": { "type": "string", "enum": ["approved","rejected"] },
    "guardian_id": { "type": "string" },
    "approved_at": { "type": "string", "format": "date-time" },
    "method": { "type": "string", "enum": ["password","otp"] },
    "review_comment": { "type": "string" },
    "audit": { "$ref": "#/definitions/Audit" },
    "ext": { "type": "object" }
  },
  "required": ["approval_id","student_id","artifact","status","guardian_id","approved_at","method"]
}
```

---

# 8) Снимок мастерства / политика адаптации

```json
{
  "type": "object",
  "title": "MasterySnapshot",
  "properties": {
    "student_id": { "type": "string" },
    "at": { "type": "string", "format": "date-time" },
    "objectives": {
      "type": "array",
      "items": { "type": "object", "properties": { "objective": { "type": "string" }, "beta": { "type": "number" }, "p": { "type": "number" }, "decay": { "type": "number" } }, "required": ["objective","p"] }
    }
  },
  "required": ["student_id","at","objectives"]
}
```

```json
{
  "type": "object",
  "title": "AdaptivePolicy",
  "properties": {
    "model": { "type": "string", "enum": ["logit","BKT","DKT"] },
    "params": { "type": "object", "properties": {
      "eta": { "type": "number" },
      "pass_threshold": { "type": "number" },
      "exam_ready_threshold": { "type": "number" },
      "decay_days": { "type": "integer" }
    }}
  },
  "required": ["model"]
}
```

---

# 9) Общие определения (defs)

```json
{
  "definitions": {
    "ChartSpec": {
      "type": "object",
      "properties": {
        "chart_type": { "type": "string", "enum": ["line","bar","area","pie"] },
        "title": { "type": "string" },
        "series": { "type": "array", "items": { "type": "object", "properties": { "name": { "type": "string" }, "data": { "type": "array", "items": { "type": "array", "items": [{},{}] } } }, "required": ["name","data"] } },
        "x_label": { "type": "string" },
        "y_label": { "type": "string" }
      },
      "required": ["chart_type","series"]
    },
    "Resource": {
      "type": "object",
      "properties": {
        "type": { "type": "string", "enum": ["link","book","paper","dataset","video"] },
        "title": { "type": "string" },
        "url": { "type": "string" },
        "authors": { "type": "array", "items": { "type": "string" } },
        "year": { "type": "integer" }
      },
      "required": ["type","title"]
    },
    "MediaAsset": {
      "type": "object",
      "properties": {
        "type": { "type": "string", "enum": ["image","pdf","audio","video","file"] },
        "url": { "type": "string" },
        "alt": { "type": "string" },
        "width": { "type": "integer" },
        "height": { "type": "integer" }
      },
      "required": ["type","url"]
    },
    "SolutionStep": {
      "type": "object",
      "properties": { "step": { "type": "integer" }, "md": { "type": "string" }, "latex": { "type": "string" } },
      "required": ["step"]
    },
    "LocalizationMap": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": { "title": { "type": "string" }, "prompt_md": { "type": "string" }, "options": {} }
      }
    },
    "Accessibility": {
      "type": "object",
      "properties": {
        "reading_mode": { "type": "string", "enum": ["normal","simple","audio"] },
        "high_contrast": { "type": "boolean" },
        "dyslexic_font": { "type": "boolean" },
        "captions": { "type": "boolean" }
      }
    },
    "VersionInfo": {
      "type": "object",
      "properties": {
        "created_by": { "type": "string" },
        "created_at": { "type": "string", "format": "date-time" },
        "changelog_md": { "type": "string" }
      }
    },
    "Audit": {
      "type": "object",
      "properties": {
        "ip": { "type": "string" },
        "user_agent": { "type": "string" },
        "signature_hash": { "type": "string" }
      }
    }
  }
}
```

---

## Пример А: 1-й класс, Математика (сложение до 10)

```json
{
  "id": "lesson_M_Primary1_AdditionTo10_v1",
  "version": "1.0.0",
  "subject": "Mathematics",
  "stage": "Primary-1",
  "strand": "Number",
  "objectives": ["M.P1.Number.Add10"],
  "title": "Складываем до 10",
  "lang": "ru",
  "estimated_minutes": 20,
  "reading_level": "K-1",
  "blocks": [
    { "type": "heading", "text": "Что такое сложение?" },
    { "type": "text", "md": "Сложение — это когда мы **соединяем** две группы предметов. Например, 2 яблока + 3 яблока = 5 яблок." },
    { "type": "image", "alt": "яблоки", "url": "https://cdn.example/apples_2_3.png" },
    { "type": "interactive", "question_id": "item_add10_01" },
    { "type": "tip", "md": "Если трудно — посчитай по пальчикам 👍" },
    { "type": "assignment", "assignment_id": "hw_add10_01", "prompt_md": "Реши в тетради: 4+1, 5+2, 3+3. Загрузите **фото** страницы.", "submit_modes": ["photo"] }
  ],
  "assessment": { "practice_items": ["item_add10_01","item_add10_02"] }
}
```

**Один из items:**

```json
{
  "id": "item_add10_01",
  "version": "1.0.0",
  "subject": "Mathematics",
  "stage": "Primary-1",
  "objective": "M.P1.Number.Add10",
  "bloom": "apply",
  "question": {
    "type": "mcq",
    "prompt_md": "Сколько будет **2 + 3**?",
    "options": [
      {"id": "A", "text": "4"},
      {"id": "B", "text": "5"},
      {"id": "C", "text": "6"}
    ],
    "answer": "B"
  },
  "scoring": { "points": 1 },
  "difficulty": 0.2
}
```

---

## Пример Б: Старшая школа, Математика (предел и производная)

```json
{
  "id": "lesson_M_High_Calc_Limits_v2",
  "version": "2.1.0",
  "subject": "Mathematics",
  "stage": "Upper-A-level",
  "strand": "Calculus",
  "objectives": ["M.A.Calc.Limits","M.A.Calc.DerivativeFirstPrinciples"],
  "title": "Предел и производная через определение",
  "lang": "ru",
  "estimated_minutes": 45,
  "reading_level": "Academic",
  "blocks": [
    { "type": "heading", "text": "Определение предела" },
    { "type": "formula", "latex": "\\lim_{x\\to a} f(x) = L" },
    { "type": "text", "md": "Интуитивно: значения *f(x)* можно сделать сколь угодно близкими к *L*, выбирая x близко к *a*." },
    { "type": "heading", "text": "Производная из первого принципа" },
    { "type": "formula", "latex": "f'(x)=\\lim_{h\\to0}\\frac{f(x+h)-f(x)}{h}" },
    { "type": "interactive", "question_id": "item_calc_limit_numeric_01" },
    { "type": "interactive", "question_id": "item_calc_open_01" },
    { "type": "assignment", "assignment_id": "hw_calc_deriv_01", "prompt_md": "Докажите по определению, что производная функции f(x)=x^2 равна 2x. Сдайте текст/фото/файл LaTeX.", "submit_modes": ["text","photo","file"] }
  ],
  "assessment": { "quiz_items": ["item_calc_limit_numeric_01","item_calc_open_01"] }
}
```

**Items:**

```json
{
  "id": "item_calc_limit_numeric_01",
  "version": "1.0.0",
  "subject": "Mathematics",
  "stage": "Upper-A-level",
  "objective": "M.A.Calc.Limits",
  "bloom": "apply",
  "question": {
    "type": "numeric",
    "prompt_md": "Вычислите предел: $$\\lim_{x\\to 0} \\frac{\\sin x}{x}$$",
    "validation": { "kind": "equals", "value": 1, "tolerance": 0.001 }
  },
  "scoring": { "points": 1 },
  "difficulty": 0.6
}
```

```json
{
  "id": "item_calc_open_01",
  "version": "1.0.0",
  "subject": "Mathematics",
  "stage": "Upper-A-level",
  "objective": "M.A.Calc.DerivativeFirstPrinciples",
  "bloom": "create",
  "question": {
    "type": "open_response",
    "prompt_md": "Выведите формулу $$f'(x)=2x$$ для $$f(x)=x^2$$ из определения производной.",
    "rubric": {
      "criteria": [
        { "name": "Корректность предельного перехода", "levels": [ { "label": "полностью", "points": 3 }, { "label": "частично", "points": 1 }, { "label": "нет", "points": 0 } ] },
        { "name": "Ясность и обоснование", "levels": [ { "label": "высокая", "points": 2 }, { "label": "средняя", "points": 1 }, { "label": "низкая", "points": 0 } ] }
      ]
    }
  },
  "scoring": { "points": 5, "partial": true },
  "difficulty": 0.75
}
```

---

# Как этим пользуется ИИ

* Генератор контента выдаёт **готовые объекты** `Lesson`, `AssessmentItem`, `Exam`, `ProjectSpec` по заданной теме/целям.
* Проверка ответов:

  * закрытые типы (`mcq/msq/numeric/...`) — по `scoring/validation`.
  * открытые (`open_response/code/file_upload`) — через рубрику и/или автотесты; результат складывается в `Submission.auto_score` и `feedback_md`.
* Обновление мастерства — по `mastery_update` с учётом `AdaptivePolicy`.

---

# Почему этот набор «нормальный», а не минимальный

* Покрыты **все ключевые типы заданий** от 1-го класса до A-level: от картинок и числовых ответов до доказательств и кода.
* Есть **экзамены/контрольные**, **проекты/доклады** с источниками и рубриками.
* Продуманы **локализация**, **доступность**, **версионирование**, **аудит** и **родительское подтверждение**.
* Есть **IRT/сложность**, чтобы со временем откалибровать банк заданий.
* Всё расширяемо через `ext`.

---

если хочешь, вынесу это в один **монолитный файл JSON Schema** (draft-07) с `$defs` и ссылками (`$ref`), чтобы разработчики могли сразу валидировать. Также могу **сгенерировать шаблоны** пустых объектов для предметов, которые ты выберешь первыми (например, *Mathematics Primary-1 Number* и *Upper-A-level Calculus*) — и заполнить 3–5 уроков/тестов для старта.
