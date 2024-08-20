from PIL import Image
import imagehash
import shutil
import cv2
import os
import sys
import csv
import platform
import glob
from skimage.metrics import structural_similarity as compare_ssim
from colorama import init, Fore, Style
init()  # initialize colorama for ANSI color codes in Windows

# Function to get a formatted checkmark or fallback
def get_checkmark():
    checkmark = f"{Fore.GREEN}✔{Style.RESET_ALL}"
    if platform.system() == 'Windows':
        checkmark = f"{Fore.GREEN}+{Style.RESET_ALL}"
    return checkmark

# Example usage with a green checkmark or fallback to a green plus sign
checkmark = get_checkmark()

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

# Extract the second_glove from the config
second_glove = config_content.get('second_glove', None)

# Extract the photoshop_pref from the config
photoshop_pref = config_content.get('photoshop_pref', None)

# Extract the pridesticker_pref from the config
pridesticker_pref = config_content.get('pridesticker_pref', None)
# Extract the helmetnumbers_pref from the config
helmetnumbers_pref = config_content.get('helmetnumbers_pref', None)
# Extract the ssnumbers_pref from the config
ssnumbers_pref = config_content.get('ssnumbers_pref', None)

# Define the 'put_textures_here' source folder
source_folder = os.path.join(script_dir, "YOUR_TEXTURES_HERE")

# Define the 'renamed' folder
renamed_folder = os.path.join(script_dir, "RENAMED")

# Define the 'default textures' folder
default_textures_folder = os.path.join(script_dir, "default-textures")

# Define the CSV input folder
csv_folder = os.path.join(script_dir, "csv-override")

print()  # Add a line break 
print()  # Add a line break 
print("#####################################################################")
print("#                                                                   #")
print("#       NCAA NEXT Uniform Expansion Texture Renaming Utility        #")
print("#                                                                   #")
print("#                     Version: 0.6-beta                             #")
print("#                                                                   #")
print("#####################################################################")

if os.path.isdir(csv_folder):
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
else:
    csv_files = []

if len(csv_files) > 1:
    print()  # Add a line break 
    print()  # Add a line break 
    print(f"{Fore.RED}!!!!!!!! ERROR:{Style.RESET_ALL} A CSV override has been provided, but there are multiple CSV files in the csv-override directory. Keep one and remove the others, or remove them all to perform automatic texture matching in your dumps folder.")
    print()  # Add a line break 
    input("Press Enter to exit...")
    sys.exit()
elif len(csv_files) == 1:
    csv_provided = True
    print()  # Add a line break 
    print()  # Add a line break 
    print(f"{Fore.GREEN}CSV override provided.{Style.RESET_ALL} Skipping image matching. Renaming using the filenames in the CSV.")
    print()  # Add a line break 
    print(f"{Fore.BLUE}IMPORTANT:{Style.RESET_ALL} Be sure to format your CSV exactly like the included example (csv-override-example.csv). The TEXTURE column must be the third column, and its contents must be as shown in the example – the names of the source textures with '.png'. The fourth column, 'FILENAME', must contain the names to which the textures will be renamed. ")
else:
    csv_provided = False
    print()  # Add a line break 
    print()  # Add a line break 
    print("No CSV Override provided. Proceeding with automatic image matching...")

# Configuration settings stage...

print()  # Add a line break 
print()  # Add a line break 
print(f"{Fore.BLUE}+++++++++++++++++++++++ CONFIGURATION SETTINGS +++++++++++++++++++++++{Style.RESET_ALL}") 
print()  # Add a line break 
print("You can define these in the config.txt file.") 
print()  # Add a line break 

