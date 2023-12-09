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
    def __init__(self, ps_url: str=None) -> None:
        self.ps_data = requests.get(ps_url).json()
    
    def get_all_pokemon(self) -> list[str]:
        return list(self.ps_data['data'].keys())

    def get_type(self, pokemon: str=None) -> str:
        return pb.pokemon(pokemon.lower()).types[0].type.name
    
    def get_base_stat(self, pokemon: str=None, stat: str=None) -> int:
        return pb.pokemon(pokemon.lower()).stats[STAT_TO_INDEX[stat.lower()]].base_stat
    
    def get_bst(self, pokemon: str=None) -> int:
        return sum([pb.pokemon(pokemon.lower()).stats[STAT_TO_INDEX[stat.lower()]].base_stat for stat in STAT_TO_INDEX.keys()])
    
    def get_teammates(self, pokemon: str=None) -> list[str]:
        return list(self.ps_data['data'][pokemon.lower().capitalize()]['Teammates'].keys())

    def get_gxe_stats(self, pokemon: str=None) -> list[int]:
        #return self.ps_data['data'][pokemon.lower().capitalize()]['Viability Ceiling'][1:]
        return self.ps_data['data'][pokemon]['Viability Ceiling'][1:]
    
    def get_tiering_data(self) -> ndarray:
        all_pokemon_gxe = []

        for pokemon in self.get_all_pokemon():
            current_pkmn = [pokemon]
            stats = self.get_gxe_stats(pokemon)
            current_pkmn.extend(stats)

            all_pokemon_gxe.append(current_pkmn)
        
        return np.array(all_pokemon_gxe, dtype=object)
    
    def get_team_data(self) -> dict[str: list[str]]:
        data = self.ps_data['data']
        teammate_data = {}

        for pokemon in data.keys():
            teammate_data[pokemon] = data[pokemon]['Teammates']
        
        return teammate_data


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

