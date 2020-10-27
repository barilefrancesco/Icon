"""
@author: Francesco Barile 677396
"""

import operator
import os

from email_requests import *
from markov_chains import *
from playlist_generator import *
from postgreSQL import *


def menu(flag_prob, flag_clas):
    """
    Funzione che mostra a video il menu di scelta.
    :param flag_prob: boolean, serve per verificare che siano stati inseriti gli artisti prima dell'esecuzione della
                      atena di Markov.
    :param flag_clas: boolen, verifica l'esecuzione della catena di Markov al fine di poter creare le classifiche e la playlist.
    :return: s: string, è l'ultima scelta effettuata.
    """
    if not flag_prob:
        print('Benvenuto.\n')
    while True:
        print('Scegli una delle seguenti opzioni:')
        print('(1) Richiedi l\'inserimento di un artista\n'
              '(2) Richiedi l\'inserimento di un album\n'
              '(3) Inserisci gli artisti\n'
              '(4) Inserisci gli album\n'
              '(5) Calcola la probabilità di preferenze\n'
              '(6) Genera la classifica degli artisti che potrebbero interessarti\n'
              '(7) Genera una playlist con spotify, in base alle tue preferenze di genere\n'
              '(8) Cancella le liste inserite\n'
              '(9) Esci\n')
        s = int(input('Inserisci la scelta: '))
        if s == 5 and not flag_prob:
            print('Non puoi calcolare una probabilità se non hai inserito almeno un artista!')
        elif s in [6, 7, 8] and not flag_clas:
            print('Non puoi generare una classifica se non hai calcolato la probabilità di preferenze di genere!')
        else:
            break
    return int(s)  # new last_input


def clear_console():
    """
    Funzione grafica per ripulire la console.
    """
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print(e)


def exit_from_input(name):
    """
    Funzione che serve per capire se l'utente ha intenzione di inserire un altro album o un altro artista.
    :param name: string, prende in input le stirnghe 'album' o 'artista'.
    :return: boolean, True, se l'utente desidera inserire un altro 'name', False altrimenti.
    """
    while True:
        exit_flag = input('Desideri inserire un altro ' + name + '? (y/n): ')
        if exit_flag.lower() == 'y':
            return True
        elif exit_flag.lower() == 'n':
            return False


def read_artists(conn_db, artist_list_saved):
    """
    Funzione utilizzata per prendere in input gli artisti preferiti di un utente.
    :param conn_db: dict, connessione al database.
    :param artist_list_saved: list, lista di artisti gia presenti nella lista.
    :return: artist_list_saved: list, lista degli artisti inseriti dall'utente più i nuovi altri.
    """
    while True:
        value = input('Inserisci un artista: ')
        arts_src = search_artist_db(conn_db, value)
        if arts_src is not None:
            if arts_src not in artist_list_saved:
                artist_list_saved.append(arts_src)
            else:
                print('L\'artista è già presente nella lista')
        if not exit_from_input('artista'):
            break

    return artist_list_saved


def read_albums(conn_db, album_list_saved):
    """
    Funzione utilizzata per prendere in input gli album preferiti di un utente.
    :param conn_db: ditc, connessione al database.
    :param album_list_saved: list, lista di album gia presenti nella lista.
    :return: album_list_saved: list, lista degli album inseriti dall'utente più i nuovi inseriti.
    """
    while True:
        value = input('Inserisci un album: ')
        alb_src = search_album_db(conn_db, value)
        if alb_src is not None:
            if alb_src not in album_list_saved:
                album_list_saved.append(alb_src)
            else:
                print('L\'album è già presente nella lista')
        if not exit_from_input('album'):
            break

    return album_list_saved


