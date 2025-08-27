отличная идея — «оцифровать» творчество так, чтобы ИИ мог учить и проверять. Ниже дам:

1. curriculum JSON для **Art** и **Music** (Cambridge-style, по стадиям);
2. как проводить уроки онлайн: какие форматы заданий и как мы их проверяем;
3. примеры **Lesson JSON** + **AssessmentItem JSON** с фото/аудио/MIDI-проверкой;
4. минимальную технику анализа (что именно смотрим в картинке/звуке).

---

# 📑 Art (Cambridge-style) — Curriculum JSON

```json
{
  "id": "curriculum_art",
  "title": "Art & Design (Cambridge-style)",
  "subject": "Art",
  "stages": [
    {
      "id": "stage_primary",
      "title": "Primary",
      "age_range": [5,11],
      "modules": [
        { "id": "art_materials_primary", "title": "Materials & Tools (pencil, crayon, paint)", "recommended_hours": 25 },
        { "id": "art_elements_primary", "title": "Elements of Art (line, shape, color)", "recommended_hours": 30 },
        { "id": "art_observation_primary", "title": "Observation Drawing (simple objects)", "recommended_hours": 25 },
        { "id": "art_composition_primary", "title": "Composition & Story in Pictures", "recommended_hours": 20 }
      ]
    },
    {
      "id": "stage_lower_secondary",
      "title": "Lower Secondary",
      "age_range": [11,14],
      "modules": [
        { "id": "art_drawing_lower", "title": "Drawing Techniques (hatching, shading, perspective)", "recommended_hours": 35 },
        { "id": "art_color_lower", "title": "Color Theory (wheel, harmony, contrast)", "recommended_hours": 30 },
        { "id": "art_genres_lower", "title": "Genres & Styles (still life, landscape, portrait)", "recommended_hours": 30 },
        { "id": "art_digital_lower", "title": "Digital Art Basics (layers, brushes)", "recommended_hours": 25 }
      ]
    },
    {
      "id": "stage_upper_secondary",
      "title": "Upper Secondary (IGCSE Art & Design)",
      "age_range": [14,16],
      "modules": [
        { "id": "art_observation_upper", "title": "Advanced Observation & Proportion", "recommended_hours": 40 },
        { "id": "art_perspective_upper", "title": "Perspective & Composition (rule of thirds, focal points)", "recommended_hours": 35 },
        { "id": "art_media_upper", "title": "Media & Techniques (ink, watercolor, acrylic, digital)", "recommended_hours": 35 },
        { "id": "art_portfolio_upper", "title": "Coursework / Portfolio Project", "recommended_hours": 40 }
      ]
    },
    {
      "id": "stage_advanced",
      "title": "Advanced (A Level Art & Design)",
      "age_range": [16,19],
      "modules": [
        { "id": "art_research_advanced", "title": "Contextual Research & Artist Studies", "recommended_hours": 40 },
        { "id": "art_process_advanced", "title": "Process & Iteration (sketchbooks, experiments)", "recommended_hours": 45 },
        { "id": "art_specialism_advanced", "title": "Specialism (painting / illustration / digital)", "recommended_hours": 50 },
        { "id": "art_personal_advanced", "title": "Personal Investigation & Final Piece", "recommended_hours": 45 }
      ]
    }
  ]
}
```

## Как «учим» удалённо в Art

* **Видео-демо + пошаговые блоки** (штриховка, свет/тень, перспектива).
* **Задания в тетради/на холсте** → загрузка **фото**.
* Авто-анализ фото:

  * **композиция** (правило третей, расположение фокуса),
  * **перспектива/наклон** (линии схода),
  * **контраст/тональные диапазоны** (гистограммы),
  * **контуры/пропорции** (сравнение ключевых расстояний по рефу).
* Рубрика (композиция/тон/точность форм/техника) + комментарии.
* Для **digital art** — загрузка **PNG/PSD/Procreate export**: слои/кисти/маски (если есть метаданные).

---

# 🎼 Music (Cambridge-style) — Curriculum JSON

