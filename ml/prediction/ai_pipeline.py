from prediction.predict import predict_priority
from prediction.risk_score import calculate_risk_score
from explanation.explain import generate_explanation


def analyze_task(task):

    # ========================================================
    # 1. AI PRIORITY PREDICTION
    # ========================================================

    priority, priority_score = predict_priority(task.copy())


    # ========================================================
    # 2. RISK SCORE
    # ========================================================

    risk_score = calculate_risk_score(
        task["severity_score"],
        task.get("urgency_score", 0),
        task.get("train_activity_score", 0),
        task["days_to_due"],
        task.get("high_priority_train_score", 0)
    )


    # ========================================================
    # 3. EXPLANATION
    # ========================================================

    explanation = generate_explanation(task)


    # ========================================================
    # 4. FINAL AI RESULT
    # ========================================================

    return {
        "priority_level": priority,
        "priority_score": round(priority_score, 2),
        "risk_score": risk_score,
        "explanation": explanation
    }