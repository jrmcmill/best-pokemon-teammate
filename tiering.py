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


from numpy import ndarray
import numpy as np
from pkmn_data import PokemonData
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class PokemonTiers:
    def __init__(self, gxe_data: ndarray=None) -> None:
        self.gxe_data = gxe_data
        self.num_tiers = self.get_num_tiers()
        self.model = KMeans(self.num_tiers)

    def get_num_tiers(self) -> int:
        X = self.gxe_data
        best_score = -1
        optimal_num_tiers = 1

        for n_clusters in range(2, 10):
            model = KMeans(n_clusters, max_iter=50, n_init=1)
            labels = model.fit_predict(X)
            score = silhouette_score(X, labels)

            if score > best_score:
                best_score = score
                optimal_num_tiers = n_clusters
        
        return optimal_num_tiers

    def get_tiers(self) -> dict[str: int]:
        X = self.gxe_data
        pokemon_names = X[:, 0]  # e.g., 'mamoswine' per row
        X_pokemon_gxe = X[:, 1].astype(float)  # e.g., 65, 73, 81 per row

        self.model.fit(X_pokemon_gxe)

        combined_avg_gxe = np.mean(X_pokemon_gxe, axis=1)
        tier_avg_gxe = {}  # for assigning combined average GXE to tiers

        for label in range(self.num_tiers):
            mask = (self.model.labels_ == label)
            avg_gxe = np.mean(combined_avg_gxe[mask])
            tier_avg_gxe[label] = avg_gxe
        
        sorted_tiers = sorted(tier_avg_gxe, key=tier_avg_gxe.get, reverse=True)
        name_tier_mapping = {}

        for label, tier in enumerate(sorted_tiers, start=self.num_tiers):
            mask = (self.model.labels_ == label)

            for name in pokemon_names[mask]:
                name_tier_mapping[name] = tier

        return name_tier_mapping


if __name__ == '__main__':
    pass

