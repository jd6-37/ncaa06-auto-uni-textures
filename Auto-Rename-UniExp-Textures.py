from PIL import Image
import imagehash
import shutil
import cv2
import os
import sys
import csv
from skimage.metrics import structural_similarity as compare_ssim

# Use sys._MEIPASS if running as a PyInstaller executable, otherwise use the script's directory
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys._MEIPASS)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Read the content of the config file
config_file_path = os.path.join(script_dir, 'config.txt')
config_content = {}
with open(config_file_path) as f:
    exec(f.read(), config_content)

# Extract the dumps_path from the config
dumps_path = config_content.get('dumps_path', None)

# Extract the uniform_slot_name from the config
uniform_slot_name = config_content.get('uniform_slot_name', None)

# Extract the uniform_type from the config
uniform_type = config_content.get('uniform_type', None)

# Extract the pridesticker_transparent from the config
pridesticker_transparent = config_content.get('pridesticker_transparent', None)

# Define the 'put_textures_here' source folder
source_folder = os.path.join(script_dir, "YOUR_TEXTURES_HERE")

# Define the 'renamed' folder
renamed_folder = os.path.join(script_dir, "RENAMED")

# Define the 'default textures' folder
default_textures_folder = os.path.join(script_dir, "default-textures")


print()  # Add a line break 
print()  # Add a line break 
print("############################################################")
print("#                                                          #")
print("#   NCAA NEXT Uniform Expansion Texture Renaming Utility   #")
print("#                                                          #")
print("#                  Version: Beta 0.1                       #")
print("#                                                          #")
print("############################################################")


# Check if dumps_path is not defined or the folder does not exist
if not dumps_path or not os.path.exists(dumps_path):
    # Prompt the user to enter a path
    print()  # Add a line break 
    user_input_path = input(r"[!] The path to the DUMPS FOLDER is not defined in config.txt or does not exist. Enter the full path to the dumps folder (Eg. C:\PCSX2\textures\SLUS-21214\dumps): ")
    
    # Validate if the entered path exists
    while not os.path.exists(user_input_path):
        print()  # Add a line break 
        print("Error: The specified folder does not exist. Please enter a valid path.")
        user_input_path = input("Enter the path to the DUMPS FOLDER: ")

    # Use the user's input for dumps_path
    dumps_path = user_input_path

# Output the value of dumps_path
print(f"\n[•]   The DUMPS FOLDER is defined and confirmed to exist at:    #")
print(f"\n#   {dumps_path}  #")
print(f"\n#---------------------------------------------------------------------#")
print()  # Add a line break 


# Check if uniform_slot_name is not defined or the folder does not exist
if not uniform_slot_name:
    # Prompt the user to enter a path
    print()  # Add a line break 
    uniform_slot_name = input("[!] The UNIFORM SLOT NAME is not defined in config.txt. Enter the name in the format of teamname-slotname (Eg. appstate-alt03, appstate-home, etc.): ")
# Output the value of uniform_slot_name
print(f"\n[•] The UNIFORM SLOT NAME is defined as (if this is incorrect, edit it in config.txt):")
print(f"\n#               {uniform_slot_name}                                   #")
print(f"\n#---------------------------------------------------------------------#")
print()  # Add a line break 

# Check if uniform_type is not defined or the folder does not exist
if not uniform_type:
    # Prompt the user to enter a path
    print()  # Add a line break 
    uniform_type = input("[!] The UNIFORM TYPE is not defined in config.txt. Are you making a dark (home) uniform or light (away) uniform? (dark/light): ")
# Output the value of uniform_type
print(f"\n[•] The UNIFORM TYPE is (if this is incorrect, edit it in config.txt): ")
print(f"\n#                {uniform_type}                                                #")
print(f"\n#---------------------------------------------------------------------#")
# Add a condition to check the uniform type and set the appropriate path
if uniform_type.lower() == 'dark':
    reference_folder = "reference-dark"
elif uniform_type.lower() == 'light':
    reference_folder = "reference-light"
else:
    print("Invalid input. Assuming dark uniform.")
    reference_folder = "reference-dark"