def priority_for_genres(artisti_genres, album_list=None):
    """
    Funzione che prende in input la lista degli ID di tutti i generi musicali eseguiti dagli artisti e degli album
    inseriti (album opzionali).
    Restituisce la lista con i primi tre generi in ordine di numero di occorrenze.
    La lista è influenzata dalla presenza degli album, questo significa che nel caso di molteplici generi con lo stesso
    numero di occorrenzze, i generi presenti sia in artisti che album verranno inseriti in lista, in maniera
    prioritaria, a discapito di generi con lo stesso numero di occorrenze, presenti solo tra gli artisti.
    :param artisti_genres: list, lista di tutti i generi musicali degli artisti inseriti in input.
    :param album_list: list, lista di Album, contiene tutti i dati relativi agli album inseriti
    :return: primi_tre_generi: list, lista di id id generi.
    """
    # Example values
    # x = get_genres_list_from_artist([{'id': 397, 'name': 'Alice in Chains'}, {'id': 476, 'name': 'Nirvana'}])
    # x = [6, 13, 16, 214, 228, 235, 244, 319, 422, 6, 16, 181, 228, 350, 403, 422]     (List of all genres chosen)
    count_for_genre = artisti_genres
    """
    Se sono stati inseriti anche gli album, inserisco gli id dei generi in due liste
    'count_for_genre' per calcolarmi il numero di occorrenze dei generi totale e
    'priority_genre' per calcolarmi la priorità in base ai generi degli album.
    """
    if album_list is not None:
        priority_genre = []
        for g_al in album_list:
            count_for_genre.append(g_al['id_genere'])
            priority_genre.append(g_al['id_genere'])

    """ Conto il numero di occorrenze dei generi e li ordino in maniera decrescente """
    count_for_genre = {i: count_for_genre.count(i) for i in count_for_genre}
    count_for_genre = sorted(count_for_genre.items(), key=operator.itemgetter(1), reverse=True)
    # print(count_for_genre)
    # print(priority_genre)

    """ Acquisisco i primi tre generi in ordine di numero di occorrenze """

    primi_tre_generi = []
    for i in range(3):
        primi_tre_generi.append(count_for_genre[i])

    # print(primi_tre_generi)

    """
    Se sono presenti gli album, controllo la priorità dei generi, altrimenti restituisco la lista 'primi_tre_generi'
    """
    if album_list is not None:
        """ Inserisco in 'pri_al_gen' le coppie genere-occorrenze di album, presenti in 'count_for_genre' """
        pri_al_gen = []
        for pg in priority_genre:
            for i in range(len(count_for_genre)):
                if count_for_genre[i][0] == pg:
                    pri_al_gen.append(count_for_genre[i])

        #  print(pri_al_gen)
        """ 
        Controllo che i generi in 'pri_al_gen' siano in 'primi_tre_generi', se non sono presenti, controllo che il 
        numero di occorrenze di un genere i presente nella lista 'primi_tre_generi' sia minore o uguale ad un genere in 
        'pri_al_gen' e in oltre per evitare ripetizione  primi_tre_generi di i non deve essere in 'priority_genre, solo 
        allora viene sostituito un genere in 'primi_tre_generi' con un genere in 'pri_al_gen'.
        """
        # check if pri_al_gen in primi_tre_generi
        for pag in range(len(pri_al_gen)):
            k = pri_al_gen[pag]
            flag = False
            for i in range(len(primi_tre_generi)):
                if primi_tre_generi[i] == k:
                    flag = True
                if flag:
                    break
            if not flag:
                for i in range(len(primi_tre_generi)):
                    if primi_tre_generi[i][1] <= k[1] and primi_tre_generi[i][0] not in priority_genre:
                        primi_tre_generi[i] = k
                        break
    # print(primi_tre_generi)
    return primi_tre_generi


def numero_occorenze(lista_generi):
    """
    Conta e restituisce il numero di occorrenze totali, presente nella lista
    :param lista_generi: list, lista dei generi con il rispettivo numero di occorrenze
    :return: count: int, numero di occorenze totali.
    """
    count = 0
    for occ in lista_generi:
        count = count + occ[1]
    return count


def num_artist_for_genre(lista_generi, n_of_artists=50):
    """
    Funzione che restituisce il numero di artisti da classificare in base alle occorrenze dei generi
    :param lista_generi: list, contiene id genere-occorrenze per ogni elemento della lista.
    :param n_of_artists: numero degli artisti da suddividere, se vuoto assume 50 di default.
    :return: n_art_list: list, lista del numero di artisti da classificare per genere.
    """
    n_art_list = []
    n = numero_occorenze(lista_generi)
    for l_g in lista_generi:
        n_art_list.append(int(n_of_artists * (l_g[1] / n)))
    return n_art_list


"""
Funzione usata in passato per la classificazione, al posto della query join usata attualmente,
per filtrare i generi e gli artisti.
def remove_input_artist(list_of_artist, input_artist_id_list, number_of_artists):
    for art in list_of_artist:
        if art[0] in input_artist_id_list:
            list_of_artist.remove(art)
            input_artist_id_list.remove(art[0])
        if not input_artist_id_list:  # Trovati gli artisti inseriti dall'utente
            break
    return list_of_artist[:number_of_artists]
"""


def genres_liked(genre_list):
    """
    Funzione che stampa a video il tasso percentuale di gradiemto dei generi selezionati.
    :param genre_list: list, lista di coppie id_genre-percenutale calcolata con la catena di Markov
    """
    for genre in genre_list:
        print(f'Gradisci il genere {get_name_by_id_genre(genre[0])} al {round(genre[1], 2)}%')
    print('')


