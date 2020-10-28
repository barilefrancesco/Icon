"""
@author: Francesco Barile 677396
"""

import numpy as np
from postgreSQL import get_id_sub_genre, get_id_prim_genre


def normalize_transition_matrix(transition_matrix):
    """
    Funzione che serve per la normalizzazione dei valori presenti in 'transition_matrix' qualora la somma risulti
    maggiore o minore di 1.0
    
    :param transition_matrix: list of list, contiene le liste delle percentuali da normalizzare
    :return: transition_matrix: list of list, transition_matrix normalizzata.
    """
    for transition_mtx in transition_matrix:
        sum_inside_values = sum(transition_mtx)
        if sum_inside_values == 1.0:
            continue
        elif sum_inside_values < 1.0:
            i = transition_mtx.index(max(transition_mtx))
            while sum_inside_values < 1.0:
                transition_mtx[i] = transition_mtx[i] + 0.05
                if i == 2:
                    i = 0
                else:
                    i += 1
                sum_inside_values = sum(transition_mtx)
        else:  # sum_inside_values > 1.0
            i = transition_mtx.index(max(transition_mtx))
            while sum_inside_values > 1.0:
                if transition_mtx[i] - 0.05 != 0.05:
                    transition_mtx[i] = transition_mtx[i] - 0.05
                if i == 2:
                    i = 0
                else:
                    i += 1
                sum_inside_values = sum(transition_mtx)
    # print(transition_matrix)
    return transition_matrix


def set_work_values(lista_generi_occorrenze):
    """
    Funzione per creare le variabili di lavoro 'transition_matrix' e 'transition_name'.
    
    :param lista_generi_occorrenze: list, contiene la lista delle coppie genere (id)-occorrenze
    :return: dict, con 'states' lista di generi (id), 'transition_name'lista di nomi significativi per le transizioni e
            'transition_matrix' lista dei valori associati alle transizioni.
    """
    # The statespace
    states = []
    for g_o in lista_generi_occorrenze:
        states.append(g_o[0])

    # Possible sequences of events
    x11 = str(states[0]) + '-' + str(states[0])
    x13 = str(states[0]) + '-' + str(states[2])
    x12 = str(states[0]) + '-' + str(states[1])

    y31 = str(states[2]) + '-' + str(states[0])
    y33 = str(states[2]) + '-' + str(states[2])
    y32 = str(states[2]) + '-' + str(states[1])

    z21 = str(states[1]) + '-' + str(states[0])
    z23 = str(states[1]) + '-' + str(states[2])
    z22 = str(states[1]) + '-' + str(states[1])
    transition_name = [[x11, x13, x12], [y31, y33, y32], [z21, z23, z22]]

    # Probabilities matrix (transition matrix)
    transition_matrix = []
    for couple_list in transition_name:
        transition_list = []
        for couple in couple_list:
            tmp = couple.split('-')
            x = get_id_sub_genre(tmp[0])
            y = get_id_sub_genre(tmp[1])
            if tmp[0] == tmp[1] or x == y:  # Se il genere è uguale o il sotto genere è lo stesso imposto 0.2
                transition_list.append(0.2)
            else:
                x = get_id_prim_genre(x)
                y = get_id_prim_genre(y)
                if x == y:  # Se il genere primario è uguale imposto 0.4
                    transition_list.append(0.4)
                else:  # Se i genere sono completamente diversi imposto 0.6
                    transition_list.append(0.6)
        transition_matrix.append(transition_list)
    transition_matrix = normalize_transition_matrix(transition_matrix)
    return {'states': states, 'transition_name': transition_name, 'transition_matrix': transition_matrix}


