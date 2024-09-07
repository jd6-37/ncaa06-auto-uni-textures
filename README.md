# NCAA NEXT Texture Renaming Utility

This utility is designed to assist in making uniforms for the NCAA NEXT mod's Uniform Expansion project. It significantly reduces the time required to create or update uniforms. It also catalogs the texture names in a CSV file and ensures that uniforms are structured in a standardized format.

The utility operates in one of two modes:

- **Mode 1 (CSV):** Renames your custom uniform textures based on the texture names provided in a CSV file.
- **Mode 2 (DUMPS):** Automatically searches through the dumps folder to find and rename the correct textures, while also cataloging them in a CSV file.

*Mode 1 is automatically selected if there is a CSV file in the `csv-override` folder. If no CSV file is present, Mode 2 is automatically selected.*

Mode 2’s Python image recognition feature means we no longer have to hunt for textures in the dumps folder and manually catalog texture names. With the renaming functionality of both modes, we never have to rename files by hand! 🎉

Additionally, dumping and Mode 2 only needs to be done once per uniform. After a CSV file is created, the uniform never has to be dumped again. We only need to use the fast Mode 1 CSV renaming in the future. 👀

Screenshot:
![Screenshot 2024-09-08 at 1 40 45 AM](https://github.com/user-attachments/assets/2d412e31-cddb-4f21-abe8-ddac3b0c3443)

## Table of Contents
- [Installation](#installation)
  - [Option 1: EXE](#installation--exe)
  - [Option 2: Python Source](#installation--python)
- [Using the App](#usage)
- [License](#license)
- [Credits](#credits)

## Installing the App <a name="installation"></a>

To install and run the app, you have two options:

### Install Option 1: Windows Installer <a name="installation--exe"></a>

Download the setup exe from the latest release and run it. Follow the installation prompts. You can save a shortcut to your desktop or run it from your Start menu like any other Windows application. 

NOTE: You will most likely be warned by Windows Defender about malware for two reasons: 1) the program used to convert the Python app to an EXE is commonly used by hackers, so Windows (as it should) flags these as potential risks, especially because 2) I created the app without a proper developers license (because it costs hundreds of dollars per year). So, if you're not comfortable installing and running the EXE, that's understandable. You can always run the Python source file directly as described in Option 2 below. And feel free to inspect the source code (or ask a programmer you trust to inspect it) beforehand. 

### Install Option 2: Python Source (required for Mac and Linux) <a name="installation--python"></a>

Alternatively, if you have Python installed on your machine, you can run the source py file instead of installing an EXE. If you're on a Mac or Linux machine, this is the only way to run the program.

**STEP 1 – INSTALL PYTHON AND REQUIRED MODULES**

First, check to see if Python is already installed with `python --version`. Also try `python3 --version` if the first one doesn't return a version number. If neither command shows you have Python, you'll need to install it. The easiest way is to go to [python.org](https://www.python.org) and download and install it from there. This project was created in Python Version 3.12.4, so it's best to use that version, if possible. 

Next, you need to install the project's required modules. This is done with the "pip" installer command. All of the project's required modules are listed in the included requirements.txt file. So, to install them all at once, simply open your Terminal or Command Prompt window, navigate to the project directory where the requirements.txt file resides, and run the command: 

    pip install -r requirements.txt

If you get an error, try:

    pip3 install -r requirements.txt


**STEP 2 – RUN THE PY FILE**

With python and all of the required modules installed, you can now start the app with:

    python Auto-Rename-Textures.py

or if that doesn't work, try... 

    python3 Auto-Rename-Textures.py

The app should open in a new window and from here it will work just the same as running the EXE.

Closing the window or pressing Ctrl + c will terminate the app.

<br>

## Using the App <a name="usage"></a>

Open the app and click the "View README" button at the top right of the window to view the documentation.

<br>

## LICENSE & PERMISSIONS <a name="license"></a>

NCAA NEXT Texture Renaming Utility © 2024 is licensed under [CC BY-NC 4.0](http://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1) 

This license requires that reusers give credit to the creator. It allows reusers to distribute, remix, adapt, and build upon the material in any medium or format, for noncommercial purposes only.

<br>

## Credits <a name="credits"></a>

This is an NCAA NEXT mod team project. The idea was conceived and POCed by @H4wduk3n, and the development of the project is a collaboration between @H4wduk3n, @JD637, and @jozur – along with the help of others in the NCAA NEXT team and community.
