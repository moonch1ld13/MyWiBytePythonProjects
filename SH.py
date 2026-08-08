import csv

#establishing all the funtions

def readcsvdata(tournament_name):
    filename = tournament_name + '.csv'
    with open(filename, mode = 'r') as file:
        csvFile = csv.DictReader(file)
        tournament_data = list(csvFile)

    return tournament_data


def reorder(winner_info_list, sorting_key, sorting_order):
    tt = sorted(winner_info_list, key = lambda x: x[sorting_key], reverse=(sorting_order == 'D'))
    return tt

def initialize():
    filename = 'classAnalysis.dat'
    with open(filename, mode = 'w') as file:
        file.write('Analysis Results\n')

def print_line(report_line):
    filename = 'classAnalysis.dat'

    with open (filename, mode = 'a') as file:
        file.write(report_line)

def print_table(table):
    filename = 'classAnalysis.dat'
    with open(filename, mode = 'a') as file:
        all_keys = list(table[0].keys())
        keys_line = ''

        for key in all_keys:
            keys_line = keys_line +key + (20 - len(key))*' '

        file.write(keys_line + '\n')

        for data in table:
            values_line = ''
            for values in data.values():
                values_line = values_line + str(values) + (20 - len(str(values)))*' '

            file.write(values_line + '\n') 


def print_set(winner_set):
    filename = 'classAnalysis.dat'
    
    with open (filename, mode = 'a') as file:
        for winner in winner_set:
            file.write(winner + ', ')

        file.write('\n\n')


def analyze(tname, tdata, sorting_key = 'Times Won', sorting_order = 'D'):

    winners_list = []


    for winner in tdata:
        winners_list.append(winner['Champion'])

    winners_set = set(winners_list)

    print_line('Analysis for ' + tname + '\n')
    print_line('Total winners ' + str(len(winners_set)) + '\n' )
    print_line('Unique winners ' + str(len(winners_set)) + '\n')


    winners_info_list = []


    for player in winners_set:
        player_info = {}
        selected = [chosen for chosen in tdata if chosen['Champion'] == player]

        player_info['Name'] = player
        player_info['Country'] = selected[0]['Country']
        player_info['Times Won'] = len(selected)
        player_info['Years Won'] = []
        for kk in selected:
            player_info['Years Won'].append(kk['Year'])

        winners_info_list.append(player_info)

    winners_info_sorted = reorder(winners_info_list, sorting_key, sorting_order)

    print_table(winners_info_sorted)
    print_line('\n')

    mto_winners_set = set()

    for player in winners_set:
        mto_winners_set.add(player)


    for player in winners_set:
        selected = [chosen for chosen in winners_info_list if chosen['Name'] == player]
        if selected[0]['Times Won'] == 1:
            mto_winners_set.remove(player)

    return winners_set, mto_winners_set


# Adding comparative analysis onto the data
def comparative_analysis(winner_set1, winner_set2):

    winner_eitheror = winner_set1 | winner_set2
    winner_both = winner_set1 & winner_set2
    winner_only1 = winner_set1 - winner_set2
    winner_only2 = winner_set2 - winner_set1
    winners_onlyone_notboth = winner_set1 ^ winner_set2

    print_line('Winners (Either/Or): ' + str(len(winner_eitheror)) + '\n')
    print_line('These players are : ' + '\n')
    print_set(winner_eitheror)
    
    print_line('Winners (Both): ' + str(len(winner_both)) + '\n')
    print_line('These players are : ' + '\n')
    print_set(winner_both)

    print_line('Winners (Only Wimbleton): ' + str(len(winner_only1)) + '\n')
    print_line('These players are : ' + '\n')
    print_set(winner_only1)

    print_line('Winners (Only French Open): ' + str(len(winner_only2)) + '\n')
    print_line('These players are : ' + '\n')
    print_set(winner_only2)

    print_line('Winners (Only 1,cnot both): ' + str(len(winners_onlyone_notboth)) + '\n')
    print_line('These players are : ' + '\n')
    print_set(winners_onlyone_notboth)
    
initialize()

wimbledon_data = readcsvdata('Wimbledon')
frenchopen_data = readcsvdata('FrenchOpen')

wimbledon_winners, wimbledon_mto_winners = analyze('Wimbledon', wimbledon_data)
frenchopen_winners, frenchopen_mto_winners = analyze('French Open', frenchopen_data)

comparative_analysis(wimbledon_winners, frenchopen_winners)
