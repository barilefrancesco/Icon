"""
@author: Francesco Barile 677396
"""

import psycopg2
from texttable import Texttable
from email_requests import *


def create_db():
    """
    Creazione del database
    """
    # establishing the connection
    conn = psycopg2.connect(
        database="postgres", user='postgres'
    )
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing query to create a database
    sql = '''CREATE database music_db'''
    try:
        # Creating a database
        cursor.execute(sql)
        print("Database creato con successo.")
    except Exception as create_db_e:
        print(create_db_e)

    # Closing the connection
    conn.close()


def conn_db(user, database):
    """
    Funzione utilizzata per creare una connessione con il database.

    :param user: str, utente con cui accediamo al db.
    :param database: str, nome del database
    :return: dict, contiene le chiavi cursor e connection per effettuare le operazioni sul db selezionato.
    """
    connection = psycopg2.connect(user=user, database=database)
    return {"cursor": connection.cursor(), "connection": connection}


def conn_close_db(conn):
    """
    Funzione utilizzata per chiudere la connessione al database.

    :param conn: dict , connesione al database da chiudere.
    :return: boolean, True se la connesione viene chiusa correttamente, False altrimenti.
    """
    try:
        conn["cursor"].close()
        conn["connection"].close()
        return True
    except Exception as e:
        print(e)
        return False


def create_primary_genre():
    """
    Funzione che crea la tabella primary_genre
    """
    try:
        conn = conn_db('postgres', 'music_db')

        create_table_query = '''CREATE TABLE IF NOT EXISTS primary_genre
              (ID SERIAL PRIMARY KEY NOT NULL,
               NAME TEXT UNIQUE NOT NULL); '''

        conn["cursor"].execute(create_table_query)
        conn["connection"].commit()
        print("Table created successfully in PostgreSQL ")

        # closing database connection.
        if conn["connection"]:
            conn_close_db(conn)
            print("PostgreSQL connection is closed")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)


def create_sub_genre():
    """
    Funzione che crea la tabella sub_genre
    """
    try:
        conn = conn_db('postgres', 'music_db')

        create_table_query = '''CREATE TABLE IF NOT EXISTS sub_genre
              (ID SERIAL PRIMARY KEY NOT NULL,
               NAME TEXT UNIQUE NOT NULL,
               ID_PRIMARY_GENRE INT,
               FOREIGN KEY (ID_PRIMARY_GENRE)
                    REFERENCES primary_genre(ID)); '''

        conn["cursor"].execute(create_table_query)
        conn["connection"].commit()
        print("Table created successfully in PostgreSQL ")

        # closing database connection.
        if conn["connection"]:
            conn_close_db(conn)
            print("PostgreSQL connection is closed")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)


def create_genre():
    """
    Funzione che crea la tabella genre
    """
    try:
        conn = conn_db('postgres', 'music_db')

        create_table_query = '''CREATE TABLE IF NOT EXISTS genre
              (ID SERIAL PRIMARY KEY NOT NULL,
               NAME TEXT UNIQUE NOT NULL,
               ID_SUB_GENRE INT NULL,
               FOREIGN KEY (ID_SUB_GENRE)
                    REFERENCES sub_genre(ID)); '''

        conn["cursor"].execute(create_table_query)
        conn["connection"].commit()
        print("Table created successfully in PostgreSQL ")

        # closing database connection.
        if conn["connection"]:
            conn_close_db(conn)
            print("PostgreSQL connection is closed")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)


def create_artist():
    """
    Funzione che crea la tabella artist
    """
    try:
        conn = conn_db('postgres', 'music_db')

        create_table_query = '''CREATE TABLE IF NOT EXISTS artist
              (ID SERIAL PRIMARY KEY NOT NULL,
               NAME TEXT); '''

        conn["cursor"].execute(create_table_query)
        conn["connection"].commit()
        print("Table created successfully in PostgreSQL ")

        # closing database connection.
        if conn["connection"]:
            conn_close_db(conn)
            print("PostgreSQL connection is closed")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)


