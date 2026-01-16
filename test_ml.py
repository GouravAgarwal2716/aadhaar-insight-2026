import pandas as pd
import sys
import os

sys.path.append(os.getcwd())
from aadhaar_eco.analysis.clustering import DistrictClusterer
from aadhaar_eco.analysis.anomaly import AnomalyDetector

def test_ml():
    # Mock Data
    data = {
        'state': ['A', 'A', 'B', 'B', 'C', 'C'],
        'district': ['d1', 'd2', 'd3', 'd4', 'd5', 'd6'],
        'age_0_5': [100, 200, 100, 50, 600, 100],
        'age_5_17': [300, 400, 300, 150, 800, 300],
        'date': pd.to_datetime(['2025-01-01']*6)
    }
    df = pd.DataFrame(data)
    
    print("Testing Clustering...")
    clusterer = DistrictClusterer(n_clusters=2)
    features = ['age_0_5', 'age_5_17']
    clustered_df, centers = clusterer.fit_predict(df, features)
    print("Clustered DF:")
    print(clustered_df.head())
    print("Centers:")
    print(centers)
    
    print("\nTesting Anomaly Detection...")
    detector = AnomalyDetector(contamination=0.1)
    # Mock Volume data (spike in one entry)
    vol_data = pd.DataFrame({
        'date': pd.to_datetime(['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05']),
        'count': [100, 105, 102, 5000, 101] # 5000 is anomaly
    })
    anomalies = detector.detect_spikes(vol_data, 'count', ['date'])
    print("Anomalies:")
    print(anomalies)

if __name__ == "__main__":
    test_ml()