# Output the selected default textures folder
print(f"The reference folder for the {uniform_type} uniform is set to: {reference_folder}. Feel free to use your actual dumped textures in here if the image matching utility is having trouble finding a match.")
print()  # Add a line break 


# Check if pridesticker_transparent is defined in the config
if pridesticker_transparent is not None:
    transparent_pride_stickers = pridesticker_transparent
else:
    # Function to ask if the pride stickers should be transparent
    def prompt_transparent_pride_stickers():
        print()  # Add a line break 
        user_input = input("[!] The PRIDE STICKER PREFERENCE is not defined in config.txt. Do you want to make the pride stickers transparent? (yes/no): ").lower()
        return user_input == "yes" or user_input == "y"

    # Check if user wants to make pride stickers transparent
    transparent_pride_stickers = prompt_transparent_pride_stickers()

# Output the value of pridesticker_transparent
print(f"\n[•] PRIDE STICKERS TRANSPARENTED? (If this is incorrect, edit it in config.txt):")
print(f"\n#                {transparent_pride_stickers}                                                  #")
print(f"\n#---------------------------------------------------------------------#")


# Ask the user to press Enter to continue
print()  # Add a line break 
input("Are you ready to proceed? Press enter to continue.")

print()  # Add a line break 
print("#----------------------------------------------------------#")
print("#                                                          #")
print("#                     RESULTS:                             #")
print("#                                                          #")

