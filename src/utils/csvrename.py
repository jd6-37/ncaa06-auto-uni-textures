from PIL import Image
import imagehash
import shutil
import cv2
import os
import sys
import csv
import platform
import glob
import time
from skimage.metrics import structural_similarity as compare_ssim
from colorama import init, Fore, Style
init()  # initialize colorama for ANSI color codes in Windows

# Function to get a formatted checkmark or fallback
def get_checkmark():
    checkmark = f"✔"
    if platform.system() == 'Windows':
        checkmark = f"+"
    return checkmark

# Example usage with a green checkmark or fallback to a green plus sign
checkmark = get_checkmark()

# Use sys._MEIPASS if running as a PyInstaller executable, otherwise use the script's directory
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
else:
    script_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate the parent directory
parent_dir = os.path.dirname(script_dir)

# define base directory
if getattr(sys, 'frozen', False):
    base_dir = script_dir
else:
    base_dir = parent_dir

def run_function(callback, dumps_path, uniform_slot_name, uniform_type, second_glove, photoshop_pref, pridesticker_pref, helmetnumbers_pref, ssnumbers_pref, only_make_csv):

    # # Output the passed parameters
    # callback(f"Using dumps path: {dumps_path}\n")
    # callback(f"Uniform Slot Name: {uniform_slot_name}\n")
    # callback(f"Uniform Type: {uniform_type}\n")
    # callback(f"Second Glove: {second_glove}\n")
    # callback(f"Photoshop Preference: {photoshop_pref}\n")
    # callback(f"Pride Sticker Preference: {pridesticker_pref}\n")
    # callback(f"Helmet Numbers Preference: {helmetnumbers_pref}\n")
    # callback(f"Sleeve/Shoulder Numbers Preference: {ssnumbers_pref}\n")

    # Define the 'put_textures_here' source folder
    source_folder = os.path.join(base_dir, "YOUR_TEXTURES_HERE")

    # Define the 'renamed' folder
    renamed_folder = os.path.join(base_dir, "RENAMED")

    # Define the 'default textures' folder
    default_textures_folder = os.path.join(base_dir, "utils", "default-textures")

    # Define the CSV input folder
    csv_folder = os.path.join(base_dir, "csv-override")

      # Add a line break 
      # Add a line break 
    callback("\n")
    callback("\n")
    callback("#####################################################################\n")
    callback("#                                                                   #\n")
    callback("#       NCAA NEXT Uniform Expansion Texture Renaming Utility        #\n")
    callback("#                                                                   #\n")
    callback("#                     Mode 1: CSV Renaming                          #\n")
    callback("#                                                                   #\n")
    callback("#####################################################################\n\n")

    if os.path.isdir(csv_folder):
        csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    else:
        csv_files = []

    # Configuration settings stage...

    callback(f"+++++++++++++++++++++++ CONFIGURATION SETTINGS +++++++++++++++++++++++\n\n", "blue") 

    # Photshop or Photopea (must rename files if photopea)
    if not photoshop_pref:
        callback(f"{Fore.YELLOW}[!] The PHOTOSHOP/PHOTOPEA preference is not defined. Check config.txt and ensure there is a line that reads: 'photoshop_pref = 1'. \n\n")

    if photoshop_pref == '1':
        # Use primary names
        photoshop_pref_output = "PhotoSHOP"
    elif photoshop_pref == '2':
        # Use secondary names
        photoshop_pref_output = "PhotoPEA"
    else:
        callback("Assuming Photoshop naming.\n")

    # Output the value of uniform_type
    callback(f"\n[•] ", "blue")
    callback(f"TEXTURES WERE MADE/NAMED WITH: ==================================#\n")
    callback(f"\n|     └-----→  {photoshop_pref_output} \n", "green")
    if photoshop_pref == '2':
        callback(f"\n|              The files in YOUR_TEXTURES_HERE will be converted to Photoshop names. \n", "green")
    callback(f"\n#ˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉ#\n")
    


    # Function to rename files to photoshop naming convention if made with photopea
    def rename_photopea_files(source_folder, texture_name_mapping, texture_name_mapping_old):
        # Check if img1.png exists
        img1_path = os.path.join(source_folder, 'img1.png')
        
        if os.path.exists(img1_path):
            current_mapping = texture_name_mapping_old
        else:
            current_mapping = texture_name_mapping
        
        for pattern, new_name in current_mapping.items():
            # Find files matching the pattern
            matching_files = glob.glob(os.path.join(source_folder, pattern))
            
            # Process each matching file
            for old_path in matching_files:
                # Extract filename from old_path
                old_name = os.path.basename(old_path)
                new_path = os.path.join(source_folder, new_name)
                
                # Check if the file exists before attempting to rename
                if os.path.exists(old_path):
                    # Rename the file
                    os.rename(old_path, new_path)
                    # callback(f'Renamed {old_name} to {new_name}')
                else:
                    callback(f'WARNING: File not found - {old_name}')

    texture_name_mapping = {
        '*_01.png': '01-TC_Wrist.png',
        '*_03.png': '03-TC_QB_Wrist.png',
        '*_04.png': '04-TC_Thin_Band.png',
        '*_06.png': '06-TC_Face_Protector.png',
        '*_07.png': '07-TC_Med_Band--34_sleeve_top.png',
        '*_10.png': '10-Wt_TC_Pad.png',
        '*_11.png': '11-TC_Half_Sleeve.png',
        '*_13.png': '13-Sock.png',
        '*_14.png': '14-Bk_TC_Pad.png',
        '*_15.png': '15-TC_Long_Sleeve.png',
        '*_16.png': '16-Shoe.png',
        '*_17.png': '17-Shoe_w_White_Tape.png',
        '*_18.png': '18-Facemask_Far.png',
        '*_20.png': '20-Facemask_Near.png',
        '*_22.png': '22-Chinstrap.png',
        '*_23.png': '23-Shoe_w_Black_Tape.png',
        '*_24.png': '24-Shoe_w_TC_Tape.png',
        '*_25.png': '25-TC_Face_Protector_Top.png',
    }
    texture_name_mapping_old = {
        'img1.png': '01-TC_Wrist.png',
        'img3.png': '03-TC_QB_Wrist.png',
        'img4.png': '04-TC_Thin_Band.png',
        'img6.png': '06-TC_Face_Protector.png',
        'img7.png': '07-TC_Med_Band--34_sleeve_top.png',
        'img10.png': '10-Wt_TC_Pad.png',
        'img11.png': '11-TC_Half_Sleeve.png',
        'img13.png': '13-Sock.png',
        'img14.png': '14-Bk_TC_Pad.png',
        'img15.png': '15-TC_Long_Sleeve.png',
        'img16.png': '16-Shoe.png',
        'img17.png': '17-Shoe_w_White_Tape.png',
        'img18.png': '18-Facemask_Far.png',
        'img20.png': '20-Facemask_Near.png',
        'img22.png': '22-Chinstrap.png',
        'img23.png': '23-Shoe_w_Black_Tape.png',
        'img24.png': '24-Shoe_w_TC_Tape.png',
        'img25.png': '25-TC_Face_Protector_Top.png',
    }

    # Functions for other configurations and preferences
    def prompt_user(message):
          # Add a line break
        callback(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}\n")
        # user_input = input("YES (y) or NO (n/Enter): \n").lower()
        # return user_input in ["yes", "y"]

    def prompt_preference(pref_name, question, header_text, answer_yes, extra_yes, answer_no, extra_no):
        if pref_name is not None and pref_name != "":
            pref_value = pref_name
        else:
            pref_value = prompt_user(question)

        answer = answer_yes if pref_value in ['yes', 'y', True] else answer_no

        output = f"{header_text}==================================#"
        callback(f"\n[•] ", "blue")
        callback(f"{output}\n")
        callback(f"\n|     └-----→  {answer}\n", "green")
        if pref_value:
            callback(f"\n|              {extra_yes if answer == answer_yes else extra_no}\n", "green")
        else:
            callback(f"\n|              {extra_yes if answer == answer_yes else extra_no}\n", "green")
        callback(f"\n#ˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉ#\n\n")
        

        return pref_value


    # Pride Stickers
    pridesticker_pref = prompt_preference(pridesticker_pref,
                                          "The helmet PRIDE STICKER preference is not defined in config.txt. \nDoes this uniform use helmet pride stickers? (y / n): ",
                                          "HELMET PRIDE STICKERS?: ========", "YES, the uniform uses helmet pride stickers.",
                                          "Be sure to provide a custom pridesticker.png.",
                                          "NO, the uniform does not use helmet pride stickers.",
                                          "The tool will automatically disable/transparent them.\n")

    # Helmet Numbers
    helmetnumbers_pref = prompt_preference(helmetnumbers_pref,
                                          "The HELMET NUMBERS preference is not defined in config.txt. \nDoes this uniform have numbers on the back or side of the helmet? (y / n): ",
                                          "HELMET NUMBERS?: ================", "YES, the uniform uses helmet numbers.",
                                          "Helmet numbers will be copied (or created from the main numbers).",
                                          "NO, the uniform does not use helmet numbers.",
                                          "Only the name will be recorded in the CSV. No textures will be copied.\n")

    # Sleeve/Shoulder Numbers
    ssnumbers_pref = prompt_preference(ssnumbers_pref,
                                          "The SLEEVE/SHOULDER NUMBERS preference is not defined in config.txt. \nDoes this uniform have numbers on the sleeves or top of the shoulders? (y / n): ",
                                          "SLEEVE/SHOULDER NUMBERS?: ======", "YES, the uniform uses SLEEVE/SHOULDER numbers.",
                                          "SLEEVE/SHOULDER numbers will be copied (or created from the main numbers).",
                                          "NO, the uniform does not use SLEEVE/SHOULDER numbers.",
                                          "Only the name will be recorded in the CSV. No textures will be copied.\n")

    # Function to convert config's string values to booleans
    def convert_to_boolean(value):
        if value is not None:
            return str(value).strip().lower() in ["yes", "true"]
        return False

    # Extract pridesticker_pref from the config
    pridesticker_pref = convert_to_boolean(pridesticker_pref)

    # Extract helmetnumbers_pref from the config
    helmetnumbers_pref = convert_to_boolean(helmetnumbers_pref)

    # Extract ssnumbers_pref from the config
    ssnumbers_pref = convert_to_boolean(ssnumbers_pref)

    # Define the transparent file and check if it exists
    transparent_source_path = os.path.join(default_textures_folder, 'transparent.png')

    # CHECK FOR MISSING DEFAULT TEXTURES
    default_textures_to_check = [
        'transparent.png',
        'wrist_Half_Sleeve_Bk.png',
        'wrist_Half_Sleeve_Wt.png',
        'wrist_QB_Wrist_Bk.png',
        'wrist_QB_Wrist_Wt.png'
    ]

    # Check if all default textures exist
    missing_default_textures = [file for file in default_textures_to_check if not os.path.exists(os.path.join(default_textures_folder, file))]

    if not missing_default_textures:
        callback(f"All necessary default textures exist. ")
        callback(f"{checkmark}\n", "green")
    else:
        callback("\n")
        callback(f"###########################################################\n")
        callback(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
        callback(f"!!! ERROR: ", "red")
        callback(f"The following required source textures are missing from\n")
        callback(f"the default-textures folder (in the utils folder):\n\n")
        for missing_file in missing_default_textures:
            callback(f"- {missing_file}\n")
        callback(f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
        callback(f"###########################################################\n")
        # Pause for a thousand minutes
        time.sleep(1000 * 60)
        
        # input()
        # sys.exit(1)


    # Rename the source files if they were made with photopea
    if photoshop_pref == '2':
        rename_photopea_files(source_folder, texture_name_mapping, texture_name_mapping_old)

    # CHECK FOR MISSING REQUIRED TEXTURES
    required_textures_to_check = [
        '01-TC_Wrist.png',
        '03-TC_QB_Wrist.png',
        '04-TC_Thin_Band.png',
        '06-TC_Face_Protector.png',
        '07-TC_Med_Band--34_sleeve_top.png',
        '10-Wt_TC_Pad.png',
        '11-TC_Half_Sleeve.png',
        '13-Sock.png',
        '14-Bk_TC_Pad.png',
        '15-TC_Long_Sleeve.png',
        '16-Shoe.png',
        '17-Shoe_w_White_Tape.png',
        '18-Facemask_Far.png',
        '20-Facemask_Near.png',
        '22-Chinstrap.png',
        '23-Shoe_w_Black_Tape.png',
        '24-Shoe_w_TC_Tape.png',
        '25-TC_Face_Protector_Top.png',
        'helmet.png',
        'jersey.png',
        'num07.png',
        'num89.png',
        'pants.png'
    ]

    # Check if all required textures exist
    missing_required_textures = [file for file in required_textures_to_check if not os.path.exists(os.path.join(source_folder, file))]

    if not missing_required_textures:
        callback(f"All required textures exist in the YOUR_TEXTURES_HERE folder. ")
        callback(f"{checkmark}\n", "green")
    else:
        callback("\n")
        callback(f"###########################################################\n")
        callback(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
        callback(f"!!! ERROR: ", "red")
        callback(f"The following required source textures are missing from\n")
        callback(f"the YOUR_TEXTURES_HERE folder:\n\n")
        for missing_file in missing_required_textures:
            callback(f"- {missing_file}\n")
        callback(f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
        callback(f"###########################################################\n")
        # Pause for a thousand minutes
        time.sleep(1000 * 60)


    # Initialize a set to store unique texture names from the CSV file
    csv_texture_names = set()

    # Open the CSV file and check for all required textures
    for csv_file in csv_files:
        csv_path = os.path.join(csv_folder, csv_file)

        # Open the CSV file for reading
        with open(csv_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)

            # Skip the header row
            next(csv_reader, None)

            # Extract all unique texture names from the TEXTURES column
            csv_texture_names.update(row[3] for row in csv_reader)

    # Check if all required textures exist in the CSV
    missing_required_textures = [texture for texture in required_textures_to_check if texture not in csv_texture_names]

    if not missing_required_textures:
        callback(f"All required textures exist in the CSV. ")
        callback(f"{checkmark}\n", "green")
        
    else:
        callback("\n")
        callback(f"###########################################################\n")
        callback(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
        callback(f"!!! ERROR: ", "red")
        callback(f"The following required textures are missing from the CSV:\n\n")
        for missing_texture in missing_required_textures:
            callback(f"- {missing_texture}\n")
        callback(f"\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
        callback(f"###########################################################\n")
        # Pause for a thousand minutes
        time.sleep(1000 * 60)


    # Ask the user to press Enter to continue
      # Add a line break 
    callback(f"___\n\n", "blue")
      # Add a line break 
    # callback("\nReview the configuration settings above.\n")
    # callback("If you are ready to proceed, PRESS ENTER to continue.\n")
    # input()  # Add a line break 

      # Add a line break 
    callback("#----------------------------------------------------------#\n")
    callback("#                                                          #\n")
    callback("#                     RESULTS:                             #\n")
    callback("#                                                          #\n")


    # Open the CSV file for the file renaming process
    for csv_file in csv_files:
        csv_path = os.path.join(csv_folder, csv_file)

        # Open the CSV file for reading
        with open(csv_path, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            
            # Skip the header row
            next(csv_reader, None)
            
            # Function to handle the sleeve/shoulder and helmet numbers logic
            def copy_numbers(source_folder, subfolder_path, filename, texture, main_texture):
                source_path = os.path.join(source_folder, texture)
                destination_path = os.path.join(subfolder_path, filename)

                if not os.path.exists(source_path):
                    source_path = os.path.join(source_folder, main_texture)
                    output = f" (using main {main_texture})"
                else:
                    output = ".png"

                shutil.copy2(source_path, destination_path)
                callback(f"{checkmark} ", "green")
                callback(f"{texture}{output} copied and renamed.\n")

            # Iterate over the rows in the CSV file
            for row in csv_reader:
                team_name, slot, type, texture, filename = row  # Assuming 'TYPE' field is not needed

                # Create subfolder path in renamed_folder based on SLOT value
                subfolder_path = os.path.join(renamed_folder, team_name, slot)

                # Ensure the subfolder exists, create it if not
                os.makedirs(subfolder_path, exist_ok=True)

                # Number shadows
                if texture == 'num07shadow.png':
                    num07_shadow_folder = os.path.join(subfolder_path, 'num07-shadow')
                    os.makedirs(num07_shadow_folder, exist_ok=True)
                    transparent_destination_path = os.path.join(num07_shadow_folder, filename)
                    shutil.copy2(transparent_source_path, transparent_destination_path)
                    callback(f"{checkmark} ", "green")
                    callback(f"num07shadow (transparented) copied and renamed.\n")
                elif texture == 'num89shadow.png':
                    num89_shadow_folder = os.path.join(subfolder_path, 'num89-shadow')
                    os.makedirs(num89_shadow_folder, exist_ok=True)
                    transparent_destination_path = os.path.join(num89_shadow_folder, filename)
                    shutil.copy2(transparent_source_path, transparent_destination_path)
                    callback(f"{checkmark} ", "green")
                    callback(f"num89shadow (transparented) copied and renamed.\n")
                
                # Num07ss
                elif texture == 'num07ss.png':
                    if ssnumbers_pref:
                        copy_numbers(source_folder, subfolder_path, filename, 'num07ss.png', 'num07.png')
                    else:
                        callback("- Skipped num07ss.png.\n")
                # Num89ss
                elif texture == 'num89ss.png':
                    if ssnumbers_pref:
                        copy_numbers(source_folder, subfolder_path, filename, 'num89ss.png', 'num89.png')
                    else:
                        callback("- Skipped num89ss.png.\n")
                # Num07helmet
                elif texture == 'num07helmet.png':
                    if helmetnumbers_pref:
                        copy_numbers(source_folder, subfolder_path, filename, 'num07helmet.png', 'num07.png')
                    else:
                        callback("- Skipped num07helmet.png\n")
                # Num89helmet
                elif texture == 'num89helmet.png':
                    if helmetnumbers_pref:
                        copy_numbers(source_folder, subfolder_path, filename, 'num89helmet.png', 'num89.png')
                    else:
                        callback("- Skipped num89helmet.png\n")
                

                # Glove
                elif texture == 'glove.png':
                    if type == "dark":
                        glove_subfolder = "glove-home"
                    else:
                        glove_subfolder = "glove-away"

                    glove_path = os.path.join(source_folder, texture)
                    glove_folder = os.path.join(subfolder_path, glove_subfolder)
                    destination_path = os.path.join(subfolder_path, glove_subfolder, filename)
                    # Check if source_image exists
                    if os.path.exists(glove_path):
                        os.makedirs(glove_folder, exist_ok=True)
                        shutil.copy2(glove_path, destination_path)
                        callback(f"{checkmark} ", "green")
                        callback(f"glove.png copied and renamed.\n")
                    else:
                        # Print error message
                        callback(f"- ", "red")
                        callback(f"Skipped. Glove in CSV but no glove.png source in YOUR_TEXTURES folder.\n")
                
                # Glove Second
                elif texture == 'glove-second.png':
                    if type == "dark":
                        glove_subfolder = "glove-away"
                    else:
                        glove_subfolder = "glove-home"

                    glove_path = os.path.join(source_folder, texture)
                    glove_folder = os.path.join(subfolder_path, glove_subfolder)
                    destination_path = os.path.join(subfolder_path, glove_subfolder, filename)
                    # Check if source_image exists
                    if os.path.exists(glove_path):
                        os.makedirs(glove_folder, exist_ok=True)
                        shutil.copy2(glove_path, destination_path)
                        callback(f"{checkmark} ", "green")
                        callback(f"glove-second.png copied and renamed.\n")
                    else:
                        # Print error message
                        callback(f"- ", "red")
                        callback(f"Skipped. Glove-second in CSV but no glove-second.png source in YOUR_TEXTURES folder.\n")
                      
                        
                
                
                # Pride Sticker
                elif texture == 'pridesticker.png':
                    pridesticker_folder = os.path.join(subfolder_path, 'pride-sticker')
                    os.makedirs(pridesticker_folder, exist_ok=True)
                    if pridesticker_pref:
                        pridesticker_path = os.path.join(source_folder, texture)
                        # Check if source_image exists
                        if os.path.exists(pridesticker_path):
                            pridesticker_source_path = pridesticker_path
                            pridesticker_output = ".png"
                        else:
                            # Print error message
                            
                            callback(f"###########################################################\n")
                            callback(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
                            callback(f"!!! ERROR:", "red")
                            callback(f" You want to use a pride sticker but no pridesticker.png source file exists in YOUR_TEXTURES. Add the source file and try again, or choose 'no' for the Pride Sticker preference next time.\n")
                            callback(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
                            callback(f"###########################################################\n")
                            # Wait for user to press enter
                            callback("Press Enter to exit the program.\n")
                            # input()
                            # sys.exit()
                        
                    else:
                        pridesticker_source_path = os.path.join(default_textures_folder, 'transparent.png')
                        pridesticker_output = " (transparented)"
                    transparent_destination_path = os.path.join(pridesticker_folder, filename)
                    shutil.copy2(pridesticker_source_path, transparent_destination_path)
                    callback(f"{checkmark} ", "green")
                    callback(f"pridesticker{pridesticker_output} copied and renamed.\n")
                
                # All others
                else:     
                    # Default textures
                    default_textures_csv = ['wrist_QB_Wrist_Bk.png', 'wrist_QB_Wrist_Wt.png', 'wrist_Half_Sleeve_Wt.png', 'wrist_Half_Sleeve_Bk.png', 'num07shadow.png', 'num89shadow.png']
                    if texture in default_textures_csv:
                        # Construct source and destination paths for default black and white textures 
                        source_path = os.path.join(default_textures_folder, texture)
                    else:
                        # Construct source path for regular cases
                        source_path = os.path.join(source_folder, texture)

                    # Construct destination path
                    destination_path = os.path.join(subfolder_path, filename)

                    # Copy the file to the destination with the specified filename
                    if os.path.exists(source_path):
                        shutil.copy2(source_path, destination_path)
                        callback(f"{checkmark} ", "green")
                        callback(f"{texture} copied and renamed.\n")
                    else:
                        callback(f"- ", "red")
                        callback(f" {texture} in CSV but no source in YOUR_TEXTURES folder\n")
                        callback("\n")
                        callback(f"###########################################################\n")
                        callback(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
                        callback(f"!!! ERROR: ", "red")
                        callback(f"Missing {texture} in the YOUR_TEXTURES_HERE folder.\n")
                        callback(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
                        callback(f"###########################################################\n")
                        # Delete the incomplete folder
                        if os.path.exists(subfolder_path):
                            shutil.rmtree(subfolder_path)
                        # Pause for a thousand minutes
                        time.sleep(1000 * 60)

    for csv_file in csv_files:
        csv_source_path = os.path.join(csv_folder, csv_file)

        # Create csv subfolder if it doesn't exist
        if not os.path.exists(os.path.join(subfolder_path, "csv-texture-names")):
            os.makedirs(os.path.join(subfolder_path, "csv-texture-names"))
        
        csv_destination_path = os.path.join(subfolder_path, "csv-texture-names", csv_file)  # Adjust the filename accordingly
        
        # Copy the CSV file to the destination with the specified filename
        shutil.copy2(csv_source_path, csv_destination_path)
        
        callback(f"\n{checkmark} ")
        callback(f"CSV file copied to subfolder > csv-texture-names.\n")

    
    # Add a line break 
    callback("\n")
    callback("\n")
    callback("#--------------------------------------------------------------#\n")
    callback(f"#                         ")
    callback(f"SUCCESS!", "green")
    callback(f"                             #\n")
    callback("#             All files were copied and renamed                #\n")
    callback("#                  according to the CSV data.                  #\n")
    callback("#                                                              #\n")
    callback("#       READ ALL OF THE OUTPUT ABOVE TO CHECK FOR ISSUES.      #\n")
    callback("#      Your renamed textures are in a subfolder of RENAMED.    #\n")
    callback("#      The source CSV file was also copied to that folder.     #\n")
    callback("#  Be sure to leave the CSV file in the folder and submit it   #\n")
    callback("#                                                              #\n")
    callback("################################################################\n\n")
      # Add a line break 
      # Add a line break 

    ############################################################################
    def find_duplicate_png_files(folder):
        png_files = {}
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith('.png'):
                    file_path = os.path.join(root, file)
                    if file in png_files:
                        png_files[file].append(file_path)
                    else:
                        png_files[file] = [file_path]
        
        # Filter out files that don't have duplicates
        duplicate_sets = {file: sorted(paths) for file, paths in png_files.items() if len(paths) > 1}

        return duplicate_sets

    folder_to_check = os.path.join(base_dir, "RENAMED")
    duplicate_sets = find_duplicate_png_files(folder_to_check)

    # callback("Checking recursively in the RENAMED folder to ensure all filenames are unique...")
    # callback("\n")

    if duplicate_sets:
        callback("\n")
        callback(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
        callback("******  ")
        callback("WARNING: ", "red")
        callback("Duplicate texture names found!  *******\n")
        callback("*                                                      *\n")
        callback("*     You may have dumped the same uniform twice.      *\n")
        callback("*    Correct it and redump. No two files can have      *\n")
        callback("*        the same name anywhere in replacements.       *\n")
        callback("*                                                      *\n")
        for idx, (filename, paths) in enumerate(duplicate_sets.items(), start=1):
            callback(f"\nDuplicate Set {idx}:\n")
            for path in paths:
                callback(path)
                callback("\n")  
        callback("\n")
        callback("\n")
        callback(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
        callback("******  ")
        callback("WARNING: ", "red")
        callback("Duplicate texture names found!  *******\n")
        callback("*                                                      *\n")
        callback("*     You may have dumped the same uniform twice.      *\n")
        callback("*    Correct it and redump. No two files can have      *\n")
        callback("*        the same name anywhere in replacements.       *\n")
        callback("*                                                      *\n")
        callback("********************************************************\n")
        callback(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", "red")
    else:
        callback("Passed duplicate PNG files check. All filenames in RENAMED are unique.\n")
