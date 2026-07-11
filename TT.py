import csv
import random
from colorama import Fore

# Functions

def display_card(card):
    # Display the card in a clean format & spacing it out right
    k = list(card.keys())
    max_chars = len(max(k, key = len))

    #Printing the stats
    for keys in card:
        print(keys, (max_chars - len(keys))*' ', ':', card[keys])

def determine_winner(m1, m2, order = 1):
    dct = {'player': m1, 'computah': m2}
    v = list(dct.values())
    k = list(dct.keys())

    if m1 == m2:
        return 'draw'
    else:
        if order == 1:
            # larger is winner
            return k[v.index(max(v))]
        else:
            if 0.0 in v: # They are a heavenly restriction user
                print("The user is a heavenly restriction user, their cursed energy drops below the level even normal humans posses, 0. They have high agility and physical combat skills and can go undetected due to the lack of cursed energy!")
                return k[v.index(min(v))]
            else:
                return k[v.index(max(v))]
            

def best_category(card):
    # check if it's Toji or Maki first
    if float(card['CE']) == 0.0:
        return 'C' 
    
    # turning them into numbers it makes it a bit easier ;-;
    ce = float(card['CE'])
    hth = float(card['HtH'])
    i = float(card['Intellect'])
    a = float(card['Agility'])

    high_physical = max(hth, i, a)

    if high_physical >= 8.0:
        if high_physical == hth:
            return 'H'
        elif high_physical == i:
            return 'I'
        else:
            return 'A'
        
    # If they have lower physical stasts then it checks the CE reserve if they're HIGH on CE
    if ce > 9000:
        return 'C'
    
    # if the CE reserves are also bad, then just choose the highest physical stat
    if high_physical == hth:
        return 'H'
    elif high_physical == i:
        return 'I'
    else:
        return 'A'


#Introduce the game!

print(Fore.GREEN + "Welcome to the JJK themed Top Trumps game!")
print()
print("You and an opponent will be presented with different sorcerers, curses, and curse users from the world of Jujutsu Kaisen.")
print("When it's your turn, choose the right stat to use against your opponent in battle!")
print()
print("The stats include the individual's Cursed Technique(CT) or Ability if they don't have an innate technique, Cursed Energy(CE) reserves, Hand to Hand(HtH) combat skills, Intellect, and Agility.")
print()
print("Good luck!")
print(Fore.CYAN)
input("press enter to begin")
print()
print(Fore.WHITE)

# Read data and create a list of dictionaries
with open('jjk_tt.csv', mode = 'r') as file:
    csvFile = csv.DictReader(file)
    all_cards = list(csvFile)

# Only use the stats
relevant_keys = list(all_cards[0].keys())
relevant_keys = relevant_keys[2::]

# Shuffle and distribute the cards
random.shuffle(all_cards)
player_cards = all_cards[0::2]
computah_cards = all_cards[1::2]
table_cards = []

# Mapping Dictionary
mapping_dict = {}
for key in relevant_keys:
    mapping_dict[key[0]] = key          
    mapping_dict[key[0].lower()] = key  
    mapping_dict[key] = key             
    mapping_dict[key.lower()] = key


chance = random.choice(['player', 'computer'])
game_over = False

# Game loop
while not game_over:
    print()
    print(Fore.YELLOW +'player cards: ', len(player_cards), 'copmuter cards: ', len(computah_cards), 'table cards: ', len(table_cards)) 

    # Make sure the card at the top of the pile is the one being chosen
    player = player_cards.pop(0)
    computah = computah_cards.pop(0)

    table_cards.append(player)
    table_cards.append(computah)

    print()
    print(Fore.GREEN + "It's ", chance + "'s", ' turn now')

    print(Fore.WHITE)
    print('Your card is: ')
    print()
    display_card(player)
    print()


    # Choosing the stats
    if chance == 'player':
        chosen_key = input("Which stat do you choose?")
        chance = "computer"
    elif chance == "computer":
        input('press enter to continue')
        print()
        chosen_key = best_category(computah) #random.choice(list(mapping_dict.keys()))
        chance = "player"


    key_requested = mapping_dict[chosen_key]
    value_player = player[key_requested]
    value_comput = computah[key_requested]

    print()
    print(Fore.LIGHTBLUE_EX + 'Choosing ', "'", key_requested, "'")
    print()
    print("Player's ", "'", key_requested, "'", "is ", value_player)
    print()
    print("Computer ", "'", key_requested, "'", "is ", value_comput)
    print("The opponent's card was ", computah["Name"])
    print(Fore.WHITE)
    print()
    print()


    if key_requested in ['HtH', 'Intellect', 'Agility']:
        #Larger the better
        winner = determine_winner(float(value_player), float(value_comput))
    else:
        # This is here because heavenly restriction is really tricky as curse users/sorcerers use CE to feel the presence of others but heavenly restrictions brings the CE level down to 0, making them undetectable
        # CE is normally whoever has the highest reserves unless it's an individual with Heavenly Restriction (Only Toji and Maki <3)
        winner = determine_winner(float(value_player), float(value_comput), 0)

    print(Fore.LIGHTRED_EX + winner, " won!")
    print(Fore.WHITE)
    print()
    input('press enter to continue')

    # Things that happen after choosing the stats
    if winner == 'player':
        player_cards.extend(table_cards)
        table_cards.clear()
        chance = 'player' # This way the winner of the round can keep player just like in the real Top Trumps game (or at least they way I've played it)
    elif winner == 'computah':
        computah_cards.extend(table_cards)
        table_cards.clear()
        chance = 'computer'

    # Winning
    if len(player_cards) == 0:
        print(Fore.RED + "The computer won the game!")
        game_over = True
    elif len(computah_cards) == 0:
        print(Fore.GREEN + "You won the game!")
        game_over = True
