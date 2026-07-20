import pandas as pd
from pathlib import Path
from columns import trial_columns
from columns import result_columns


#convert txt raw data files to csv for data analysis
def convert_txt_to_csv(file, column_names, outputfolder):
    df = pd.read_csv(
        file,
        sep=r"\s+",
        header = None,
        names= column_names
    )
    csv_name = Path(file).stem

    df.to_csv(
    f"processed/{outputfolder}/{csv_name}.csv",
    index=False
    )

def convert_multiple_files_in_folder(folder, outputfolder):
    for file in Path(folder).glob("*.txt"):
        convert_txt_to_csv(file, trial_columns, outputfolder)

def convert_result_files_in_folder(folder, outputfolder):
    for file in Path(folder).glob("*.txt"):
        convert_txt_to_csv(file, result_columns, outputfolder)

print(len(trial_columns))
assert len(trial_columns) == 76

print(len(result_columns))
assert len(result_columns) == 9

tasks = [
    ("raw/knot_tying", "knot_tying"),
    ("raw/suturing", "suturing"),
    ("raw/needle_passing", "needle_passing"),
]

for folder, output in tasks:
    convert_multiple_files_in_folder(folder, output)

convert_result_files_in_folder("raw/trial_results", "trial_results")
