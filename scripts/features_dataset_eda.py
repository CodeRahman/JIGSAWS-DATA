import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. FILE PATHS
# ============================================================

DATASET_PATH = Path("features/features_dataset_completed.csv")

RESULTS_FOLDER = Path("results/eda")

REPORTS_FOLDER = RESULTS_FOLDER / "reports"
HISTOGRAM_FOLDER = RESULTS_FOLDER / "histograms"
BOXPLOT_FOLDER = RESULTS_FOLDER / "boxplots"
SKILL_BOXPLOT_FOLDER = BOXPLOT_FOLDER / "by_skill"
TASK_BOXPLOT_FOLDER = BOXPLOT_FOLDER / "by_task"
SCATTERPLOT_FOLDER = RESULTS_FOLDER / "scatterplots_grs"
CORRELATION_FOLDER = RESULTS_FOLDER / "correlation"

OUTPUT_FOLDERS = [
    RESULTS_FOLDER,
    REPORTS_FOLDER,
    HISTOGRAM_FOLDER,
    BOXPLOT_FOLDER,
    SKILL_BOXPLOT_FOLDER,
    TASK_BOXPLOT_FOLDER,
    SCATTERPLOT_FOLDER,
    CORRELATION_FOLDER,
]

for folder in OUTPUT_FOLDERS:
    folder.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATASET
# ============================================================

features_df = pd.read_csv(DATASET_PATH)


# ============================================================
# 3. DEFINE DATASET COLUMNS
# ============================================================

metadata_columns = [
    "Trial_ID",
    "Trial_Name",
    "Task",
    "Subject",
    "Repetition",
    "Frames",
    "Duration_Seconds",
    "Self_Proclaimed_Skill",
]

target_columns = [
    "GRS_Total",
    "GRS_Tissue_Respect",
    "GRS_Handling",
    "GRS_Time_Motion",
    "GRS_Flow",
    "GRS_Performance",
    "GRS_Quality",
]

feature_columns = [
    "Left_Mean_Speed",
    "Left_Median_Speed",
    "Left_Max_Speed",
    "Left_Speed_Std",
    "Right_Mean_Speed",
    "Right_Median_Speed",
    "Right_Max_Speed",
    "Right_Speed_Std",

    "Left_Idle_Ratio",
    "Left_Idle_Time",
    "Right_Idle_Ratio",
    "Right_Idle_Time",

    "Left_Mean_Acceleration",
    "Left_Median_Acceleration",
    "Left_Max_Acceleration",
    "Left_Acceleration_Std",
    "Right_Mean_Acceleration",
    "Right_Median_Acceleration",
    "Right_Max_Acceleration",
    "Right_Acceleration_Std",

    "Left_Mean_Jerk",
    "Left_Median_Jerk",
    "Left_Max_Jerk",
    "Left_Jerk_Std",
    "Right_Mean_Jerk",
    "Right_Median_Jerk",
    "Right_Max_Jerk",
    "Right_Jerk_Std",
]

# This order makes plots appear as Novice, Intermediate, Expert.
skill_order = ["N", "I", "E"]

skill_labels = {
    "N": "Novice",
    "I": "Intermediate",
    "E": "Expert",
}

task_order = [
    "Knot Tying",
    "Needle Passing",
    "Suturing",
]


# ============================================================
# 4. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = (
    metadata_columns
    + target_columns
    + feature_columns
)

missing_columns = [
    column
    for column in required_columns
    if column not in features_df.columns
]

if missing_columns:
    raise ValueError(
        "The following required columns are missing:\n"
        + "\n".join(missing_columns)
    )


# ============================================================
# 5. DESCRIPTIVE STATISTICS
# ============================================================

numeric_analysis_columns = [
    "Frames",
    "Duration_Seconds",
    *target_columns,
    *feature_columns,
]

descriptive_statistics = (
    features_df[numeric_analysis_columns]
    .describe()
    .transpose()
)

descriptive_statistics["Missing"] = (
    features_df[numeric_analysis_columns]
    .isna()
    .sum()
)