# Config settings for only the image matching method
if len(csv_files) != 1:
  # Check if dumps_path is not defined or the folder does not exist
  if not dumps_path or not os.path.exists(dumps_path):
      # Prompt the user to enter a path
      print()  # Add a line break 
      print(f"{Fore.YELLOW}[!] The path to the DUMPS FOLDER is not defined in config.txt or does not exist.")
      print(r"Enter the full path to the dumps folder (Eg. C:\PCSX2\textures\SLUS-21214\dumps): ")
      print(f"{Style.RESET_ALL} ")
      user_input_path = input("full path: ")
      
      # Validate if the entered path exists
      while not os.path.exists(user_input_path):
          print()  # Add a line break 
          print(f"{Fore.RED}ERROR:{Style.RESET_ALL} The specified folder does not exist. Please enter a valid path.")
          user_input_path = input("Enter the path to the DUMPS FOLDER: ")

      # Use the user's input for dumps_path
      dumps_path = user_input_path

  # Output the value of dumps_path
  print(f"\n{Fore.BLUE}[•]{Style.RESET_ALL}  DUMPS FOLDER is defined and confirmed to exist at: ==============#")
  print(f"\n|     └-----→  {Fore.GREEN}{dumps_path}{Style.RESET_ALL}")
  print(f"\n#ˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉ#")
  print()  # Add a line break 


  # Check if uniform_slot_name is not defined or the folder does not exist
  if not uniform_slot_name:
      # Prompt the user to enter a path
      print()  # Add a line break 
      print(f"{Fore.YELLOW}[!] The UNIFORM SLOT NAME is not defined in config.txt.")
      print("Enter the name in the format of teamname-slotname (Eg. appstate-alt03, appstate-home, etc.): ")
      print(f"{Style.RESET_ALL} ")
      uniform_slot_name = input("teamname-slotname: ")
  # Output the value of uniform_slot_name
  print(f"\n{Fore.BLUE}[•]{Style.RESET_ALL}  UNIFORM SLOT NAME is defined as: ================================#")    
  print(f"\n|     └-----→  {Fore.GREEN}{uniform_slot_name}{Style.RESET_ALL} ")
  print(f"\n#ˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉ#")
  print()  # Add a line break 

  # Check if uniform_type is not defined 
  if not uniform_type:
      # Prompt the user to enter a path
      print()  # Add a line break 
      print(f"{Fore.YELLOW}[!] The UNIFORM TYPE is not defined in config.txt. \nAre you making a dark uniform or a light uniform? (dark/light):{Style.RESET_ALL}")
      uniform_type = input("dark or light: ")
  # Add a condition to check the uniform type and set the appropriate path
  if uniform_type.lower() == 'dark':
      uniform_type_output = "DARK"
      reference_folder = "reference-dark"
  elif uniform_type.lower() == 'light':
      uniform_type_output = "LIGHT"
      reference_folder = "reference-light"
  else:
      uniform_type_output = "Invalid input. Assuming DARK uniform."
      reference_folder = "reference-dark"
  # Output the value of uniform_type
  print(f"\n{Fore.BLUE}[•]{Style.RESET_ALL} UNIFORM TYPE is: =================================================#")
  print(f"\n|     └-----→  {Fore.GREEN}{uniform_type_output}{Style.RESET_ALL} ")
  print(f"\n#ˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉ#")
  # Output the selected default textures folder
  print(f" └→ The reference folder for the {uniform_type} uniform is set to: {reference_folder}. Feel free to put your actual dumped textures in here (or its alts subfolder) if the image matching utility is having trouble finding a match.")
  print()  # Add a line break 

  # Check if second_glove is not defined 
  if not second_glove:
      # Prompt the user to enter a path
      print()  # Add a line break 
      print(f"{Fore.YELLOW}[!] The GLOVE TYPE is not defined in config.txt. \nAre you dumping the second glove? Answer 'no' if you don't know what this means. (yes/no):{Style.RESET_ALL}")
      second_glove = input("yes or no: ")
  # Add a condition to check the uniform type and set the appropriate path
  if second_glove.lower() == 'no':
      second_glove_output = "NORMAL (not the second glove)"
      reference_glove = "glove"
  elif second_glove.lower() == 'yes':
      second_glove_output = "SECOND GLOVE (dark uniform as vistor OR light uniform as home team)"
      reference_glove = "glove-second"
  else:
      second_glove_output = "Invalid input. Assuming normal glove."
      reference_glove = "glove"
  # Output the value of second_glove
  print(f"\n{Fore.BLUE}[•]{Style.RESET_ALL} GLOVE TYPE is: =================================================#")
  print(f"\n|     └-----→  {Fore.GREEN}{second_glove_output}{Style.RESET_ALL} ")
  print(f"\n#ˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉ#")
  # Output the selected default textures folder
  print(f" └→ The dumps finder will look for a dumped match with {reference_glove}.png in the '{reference_folder}' folder. It will rename your glove of the same name.")
  if second_glove.lower() == 'yes':
    print(f" └→ THIS IS THE ONLY TEXTURE THAT WILL BE PROCESSED. Change this setting to 'yes' to do the rest of the uniform.")
  print()  # Add a line break 



# Simplify the glove boolean
glove_normal_or_csv = csv_provided or (not csv_provided and second_glove.lower() != 'yes')


# General Config Settings for both methods
if glove_normal_or_csv:

    # Photshop or Photopea (must rename files if photopea)
    if not photoshop_pref:
        # Prompt the user to enter a path
        print()  # Add a line break 
        print(f"{Fore.YELLOW}[!] The PHOTOSHOP/PHOTOPEA preference is not defined in config.txt. \nWere the TC Gear textures exported from Photoshop or PhotoPea? :{Style.RESET_ALL}")
        print()
        print("1. Photoshop (files named: 01-TC_Wrist.png, 03-TC_QB_Wrist.png, etc.)")
        print("2. PhotoPea (files named: img1.png, img3.png, etc.)")
        print()

        # Prompt the user to choose a numbered option
        print("Enter the number of your choice: ")
        photoshop_pref = input(": ")

    # Choose the appropriate mapping based on user choice
    if photoshop_pref == '1':
        # Use primary names
        photoshop_pref_output = "PhotoSHOP"
    elif photoshop_pref == '2':
        # Use secondary names
        photoshop_pref_output = "PhotoPEA"
        # run renaming function after the user presses enter 
    else:
        print("Invalid choice. Assuming Photoshop naming.")

    # Output the value of uniform_type
    print(f"\n{Fore.BLUE}[•]{Style.RESET_ALL} TEXTURES WERE MADE/NAMED WITH: ==================================#")
    print(f"\n|     └-----→  {Fore.GREEN}{photoshop_pref_output}{Style.RESET_ALL} ")
    if photoshop_pref == '2':
        print(f"\n|              {Fore.GREEN}The files in YOUR_TEXTURES_HERE will be converted to Photoshop names.{Style.RESET_ALL} ")
    print(f"\n#ˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉ#")
    print()


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
                    # print(f'Renamed {old_name} to {new_name}')
                else:
                    print(f'WARNING: File not found - {old_name}')

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
        print()  # Add a line break
        print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")
        user_input = input("YES (y) or NO (n/Enter): ").lower()
        return user_input in ["yes", "y"]

    def prompt_preference(pref_name, question, header_text, answer_yes, extra_yes, answer_no, extra_no):
        if pref_name is not None and pref_name != "":
            pref_value = pref_name
        else:
            pref_value = prompt_user(question)

        answer = answer_yes if pref_value in ['yes', 'y', True] else answer_no

        output = f"{header_text}==================================#"
        print(f"\n{Fore.BLUE}[•]{Style.RESET_ALL} {output}")
        print(f"\n|     └-----→  {Fore.GREEN}{answer}{Style.RESET_ALL}")
        if pref_value:
            print(f"\n|              {Fore.GREEN}{extra_yes if answer == answer_yes else extra_no}{Style.RESET_ALL}")
        else:
            print(f"\n|              {Fore.GREEN}{extra_yes if answer == answer_yes else extra_no}{Style.RESET_ALL}")
        print(f"\n#ˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉˉ#")
        print()

        return pref_value


    # Pride Stickers
    pridesticker_pref = prompt_preference(pridesticker_pref,
                                          "The helmet PRIDE STICKER preference is not defined in config.txt. \nDoes this uniform use helmet pride stickers? (y / n): ",
                                          "HELMET PRIDE STICKERS?: ========", "YES, the uniform uses helmet pride stickers.",
                                          "Be sure to provide a custom pridesticker.png.",
                                          "NO, the uniform does not use helmet pride stickers.",
                                          "The tool will automatically disable/transparent them.")

    # Helmet Numbers
    helmetnumbers_pref = prompt_preference(helmetnumbers_pref,
                                          "The HELMET NUMBERS preference is not defined in config.txt. \nDoes this uniform have numbers on the back or side of the helmet? (y / n): ",
                                          "HELMET NUMBERS?: ================", "YES, the uniform uses helmet numbers.",
                                          "Helmet numbers will be copied (or created from the main numbers).",
                                          "NO, the uniform does not use helmet numbers.",
                                          "Only the name will be recorded in the CSV. No textures will be copied.")

    # Sleeve/Shoulder Numbers
    ssnumbers_pref = prompt_preference(ssnumbers_pref,
                                          "The SLEEVE/SHOULDER NUMBERS preference is not defined in config.txt. \nDoes this uniform have numbers on the sleeves or top of the shoulders? (y / n): ",
                                          "SLEEVE/SHOULDER NUMBERS?: ======", "YES, the uniform uses SLEEVE/SHOULDER numbers.",
                                          "SLEEVE/SHOULDER numbers will be copied (or created from the main numbers).",
                                          "NO, the uniform does not use SLEEVE/SHOULDER numbers.",
                                          "Only the name will be recorded in the CSV. No textures will be copied.")

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

