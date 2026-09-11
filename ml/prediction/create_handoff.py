import pandas as pd


AI_FILE = "data/prioritized_tasks.csv"
MAINTENANCE_FILE = "data/integrated_maintenance.csv"
OUTPUT_FILE = "data/ai_optimization_handoff.csv"


# Load AI results
ai_data = pd.read_csv(AI_FILE)

# Load integrated maintenance data
maintenance_data = pd.read_csv(MAINTENANCE_FILE)


# Select information required by optimization
maintenance_columns = [
    "task_id",
    "department",
    "section_id",
    "maintenance_type",
    "maintenance_duration",
    "status",
    "requested_date",
    "requested_start",
    "requested_end",
    "train_count",
    "high_priority_train_count",
    "start_location",
    "end_location"
]

maintenance_data = maintenance_data[
    maintenance_columns
]


# Combine AI output with maintenance information
handoff = maintenance_data.merge(
    ai_data[
        [
            "rank",
            "task_id",
            "priority_level",
            "priority_score"
        ]
    ],
    on="task_id",
    how="inner"
)


# Sort according to AI priority
handoff = handoff.sort_values(
    by="priority_score",
    ascending=False
).reset_index(drop=True)


# Save final handoff
handoff.to_csv(
    OUTPUT_FILE,
    index=False
)


print("=" * 70)
print("AI → OPTIMIZATION HANDOFF")
print("=" * 70)

print()
print("AI tasks:", len(ai_data))
print("Handoff tasks:", len(handoff))

print()
print("Handoff columns:")
print(handoff.columns.tolist())

print()
print("Top 10 priority tasks:")
print(
    handoff.head(10).to_string(index=False)
)

print()
print("Handoff file created successfully!")
print("File:", OUTPUT_FILE)