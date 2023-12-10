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
FORMS = {'tornadus': 'tornadus-incarnate',
         'thundurus': 'thundurus-incarnate',
         'landorus': 'landorus-incarnate',
         'enamorus' : 'enamorus-incarnate',
         'urshifu': 'urshifu-single-strike',
         'basculegion': 'basculegion-male',
         'mimikyu': 'mimikyu-disguised',
         'toxtricity': 'toxtricity-amped',
         'indeedee': 'indeedee-male',
         'eiscue': 'eiscue-ice',
         'lycanroc': 'lycanroc-midday',
         'oricorio': 'oricorio-baile',
         'morpeko': 'morpeko-full-belly',
         'basculin': 'basculin-red-striped'}


from pkmn_data import PokemonData
from pkmn_tiering import PokemonTiers
from pkmn_network import PokemonGraph


def to_api_names(names: list[str]=None) -> list[str]:
    renamed = []

    for p in names:
        p = p.lower()
        p = p.replace(' ', '-')
        p = p.replace("'", '')
        p = p.replace('wellspring', 'wellspring-mask')
        p = p.replace('hearthflame', 'hearthflame-mask')
        p = p.replace('cornerstone', 'cornerstone-mask')
        p = p.replace('paldea-blaze', 'paldea-blaze-breed')
        p = p.replace('paldea-combat', 'paldea-combat-breed')
        p = p.replace('paldea-aqua', 'paldea-aqua-breed')

        if p[-2:] == '-f':
            p = p.replace('-f', '-female')

        if p in FORMS.keys():
            p = FORMS[p]
        
        renamed.append(p)
    
    return renamed

def find_best_teammate(ranks: dict[str: float]=None, num_teammates: int=1, data: PokemonData=None, pokemon: str=None, typing: str=None, stat: str=None, stat_value: int=None) -> None:
    ranked = list(ranks.keys())
    api_named_ranked = []

    if typing or stat:
        # recreate the ranked pokemon strings to work with API
        api_named_ranked = to_api_names(ranked)

    if typing:
        typing = typing.lower()
        ranked = [p for i, p in enumerate(ranked) if data.get_type(api_named_ranked[i]) == typing]

    if stat and stat_value:
        stat = stat.lower()
        if stat == 'bst':
            ranked = [p for i, p in enumerate(ranked) if data.get_bst(api_named_ranked[i]) > stat_value]
        else:
            ranked = [p for i, p in enumerate(ranked) if data.get_base_stat(api_named_ranked[i], stat) > stat_value]

    if not pokemon:
        print('The best teammate(s) are:')
        print(*ranked[:num_teammates], sep='\n')
    
    if pokemon:
        print(f'The best teammate(s) for {pokemon} are:')
        print(*[p for p in ranked if p in data.get_teammates(pokemon)][:num_teammates], sep='\n')

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
    find_best_teammate(pr, 3, all_data, 'mamoswine')
    #find_best_teammate(pr, 2, all_data, typing='Fire')
    #find_best_teammate(pr, 3, all_data, stat='speed', stat_value=90)
    #find_best_teammate(pr, 5, all_data, stat='BST', stat_value=550)
    find_best_teammate(pr, 4, all_data,'MAMOSWINE', typing='Fire')

