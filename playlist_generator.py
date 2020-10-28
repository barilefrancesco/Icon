"""
@author: Francesco Barile 677396
"""

import requests
import json
from selenium import webdriver


def get_code():
    """
    Funzione che serve per acquisire il code dell'utente, partendo dal suo account di spotify.

    :return: code: str, code generato dopo aver effettuato l'accesso a spotify.
    """
    # Apro su chromium la pagina di accesso a spotify
    browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

    browser.get("https://accounts.spotify.com/authorize?client_id=903d61966dab4facb136cdf918b42fba&"
                "scope=playlist-modify-private&scope=playlist-modify-public&response_type=code&"
                "redirect_uri=http%3A%2F%2Fmemorycloud.altervista.org%2F")


    while True:
        if 'http://memorycloud.altervista.org/?code=' in str(browser.current_url):
            url_code = str(browser.current_url)
            break
    # Acquisisco il code dall'url
    code = url_code.replace('http://memorycloud.altervista.org/?code=', '')
    return code


def request_access_token():
    """
    Funzione che serve per acquisire l'access token, per poter eseguire le API request su spotify.

    :return: str, access token; False se cè un problema di autenticazione legato al code.
    """
    code = get_code()

    headers = {
        'Authorization': 'Basic OTAzZDYxOTY2ZGFiNGZhY2IxMzZjZGY5MThiNDJmYmE6YzIyNDg4MjJlMmE3NGVlNWIyYmQzMWIyMjRhY2ZhMDU'
                         '==',
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://memorycloud.altervista.org/'
    }

    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    dict_acc_tockn = json.loads(response.text)
    try:
        # print(dict_acc_tockn['access_token'])
        return dict_acc_tockn['access_token']
    except:
        print(dict_acc_tockn['error'])
        print(dict_acc_tockn['error_description'])
        return False


def request_playlist_id(access_token, playlist_name):
    """
    Funzione che con l'access token e il nome della playlist, cerca e restituisce, l'id id quest'ultimo.
    
    :param access_token: str, stringa generata da spotify.
    :param playlist_name: str, nome della playlist da cercare.
    :return: str, id della playlist.
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + str(access_token),
    }

    params = (
        ('q', playlist_name),
        ('type', 'playlist'),
    )

    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
    return json.loads(response.text)['playlists']['items'][0]['id']


def get_playlist_items(access_token, id_playlist, number_items):
    """
    Funzione che restituisce la lista dei primi 'number_items' della playlist specificata da 'id_playlist'.

    :param access_token: str, stringa generata da spotify.
    :param id_playlist: str, id della playlist.
    :param number_items: int, numero di canzoni da recuperare dalla playlist
    :return: track_list: list, lista di dict contenete titolo della canzone e artista.
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
    }

    params = (
        ('market', 'US'),
        ('limit', str(number_items)),
    )

    response = requests.get('https://api.spotify.com/v1/playlists/' + str(id_playlist) + '/tracks', headers=headers,
                            params=params)

    items = json.loads(response.text)['items']

    track_list = []
    for i in items:
        title = i['track']['name']
        artist = i['track']['artists'][0]['name']
        uri = i['track']['uri']
        track_list.append({'title': title, 'artist': artist, 'uri': uri})
    return track_list


def get_user_id(access_token):
    """
    Funzione che richiede l'user_id per poter successuvamente creare la playlist.

    :param access_token: str, stringa generata da spotify.
    :return: user_id: str, id dell'utente.
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
    }

    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    user_id = json.loads(response.text)['id']
    return user_id


def create_playlist(access_token, generi, track_list):
    """
    Funzione che crea e inserisce gli items all'interno della playlist creata.

    :param access_token: str, stringa generata da spotify.
    :param generi: list, contiene i nomi dei generi.
    :param track_list: dict, contiene le canzoni in particolare viene utilizzata la uri delle canzoni.
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
    }

    playlist_name = generi[0] + '_' + generi[1] + '_' + generi[2]
    data = '{"name":"' + str(playlist_name).replace(' ', '-') + '","description":"' + str(playlist_name).replace(' ', '-') + ' playlist","public":false}'

    user_id = get_user_id(access_token)
    response = requests.post('https://api.spotify.com/v1/users/' + user_id + '/playlists', headers=headers,
                             data=data)
    x = json.loads(response.text)
    playlist_id = x['id']

    add_items_playlist(access_token, playlist_id, track_list)
    print('Playlist creata con successo!')


def add_items_playlist(access_token, playlist_id, track_list):
    """
    Funzione che inserisce le canzoni all'interno della playist appena creata

    :param access_token: str, stringa generata da spotify.
    :param playlist_id: str, id della playlist creata.
    :param track_list: list, lista di dict conteneti informazioni legate alle canzoni da inserire
    :return: user_id: str, id dell'utente.
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
    }

    for track in track_list:
        params = (
            ('uris', track['uri']),
        )
        response = requests.post('https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks', headers=headers,
                                 params=params)


"""
if __name__ == '__main__':
    at = request_access_token()
    if at:
        playlist_id = request_playlist_id(at, 'grunge')
        tracklist = get_playlist_items(at, playlist_id, 10)
    else:
        playlist = None
    
    print(tracklist)
"""

