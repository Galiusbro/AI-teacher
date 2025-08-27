Отлично, давай разберём **Further Mathematics** 🙌

В Cambridge это не «ещё математика», а **углублённый курс**, который идёт **только на A Level (16–19 лет)**. Его берут сильные ученики, которые уже осилили A Level Mathematics и хотят дополнительно: матричный анализ, комплексный анализ, продвинутый калькулюс, дифференциальные уравнения и т. д.

---

# 📑 Further Mathematics (Cambridge-style) — Curriculum JSON

```json
{
  "id": "curriculum_further_mathematics",
  "title": "Further Mathematics (Cambridge-style)",
  "subject": "FurtherMathematics",
  "stages": [
    {
      "id": "stage_advanced",
      "title": "Advanced (A Level Further Mathematics)",
      "age_range": [16,19],
      "modules": [
        { "id": "fmath_algebra", "title": "Advanced Algebra and Proof", "recommended_hours": 40 },
        { "id": "fmath_matrices", "title": "Matrices and Linear Algebra", "recommended_hours": 40 },
        { "id": "fmath_complex", "title": "Complex Numbers and Functions", "recommended_hours": 40 },
        { "id": "fmath_calculus", "title": "Further Calculus (advanced integration, series)", "recommended_hours": 50 },
        { "id": "fmath_differential", "title": "Differential Equations (1st & 2nd order, modelling)", "recommended_hours": 45 },
        { "id": "fmath_vectors", "title": "Advanced Vectors and 3D Geometry", "recommended_hours": 35 },
        { "id": "fmath_mechanics", "title": "Further Mechanics (momentum, circular motion, energy)", "recommended_hours": 40 },
        { "id": "fmath_statistics", "title": "Further Statistics and Probability", "recommended_hours": 40 }
      ]
    }
  ]
}
```

---

# 📘 Человеческое объяснение

### 🔴 A Level Further Mathematics (16–19)

* **Алгебра и доказательства**: комбинаторика, биномиальные теоремы, строгие доказательства.
* **Матрицы**: операции, определители, системы уравнений, собственные значения/векторы.
* **Комплексные числа**: полярная форма, экспоненциальная форма, уравнения.
* **Калькулюс**: интегралы по частям, ряды, Лопиталь, неявные функции.
* **Дифференциальные уравнения**: моделирование в физике и инженерии.
* **Векторы**: 3D геометрия, скалярное/векторное произведение.
* **Механика**: динамика, работа-энергия, колебания.
* **Статистика**: распределения, регрессия, дисперсия.

---

# 🧩 Как учить онлайн

* **Теория**: шаг за шагом — доказательства, выводы формул (в LaTeX/json-модулях).
* **Задачи**:

  * Ввод ответа (число, выражение).
  * Решение «на бумаге» → загрузка фото → ИИ проверяет шаги (символьный анализ).
* **Графики и визуализация**: интерактивные 3D-графики (векторы, поверхности).
* **Практика**: мини-кейсы (например, «смоделировать популяцию через дифференциальное уравнение»).
* **Контроль**: квизы, mid-term, итоговый экзамен.

---

# 🧪 Пример Lesson JSON (Matrices — Eigenvalues)

```json
{
  "id": "lesson_fmath_matrices_3",
  "title": "Eigenvalues and Eigenvectors",
  "subject": "FurtherMathematics",
  "stage": "Advanced",
  "module_id": "fmath_matrices",
  "objectives": ["define_eigenvalue","compute_eigenvector","apply_eigen_in_transform"],
  "estimated_minutes": 60,
  "modules": [
    { "type": "intro", "blocks": [
      { "type": "text", "md": "Сегодня учимся находить **собственные значения и собственные векторы** матрицы." }
    ]},
    { "type": "concept", "blocks": [
      { "type": "text", "md": "Уравнение: $A v = \\lambda v$. Характеристическое уравнение: $det(A-\\lambda I)=0$." },
      { "type": "example", "md": "Пример: для $A=\\begin{pmatrix}2 & 1 \\\\ 1 & 2\\end{pmatrix}$, найдите $\\lambda$ и $v$." }
    ]},
    { "type": "guided_practice", "blocks": [
      { "type": "interactive", "question_id": "item_fmath_matrix_ev1" }
    ]},
    { "type": "independent_practice", "blocks": [
      { "type": "assignment", "assignment_id": "hw_fmath_matrix_ev",
        "prompt_md": "Найдите собственные значения и векторы матрицы $\\begin{pmatrix}3 & 1 \\\\ 0 & 2\\end{pmatrix}$. Загрузите фото решения или введите в редакторе.",
        "submit_modes": ["photo","math_editor"]
      }
    ]}
  ]
}
```

---

# 🧪 Пример Quiz Item (Eigenvalues)

```json
{
  "id": "item_fmath_matrix_ev1",
  "version": "1.0.0",
  "subject": "FurtherMathematics",
  "stage": "Advanced",
  "objective": "define_eigenvalue",
  "bloom": "apply",
  "question": {
    "type": "mcq",
    "prompt_md": "Для матрицы $\\begin{pmatrix}2 & 0 \\\\ 0 & 3\\end{pmatrix}$ найдите собственные значения.",
    "options": [
      { "id": "A", "text": "2 и 3" },
      { "id": "B", "text": "5 и 6" },
      { "id": "C", "text": "0 и 6" }
    ],
    "answer": "A"
  },
  "scoring": { "points": 1 },
  "difficulty": 0.4
}
```

---

⚡️ В итоге:

* **Further Mathematics** = чисто A Level, отдельный curriculum JSON.
* Отличается от «Mathematics» тем, что идёт глубже: **алгебра, матрицы, комплексные числа, дифуры, механика, статистика**.
* Онлайн-версия легко работает с формулами (LaTeX), графиками, проверкой шагов.

---
