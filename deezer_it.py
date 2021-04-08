import deezloader
from deezloader.utils import generate_token
import requests
import os
import glob


def global_search(query):
    global final_res, ind_search, res_search, link_search, links, raw_response
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

        try:
            raw_response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
        except:
            print('Impossibile raggiungere il servizio, controlla la tua connessione...')
            input('Premi \'Invio\' per chiudere il programma')
            quit()
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
            offset = 0
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


def settings():
    while True:
        with open('settings.txt', 'r') as settings:
            lines = []
            for line in settings:
                print(line, end='')
                lines.append(line)
            setting = input('\nQuale opzione vuoi cambiare?(e = exit)\n')
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
                if 'True' in lines[2]:
                    new = lines[2].replace('True', 'False')
                    lines.pop(2)
                    lines.insert(2, new)
                else:
                    new = lines[2].replace('False', 'True')
                    lines.pop(2)
                    lines.insert(2, new)

            elif setting == '4':
                path = input('Inserisci il nuovo percorso=\n')
                lines.pop(2)
                lines.insert(2, f'3) output = {path}\n')
            elif setting == '5':
                print(f'\n{generate_token()}\n')
            else:
                print('Non mi aspettavo questo... solo dal 1 al 4')
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
            if ind == 4:
                break
            settings.append(line.split('= ')[-1].strip())
            ind += 1

        # settings.pop(-1)
    return settings


def check_output(output):
    if output == 'NONE':
        print('L\'output non è ancora stato modificato, inseriscine uno valido selezionando la quarta opzione.')
        settings()
        return
    elif not os.path.isdir(output):
        a = input('La cartella di output data non esiste, crearla? (y/n)\n')
        if a == 'y':
            checked = output
        elif a == 'n':
            new_out = input('nuovo output= ')
            if not os.path.isdir(new_out):
                print('Non importa, metti un output valido nelle opzioni o in quello temporaneo.')
                quit()
            checked = new_out
        else:
            print('Lo prendo come un sì')
            checked = output
        return checked
    return output


while True:
    # DOWNLOAD INFO
    repeat, file_mover, ask_for_output, standard_output = get_settings()
    # print(repeat, file_mover, standard_output)
    repeat = str(repeat)
    file_mover = str(file_mover)
    ask_for_output = str(ask_for_output)

    search_type = input('Ricerca globale (lasciare vuoto per ricerca specifica, --options = impostazioni):\n')
    tracklink = None
    albumlink = None
    playlink = None
    deezlink = None
    link = ''
    artist = ''
    song = ''
    out = ''

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
        song = input('Brano= ')
        artist = input('Artista= ')
        tracklink = False
        albumlink = False

    else:
        link = global_search(search_type)

        tracklink = True
        albumlink = False
    if ask_for_output == 'True':
        out = input('Cambiare Output (lasciare vuoto per standard)?\n')
    if len(out) == 0:
        output = check_output(standard_output)
    else:
        output = check_output(out)

# DEEZER DOWNLOADER
    try:
        download = deezloader.Login(requests.get('https://pastebin.com/raw/LkP0Hbkq').text)  # requests.get('https://pastebin.com/raw/LkP0Hbkq').text
    except deezloader.exceptions.BadCredentials:
        print('Invalid ARL token, please check you connection or try again later')
        input('Premi \'Invio\' per chiudere il programma')
        quit()
    except Exception:
        print('Trovato errore imprevisto...')
        input('Premi \'Invio\' per chiudere il programma')
        quit()
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
            input('Premi \'Invio\' per chiudere il programma')
            quit()
        except Exception:
            print('Trovato errore imprevisto...')
            input('Premi \'Invio\' per chiudere il programma')
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
            input('Premi \'Invio\' per chiudere il programma')
            quit()
        except Exception:
            print('Trovato errore imprevisto...')
            input('Premi \'Invio\' per chiudere il programma')
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
            input('Premi \'Invio\' per chiudere il programma')
            quit()
        except Exception:
            print('Trovato errore imprevisto...')
            input('Premi \'Invio\' per chiudere il programma')
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
            input('Premi \'Invio\' per chiudere il programma')
            quit()
        except Exception:
            print('Trovato errore imprevisto...')
            input('Premi \'Invio\' per chiudere il programma')
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

        """for _ in range(len(files)):
            if os.path.isfile(f'{output}/{number}.mp3'):
                number += 1
            else:
                break
        try:
            os.rename(song_move, f'{output}/{number}.mp3')
        except:
            print('Brano non spostabile :(')
            quit()"""

        try:
            os.rename(song_move, f'{output}/{song_move}')
        except:
            print('Brano non spostabile :(')
            quit()
        print('\nBrano spostato!')
        os.chdir(project_dir)
        os.rmdir(folder)
        print('Cartella eliminata!')
    if repeat == 'False':
        break

print('\nFinito!\n')
quit()
