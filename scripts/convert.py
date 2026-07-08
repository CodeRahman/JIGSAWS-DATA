import pandas as pd
from pathlib import Path
from columns import columns


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
        convert_txt_to_csv(file, columns, outputfolder)


print(len(columns))
assert len(columns) == 76

tasks = [
    ("raw/knot_tying", "knot_tying"),
    ("raw/suturing", "suturing"),
    ("raw/needle_passing", "needle_passing"),
]

for folder, output in tasks:
    convert_multiple_files_in_folder(folder, output)

