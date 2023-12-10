'''
Create a network of Pokemon whose edges indicate teammates
'''
BASE_URL = 'https://www.smogon.com/stats/'
TEST_MONTH_URL = '2023-11/'
#TEST_MONTH_URL = '2020-06/'
TEST_FORMAT_URL = 'chaos/gen9vgc2023regulationebo3-1760.json'
#TEST_FORMAT_URL = 'chaos/gen8vgc2020-1760.json'
STAT_TO_INDEX = {'hp': 0,
                 'attack': 1,
                 'defense': 2,
                 'special attack': 3,
                 'special defense': 4,
                 'speed': 5}


from numpy import ndarray
import numpy as np
from pkmn_data import PokemonData
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


class PokemonTiers:
    '''
        A class for determining Pokemon tiers based on their Viability Ceiling scores.

        Attributes:
        - gxe_data (ndarray): NumPy array containing Pokemon names and their corresponding GXE scores.
        - num_tiers (int): The optimal number of tiers determined by the KMeans clustering algorithm.
        - model (KMeans): The KMeans clustering model.

        Methods:
        - __init__(gxe_data: ndarray=None): Initializes the PokemonTiers class with GXE data and sets up the clustering model.
        - get_num_tiers() -> int: Determines the optimal number of tiers using the silhouette score.
        - get_tiers(plotting: bool=False) -> dict[str: int]: Assigns Pokemon to tiers and optionally plots the results.
    '''
    def __init__(self, gxe_data: ndarray=None) -> None:
        '''
            Initializes the PokemonTiers class with GXE data and sets up the clustering model.

            Args:
            - gxe_data (ndarray): NumPy array containing Pokemon names and their corresponding GXE scores.
        '''
        self.gxe_data = gxe_data
        self.num_tiers = self.get_num_tiers()
        self.model = KMeans(self.num_tiers, n_init='auto')

    def get_num_tiers(self) -> int:
        '''
            Determines the optimal number of tiers using the silhouette score.

            Returns:
            int: The optimal number of tiers.
        '''
        X = self.gxe_data[:, 1:].astype(float)  # e.g., 65, 73, 81 per row
        best_score = -1  # set best score and optimal tiers to -1
        optimal_num_tiers = 1

        for n_clusters in range(2, 10):  # test different number of tiers
            model = KMeans(n_clusters, max_iter=50, n_init='auto')
            labels = model.fit_predict(X)  # with silhouette metric
            score = silhouette_score(X, labels)

            if n_clusters == 2:  # must be significantly better
                threshold = 2  # to pick 2 over 3
                if score > best_score + threshold:
                    best_score = score
                    optimal_num_tiers = n_clusters
            else:  # else continue past 2 clusters
                if score > best_score:
                    best_score = score
                    optimal_num_tiers = n_clusters
        
        return optimal_num_tiers  # return the number of tiers to be used

    def get_tiers(self, plotting: bool=False) -> dict[str: int]:
        '''
            Assigns Pokemon to tiers and optionally plots the results.

            Args:
            - plotting (bool): If True, plots the Pokemon tiers.

            Returns:
            dict[str: int]: A dictionary where keys are Pokemon names and values are their assigned tiers.
        '''
        X = self.gxe_data
        pokemon_names = X[:, 0]  # e.g., 'mamoswine' per row
        X_pokemon_gxe = X[:, 1:].astype(float)  # e.g., 65, 73, 81 per row

        self.model.fit(X_pokemon_gxe)

        combined_avg_gxe = np.mean(X_pokemon_gxe, axis=1)
        tier_avg_gxe = {}  # for assigning combined average GXE to tiers

        for label in range(self.num_tiers):  # reorder tiers by average GXE
            mask = (self.model.labels_ == label)
            avg_gxe = np.mean(combined_avg_gxe[mask])
            tier_avg_gxe[label] = avg_gxe
        
        sorted_tiers = sorted(tier_avg_gxe, key=tier_avg_gxe.get)
        name_tier_mapping = {}  # and assign PKMN labels to new tiers

        if plotting:
            fig = plt.figure(figsize=(7.25, 5.5))
            ax = fig.add_subplot(111, projection='3d')
            cmap = plt.cm.get_cmap('viridis', self.num_tiers)

        for label, tier in enumerate(sorted_tiers, start=1):
            mask = (self.model.labels_ == tier)

            for name in pokemon_names[mask]:  # assign PKMN to tier
                name_tier_mapping[name] = label
            
            if plotting:  # and plot it with its centroid
                ax.scatter(
                    X_pokemon_gxe[mask, 0], X_pokemon_gxe[mask, 1], X_pokemon_gxe[mask, 2],
                    label=f'pokémon of tier {label}', c=[cmap(label / (self.num_tiers + 1))]
                )

                centroid = self.model.cluster_centers_[tier]
                ax.scatter(
                    centroid[0], centroid[1], centroid[2], s=200, marker='o',
                    label=f'centroid tier {label}', c=[cmap(label / (self.num_tiers + 1))], edgecolors='black'
                )
        
        if plotting:
            ax.set_xlabel('top player')
            ax.set_ylabel('top 1% player')
            ax.set_zlabel('top 5% player')
            ax.set_title('Tiers of Pokémon (tier 1 is worst, tier N is best)')

            handles, labels = ax.get_legend_handles_labels()
            legend_elements = [(handle, label) for handle, label in zip(handles, labels)]

            fig.legend(*zip(*legend_elements[::-1]), loc='upper right', bbox_to_anchor=(1, 1))

            
            plt.show()
            plt.close()

        return name_tier_mapping  # return PKMN to tier


if __name__ == '__main__':
    all_data = PokemonData(BASE_URL+TEST_MONTH_URL+TEST_FORMAT_URL)
    training_data = all_data.get_tiering_data()
    pkmn_tiers = PokemonTiers(training_data)

    results = pkmn_tiers.get_tiers(True)

    print(results)

