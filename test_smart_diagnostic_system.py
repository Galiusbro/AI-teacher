from smart_diagnostic_system import SmartDiagnosticSystem, DifficultyLevel


def test_level_progression():
    system = SmartDiagnosticSystem()
    profile = system.initialize_student_profile("s1", 10, ["Mathematics"])
    q1 = system.generate_next_question("s1", "Mathematics")
    assert q1.difficulty_level == DifficultyLevel.BEGINNER
    system.process_answer("s1", q1.id, {"answer": "ok"}, 5)
    assert profile.subjects["Mathematics"].current_level == DifficultyLevel.ELEMENTARY
    q2 = system.generate_next_question("s1", "Mathematics")
    system.process_answer("s1", q2.id, {"answer": q2.content["correct_answer"]}, 5)
    assert profile.subjects["Mathematics"].current_level == DifficultyLevel.INTERMEDIATE
    q3 = system.generate_next_question("s1", "Mathematics")
    system.process_answer("s1", q3.id, {"answer": "wrong"}, 5)
    assert profile.subjects["Mathematics"].current_level == DifficultyLevel.ELEMENTARY


def test_learning_plan_structure():
    system = SmartDiagnosticSystem()
    system.initialize_student_profile("s2", 11, ["Mathematics"])
    q1 = system.generate_next_question("s2", "Mathematics")
    system.process_answer("s2", q1.id, {"answer": "hello"}, 4)
    plan = system.generate_learning_plan("s2")
    assert "overall_level" in plan
    assert "subject_breakdown" in plan
    assert "Mathematics" in plan["subject_breakdown"]
