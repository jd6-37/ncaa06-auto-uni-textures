
#===== NCAA NEXT UNIFORM EXPANSION TEXTURE RENAMING UTILITY =====

This is the second generation of the batch renaming companion utility 
for the NCAA NEXT Uniform Expansion project. It can still rename textures 
using texture names provided in a CSV file, but also...

It can now automatically find the proper filename to use by looking at your dumps folder!
You no longer need to hunt in the dumps folder and manually track textures names!


##----------- PREPARING YOUR TEXTURES (For both renaming methods): ----------

STEP 1. Copy all of the exported PNG files from the TC Gear template into 
the "YOUR_TEXTURES_HERE" folder.

NOTE: Don't feel like you need to use the chinstrap from the TC Gear template. 
It's probably best to use a plain white one anyway unless you see differently 
in reference photos. The default white one is in the 'default-textures' folder. 
If you want to use that, copy it into the 'YOUR_TEXTURES_HERE' folder and replace the 
chinstrap from the TC Gear export. Make sure it is named 'img22.png' or '22-Chinstrap.png'.

Step 2 (only required for users of the LITE or XLITE TC Gear Template).
Create your shoe textures using the cleats template and overwrite the following files
with your finished textures. This is not required if you used the FULL version of the
TC Gear template.

16-Shoe.png
17-Shoe_w_White_Tape.png
23-Shoe_w_Black_Tape.png
24-Shoe_w_TC_Tape.png

STEP 3. Put your other uniform pieces in the same folder. They must be named 
exactly as follows. The number shadows are automatically made transparent. No need to add those.

helmet.png
pants.png
jersey.png
num07.png
num89.png
pridesticker.png*
num07helmet.png†
num89helmet.png†
num07ss.png† 
num89ss.png† 

* optional, these can be transparented by the tool

† optional, and if no source texture is provided, the script can use the main jersey numbers for 
  the helmet and/or sleeve/shoulders (this is usually what you want)



##----------- INSTRUCTIONS (For Auto Dumps Image Matching): ----------

Before you start: It's important that you dumped your textures in a very specific way. 
Follow these instructions closely:
https://docs.google.com/document/d/1RI2ceiXVRgVu8H-POCee2n3O08iQxa_Q/

STEP 1. Open config.txt and define the path to your dumps folder. 
You can also define the other variables here if you want. 
For the uniform slot name, use the format teamname-slotname (note the dash) where slotname 
is home/away/alt01/etc. The part after the dash is what is used to name the output folder.

STEP 2. Double-click the Auto-Rename-UniExp-Textures.exe file and follow the prompts.

STEP 3. That's it! Move the subfolder in RENAMED to your emulator textures folder 
Eg. PCSX2/texture/SLUS-21214/replacements folder to test the uniform.

STEP 4. Test the textures in-game to ensure everything is named properly and working as intended. 

DONE!


##----------- INSTRUCTIONS (For CSV Input): ----------

STEP 1: Put one CSV file in the csv-override folder. Make sure it is in the same format 
as csv-override-example.csv.

STEP 2: Double-click the Auto-Rename-UniExp-Textures.exe file and follow the prompts.

STEP 3. That's it! Move the subfolder in RENAMED to your emulator textures folder 
Eg. PCSX2/texture/SLUS-21214/replacements folder to test the uniform.

STEP 4. Test the textures in-game to ensure everything is named properly and working as intended. 

DONE!