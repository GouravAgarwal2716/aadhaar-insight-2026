import pandas as pd
import numpy as np

class PolicyAnalyzer:
    """
    Computes high-level governance indicators for UIDAI policy planning.
    Focuses on aggregated trends to ensure privacy.
    """

    @staticmethod
    def calculate_ghost_child_risk(enrolment_df: pd.DataFrame, demographic_df: pd.DataFrame) -> pd.DataFrame:
        """
        Idea 1: Ghost Child Awareness Indicator.
        Compares normalized Age 0-5 Enrolment volumes against Age 5-17 Demographic Updates.
        High Enrolment (0-5) but Low Updates (5-17) may indicate 'drop-off' or lack of continuity.
        """
        # Aggregate by District
        enrol_0_5 = enrolment_df.groupby(['state', 'district'])['age_0_5'].sum().reset_index()
        enrol_0_5.rename(columns={'age_0_5': 'enrolment_vol'}, inplace=True)
        
        # We need to be careful if 'demo_age_5_17' column exists or needs inference
        # Based on schema check: demographic df has 'demo_age_5_17'
        if 'demo_age_5_17' not in demographic_df.columns:
             # Fallback if specific column missing
             return pd.DataFrame()

        update_5_17 = demographic_df.groupby(['state', 'district'])['demo_age_5_17'].sum().reset_index()
        update_5_17.rename(columns={'demo_age_5_17': 'update_vol'}, inplace=True)
        
        # Merge
        merged = pd.merge(enrol_0_5, update_5_17, on=['state', 'district'], how='inner')
        
        # Calculate Risk Ratio (Avoid division by zero)
        # Risk = Enrolment Volume / (Update Volume + 1)
        # Higher Ratio = Potentially higher risk (Lots of kids entering, few updating later)
        # Note: This is an Aggregated Proxy, not longitudinal tracking.
        merged['continuity_ratio'] = merged['update_vol'] / (merged['enrolment_vol'] + 1)
        merged['risk_index'] = 1 / (merged['continuity_ratio'] + 0.001) 
        
        # Normalize Index 0-100
        merged['risk_score'] = (merged['risk_index'] - merged['risk_index'].min()) / \
                               (merged['risk_index'].max() - merged['risk_index'].min()) * 100
                               
        return merged.sort_values(by='risk_score', ascending=False)

    @staticmethod
    def analyze_youth_engagement(demographic_df: pd.DataFrame, biometric_df: pd.DataFrame) -> pd.DataFrame:
        """
        Idea 2: Youth Connection & Awareness Gap.
        Compare Demographic Updates (5-17) vs Biometric Updates (17+).
        """
        # Check columns
        if 'demo_age_5_17' not in demographic_df.columns or 'bio_age_17_' not in biometric_df.columns:
            return pd.DataFrame()
            
        demo_yg = demographic_df.groupby(['state'])['demo_age_5_17'].sum().reset_index()
        bio_adult = biometric_df.groupby(['state'])['bio_age_17_'].sum().reset_index()
        
        merged = pd.merge(demo_yg, bio_adult, on='state', how='inner')
        merged['engagement_gap'] = abs(merged['demo_age_5_17'] - merged['bio_age_17_'])
        
        return merged.sort_values(by='engagement_gap', ascending=False)

    @staticmethod
    def detect_migration_signals(demographic_df: pd.DataFrame) -> pd.DataFrame:
        """
        Idea 3: Migration Intelligence.
        High volume of demographic updates (address changes) in short periods.
        """
        # Group by District and Date
        daily_updates = demographic_df.groupby(['state', 'district', 'date']).size().reset_index(name='update_count')
        
        # Calculate Variance (Volatility)
        district_variance = daily_updates.groupby(['state', 'district'])['update_count'].var().reset_index()
        district_variance.rename(columns={'update_count': 'raw_volatility'}, inplace=True)
        
        # Z-Score Normalization
        mean_var = district_variance['raw_volatility'].mean()
        std_var = district_variance['raw_volatility'].std()
        district_variance['volatility_score'] = ((district_variance['raw_volatility'] - mean_var) / std_var).fillna(0)
        
        return district_variance.sort_values(by='volatility_score', ascending=False)

    @staticmethod
    def assess_kendra_performance(enrolment_df: pd.DataFrame, update_df: pd.DataFrame) -> pd.DataFrame:
        """
        Idea 5: Aadhaar Kendra Performance Signal.
        Assists in optimizing service center capacity.
        Logic: Combined volume of Enrolments + Updates per district.
        """
        # Aggregate Enrolment Volume
        e_vol = enrolment_df.groupby(['state', 'district']).size().reset_index(name='enrol_vol')
        
        # Aggregate Update Volume (Demographic)
        u_vol = update_df.groupby(['state', 'district']).size().reset_index(name='update_vol')
        
        # Merge
        perf_df = pd.merge(e_vol, u_vol, on=['state', 'district'], how='outer').fillna(0)
        perf_df['total_activity'] = perf_df['enrol_vol'] + perf_df['update_vol']
        
        # Normalize 0-100 (Performance Index)
        max_act = perf_df['total_activity'].max()
        perf_df['performance_score'] = (perf_df['total_activity'] / max_act * 100).round(1)
        
        # Assign Tiers
        conditions = [
            (perf_df['performance_score'] >= 80),
            (perf_df['performance_score'] >= 40),
            (perf_df['performance_score'] < 40)
        ]
        choices = ['High Load (Expansion Needed)', 'Optimal', 'Under-Utilized']
        perf_df['kendra_status'] = np.select(conditions, choices, default='Optimal')
        
        return perf_df.sort_values(by='performance_score', ascending=False)
