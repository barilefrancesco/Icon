"""
@author: Francesco Barile 677396
"""
 
import smtplib
from email.mime.multipart import MIMEMultipart
import socket
from email.mime.text import MIMEText

#from decouple import config

from main import draw_table_two_col


def exit_from_genres_list():
    """
    Funzione per chiedere all'utente se desidera inserire un altro genere associato all'artista.
    
    :return: boolean, True se l'utente vuole inserire un nuovo genere, False altrimenti.
    """
    while True:
        exit_flag = input('Inserire un altro genere? (y/n): ')
        if exit_flag.lower() == 'y':
            return True
        elif exit_flag.lower() == 'n':
            return False


def email_sender(type, conn):
    """
    Funzione che manda la mail all'aministratore del sistema.
    
    :param type: int, valori possibili: 1, 2; 1 se la richiesta è relativa ad un artista, 2 se ad un album.
    :param conn: dict, connessione al database.
    :return: boolean, True se l'email è mandata con successo, False altriemnti.
    """
    sender_address = config('SENDER_EMAIL')
    sender_pass = config('PASSWORD_SENDER')
    receiver_address = config('RECEVER_EMAIL')

    message = MIMEMultipart()

    message['From'] = sender_address
    message['To'] = receiver_address

    if type == 1:
        message['Subject'] = "Richiesta per l'aggiunta di un nuovo ARTISTA"
        a = input('Inserisci l\'artista da voler aggiungere al database: ')
        g = []
        while True:
            genre = input('Inserisci un genere a cui appartiene l\'artista: ')
            postgres_select_genre_query = """ select name from genre where LOWER(name)=LOWER('""" + str(genre) + """') """
            conn["cursor"].execute(postgres_select_genre_query)
            result = conn["cursor"].fetchall()[0][0]
            if result:
                g.append(result)
                print('Genere inserito con successo.')
            else:
                print('Genere non trovato.')

            if not exit_from_genres_list():
                break

        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        mail_content = "L\'utente " + hostname + " con indirizzo IP: " + IPAddr + " richiede l'inserimento del seguente " \
                   "artista\n" + a + " con i relativi generi associati: " + str(g)

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Richiesta mandata con successo\n')
        return True
    else:
        message['Subject'] = "Richiesta per l'aggiunta di un nuovo ALBUM"
        while True:
            a = input('Inserisci l\'artista dell\'album da voler aggiungere al database: ')
            postgres_check_artista_query = """ select * from artist where LOWER(name) LIKE LOWER('%""" + str(a) + """%') """
            conn["cursor"].execute(postgres_check_artista_query)
            result = conn["cursor"].fetchall()
            if result:
                if len(result) == 1:
                    artist_found = result[0]
                    draw_table_two_col(['ID ARTISTA', 'NOME ARTISTA'], result)
                    while True:
                        scelta = input('È Stato trovato soltanto questo artista, confermi la scelta? (y/n): ')
                        if scelta.lower() == 'n':
                            flag = False
                            break
                        elif scelta.lower() == 'y':
                            flag = True
                            break
                    if flag:
                        break
                else:
                    draw_list = []
                    i = 1
                    for r in result:
                        draw_list.append([i, r[0], r[1]])
                        i += 1
                    draw_table_two_col(['Choose', 'Name', 'Genres'], draw_list)
                    print('\nSono state trovate ' + str(len(result)) +
                          ' istanze, scegli l\'artista che stavi cercando tra questi (inserisci il numero presente '
                          'nella prima colonna, 0 se nessunoo di questi corrisponde alla ricerca))')
                    while True:
                        scelta = input('Inserisci la tua scelta (da 1 a ' + str(len(result)) + '):')
                        if 1 <= int(scelta) <= len(result):
                            flag = True
                            break
                        elif int(scelta) == 0:
                            flag = False
                            break
                    if flag:
                        artist_found = result[int(scelta) - 1]
                        print('Artista inserito con successo.')
                        break
            else:
                print('L\'artista non è stato trovato.')

        nome_album = input('Inserisci il nome dell\'album: ')

        while True:
            genre = input('Inserisci il genere dell\'album: ')
            postgres_select_genre_query = """ select name from genre where LOWER(name)=LOWER('""" + str(genre) + """')"""
            conn["cursor"].execute(postgres_select_genre_query)
            result = conn["cursor"].fetchall()[0][0]
            if result:
                genre_found = result
                print('Genere trovato.')
                break
            else:
                print('Genere non trovato.')

        print('Invio email in corso. . .')
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        mail_content = "L\'utente " + hostname + " con indirizzo IP: " + IPAddr + " richiede l'inserimento del seguente " \
                   "album:\n" + nome_album + " con il relativo genere associato, " + str(genre_found) + \
                   ". \nDell\'artista: " + str(artist_found)

        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'plain'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        print('Richiesta mandata con successo\n')
        return True

    print('Richiesta fallita, riprovare.')
    return False
