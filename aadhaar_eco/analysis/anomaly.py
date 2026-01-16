import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AnomalyDetector:
    """
    Detects anomalous patterns in enrollment/transaction logs using Isolation Forest.
    """
    
    def __init__(self, contamination=0.01):
        # Contamination is the expected logical proportion of outliers
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def detect_spikes(self, df: pd.DataFrame, value_col: str, group_cols: list) -> pd.DataFrame:
        """
        Aggregates data by group_cols (e.g., State+Date) and finds Volume anomalies.
        """
        # 1. Aggregate
        daily_vol = df.groupby(group_cols)[value_col].sum().reset_index()
        
        # 2. Fit Isolation Forest on the Volume
        X = daily_vol[[value_col]]
        self.model.fit(X)
        
        # 3. Predict (-1 is anomaly, 1 is normal)
        daily_vol['anomaly'] = self.model.predict(X)
        daily_vol['anomaly_score'] = self.model.decision_function(X)
        
        # Filter only anomalies for return, or return full?
        # Let's return full but flagged
        return daily_vol
