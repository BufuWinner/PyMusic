import deezloader
from deezloader.utils import generate_token
import requests
import os
import glob



def global_search(query):
    global final_res, ind_search, res_search, link_search, links
    q = '\"' + query + '\"'
    offset = 0
    again = False
    new = None
    while True:
        if again:
            q = '\"' + input('= ') + '\"'
            new = None
        token = generate_token()
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
            'offset': offset
        }

        raw_response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
        # print(raw_response.url)
        response = raw_response.json()
        # print(response)

        if len(response['tracks']['items']) == 0:
            new = input('Non ci sono più risultati, riprovare (vuoto = si, e = exit)?\n')
        if new == 'e':
            print('\nOk, alla prossima!')
            exit()
        elif new == '':
            again = True
            continue

        index = 1
        for sg in response['tracks']['items']:
            artist = sg['artists'][0]['name']
            song = sg['name']
            print(f'{index}) {artist} - {song}')
            index += 1

        # print(res)
        ind = 1
        links = {}
        for link in response['tracks']['items']:
            url = link['external_urls']['spotify']
            links.setdefault(ind, url)
            ind += 1

        # print(ind_search)
        # print(res_search)
        final_res = input('\nQuale canzone (inserisci numero, lasciare vuoto per riprovare, n = next, e = exit)?\n')
        if len(final_res) == 0:
            again = True
        elif final_res == 'n':
            offset += 5
            again = False
        elif final_res == 'e':
            print('\nOk, alla prossima!')
            quit()
        elif int(final_res) not in range(index):
            print('Numero invalido :(')
            continue
        else:
            break

    link = links[int(final_res)]

    return link


# DOWNLOAD INFO
standard_output = '/Users/stefamily/Documents/Convertitore'
file_mover = True

search_type = input('Ricerca globale (lasciare vuoto per ricerca specifica):\n')
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
    song = input('Brano= ')
    artist = input('Artista= ')
    tracklink = False
    albumlink = False

else:
    link = global_search(search_type)

    tracklink = True
    albumlink = False
out = input('Cambiare Output (lasciare vuoto per standard)?\n')
if len(out) == 0:
    output = standard_output
else:
    output = out

# DEEZER DOWNLOADER
download = deezloader.Login("90cc591f741847a0e93a2b5162df39b9ce1e0e3e35d50e138d3c29f805ccb97f75da0ac8c57219f742ceb64e6238cfeff9f50dd95eb31ea2eca6470c7e82ca1c5e4971498437b3462e3ccd494c185d8df6bcfb254b8543878299d8c84e11fc26")
if tracklink:
    try:
        download.download_trackspo(
            URL=link,
            output=output,
            quality="MP3_320",
            recursive_quality=True,
            recursive_download=False,
            not_interface=False
        )
    except(deezloader.exceptions.TrackNotFound, deezloader.exceptions.NoDataApi, deezloader.exceptions.InvalidLink):
        print('Brano Non Trovato :(\n')
        quit()

elif albumlink:
    try:
        download.download_albumspo(
            URL=link,
            output=output,
            quality="MP3_320",
            recursive_quality=True,
            recursive_download=False,
            not_interface=False,
            zips=False
        )
        file_mover = False
    except(deezloader.exceptions.TrackNotFound, deezloader.exceptions.NoDataApi, deezloader.exceptions.InvalidLink):
        print('Brano Non Trovato :(\n')
        quit()

elif playlink:
    try:
        download.download_playlistspo(
            URL=link,
            output=output,
            quality="MP3_320",
            recursive_quality=True,
            recursive_download=False,
            not_interface=False,
            zips=False
        )
        file_mover = False
    except(deezloader.exceptions.TrackNotFound, deezloader.exceptions.NoDataApi, deezloader.exceptions.InvalidLink):
        print('Brano Non Trovato :(\n')
        quit()

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
    except(deezloader.exceptions.TrackNotFound, deezloader.exceptions.NoDataApi):
        print('Brano Non Trovato :(\n')
        quit()

# File Mover
if file_mover:
    files = glob.glob(f'{output}/*')
    folder = max(files, key=os.path.getmtime)
    os.chdir(folder)
    list2 = os.listdir()
    song_move = list2[0]
    number = 1
    for _ in range(len(files)):
        if os.path.isfile(f'{output}/{number}.mp3'):
            number += 1
        else:
            break
    try:
        os.rename(song_move, f'{output}/{number}.mp3')
    except:
        print('Brano non spostabile :(')
        quit()
    print('\nBrano spostato!')

    os.rmdir(folder)
    print('Cartella eliminata!\n')