def probable_genre_path(start_state, work_dict, n_states=2):
    """
    Geenra un percorso casuale di transizioni di genere, serve per calcolare la probabilità di gradimento dei generi.
    
    :param start_state: str, genere di partenza.
    :param work_dict: contiene il dict generato dalla funzione precedente.
    :param n_states: int, numero di stage che passimo, se non è settato, è impostato a 2.
    :return: genre_prob_list: list, lista di generi (id) attraversasti dalla catena.
    """
    # Choose the starting state
    status_genre = start_state
    genre_prob_list = [start_state]
    i = 0
    prob = 1
    while i != n_states:
        if status_genre == work_dict['states'][0]:
            # np.random.choice serve per scegleire una transition casuale
            change = np.random.choice(work_dict["transition_name"][0], replace=True,
                                      p=work_dict['transition_matrix'][0])
            if change == work_dict["transition_name"][0][0]:
                prob = prob * work_dict["transition_matrix"][0][0]
                genre_prob_list.append(work_dict['states'][0])
                pass
            elif change == work_dict["transition_name"][0][1]:
                prob = prob * work_dict["transition_matrix"][0][1]
                status_genre = work_dict['states'][2]
                genre_prob_list.append(work_dict['states'][2])
            else:
                prob = prob * work_dict["transition_matrix"][0][2]
                status_genre = work_dict['states'][1]
                genre_prob_list.append(work_dict['states'][1])
        elif status_genre == work_dict['states'][2]:
            change = np.random.choice(work_dict["transition_name"][1], replace=True,
                                      p=work_dict['transition_matrix'][1])
            if change == work_dict["transition_name"][1][1]:
                prob = prob * work_dict["transition_matrix"][1][1]
                genre_prob_list.append(work_dict['states'][2])
                pass
            elif change == work_dict["transition_name"][1][0]:
                prob = prob * work_dict["transition_matrix"][1][0]
                status_genre = work_dict['states'][0]
                genre_prob_list.append(work_dict['states'][0])
            else:
                prob = prob * work_dict["transition_matrix"][1][2]
                status_genre = work_dict['states'][1]
                genre_prob_list.append(work_dict['states'][1])
        elif status_genre == work_dict['states'][1]:
            change = np.random.choice(work_dict["transition_name"][2], replace=True,
                                      p=work_dict['transition_matrix'][2])
            if change == work_dict["transition_name"][2][2]:
                prob = prob * work_dict["transition_matrix"][2][2]
                genre_prob_list.append(work_dict['states'][1])
                pass
            elif change == work_dict["transition_name"][2][0]:
                prob = prob * work_dict["transition_matrix"][2][0]
                status_genre = work_dict['states'][0]
                genre_prob_list.append(work_dict['states'][0])
            else:
                prob = prob * work_dict["transition_matrix"][2][1]
                status_genre = work_dict['states'][2]
                genre_prob_list.append(work_dict['states'][2])
        i += 1
    return genre_prob_list


def percentage_rate_genre(start_status, end_status, work_dict, n_states=2):
    """
    Calcolo della percentuale basandoci sui valori ottenuti dalla funzione precedente ed iterandoli per 10 mila volte,
    per cercare di ottenere un risultato preciso.
    
    :param start_status:  str, genere di partenza, passata alla funzione 'probable_genre_path'.
    :param end_status: str, nome
    :param work_dict: contiene il dict generato dalla funzione 'set_work_values'.
    :param n_states: int, numero di stage della catena di Markov, se non è settato è impostato a 2 di default.
    :return: percentage: float, percentuale di gradiemento del genere 'end_status'
    """
    # Per salvare tutti i perscorsi
    list_path = []
    count = 0

    for iterations in range(1, 10000):
        list_path.append(probable_genre_path(start_status, work_dict, n_states))

    # print(list_path)

    # Controllo tutte le liste e cerco quelle che terminano con: 'end_status'
    for smaller_list in list_path:
        if smaller_list[1] == end_status:
            count += 1

    # Calcolo la probabilità che inizi con 'start_status' e termini con 'end_status'
    percentage = (count / 10000) * 100
    #print("La prob che parta da:'" + str(start_status) + "' e termini in:'" + str(end_status) +
    #      "'= " + str(percentage) + "%")
    return percentage