descriptive_statistics["Skewness"] = (
    features_df[numeric_analysis_columns]
    .skew()
)

descriptive_statistics.to_csv(
    REPORTS_FOLDER / "descriptive_statistics.csv"
)


# Feature-only descriptive statistics
feature_descriptive_statistics = (
    features_df[feature_columns]
    .describe()
    .transpose()
)

feature_descriptive_statistics["Missing"] = (
    features_df[feature_columns]
    .isna()
    .sum()
)

feature_descriptive_statistics["Skewness"] = (
    features_df[feature_columns]
    .skew()
)

feature_descriptive_statistics.to_csv(
    REPORTS_FOLDER / "feature_descriptive_statistics.csv"
)


# ============================================================
# 6. DATASET COMPOSITION TABLES
# ============================================================

task_counts = (
    features_df["Task"]
    .value_counts()
    .reindex(task_order)
    .rename_axis("Task")
    .reset_index(name="Trial_Count")
)

task_counts.to_csv(
    REPORTS_FOLDER / "trial_counts_by_task.csv",
    index=False,
)


skill_counts = (
    features_df["Self_Proclaimed_Skill"]
    .value_counts()
    .reindex(skill_order)
    .rename_axis("Skill_Code")
    .reset_index(name="Trial_Count")
)

skill_counts["Skill_Level"] = (
    skill_counts["Skill_Code"]
    .map(skill_labels)
)

skill_counts.to_csv(
    REPORTS_FOLDER / "trial_counts_by_skill.csv",
    index=False,
)


task_skill_counts = pd.crosstab(
    features_df["Task"],
    features_df["Self_Proclaimed_Skill"],
)

task_skill_counts = task_skill_counts.reindex(
    index=task_order,
    columns=skill_order,
    fill_value=0,
)

task_skill_counts = task_skill_counts.rename(
    columns=skill_labels
)

task_skill_counts.to_csv(
    REPORTS_FOLDER / "trial_counts_by_task_and_skill.csv"
)


subject_counts = (
    features_df["Subject"]
    .value_counts()
    .sort_index()
    .rename_axis("Subject")
    .reset_index(name="Trial_Count")
)

subject_counts.to_csv(
    REPORTS_FOLDER / "trial_counts_by_subject.csv",
    index=False,
)


# ============================================================
# 7. FEATURE STATISTICS BY SKILL
# ============================================================

feature_statistics_by_skill = (
    features_df
    .groupby("Self_Proclaimed_Skill")[feature_columns]
    .agg(["count", "mean", "median", "std", "min", "max"])
)

feature_statistics_by_skill = (
    feature_statistics_by_skill
    .reindex(skill_order)
)

feature_statistics_by_skill.to_csv(
    REPORTS_FOLDER / "feature_statistics_by_skill.csv"
)


# ============================================================
# 8. FEATURE STATISTICS BY TASK
# ============================================================

feature_statistics_by_task = (
    features_df
    .groupby("Task")[feature_columns]
    .agg(["count", "mean", "median", "std", "min", "max"])
)

feature_statistics_by_task = (
    feature_statistics_by_task
    .reindex(task_order)
)

feature_statistics_by_task.to_csv(
    REPORTS_FOLDER / "feature_statistics_by_task.csv"
)


# ============================================================
# 9. OUTLIER DETECTION USING THE IQR RULE
# ============================================================

outlier_rows = []

for column in feature_columns:
    q1 = features_df[column].quantile(0.25)
    q3 = features_df[column].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    outlier_mask = (
        (features_df[column] < lower_bound)
        | (features_df[column] > upper_bound)
    )

    outlier_trials = features_df.loc[
        outlier_mask,
        [
            "Trial_ID",
            "Trial_Name",
            "Task",
            "Subject",
            "Self_Proclaimed_Skill",
            "GRS_Total",
            column,
        ],
    ]

    for _, row in outlier_trials.iterrows():
        outlier_rows.append(
            {
                "Feature": column,
                "Trial_ID": row["Trial_ID"],
                "Trial_Name": row["Trial_Name"],
                "Task": row["Task"],
                "Subject": row["Subject"],
                "Self_Proclaimed_Skill":
                    row["Self_Proclaimed_Skill"],
                "GRS_Total": row["GRS_Total"],
                "Feature_Value": row[column],
                "Lower_Bound": lower_bound,
                "Upper_Bound": upper_bound,
            }
        )

