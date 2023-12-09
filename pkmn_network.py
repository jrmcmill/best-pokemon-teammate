'''
Create a network of Pokemon whose edges indicate teammates
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


import networkx as nx
from pkmn_data import PokemonData
from pkmn_tiering import PokemonTiers


class PokemonGraph:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def build_graph(self, edges: dict[str: list[str]], tiers: dict[str: int]) -> None:
        for pokemon in edges.keys():
            for teammate in edges[pokemon]:
                # add edge from teammate to pokemon
                self.graph.add_edge(teammate, pokemon)
                # add weight based on pokemon tier
                self.graph[teammate][pokemon]['weight'] = tiers[pokemon]
    
    @staticmethod
    def get_pagerank(graph: nx.DiGraph=None) -> dict[str: float]:
        scores = nx.pagerank(graph.graph)
        sorted_scores = dict(sorted(scores.items(), key=lambda score: score[1], reverse=True))
        
        return sorted_scores


if __name__ == '__main__':
    all_data = PokemonData(BASE_URL+TEST_MONTH_URL+TEST_FORMAT_URL)
    training_data = all_data.get_tiering_data()
    pkmn_tiers = PokemonTiers(training_data)

    tiers = pkmn_tiers.get_tiers(True)

    graph = PokemonGraph()
    edge_data = all_data.get_team_data()

    graph.build_graph(edge_data, tiers)
    pr = graph.get_pagerank(graph)
    print(pr)

