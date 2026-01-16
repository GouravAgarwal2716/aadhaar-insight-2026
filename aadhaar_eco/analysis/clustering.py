import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Tuple

class DistrictClusterer:
    """
    Groups districts based on demographic profiles using K-Means.
    """
    
    def __init__(self, n_clusters=3):
        self.k = n_clusters
        self.model = KMeans(n_clusters=n_clusters, random_state=42)
        self.scaler = StandardScaler()

    def fit_predict(self, df: pd.DataFrame, feature_cols: list) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Fits the clustering model on district-level aggregates.
        Returns:
            - df_clustered: DataFrame with a 'Cluster' column.
            - centers: DataFrame defining the center of each cluster.
        """
        # 1. Aggregate by District
        # Sum the numerical features
        district_profile = df.groupby(['state', 'district'])[feature_cols].sum().reset_index()
        
        # 2. Normalize
        X = district_profile[feature_cols]
        X_scaled = self.scaler.fit_transform(X)
        
        # 3. Fit
        labels = self.model.fit_predict(X_scaled)
        district_profile['Cluster'] = labels
        
        # 4. Interpret Centers (inverse transform to get real values)
        centers = pd.DataFrame(self.scaler.inverse_transform(self.model.cluster_centers_), columns=feature_cols)
        centers['Cluster'] = range(self.k)
        
        return district_profile, centers
