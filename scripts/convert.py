import pandas as pd
from pathlib import Path


#convert txt raw data files to csv for data analysis
def convert_txt_to_csv(file, column_names, subfolder):
    df = pd.read_csv(
        file,
        sep=r"\s+",
        header = None,
        names= column_names
    )
    csv_name = Path(file).stem

    df.to_csv(
    f"processed/{subfolder}/{csv_name}.csv",
    index=False
    )

def convert_multiple_files_in_folder(folder, subfolder):
    for file in Path(folder).glob("*.txt"):
        convert_txt_to_csv(file, columns, subfolder)

columns = ["MASTER_LEFT_POS_X", "MASTER_LEFT_POS_Y", "MASTER_LEFT_POS_Z", "MASTER_LEFT_ROT_R11", 
           "MASTER_LEFT_ROT_R12", "MASTER_LEFT_ROT_R13", "MASTER_LEFT_ROT_R21", "MASTER_LEFT_ROT_R22", "MASTER_LEFT_ROT_R23", 
           "MASTER_LEFT_ROT_R31", "MASTER_LEFT_ROT_R32", "MASTER_LEFT_ROT_R33", "MASTER_LEFT_LIN_VEL_X", "MASTER_LEFT_LIN_VEL_Y",
           "MASTER_LEFT_LIN_VEL_Z", "MASTER_LEFT_ROT_VEL_X", "MASTER_LEFT_ROT_VEL_Y", "MASTER_LEFT_ROT_VEL_Z", "MASTER_LEFT_GRIPPER_ANGLE", 
           "MASTER_RIGHT_POS_X", "MASTER_RIGHT_POS_Y", "MASTER_RIGHT_POS_Z", "MASTER_RIGHT_ROT_R11", "MASTER_RIGHT_ROT_R12", 
           "MASTER_RIGHT_ROT_R13", "MASTER_RIGHT_ROT_R21", "MASTER_RIGHT_ROT_R22", "MASTER_RIGHT_ROT_R23", "MASTER_RIGHT_ROT_R31", 
           "MASTER_RIGHT_ROT_R32", "MASTER_RIGHT_ROT_R33", "MASTER_RIGHT_LIN_VEL_X", "MASTER_RIGHT_LIN_VEL_Y", "MASTER_RIGHT_LIN_VEL_Z", 
           "MASTER_RIGHT_ROT_VEL_X", "MASTER_RIGHT_ROT_VEL_Y", "MASTER_RIGHT_ROT_VEL_Z", "MASTER_RIGHT_GRIPPER_ANGLE", "SLAVE_LEFT_POS_X", 
           "SLAVE_LEFT_POS_Y", "SLAVE_LEFT_POS_Z", "SLAVE_LEFT_ROT_R11", 
           "SLAVE_LEFT_ROT_R12", "SLAVE_LEFT_ROT_R13", "SLAVE_LEFT_ROT_R21", "SLAVE_LEFT_ROT_R22", "SLAVE_LEFT_ROT_R23", 
           "SLAVE_LEFT_ROT_R31", "SLAVE_LEFT_ROT_R32", "SLAVE_LEFT_ROT_R33", "SLAVE_LEFT_LIN_VEL_X", "SLAVE_LEFT_LIN_VEL_Y",
           "SLAVE_LEFT_LIN_VEL_Z", "SLAVE_LEFT_ROT_VEL_X", "SLAVE_LEFT_ROT_VEL_Y", "SLAVE_LEFT_ROT_VEL_Z", "SLAVE_LEFT_GRIPPER_ANGLE", 
           "SLAVE_RIGHT_POS_X", "SLAVE_RIGHT_POS_Y", "SLAVE_RIGHT_POS_Z", "SLAVE_RIGHT_ROT_R11", "SLAVE_RIGHT_ROT_R12", 
           "SLAVE_RIGHT_ROT_R13", "SLAVE_RIGHT_ROT_R21", "SLAVE_RIGHT_ROT_R22", "SLAVE_RIGHT_ROT_R23", "SLAVE_RIGHT_ROT_R31", 
           "SLAVE_RIGHT_ROT_R32", "SLAVE_RIGHT_ROT_R33", "SLAVE_RIGHT_LIN_VEL_X", "SLAVE_RIGHT_LIN_VEL_Y", "SLAVE_RIGHT_LIN_VEL_Z", 
           "SLAVE_RIGHT_ROT_VEL_X", "SLAVE_RIGHT_ROT_VEL_Y", "SLAVE_RIGHT_ROT_VEL_Z", "SLAVE_RIGHT_GRIPPER_ANGLE"]

print(len(columns))
assert len(columns) == 76

convert_multiple_files_in_folder("raw/knot_tying", "knot_tying")
convert_multiple_files_in_folder("raw/suturing", "suturing")
convert_multiple_files_in_folder("raw/needle_passing", "needle_passing")

