import pandas as pd
from pathlib import Path


def save_dataframe(df, folder, filename, keep_index=False):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    filepath = folder / f"{filename}.csv"
    df.to_csv(filepath, index=keep_index)

    print(f"Saved to {filepath}")


def summary_statistics(df):
    summary = df.describe().T
    summary.index.name = "Variable"
    return summary


def get_stats(folder):
    folder = Path(folder)
    task_name = folder.name

    for file in folder.glob("*.csv"):
        df = pd.read_csv(file)

        summary = summary_statistics(df)

        save_dataframe(
            summary,
            f"results/eda/{task_name}/statistics",
            f"{file.stem}_summary_statistics",
            keep_index=True
        )

def dataset_overview(folder, sampling_frequency=30):
    folder = Path(folder)
    task_name = folder.name

    rows = []

    for file in folder.glob("*.csv"):
        df = pd.read_csv(file)

        num_rows = df.shape[0]
        num_cols = df.shape[1]
        duration_seconds = num_rows / sampling_frequency

        rows.append({
            "file": file.name,
            "rows": num_rows,
            "columns": num_cols,
            "sampling_frequency_hz": sampling_frequency,
            "duration_seconds": duration_seconds
        })

    overview = pd.DataFrame(rows)

    save_dataframe(
        overview,
        f"results/eda/{task_name}/overview",
        f"{task_name}_dataset_overview"
    )

    return overview

def data_types_report(folder):
    folder = Path(folder)
    task_name = folder.name

    for file in folder.glob("*.csv"):
        df = pd.read_csv(file)

        report = pd.DataFrame({
            "column": df.columns,
            "dtype": df.dtypes.astype(str).values,
            "non_null_count": df.notna().sum().values,
            "memory_bytes": df.memory_usage(deep=True).values[1:]
        })

        save_dataframe(
            report,
            f"results/eda/{task_name}/data_types",
            f"{file.stem}_data_types"
        )

def missing_values_report(folder):
    folder = Path(folder)
    task_name = folder.name

    for file in folder.glob("*.csv"):
        df = pd.read_csv(file)

        report = pd.DataFrame({
            "column": df.columns,
            "missing_count": df.isna().sum().values,
            "missing_percent": (df.isna().mean() * 100).values
        })

        empty_rows = df.isna().all(axis=1).sum()

        report.loc[len(report)] = [
            "EMPTY_ROWS_TOTAL",
            empty_rows,
            ""
        ]

        save_dataframe(
            report,
            f"results/eda/{task_name}/missing_values",
            f"{file.stem}_missing_values"
        )

def distribution_report(folder):
    folder = Path(folder)
    task_name = folder.name

    for file in folder.glob("*.csv"):
        df = pd.read_csv(file)
        numeric_df = df.select_dtypes(include="number")

        report = pd.DataFrame({
            "mean": numeric_df.mean(),
            "median": numeric_df.median(),
            "std": numeric_df.std(),
            "skewness": numeric_df.skew(),
            "min": numeric_df.min(),
            "max": numeric_df.max()
        })

        report.index.name = "Variable"

        save_dataframe(
            report,
            f"results/eda/{task_name}/distribution",
            f"{file.stem}_distribution_report",
            keep_index=True
        )

def outlier_report(folder):
    folder = Path(folder)
    task_name = folder.name

    for file in folder.glob("*.csv"):
        df = pd.read_csv(file)
        numeric_df = df.select_dtypes(include="number")

        rows = []

        for col in numeric_df.columns:
            q1 = numeric_df[col].quantile(0.25)
            q3 = numeric_df[col].quantile(0.75)
            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = ((numeric_df[col] < lower_bound) | 
                        (numeric_df[col] > upper_bound)).sum()

            rows.append({
                "Variable": col,
                "Q1": q1,
                "Q3": q3,
                "IQR": iqr,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "outlier_count": outliers,
                "outlier_percent": outliers / len(numeric_df) * 100
            })

        report = pd.DataFrame(rows)

        save_dataframe(
            report,
            f"results/eda/{task_name}/outliers",
            f"{file.stem}_outlier_report"
        )



tasks = [
    "processed/knot_tying",
    "processed/suturing",
    "processed/needle_passing",
]

for folder in tasks:
    dataset_overview(folder)
    get_stats(folder)
    data_types_report(folder)
    missing_values_report(folder)
    distribution_report(folder)
    outlier_report(folder)