def markov_chains(lista_generi_occorrenze):
    """
    Funzione principale per il calcolo della percentuale di gradimento per ogni genere e fatto in due modi, con tre
    stage e successivamente con due.
    
    :param lista_generi_occorrenze: list, lista delle coppie genere(id)-occorrenze
    :return: result, dict, contiene tutte le percentuali calcolate dalle catene di Markov
    """
    work_dict = set_work_values(lista_generi_occorrenze)

    start_w_first_1 = percentage_rate_genre(work_dict["states"][0], work_dict["states"][0], work_dict)
    start_w_first_2 = percentage_rate_genre(work_dict["states"][0], work_dict["states"][1], work_dict)
    start_w_first_3 = percentage_rate_genre(work_dict["states"][0], work_dict["states"][2], work_dict)

    start_w_second_1 = percentage_rate_genre(work_dict["states"][1], work_dict["states"][0], work_dict)
    start_w_second_2 = percentage_rate_genre(work_dict["states"][1], work_dict["states"][1], work_dict)
    start_w_second_3 = percentage_rate_genre(work_dict["states"][1], work_dict["states"][2], work_dict)

    start_w_third_1 = percentage_rate_genre(work_dict["states"][2], work_dict["states"][0], work_dict)
    start_w_third_2 = percentage_rate_genre(work_dict["states"][2], work_dict["states"][1], work_dict)
    start_w_third_3 = percentage_rate_genre(work_dict["states"][2], work_dict["states"][2], work_dict)

    # print('- End for 3 states -')
    rate_first_three_s = (start_w_first_1 + start_w_second_1 + start_w_third_1) / 3
    rate_second_three_s = (start_w_first_2 + start_w_second_2 + start_w_third_2) / 3
    rate_third_three_s = (start_w_first_3 + start_w_second_3 + start_w_third_3) / 3
    """
    output = f'Rate artist with all genres:\n{work_dict["states"][0]} - {rate_first_three_s} %\n{work_dict["states"][1]} - ' \
             f'{rate_second_three_s} %\n{work_dict["states"][2]} - {rate_third_three_s} %\n '
    print(output)
    """
    start_w_first_1 = percentage_rate_genre(work_dict["states"][0], work_dict["states"][0], work_dict, 1)
    start_w_first_2 = percentage_rate_genre(work_dict["states"][0], work_dict["states"][1], work_dict, 1)
    start_w_first_3 = percentage_rate_genre(work_dict["states"][0], work_dict["states"][2], work_dict, 1)

    start_w_second_1 = percentage_rate_genre(work_dict["states"][1], work_dict["states"][0], work_dict, 1)
    start_w_second_2 = percentage_rate_genre(work_dict["states"][1], work_dict["states"][1], work_dict, 1)
    start_w_second_3 = percentage_rate_genre(work_dict["states"][1], work_dict["states"][2], work_dict, 1)

    start_w_third_1 = percentage_rate_genre(work_dict["states"][2], work_dict["states"][0], work_dict, 1)
    start_w_third_2 = percentage_rate_genre(work_dict["states"][2], work_dict["states"][1], work_dict, 1)
    start_w_third_3 = percentage_rate_genre(work_dict["states"][2], work_dict["states"][2], work_dict, 1)

    # print('- End for 2 states -')
    rate_first_two_s = (start_w_first_1 + start_w_second_1 + start_w_third_1) / 3
    rate_second_two_s = (start_w_first_2 + start_w_second_2 + start_w_third_2) / 3
    rate_third_two_s = (start_w_first_3 + start_w_second_3 + start_w_third_3) / 3
    """
    output = f'Rate artist with for genres:\n{work_dict["states"][0]} - {rate_first_two_s} %\n{work_dict["states"][1]} - ' \
             f'{rate_second_two_s} %\n{work_dict["states"][2]} - {rate_third_two_s} %\n '
    print(output)
    """
    result = {
        'all_genres': [(work_dict["states"][0], rate_first_three_s), (work_dict["states"][1], rate_second_three_s),
                       (work_dict["states"][2], rate_third_three_s)],
        'single_genre': [(work_dict["states"][0], rate_first_two_s), (work_dict["states"][1], rate_second_two_s),
                         (work_dict["states"][2], rate_third_two_s)]
        }
    return result
