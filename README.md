# PythonMusic
Simple python file (EN or IT) that let's you search and download music using the [Spotify API](https://developer.spotify.com/) and the famous [deezloader](https://github.com/An0nimia/deezloader) library.


### How to get it working:
- Download the modules:
	- spotipy ```pip3 install spotipy```
	- deezloader ```pip3 install deezloader```
	- requests ```pip3 install requests```

- Get an ARL token from [_the deezer site_](https://www.deezer.com/) and change string at __line 142__. [Tutorial](https://www.youtube.com/watch?v=pWcG9T3WyYQ)

	```python3
	download = deezloader.Login('your ARL token here')  # line 142
	```
- Create an app on the [_spotify for developers site_](https://developer.spotify.com/dashboard/) and change client_id and client_secret at __line 18__. [Tutorial](https://developer.spotify.com/documentation/web-api/quick-start/)

	```python3
	auth_manager = SpotifyClientCredentials(client_id='your id', client_secret='your secret')  # line 18
	```
- I recommend to change the standard output directory at __line 102__ to your desired folder.

	```python3
	standard_output = '~/Desktop/'  # line 102
	```
	
- If you need it I created from __line 191 to 216__ a simple file mover(moves song out of album folder), if not delete those lines.
  You'll need to modify it if you have more then one file/directory in the output directory.
  
	```python3
	# File Mover from line 191 to end of file
	if output == standard_output:
		time.sleep(2)
		os.chdir(output)
		list1 = os.listdir()
		folder = output + list1[0]
		os.chdir(folder)
		list2 = os.listdir()
		song_move = list2[0]
		try:
			os.rename(song_move, output + 'music.mp3')
		except:
			print('Couldn\'t move file :(')
			quit()
		print('\nMoved song!')

		os.rmdir(folder)
		print('Folder deleted!\n')
	```  
  
- Done, yay!:smile:
 
 
### Optional (on macOS):
- open Terminal
- write ```nano```
- write:
```
cd YOUR PYTHON FILE PATH
python3 YOUR_FILE_NAME.py
```
 - press ctrl + x
 - press y
 - write ```CHOOSE_NAME.command```
 - press enter
 - you should find a file named ```CHOOSE_NAME.command``` in your current directory
 - double click to open
 - the Terminal opens, you should see the python file running in the window
 - change icon, change name(you can remove .command) = perfect music downloader 'app'!:smile:
 
 
The code isn't too advanced, so feel free to report any issues!
