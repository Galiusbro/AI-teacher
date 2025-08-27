#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import math

# ---------- Конфиг ----------

@dataclass
class MasteryConfig:
    # Веса компонентов
    w_accuracy: float = 0.45
    w_speed: float = 0.2
    w_consistency: float = 0.15
    w_difficulty: float = 0.1
    w_spacing: float = 0.1

    # Ожидаемые времена базовые (сек)
    expected_times: Dict[str, int] = None
    # Пороги точности по типам
    accuracy_thresholds: Dict[str, float] = None
    # Коэф. сложности (модификатор ожидаемого времени)
    difficulty_time_mult: Dict[str, float] = None
    # Мини-порог на время (анти-чит)
    min_time_floor_sec: int = 8
    # EMA для обновления мастерства
    ema_alpha_min: float = 0.2
    ema_alpha_max: float = 0.6
    ema_warmup_n: int = 5  # пока мало попыток — выше alpha
    # Оптимальный интервал (база, сек) при mastery≈0.7
    spacing_base_sec: int = 24*60*60

    def __post_init__(self):
        if self.expected_times is None:
            self.expected_times = {"concept": 300, "guided": 600, "independent": 900, "assessment": 1200}
        if self.accuracy_thresholds is None:
            self.accuracy_thresholds = {"concept": 0.6, "guided": 0.7, "independent": 0.8, "assessment": 0.85}
        if self.difficulty_time_mult is None:
            self.difficulty_time_mult = {"easy": 0.85, "medium": 1.0, "hard": 1.2}

# ---------- Калькулятор ----------

