# PythonMusic
Simple python file (EN or IT) that let's you search and download high quality music using the [Spotify API](https://developer.spotify.com/) and the famous [deezloader](https://github.com/An0nimia/deezloader) library.


### How to get it working:
- Download the modules:
	- deezloader ```pip3 install deezloader```
	- requests ```pip3 install requests```

- Get an ARL token from [_the deezer site_](https://www.deezer.com/) and change string at __line 126__. [Tutorial](https://www.youtube.com/watch?v=pWcG9T3WyYQ)

	```python3
	download = deezloader.Login('your ARL token here')  # line 126
	```

- I recommend to change the standard output directory at __line 86__ to your desired folder.

	```python3
	standard_output = '/Desktop'  # line 86
	```
	
- If you need it I created from __line 188 to 210__ a simple file mover (moves song out of album folder and renames with a number), else change the option at __line 87__.
	```python3
	file_mover = True  # line 87, put False to disable
	```
  
- Done, yay!:smile:
 
 
### Optional (on macOS):
- open Terminal
- write ```nano```
- inside write:
	```
	cd YOUR PYTHON FILE PATH
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
 
 
The code isn't too advanced and was only tested on macOS, feel free to report any issues!
