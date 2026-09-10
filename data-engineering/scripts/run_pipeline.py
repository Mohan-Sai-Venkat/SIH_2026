import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


SCRIPTS = [
    "transform.py",
    "clean.py",
    "validate.py",
    "validate_bdms.py",
    "train_summary.py",
    "integrate.py",
    "validate_integrated.py",
    "priority_features.py",
    "validate_priority.py",
    "validate_priority_levels.py",
    "create_ai_dataset.py",
    "validate_ai_dataset.py",
    "create_optimization_dataset.py",
    "validate_optimization_dataset.py",
    "create_available_windows.py",
    "validate_available_windows.py",
    "create_task_window_matches.py",
    "validate_task_window_matches.py",
    "calculate_matching_score.py",
    "validate_optimization_candidates.py",
    "create_optimization_input.py",
    "validate_optimization_input.py",
    "create_optimization_summary.py",
    "validate_optimization_summary.py",
    "create_optimization_handoff.py",
    "validate_optimization_handoff.py"
]


def run_script(script_name):

    script_path = BASE_DIR / script_name

    print()
    print("=" * 60)
    print(f"RUNNING: {script_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(script_path)]
    )

    if result.returncode != 0:
        print()
        print(f"PIPELINE FAILED AT: {script_name}")
        sys.exit(1)

    print(f"✓ {script_name} completed successfully.")


def main():

    print()
    print("=" * 60)
    print("AUTOMATIC BLOCK PLANNING")
    print("DATA ENGINEERING PIPELINE")
    print("=" * 60)

    for script in SCRIPTS:
        run_script(script)

    print()
    print("=" * 60)
    print("DATA ENGINEERING PIPELINE COMPLETED ✓")
    print("=" * 60)

    print()
    print("Final output:")
    print(
        "processed/optimization_handoff.csv"
    )


if __name__ == "__main__":
    main()