import os

def find_duplicate_png_files(folder):
    png_files = {}
    duplicate_sets = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith('.png'):
                file_path = os.path.join(root, file)
                if file in png_files:
                    existing_file_path = png_files[file]
                    duplicate_set = {existing_file_path, file_path}
                    duplicate_sets.append(duplicate_set)
                else:
                    png_files[file] = file_path

    return duplicate_sets

folder_to_check = 'RENAMED'
duplicate_sets = find_duplicate_png_files(folder_to_check)

print()
print("Checking recursively in the RENAMED folder to ensure all filenames are unique...")
print()

if duplicate_sets:
    print()
    print("******  WARNING: Duplicate texture names found*  *******")
    print("*                                                      *")
    print("*     You may have dumped the same uniform twice.      *")
    print("*     Correct it or redump. No two files can have      *")
    print("*        the same name anywhere in replacements.       *")
    print("*                                                      *")
    for idx, duplicate_set in enumerate(duplicate_sets, start=1):
        print(f"\nDuplicate Set {idx}:")
        for duplicate in duplicate_set:
            print(duplicate)
    print()
else:
    print()
    print("Success. No duplicate PNG files found.")
    print()

print("Press Enter or close this window to exit.")
input()