import deezloader
from deezloader.utils import generate_token
import requests
import os
import glob


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
            'market': 'IT',
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
        final_res = input('\nQuale canzone (inserisci numero, lasciare vuoto per riprovare, n = next, e = exit)?\n')
        if len(final_res) == 0:
            again = True
        elif final_res == 'n':
            offset += 5
        elif final_res == 'e':
            print('\nOk, alla prossima!')
            exit()
        elif int(final_res) not in ind_search.keys():
            print('Numero invalido :(')
            continue
        else:
            break

    index = int(final_res)
    artist = ind_search[index]
    song = res_search[artist]
    link = link_search[song]

    return artist, song, link


# DOWNLOAD INFO
standard_output = '/Desktop'
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
    _, _, link = global_search(search_type)

    tracklink = True
    albumlink = False
out = input('Cambiare Output (lasciare vuoto per standard)?\n')
if len(out) == 0:
    output = standard_output
else:
    output = out

# DEEZER DOWNLOADER
download = deezloader.Login("il tuo ARL token")
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
            zips=True
        )
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
            zips=True
        )
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