outlier_report = pd.DataFrame(outlier_rows)

outlier_report.to_csv(
    REPORTS_FOLDER / "feature_outliers_iqr.csv",
    index=False,
)


if not outlier_report.empty:
    outlier_counts = (
        outlier_report["Feature"]
        .value_counts()
        .rename_axis("Feature")
        .reset_index(name="Outlier_Count")
    )
else:
    outlier_counts = pd.DataFrame(
        columns=["Feature", "Outlier_Count"]
    )

outlier_counts.to_csv(
    REPORTS_FOLDER / "outlier_counts_by_feature.csv",
    index=False,
)


# ============================================================
# 10. SKEWNESS REPORT
# ============================================================

skewness_report = (
    features_df[feature_columns]
    .skew()
    .sort_values(
        key=lambda series: series.abs(),
        ascending=False,
    )
    .rename("Skewness")
    .reset_index()
    .rename(columns={"index": "Feature"})
)

skewness_report["Absolute_Skewness"] = (
    skewness_report["Skewness"].abs()
)

skewness_report["Interpretation"] = np.select(
    [
        skewness_report["Absolute_Skewness"] < 0.5,
        skewness_report["Absolute_Skewness"] < 1.0,
    ],
    [
        "Approximately symmetric",
        "Moderately skewed",
    ],
    default="Highly skewed",
)

skewness_report.to_csv(
    REPORTS_FOLDER / "feature_skewness.csv",
    index=False,
)


# ============================================================
# 11. HISTOGRAMS
# ============================================================