############################################################################
# IMAGE MATCHING IF NO CSV OVERRIDE PROVIDED
if csv_provided == False:

    if glove_normal_or_csv:
        # Pre-run Checklist
        print()  # Add a line break 
        print()  # Add a line break 
        print(f"{Fore.BLUE}++++++++++++++++++++++++++ PRE-RUN CHECKLIST ++++++++++++++++++++++++++{Style.RESET_ALL}")
        print()  # Add a line break 
        print("Before we begin, your dumps folder is expected to contain all 30-34 dumped textures")
        print("for your chosen uniform type (light/dark). To dump all of these, you must have: ")
        print()  # Add a line break 
        print(" • Used the dumps ISO not the dev ISO or the normal mod ISO (so all numbers get dumped)")
        print(" • Reset your rosters to that of the ISO default (so all gear gets used)")
        print(" • Set the game weather to cold (so the Face Protector is worn)")
        print(" • Deleted everything in your dumps folder during the game loading screen (after the uniform")
        print("   selection screen and prior to the coin toss)")
        print(" • Dumped during the coin toss (so the Face Protector top piece can dump)")
        print(" • Run at least one play from scrimmage (not just the kickoff)")
        print(" • Either let the the pre-game onfield presentation run its course OR have zoomed in close")
        print("   during an instant replay (so the facemask near textures can dump)")
        print()  # Add a line break 
        print("If you didn't do all of the things above when dumping the textures, your dumps folder")
        print("probably does not contain all of the required textures, and you should exit now (by")
        print("closing this window), delete the contents of the dumps folder, and do the dump again.")
    else:
        # Pre-run Checklist
        print()  # Add a line break 
        print()  # Add a line break 
        print(f"{Fore.BLUE}++++++++++++++++++++++++++ PRE-RUN CHECKLIST ++++++++++++++++++++++++++{Style.RESET_ALL}")
        print()  # Add a line break 
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
        print("!!!!!!!!!  NOTE: YOU HAVE DEFINED the glove type as 'second glove'. !!!!!!!!! ")
        print("!!!!!!!!!!!!!!!  ALL OTHER UNIFORM TEXTURES WILL BE SKIPPED.  !!!!!!!!!!!!!!! ")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
        print("Before we begin, make sure that you chose the right setting or the wrong texture")
        print("will be matched. Only proceed if you have done one of the following: ")
        print()
        print(" • If this is a LIGHT uniform, it is the HOME team")
        print(" OR ")
        print(" • If this is a DARK uniform, it is the VISITING team")
      
      



    # Ask the user to press Enter to continue
    print()  # Add a line break 
    print(f"{Fore.BLUE}___{Style.RESET_ALL}")
    print()  # Add a line break 
    print("Review the configuration settings and checklist above.")
    print("If you are ready to proceed, PRESS ENTER to continue.")
    input()  # Add a line break 

    print()  # Add a line break 
    print("#----------------------------------------------------------#")
    print("#                                                          #")
    print("#                     RESULTS:                             #")
    print("#                                                          #")


    if glove_normal_or_csv:
        # Rename the source files if they were made with photopea
        if photoshop_pref == '2':
            rename_photopea_files(source_folder, texture_name_mapping, texture_name_mapping_old)

    # Extract the first segment of uniform_slot_name
    if '-' in uniform_slot_name:
        teamname = uniform_slot_name.split('-')[0]
    else:
        teamname = uniform_slot_name

    # Extract the second segment of uniform_slot_name
    if '-' in uniform_slot_name:
        slotname = uniform_slot_name.split('-')[1]
    else:
        slotname = uniform_slot_name

    # Open a CSV file for writing
    csv_filename = f"textures-{uniform_slot_name}.csv"

    # Extract the second segment of uniform_slot_name for the subfolder
    if '-' in uniform_slot_name:
        renamed_subfolder = uniform_slot_name.split('-')[1]
    else:
        renamed_subfolder = uniform_slot_name
    
    # Define the full path for the renamed folder and the destination CSV folder
    renamed_folder = os.path.join(script_dir, "RENAMED")
    csv_destination_folder = os.path.join(renamed_folder, renamed_subfolder, "csv-texture-names")

    # Ensure the destination folder exists
    if glove_normal_or_csv:
        if not os.path.exists(csv_destination_folder):
            os.makedirs(csv_destination_folder)

    # Define the full path to the CSV file in the destination folder
    csv_file_path = os.path.join(csv_destination_folder, csv_filename)

    # Determine the file mode based on the value of glove_normal_or_csv
    if glove_normal_or_csv:
        # Open the CSV file in write mode ('w')
        file_mode = 'w'
    else:
        # Check if the file exists
        if os.path.isfile(csv_file_path):
            # If the file exists, use append mode ('a')
            file_mode = 'a'
        else:
            # If the file doesn't exist, print an error message and exit
            print(f"ERROR: The file {csv_filename} does not exist. You must first run this tool with glove_second set to 'no' and keep the folder it makes in RENAMED.")
            input("Press Enter to exit...")  # Pause before exiting
            sys.exit(1)

    # Open the CSV file with the determined mode
    with open(csv_file_path, mode=file_mode, newline='') as csvfile:
        fieldnames = ['TEAM NAME', 'SLOT', 'TYPE', 'TEXTURE', 'FILENAME']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is opened in write mode ('w')
        if file_mode == 'w':
            csv_writer.writeheader()

        # Function to calculate hash_tolerance_for_pass
        def calculate_hash_tolerance(reference_hash_phash, compared_hash_phash, reference_hash_dhash, compared_hash_dhash):
            return max(
                abs(reference_hash_phash - compared_hash_phash),
                abs(reference_hash_dhash - compared_hash_dhash)
            )

        # function to get all files in a directory
        def get_all_png_files_in_directory(directory):
            return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith(".png")]

        # Using a few different methods for comparing files to find the matching dumped texture
        def find_similar_images(reference_image_path, dumps_path, file_params=None, context=None):
                                
            # # Construct the correct path for the reference image
            # if context:
            #   reference_image_path = os.path.join(script_dir, reference_folder, 'alts', source_image)
            # else:
            #   reference_image_path = os.path.join(script_dir, reference_folder, source_image)

            # Extract the directory containing the reference image
            reference_directory = os.path.dirname(reference_image_path)

            try:
                reference_image = Image.open(reference_image_path)
            except FileNotFoundError:
                print()
                print()
                print(f"{Fore.RED}!!!!!!!! ERROR:{Style.RESET_ALL}  Missing reference file at: {reference_image_path}")
                return []  # or handle the error as needed
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
            "glove-second.png": {"source": "glove-second.png", "hash_tolerance": config_content.get('hash_tolerance_glove'), "ssim_threshold": config_content.get('ssim_threshold_glove')},
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
            "num89ss.png": {"source": "num89ss.png", "hash_tolerance": config_content.get('hash_tolerance_num89ss'), "ssim_threshold": config_content.get('ssim_threshold_num89ss')},
            "glove.png": {"source": "glove.png", "hash_tolerance": config_content.get('hash_tolerance_glove'), "ssim_threshold": config_content.get('ssim_threshold_glove')}
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
            print(f"{Fore.BLUE}[•]{Style.RESET_ALL} Dumped texture found for {file}:")
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
                            # Create subfolder if it doesn't exist
                            if not os.path.exists(os.path.join(renamed_folder, renamed_subfolder)):
                                os.makedirs(os.path.join(renamed_folder, renamed_subfolder))
                            # Copy a transparent to the 'renamed' folder and rename 
                            new_file_name = f"{found_filename_base}.png"

                            try:
                                # Attempt to copy the file
                                shutil.copy(os.path.join(default_textures_folder, "transparent.png"), os.path.join(renamed_folder, renamed_subfolder, new_file_name))
                                print("NUMBER SHADOW TRANSPARENTED")
                                print(f"{checkmark} SUCCESS. Transparent renamed and filename added to the CSV file.")
                                required_textures_counter += 1
                                # Write to the CSV file
                                csv_writer.writerow({'TEAM NAME': teamname, 'SLOT': slotname, 'TYPE': uniform_type, 'TEXTURE': file, 'FILENAME': new_file_name})
                            except FileNotFoundError:
                                # Handle the FileNotFoundError gracefully
                                print(f"{Fore.RED}FileNotFoundError: {Style.RESET_ALL}File not found: {os.path.join(source_folder, source_image)}")
                                print(f"{Fore.RED}Message: {Style.RESET_ALL}The file required for processing is missing.")



                # Glove
                elif file == "glove.png":
                    new_file_name = f"{found_filename}.png"
                    # Create glove subfolder if it doesn't exist
                    if uniform_type == "dark":
                        glove_folder = "glove-home"
                    else:
                        glove_folder = "glove-away"
                    glove_path = os.path.join(source_folder, source_image)
                    # Check if source_image exists
                    if os.path.exists(glove_path):
                        if not os.path.exists(os.path.join(renamed_folder, glove_folder)):
                            os.makedirs(os.path.join(renamed_folder, glove_folder))
                        # Copy and rename glove.png
                        shutil.copy(glove_path, os.path.join(renamed_folder, glove_folder, new_file_name))
                        # Write to the CSV file
                        csv_writer.writerow({'TEAM NAME': teamname, 'SLOT': slotname, 'TYPE': uniform_type, 'TEXTURE': file, 'FILENAME': new_file_name})
                        print(f"{checkmark} SUCCESS. Texture renamed and filename added to the CSV file.")
                        optional_textures_counter += 1
                    else:
                        print("NO GLOVE SOURCE FILE FOUND. SKIPPING RENAMING.")
                        # Write to the CSV file
                        csv_writer.writerow({'TEAM NAME': teamname, 'SLOT': slotname, 'TYPE': uniform_type, 'TEXTURE': file, 'FILENAME': new_file_name})
                        print(f"{checkmark} SUCCESS. Filename added to the CSV file. No texture used.")
                
                # Second Glove
                elif file == "glove-second.png":
                    new_file_name = f"{found_filename}.png"
                    # Create glove subfolder if it doesn't exist
                    if uniform_type == "dark":
                        glove_folder = "glove-away"
                    else:
                        glove_folder = "glove-home"
                    glove_path = os.path.join(source_folder, source_image)
                    # Check if source_image exists
                    if os.path.exists(glove_path):
                        if not os.path.exists(os.path.join(renamed_folder, glove_folder)):
                            os.makedirs(os.path.join(renamed_folder, glove_folder))
                        # Copy and rename glove.png
                        shutil.copy(glove_path, os.path.join(renamed_folder, glove_folder, new_file_name))
                        # Write to the CSV file
                        csv_writer.writerow({'TEAM NAME': teamname, 'SLOT': slotname, 'TYPE': uniform_type, 'TEXTURE': file, 'FILENAME': new_file_name})
                        print(f"{checkmark} SUCCESS. Texture renamed and filename added to the CSV file.")
                        required_textures_counter += 1
                    else:
                        # Print error message
                        print()
                        print(f"###########################################################")
                        print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
                        print(f"{Fore.RED}!!! ERROR:{Style.RESET_ALL} No file named glove-second.png exists in YOUR_TEXTURES. Add the source file and try again.")
                        print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
                        print(f"###########################################################")
                        # Wait for user to press enter
                        print("Press Enter to exit the program.")
                        input()
                        sys.exit()

                
                # If answered yes to transparent pride sticker, copy the transparent image instead of a source image
                elif file == "pridesticker.png":
                    new_file_name = f"{found_filename}.png"
                    # Create Pride Sticker subfolder if it doesn't exist
                    if not os.path.exists(os.path.join(renamed_folder, "pride-sticker")):
                        os.makedirs(os.path.join(renamed_folder, "pride-sticker"))
                    if pridesticker_pref:
                        pridesticker_path = os.path.join(source_folder, source_image)
                        # Check if source_image exists
                        if os.path.exists(pridesticker_path):
                            # Copy and rename pridesticker.png folder and rename 
                            shutil.copy(pridesticker_path, os.path.join(renamed_folder, "pride-sticker", new_file_name))
                            # Write to the CSV file
                            csv_writer.writerow({'TEAM NAME': teamname, 'SLOT': slotname, 'TYPE': uniform_type, 'TEXTURE': file, 'FILENAME': new_file_name})
                            print(f"{checkmark} SUCCESS. Texture renamed and filename added to the CSV file.")
                            required_textures_counter += 1
                        else:
                            # Print error message
                            print()
                            print(f"###########################################################")
                            print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
                            print(f"{Fore.RED}!!! ERROR:{Style.RESET_ALL} You want to use a pride sticker but no pridesticker.png source file exists in YOUR_TEXTURES. Add the source file and try again, or choose 'no' for the Pride Sticker preference next time.")
                            print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
                            print(f"###########################################################")
                            # Wait for user to press enter
                            print("Press Enter to exit the program.")
                            input()
                            sys.exit()
                    else: 
                        # Copy a transparent to the 'renamed' folder and rename 
                        shutil.copy(os.path.join(default_textures_folder, "transparent.png"), os.path.join(renamed_folder, "pride-sticker", new_file_name))
                        print("PRIDE STICKER TRANSPARENTED")
                        # Write to the CSV file
                        csv_writer.writerow({'TEAM NAME': teamname, 'SLOT': slotname, 'TYPE': uniform_type, 'TEXTURE': file, 'FILENAME': new_file_name})
                        print(f"{checkmark} SUCCESS. Transparent texture renamed and filename added to the CSV file.")
                        required_textures_counter += 1
                
                # HELMET AND SLEEVE/SHOULDER NUMBERS
                secondary_numbers = ["num07helmet.png", "num89helmet.png", "num07ss.png", "num89ss.png"]
                if os.path.basename(file) in secondary_numbers:
                  numbers_filename = os.path.basename(file)
                  numbers_file = os.path.join(source_folder, os.path.basename(file))
                  
                  # determine if 07 or 89
                  if numbers_filename == "num07helmet.png" or numbers_filename == "num07ss.png":
                      numbers_main = "num07.png"
                  elif numbers_filename == "num89helmet.png" or numbers_filename == "num89ss.png":
                      numbers_main = "num89.png"
                  
                  # determine if helmet or ss
                  if numbers_filename == "num07helmet.png" or numbers_filename == "num89helmet.png":
                      numbers_type = "helmet"
                  elif numbers_filename == "num07ss.png" or numbers_filename == "num89ss.png":
                      numbers_type = "ss"
                  
                  #check if there is a specific texture provided for the helmet numbers
                  if os.path.exists(numbers_file):
                      new_file_name = f"{found_filename}.png"
                      if helmetnumbers_pref and numbers_type == "helmet":
                          shutil.copy(numbers_file, os.path.join(renamed_folder, new_file_name))
                          success_msg = "Texture renamed and filename added to the CSV file."
                          optional_textures_counter += 1
                      elif ssnumbers_pref and numbers_type == "ss":
                          shutil.copy(numbers_file, os.path.join(renamed_folder, new_file_name))
                          success_msg = "Texture renamed and filename added to the CSV file."
                          optional_textures_counter += 1
                      else:
                          success_msg = "Filename added to the CSV file. No texture used."
                      # Write to the CSV file
                      csv_writer.writerow({'TEAM NAME': teamname, 'SLOT': slotname, 'TYPE': uniform_type, 'TEXTURE': file, 'FILENAME': new_file_name})
                      print(f"{checkmark} SUCCESS. {success_msg}")
                  
                  # If no helmet or sleeve/shoulder numbers are provided, use the main jersey numbers
                  else:
                      new_file_name = f"{found_filename}.png"
                      is_success = False
                      if helmetnumbers_pref and numbers_type == "helmet":
                          try:
                              shutil.copy(os.path.join(source_folder, numbers_main), os.path.join(renamed_folder, new_file_name))
                              success_msg = "Texture (used main numbers) renamed and filename added to the CSV file."
                              optional_textures_counter += 1
                              is_success = True
                          except FileNotFoundError:
                              # Handle the FileNotFoundError gracefully
                              print(f"{Fore.RED}FileNotFoundError: {Style.RESET_ALL}File not found: {os.path.join(source_folder, source_image)}")
                              success_msg = f"{Fore.RED}Message: {Style.RESET_ALL}The source file {source_image} is missing."
                      elif ssnumbers_pref and numbers_type == "ss":
                          try:
                              shutil.copy(os.path.join(source_folder, numbers_main), os.path.join(renamed_folder, new_file_name))
                              success_msg = "Texture (used main numbers) renamed and filename added to the CSV file."
                              optional_textures_counter += 1
                              is_success = True
                          except FileNotFoundError:
                              # Handle the FileNotFoundError gracefully
                              print(f"{Fore.RED}FileNotFoundError: {Style.RESET_ALL}File not found: {os.path.join(source_folder, source_image)}")
                              success_msg = f"{Fore.RED}Message: {Style.RESET_ALL}The source file {source_image} is missing."
                      else:
                          success_msg = "Filename added to the CSV file. No texture used."
                      # Write to the CSV file
                      csv_writer.writerow({'TEAM NAME': teamname, 'SLOT': slotname, 'TYPE': uniform_type, 'TEXTURE': file, 'FILENAME': new_file_name})
                      if is_success:
                        print(f"{checkmark} SUCCESS. {success_msg}")
                      else:
                        print(f"{success_msg}")

                
                # Everything else
                elif file not in ["num07shadow.png", "num89shadow.png", "num07helmet.png", "num07ss.png", "num89helmet.png", "num89ss.png", "pridesticker.png", "glove.png", "glove-second.png"]:
                  if file in ["wrist_Half_Sleeve_Bk.png", "wrist_Half_Sleeve_Wt.png", "wrist_QB_Wrist_Bk.png", "wrist_QB_Wrist_Wt.png"]:
                      # Copy from os.path.join(script_dir, reference_folder) for specific files
                      new_file_name = f"{found_filename}.png"
                      shutil.copy(os.path.join(default_textures_folder, source_image), os.path.join(renamed_folder, new_file_name))
                      # Write to the CSV file
                      csv_writer.writerow({'TEAM NAME': teamname, 'SLOT': slotname, 'TYPE': uniform_type, 'TEXTURE': file, 'FILENAME': new_file_name})
                      print(f"{checkmark} SUCCESS. Texture renamed and filename added to the CSV file.")
                      required_textures_counter += 1
                  else:
                      try:
                          # Copy from source_folder for other files
                          new_file_name = f"{found_filename}.png"
                          shutil.copy(os.path.join(source_folder, source_image), os.path.join(renamed_folder, new_file_name))
                          # Write to the CSV file
                          csv_writer.writerow({'TEAM NAME': teamname, 'SLOT': slotname, 'TYPE': uniform_type, 'TEXTURE': file, 'FILENAME': new_file_name})
                          print(f"{checkmark} SUCCESS. Texture renamed and filename added to the CSV file.")
                          required_textures_counter += 1
                      except FileNotFoundError:
                          # Handle the FileNotFoundError gracefully
                          print(f"{Fore.RED}FileNotFoundError: {Style.RESET_ALL}File not found: {os.path.join(source_folder, source_image)}")
                          print(f"{Fore.RED}Message: {Style.RESET_ALL}The source file {source_image} is missing.")


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
              print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
              print(f"{Fore.BLUE}[•]{Style.RESET_ALL} ==== NO similar images found for {file}. Are you sure the texture dumped? If so...try raising the hash_tolerance to 2 or more and/or lowering the ssim_threshold for this item in config.txt to broaden the search. Alternatively, you can replace the reference texture with the actual dumped texture for a definite match. ====")
              print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
              print(f"###########################################################")
            if file in ["13-Sock.png"]:
              print(f"###########################################################")
              print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
              print(f"{Fore.BLUE}[•]{Style.RESET_ALL} ==== NO similar images found for {file}. Are you sure the texture dumped? If so...the light uniform's sock is a particularly troublesome texture. The only solution is go find the actual dumped texture in your dumps folder, and then add it to the ALTS-SOCK folder inside the REFERENCE-LIGHT directory (or, if a dark uniform, in the REFERENCE-DARK directory). You don't need to rename it. Also, please ping @JD637 on Discord with this sock texture attached so he can add it to the tool for others.  ====")
              print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
              print(f"###########################################################")
            elif file in ["num07helmet.png", "num89helmet.png"]:
              print(f"{Fore.BLUE}[•]{Style.RESET_ALL} ==== No similar images found for {file}. This is okay if helmet numbers are disabled in this uniform slot. ====")
            elif file in ["num07ss.png", "num89ss.png"]:
              print(f"{Fore.BLUE}[•]{Style.RESET_ALL} ==== No similar images found for {file}. This is okay if sleeve/shoulder numbers are disabled in this uniform slot. ====")
            else:
              print(f"###########################################################")
              print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
              print(f"{Fore.BLUE}[•]{Style.RESET_ALL} ==== NO similar images found for {file}. Are you sure the texture dumped? If so...try raising the hash_tolerance and/or lowering the ssim_threshold for this item in config.txt to broaden the search. Alternatively, you can copy the actual dumped texture into the ALTS folder inside the REFERENENCE-LIGHT/DARK and rename it {file} to ensure a match. ====")
              print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
              print(f"###########################################################")

        
        
        
        #-----------------------------------------#
        # Iterate over the reference files to find matches in the dumps and perform the actions
        for file, file_data in reference_files.items():

            # If second glove, only process "glove-second.png" and skip all others
            if not glove_normal_or_csv:
                if file != "glove-second.png":
                    continue  # Skip processing any file that is not "glove-second.png"
                # Process "glove-second.png"
                source_image = file_data["source"]
                params = file_data if 'hash_tolerance' in file_data and 'ssim_threshold' in file_data else None
                original_similar_images = find_similar_images(os.path.join(script_dir, reference_folder, source_image), dumps_path, params)
                
                if original_similar_images:
                    process_texture(file, file_data, original_similar_images)
                else:
                    no_texture(file, file_data, original_similar_images)
                continue  # Continue after processing "glove-second.png"

            # Regular processing for other cases when glove_normal_or_csv is True
            source_image = file_data["source"]
            params = file_data if 'hash_tolerance' in file_data and 'ssim_threshold' in file_data else None
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
                    if file in ["13-Sock.png"]:
                        alts_folder = "alts-sock"
                        alternate_source_directory = os.path.join(script_dir, reference_folder, alts_folder)

                        # Check if the alternate source directory exists
                        if os.path.exists(alternate_source_directory):
                            print()  # Add a line break
                            print()  # Add a line break
                            print(f"↓↓↓↓↓↓↓ No match for {source_image}. Trying again using the reference images in the {alts_folder} folder")

                            # Get all PNG files in the alternate source directory
                            alternate_source_files = get_all_png_files_in_directory(alternate_source_directory)

                            for alternate_source_path in alternate_source_files:
                                print(f"at: {alternate_source_path}...")
                                alternate_similar_images = find_similar_images(alternate_source_path, dumps_path, params, context=f"{alts_folder}")

                                if alternate_similar_images:
                                    process_texture(file, file_data, [alternate_similar_images[0]])
                                    break  # Break out of the loop if a match is found

                            else:
                                no_texture(file, file_data, alternate_similar_images)
                        else:
                            no_texture(file, file_data, original_similar_images)
                    else:
                        # Continue with the old way for other files
                        alts_folder = "alts"
                        alternate_source_path = os.path.join(script_dir, reference_folder, alts_folder, source_image)
                        if os.path.exists(alternate_source_path):
                            print()  # Add a line break 
                            print()  # Add a line break 
                            print(f"↓↓↓↓↓↓↓ No match for {source_image}. Trying again using the reference image in the alts folder")
                            alternate_similar_images = find_similar_images(alternate_source_path, dumps_path, params, context=f"{alts_folder}")
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

    # Create csv subfolder if it doesn't exist
    if not os.path.exists(os.path.join(renamed_folder, "csv-texture-names")):
        os.makedirs(os.path.join(renamed_folder, "csv-texture-names"))
    
    if glove_normal_or_csv:
        # Move the CSV file to the 'renamed' folder
        shutil.move(csv_file_path, os.path.join(renamed_folder, "csv-texture-names", csv_filename))

        print()
        print(f"{checkmark} CSV file copied to subfolder.")

    print()  # Add a line break 
    print("#--------------------------------------------------------------#")
    print("#                                                              #")
    if glove_normal_or_csv and required_textures_counter < 30:
      print(f"#                 {Fore.RED}!!!! DONE WITH ERRORS !!!!{Style.RESET_ALL}                   #")
      print(f"#         Number of textures found and renamed: {required_textures_counter + optional_textures_counter}             #")
      print(f"#                   Required: {Fore.RED}{required_textures_counter}{Style.RESET_ALL} of 30                         #")
    if not glove_normal_or_csv and required_textures_counter < 1:
      print(f"#                 {Fore.RED}!!!! DONE WITH ERRORS !!!!{Style.RESET_ALL}                   #")
      print(f"#         Number of textures found and renamed: {required_textures_counter + optional_textures_counter}             #")
      print(f"#                   Required: {Fore.RED}{required_textures_counter}{Style.RESET_ALL} of 1                          #")
    else: 
      print(f"#                         {Fore.GREEN}SUCCESS!{Style.RESET_ALL}                             #")
      print(f"#         Number of textures found and renamed: {required_textures_counter + optional_textures_counter}             #")
      if glove_normal_or_csv:
        print(f"#                   Required: {Fore.GREEN}{required_textures_counter}{Style.RESET_ALL} of 30                         #")
      else:
        print(f"#                   Required: {Fore.GREEN}{required_textures_counter}{Style.RESET_ALL} of 1                           #")
    if glove_normal_or_csv:
      print(f"#                    Optional: {optional_textures_counter} of 5                          #")
    if glove_normal_or_csv and required_textures_counter < 30:
      print("#                                                              #")
      print(f"#                {Fore.RED}!!!!  SOMETHING WENT WRONG. !!!{Style.RESET_ALL}               #")
      print(f"#     {Fore.RED}!!!!  {30 - required_textures_counter} of the required textures are missing.  !!!{Style.RESET_ALL}       #")
    if not glove_normal_or_csv and required_textures_counter < 1:
      print("#                                                              #")
      print(f"#                {Fore.RED}!!!!  SOMETHING WENT WRONG. !!!{Style.RESET_ALL}               #")
      print(f"#     {Fore.RED}!!!!  {30 - required_textures_counter} of the required textures are missing.  !!!{Style.RESET_ALL}       #")
    print("#                                                              #")
    print("#       READ ALL OF THE OUTPUT ABOVE TO CHECK FOR ISSUES.      #")
    print("#      Your renamed textures are in a subfolder of RENAMED.    #")
    print("# The texture names were written to a CSV file in that folder. #")
    print("#  Be sure to leave the CSV file in the folder and submit it   #")
    print("#    with the uniform for easy future edits of this slot.      #")
    print("#                                                              #")
    print("#        ---  PRESS ENTER OR CLOSE THIS WINDOW  ---            #")
    print("#                                                              #")
    print("################################################################")
    print()  # Add a line break 
    print()  # Add a line break 

    input()
    sys.exit()
