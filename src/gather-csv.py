import os
import shutil

# Check if CSVs folder exists, and create it if not
csv_folder_path = "RENAMED-DONE/CSVs"
if not os.path.exists(csv_folder_path):
    os.makedirs(csv_folder_path)

# Move all CSV files to RENAMED-DONE/CSVs, avoiding overwriting by appending suffix
for root, dirs, files in os.walk("RENAMED-DONE"):
    for file in files:
        if file.endswith(".csv") and not root.startswith(csv_folder_path):
            source_path = os.path.join(root, file)
            target_path = os.path.join(csv_folder_path, file)
            count = 1

            while os.path.exists(target_path):
                target_path = os.path.join(
                    csv_folder_path, f"{os.path.splitext(file)[0]}-{count}.csv"
                )
                count += 1

            shutil.move(source_path, target_path)

# Delete everything in RENAMED-DONE except for CSVs folder and its contents
for item in os.listdir("RENAMED-DONE"):
    item_path = os.path.join("RENAMED-DONE", item)
    if os.path.isdir(item_path) and item != "CSVs":
        shutil.rmtree(item_path)
