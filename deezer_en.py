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
            new = input('There are no more results, retry? (empty = yes, e = exit)\n')
        if new == 'e':
            print('\nOk, goodbye!')
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
        final_res = input('\nWhich song? (insert number, leave empty to retry, n = next, e = exit)\n')
        if len(final_res) == 0:
            again = True
            offset = 0
        elif final_res == 'n':
            offset += 5
            again = False
        elif final_res == 'e':
            print('\nOk, goodbye!')
            quit()
        elif final_res not in range(index):
            print('Number outrange :(')
            continue
        else:
            break

    link = links[int(final_res)]

    return link


def settings():
    while True:
        with open('settings.txt', 'r') as settings:
            lines = []
            for line in settings:
                print(line, end='')
                lines.append(line)
            setting = input('\nWhich option do you want to change? (e = exit)\n')
            if setting == 'e':
                break
            elif setting == '1':
                if 'True' in lines[0]:
                    new = lines[0].replace('True', 'False')
                    lines.pop(0)
                    lines.insert(0, new)
                else:
                    new = lines[0].replace('False', 'True')
                    lines.pop(0)
                    lines.insert(0, new)
            elif setting == '2':
                if 'True' in lines[1]:
                    new = lines[1].replace('True', 'False')
                    lines.pop(1)
                    lines.insert(1, new)
                else:
                    new = lines[1].replace('False', 'True')
                    lines.pop(1)
                    lines.insert(1, new)
            elif setting == '3':
                path = input('Insert new path=\n')
                lines.pop(2)
                lines.insert(2, f'3) output = {path}\n')
            elif setting == '4':
                print(f'\n{generate_token()}\n')
            else:
                print('I wasn\'t expecting this... only from 1 to 4')
                return
            new_settings = ''.join(lines)
            # print(new_settings)
        rp = open('settings.txt', 'w')
        rp.write(new_settings)
        rp.close()


def get_settings():
    with open('settings.txt', 'r') as raw_settings:
        settings = []
        ind = 0
        for line in raw_settings:
            if ind == 3:
                break
            settings.append(line.split('= ')[-1].strip())
            ind += 1

        # settings.pop(-1)
    return settings


def check_output(output):
    if not os.path.isdir(output):
        a = input('The given output folder doesn\'t exist, do you want to create it? (y/n)\n')
        if a == 'y':
            checked = output
        elif a == 'n':
            new_out = input('new output= ')
            if not os.path.isdir(new_out):
                print('Nevermind, just put a valid output in the options or while searching.')
                quit()
            checked = new_out
        else:
            print('I\'ll get that as a yes...')
            checked = output
        return checked
    return output


while True:
    # DOWNLOAD INFO
    repeat, file_mover, standard_output = get_settings()
    # print(repeat, file_mover, standard_output)
    repeat = str(repeat)
    file_mover = str(file_mover)

    search_type = input('Global search (leave empty for specific search, --options to enter the settings):\n')
    tracklink = None
    albumlink = None
    playlink = None
    deezlink = None
    link = ''
    artist = ''
    song = ''

    if search_type == '--options':
        settings()
        continue

    elif 'https://open.spotify.com/' in search_type:
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
        song = input('Track= ')
        artist = input('Artist= ')
        tracklink = False
        albumlink = False

    else:
        link = global_search(search_type)

        tracklink = True
        albumlink = False
    out = input('Change output? (leave empty for standard)\n')
    if len(out) == 0:
        output = check_output(standard_output)
    else:
        output = check_output(out)

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
            print('Couldn\'t find the song :(\n')
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
            print('Couldn\'t find the song :(\n')
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
            print('Couldn\'t find the song :(\n')
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
            print('Couldn\'t find the song :(\n')
            quit()

    # File Mover
    if file_mover == 'True':
        project_dir = os.getcwd()
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
            print('Couldn\'t move song :(')
            quit()
        print('\nSong moved!')

        os.rmdir(folder)
        print('Folder deleted!\n')
        if repeat == 'True':
            os.chdir(project_dir)
    if repeat == 'False':
        break
