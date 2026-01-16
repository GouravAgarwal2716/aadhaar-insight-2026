import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px

# Check if running from correct dir, if not add to path
sys.path.append(os.getcwd())

from aadhaar_eco.data.loader import DataLoader
from aadhaar_eco.data.cleaner import DataCleaner
from aadhaar_eco.analysis.eda import EDAService
from aadhaar_eco.analysis.clustering import DistrictClusterer
from aadhaar_eco.analysis.anomaly import AnomalyDetector
from aadhaar_eco.analysis.policy import PolicyAnalyzer

st.set_page_config(page_title="Aadhaar Insight", layout="wide", page_icon="🆔")

# Apply custom dark theme CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base_path = "C:\\Users\\goura\\OneDrive\\Desktop\\UIDAI Hackathon"
    loader = DataLoader(base_path)
    data = loader.load_all()
    
    # Clean Data
    for cat in data:
        data[cat] = DataCleaner.process(data[cat])
    
    return data

def main():
    st.title("🆔 Aadhaar Insight: National Governance Intelligence Framework")
    st.markdown("### 🏛️ Data-Driven Policy | Operational Integrity | Social Inclusion")
    
    with st.spinner("Loading and Consolidating Multi-Source Data..."):
        try:
            data = load_data()
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return

    if not data:
        st.warning("No data loaded. Check paths.")
        return

    # Sidebar Controls
    st.sidebar.header("Configuration")
    category = st.sidebar.selectbox("Select Dataset Analysis", list(data.keys()))
    df = data[category]

    # Privacy Sidebar
    st.sidebar.markdown("---")
    st.sidebar.info("🔒 **Data Ethics & Privacy:**\nThis system uses only aggregated UIDAI hackathon datasets. No personal, biometric, or identifiable data is processed or inferred.")


    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📍 Regional Intelligence", "🧠 ML Clustering", "🚨 Anomaly Radar", "🏛️ Governance Actions"])

    with tab1:
        st.subheader(f"Dataset Overview: {category.title()}")
        stats = EDAService.get_basic_stats(df)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Rows", f"{stats['rows']:,}")
        c2.metric("Columns", len(stats['columns']))
        if stats['date_range']:
            c3.metric("Date Range", f"{stats['date_range'][0].strftime('%Y-%m-%d')} to {stats['date_range'][1].strftime('%Y-%m-%d')}")
        
        st.markdown("#### Trend Over Time")
        # Identify numeric column for plotting
        numerics = df.select_dtypes(include=['number']).columns.tolist()
        numeric_col = st.selectbox("Select Metric for Trend", numerics, index=min(3, len(numerics)-1))
        
        fig = EDAService.plot_trend(df, value_col=numeric_col)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            # Insight Card
            insight = EDAService.generate_trend_insight(df, value_col=numeric_col)
            st.info(insight)

    with tab2:
        st.subheader("Regional Performance")
        if 'state' in df.columns:
            st.markdown("#### Top States by Activity")
            # Reuse metric selection from Tab 1 or new one?
            state_metric = st.selectbox("Select Metric for State View", numerics, index=min(3, len(numerics)-1))
            fig_state = EDAService.plot_state_distribution(df, value_col=state_metric)
            st.plotly_chart(fig_state, use_container_width=True)
            st.caption(EDAService.generate_distribution_insight(df, group_col='state', value_col=state_metric))
            
            st.markdown("#### District Deep Dive")
            selected_state = st.selectbox("Filter by State", ["All"] + sorted(df['state'].unique().tolist()))
            if selected_state != "All":
                state_df = df[df['state'] == selected_state]
                fig_dist = EDAService.plot_state_distribution(state_df, state_col='district', value_col=state_metric)
                st.plotly_chart(fig_dist, use_container_width=True)
                st.caption(EDAService.generate_distribution_insight(state_df, group_col='district', value_col=state_metric))

    with tab3:
        st.subheader("Demographic Clustering (K-Means)")
        st.markdown("Groups districts based on similar profiles to identify 'Under-served' or 'High-Activity' regions.")
        
        # User selection for Clustering Features
        cluster_feats = st.multiselect("Select Feature for Profiling", numerics, default=numerics[:2])
        
        if len(cluster_feats) < 2:
            st.warning("Select at least 2 features for clustering.")
        else:
            if st.button("Run Clustering Model"):
                clusterer = DistrictClusterer(n_clusters=3)
                clustered_df, centers = clusterer.fit_predict(df, cluster_feats)
                
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    st.markdown("**Cluster Assignments**")
                    # Visualizing Clusters (PCA or 2D scatter)
                    fig_cluster = px.scatter(clustered_df, x=cluster_feats[0], y=cluster_feats[1], 
                                            color='Cluster', hover_data=['district', 'state'],
                                            title="District Clusters")
                    st.plotly_chart(fig_cluster, use_container_width=True)
                
                with c2:
                    st.markdown("**Cluster Profiles (Centroids)**")
                    st.dataframe(centers)

    with tab4:
        st.subheader("Anomaly Detection (Isolation Forest)")
        st.markdown("Identifies unusual spikes or drops in daily activity which could indicate **Fraud** or **System Outages**.")
        
        anomaly_metric = st.selectbox("Select Metric for Anomalies", numerics, index=min(3, len(numerics)-1))
        contamination = st.slider("Anomaly Sensitivity (Contamination)", 0.001, 0.05, 0.01)
        
        if st.button("Detect Anomalies"):
            detector = AnomalyDetector(contamination=contamination)
            # Group by Date
            anomalies = detector.detect_spikes(df, anomaly_metric, ['date'])
            
            # Scatter Plot: Normal vs Anomaly
            fig_anom = px.scatter(anomalies, x='date', y=anomaly_metric, 
                                  color=anomalies['anomaly'].astype(str),
                                  color_discrete_map={'1': 'blue', '-1': 'red'},
                                  title=f"Anomaly Detection on {anomaly_metric}")
            
            st.plotly_chart(fig_anom, use_container_width=True)
            
            st.markdown("#### Flagged Anomalies")
            st.dataframe(anomalies[anomalies['anomaly'] == -1].sort_values(by=anomaly_metric, ascending=False))

    with tab5:
        st.subheader("🏛️ National Governance Intelligence Framework")
        st.markdown("Automated indicators for Policy, Inclusion, and Operations.")
        
        if 'enrolment' not in data or 'demographic' not in data or 'biometric' not in data:
            st.error("⚠️ All datasets (Enrolment, Demographic, Biometric) are required for full Governance Analysis.")
        else:
            # 1. Ghost Child Indicator
            st.markdown("### 1️⃣ Ghost Child Risk Indicator")
            c1, c2 = st.columns([3, 1])
            with c1:
                risk_df = PolicyAnalyzer.calculate_ghost_child_risk(data['enrolment'], data['demographic'])
                if not risk_df.empty:
                    st.dataframe(risk_df[['state', 'district', 'risk_score']].head(5), hide_index=True, use_container_width=True)
                else:
                    st.info("Insufficient data.")
            with c2:
                st.success("**Suggested Governance Action:**\nLaunch targeted 'Bal Aadhaar' update camps in these top 5 districts. Partner with local Anganwadis.")
                st.caption(f"ℹ️ **Reliability:** Based on normalized continuity ratio of 0-5 Enrolments vs 5-17 Updates.")

            st.divider()

            # 2. Youth Disconnect
            st.markdown("### 2️⃣ Youth Disconnect Indicator")
            c1, c2 = st.columns([3, 1])
            with c1:
                gap_df = PolicyAnalyzer.analyze_youth_engagement(data['demographic'], data['biometric'])
                if not gap_df.empty:
                    st.dataframe(gap_df[['state', 'engagement_gap']].head(5), hide_index=True, use_container_width=True)
            with c2:
                st.warning("**Suggested Governance Action:**\nInitiate SMS campaigns for 18+ Mandatory Biometric Updates in these states.")
                st.caption("ℹ️ **Reliability:** Derived from volume gap between adolescent demographic updates and adult biometric conversions.")

            st.divider()

            # 3. Migration Signals
            st.markdown("### 3️⃣ Migration Signal Index")
            c1, c2 = st.columns([3, 1])
            with c1:
                mig_df = PolicyAnalyzer.detect_migration_signals(data['demographic'])
                if not mig_df.empty:
                    st.dataframe(mig_df[['state', 'district', 'volatility_score']].head(5), hide_index=True, use_container_width=True)
            with c2:
                st.info("**Suggested Governance Action:**\nTemporarily increase Kendra working hours in these high-volatility districts to manage inward migration load.")
                st.caption("ℹ️ **Reliability:** Measures temporal variance (Volatility Z-Score) of address updates.")

            st.divider()

            # 4. Unusual Data Patterns
            st.markdown("### 4️⃣ Unusual Data Pattern Detection (Operational Radar)")
            c1, c2 = st.columns([3, 1])
            with c1:
                 # Reuse Anomaly Detector
                anomaly_metric = st.selectbox("Select Operational Metric", df.select_dtypes(include=['number']).columns.tolist(), key='gov_anom')
                detector = AnomalyDetector(contamination=0.02)
                anomalies = detector.detect_spikes(df, anomaly_metric, ['date'])
                
                fig_anom = px.scatter(anomalies, x='date', y=anomaly_metric, color=anomalies['anomaly'].astype(str),
                                    color_discrete_map={'1': 'blue', '-1': 'red'}, title="Operational Anomalies")
                st.plotly_chart(fig_anom, use_container_width=True)
            with c2:
                st.error("**Suggested Governance Action:**\nTrigger automated audit logs for dates marked in RED. Check for bulk-upload errors or operator fraud.")
                st.caption("ℹ️ **Reliability:** Isolation Forest (Unsupervised ML) flags top 2% statistical outliers.")

            st.divider()

            # 5. Kendra Performance
            st.markdown("### 5️⃣ Aadhaar Kendra Performance Signal")
            c1, c2 = st.columns([3, 1])
            with c1:
                kendra_df = PolicyAnalyzer.assess_kendra_performance(data['enrolment'], data['demographic'])
                st.dataframe(kendra_df[['state', 'district', 'performance_score', 'kendra_status']].head(5), hide_index=True, use_container_width=True)
            with c2:
                st.success("**Suggested Governance Action:**\nExpansion Needed: Allocate new kits to 'High Load' districts. Optimization: Reduce shifts in 'Under-Utilized' zones.")
                st.caption("ℹ️ **Reliability:** Composite Index of Total Activity (Enrolment + Update) normalized 0-100.")

if __name__ == "__main__":
    main()
