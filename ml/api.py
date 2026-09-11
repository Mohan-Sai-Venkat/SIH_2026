from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from prediction.ai_pipeline import analyze_task
from prediction.prioritize_tasks import prioritize_tasks
from optimizer.scheduler import generate_schedule


# --------------------------------------------------
# CREATE FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title="Railway AI Block Planning API",
    description="AI-powered maintenance prioritization and optimized block scheduling API",
    version="1.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5501",
        "http://localhost:5501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Railway AI Block Planning API is running successfully!"
    }


# --------------------------------------------------
# AI - PRIORITIZE ONE TASK
# --------------------------------------------------

@app.post("/ai/prioritize")
def prioritize(task: dict):

    result = analyze_task(task)

    result["task_id"] = task.get(
        "task_id",
        "UNKNOWN"
    )

    return result


# --------------------------------------------------
# AI - PRIORITIZE ALL TASKS
# --------------------------------------------------

@app.get("/ai/prioritize-all")
def prioritize_all():

    results = prioritize_tasks()

    return results.to_dict(
        orient="records"
    )


# --------------------------------------------------
# GENERATE FINAL SCHEDULE
# --------------------------------------------------

@app.post("/generate-schedule")
def generate_final_schedule():

    schedule = generate_schedule()

    if schedule is None:
        return {
            "success": False,
            "message": "No feasible schedule found."
        }

    return {
        "success": True,
        "message": "Schedule generated successfully!",
        "total_tasks": len(schedule),
        "schedule": schedule
    }


# --------------------------------------------------
# GET EXISTING SCHEDULE
# --------------------------------------------------

@app.get("/schedule")
def get_schedule():

    schedule = pd.read_csv(
        "data/final_schedule.csv"
    )

    return schedule.to_dict(
        orient="records"
    )