def create_genre_artist():
    """
    Funzione che crea la tabella genre_artist
    """
    try:
        conn = conn_db('postgres', 'music_db')

        create_table_query = '''CREATE TABLE IF NOT EXISTS genre_artist
              (ID SERIAL PRIMARY KEY NOT NULL,
               ID_ARTIST INT,
               ID_GENRE INT,
               FOREIGN KEY (ID_ARTIST)
                    REFERENCES artist(ID),              
               FOREIGN KEY (ID_GENRE)
                    REFERENCES genre(ID)); '''

        conn["cursor"].execute(create_table_query)
        conn["connection"].commit()
        print("Table created successfully in PostgreSQL ")

        # closing database connection.
        if conn["connection"]:
            conn_close_db(conn)
            print("PostgreSQL connection is closed")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)


def create_album():
    """
    Funzione che crea la tabella album
    """
    try:
        conn = conn_db('postgres', 'music_db')

        create_table_query = '''CREATE TABLE IF NOT EXISTS album
              (ID SERIAL PRIMARY KEY NOT NULL,
               TITLE TEXT,               
               ID_ARTIST INT,
               ID_GENRE INT,
               FOREIGN KEY (ID_ARTIST)
                    REFERENCES artist(ID),
               FOREIGN KEY (ID_GENRE)
                    REFERENCES genre(ID)); '''

        conn["cursor"].execute(create_table_query)
        conn["connection"].commit()
        print("Table created successfully in PostgreSQL ")

        # closing database connection.
        if conn["connection"]:
            conn_close_db(conn)
            print("PostgreSQL connection is closed")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while creating PostgreSQL table", error)


def populate_db():
    """
    Funzione che popola le tabelle del database attravero i file csv presenti nella cartella dedicata 'csv_files'
    """
    try:
        path = '/csv_files/'
        conn = conn_db('postgres', 'music_db')
        postgres_populate_primary_genre = """ COPY primary_genre(id, name) FROM '""" + path + 'primary_genre.csv' + \
                                          """' DELIMITER ',' CSV HEADER; """
        conn["cursor"].execute(postgres_populate_primary_genre)

        postgres_populate_sub_genre = """ COPY sub_genre(id, name, id_primary_genre) FROM '""" + path + \
                                      'sub_genre.csv' + """' DELIMITER ',' CSV HEADER; """
        conn["cursor"].execute(postgres_populate_sub_genre)

        postgres_populate_genre = """ COPY genre(id, name, id_sub_genre) FROM '""" + path + 'genres.csv' + \
                                  """' DELIMITER ',' CSV HEADER; """
        conn["cursor"].execute(postgres_populate_genre)

        postgres_populate_artist = """ COPY artist(id, name) FROM '""" + path + 'artists.csv' + \
                                   """' DELIMITER ',' CSV HEADER; """
        conn["cursor"].execute(postgres_populate_artist)

        postgres_populate_genre_artist = """ COPY genre_artist(id, id_artist, id_genre) FROM '""" + path + \
                                         'genres_artists.csv' + """' DELIMITER ',' CSV HEADER; """
        conn["cursor"].execute(postgres_populate_genre_artist)

        postgres_populate_album = """ COPY album(id, title, id_artist, id_genre) FROM '""" + path + \
                                  'albums.csv' + """' DELIMITER ',' CSV HEADER; """
        conn["cursor"].execute(postgres_populate_album)

        conn["connection"].commit()
        conn_close_db(conn)
    except Exception as populate_db_err:
        print(populate_db_err)


def crete_music_database():
    """
    Funzione che utilizza le funzioni precedenti per creare e popolare il database.
    """
    try:
        if conn_db('postgres', 'music_db'):
            pass  # Il database esiste
    except:
        create_db()
        create_primary_genre()
        create_sub_genre()
        create_genre()
        create_artist()
        create_genre_artist()
        create_album()
        populate_db()
        print('Creazione e popolazione avvenuta con successo.\n')