for column in feature_columns:
    figure, axis = plt.subplots(figsize=(8, 5))

    axis.hist(
        features_df[column].dropna(),
        bins=15,
        edgecolor="black",
    )

    axis.set_title(
        f"Distribution of {column.replace('_', ' ')}"
    )
    axis.set_xlabel(column.replace("_", " "))
    axis.set_ylabel("Number of Trials")
    axis.grid(axis="y", alpha=0.3)

    figure.tight_layout()

    figure.savefig(
        HISTOGRAM_FOLDER / f"{column}_histogram.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)


# ============================================================
# 12. OVERALL BOXPLOTS
# ============================================================

for column in feature_columns:
    figure, axis = plt.subplots(figsize=(7, 5))

    axis.boxplot(
        features_df[column].dropna(),
        vert=True,
    )

    axis.set_title(
        f"Overall Boxplot of {column.replace('_', ' ')}"
    )
    axis.set_ylabel(column.replace("_", " "))
    axis.set_xticks([1])
    axis.set_xticklabels(["All Trials"])
    axis.grid(axis="y", alpha=0.3)

    figure.tight_layout()

    figure.savefig(
        BOXPLOT_FOLDER / f"{column}_overall_boxplot.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)


# ============================================================
# 13. BOXPLOTS BY SELF-PROCLAIMED SKILL
# ============================================================

for column in feature_columns:
    skill_data = []

    for skill_code in skill_order:
        values = features_df.loc[
            features_df["Self_Proclaimed_Skill"]
            == skill_code,
            column,
        ].dropna()

        skill_data.append(values)

    figure, axis = plt.subplots(figsize=(8, 5))

    axis.boxplot(
        skill_data,
        tick_labels=[
            skill_labels[code]
            for code in skill_order
        ],
    )

    axis.set_title(
        f"{column.replace('_', ' ')} by Skill Level"
    )
    axis.set_xlabel("Self-Proclaimed Skill Level")
    axis.set_ylabel(column.replace("_", " "))
    axis.grid(axis="y", alpha=0.3)

    figure.tight_layout()

    figure.savefig(
        SKILL_BOXPLOT_FOLDER
        / f"{column}_by_skill.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)


# ============================================================
# 14. BOXPLOTS BY TASK
# ============================================================

for column in feature_columns:
    task_data = []

    for task in task_order:
        values = features_df.loc[
            features_df["Task"] == task,
            column,
        ].dropna()

        task_data.append(values)

    figure, axis = plt.subplots(figsize=(9, 5))

    axis.boxplot(
        task_data,
        tick_labels=task_order,
    )

    axis.set_title(
        f"{column.replace('_', ' ')} by Task"
    )
    axis.set_xlabel("Task")
    axis.set_ylabel(column.replace("_", " "))
    axis.grid(axis="y", alpha=0.3)

    figure.tight_layout()

    figure.savefig(
        TASK_BOXPLOT_FOLDER
        / f"{column}_by_task.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)


# ============================================================
# 15. SCATTERPLOTS AGAINST GRS TOTAL
# ============================================================

for column in feature_columns:
    x = features_df[column]
    y = features_df["GRS_Total"]

    figure, axis = plt.subplots(figsize=(8, 5))

    axis.scatter(
        x,
        y,
        alpha=0.75,
    )

    # Add a simple linear trend line.
    valid_mask = x.notna() & y.notna()

    if valid_mask.sum() >= 2:
        slope, intercept = np.polyfit(
            x[valid_mask],
            y[valid_mask],
            1,
        )

        x_line = np.linspace(
            x[valid_mask].min(),
            x[valid_mask].max(),
            100,
        )

        y_line = (
            slope * x_line
            + intercept
        )

        axis.plot(
            x_line,
            y_line,
            linewidth=2,
        )

    correlation = features_df[
        [column, "GRS_Total"]
    ].corr().iloc[0, 1]

    axis.set_title(
        f"{column.replace('_', ' ')} vs GRS Total\n"
        f"Pearson r = {correlation:.3f}"
    )

    axis.set_xlabel(column.replace("_", " "))
    axis.set_ylabel("GRS Total")
    axis.grid(alpha=0.3)

    figure.tight_layout()

    figure.savefig(
        SCATTERPLOT_FOLDER
        / f"{column}_vs_GRS_Total.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(figure)


# ============================================================
# 16. CORRELATION MATRIX
# ============================================================

correlation_columns = [
    "GRS_Total",
    *feature_columns,
]

correlation_matrix = (
    features_df[correlation_columns]
    .corr(method="pearson")
)

correlation_matrix.to_csv(
    CORRELATION_FOLDER
    / "feature_correlation_matrix.csv"
)


# ============================================================
# 17. FEATURE CORRELATION WITH GRS TOTAL
# ============================================================

grs_correlations = (
    correlation_matrix["GRS_Total"]
    .drop("GRS_Total")
    .sort_values(
        key=lambda series: series.abs(),
        ascending=False,
    )
    .rename("Pearson_Correlation")
    .reset_index()
    .rename(columns={"index": "Feature"})
)

grs_correlations["Absolute_Correlation"] = (
    grs_correlations[
        "Pearson_Correlation"
    ].abs()
)

grs_correlations["Direction"] = np.where(
    grs_correlations["Pearson_Correlation"] >= 0,
    "Positive",
    "Negative",
)

grs_correlations.to_csv(
    CORRELATION_FOLDER
    / "feature_correlations_with_GRS_Total.csv",
    index=False,
)


# ============================================================
# 18. CORRELATION HEATMAP
# ============================================================

figure, axis = plt.subplots(figsize=(18, 16))

heatmap = axis.imshow(
    correlation_matrix,
    aspect="auto",
    vmin=-1,
    vmax=1,
)

axis.set_xticks(
    np.arange(len(correlation_columns))
)

axis.set_yticks(
    np.arange(len(correlation_columns))
)

axis.set_xticklabels(
    [
        column.replace("_", " ")
        for column in correlation_columns
    ],
    rotation=90,
    fontsize=7,
)

axis.set_yticklabels(
    [
        column.replace("_", " ")
        for column in correlation_columns
    ],
    fontsize=7,
)

axis.set_title(
    "Feature Correlation Matrix"
)

colorbar = figure.colorbar(
    heatmap,
    ax=axis,
    fraction=0.046,
    pad=0.04,
)

colorbar.set_label(
    "Pearson Correlation"
)

figure.tight_layout()

figure.savefig(
    CORRELATION_FOLDER
    / "feature_correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close(figure)


# ============================================================
# 19. GRS CORRELATION BAR CHART
# ============================================================

plot_correlations = (
    grs_correlations
    .sort_values("Pearson_Correlation")
)

figure, axis = plt.subplots(figsize=(10, 10))

axis.barh(
    plot_correlations["Feature"],
    plot_correlations["Pearson_Correlation"],
)

axis.axvline(
    0,
    linewidth=1,
)

axis.set_title(
    "Feature Correlations with GRS Total"
)

axis.set_xlabel(
    "Pearson Correlation with GRS Total"
)

axis.set_ylabel(
    "Feature"
)

axis.grid(
    axis="x",
    alpha=0.3,
)

figure.tight_layout()

figure.savefig(
    CORRELATION_FOLDER
    / "feature_correlations_with_GRS_Total.png",
    dpi=300,
    bbox_inches="tight",
)

plt.close(figure)


# ============================================================
# 20. TASK-SPECIFIC FEATURE–GRS CORRELATIONS
# ============================================================

task_correlation_tables = []

for task in task_order:
    task_df = features_df[
        features_df["Task"] == task
    ]

    task_correlations = (
        task_df[
            ["GRS_Total", *feature_columns]
        ]
        .corr()["GRS_Total"]
        .drop("GRS_Total")
        .sort_values(
            key=lambda series: series.abs(),
            ascending=False,
        )
        .rename("Pearson_Correlation")
        .reset_index()
        .rename(columns={"index": "Feature"})
    )

    task_correlations.insert(
        0,
        "Task",
        task,
    )

    task_correlation_tables.append(
        task_correlations
    )

    safe_task_name = (
        task.lower()
        .replace(" ", "_")
    )

    task_correlations.to_csv(
        CORRELATION_FOLDER
        / f"{safe_task_name}_feature_correlations_with_GRS.csv",
        index=False,
    )

all_task_correlations = pd.concat(
    task_correlation_tables,
    ignore_index=True,
)

all_task_correlations.to_csv(
    CORRELATION_FOLDER
    / "all_task_specific_feature_correlations.csv",
    index=False,
)


# ============================================================
# 21. MAIN TEXT REPORT
# ============================================================

report_path = (
    REPORTS_FOLDER
    / "feature_dataset_eda_report.txt"
)

with open(
    report_path,
    "w",
    encoding="utf-8",
) as report:

    report.write("=" * 80 + "\n")
    report.write(
        "FEATURE DATASET EXPLORATORY DATA ANALYSIS REPORT\n"
    )
    report.write("=" * 80 + "\n\n")

    report.write("1. DATASET OVERVIEW\n")
    report.write("-" * 80 + "\n")
    report.write(
        f"Rows: {features_df.shape[0]}\n"
    )
    report.write(
        f"Columns: {features_df.shape[1]}\n"
    )
    report.write(
        f"Number of extracted features: "
        f"{len(feature_columns)}\n"
    )
    report.write(
        f"Number of tasks: "
        f"{features_df['Task'].nunique()}\n"
    )
    report.write(
        f"Number of subjects: "
        f"{features_df['Subject'].nunique()}\n\n"
    )

    report.write("2. TRIAL COUNTS BY TASK\n")
    report.write("-" * 80 + "\n")
    report.write(
        task_counts.to_string(index=False)
    )
    report.write("\n\n")

    report.write(
        "3. TRIAL COUNTS BY SELF-PROCLAIMED SKILL\n"
    )
    report.write("-" * 80 + "\n")
    report.write(
        skill_counts.to_string(index=False)
    )
    report.write("\n\n")

    report.write(
        "4. TRIAL COUNTS BY TASK AND SKILL\n"
    )
    report.write("-" * 80 + "\n")
    report.write(
        task_skill_counts.to_string()
    )
    report.write("\n\n")

    report.write("5. GRS TOTAL SUMMARY\n")
    report.write("-" * 80 + "\n")
    report.write(
        features_df["GRS_Total"]
        .describe()
        .to_string()
    )
    report.write("\n\n")

    report.write(
        "6. TOP POSITIVE CORRELATIONS WITH GRS TOTAL\n"
    )
    report.write("-" * 80 + "\n")

    positive_correlations = (
        grs_correlations[
            grs_correlations[
                "Pearson_Correlation"
            ] > 0
        ]
        .sort_values(
            "Pearson_Correlation",
            ascending=False,
        )
        .head(10)
    )

    report.write(
        positive_correlations.to_string(
            index=False
        )
    )
    report.write("\n\n")

    report.write(
        "7. TOP NEGATIVE CORRELATIONS WITH GRS TOTAL\n"
    )
    report.write("-" * 80 + "\n")

    negative_correlations = (
        grs_correlations[
            grs_correlations[
                "Pearson_Correlation"
            ] < 0
        ]
        .sort_values(
            "Pearson_Correlation"
        )
        .head(10)
    )

    report.write(
        negative_correlations.to_string(
            index=False
        )
    )
    report.write("\n\n")

    report.write("8. MOST SKEWED FEATURES\n")
    report.write("-" * 80 + "\n")
    report.write(
        skewness_report
        .head(10)
        .to_string(index=False)
    )
    report.write("\n\n")

    report.write("9. OUTLIER SUMMARY\n")
    report.write("-" * 80 + "\n")
    report.write(
        f"Total IQR-identified outlier observations: "
        f"{len(outlier_report)}\n"
    )

    report.write(
        f"Number of features containing at least "
        f"one outlier: {len(outlier_counts)}\n\n"
    )

    if not outlier_counts.empty:
        report.write(
            outlier_counts
            .head(15)
            .to_string(index=False)
        )
        report.write("\n\n")
    else:
        report.write(
            "No IQR outliers were identified.\n\n"
        )

    report.write("10. GENERATED OUTPUTS\n")
    report.write("-" * 80 + "\n")
    report.write(
        f"Histogram count: {len(feature_columns)}\n"
    )
    report.write(
        f"Overall boxplot count: {len(feature_columns)}\n"
    )
    report.write(
        f"Skill boxplot count: {len(feature_columns)}\n"
    )
    report.write(
        f"Task boxplot count: {len(feature_columns)}\n"
    )
    report.write(
        f"GRS scatterplot count: {len(feature_columns)}\n"
    )
    report.write(
        "Correlation heatmaps: 1\n"
    )
    report.write(
        "Correlation ranking charts: 1\n\n"
    )

    report.write("=" * 80 + "\n")
    report.write(
        "EDA GENERATION COMPLETED SUCCESSFULLY\n"
    )
    report.write("=" * 80 + "\n")


# ============================================================
# 22. TERMINAL SUMMARY
# ============================================================

print("=" * 70)
print("EDA COMPLETED")
print("=" * 70)

print(f"Dataset rows: {features_df.shape[0]}")
print(f"Dataset columns: {features_df.shape[1]}")
print(f"Feature columns analyzed: {len(feature_columns)}")

print(
    f"Histograms created: "
    f"{len(feature_columns)}"
)

print(
    f"Overall boxplots created: "
    f"{len(feature_columns)}"
)

print(
    f"Skill boxplots created: "
    f"{len(feature_columns)}"
)

print(
    f"Task boxplots created: "
    f"{len(feature_columns)}"
)

print(
    f"GRS scatterplots created: "
    f"{len(feature_columns)}"
)

print(
    f"EDA report saved to: "
    f"{report_path}"
)

print(
    f"All EDA results saved under: "
    f"{RESULTS_FOLDER}"
)