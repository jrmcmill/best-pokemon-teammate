'''
Handle user interaction with program via CLI
'''
BASE_URL = 'https://www.smogon.com/stats/'
TEST_MONTH_URL = '2023-11/'
TEST_FORMAT_URL = 'chaos/gen9vgc2023regulationebo3-1760.json'


from pkmn_data import PokemonData
from pkmn_tiering import PokemonTiers
from pkmn_network import PokemonGraph
from best_teammate import find_best_teammate


def print_intro() -> None:
    '''
        Print the introduction message for the program.

        Returns:
        None
    '''
    print('WELCOME!!!\nThis application can tell you what the ~BEST~ Pokémon teammates are--simply follow the prompts (QUIT at any time by entering "quit"):\n')

def find_teammate() -> bool:
    '''
        Handle user interaction for finding the best Pokemon teammate(s).

        Returns:
        bool: True if the user wants to find teammates again, False otherwise.
    '''
    # handle display plots to user
    plotting = input('Do you want to view the behind-the-scenes plots? (enter "yes" to enable or anything else to disable): ').lower().strip()
    
    if plotting == 'quit':
        return False
    elif plotting == 'yes':
        plotting = True
    else:
        plotting = False
    
    # handle loading necessary objects and data
    print('Loading Pokémon data...\n')

    all_data = PokemonData(BASE_URL+TEST_MONTH_URL+TEST_FORMAT_URL)
    training_data = all_data.get_tiering_data()
    pkmn_tiers = PokemonTiers(training_data)
    tiers = pkmn_tiers.get_tiers(plotting=plotting)
    graph = PokemonGraph()
    edge_data = all_data.get_team_data()
    
    graph.build_graph(edge_data, tiers)

    pr = graph.get_pagerank(graph)

    if plotting:
        graph.viz_graph(graph)

    print('Pokémon data loaded!\n')

    # handle getting best teammate(s)
    pokemon = input('Would you like to start with a Pokémon? Enter a name if so, or leave this blank if you just want the best general teammates: ').lower().strip()

    if pokemon == 'quit':
        return False
    
    typing = input('Would you like to only get back best teammates of a certain primary type? Enter a primary type if so, or leave this blank if you want all types: ').lower().strip()

    if typing == 'quit':
        return False
    
    stat = input('Would you like to filter by a stat or by base-stat total? Enter a stat name or "bst" if so, or leave this blank if you want all stats: ').lower().strip()
    value = 0

    if stat == 'quit':
        return False
    elif stat in ('hp', 'attack', 'defense', 'special attack', 'special defense', 'speed', 'bst'):
        value = input('Enter a value for the stat or BST: ').lower().strip()

        if value == 'quit':
            return False
        
        try:
            value = int(value)
        except TypeError:
            print('ERROR: Invalid entry! Please try again...')

            return True
    else:
        print('ERROR: invalid entry! Please try again...')

        return True
    
    num_teammates = input('Enter how many teammates you want: ')

    if num_teammates == 'quit':
        return False
    
    try:
        num_teammates = int(num_teammates)
    except ValueError:
        print('ERROR: Invalid entry! Please try again...')

        return True
    
    print('Now finding best teammate(s)...\n')
    
    # take all inputs and return results
    find_best_teammate(ranks=pr, num_teammates=num_teammates, data=all_data, pokemon=pokemon, typing=typing, stat=stat, stat_value=value)

    # handle if user wants to do this again
    run_again = input('\nWould you like to find teammates again? Enter "yes" if so, or anything else to quit: ').lower().strip()

    if run_again == 'quit':
        return False
    
    if run_again == 'yes':
        return True
    else:
        return False

def print_outro() -> None:
    '''
        Print the outro message for the program.

        Returns:
        None
    '''
    print('\nTHANK YOU\nWe hope you found some new teammates to use!\n')

if __name__ == '__main__':
    # do it all!!!
    print_intro()

    while find_teammate():
        continue

    print_outro()

    exit(0)