def backup_music_database():
    """
    Funzione che esegue il backup del database all'interno di file csv, posizionati nella cartella tmp del pc
    """
    try:
        path = '/tmp/'
        conn = conn_db('postgres', 'music_db')
        postgres_bp_prim_genre = """ COPY primary_genre(id, name) TO '""" + path + 'primary_genre.csv' + \
                                 """' DELIMITER ',' CSV HEADER;"""
        conn["cursor"].execute(postgres_bp_prim_genre)

        postgres_bp_sub_genre = """ COPY sub_genre(id, name, id_primary_genre) TO '""" + path + 'sub_genre.csv' + \
                                """' DELIMITER ',' CSV HEADER;"""
        conn["cursor"].execute(postgres_bp_sub_genre)

        postgres_bp_genre = """ COPY genre(id, name, id_sub_genre) TO '""" + path + 'genres.csv' + \
                            """' DELIMITER ',' CSV HEADER;"""
        conn["cursor"].execute(postgres_bp_genre)

        postgres_bp_artist = """ COPY artist(id, name) TO '""" + path + 'artists.csv' + \
                             """' DELIMITER ',' CSV HEADER;"""
        conn["cursor"].execute(postgres_bp_artist)

        postgres_bp_genre_artist = """ COPY genre_artist(id, id_artist, id_genre) TO '""" + path + \
                                   'genres_artists.csv' + """' DELIMITER ',' CSV HEADER;"""
        conn["cursor"].execute(postgres_bp_genre_artist)

        postgres_bp_album = """ COPY album(id, title, id_artist, id_genre) TO '""" + path + 'albums.csv' + \
                            """' DELIMITER ',' CSV HEADER;"""
        conn["cursor"].execute(postgres_bp_album)
        conn["connection"].commit()
        conn_close_db(conn)
        print('Backup eseguito con successo.\n')
    except Exception as bp_db_err:
        print(bp_db_err)


def draw_album_table(header, rows):
    """
    Funzione utilizzata per stamapre a video una tabella contenete tutti gli album corispondenti alla ricerca
    dell'utente.

    :param header: list, contiene gli elementi dell'header della tabella.
    :param rows: list, lista degli album da inseire nella tabella, con nome e generi associati ad esso.
    """
    t = Texttable()
    t.add_row(header)
    choose = 1
    for a in rows:
        t.add_row([choose, a['name'], a["name_genre"], a["name_artist"]])
        choose += 1
    print(t.draw())


def draw_artist_table(header, rows):
    """
    Funzione utilizzata per stamapre a video una tabella contenete tutti gli artisti corispondenti alla ricerca
    dell'utente.

    :param header: list, contiene gli elementi dell'header della tabella.
    :param rows: list, lista degli artist da inseire nella tabella, con nome e generi associati ad esso.
    """
    t = Texttable()
    t.add_row(header)
    choose = 1
    for a in rows:
        x = a['genre_1']
        for g in range(2, a["n_gen"]):
            x = x + ',' + a['genre_' + str(g)]
        t.add_row([choose, a['name'], x])
        choose += 1
    print(t.draw())


def search_album_db(conn, value):
    """
    Funzione che verifica se l'album inserito è presente nel database.

    :param conn: dict, connessione al database.
    :param value: str, nome dell'album di cui si verifica la presenza.
    :return: album_found: dict, contiene le informazioni relative all'album trovato.
    """
    list_album = []
    x = "'%" + str(value) + "%'"
    postgres_select_album_query = """ select id, title, id_artist, id_genre from album where LOWER(title) LIKE LOWER(""" + x + """) """
    conn["cursor"].execute(postgres_select_album_query)
    for row_alb in conn["cursor"].fetchall():
        context = {"name": row_alb[1], "id": row_alb[0], "id_artist": row_alb[2], "id_genre": row_alb[3]}
        #  Inserisco il nome del genere
        postgres_select_alb_genre_query = """ select name from genre where id=""" + "'" + str(
            row_alb[3]) + "'" + """ """
        conn["cursor"].execute(postgres_select_alb_genre_query)
        context["name_genre"] = str(conn["cursor"].fetchall()[0][0])

        #  Inserisco il nome dell'artista
        postgres_select_alb_artist_query = """ select name from artist where id=""" + "'" + str(
            row_alb[2]) + "'" + """ """
        conn["cursor"].execute(postgres_select_alb_artist_query)
        context["name_artist"] = str(conn["cursor"].fetchall()[0][0])
        #  Aggiungo l'album alla lista degli album trovati
        list_album.append(context)

    if not list_album:
        print('Album non trovato')
        while True:
            scelta = input('Vuoi chiedere all\'amministratore di inserire un album nel database? (y/n): ')
            if scelta.lower() == 'n':
                return None
            elif scelta.lower() == 's':
                email_sender(2, conn)
    else:
        if len(list_album) == 1:
            album_found = list_album[0]
            album_found = {"id": album_found["id"], "name": album_found["name"], "id_artista": album_found["id_artist"],
                           "artista": album_found["name_artist"], "id_genere": album_found["id_genre"],
                           "name_genre": album_found["name_genre"]}
            draw_album_table(['Choose', 'Name album', 'Genres', 'Artist'], list_album)
            while True:
                scelta = input('È Stato trovato soltanto questo album, confermi la scelta? (y/n): ')
                if scelta.lower() == 'n':
                    return None
                elif scelta.lower() == 'y':
                    return album_found
        else:
            draw_album_table(['Choose', 'Name album', 'Genres', 'Artist'], list_album)
            print('\nSono state trovate ' + str(len(list_album)) + ' istanze, scegli l\'album che stavi '
                  'cercando tra questi (inserisci il numero presente nella prima colonna, 0 se nessunoo di questi '
                  'corrisponde alla ricerca)')
            while True:
                scelta = input('Inserisci la tua scelta (da 1 a ' + str(len(list_album)) + '):')
                if 1 <= int(scelta) <= len(list_album):
                    break
                elif int(scelta) == 0:
                    return None
            album_found = list_album[int(scelta) - 1]
            album_found = {"id": album_found["id"], "name": album_found["name"], "id_artista": album_found["id_artist"],
                           "artista": album_found["name_artist"], "id_genere": album_found["id_genre"],
                           "name_genre": album_found["name_genre"]}
        return album_found