```json
{
  "id": "curriculum_music",
  "title": "Music (Cambridge-style)",
  "subject": "Music",
  "stages": [
    {
      "id": "stage_primary",
      "title": "Primary",
      "age_range": [5,11],
      "modules": [
        { "id": "music_listen_primary", "title": "Listening & Keeping the Beat", "recommended_hours": 30 },
        { "id": "music_pitch_primary", "title": "Pitch & Simple Notation (do–re–mi)", "recommended_hours": 25 },
        { "id": "music_rhythm_primary", "title": "Rhythm (quarter, eighth, rests)", "recommended_hours": 25 },
        { "id": "music_create_primary", "title": "Singing & Simple Composition", "recommended_hours": 20 }
      ]
    },
    {
      "id": "stage_lower_secondary",
      "title": "Lower Secondary",
      "age_range": [11,14],
      "modules": [
        { "id": "music_notation_lower", "title": "Staff Notation & Keys (C/G/F)", "recommended_hours": 30 },
        { "id": "music_scales_lower", "title": "Scales & Intervals (major/minor)", "recommended_hours": 30 },
        { "id": "music_rhythm_lower", "title": "Rhythm & Meter (2/4, 3/4, 4/4, syncopation)", "recommended_hours": 30 },
        { "id": "music_perform_lower", "title": "Performance Basics (voice/instrument)", "recommended_hours": 25 }
      ]
    },
    {
      "id": "stage_upper_secondary",
      "title": "Upper Secondary (IGCSE Music)",
      "age_range": [14,16],
      "modules": [
        { "id": "music_theory_upper", "title": "Music Theory (notation, harmony, chords)", "recommended_hours": 40 },
        { "id": "music_history_upper", "title": "Listening & Set Works (styles, forms)", "recommended_hours": 35 },
        { "id": "music_comp_upper", "title": "Composition (melody, harmony, structure)", "recommended_hours": 35 },
        { "id": "music_perf_upper", "title": "Performance (solo/ensemble) + Recording", "recommended_hours": 40 }
      ]
    },
    {
      "id": "stage_advanced",
      "title": "Advanced (A Level Music)",
      "age_range": [16,19],
      "modules": [
        { "id": "music_analysis_advanced", "title": "Advanced Analysis (form, harmony, counterpoint)", "recommended_hours": 45 },
        { "id": "music_comp_advanced", "title": "Advanced Composition & Orchestration", "recommended_hours": 50 },
        { "id": "music_perf_advanced", "title": "Advanced Performance & Interpretation", "recommended_hours": 50 },
        { "id": "music_technology_advanced", "title": "Music Technology (DAW, MIDI, notation software)", "recommended_hours": 35 }
      ]
    }
  ]
}
```

## Как «учим» удалённо в Music

* **Тренажёр нот**: экранная клавиатура/нотный стан; ученик кликает ноты или играет на MIDI-клавиатуре.
* **Ритм-тренажёр**: метроном + тап по клавише/тач-зоне → фиксируем тайминги.
* **Сольфеджио**: «повтори мелодию» → запись **аудио** (микрофон) → распознаём **высоту/интонацию/ритм**.
* **Теория**: упражнения на интервал, тональность, аккорды (MCQ, ввод).
* **Производительность**: загрузка **аудио/видео** или **MIDI** (из DAW/клавиш).

---

# 🔧 Типы заданий и проверки (обе дисциплины)

**Art (photo/file):**

* `photo` → CV-анализ: композиция (правило третей), контуры/пропорции, тональный диапазон, наличие штриховок/градиента.
* `file` (PNG/PSD/Procreate) → базовая метадата (размер, слои), превью.

**Music (audio/MIDI/interactive):**

* `audio` (WAV/MP3) → извлекаем **pitch contour**, **onset/tempo**, **intonation deviation**; сравниваем с эталоном.
* `midi` → ноты и длительности → прямой скоринг по шаблону.
* `interactive` → нотный стан/клавиатура: валидируем ответы по правилам теории.

