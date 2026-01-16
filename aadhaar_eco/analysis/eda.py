import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

class EDAService:
    """
    Automated Exploratory Data Analysis service.
    Generates summary stats and Plotly figures for the dashboard.
    """

    @staticmethod
    def get_basic_stats(df: pd.DataFrame) -> Dict[str, Any]:
        """Returns row count, column list, and potential missing value flags."""
        return {
            "rows": len(df),
            "columns": df.columns.tolist(),
            "missing_values": df.isnull().sum().to_dict(),
            "date_range": (df['date'].min(), df['date'].max()) if 'date' in df.columns else None
        }

    @staticmethod
    def generate_trend_insight(df: pd.DataFrame, date_col='date', value_col=None) -> str:
        """Generates a text insight about the trend."""
        if date_col not in df.columns or value_col not in df.columns:
            return ""
        
        daily = df.groupby(date_col)[value_col].sum()
        if daily.empty:
            return "Insufficient data to determine trend."
            
        start_val = daily.iloc[0]
        end_val = daily.iloc[-1]
        
        # Avoid division by zero
        change_pct = ((end_val - start_val) / start_val * 100) if start_val != 0 else 0
        direction = "increased" if change_pct > 0 else "decreased"
        
        peak_date = daily.idxmax()
        peak_val = daily.max()
        
        return (f"📉 **Insight:** Activity has **{direction} by {abs(change_pct):.1f}%** over the period. "
                f"Peak activity was observed on **{peak_date.strftime('%Y-%m-%d')}** with {peak_val:,} records.")

    @staticmethod
    def generate_distribution_insight(df: pd.DataFrame, group_col='state', value_col=None) -> str:
        """Generates a text insight about the distribution."""
        if group_col not in df.columns or value_col not in df.columns:
            return ""
            
        grouped = df.groupby(group_col)[value_col].sum().sort_values(ascending=False)
        if grouped.empty:
            return ""
            
        top_name = grouped.index[0]
        top_val = grouped.iloc[0]
        total = grouped.sum()
        share = (top_val / total * 100) if total > 0 else 0
        
        return (f"📊 **Insight:** **{top_name}** is the dominant logical unit, contributing **{share:.1f}%** "
                f"of the total {value_col}. This suggests a need for focused resource allocation in this region.")

    @staticmethod
    def plot_trend(df: pd.DataFrame, date_col='date', value_col=None, title="Trend Over Time"):
        """Generates a line chart for a numeric column over time."""
        if date_col not in df.columns or value_col not in df.columns:
            return None
        
        # Resample by Day or Week for cleaner lines
        daily = df.groupby(date_col)[value_col].sum().reset_index()
        fig = px.line(daily, x=date_col, y=value_col, title=title, markers=True)
        return fig

    @staticmethod
    def plot_state_distribution(df: pd.DataFrame, state_col='state', value_col=None):
        """Generates a bar chart of values per state."""
        if state_col not in df.columns or value_col not in df.columns:
            return None
            
        state_agg = df.groupby(state_col)[value_col].sum().reset_index().sort_values(by=value_col, ascending=False)
        fig = px.bar(state_agg, x=state_col, y=value_col, title=f"Distribution by State ({value_col})")
        return fig
    
    @staticmethod
    def plot_correlation(df: pd.DataFrame):
        """Generates a heatmap of numeric correlations."""
        corr = df.select_dtypes(include=['number']).corr()
        fig = px.imshow(corr, text_auto=True, title="Feature Correlation Matrix")
        return fig