def search_artist_db(conn, value):
    """
    Funzione che verifica se l'artista è presente nel database.

    :param conn: dict, connessione al database.
    :param value: str, nome dell'artista di cui si verifica la presenza.
    :return: artists_found: dict, contiene le informazioni relative all'artista trovato.
    """
    list_artists = []
    x = "'%" + str(value) + "%'"
    postgres_select_artist_query = """ select id, name from artist where LOWER(name) LIKE LOWER(""" + x + """) """
    conn["cursor"].execute(postgres_select_artist_query)
    for row_art in conn["cursor"].fetchall():
        context = {"name": row_art[1], "id": row_art[0]}
        postgres_select_genres_query = """ select * from genre_artist where id_artist=""" + "'" + str(
            row_art[0]) + "'" + """ """
        conn["cursor"].execute(postgres_select_genres_query)
        count_genres = 1
        for row_genre in conn["cursor"].fetchall():
            postgres_select_genre_query = """ select name from genre where id=' """ + str(row_genre[2]) + """' """
            conn["cursor"].execute(postgres_select_genre_query)
            gen = conn["cursor"].fetchall()[0][0]
            if gen:
                context["genre_" + str(count_genres)] = gen
                count_genres += 1
        context["n_gen"] = int(count_genres)
        list_artists.append(context)

    if not list_artists:
        print('Artista non trovato')
        while True:
            scelta = input('Vuoi chiedere all\'amministratore di inserire un artista nel database? (y/n): ')
            if scelta.lower() == 'n':
                return None
            elif scelta.lower() == 'y':
                email_sender(1, conn)
    else:
        if len(list_artists) == 1:
            artist_found = list_artists[0]
            artist_found = {"id": artist_found["id"], "name": artist_found["name"]}
            draw_artist_table(['Choose', 'Name', 'Genres'], list_artists)
            while True:
                scelta = input('È Stato trovato soltanto questo artista, confermi la scelta? (y/n): ')
                if scelta.lower() == 'n':
                    return None
                elif scelta.lower() == 'y':
                    return artist_found
        else:
            draw_artist_table(['Choose', 'Name', 'Genres'], list_artists)
            print('\nSono state trovate le seguenti ' + str(len(list_artists)) +
                  ' istanze, scegli l\'artista che stavi cercando tra questi (inserisci il numero presente nella prima '
                  'colonna, 0 se nessunoo di questi corrisponde alla ricerca)')
            while True:
                scelta = input('Inserisci la tua scelta (da 1 a ' + str(len(list_artists)) + '):')
                if 1 <= int(scelta) <= len(list_artists):
                    break
                elif int(scelta) == 0:
                    return None
            artist_found = list_artists[int(scelta) - 1]
            artist_found = {"id": artist_found["id"], "name": artist_found["name"]}
        return artist_found


def get_genres_list_from_artist(artisti):
    """
    Funzione che prende in input la lista degli artisti e restiruisce la lista degli id dei generi associati.

    :param artisti: list, lista di artisti
    :return: genres: list, lista degli id relativi ai generi suonati dagli artisti.
    """
    genres = []
    conn = conn_db('postgres', 'music_db')
    for artista in artisti:
        try:
            postgres_select_genres_query = """ select id_genre from genre_artist where id_artist=' """ + str(
                artista["id"]) + """' """
            conn["cursor"].execute(postgres_select_genres_query)
            for g in conn["cursor"].fetchall():
                genres.append(g[0])
        except Exception as artist_genre_err:
            print(artist_genre_err)
    conn_close_db(conn)
    return genres