---

# 🧩 Примеры JSON уроков и заданий

## Art — Lesson JSON (штриховка и тон)

```json
{
  "id": "lesson_art_shading_lower",
  "title": "Hatching & Shading Basics",
  "subject": "Art",
  "stage": "Lower Secondary",
  "module_id": "art_drawing_lower",
  "objectives": ["apply_basic_shading","control_line_density","observe_light_shadow"],
  "estimated_minutes": 45,
  "modules": [
    { "type": "intro", "blocks": [ { "type": "text", "md": "Учимся передавать объём с помощью штриховки и тонов." } ] },
    { "type": "concept", "blocks": [
      { "type": "image", "url": "https://cdn.example/shading_examples.png", "alt": "Примеры штриховки" },
      { "type": "text", "md": "Основные приёмы: параллельная, перекрёстная штриховка, растушёвка." }
    ]},
    { "type": "demo", "blocks": [
      { "type": "video", "url": "https://cdn.example/demo_shading.mp4", "caption": "Пошаговый разбор" }
    ]},
    { "type": "guided_practice", "blocks": [
      { "type": "interactive", "question_id": "item_art_shading_quiz1" }
    ]},
    { "type": "independent_practice", "blocks": [
      { "type": "assignment", "assignment_id": "hw_art_shading_sphere",
        "prompt_md": "Нарисуйте **шар** с источником света слева. Загрузите **фото** рисунка.",
        "submit_modes": ["photo"] }
    ]},
    { "type": "summary", "blocks": [ { "type": "text", "md": "Ключ: градации тона от света к тени, плавность переходов." } ] },
    { "type": "exit_ticket", "blocks": [ { "type": "interactive", "question_id": "item_art_exit1" } ] }
  ]
}
```

**Art — Item (мини-квиз по технике)**

```json
{
  "id": "item_art_shading_quiz1",
  "version": "1.0.0",
  "subject": "Art",
  "stage": "Lower Secondary",
  "objective": "apply_basic_shading",
  "bloom": "understand",
  "question": {
    "type": "mcq",
    "prompt_md": "Какой приём лучше всего создаёт **мягкий** переход тона?",
    "options": [
      { "id": "A", "text": "Чёткие параллельные линии" },
      { "id": "B", "text": "Перекрёстная штриховка" },
      { "id": "C", "text": "Растушёвка и постепенное уплотнение штрихов" }
    ],
    "answer": "C"
  },
  "scoring": { "points": 1 },
  "difficulty": 0.3
}
```

**Art — Проверка фото (Submission)**

```json
{
  "submission_id": "sub_art_001",
  "student_id": "stu_42",
  "ref": "hw_art_shading_sphere",
  "ref_type": "assignment",
  "mode": "photo",
  "artifacts": [{ "type": "image", "url": "store://uploads/stu_42/sphere.jpg" }],
  "submitted_at": "2025-08-26T12:00:00+07:00",
  "analysis": {
    "errors": [],
    "ocr_math": [],
    "ext": {
      "composition": { "rule_of_thirds_score": 0.7, "focus_in_hotspot": true },
      "tones": { "contrast_index": 0.62, "range_ok": true, "banding_detected": false },
      "edges": { "median_edge_strength": 0.44 }
    }
  },
  "feedback_md": "Хороший диапазон тонов. Попробуй добавить более **мягкий** полутон справа.",
  "auto_score": 0.8,
  "max_points": 1,
  "review_needed": false
}
```

---

## Music — Lesson JSON (ноты и ритм: C-мажор)

