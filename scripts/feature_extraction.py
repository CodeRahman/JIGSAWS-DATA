import pandas as pd
import numpy as np
from pathlib import Path


features_df = pd.read_csv("features/features_dataset.csv")

"""
print(features_df.head())
print(features_df.tail())
print(features_df.shape)
print(features_df.columns)
"""

def extract_speed_features(df, side):
    if side == "left":
        x_arr = df["MASTER_LEFT_LIN_VEL_X"]
        y_arr = df["MASTER_LEFT_LIN_VEL_Y"]
        z_arr = df["MASTER_LEFT_LIN_VEL_Z"]
    elif side == "right":
        x_arr = df["MASTER_RIGHT_LIN_VEL_X"]
        y_arr = df["MASTER_RIGHT_LIN_VEL_Y"]
        z_arr = df["MASTER_RIGHT_LIN_VEL_Z"] 
    speed_array = np.sqrt((x_arr ** 2 ) + (y_arr ** 2) + (z_arr ** 2))
    mean_speed = speed_array.mean()
    median_speed =  speed_array.median()
    max_speed = speed_array.max()
    std_speed = speed_array.std()

    speed_dict = {"Mean": mean_speed, 
                  "Median": median_speed, 
                  "Max": max_speed, 
                  "Std": std_speed}
    return speed_dict, speed_array

def extract_idle_features(speed_array, frames):
    idle_count = 0
    for v in speed_array:
        if v <= 0.001:
            idle_count+= 1
    
    idle_time = idle_count/30 #sampling rate = 30Hz
    idle_ratio = idle_count/frames

    idle_dict = {"Idle_Time": idle_time,
                 "Idle_Ratio": idle_ratio}

    return idle_dict

def extract_acceleration_features(speed_array):
    acceleration_arr = []

    for i in range(1, len(speed_array)):
        a = (speed_array[i] - speed_array[i - 1]) * 30
        acceleration_arr.append(a)

    acceleration_array = np.array(acceleration_arr)

    acceleration_magnitude = np.abs(acceleration_array)

    mean_acceleration = acceleration_magnitude.mean()
    median_acceleration = np.median(acceleration_magnitude)
    max_acceleration = acceleration_magnitude.max()
    std_acceleration = acceleration_magnitude.std()

    acceleration_dict = {
        "Mean": mean_acceleration,
        "Median": median_acceleration,
        "Max": max_acceleration,
        "Std": std_acceleration
    }

    return acceleration_dict, acceleration_array

def extract_jerk_features(acceleration_array):
    jerk_arr = []

    for i in range(1, len(acceleration_array)):
        j = (acceleration_array[i] - acceleration_array[i - 1]) * 30
        jerk_arr.append(j)

    jerk_array = np.array(jerk_arr)

    jerk_magnitude = np.abs(jerk_array)

    mean_jerk_mag = jerk_magnitude.mean()
    median_jerk_mag = np.median(jerk_magnitude)
    max_jerk_mag = jerk_magnitude.max()
    std_jerk_mag = jerk_magnitude.std()

    jerk_dict = {
        "Mean": mean_jerk_mag,
        "Median": median_jerk_mag,
        "Max": max_jerk_mag,
        "Std": std_jerk_mag
    }

    return jerk_dict, jerk_array

def calc_speed_anals(speed_dict, speed_array):
    print(f"5th percentile Speed is {speed_array.quantile(0.05)}")
    print(f"10th percentile Speed is {speed_array.quantile(0.1)}")
    print(f"Median Speed is {speed_dict["Median"]}")
    print(f"Max Speed is {speed_dict["Max"]}")
    


