'''
Grab necessary data from API and Showdown JSONs
'''
BASE_URL = 'https://www.smogon.com/stats/'
TEST_MONTH_URL = '2023-11/'
TEST_FORMAT_URL = 'chaos/gen9vgc2023regulationebo3-1760.json'
STAT_TO_INDEX = {'hp': 0,
                 'attack': 1,
                 'defense': 2,
                 'special attack': 3,
                 'special defense': 4,
                 'speed': 5}


import pokebase as pb
import requests
from numpy import ndarray
import numpy as np


class PokemonData:
    '''
        A class for retrieving and processing Pokemon data from Smogon Showdown.

        Args:
        ps_url (str): The URL to the Smogon Showdown JSON data.

        Attributes:
        ps_data (dict): The parsed JSON data retrieved from the Smogon Showdown API.

        Methods:
        - get_all_pokemon(): Returns a list of all Pokemon in the JSON data.
        - get_type(pokemon: str): Returns the primary type of a given Pokemon.
        - get_base_stat(pokemon: str, stat: str): Returns the base stat of a given Pokemon for a specified stat.
        - get_bst(pokemon: str): Returns the Base Stat Total (BST) of a given Pokemon.
        - get_teammates(pokemon: str): Returns a list of Pokemon that have been used on the same team as the given Pokemon.
        - get_gxe_stats(pokemon: str): Returns the GXE (Global Usage Expectancy) stats of a given Pokemon.
        - get_tiering_data(): Returns a NumPy array containing Pokemon names and their corresponding GXE stats.
        - get_team_data(): Returns a dictionary containing Pokemon names as keys and their known teammates as values.
    '''
    def __init__(self, ps_url: str=None) -> None:
        '''
            Initializes the PokemonData class.

            Args:
            ps_url (str): The URL to the Smogon Showdown JSON data.
        '''
        self.ps_data = requests.get(ps_url).json()
    
    def get_all_pokemon(self) -> list[str]:
        '''
            Returns a list of all Pokemon in the JSON data.

            Returns:
            list[str]: A list of all Pokemon in the JSON data.
        '''
        return list(self.ps_data['data'].keys())  # return list of all PKMN in JSON

    def get_type(self, pokemon: str=None) -> str:
        '''
            Returns the primary type of a given Pokemon.

            Args:
            pokemon (str): The name of the Pokemon.

            Returns:
            str: The primary type of the given Pokemon.
        '''
        return pb.pokemon(pokemon.lower()).types[0].type.name  # return a PKMN's primary type
    
    def get_base_stat(self, pokemon: str=None, stat: str=None) -> int:
        '''
            Returns the base stat of a given Pokemon for a specified stat.

            Args:
            pokemon (str): The name of the Pokemon.
            stat (str): The name of the stat.

            Returns:
            int: The base stat of the given Pokemon for the specified stat.
        '''
        return pb.pokemon(pokemon.lower()).stats[STAT_TO_INDEX[stat.lower()]].base_stat  # return a PKMN's base stat
    
    def get_bst(self, pokemon: str=None) -> int:
        '''
            Returns the Base Stat Total (BST) of a given Pokemon.

            Args:
            pokemon (str): The name of the Pokemon.

            Returns:
            int: The Base Stat Total (BST) of the given Pokemon.
        '''
        return sum([pb.pokemon(pokemon.lower()).stats[STAT_TO_INDEX[stat.lower()]].base_stat for stat in STAT_TO_INDEX.keys()])  # return a PKMN's BST
    
    def get_teammates(self, pokemon: str=None) -> list[str]:
        '''
            Returns a list of Pokemon that have been used on the same team as the given Pokemon.

            Args:
            pokemon (str): The name of the Pokemon.

            Returns:
            list[str]: A list of Pokemon that have been used on the same team as the given Pokemon.
        '''
        return list(self.ps_data['data'][pokemon.lower().capitalize()]['Teammates'].keys())  # return PKMN that have been used on the same team as a PKMN

    def get_gxe_stats(self, pokemon: str=None) -> list[int]:
        '''
            Returns the GXE (Global Usage Expectancy) stats of a given Pokemon.

            Args:
            pokemon (str): The name of the Pokemon.

            Returns:
            list[int]: A list of three GXE stats for the given Pokemon.
        '''
        return self.ps_data['data'][pokemon]['Viability Ceiling'][1:]  # return a PKMN's 3 GXE stats
    
    def get_tiering_data(self) -> ndarray:
        '''
            Returns a NumPy array containing Pokemon names and their corresponding GXE stats.

            Returns:
            ndarray: A NumPy array containing Pokemon names and their corresponding GXE stats.
        '''
        all_pokemon_gxe = []  # empty list to append rows

        for pokemon in self.get_all_pokemon():  # create row of PKMN and its GXE stats
            current_pkmn = [pokemon]
            stats = self.get_gxe_stats(pokemon)
            current_pkmn.extend(stats)

            all_pokemon_gxe.append(current_pkmn)  # append row total data list
        
        return np.array(all_pokemon_gxe, dtype=object)  # return NP array dataset
    
    def get_team_data(self) -> dict[str: list[str]]:
        '''
            Returns a dictionary containing Pokemon names as keys and their known teammates as values.

            Returns:
            dict[str, list[str]]: A dictionary containing Pokemon names as keys and their known teammates as values.
        '''
        data = self.ps_data['data']  # get all data from JSON
        teammate_data = {}  # empty dictionary to add connections

        for pokemon in data.keys():  # for every PKMN
            teammate_data[pokemon] = data[pokemon]['Teammates']  # add to dict and its known teammates
        
        return teammate_data  # return all data needed for graph


if __name__ == '__main__':
    # # RUN TESTS ON GETTING THE DATA
    # charmander = pb.pokemon('charmander')
    # print(charmander.types[0].type.name)  # get its primary type
    # print(charmander.stats[0].stat.name)  # get its 0-index stat name
    # print(charmander.stats[0].base_stat)  # get its 0-index base stat

    # regulation_pull = requests.get(BASE_URL+TEST_MONTH_URL+TEST_FORMAT_URL)
    # regulation_data = regulation_pull.json()
    # # get its teammates
    # print(regulation_data['data']['Mamoswine']['Teammates'])
    # # get its GXE of top, top 1%, top 5%
    # print(regulation_data['data']['Mamoswine']['Viability Ceiling'][1:])
    
    all_data = PokemonData(BASE_URL+TEST_MONTH_URL+TEST_FORMAT_URL)

    print(all_data.get_type('Mamoswine'))  # ice
    print(all_data.get_base_stat('MamoswinE', 'HP'))  # 110
    print(all_data.get_bst('MAMOSWINE'))  # 530
    print(all_data.get_teammates('Mamoswine'))  # list of Pokemon
    #print(all_data.get_gxe_stats('mamoswine'))  # 3 GXEs
    print(all_data.get_all_pokemon())  # list of all Pokemon in format

    print(all_data.get_tiering_data())

