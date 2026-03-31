import pandas as pd
import os

def save_to_csv(df, filepath):
    # create parent folder if it does not exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # if file already exists, append to it, otherwise create a new file
    if os.path.exists(filepath):
        existing_df = pd.read_csv(filepath)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_csv(filepath, index=False)
    else:
        df.to_csv(filepath, index=False)

    print(f"Saved data to {filepath}")