# Open a CSV file for writing
csv_filename = f"{uniform_slot_name}.csv"
csv_file_path = os.path.join(script_dir, csv_filename)
with open(csv_file_path, mode='w', newline='') as csvfile:
    fieldnames = ['file', 'new_file_name']
    csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    csv_writer.writeheader()

    # Function to calculate hash_tolerance_for_pass
    def calculate_hash_tolerance(reference_hash_phash, compared_hash_phash, reference_hash_dhash, compared_hash_dhash):
        return max(
            abs(reference_hash_phash - compared_hash_phash),
            abs(reference_hash_dhash - compared_hash_dhash)
        )

    # Using a few different methods for comparing files to find the matching dumped texture
    def find_similar_images(reference_image_path, dumps_path, file_params=None, context=None):
        
        
                            
        # Construct the correct path for the reference image
        if context:
          reference_image_path = os.path.join(script_dir, reference_folder, 'alts', source_image)
        else:
          reference_image_path = os.path.join(script_dir, reference_folder, source_image)

        # Extract the directory containing the reference image
        reference_directory = os.path.dirname(reference_image_path)

        reference_image = Image.open(reference_image_path)
        reference_hash_phash = imagehash.phash(reference_image)
        reference_hash_dhash = imagehash.dhash(reference_image)
        reference_image_dimensions = reference_image.size
        reference_file_info = os.stat(reference_image_path)
        reference_file_size = reference_file_info.st_size

        similar_images = []

        for filename in os.listdir(dumps_path):
            if filename.endswith(".png"):
                file_path = os.path.join(dumps_path, filename)

                # print()
                # print()
                # print(f"Comparing {reference_image_path} and {file_path}") 
                # print(f"file is a PNG file.")

                compared_file_info = os.stat(file_path)
                compared_file_size = compared_file_info.st_size

                # Limit to only files of similar size
                if abs(reference_file_size - compared_file_size) <= 100:  # 1024 = Within 1kb file size difference
                    compared_image = Image.open(file_path)
                    compared_image_dimensions = compared_image.size

                    if context and "alternate" in context:
                          print(f"Running in alternate context.")
                    

                    if reference_image_dimensions == compared_image_dimensions:
                        compared_hash_phash = imagehash.phash(compared_image)
                        compared_hash_dhash = imagehash.dhash(compared_image)

                        

                        # Check if per-item parameters exist and use default values from config.txt if not
                        hash_tolerance_default = config_content.get('hash_tolerance_default', 8)
                        ssim_threshold_default = config_content.get('ssim_threshold_default', 0.93)

                        hash_tolerance = file_params.get('hash_tolerance', None) if file_params is not None else None
                        ssim_threshold = file_params.get('ssim_threshold', None) if file_params is not None else None

                        # Set to default if not provided in file_params
                        hash_tolerance = hash_tolerance if hash_tolerance is not None else hash_tolerance_default
                        ssim_threshold = ssim_threshold if ssim_threshold is not None else ssim_threshold_default

                        if (
                                abs(reference_hash_phash - compared_hash_phash) <= hash_tolerance
                                and abs(reference_hash_dhash - compared_hash_dhash) <= hash_tolerance
                        ):
                          reference_cv_image = cv2.imread(reference_image_path)
                          compared_cv_image = cv2.imread(file_path)

                          ssim = compare_ssim(reference_cv_image, compared_cv_image, win_size=5, multichannel=True,
                                              channel_axis=2)
                        
                          
                          # print(f"Comparing {reference_image_path} and {file_path}")
                          # print(f"SSIM: {ssim}")


                          if ssim >= ssim_threshold:
                              # Calculate hash_tolerance_for_pass and print the result
                              hash_tolerance_for_pass = calculate_hash_tolerance(
                                  reference_hash_phash, compared_hash_phash,
                                  reference_hash_dhash, compared_hash_dhash
                              )
                              similar_images.append((file_path, ssim, hash_tolerance_for_pass))
                              # Sort by SSIM value (descending) and hash_tolerance_for_pass (ascending)
                              similar_images.sort(key=lambda x: (-x[1], x[2]))

        return similar_images







    # Dictionary of files and their corresponding source images in the reference_folder folder
    # you can override the default file match paramaters to tighten or loosen the search
    # Assuming that you have already loaded the config.txt values into config_content dictionary

    # Dictionary of files and their corresponding source images in the reference_folder folder
    # you can override the default file match parameters to tighten or loosen the search
    reference_files = {
        "06-TC_Face_Protector.png": {"source": "06-TC_Face_Protector.png", "hash_tolerance": config_content.get('hash_tolerance_06_TC_Face_Protector'), "ssim_threshold": config_content.get('ssim_threshold_06_TC_Face_Protector')},
        "25-TC_Face_Protector_Top.png": {"source": "25-TC_Face_Protector_Top.png", "hash_tolerance": config_content.get('hash_tolerance_25_TC_Face_Protector_Top'), "ssim_threshold": config_content.get('ssim_threshold_25_TC_Face_Protector_Top')},
        "14-Bk_TC_Pad.png": {"source": "14-Bk_TC_Pad.png", "hash_tolerance": config_content.get('hash_tolerance_14_Bk_TC_Pad'), "ssim_threshold": config_content.get('ssim_threshold_14_Bk_TC_Pad')},
        "10-Wt_TC_Pad.png": {"source": "10-Wt_TC_Pad.png", "hash_tolerance": config_content.get('hash_tolerance_10_Wt_TC_Pad'), "ssim_threshold": config_content.get('ssim_threshold_10_Wt_TC_Pad')},
        "07-TC_Med_Band--34_sleeve_top.png": {"source": "07-TC_Med_Band--34_sleeve_top.png", "hash_tolerance": config_content.get('hash_tolerance_07_TC_Med_Band--34_sleeve_top'), "ssim_threshold": config_content.get('ssim_threshold_07_TC_Med_Band--34_sleeve_top')},
        "04-TC_Thin_Band.png": {"source": "04-TC_Thin_Band.png", "hash_tolerance": config_content.get('hash_tolerance_04_TC_Thin_Band'), "ssim_threshold": config_content.get('ssim_threshold_04_TC_Thin_Band')},
        "15-TC_Long_Sleeve.png": {"source": "15-TC_Long_Sleeve.png", "hash_tolerance": config_content.get('hash_tolerance_15_TC_Long_Sleeve'), "ssim_threshold": config_content.get('ssim_threshold_15_TC_Long_Sleeve')},
        "wrist_QB_Wrist_Bk.png": {"source": "wrist_QB_Wrist_Bk.png", "hash_tolerance": config_content.get('hash_tolerance_wrist_QB_Wrist_Bk'), "ssim_threshold": config_content.get('ssim_threshold_wrist_QB_Wrist_Bk')},
        "wrist_QB_Wrist_Wt.png": {"source": "wrist_QB_Wrist_Wt.png", "hash_tolerance": config_content.get('hash_tolerance_wrist_QB_Wrist_Wt'), "ssim_threshold": config_content.get('ssim_threshold_wrist_QB_Wrist_Wt')},
        "03-TC_QB_Wrist.png": {"source": "03-TC_QB_Wrist.png", "hash_tolerance": config_content.get('hash_tolerance_03_TC_QB_Wrist'), "ssim_threshold": config_content.get('ssim_threshold_03_TC_QB_Wrist')},
        "01-TC_Wrist.png": {"source": "01-TC_Wrist.png", "hash_tolerance": config_content.get('hash_tolerance_01_TC_Wrist'), "ssim_threshold": config_content.get('ssim_threshold_01_TC_Wrist')},
        "wrist_Half_Sleeve_Wt.png": {"source": "wrist_Half_Sleeve_Wt.png", "hash_tolerance": config_content.get('hash_tolerance_wrist_Half_Sleeve_Wt'), "ssim_threshold": config_content.get('ssim_threshold_wrist_Half_Sleeve_Wt')},
        "wrist_Half_Sleeve_Bk.png": {"source": "wrist_Half_Sleeve_Bk.png", "hash_tolerance": config_content.get('hash_tolerance_wrist_Half_Sleeve_Bk'), "ssim_threshold": config_content.get('ssim_threshold_wrist_Half_Sleeve_Bk')},
        "11-TC_Half_Sleeve.png": {"source": "11-TC_Half_Sleeve.png", "hash_tolerance": config_content.get('hash_tolerance_11_TC_Half_Sleeve'), "ssim_threshold": config_content.get('ssim_threshold_11_TC_Half_Sleeve')},
        "16-Shoe.png": {"source": "16-Shoe.png", "hash_tolerance": config_content.get('hash_tolerance_16_Shoe'), "ssim_threshold": config_content.get('ssim_threshold_16_Shoe')},
        "17-Shoe_w_White_Tape.png": {"source": "17-Shoe_w_White_Tape.png", "hash_tolerance": config_content.get('hash_tolerance_17_Shoe_w_White_Tape'), "ssim_threshold": config_content.get('ssim_threshold_17_Shoe_w_White_Tape')},
        "23-Shoe_w_Black_Tape.png": {"source": "23-Shoe_w_Black_Tape.png", "hash_tolerance": config_content.get('hash_tolerance_23_Shoe_w_Black_Tape'), "ssim_threshold": config_content.get('ssim_threshold_23_Shoe_w_Black_Tape')},
        "24-Shoe_w_TC_Tape.png": {"source": "24-Shoe_w_TC_Tape.png", "hash_tolerance": config_content.get('hash_tolerance_24_Shoe_w_TC_Tape'), "ssim_threshold": config_content.get('ssim_threshold_24_Shoe_w_TC_Tape')},
        "13-Sock.png": {"source": "13-Sock.png", "hash_tolerance": config_content.get('hash_tolerance_13_Sock'), "ssim_threshold": config_content.get('ssim_threshold_13_Sock')},
        "helmet.png": {"source": "helmet.png", "hash_tolerance": config_content.get('hash_tolerance_helmet'), "ssim_threshold": config_content.get('ssim_threshold_helmet')},
        "22-Chinstrap.png": {"source": "22-Chinstrap.png", "hash_tolerance": config_content.get('hash_tolerance_22_Chinstrap'), "ssim_threshold": config_content.get('ssim_threshold_22_Chinstrap')},
        "pridesticker.png": {"source": "pridesticker.png", "hash_tolerance": config_content.get('hash_tolerance_pridesticker'), "ssim_threshold": config_content.get('ssim_threshold_pridesticker')},
        "18-Facemask_Far.png": {"source": "18-Facemask_Far.png", "hash_tolerance": config_content.get('hash_tolerance_18_Facemask_Far'), "ssim_threshold": config_content.get('ssim_threshold_18_Facemask_Far')},
        "20-Facemask_Near.png": {"source": "20-Facemask_Near.png", "hash_tolerance": config_content.get('hash_tolerance_20_Facemask_Near'), "ssim_threshold": config_content.get('ssim_threshold_20_Facemask_Near')},
        "pants.png": {"source": "pants.png", "hash_tolerance": config_content.get('hash_tolerance_pants'), "ssim_threshold": config_content.get('ssim_threshold_pants')},
        "jersey.png": {"source": "jersey.png", "hash_tolerance": config_content.get('hash_tolerance_jersey'), "ssim_threshold": config_content.get('ssim_threshold_jersey')},
        "num07.png": {"source": "num07.png", "hash_tolerance": config_content.get('hash_tolerance_num07'), "ssim_threshold": config_content.get('ssim_threshold_num07')},
        "num89.png": {"source": "num89.png", "hash_tolerance": config_content.get('hash_tolerance_num89'), "ssim_threshold": config_content.get('ssim_threshold_num89')},
        "num07shadow.png": {"source": "num07shadow.png", "hash_tolerance": config_content.get('hash_tolerance_num07shadow'), "ssim_threshold": config_content.get('ssim_threshold_num07shadow')},
        "num89shadow.png": {"source": "num89shadow.png", "hash_tolerance": config_content.get('hash_tolerance_num89shadow'), "ssim_threshold": config_content.get('ssim_threshold_num89shadow')},
        "num07helmet.png": {"source": "num07helmet.png", "hash_tolerance": config_content.get('hash_tolerance_num07helmet'), "ssim_threshold": config_content.get('ssim_threshold_num07helmet')},
        "num89helmet.png": {"source": "num89helmet.png", "hash_tolerance": config_content.get('hash_tolerance_num89helmet'), "ssim_threshold": config_content.get('ssim_threshold_num89helmet')},
        "num07ss.png": {"source": "num07ss.png", "hash_tolerance": config_content.get('hash_tolerance_num07ss'), "ssim_threshold": config_content.get('ssim_threshold_num07ss')},
        "num89ss.png": {"source": "num89ss.png", "hash_tolerance": config_content.get('hash_tolerance_num89ss'), "ssim_threshold": config_content.get('ssim_threshold_num89ss')}
    }


    # Track multiple matches for warnings
    multiple_matches_dict = {}

    # Define a list of files to skip the multiple matches warning
    skip_warn_multiple = ["num07shadow.png", "num89shadow.png"]

    # Define variables for the base jersey numbers file names
    base_image_num07 = None
    base_image_num89 = None

    # Find the matching dumps for the base jersey numbers and save the filenames for the number shadows step later
    for file, file_data in reference_files.items():
        source_image = file_data["source"]
        params = file_data if 'hash_tolerance' in file_data and 'ssim_threshold' in file_data else None
        similar_images = find_similar_images(os.path.join(script_dir, reference_folder, source_image), dumps_path, params)

        if file == "num07.png" and similar_images:
            base_image_num07 = similar_images[0]  # Taking the first match as the base for num07.png
        elif file == "num89.png" and similar_images:
            base_image_num89 = similar_images[0]  # Taking the first match as the base for num89.png

        if len(similar_images) > 1:
            multiple_matches_dict[file] = True  # Track items with multiple matches
    



    # Initialize a counter for successful operations
    required_textures_counter = 0
    optional_textures_counter = 0

    # Function to process each matching texture
    def process_texture(file, file_data, similar_images):
        global required_textures_counter  # Declare the counter as a global variable
        global optional_textures_counter  # Declare the counter as a global variable
        print()  # Add a line break 
        print(f"[•] Dumped texture found for {file}:")
        for image_path, similarity, hash_tolerance_for_pass in similar_images:
            print(f"{image_path}")
            print(f"Min hash: {hash_tolerance_for_pass} - Max SSIM: {similarity:.4f}")


            # Extract the filename (without extension) of the found image
            found_filename = os.path.splitext(os.path.basename(image_path))[0]

            # Extract the reference file name (without extension)
            reference_filename = os.path.splitext(source_image)[0]

            # Extract the second segment of uniform_slot_name
            if '-' in uniform_slot_name:
                renamed_subfolder = uniform_slot_name.split('-')[1]
            else:
                renamed_subfolder = uniform_slot_name

            # Redefine the 'renamed' folder
            renamed_folder = os.path.join(script_dir, "RENAMED", renamed_subfolder)
            
            # Create 'renamed' folder if it doesn't exist
            if not os.path.exists(renamed_folder):
                os.makedirs(renamed_folder)
            
            
            # Transparent the number shadows
            if file in ["num07shadow.png", "num89shadow.png"]:
                base_image = None
                
                if file == "num07shadow.png" and base_image_num07:
                    base_image = base_image_num07
                    renamed_subfolder = "num07-shadow"
                elif file == "num89shadow.png" and base_image_num89:
                    base_image = base_image_num89
                    renamed_subfolder = "num89-shadow"

                if base_image:
                    base_image_name = os.path.splitext(os.path.basename(base_image[0]))[0] 
                    found_filename_base = os.path.splitext(os.path.basename(image_path))[0]
                    
                    # Extract the number part of the filenames to compare
                    base_image_number = base_image_name[3:5]
                    found_number = found_filename_base[3:5]
                    
                    if base_image_number == found_number:
                        # Create transparents subfolder if it doesn't exist
                        if not os.path.exists(os.path.join(renamed_folder, "transparents", renamed_subfolder)):
                            os.makedirs(os.path.join(renamed_folder, "transparents", renamed_subfolder))
                        # Copy a transparent to the 'renamed' folder and rename 
                        new_file_name = f"{found_filename_base}.png"
                        shutil.copy(os.path.join(default_textures_folder, "transparent.png"), os.path.join(renamed_folder, "transparents", renamed_subfolder, new_file_name))
                        print("NUMBER SHADOW TRANSPARENTED")
                        print("\u2713 SUCCESS. Transparent renamed and filename added to the CSV file.")
                        required_textures_counter += 1
                        # Write to the CSV file
                        csv_writer.writerow({'file': file, 'new_file_name': new_file_name})


            # If answered yes to transparent pride sticker, copy the transparent image instead of a source image
            elif file == "pridesticker.png":
                new_file_name = f"{found_filename}.png"
                if transparent_pride_stickers:
                  # Create transparents subfolder if it doesn't exist
                  if not os.path.exists(os.path.join(renamed_folder, "transparents", "pride-sticker")):
                      os.makedirs(os.path.join(renamed_folder, "transparents", "pride-sticker"))
                  # Copy a transparent to the 'renamed' folder and rename 
                  shutil.copy(os.path.join(default_textures_folder, "transparent.png"), os.path.join(renamed_folder, "transparents", "pride-sticker", new_file_name))
                  print("PRIDE STICKER TRANSPARENTED")
                  # Write to the CSV file
                  csv_writer.writerow({'file': file, 'new_file_name': new_file_name})
                  print("\u2713 SUCCESS. Transparent texture renamed and filename added to the CSV file.")
                  required_textures_counter += 1
                else: 
                  shutil.copy(os.path.join(source_folder, source_image), os.path.join(renamed_folder, new_file_name))
                  # Write to the CSV file
                  csv_writer.writerow({'file': file, 'new_file_name': new_file_name})
                  print("\u2713 SUCCESS. Texture renamed and filename added to the CSV file.")
                  required_textures_counter += 1
            
            # If no helmet or sleeve/shoulder numbers are provided, use the main jersey numbers
            secondary_07_numbers = ["num07helmet.png", "num07ss.png"]
            if os.path.basename(file) in secondary_07_numbers:
              helmet_file = os.path.join(source_folder, os.path.basename(file))
              if os.path.exists(helmet_file):
                  new_file_name = f"{found_filename}.png"
                  shutil.copy(helmet_file, os.path.join(renamed_folder, new_file_name))
                  # Write to the CSV file
                  csv_writer.writerow({'file': file, 'new_file_name': new_file_name})
                  print("\u2713 SUCCESS. Texture renamed and filename added to the CSV file.")
                  optional_textures_counter += 1
              else:
                  new_file_name = f"{found_filename}.png"
                  shutil.copy(os.path.join(source_folder, "num07.png"), os.path.join(renamed_folder, new_file_name))
                  # Write to the CSV file
                  csv_writer.writerow({'file': file, 'new_file_name': new_file_name})
                  print("\u2713 SUCCESS. Texture renamed and filename added to the CSV file.")
                  optional_textures_counter += 1


            secondary_89_numbers = ["num89helmet.png", "num89ss.png"]
            if os.path.basename(file) in secondary_89_numbers:
                helmet_file = os.path.join(source_folder, os.path.basename(file))
                if os.path.exists(helmet_file):
                    new_file_name = f"{found_filename}.png"
                    shutil.copy(helmet_file, os.path.join(renamed_folder, new_file_name))
                    # Write to the CSV file
                    csv_writer.writerow({'file': file, 'new_file_name': new_file_name})
                    print("\u2713 SUCCESS. Texture renamed and filename added to the CSV file.")
                    optional_textures_counter += 1
                else:
                    new_file_name = f"{found_filename}.png"
                    shutil.copy(os.path.join(source_folder, "num89.png"), os.path.join(renamed_folder, new_file_name))
                    # Write to the CSV file
                    csv_writer.writerow({'file': file, 'new_file_name': new_file_name})
                    print("\u2713 SUCCESS. Texture renamed and filename added to the CSV file.")
                    optional_textures_counter += 1

            
            # Everything else
            elif file not in ["num07shadow.png", "num89shadow.png", "num07helmet.png", "num07ss.png", "num89helmet.png", "num89ss.png", "pridesticker.png"]:
              if file in ["wrist_Half_Sleeve_Bk.png", "wrist_Half_Sleeve_Wt.png", "wrist_QB_Wrist_Bk.png", "wrist_QB_Wrist_Wt.png"]:
                  # Copy from os.path.join(script_dir, reference_folder) for specific files
                  new_file_name = f"{found_filename}.png"
                  shutil.copy(os.path.join(default_textures_folder, source_image), os.path.join(renamed_folder, new_file_name))
                  # Write to the CSV file
                  csv_writer.writerow({'file': file, 'new_file_name': new_file_name})
                  print("\u2713 SUCCESS. Texture renamed and filename added to the CSV file.")
                  required_textures_counter += 1
              else:
                  # Copy from source_folder for other files
                  new_file_name = f"{found_filename}.png"
                  shutil.copy(os.path.join(source_folder, source_image), os.path.join(renamed_folder, new_file_name))
                  # Write to the CSV file
                  csv_writer.writerow({'file': file, 'new_file_name': new_file_name})
                  print("\u2713 SUCCESS. Texture renamed and filename added to the CSV file.")
                  required_textures_counter += 1


        # Check if there are multiple matches for this file only if it's not in the skip list
        if file not in skip_warn_multiple and file in multiple_matches_dict:
            # print("^^^^^ !!!! ERROR: MULTIPLE MATCHES !!!!  Try lowering the hash_tolerance and/or raising the ssim_threshold. Only one match is allowed for this texture. ^^^^^")
            print("^^^^^ !! MULTIPLE MATCHES !!  We used the one with the highest SSIM (similarity) value, so all should be okay, but you should keep an eye on this one in your testing. ^^^^^")
        elif file in skip_warn_multiple and file in multiple_matches_dict:
            print("^^^^^ Don't worry, two matches for this texture is okay. We used the correct one by comparing its filename to the other numbers. ^^^^^")
    
    
    def no_texture(file, file_data, similar_images):
        print()  # Add a line break 
        if file in ["17-Shoe_w_White_Tape.png"]:
          print(f"###########################################################")
          print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
          print(f"[•] ==== NO similar images found for {file}. Try raising the hash_tolerance to 2 or more and/or lowering the ssim_threshold for this item in config.txt to broaden the search. Alternatively, you can replace the reference texture with the actual dumped texture for a definite match. ====")
          print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
          print(f"###########################################################")
        elif file in ["num07helmet.png", "num89helmet.png"]:
          print(f"[•] ==== No similar images found for {file}. This is okay if helmet numbers are disabled in this uniform slot. ====")
        elif file in ["num07ss.png", "num89ss.png"]:
          print(f"[•] ==== No similar images found for {file}. This is okay if sleeve/shoulder numbers are disabled in this uniform slot. ====")
        else:
          print(f"###########################################################")
          print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
          print(f"[•] ==== NO similar images found for {file}. Try raising the hash_tolerance and/or lowering the ssim_threshold for this item in config.txt to broaden the search. Alternatively, you can replace the reference texture with the actual dumped texture for a definite match. ====")
          print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
          print(f"###########################################################")

    
    
    
    #-----------------------------------------#
    # Iterate over the reference files to find matches in the dumps and perform the actions
    for file, file_data in reference_files.items():
        source_image = file_data["source"]
        params = file_data if 'hash_tolerance' in file_data and 'ssim_threshold' in file_data else None
        # print(f"Value for first property passed to find_similar_images: {os.path.join(script_dir, reference_folder, source_image)}")
        original_similar_images = find_similar_images(os.path.join(script_dir, reference_folder, source_image), dumps_path, params)

        if file in ["num07shadow.png", "num89shadow.png"]:
            if original_similar_images:
                process_texture(file, file_data, original_similar_images)
            else:
                no_texture(file, file_data, original_similar_images)
        else:
            if original_similar_images and len(original_similar_images) > 0:
                process_texture(file, file_data, [original_similar_images[0]])
            else:
                # Check alternates only when there are no similar images in the original check
                alternate_source_path = os.path.join(script_dir, reference_folder, 'alts', source_image)
                if os.path.exists(alternate_source_path):
                    print()  # Add a line break 
                    print()  # Add a line break 
                    print(f"No match for {source_image}. Trying again using the reference image in the alts folder")
                    alternate_similar_images = find_similar_images(alternate_source_path, dumps_path, params, context="alts")
                    print(f"at: {alternate_source_path}...")
               
                    if alternate_similar_images:
                        process_texture(file, file_data, [alternate_similar_images[0]])
                    else:
                        no_texture(file, file_data, alternate_similar_images)
                else:
                    no_texture(file, file_data, original_similar_images)