def classifica_sigle_genre(n_art_list, single_genre_list):
    """
    Attravero le interrogazioni al database acquisisco gli artisti con uno ed uno solo dei tre generi in lista,
    successivamente vengono stampati a video attraverso una visualizzazione tabellare.
    :param n_art_list: list, lista del numero di artisti da acquisire per genere.
    :param single_genre_list: list, lista degli id_genre,
    :return: list_of_artist: list, lista di tutti gli artisti classificati.
    """
    list_of_artist = []
    for i in range(3):  # 3 come i generi che prendiamo in considerazione
        list_of_artist.append(get_artist_list(single_genre_list, i, n_art_list[i]))
    print('Classifica in base alle preferenze di genere:')
    for c in list_of_artist:
        draw_table_two_col(['ID ARTISTA', 'NOME'], c)
    return list_of_artist


def classifica_all_genres(gen_list, input_artist_id_list):
    """
    Funzione che stampa a video tutti gli artisti presenti nel database che hanno tutti e tre i generi
    della lista 'gen_list', sempre se esistono, altriementi prova a cercare gli artisti con coppie di generi.
    :param gen_list: list, lista degli id_genre
    :param input_artist_id_list: list, lista degli id degli artisti inseriti in input
    """
    classifica_tre_generi = get_list_artist_three_genres(gen_list, input_artist_id_list)
    if classifica_tre_generi:
        draw_table_two_col(['ID ARTISTA', 'NOME'], classifica_tre_generi)
        # return classifica_tre_generi
    else:
        print('Nessun artista presente nel database suona tutti e tre i generi classificati')
        print('classifica artisti per coppia di generi')
        lista_generi_nomi = [get_name_by_id_genre(gen_list[0]), get_name_by_id_genre(gen_list[1]),
                             get_name_by_id_genre(gen_list[2])]
        classifica_0_1 = get_list_artist_two_genres([gen_list[0], gen_list[1]], input_artist_id_list)
        classifica_0_2 = get_list_artist_two_genres([gen_list[0], gen_list[2]], input_artist_id_list)
        classifica_1_2 = get_list_artist_two_genres([gen_list[1], gen_list[2]], input_artist_id_list)
        if classifica_0_1:
            print(f'Classifica degli artisti che suonano i generi {lista_generi_nomi[0]} e {lista_generi_nomi[1]}')
            draw_table_two_col(['ID ARTISTA', 'NOME'], classifica_tre_generi)
        else:
            print(f'Classifica degli artisti che suonano i generi {lista_generi_nomi[0]} e {lista_generi_nomi[1]} '
                  f'è VUOTA')

        if classifica_0_2:
            print(f'Classifica degli artisti che suonano i generi {lista_generi_nomi[0]} e {lista_generi_nomi[2]}')
            draw_table_two_col(['ID ARTISTA', 'NOME'], classifica_tre_generi)
        else:
            print(f'Classifica degli artisti che suonano i generi {lista_generi_nomi[0]} e {lista_generi_nomi[2]} '
                  f'è VUOTA')

        if classifica_1_2:
            print(f'Classifica degli artisti che suonano i generi {lista_generi_nomi[1]} e {lista_generi_nomi[2]}')
            draw_table_two_col(['ID ARTISTA', 'NOME'], classifica_tre_generi)
        else:
            print(f'Classifica degli artisti che suonano i generi {lista_generi_nomi[1]} e {lista_generi_nomi[2]} '
                  f'è VUOTA')
        # return classifica_0_1 + classifica_0_2 + classifica_1_2


def get_genre_list(genres_occ):
    """
    Funzione che prende in input la lista delle coppie id_genre-occorrenze e restituisce la lista dei soli id_genre
    :param genres_occ: list, lista delle coppie id_genre-occorrenze
    :return: g_list: list,  la lista dei soli id_genre
    """
    g_list = []
    for g in genres_occ:
        g_list.append(g[0])
    return g_list


def draw_table_two_col(header, rows):
    """
    Funzione utilizzata per stampare a video una tabella generica di 2 o tre colonne.
    :param header: list, Contiene gli elementi dell'header della tabella.
    :param rows: list, lista degli artist da inseire nella tabella, con nome e generi associati ad esso.
    :return:
    """

    try:
        if len(rows[0]) == 2:
            t = Texttable()
            t.add_row(header)

            for r in rows:
                t.add_row([r[0], r[1]])
            print(t.draw())
        else:
            t = Texttable()
            t.add_row(header)
            for r in rows:
                t.add_row([r[0], r[1], r[2]])
            print(t.draw())
    except:
        # Entra in except quando la tabella non ha righe
        print('')


