'''
Handle getting best teammate(s) with support for filtering by type and/or stats
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

from pkmn_data import PokemonData
from pkmn_tiering import PokemonTiers
from pkmn_network import PokemonGraph


def find_best_teammate(ranks: dict[str: float]=None, num_teammates: int=1, pokemon: str=None, teammates: list[str]=None, typing: str=None, stat: str=None, stat_value: int=None) -> None:
    ranked = list(ranks.keys())

    if typing:
        pass

    if stat:
        pass

    if not pokemon:
        print('The best teammate(s) are:')
        print(*ranked[:num_teammates], sep='\n')
    
    if pokemon:
        print(f'The best teammate(s) for {pokemon} are:')
        print(*[p for p in ranked if p in teammates][:num_teammates], sep='\n')

if __name__ == '__main__':
    all_data = PokemonData(BASE_URL+TEST_MONTH_URL+TEST_FORMAT_URL)
    training_data = all_data.get_tiering_data()
    pkmn_tiers = PokemonTiers(training_data)

    tiers = pkmn_tiers.get_tiers(True)

    graph = PokemonGraph()
    edge_data = all_data.get_team_data()

    graph.build_graph(edge_data, tiers)
    pr = graph.get_pagerank(graph)

    find_best_teammate(pr, 6)
    find_best_teammate(pr, 3, 'mamoswine', all_data.get_teammates('mamoswine'))

