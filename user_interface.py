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
    print('WELCOME!!!\nThis application can tell you what the ~BEST~ Pokémon teammates are--simply follow the prompts:\n')

def build_backend(url: str=None) -> tuple[PokemonData, PokemonTiers, PokemonGraph]:
    pass

def find_teammate(data: PokemonData=None, tiers: PokemonTiers=None, graph: PokemonGraph=None) -> bool:
    pass

def print_outro() -> None:
    print('THANK YOU\nWe hope you found some new teammates to use!\n')

if __name__ == '__main__':
    print_intro()

    data, tiers, graph = build_backend(BASE_URL + TEST_MONTH_URL + TEST_FORMAT_URL)

    while find_teammate(data, tiers, graph):
        continue

    print_outro()

    exit(0)