```json
{
  "id": "lesson_music_notation_lower",
  "title": "Staff Notation: C major & basic rhythm",
  "subject": "Music",
  "stage": "Lower Secondary",
  "module_id": "music_notation_lower",
  "objectives": ["read_staff_c_major","identify_rhythm_basic"],
  "estimated_minutes": 45,
  "modules": [
    { "type": "intro", "blocks": [ { "type": "text", "md": "Вспомним ноты **C–D–E–F–G–A–B** и простые длительности." } ] },
    { "type": "concept", "blocks": [
      { "type": "image", "url": "https://cdn.example/staff_c_major.png", "alt": "Нотный стан C major" },
      { "type": "text", "md": "Доли: четверть ♩, восьмая ♪, пауза 𝄽." }
    ]},
    { "type": "demo", "blocks": [
      { "type": "video", "url": "https://cdn.example/demo_play_c_scale.mp4", "caption": "Как играть гамму C-мажор" }
    ]},
    { "type": "guided_practice", "blocks": [
      { "type": "interactive", "question_id": "item_music_note_id_01" }
    ]},
    { "type": "independent_practice", "blocks": [
      { "type": "assignment", "assignment_id": "hw_music_play_c_major",
        "prompt_md": "Сыграй гамму **C-мажор** вверх-вниз **под метроном 80**. Отправь **MIDI** или **аудио**.",
        "submit_modes": ["file","audio"] }
    ]},
    { "type": "summary", "blocks": [ { "type": "text", "md": "Следи за устойчивыми нотами (C, G) и ровным пульсом." } ] }
  ]
}
```

**Music — Item (распознавание нот)**

```json
{
  "id": "item_music_note_id_01",
  "version": "1.0.0",
  "subject": "Music",
  "stage": "Lower Secondary",
  "objective": "read_staff_c_major",
  "bloom": "apply",
  "question": {
    "type": "mcq",
    "prompt_md": "Какая нота на этой линии?",
    "options": [
      { "id": "A", "text": "E" },
      { "id": "B", "text": "F" },
      { "id": "C", "text": "G" }
    ],
    "answer": "B"
  },
  "scoring": { "points": 1 },
  "difficulty": 0.3
}
```

**Music — Проверка MIDI/аудио (Submission)**

```json
{
  "submission_id": "sub_music_101",
  "student_id": "stu_42",
  "ref": "hw_music_play_c_major",
  "ref_type": "assignment",
  "mode": "file",
  "artifacts": [{ "type": "file", "url": "store://uploads/stu_42/c_major.mid" }],
  "submitted_at": "2025-08-26T12:15:00+07:00",
  "analysis": {
    "ext": {
      "midi": {
        "tempo_est": 80,
        "notes_expected": ["C4","D4","E4","F4","G4","A4","B4","C5","B4","A4","G4","F4","E4","D4","C4"],
        "notes_played": ["C4","D4","E4","F4","G4","A4","B4","C5","B4","A4","G4","F4","E4","D4","C4"],
        "timing_deviation_ms_avg": 42,
        "wrong_pitches": 0
      }
    }
  },
  "feedback_md": "Темп держишь ровно, среднее отклонение **42 мс** — отлично для старта. Попробуй довести до ~25 мс.",
  "auto_score": 0.9,
  "max_points": 1,
  "review_needed": false
}
```

*Если пришёл **аудио** вместо MIDI, анализ сохраняем схожим образом в `analysis.ext.audio`: `pitch_track`, `onsets`, `tempo_est`, `intonation_cents_avg`.*

---

# 🧪 Быстрый план «как это собрать» (техно-кратко)

* **Фронтенд**:

  * Art: просмотр примеров → загрузка фото → просмотр подсветки (маска тонов/линий, сетка третей).
  * Music: экранная **клавиатура/стан**, метроном, запись микрофона, загрузка **MIDI**.
* **Бэкенд анализ**:

  * Art: OpenCV/mediapipe-подобные эвристики (правило третей, доминирующие линии, histograms).
  * Music:

    * MIDI — прямой парсинг (mido),
    * Аудио — pitch detection (YIN/CREPE), onset detection, tempo tracking; рассчёт таймингов и интонации.
* **Оценивание**: через наши **рубрики** + авто-метрики (в `analysis.ext`).
* **Прозрачность**: в фидбеке показываем, **что именно** было хорошо/не очень (например, «слабый контраст теней» или «неровный ритм в тактах 3–4»).

---
