'''
Create a network of Pokemon whose edges indicate teammates
'''
import networkx as nx
from pkmn_data import PokemonData


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
        return nx.pagerank(graph)
    
    def find_best_teammate(self, type: str=None, stat: str=None, stat_value: int=None) -> list[str]:
        self.get_pagerank(self.graph)  # need to add sorting by PageRank scores
        # and filtering by type and stat OR base-stat total (BST)


if __name__ == '__main__':
    pass

