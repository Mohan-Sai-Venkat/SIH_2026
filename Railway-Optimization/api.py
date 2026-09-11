from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

from src.optimization.optimizer import optimize_with_cp_sat


app = FastAPI(
    title="Railway Automatic Block Planning API",
    version="1.0.0"
)

# Allow your Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")


@app.get("/")
def root():
    return {
        "service": "Railway Automatic Block Planning API",
        "status": "UP"
    }


@app.get("/health")
def health():
    return {
        "service": "Railway Optimization Engine",
        "status": "UP"
    }


@app.post("/api/optimize")
def optimize():
    try:
        candidate_file = os.path.join(
            INPUT_DIR,
            "task_window_matches.csv"
        )

        handoff_file = os.path.join(
            INPUT_DIR,
            "optimization_handoff.csv"
        )

        trains_file = os.path.join(
            INPUT_DIR,
            "trains.csv"
        )

        goods_file = os.path.join(
            INPUT_DIR,
            "goods_forecast.csv"
        )

        # Check input files
        required_files = [
            candidate_file,
            handoff_file,
            trains_file,
            goods_file
        ]

        for file_path in required_files:
            if not os.path.exists(file_path):
                raise HTTPException(
                    status_code=404,
                    detail=f"Input file not found: {file_path}"
                )

        # Load data
        candidate_windows = pd.read_csv(candidate_file)
        handoff = pd.read_csv(handoff_file)
        trains = pd.read_csv(trains_file)
        goods_forecast = pd.read_csv(goods_file)

        # Add optimization handoff information
        if not handoff.empty:
            candidate_windows = candidate_windows.merge(
                handoff[
                    [
                        "task_id",
                        "matching_score",
                        "optimization_rank"
                    ]
                ],
                on="task_id",
                how="left"
            )

        # Run optimizer
        result = optimize_with_cp_sat(
            candidate_windows=candidate_windows,
            trains=trains,
            goods_forecast=goods_forecast,
            goods_probability_threshold=0.70
        )

        # Create output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Extract schedule
        if isinstance(result, tuple):
            optimized_schedule = result[0]
            unscheduled_tasks = (
                result[1] if len(result) > 1 else pd.DataFrame()
            )
        else:
            optimized_schedule = result
            unscheduled_tasks = pd.DataFrame()

        # Convert DataFrames to JSON
        if isinstance(optimized_schedule, pd.DataFrame):
            schedule_data = optimized_schedule.fillna("").to_dict(
                orient="records"
            )
        else:
            schedule_data = []

        if isinstance(unscheduled_tasks, pd.DataFrame):
            unscheduled_data = unscheduled_tasks.fillna("").to_dict(
                orient="records"
            )
        else:
            unscheduled_data = []

        return {
            "status": "success",
            "message": "Optimization completed successfully",
            "scheduled_tasks": len(schedule_data),
            "unscheduled_tasks": len(unscheduled_data),
            "schedule": schedule_data,
            "unscheduled": unscheduled_data
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )