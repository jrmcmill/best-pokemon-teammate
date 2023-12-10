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
from pyvis.network import Network
import json
import webbrowser


class PokemonGraph:
    '''
        A class for creating a network graph of Pokemon where edges indicate teammates.

        Attributes:
        - graph (nx.DiGraph): A directed graph representing the Pokemon network.

        Methods:
        - __init__(): Initializes an empty directed graph.
        - build_graph(edges: dict[str: list[str]], tiers: dict[str: int]): Builds the graph using a dictionary of Pokemon edges and their tiers.
        - get_pagerank(graph: nx.DiGraph=None) -> dict[str: float]: Computes and returns the PageRank scores of the graph.
        - viz_graph(graph: nx.DiGraph=None): Visualizes the graph using the pyvis library and saves it as an HTML file.
    '''
    def __init__(self) -> None:
        '''
            Initializes an empty directed graph.
        '''
        self.graph = nx.DiGraph()

    def build_graph(self, edges: dict[str: list[str]], tiers: dict[str: int]) -> None:
        '''
            Builds the graph using a dictionary of Pokemon edges and their tiers.

            Args:
            - edges (dict[str: list[str]]): A dictionary where keys are Pokemon names and values are lists of teammates.
            - tiers (dict[str: int]): A dictionary where keys are Pokemon names and values are their tier levels.

            Returns:
            None
        '''
        for pokemon in edges.keys():  # for all pokemon
            for teammate in edges[pokemon]:  # and its teammates
                if teammate == 'empty':  # skip empty values
                    continue
                # add edge from teammate to pokemon
                self.graph.add_edge(teammate, pokemon)
                # add weight based on pokemon tier
                self.graph[teammate][pokemon]['weight'] = tiers[pokemon]
    
    @staticmethod
    def get_pagerank(graph: nx.DiGraph=None) -> dict[str: float]:
        '''
            Computes and returns the PageRank scores of the graph.

            Args:
            - graph (nx.DiGraph): The directed graph.

            Returns:
            dict[str: float]: A dictionary where keys are Pokemon names and values are their PageRank scores.
        '''
        scores = nx.pagerank(graph.graph)  # generate PageRank scores and sort them
        sorted_scores = dict(sorted(scores.items(), key=lambda score: score[1], reverse=True))
        
        return sorted_scores  # return highest to lowest scores
    
    @staticmethod
    def viz_graph(graph: nx.DiGraph=None) -> None:
        '''
            Visualizes the graph using the pyvis library and saves it as an HTML file.

            Args:
            - graph (nx.DiGraph): The directed graph.

            Returns:
            None
        '''
        graph = graph.graph
        net = Network(height='800px', width='100%')

        for node in graph.nodes:  # add nodes to viz
            net.add_node(node)

        for edge in graph.edges:  # and edges to viz
            source, target = edge
            net.add_edge(source, target, value=graph[source][target].get('weight', 1))

        net_options = {  # set viz options for less bounce lmfao
            'physics': {
                'enabled': True,
                'barnesHut': {'gravitationalConstant': -100000, 'springLength': 3000, 'springConstant': 0.001},
            },
            'edges': {'color': {'inherit': 'from'}, 'smooth': False},
        }

        net_options_str = json.dumps(net_options)  # as a proper JSON

        net.set_options(net_options_str)  # set and save
        net.write_html('graph.html')
        webbrowser.open('graph.html')  # this doesn't work for some reason


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

    graph.viz_graph(graph)

