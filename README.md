# PyMusic
Simple python file (EN or IT) that let's you search and download high quality music using the [Spotify API](https://developer.spotify.com/) and the famous [deezloader](https://github.com/An0nimia/deezloader) library.


### How to get it working:
- Download the python file in the desired language and the settings.txt file and put them in the same folder
- Otherwise [__DOWNLOAD THE NEW EXECUTABLE__](https://github.com/BufuWinner/PythonMusic/releases/tag/%401.0), no python needed!

- Download the modules:
	- deezloader ```pip3 install deezloader```
	- requests ```pip3 install requests```
	

- I recommend to change the standard output directory using the settings menu accesible by writing ```--options``` in the global search and changing the output
  path by inserting 4. Otherwise the program will ask you on first run. 

	```
	Global search (leave empty for specific search, --options to enter the settings):
	--options
	1) repeat = False
	2) file_mover = True
	3) ask_for_output = False
	4) output = NONE
	5) token
	Which option do you want to change? (e = exit)
	4
	Insert new path=
	```
	
- In the menu you can also choose wether to enable the ```file mover``` (moves song out of album folder) or the ```repeat``` option (the script loops letting you download multiple songs).
  
- Done, yay!:smile:

### How to use:
This is the structure:

- Global search --> query / empty (specific search) / --options (settings menu)
	- Choose song --> number (from 1 to 5) / n (continue search list) / e (exit script)
	- Change output --> empty (uses the settings output) / path to folder
		- Folder doesn't exist --> y (create it) / n (insert new path)
	- Download
- Specific search
	- Track
	- Artist
	- Download
- Settings menu
	- Choose option =
	  - 1 (repeat, T / F) 
	  - 2 (file mover, T / F)
	  - 3 (ask temp output, T/F)
	  - 4 (output path, insert new path)
	  - 5 (print spotify API token)
	
 
### Optional (on macOS):
- open Terminal
- write ```nano```
- inside write:
	```
	cd YOUR PYTHON_FILE_PATH
	python3 YOUR_FILE_NAME.py
	```
 - press ctrl + x
 - press y
 - write ```CHOOSE_NAME.command```
 - press enter
 - you should find a file named ```CHOOSE_NAME.command``` in your current directory
 - (in terminal) write ```chmod +x PATH_TO_NEW_FILE.command``` to grant permission to the file
 - double click to open
 - the Terminal opens, you should see the downloder running in the window
 - change icon, change name(you can remove '.command') = perfect music downloader!:smile:

### Optional (on Windows)
- open Notepad
- inside write:
	```
	cd YOUR_PYTHON_FILE_PATH
	python YOUR_FILE_NAME.py
	```
- save file as ```CHOOSE_A_NAME.cmd```
- create a shortcut (right click in folder -> new -> shortcut) and write:
	```
	cmd /c "PATH_TO_CMD_FILE"
	```
- save shortcut
- go on properties and modify whatever you want! (font color, icon...)
- you can even put it in the application bar!
 
The code isn't too advanced and was tested on macOS and Windows, feel free to report any issues!