class MasteryCalculatorV2:
    def __init__(self, cfg: Optional[MasteryConfig] = None):
        self.cfg = cfg or MasteryConfig()

    # ---- Публичные методы ----

    def lesson_mastery(
        self,
        submissions_history: List[Dict[str, Any]],
        lesson_type: str,
        time_spent_sec: int,
        score: float,  # 0..1
        difficulty: str = "medium",
        student_speed_factor: float = 1.0  # <1 быстрее среднего, >1 медленнее
    ) -> Tuple[float, Dict[str, float]]:
        """
        Возвращает (mastery, diagnostics)
        """
        acc = self._score_accuracy(score, lesson_type)
        spd = self._score_speed(time_spent_sec, lesson_type, difficulty, student_speed_factor)
        cns = self._score_consistency(submissions_history, lesson_type)
        dif = self._score_difficulty(difficulty)
        spc = self._score_spacing(submissions_history)

        mastery = (
            self.cfg.w_accuracy*acc +
            self.cfg.w_speed*spd +
            self.cfg.w_consistency*cns +
            self.cfg.w_difficulty*dif +
            self.cfg.w_spacing*spc
        )
        mastery = max(0.0, min(1.0, mastery))
        diag = {"accuracy": acc, "speed": spd, "consistency": cns, "difficulty": dif, "spacing": spc, "overall": mastery}
        return round(mastery, 3), diag

    def update_mastery_ema(
        self,
        current_mastery: Dict[str, Any],
        lesson_type: str,
        lesson_mastery_value: float,
        total_submissions: int
    ) -> Dict[str, Any]:
        """
        Обновляет per-type и overall по EMA, а не «перезаписью».
        """
        cur = dict(current_mastery or {})
        # инициализация
        for k in ("concept","guided","independent","assessment"):
            cur.setdefault(k, 0.0)
        cur.setdefault("overall", 0.0)
        cur.setdefault("last_updated", datetime.now().isoformat())
        cur.setdefault("total_submissions", 0)

        alpha = self._ema_alpha(total_submissions)
        cur[lesson_type] = (1 - alpha) * cur[lesson_type] + alpha * lesson_mastery_value

        # взвешенное среднее типов (можно подстроить под module.lesson_policy)
        weights = {"concept": 0.3, "guided": 0.25, "independent": 0.25, "assessment": 0.2}
        overall = 0.0
        total_w = 0.0
        for k, w in weights.items():
            overall += cur.get(k, 0.0) * w
            total_w += w
        cur["overall"] = round(overall / total_w if total_w else 0.0, 3)
        cur["last_updated"] = datetime.now().isoformat()
        cur["total_submissions"] = int(total_submissions)
        return cur

    def recommend_next_lesson_type(
        self,
        current_mastery: Dict[str, Any],
        lesson_policy_mix: Dict[str, float],  # { "concept":0.3,... }
        counters: Dict[str, int],             # пройдено по типам
        gates: Dict[str, int] = None          # {"independent_min_concept":1, ...}
    ) -> Tuple[str, str]:
        """
        Возвращает (next_type, explanation)
        """
        overall = float(current_mastery.get("overall", 0.0))
        counters = counters or {}
        mix = lesson_policy_mix or {"concept":0.3,"guided":0.25,"independent":0.25,"assessment":0.2}
        gates = gates or {"independent_min_concept": 1, "assessment_min_independent": 1}

        # 1) базовая логика по мастерству
        if overall < 0.3:
            base = "concept"
        elif overall < 0.6:
            base = "guided"
        elif overall < 0.85:
            base = "independent"
        else:
            base = "assessment"

        # 2) проверка гейтов
        concept_done = counters.get("concept", 0)
        indep_done = counters.get("independent", 0)
        if base in ("independent","assessment"):
            if concept_done < gates["independent_min_concept"]:
                base = "concept"
        if base == "assessment" and indep_done < gates["assessment_min_independent"]:
            base = "independent"

        # 3) выравнивание под целевой микс (ищем «недокормленный» тип)
        total = sum(counters.get(k,0) for k in mix.keys()) or 1
        deficits = []
        for k, target_share in mix.items():
            actual_share = counters.get(k,0) / total
            deficits.append((k, target_share - actual_share))
        deficits.sort(key=lambda x: x[1], reverse=True)
        most_under = deficits[0][0] if deficits else base

        # финальный выбор: если «база» и «недокормленный» не конфликтуют сильно — отдаём недокормленный
        next_type = most_under if self._compatible(base, most_under) else base

        explain = f"overall={overall:.2f}, base={base}, underfed={most_under}, counters={counters}, mix={mix}"
        return next_type, explain

    # ---- Частные метрики ----

    def _score_accuracy(self, score: float, lesson_type: str) -> float:
        thr = self.cfg.accuracy_thresholds.get(lesson_type, 0.7)
        # гладко нормируем относительно порога (логистикой)
        # s==thr -> ~0.5; выше порога растёт к 1, ниже к 0
        k = 12.0
        x = score - thr
        return round(1/(1 + math.exp(-k*x)), 3)

    def _score_speed(self, t_sec: int, lesson_type: str, difficulty: str, speed_factor: float) -> float:
        if t_sec < self.cfg.min_time_floor_sec:
            # слишком быстро — вероятно, щёлкнули «далее»
            return 0.2
        base = self.cfg.expected_times.get(lesson_type, 600)
        mult = self.cfg.difficulty_time_mult.get(difficulty, 1.0)
        expected = base * mult * max(0.5, min(1.5, speed_factor))
        # отношение факта к ожиданию → логистическая оценка
        ratio = t_sec / max(1.0, expected)
        # лучше чуть быстрее ожидаемого; 1.0 → 0.8–0.9; 0.6 → 1.0; 1.6 → 0.5
        # превращаем в score симметрично вокруг ~1.0
        k = 6.0
        x = 1.0 - ratio
        return round(1/(1 + math.exp(-k*x)), 3)

    def _score_consistency(self, subs: List[Dict[str,Any]], lesson_type: str) -> float:
        if not subs:
            return 0.5
        # последние 10 данного типа
        recent = [s for s in subs if s.get("lesson_type")==lesson_type][-10:]
        if not recent:
            return 0.5
        # EWMA точности
        alpha = 0.4
        ewma = 0.0
        streak = 0
        best_streak = 0
        for s in recent:
            sc = float(s.get("score", 0.0))
            ewma = alpha*sc + (1-alpha)*ewma
            if sc >= 0.6:
                streak += 1
                best_streak = max(best_streak, streak)
            else:
                streak = 0
        # бонус за стрик (мягкий)
        bonus = min(0.15, 0.03 * best_streak)
        return round(max(0.0, min(1.0, ewma + bonus)), 3)

    def _score_difficulty(self, difficulty: str) -> float:
        # вместо «дармового» бонуса — умеренная надбавка
        base = {"easy": 0.75, "medium": 0.85, "hard": 0.95}
        return base.get(difficulty, 0.85)

    def _score_spacing(self, subs: List[Dict[str,Any]]) -> float:
        if len(subs) < 3:
            return 0.5
        # берём последние N timestamps
        ts = []
        for s in subs[-10:]:
            t = s.get("created_at")
            if isinstance(t, str):
                try:
                    ts.append(datetime.fromisoformat(t.replace("Z","+00:00")))
                except Exception:
                    pass
            elif isinstance(t, (int, float)):
                ts.append(datetime.fromtimestamp(t))
        if len(ts) < 3:
            return 0.5
        ts.sort()
        intervals = [(ts[i]-ts[i-1]).total_seconds() for i in range(1,len(ts))]
        if not intervals:
            return 0.5
        avg = sum(intervals)/len(intervals)

        # динамический оптимум: чем выше среднее мастерство по истории, тем длиннее интервал
        # грубо оценим по последним 5 score
        last_scores = [float(s.get("score",0)) for s in subs[-5:]]
        avg_score = sum(last_scores)/len(last_scores) if last_scores else 0.6
        optimal = self.cfg.spacing_base_sec * (0.8 + 0.6*avg_score)  # примерно 0.8..1.4 * base

        # гладкая оценка вокруг оптимума
        # если avg == optimal → 1.0; в 2 раза чаще/реже → ~0.7
        ratio = avg / max(1.0, optimal)
        score = math.exp(-abs(math.log(ratio)))  # симметрично по отношению
        return round(0.5 + 0.5*score, 3)

    def _ema_alpha(self, n: int) -> float:
        # чем меньше данных, тем больше alpha (быстрее подстраивается)
        if n <= 0:
            return self.cfg.ema_alpha_max
        if n < self.cfg.ema_warmup_n:
            # линейная интерполяция от max к min
            f = n / float(self.cfg.ema_warmup_n)
            return self.cfg.ema_alpha_max*(1-f) + self.cfg.ema_alpha_min*f
        return self.cfg.ema_alpha_min

    def _compatible(self, base: str, underfed: str) -> bool:
        # базовая совместимость: assessment оставляем, если base=assessment
        if base == "assessment":
            return underfed in ("assessment","independent","guided")  # можно шаг назад при необходимости
        if base == "independent" and underfed == "concept":
            return False
        return True

