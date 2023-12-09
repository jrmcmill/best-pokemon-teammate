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

def find_best_teammate(type: str=None, stat: str=None, stat_value: int=None) -> list[str]:
    pass
    #get_pagerank(graph)  # need to add sorting by PageRank scores
    # and filtering by type and stat OR base-stat total (BST)