def draw_table_tracklist(header, rows):
    """
    Funzione utilizzata per stampare a video una tabella contenete i titoli dellec canzoni e rispettivi artisti.

    :param header: list, Contiene gli elementi dell'header della tabella.
    :param rows: list, tracklist da inseire nella tabella, con titolo e artista associati ad esso.
    """
    try:
        if len(rows[0]) == 2:
            t = Texttable()
            t.add_row(header)

            for r in rows:
                x = r['title']
                t.add_row([r['title'], r['artist']])
            print(t.draw())
        else:
            t = Texttable()
            t.add_row(header)
            for r in rows:
                t.add_row([r[0], r[1], r[2]])
            print(t.draw())
    except:
        # Entra in except quando la tabella non ha righe
        print('')


def create_playlist_from_music_genre(generi_list):
    """
    Funzione che partendo dai generi (id) e la loro percentuale di gradimento, restituisce una playlist di canzoni
    disponibili su spotify.
    :param generi_list: list, lista di coppie id_genre-percentuale gradimento.
    :return: tracklists: list, lista di dict contenete 'titolo' e 'artista'
    """
    at = request_access_token()
    tracklists = []
    for generi in generi_list:
        try:
            if at:
                playlist_id = request_playlist_id(at, get_name_by_id_genre(generi[0]))
                num_of_tracks = int(50*(generi[1]/100))
                tracklist = get_playlist_items(at, playlist_id, num_of_tracks)
            else:
                playlist = None
        except:
            print('Problemi con l\'access token')

        if tracklist not in tracklists:
            tracklists = tracklists + tracklist
            # tracklists.append(tracklist)
    draw_table_tracklist(['Titolo', 'Artista'], tracklist)
    return tracklists

    
if __name__ == '__main__':
    # Crea il database se non esiste
    crete_music_database()

    # Connesione al db
    conn = conn_db('postgres', 'music_db')
    # Imposto i flag per i controlli del menu (vedi def menu per dettagli)
    flag_p = False
    flag_c = False
    s = menu(flag_p, flag_c)
    # Liste degli artisti e degli album, vengono cancellati solo attraverso l'opportina scelta dal menu.
    artist_list = []
    album_list = []
    while True:
        if s == 1:
            """ Richiesta inseriemto artista al database tramite email """
            email_sender(1, conn)
        elif s == 2:
            """ Richiesta inseriemto album al database tramite email """
            email_sender(2, conn)
        elif s == 3:
            """ Inserimeto artisti """
            artist_list = read_artists(conn, artist_list)
            if artist_list:
                flag_p = True
            # print(artist_list)
        elif s == 4:
            """ Inserimeto album """
            album_list = read_albums(conn, album_list)
            # print(album_list)
        elif s == 5:
            """ Calcolo probabilità condizionata con la catena di Markov """
            flag_p = True
            generi_artisti = get_genres_list_from_artist(artist_list)
            if album_list:
                lista_generi = priority_for_genres(generi_artisti, album_list)
            else:
                lista_generi = priority_for_genres(generi_artisti)
            # print(lista_generi)
            result = markov_chains(lista_generi)
            genres_liked(result["single_genre"])
            flag_c = True
            # Es: [(16, 3), (13, 2), (132, 2)] coppie genere-occorrenze
        elif s == 6:
            # print('Genera classifica')
            """ CLASSIFICA PER GENERI PRESI SINGOLARMENTE (escludendo gli altri due) """
            num_artist_list = num_artist_for_genre(lista_generi)
            input_artist_id_list = []
            for input_artist in artist_list:
                input_artist_id_list.append(input_artist["id"])

            id_gen_list = get_genre_list(lista_generi)

            classifica_sigle_genre(num_artist_list, id_gen_list)

            """ Classifica artisti con tutti e tre i generi """
            print('Classifica con artisti che seguono tutti e tre i primi generi preferiti: ')
            classifica_all_genres(id_gen_list, input_artist_id_list)
        elif s == 7:
            """ Generazione playlist da spotify """
            create_playlist_from_music_genre(result["single_genre"])
        elif s == 8:
            """ Cancellazioni liste di artisti e album inseriti precedentemente """
            artist_list = []
            album_list = []
            print('Cancellazione eseguita.\n')
        elif s == 9:
            """ Condizione di uscita"""
            break
        # clear_console()
        s = menu(flag_p, flag_c)

    conn_close_db(conn)

    # Effettuo un backup del database
    backup_music_database()
    print('Bye.')