# ---------- Удобные врапперы ----------

calc = MasteryCalculatorV2()

def calculate_lesson_mastery_v2(
    submissions_history: List[Dict[str,Any]],
    lesson_type: str,
    time_spent_sec: int,
    score: float,
    difficulty: str = "medium",
    student_speed_factor: float = 1.0
) -> Tuple[float, Dict[str,float]]:
    return calc.lesson_mastery(submissions_history, lesson_type, time_spent_sec, score, difficulty, student_speed_factor)

def update_learning_mastery_v2(
    current_mastery: Dict[str,Any],
    lesson_type: str,
    lesson_mastery_value: float,
    total_submissions: int
) -> Dict[str,Any]:
    return calc.update_mastery_ema(current_mastery, lesson_type, lesson_mastery_value, total_submissions)

def next_lesson_recommendation_v2(
    current_mastery: Dict[str,Any],
    lesson_policy_mix: Dict[str,float],
    counters: Dict[str,int],
    gates: Dict[str,int] = None
) -> Tuple[str,str]:
    return calc.recommend_next_lesson_type(current_mastery, lesson_policy_mix, counters, gates)


def get_mastery_description(mastery_score: float) -> str:
    """Получить текстовое описание уровня освоения."""
    if mastery_score >= 0.9:
        return "Мастер 🎖️"
    elif mastery_score >= 0.8:
        return "Эксперт 🏆"
    elif mastery_score >= 0.7:
        return "Продвинутый 🎯"
    elif mastery_score >= 0.6:
        return "Средний 📈"
    elif mastery_score >= 0.4:
        return "Новичок 🌱"
    else:
        return "Начинающий 👶"
