from prediction.prioritize_tasks import prioritize_tasks


def run_ai_module():

    # Generate prioritized maintenance tasks
    results = prioritize_tasks()

    # Save results for backend/optimizer
    results.to_csv(
        "data/prioritized_tasks.csv",
        index=False
    )

    return results


if __name__ == "__main__":

    results = run_ai_module()

    print()
    print("Railway AI Maintenance Priority Module")
    print("======================================")
    print("AI analysis completed successfully!")
    print("Total tasks analyzed:", len(results))

    print()
    print("Top 5 Priority Tasks")
    print("----------------------------")
    print(results.head(5).to_string(index=False))

    print()
    print("Output saved to:")
    print("data/prioritized_tasks.csv")