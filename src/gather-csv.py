import os
import shutil

# Define the source and destination folders
source_folder = "RENAMED"
destination_folder = "RENAMED-DONE/CSVs"

# Create the destination folder if it does not exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)
    print(f"\nCreated desination directory: {destination_folder}\n")
else:
    print(f"\nDestination directory exists: {destination_folder}\n")

# Walk through the source folder up to 2 levels deep
for root, dirs, files in os.walk(source_folder):
    # Calculate the depth of the current directory from the source folder
    depth = root[len(source_folder):].count(os.sep)
    
    # Process files only if the depth is 2 or less
    if depth <= 2:
        for file in files:
            if file.endswith(".csv"):
                source_path = os.path.join(root, file)
                target_path = os.path.join(destination_folder, file)
                count = 1

                # print(f"Found CSV file: {source_path}")

                # Ensure the target path does not overwrite existing files
                while os.path.exists(target_path):
                    target_path = os.path.join(
                        destination_folder, f"{os.path.splitext(file)[0]}-{count}.csv"
                    )
                    count += 1

                # Copy the CSV file to the destination folder
                print(f"Copying {file} to {destination_folder}")
                shutil.copy2(source_path, target_path)

print("\nCSV files copying completed.\n")
