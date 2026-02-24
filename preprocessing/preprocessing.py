import os
import pandas as pd
from tqdm import tqdm

# ── Parameters ───────────────────────────────────────────────
TIME_SIZE   = 10          # Default interval fill value (seconds)
WINDOW_SIZE = f'{TIME_SIZE}s'  # Rolling window size for frequency features


def processing(df):
    """
    Feature extraction pipeline for raw CAN bus log data.
    
    Input columns : Interface, Timestamp, Arbitration_ID, DLC, Data, Label
    Output columns: Arbitration_ID, DLC, Label,
                    Prev_Interver, ID_Prev_Interver, Data_Prev_Interver,
                    ID_Frequency, Data_Frequency, Frequency_diff
    """

    # 1. Label Encoding
    #    Map string attack labels to integer class codes
    #    Normal→0, DoS→1, Spoofing→2, Replay→3, Fuzzing→4, Spoofing_UDS_*→5
    pass

    # 2. Data Field Conversion
    #    Fill missing Data values with '00'
    #    Parse space-separated hex bytes into a single integer
    #    e.g., "40 B2 81" → 0x40B281 → int
    pass

    # 3. Arbitration ID Conversion
    #    Convert hex string to integer
    #    e.g., "7FF" → 2047
    pass

    # 4. Time Interval Features
    #    Prev_Interver      : time elapsed since the previous frame (global)
    #    ID_Prev_Interver   : time elapsed since the previous frame with the same Arbitration_ID
    #    Data_Prev_Interver : time elapsed since the previous frame with the same (ID, Data) pair
    #    Fill NaN (first occurrence) with TIME_SIZE
    pass

    # 5. Rolling Frequency Features
    #    Set DateTime index from Timestamp for rolling window operations
    #
    #    ID_Frequency   : count of frames with the same Arbitration_ID within WINDOW_SIZE
    #    Data_Frequency : count of frames with the same (ID, Data) pair within WINDOW_SIZE
    #    Frequency_diff : ID_Frequency - Data_Frequency
    #                     (measures how many IDs share the same data pattern)
    pass

    # 6. Cleanup
    #    Drop intermediate/raw columns: DateTime, Timestamp, Data, Interface
    #    Reset index
    pass

    return df


def main():
    """
    Load raw train/test label CSVs, apply processing(), and save as proc.csv files.

    Input  : dataset/.../Interface/{train,test}/*labels.csv
    Output : source/AutoHack/train_proc.csv
             source/AutoHack/test_proc.csv
    """

    program_path = os.getcwd()

    # Paths to train and test raw label files
    path_list = [
        os.path.join(program_path, "dataset", "AutoHack_Dataset", "Interface", "train"),
        os.path.join(program_path, "dataset", "AutoHack_Dataset", "Interface", "test"),
    ]

    source_path = os.path.join(program_path, "source", "AutoHack")
    os.makedirs(source_path, exist_ok=True)

    for path in path_list:
        # Collect all label CSV files in the split directory
        pass

        # Process each label file and store results
        #   - Load CSV
        #   - Apply processing()
        #   - Append to file_data dict
        pass

        # Concatenate all processed files and save
        #   → {split}_proc.csv  (e.g., train_proc.csv)
        pass


if __name__ == "__main__":
    main()
