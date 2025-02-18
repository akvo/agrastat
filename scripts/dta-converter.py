import os
import pandas as pd
from pathlib import Path

# Define the root directory
root_dir = "2016 Baseline Data"  # Change this to your base directory
converted_root = f"{root_dir}_converted"

# Ensure the converted root directory exists
os.makedirs(converted_root, exist_ok=True)

# Walk through all subdirectories
for dirpath, dirnames, filenames in os.walk(root_dir):

    # Create corresponding directory in converted_root with full depth structure
    relative_path = os.path.relpath(dirpath, root_dir)
    converted_dir = os.path.join(converted_root, relative_path)
    os.makedirs(converted_dir, exist_ok=True)

    for file in filenames:
        if file.endswith(".dta"):
            dta_file_path = os.path.join(dirpath, file)
            csv_file_path = os.path.join(
                converted_dir, file.replace(".dta", ".csv")
            )

            # Convert .dta to .csv
            try:
                df = pd.read_stata(dta_file_path, convert_categoricals=False)
                df.to_csv(csv_file_path, index=False, encoding="utf-8")
                print(f"Converted: {dta_file_path} -> {csv_file_path}")
            except UnicodeDecodeError:
                try:
                    df = pd.read_stata(
                        dta_file_path,
                        convert_categoricals=False,
                        preserve_dtypes=False,
                    )
                    df.to_csv(csv_file_path, index=False, encoding="utf-8")
                    print(
                        f"Converted with preserve_dtypes=False: {dta_file_path} -> {csv_file_path}"
                    )
                except Exception as e:
                    print(f"Error converting {dta_file_path}: {e}")
            except Exception as e:
                print(f"Error converting {dta_file_path}: {e}")

print("Conversion completed.")