# Extract the second segment of uniform_slot_name
if '-' in uniform_slot_name:
    renamed_subfolder = uniform_slot_name.split('-')[1]
else:
    renamed_subfolder = uniform_slot_name

# Redefine the 'renamed' folder
renamed_folder = os.path.join(script_dir, "RENAMED", renamed_subfolder)

# Move the CSV file to the 'renamed' folder
shutil.move(csv_file_path, os.path.join(renamed_folder, csv_filename))
shutil.copy(config_file_path, os.path.join(renamed_folder, 'config.txt'))
           
print()  # Add a line break 
print("#--------------------------------------------------------------#")
print("#                                                              #")
if required_textures_counter < 30:
  print("#                 !!!! DONE WITH ERRORS !!!!                   #")
  print(f"#         Number of textures found and renamed: {required_textures_counter + optional_textures_counter}             #")
else: 
  print("#                         SUCCESS!                             #")
  print(f"#         Number of textures found and renamed: {required_textures_counter + optional_textures_counter}             #")
print(f"#                   Required: {required_textures_counter} of 30 ✔                       #")
print(f"#                    Optional: {optional_textures_counter} of 4                          #")
if required_textures_counter < 30:
  print("#                                                              #")
  print("#                !!!!  SOMETHING WENT WRONG. !!!               #")
  print(f"#     !!!!  {30 - required_textures_counter} of the required textures are missing.  !!!       #")
print("#                                                              #")
print("#       READ ALL OF THE OUTPUT ABOVE TO CHECK FOR ISSUES.      #")
print("#      Your renamed textures are in a subfolder of RENAMED.    #")
print("# The texture names were written to a CSV file in that folder. #")
print("#     (a copy of your config file has also been put there)     #")
print("#  Be sure to leave the CSV file in the folder and submit it   #")
print("#    with the uniform for easy future edits of this slot.      #")
print("#                                                              #")
print("#        ---  PRESS ENTER OR CLOSE THIS WINDOW  ---            #")
print("#                                                              #")
print("################################################################")
print()  # Add a line break 
print()  # Add a line break 

input()