def get_artist_from_id(id_artist):
    """
    Funzione che prende in input l'id dell'artista e restituisce il suo nome.

    :param id_artist: str, id dell'artista.
    :return: art_name: str, nome dell'artista
    """
    conn = conn_db('postgres', 'music_db')
    query_for_id_sub_gen = """ select * from artist where id='""" + str(id_artist) + """' """
    conn["cursor"].execute(query_for_id_sub_gen)
    art_name = conn["cursor"].fetchall()[0]
    conn_close_db(conn)
    return art_name


def get_name_by_id_genre(id_genre):
    """
    Funzione che prende in input l'id del genere e restituisce il nome associato.

    :param id_genre: str, id del genere.
    :return: n_g: str, nome genere.
    """
    conn = conn_db('postgres', 'music_db')
    query_for_id_sub_gen = """ select name from genre where id='""" + str(id_genre) + """' """
    conn["cursor"].execute(query_for_id_sub_gen)
    n_g = conn["cursor"].fetchall()[0][0]
    conn_close_db(conn)
    return n_g


def get_id_sub_genre(id_genre):
    """
    Funzione che pardendo dall'id del genere, restituisce l'id del suo genere padre presente nella tabella sub_genre.

    :param id_genre: str, id genere dalla tabella genre
    :return: s_g: int, id sub_genre padre del genre 'id_genre'.
    """
    conn = conn_db('postgres', 'music_db')
    query_for_id_sub_gen = """ select id_sub_genre from genre where id='""" + str(id_genre) + """' """
    conn["cursor"].execute(query_for_id_sub_gen)
    s_g = conn["cursor"].fetchall()[0][0]
    conn_close_db(conn)
    return s_g


def get_id_prim_genre(id_sub_genre):
    """
    Funzione che pardendo dall'id del sub_genre, restituisce l'id del suo genere padre presente nella tabella
    primary_genre.

    :param id_sub_genre: str, id genere dalla tabella sub_genre
    :return: p_g: int, id primary_genre padre del genere 'id_sub_genre'.
    """
    conn = conn_db('postgres', 'music_db')
    query_for_id_prim_gen = """ select id_primary_genre from sub_genre where id='""" + str(id_sub_genre) + """' """
    conn["cursor"].execute(query_for_id_prim_gen)
    p_g = conn["cursor"].fetchall()[0][0]
    conn_close_db(conn)
    return p_g


def delete_genres_from_list(genres, pos_id_gen):
    """
    Funzione che restituisce la lista dei generi (id) sottoforma di stringa, escluso quello di riferimento in
    posizione 'pos_id_gen'.

    :param genres: list, lista degli id dei generi
    :param pos_id_gen: int, posizione del genere (id) da esclude dalla coppia in output.
    :return: str, composto da due generi (id).
    """
    if pos_id_gen == 0:
        return str(genres[1]) + ', ' + str(genres[2])
    elif pos_id_gen == 1:
        return str(genres[0]) + ', ' + str(genres[2])
    else:
        return str(genres[0]) + ', ' + str(genres[1])


def get_artist_list(genres, pos_id_gen, limit_num_artist):
    """
    Funzione che restituisce gli artisti che suonano il genere genres[pos_id_gen], escludendo gli altri due generi.

    :param genres: list,  lista di generi (id)
    :param pos_id_gen: int, posizione del genere da considerare per la lista di artisti in output.
    :param limit_num_artist: int, numero massimo di artisti da cercare all'interno del database.
    :return: list_artist: list, lista di artisti con id e nome, che suonano il genere genres[pos_id_gen], ma non gli
    altri due presenti in genres.
    """
    conn = conn_db('postgres', 'music_db')
    # Seleziono tutti gli artisti del genere indicato
    id_gen = genres[pos_id_gen]
    lista_genere_escludere = delete_genres_from_list(genres, pos_id_gen)

    select_artists_query = """ select id,name from artist
                               join (
                                     select distinct genre_artist.id_artist from genre_artist 
                                     join (
                                           select distinct genre_artist.id_artist from genre_artist 
                                           where genre_artist.id_genre in (""" + str(lista_genere_escludere) + """)
                                          ) as ga_ex on genre_artist.id_artist <> ga_ex.id_artist 
                                     where genre_artist.id_genre = '""" + str(id_gen) + """'
                                    ) as artisti_un_genere on artist.id = artisti_un_genere.id_artist
                               offset floor(random()*'""" + str(limit_num_artist) + """') 
                               limit '""" + str(limit_num_artist) + """' """
    conn["cursor"].execute(select_artists_query)

    list_artist = conn["cursor"].fetchall()

    conn_close_db(conn)
    return list_artist