def extract_features(file):
    trial_df = pd.read_csv(file)

    frames = len(trial_df)
    duration_seconds = frames / 30

    # Left-hand features
    left_speed_dict, left_speed_array = extract_speed_features(
        trial_df, "left"
    )

    left_idle_dict = extract_idle_features(
        left_speed_array, frames
    )

    left_acceleration_dict, left_acceleration_array = (
        extract_acceleration_features(left_speed_array)
    )

    left_jerk_dict, left_jerk_array = extract_jerk_features(
        left_acceleration_array
    )

    # Right-hand features
    right_speed_dict, right_speed_array = extract_speed_features(
        trial_df, "right"
    )

    right_idle_dict = extract_idle_features(
        right_speed_array, frames
    )

    right_acceleration_dict, right_acceleration_array = (
        extract_acceleration_features(right_speed_array)
    )

    right_jerk_dict, right_jerk_array = extract_jerk_features(
        right_acceleration_array
    )

    # Return one dictionary containing all calculated values
    feature_values = {
        "Frames": frames,
        "Duration_Seconds": duration_seconds,

        "Left_Mean_Speed": left_speed_dict["Mean"],
        "Left_Median_Speed": left_speed_dict["Median"],
        "Left_Max_Speed": left_speed_dict["Max"],
        "Left_Speed_Std": left_speed_dict["Std"],

        "Right_Mean_Speed": right_speed_dict["Mean"],
        "Right_Median_Speed": right_speed_dict["Median"],
        "Right_Max_Speed": right_speed_dict["Max"],
        "Right_Speed_Std": right_speed_dict["Std"],

        "Left_Idle_Ratio": left_idle_dict["Idle_Ratio"],
        "Left_Idle_Time": left_idle_dict["Idle_Time"],
        "Right_Idle_Ratio": right_idle_dict["Idle_Ratio"],
        "Right_Idle_Time": right_idle_dict["Idle_Time"],

        "Left_Mean_Acceleration": left_acceleration_dict["Mean"],
        "Left_Median_Acceleration": left_acceleration_dict["Median"],
        "Left_Max_Acceleration": left_acceleration_dict["Max"],
        "Left_Acceleration_Std": left_acceleration_dict["Std"],

        "Right_Mean_Acceleration": right_acceleration_dict["Mean"],
        "Right_Median_Acceleration": right_acceleration_dict["Median"],
        "Right_Max_Acceleration": right_acceleration_dict["Max"],
        "Right_Acceleration_Std": right_acceleration_dict["Std"],

        "Left_Mean_Jerk": left_jerk_dict["Mean"],
        "Left_Median_Jerk": left_jerk_dict["Median"],
        "Left_Max_Jerk": left_jerk_dict["Max"],
        "Left_Jerk_Std": left_jerk_dict["Std"],

        "Right_Mean_Jerk": right_jerk_dict["Mean"],
        "Right_Median_Jerk": right_jerk_dict["Median"],
        "Right_Max_Jerk": right_jerk_dict["Max"],
        "Right_Jerk_Std": right_jerk_dict["Std"]
    }

    return feature_values

required_feature_columns = [
    "Frames",
    "Duration_Seconds",

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
    "Right_Jerk_Std"
]

for column in required_feature_columns:
    if column not in features_df.columns:
        features_df[column] = np.nan

processed_folder = Path("processed")

task_folder_map = {
    "Knot Tying": processed_folder / "knot_tying",
    "Needle Passing": processed_folder / "needle_passing",
    "Suturing": processed_folder / "suturing"
}

successful_trials = 0
missing_files = []
failed_trials = []

for row_index, row in features_df.iterrows():
    trial_name = row["Trial_Name"]
    task = row["Task"]

    print("=" * 60)
    print(
        f"Processing row {row_index + 1} "
        f"of {len(features_df)}: {trial_name}"
    )

    if task not in task_folder_map:
        print(f"Unknown task: {task}")
        failed_trials.append((trial_name, f"Unknown task: {task}"))
        continue

    trial_file = task_folder_map[task] / f"{trial_name}.csv"

    if not trial_file.exists():
        print(f"File not found: {trial_file}")
        missing_files.append(str(trial_file))
        continue

    try:
        feature_values = extract_features(trial_file)

        # Place every calculated feature into the current metadata row
        for column_name, value in feature_values.items():
            features_df.at[row_index, column_name] = value

        successful_trials += 1
        print("Features added successfully.")

    except Exception as error:
        print(f"Feature extraction failed: {error}")
        failed_trials.append((trial_name, str(error)))


print("\n" + "=" * 60)
print("EXTRACTION SUMMARY")
print("=" * 60)

print(f"Metadata rows: {len(features_df)}")
print(f"Successful trials: {successful_trials}")
print(f"Missing files: {len(missing_files)}")
print(f"Failed trials: {len(failed_trials)}")

if missing_files:
    print("\nMissing trial files:")
    for file in missing_files:
        print(file)

if failed_trials:
    print("\nFailed trials:")
    for trial_name, error in failed_trials:
        print(f"{trial_name}: {error}")

missing_feature_counts = (
    features_df[required_feature_columns]
    .isna()
    .sum()
)

print("\nMissing values by feature column:")
print(missing_feature_counts)

rows_with_missing_features = features_df[
    features_df[required_feature_columns]
    .isna()
    .any(axis=1)
]

print(
    "\nRows containing at least one missing feature:",
    len(rows_with_missing_features)
)

if not rows_with_missing_features.empty:
    print(
        rows_with_missing_features[
            ["Trial_ID", "Trial_Name", "Task"]
        ]
    )

output_file = Path("features/features_dataset_completed.csv")

features_df.to_csv(
    output_file,
    index=False
)

print(f"\nCompleted dataset saved to: {output_file}")