import json


def create_ai_result(task_id, analysis_result):

    result = {
        "task_id": task_id,
        "priority_level": analysis_result["priority_level"],
        "priority_score": analysis_result["priority_score"],
        "risk_score": analysis_result["risk_score"],
        "explanation": analysis_result["explanation"]
    }

    return result


if __name__ == "__main__":

    sample_result = {
        "priority_level": "Critical",
        "priority_score": 0.94,
        "risk_score": 0.97,
        "explanation": [
            "High defect severity",
            "High asset criticality",
            "High safety impact",
            "Maintenance is significantly overdue",
            "High train traffic frequency"
        ]
    }

    result = create_ai_result("T001", sample_result)

    print("\nAI Result")
    print("============================")
    print(json.dumps(result, indent=4))