def get_list_artist_three_genres(gen_list, input_artist_id_list):
    """
    Funzione che restituisce gli artisti che suonano tutti i generi della lista gen_list. (Potrebbe essere vuota)

    :param gen_list: list, lista dei generi (id).
    :param input_artist_id_list: list, lista degli artisti (id) inseriti dall'utente, da escludere nella ricerca.
    :return: lista_artisti: list, lista degli artisti trovati; None, se non viene trovato nessun artista.
    """
    s = ''
    for in_list in input_artist_id_list:
        s = s + '%s, '
    s = s[:-2]
    conn = conn_db('postgres', 'music_db')
    query = """ select * from artist where id in 
                (
                    select genre_artist.id_artist as id_artist_g3
                    from genre_artist 
                    join ( select genre_artist.id as id_row_g2, genre_artist.id_genre as id_genre_g2, 
                           genre_artist.id_artist as id_artist_g2, 
                           first_genre.id as id_row_g1, first_genre.id_genre as id_genre_g1, 
                           first_genre.id_artist as id_artist_g1 
                           from genre_artist 
                               join ( select * from genre_artist 
                                      where id_genre = '""" + str(gen_list[0]) + """') 
                               as first_genre 
                               on genre_artist.id_artist = first_genre.id_artist 
                               where genre_artist.id_genre = '""" + str(gen_list[1]) + """' 
                               order by genre_artist.id_artist
                         ) as second_genre
                    on genre_artist.id_artist = id_artist_g2
                    where genre_artist.id_genre = '""" + str(gen_list[2]) + """' and 
                          genre_artist.id_artist not in (
                                                         select id from artist 
                                                         where id in (""" + str(s) + """)
                                                        )
                    order by genre_artist.id_artist
                )
                limit 50;
    """
    conn["cursor"].execute(query, input_artist_id_list)
    lista_artisti = conn["cursor"].fetchall()
    # print(lista_artisti)

    conn_close_db(conn)
    if lista_artisti:
        return lista_artisti
    else:
        return None


def get_list_artist_two_genres(gen_list, input_artist_id_list):
    """
    Funzione che restituisce gli artisti che suonano due dei tre generi presenti nella lista 'gen_list'.

    :param gen_list: list, lista di generi (id).
    :param input_artist_id_list: list, lista di artisti inseriti dall'utente, da escludere nella query.
    :return: lista_artisti: list, lista degli artisti trovati; None, se non viene trovato nessun artista.
    """
    s = ''
    for in_list in input_artist_id_list:
        s = s + '%s, '
    s = s[:-2]
    conn = conn_db('postgres', 'music_db')
    query = """ select id, name from artist where id in 
                (
                    select genre_artist.id_artist
                    from genre_artist 
                    join ( 
                           select * from genre_artist 
                           where id_genre = '""" + str(gen_list[0]) + """'
                         ) as first_genre on genre_artist.id_artist = first_genre.id_artist 
                    where genre_artist.id_genre = '""" + str(gen_list[1]) + """' and 
                          genre_artist.id_artist not in (""" + str(s) + """)
                    order by genre_artist.id_artist
                )
                limit 50;
    """
    conn["cursor"].execute(query, input_artist_id_list)
    lista_artisti = conn["cursor"].fetchall()
    # print(lista_artisti)

    conn_close_db(conn)
    if lista_artisti:
        return lista_artisti
    else:
        return None


"""
if __name__ == '__main__':
    get_list_artist_three_genres([16, 13, 423], [397, 439])
    get_list_artist_two_genres([16, 229], [397, 439])
"""

"""
Mi è servito per inserire i sottogeneri, adesso li prendo direttamente dai file csv

root_prg/def_alter_genre().txt
"""
