import deezloader
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import os
import time


def global_search(query):
    global final_res, ind_search, res_search, link_search
    q = '\"' + query + '\"'
    offset = 0
    again = False
    new = None
    while True:
        if again:
            q = '\"' + input('= ') + '\"'
            new = None
        auth_manager = SpotifyClientCredentials(client_id='bf9b4c04c511406886e8e952b9f68a7c',
                                                client_secret='65e8bded9989432399e4da9ddef77eac')
        token = auth_manager.get_access_token(as_dict=False)
        # print(token)

        # My Search
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }
        params = {
            'q': q,
            'type': 'track',
            'limit': 5,
            'market': 'IT',
            'offset': offset
        }

        raw_response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
        # print(raw_response.url)
        response = raw_response.json()
        # print(response)

        if len(response['tracks']['items']) == 0:
            new = input('No more results, try again (empty = yes, e = exit)?\n')
        if new == 'e':
            print('\nOk, goodbye!')
            exit()
        elif new == '':
            again = True
            continue

        rawres = []

        for sg in response['tracks']['items']:
            rawres.append(sg['artists'][0]['name'])
            rawres.append(sg['name'])

        res_search = {rawres[i]: rawres[i + 1] for i in range(0, len(rawres), 2)}
        # print(f'\n{res}')
        ind = 1
        rawind = []

        for key in res_search.keys():
            print(f'{ind}) {key} - {res_search[key]}')
            rawind.append(ind)
            rawind.append(key)
            ind += 1

        ind_search = {rawind[i]: rawind[i + 1] for i in range(0, len(rawind), 2)}
        rawlink = []

        for link in response['tracks']['items']:
            rawlink.append(link['name'])
            rawlink.append(link['external_urls']['spotify'])

        link_search = {rawlink[i]: rawlink[i + 1] for i in range(0, len(rawlink), 2)}

        # print(ind_search)
        # print(res_search)
        final_res = input('\nWhich song (insert number, leave empty to try again, n = next, e = exit)?\n')
        if len(final_res) == 0:
            again = True
        elif final_res == 'n':
            offset += 5
        elif final_res == 'e':
            print('\nOk, goodbye!')
            exit()
        elif int(final_res) not in ind_search.keys():
            print('Number outrange :(')
            continue
        else:
            break

    index = int(final_res)
    artist = ind_search[index]
    song = res_search[artist]
    link = link_search[song]

    return artist, song, link


# DOWNLOAD INFO
standard_output = '~/Desktop/'

search_type = input('Global search (leave empty for specific search):\n')

tracklink = None
albumlink = None
playlink = None
link = ''
artist = ''
song = ''

if 'https://open.spotify.com/' in search_type:
    link = search_type
    if '/track/' in search_type:
        tracklink = True
        albumlink = False
    elif '/album/' in search_type:
        albumlink = True
    elif '/playlist/' in search_type:
        playlink = True
        albumlink = False

elif len(search_type) == 0:
    song = input('Song= ')
    artist = input('Artist= ')
    tracklink = False
    albumlink = False

else:
    _, _, link = global_search(search_type)

    tracklink = True
    albumlink = False
out = input('Change output (leave empty for standard)?\n')
if len(out) == 0:
    output = standard_output
else:
    output = out

# DEEZER DOWNLOADER
download = deezloader.Login(
    "90cc591f741847a0e93a2b5162df39b9ce1e0e3e35d50e138d3c29f805ccb97f75da0ac8c57219f742ceb64e6238cfeff9f50dd95eb31ea2eca6470c7e82ca1c5e4971498437b3462e3ccd494c185d8df6bcfb254b8543878299d8c84e11fc26")
if tracklink:
    download.download_trackspo(
        URL=link,
        output=output,
        quality="MP3_320",
        recursive_quality=True,
        recursive_download=False,
        not_interface=False
    )

elif albumlink:
    download.download_albumspo(
        URL=link,
        output=output,
        quality="MP3_320",
        recursive_quality=True,
        recursive_download=False,
        not_interface=False,
        zips=True
    )

elif playlink:
    download.download_playlistspo(
        URL=link,
        output=output,
        quality="MP3_320",
        recursive_quality=True,
        recursive_download=False,
        not_interface=False,
        zips=True
    )

else:
    try:
        download.download_name(
            artist=artist.lower(),
            song=song.lower(),
            output=output,
            quality="MP3_320",
            recursive_quality=True,
            recursive_download=False,
            not_interface=False
        )
    except deezloader.exceptions.TrackNotFound:
        print('Song not found :(')

# File Mover
if output == standard_output:
    time.sleep(2)
    os.chdir(output)
    list1 = os.listdir()
    ind = None
    """for i in list1:
        if i != '.DS_Store' and i != 'Icon\r':
            ind = list1.index(i)"""

    folder = output + list1[0]
    os.chdir(folder)
    list2 = os.listdir()
    song_move = list2[0]
    """song_move2 = song_move1.replace(' ', '\\ ')
    song_move3 = song_move2.replace('(', '\\(')
    song_move4 = song_move3.replace(')', '\\)')"""
    try:
        # os.system(f'mv {song_move4} {output}music.mp3)
        os.rename(song_move, output + 'music.mp3')
    except:
        print('Couldn\'t move file :(')
        quit()
    print('\nMoved song!')

    os.rmdir(folder)
    print('Folder deleted!\n')