# /END IMAGE MATCHING IF NO CSV OVERRIDE PROVIDED
############################################################################





############################################################################
# SKIP IMAGE MATCHING AND USE THE TEXTURES NAMES IN THE CSV, IF PROVIDED
elif csv_provided == True:


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
        print(f"All necessary default textures exist. {Fore.GREEN}{checkmark}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}!!!!!!!! ERROR:{Style.RESET_ALL} The following files are missing from the default-textures folder:")
        for missing_file in missing_default_textures:
            print(f"- {missing_file}")
        print()
        print("Cannot proceed. Press enter to exit.")
        print()
        input()
        sys.exit(1)


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
        print(f"All required textures exist in the YOUR_TEXTURES_HERE folder. {Fore.GREEN}{checkmark}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}!!!!!!!! ERROR:{Style.RESET_ALL} The following required textures are missing from the YOUR_TEXTURES_HERE folder:")
        for missing_file in missing_required_textures:
            print(f"- {missing_file}")
        print("Cannot proceed. Press enter to exit.")
        input()
        sys.exit(1)


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
        print(f"All required textures exist in the CSV. {Fore.GREEN}{checkmark}{Style.RESET_ALL}")
        print()
    else:
        print(f"{Fore.RED}!!!!!!!! ERROR:{Style.RESET_ALL} The following required textures are missing from the CSV:")
        for missing_texture in missing_required_textures:
            print(f"- {missing_texture}")
        print("Cannot proceed. Press enter to exit.")
        input()
        sys.exit(1)


    # Ask the user to press Enter to continue
    print()  # Add a line break 
    print(f"{Fore.BLUE}___{Style.RESET_ALL}")
    print()  # Add a line break 
    print("Review the configuration settings above.")
    print("If you are ready to proceed, PRESS ENTER to continue.")
    input()  # Add a line break 

    print()  # Add a line break 
    print("#----------------------------------------------------------#")
    print("#                                                          #")
    print("#                     RESULTS:                             #")
    print("#                                                          #")


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
                print(f"{checkmark} {texture}{output} copied and renamed.")

            # Iterate over the rows in the CSV file
            for row in csv_reader:
                team_name, slot, type, texture, filename = row  # Assuming 'TYPE' field is not needed

                # Create subfolder path in renamed_folder based on SLOT value
                subfolder_path = os.path.join(renamed_folder, slot)

                # Ensure the subfolder exists, create it if not
                os.makedirs(subfolder_path, exist_ok=True)

                # Number shadows
                if texture == 'num07shadow.png':
                    num07_shadow_folder = os.path.join(subfolder_path, 'num07-shadow')
                    os.makedirs(num07_shadow_folder, exist_ok=True)
                    transparent_destination_path = os.path.join(num07_shadow_folder, filename)
                    shutil.copy2(transparent_source_path, transparent_destination_path)
                    print(f"{checkmark} num07shadow (transparented) copied and renamed.")
                elif texture == 'num89shadow.png':
                    num89_shadow_folder = os.path.join(subfolder_path, 'num89-shadow')
                    os.makedirs(num89_shadow_folder, exist_ok=True)
                    transparent_destination_path = os.path.join(num89_shadow_folder, filename)
                    shutil.copy2(transparent_source_path, transparent_destination_path)
                    print(f"{checkmark} num89shadow (transparented) copied and renamed.")
                
                # Num07ss
                elif texture == 'num07ss.png':
                    if ssnumbers_pref:
                        copy_numbers(source_folder, subfolder_path, filename, 'num07ss.png', 'num07.png')
                    else:
                        print("- Skipped num07ss.png.")
                # Num89ss
                elif texture == 'num89ss.png':
                    if ssnumbers_pref:
                        copy_numbers(source_folder, subfolder_path, filename, 'num89ss.png', 'num89.png')
                    else:
                        print("- Skipped num89ss.png.")
                # Num07helmet
                elif texture == 'num07helmet.png':
                    if helmetnumbers_pref:
                        copy_numbers(source_folder, subfolder_path, filename, 'num07helmet.png', 'num07.png')
                    else:
                        print("- Skipped num07helmet.png")
                # Num89helmet
                elif texture == 'num89helmet.png':
                    if helmetnumbers_pref:
                        copy_numbers(source_folder, subfolder_path, filename, 'num89helmet.png', 'num89.png')
                    else:
                        print("- Skipped num89helmet.png")
                

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
                        print(f"{checkmark} glove.png copied and renamed.")
                    else:
                        # Print error message
                        print(f"{Fore.RED}-{Style.RESET_ALL} Skipped. Glove in CSV but no glove.png source in YOUR_TEXTURES folder.")
                
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
                        print(f"{checkmark} glove-second.png copied and renamed.")
                    else:
                        # Print error message
                        print(f"{Fore.RED}-{Style.RESET_ALL} Skipped. Glove-second in CSV but no glove-second.png source in YOUR_TEXTURES folder.")
                      
                        
                
                
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
                            print()
                            print(f"###########################################################")
                            print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
                            print(f"{Fore.RED}!!! ERROR:{Style.RESET_ALL} You want to use a pride sticker but no pridesticker.png source file exists in YOUR_TEXTURES. Add the source file and try again, or choose 'no' for the Pride Sticker preference next time.")
                            print(f"{Fore.RED}!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}")
                            print(f"###########################################################")
                            # Wait for user to press enter
                            print("Press Enter to exit the program.")
                            input()
                            sys.exit()
                        
                    else:
                        pridesticker_source_path = os.path.join(default_textures_folder, 'transparent.png')
                        pridesticker_output = " (transparented)"
                    transparent_destination_path = os.path.join(pridesticker_folder, filename)
                    shutil.copy2(pridesticker_source_path, transparent_destination_path)
                    print(f"{checkmark} pridesticker{pridesticker_output} copied and renamed.")
                
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
                        print(f"{checkmark} {texture} copied and renamed.")
                    else:
                        print(f"{Fore.RED}-{Style.RESET_ALL} {texture} in CSV but no source in YOUR_TEXTURES folder")

    for csv_file in csv_files:
        csv_source_path = os.path.join(csv_folder, csv_file)

        # Create csv subfolder if it doesn't exist
        if not os.path.exists(os.path.join(subfolder_path, "csv-texture-names")):
            os.makedirs(os.path.join(subfolder_path, "csv-texture-names"))
        
        csv_destination_path = os.path.join(subfolder_path, "csv-texture-names", csv_file)  # Adjust the filename accordingly
        
        # Copy the CSV file to the destination with the specified filename
        shutil.copy2(csv_source_path, csv_destination_path)
        print()
        print(f"{checkmark} CSV file copied to subfolder > csv-texture-names.")

    print()
    print()  # Add a line break 
    print("#--------------------------------------------------------------#")
    print(f"#                         {Fore.GREEN}SUCCESS!{Style.RESET_ALL}                             #")
    print("#             All files were copied and renamed                #")
    print("#                  according to the CSV data.                  #")
    print("#                                                              #")
    print("#       READ ALL OF THE OUTPUT ABOVE TO CHECK FOR ISSUES.      #")
    print("#      Your renamed textures are in a subfolder of RENAMED.    #")
    print("#      The source CSV file was also copied to that folder.     #")
    print("#  Be sure to leave the CSV file in the folder and submit it   #")
    print("#                                                              #")
    print("#        ---  PRESS ENTER OR CLOSE THIS WINDOW  ---            #")
    print("#                                                              #")
    print("################################################################")
    print()  # Add a line break 
    print()  # Add a line break 

    input()
    sys.exit()