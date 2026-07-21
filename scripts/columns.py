trial_columns = ["MASTER_LEFT_POS_X", "MASTER_LEFT_POS_Y", "MASTER_LEFT_POS_Z", "MASTER_LEFT_ROT_R11", 
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

result_columns = ["trial", "self_skil", "grs_score", "tissue_respect", "handling", "time_and_motion", "flow", "performance", "quality"]

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