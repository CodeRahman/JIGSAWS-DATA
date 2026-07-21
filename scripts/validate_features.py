import pandas as pd
from pathlib import Path

features_df = pd.read_csv("features/features_dataset_completed.csv")

output_folder = Path("results/validation")
output_folder.mkdir(parents=True, exist_ok=True)

report_path = output_folder / "feature_dataset_validation.txt"

with open(report_path, "w") as report:

    report.write("=" * 70 + "\n")
    report.write("FEATURE DATASET VALIDATION REPORT\n")
    report.write("=" * 70 + "\n\n")

    # Dataset shape
    report.write("1. DATASET SHAPE\n")
    report.write("-" * 70 + "\n")
    report.write(f"Rows: {features_df.shape[0]}\n")
    report.write(f"Columns: {features_df.shape[1]}\n\n")

    # Missing values
    report.write("2. MISSING VALUES\n")
    report.write("-" * 70 + "\n")
    report.write(features_df.isna().sum().to_string())
    report.write("\n\n")

    # Duplicates
    report.write("3. DUPLICATE CHECKS\n")
    report.write("-" * 70 + "\n")
    report.write(
        f"Duplicate rows: {features_df.duplicated().sum()}\n"
    )
    report.write(
        f"Duplicate Trial IDs: "
        f"{features_df['Trial_ID'].duplicated().sum()}\n"
    )
    report.write(
        f"Duplicate Trial Names: "
        f"{features_df['Trial_Name'].duplicated().sum()}\n\n"
    )

    # Duration validation
    calculated_duration = features_df["Frames"] / 30

    duration_difference = (
        calculated_duration -
        features_df["Duration_Seconds"]
    ).abs()

    report.write("4. DURATION VALIDATION\n")
    report.write("-" * 70 + "\n")
    report.write(
        f"Maximum duration error: "
        f"{duration_difference.max()}\n\n"
    )

    # Idle ratio range
    report.write("5. IDLE RATIO RANGE\n")
    report.write("-" * 70 + "\n")

    idle_columns = [
        "Left_Idle_Ratio",
        "Right_Idle_Ratio"
    ]

    for column in idle_columns:
        report.write(f"{column}\n")
        report.write(
            f"Minimum: {features_df[column].min()}\n"
        )
        report.write(
            f"Maximum: {features_df[column].max()}\n\n"
        )

    # Idle time validation
    left_idle_exceeds_duration = (
        features_df["Left_Idle_Time"] >
        features_df["Duration_Seconds"]
    ).sum()

    right_idle_exceeds_duration = (
        features_df["Right_Idle_Time"] >
        features_df["Duration_Seconds"]
    ).sum()

    report.write("6. IDLE TIME VALIDATION\n")
    report.write("-" * 70 + "\n")
    report.write(
        f"Left idle time greater than duration: "
        f"{left_idle_exceeds_duration}\n"
    )
    report.write(
        f"Right idle time greater than duration: "
        f"{right_idle_exceeds_duration}\n\n"
    )

    # Negative feature values
    feature_columns = features_df.columns[15:]
    negative_counts = (features_df[feature_columns] < 0).sum()
    negative_results = negative_counts[negative_counts > 0]

    report.write("7. NEGATIVE FEATURE CHECK\n")
    report.write("-" * 70 + "\n")

    if negative_results.empty:
        report.write("No negative feature values found.\n\n")
    else:
        report.write(negative_results.to_string())
        report.write("\n\n")

    # Logical consistency
    checks = {
        "Left speed max < mean":
            features_df["Left_Max_Speed"] <
            features_df["Left_Mean_Speed"],

        "Right speed max < mean":
            features_df["Right_Max_Speed"] <
            features_df["Right_Mean_Speed"],

        "Left speed max < median":
            features_df["Left_Max_Speed"] <
            features_df["Left_Median_Speed"],

        "Right speed max < median":
            features_df["Right_Max_Speed"] <
            features_df["Right_Median_Speed"],

        "Left acceleration max < mean":
            features_df["Left_Max_Acceleration"] <
            features_df["Left_Mean_Acceleration"],

        "Right acceleration max < mean":
            features_df["Right_Max_Acceleration"] <
            features_df["Right_Mean_Acceleration"],

        "Left acceleration max < median":
            features_df["Left_Max_Acceleration"] <
            features_df["Left_Median_Acceleration"],

        "Right acceleration max < median":
            features_df["Right_Max_Acceleration"] <
            features_df["Right_Median_Acceleration"],

        "Left jerk max < mean":
            features_df["Left_Max_Jerk"] <
            features_df["Left_Mean_Jerk"],

        "Right jerk max < mean":
            features_df["Right_Max_Jerk"] <
            features_df["Right_Mean_Jerk"],

        "Left jerk max < median":
            features_df["Left_Max_Jerk"] <
            features_df["Left_Median_Jerk"],

        "Right jerk max < median":
            features_df["Right_Max_Jerk"] <
            features_df["Right_Median_Jerk"],
    }

    report.write("8. LOGICAL CONSISTENCY CHECKS\n")
    report.write("-" * 70 + "\n")

    for check_name, invalid_rows in checks.items():
        report.write(
            f"{check_name}: {invalid_rows.sum()}\n"
        )

    report.write("\n")

    # Idle ratio formula validation
    left_idle_ratio_recalculated = (
        features_df["Left_Idle_Time"] /
        features_df["Duration_Seconds"]
    )

    right_idle_ratio_recalculated = (
        features_df["Right_Idle_Time"] /
        features_df["Duration_Seconds"]
    )

    left_idle_error = (
        left_idle_ratio_recalculated -
        features_df["Left_Idle_Ratio"]
    ).abs()

    right_idle_error = (
        right_idle_ratio_recalculated -
        features_df["Right_Idle_Ratio"]
    ).abs()

    report.write("9. IDLE RATIO FORMULA VALIDATION\n")
    report.write("-" * 70 + "\n")
    report.write(
        f"Maximum left idle-ratio error: "
        f"{left_idle_error.max()}\n"
    )
    report.write(
        f"Maximum right idle-ratio error: "
        f"{right_idle_error.max()}\n\n"
    )

    # Overall result
    all_checks_passed = (
        features_df.shape[0] == 103
        and features_df.isna().sum().sum() == 0
        and features_df.duplicated().sum() == 0
        and features_df["Trial_ID"].duplicated().sum() == 0
        and features_df["Trial_Name"].duplicated().sum() == 0
        and left_idle_exceeds_duration == 0
        and right_idle_exceeds_duration == 0
        and negative_results.empty
        and all(
            invalid_rows.sum() == 0
            for invalid_rows in checks.values()
        )
    )

    report.write("=" * 70 + "\n")

    if all_checks_passed:
        report.write("OVERALL RESULT: VALIDATION PASSED\n")
    else:
        report.write("OVERALL RESULT: VALIDATION FAILED\n")

    report.write("=" * 70 + "\n")

print(f"Validation report saved to: {report_path}")