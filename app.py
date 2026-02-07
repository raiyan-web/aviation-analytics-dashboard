"""
Aviation Operations & Flight Delay Analytics Dashboard
Streamlit Application with Professional UI Design
COMPLETE VERSION - Fixed & Working
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from src.data_processor import load_and_process_data
from src.analytics import FlightAnalytics

# Page configuration
st.set_page_config(
    page_title="Aviation Analytics Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    :root {
        --primary-blue: #4318FF;
        --light-blue: #868CFF;
        --success-green: #05CD99;
        --warning-orange: #FFB547;
        --danger-red: #EE5D50;
        --dark-bg: #0B1437;
        --card-bg: #111C44;
        --text-primary: #FFFFFF;
        --text-secondary: #A3AED0;
        --border-color: #1B254B;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .main {
        background: linear-gradient(135deg, #0B1437 0%, #1a2744 100%);
        padding: 1rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111C44 0%, #0B1437 100%);
        border-right: 1px solid var(--border-color);
    }

    .stats-card {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--light-blue) 100%);
        border-radius: 15px;
        padding: 1.2rem;
        color: white;
        text-align: center;
        height: 100%;
    }
    .stats-card.green {background: linear-gradient(135deg, #05CD99 0%, #04b886 100%);}
    .stats-card.orange {background: linear-gradient(135deg, #FFB547 0%, #ffa733 100%);}
    .stats-card.red {background: linear-gradient(135deg, #EE5D50 0%, #e04d41 100%);}

    .stat-value {font-size: 2.3rem; font-weight: 700;}
    .stat-label {font-size: 0.9rem; opacity: 0.95;}

    .dashboard-header {
        background: linear-gradient(135deg, var(--card-bg) 0%, #1a2850 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
    }

    .section-header {
        color: white;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #4318FF;
        display: inline-block;
    }

    .chart-container {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .insight-box {
        background: linear-gradient(135deg, #1a2850 0%, var(--card-bg) 100%);
        border-left: 4px solid #4318FF;
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: white;
    }
    .insight-box.success {border-left-color: #05CD99;}
    .insight-box.warning {border-left-color: #FFB547;}
    .insight-box.danger {border-left-color: #EE5D50;}
</style>
""", unsafe_allow_html=True)

# Load and cache data
@st.cache_data
def get_data():
    df, processor = load_and_process_data('data/indian_flights_data.csv')
    return df, processor

def main():
    try:
        df, processor = get_data()
        analytics = FlightAnalytics(df)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Make sure data/indian_flights_data.csv exists and src files are present.")
        return

    # Header
    st.markdown("""
    <div class="dashboard-header">
        <h1>✈️ Aviation Operations & Flight Delay Analytics</h1>
        <p style="color:#A3AED0;">Real-time insights into Indian aviation operations and delay patterns</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar filters
    with st.sidebar:
        st.markdown("### 🎯 Dashboard Filters")

        min_date = df['date'].min().date()
        max_date = df['date'].max().date()

        date_range = st.date_input("Date Range", value=(min_date, max_date))

        airlines = ['All'] + sorted(df['airline'].unique().tolist())
        selected_airline = st.selectbox("Airline", airlines)

        origins = ['All'] + sorted(df['origin_city'].unique().tolist())
        selected_origin = st.selectbox("Origin City", origins)

        destinations = ['All'] + sorted(df['destination_city'].unique().tolist())
        selected_destination = st.selectbox("Destination City", destinations)

        weather_conditions = ['All'] + sorted(df['weather'].unique().tolist())
        selected_weather = st.selectbox("Weather", weather_conditions)

    # Filter data
    filtered_df = df.copy()

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= start_date) &
            (filtered_df['date'].dt.date <= end_date)
        ]

    if selected_airline != 'All':
        filtered_df = filtered_df[filtered_df['airline'] == selected_airline]
    if selected_origin != 'All':
        filtered_df = filtered_df[filtered_df['origin_city'] == selected_origin]
    if selected_destination != 'All':
        filtered_df = filtered_df[filtered_df['destination_city'] == selected_destination]
    if selected_weather != 'All':
        filtered_df = filtered_df[filtered_df['weather'] == selected_weather]

    analytics = FlightAnalytics(filtered_df)

    # KPIs
    st.markdown("### 📊 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    total_flights = len(filtered_df)
    cancelled_flights = int(filtered_df['cancelled'].sum()) if total_flights > 0 else 0
    avg_delay = filtered_df[~filtered_df['cancelled']]['delay_minutes'].mean() if total_flights > 0 else 0
    on_time_rate = (filtered_df[~filtered_df['cancelled']]['delay_minutes'] <= 15).mean() * 100 if total_flights > 0 else 0

    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">Total Flights</div>
            <div class="stat-value">{total_flights}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stats-card green">
            <div class="stat-label">On-Time Rate</div>
            <div class="stat-value">{on_time_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stats-card orange">
            <div class="stat-label">Avg Delay (min)</div>
            <div class="stat-value">{avg_delay:.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        cancel_rate = (cancelled_flights / total_flights * 100) if total_flights > 0 else 0
        st.markdown(f"""
        <div class="stats-card red">
            <div class="stat-label">Cancellations</div>
            <div class="stat-value">{cancel_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # Charts area
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<h3 class="section-header">📈 Delay by Airline</h3>', unsafe_allow_html=True)
        airline_perf = analytics.get_airline_performance()

        if len(airline_perf) > 0:
            fig = go.Figure(go.Bar(
                x=airline_perf['airline'],
                y=airline_perf['avg_delay'],
                text=airline_perf['avg_delay'].round(1),
                textposition='outside'
            ))
            fig.update_layout(height=400, title="Average Delay by Airline")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data for selected filters.")

    with col_right:
        st.markdown('<h3 class="section-header">🎯 Delay Categories</h3>', unsafe_allow_html=True)
        delay_dist = filtered_df['delay_category'].value_counts()

        if len(delay_dist) > 0:
            fig = go.Figure(go.Pie(labels=delay_dist.index, values=delay_dist.values, hole=0.5))
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

    # Data Table
    st.markdown('<h3 class="section-header">📋 Flight Data Sample</h3>', unsafe_allow_html=True)
    display_cols = ['date', 'airline', 'origin_city', 'destination_city', 'delay_minutes', 'delay_category', 'weather', 'cancelled']
    available_cols = [c for c in display_cols if c in filtered_df.columns]
    st.dataframe(filtered_df[available_cols].head(20), use_container_width=True)

    # Insights
    st.markdown('<h3 class="section-header">💡 Key Insights</h3>', unsafe_allow_html=True)

    avg_delay_val = avg_delay if not pd.isna(avg_delay) else 0
    if avg_delay_val > 30:
        box_class = "danger"
        msg = f"⚠️ High average delay of {avg_delay_val:.0f} minutes. Review operations."
    elif avg_delay_val > 15:
        box_class = "warning"
        msg = f"📊 Moderate delay of {avg_delay_val:.0f} minutes. Monitor closely."
    else:
        box_class = "success"
        msg = f"✅ Good performance with {avg_delay_val:.0f} minutes average delay."

    st.markdown(f"""
    <div class="insight-box {box_class}">
        <strong>Delay Performance</strong><br>{msg}
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center;color:#A3AED0;padding:1rem;">
        <p>📊 Aviation Operations & Flight Delay Analytics Dashboard</p>
        <p>Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

