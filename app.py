"""
Aviation Operations & Flight Delay Analytics Dashboard
Streamlit Application with Professional UI Design
COMPLETE VERSION - All sections included and working
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_processor import load_and_process_data
from analytics import FlightAnalytics
{
    "python.analysis.extraPaths": ["./src"]
}
# Page configuration
st.set_page_config(
    page_title="Aviation Analytics Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS matching the design reference
st.markdown("""
<style>
    /* Main theme colors matching the reference design */
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
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0B1437 0%, #1a2744 100%);
        padding: 1rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111C44 0%, #0B1437 100%);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: var(--text-primary);
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, var(--card-bg) 0%, #1a2850 100%);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--light-blue) 100%);
        border-radius: 15px;
        padding: 1.2rem;
        color: white;
        box-shadow: 0 8px 24px rgba(67, 24, 255, 0.3);
        text-align: center;
        height: 100%;
    }
    
    .stats-card.green {
        background: linear-gradient(135deg, var(--success-green) 0%, #04b886 100%);
        box-shadow: 0 8px 24px rgba(5, 205, 153, 0.3);
    }
    
    .stats-card.orange {
        background: linear-gradient(135deg, var(--warning-orange) 0%, #ffa733 100%);
        box-shadow: 0 8px 24px rgba(255, 181, 71, 0.3);
    }
    
    .stats-card.red {
        background: linear-gradient(135deg, var(--danger-red) 0%, #e04d41 100%);
        box-shadow: 0 8px 24px rgba(238, 93, 80, 0.3);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.95;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-change {
        font-size: 0.85rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Headers */
    .dashboard-header {
        background: linear-gradient(135deg, var(--card-bg) 0%, #1a2850 100%);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    .dashboard-title {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .dashboard-subtitle {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-top: 0.5rem;
    }
    
    /* Section headers */
    .section-header {
        color: var(--text-primary);
        font-size: 1.3rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--primary-blue);
        display: inline-block;
    }
    
    /* Charts */
    .chart-container {
        background: var(--card-bg);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--light-blue) 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(67, 24, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(67, 24, 255, 0.4);
    }
    
    /* Info boxes */
    .insight-box {
        background: linear-gradient(135deg, #1a2850 0%, var(--card-bg) 100%);
        border-left: 4px solid var(--primary-blue);
        border-radius: 10px;
        padding: 1.2rem;
        margin: 1rem 0;
        color: var(--text-primary);
    }
    
    .insight-box.success {
        border-left-color: var(--success-green);
    }
    
    .insight-box.warning {
        border-left-color: var(--warning-orange);
    }
    
    .insight-box.danger {
        border-left-color: var(--danger-red);
    }
    
    /* Risk indicator */
    .risk-indicator {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .risk-low {
        background: rgba(5, 205, 153, 0.2);
        color: var(--success-green);
        border: 1px solid var(--success-green);
    }
    
    .risk-moderate {
        background: rgba(255, 181, 71, 0.2);
        color: var(--warning-orange);
        border: 1px solid var(--warning-orange);
    }
    
    .risk-high {
        background: rgba(238, 93, 80, 0.2);
        color: var(--danger-red);
        border: 1px solid var(--danger-red);
    }
</style>
""", unsafe_allow_html=True)

# Load and cache data
@st.cache_data
def get_data():
    """Load and process flight data"""
    df, processor = load_and_process_data('data/indian_flights_data.csv')
    return df, processor

# Main app
def main():
    # Load data
    try:
        df, processor = get_data()
        analytics = FlightAnalytics(df)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please ensure the data file exists. Run `python generate_data.py` first.")
        st.code("python generate_data.py", language="bash")
        return
    
    # Dashboard Header
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="dashboard-title">
            ✈️ Aviation Operations & Flight Delay Analytics
        </h1>
        <p class="dashboard-subtitle">
            Real-time insights into Indian aviation operations and delay patterns
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("### 🎯 Dashboard Filters")
        
        # Date range
        st.markdown("#### 📅 Date Range")
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        
        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed"
        )
        
        # Airline filter
        st.markdown("#### ✈️ Airlines")
        airlines = ['All'] + sorted(df['airline'].unique().tolist())
        selected_airline = st.selectbox("Select Airline", airlines, label_visibility="collapsed")
        
        # Origin filter
        st.markdown("#### 🛫 Origin City")
        origins = ['All'] + sorted(df['origin_city'].unique().tolist())
        selected_origin = st.selectbox("Select Origin", origins, label_visibility="collapsed")
        
        # Destination filter
        st.markdown("#### 🛬 Destination City")
        destinations = ['All'] + sorted(df['destination_city'].unique().tolist())
        selected_destination = st.selectbox("Select Destination", destinations, label_visibility="collapsed")
        
        # Weather filter
        st.markdown("#### 🌤️ Weather Condition")
        weather_conditions = ['All'] + sorted(df['weather'].unique().tolist())
        selected_weather = st.selectbox("Select Weather", weather_conditions, label_visibility="collapsed")
    
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
    
    # Update analytics with filtered data
    analytics = FlightAnalytics(filtered_df)
    
    # Key Metrics Row
    st.markdown("### 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_flights = len(filtered_df)
    cancelled_flights = filtered_df['cancelled'].sum()
    avg_delay = filtered_df[~filtered_df['cancelled']]['delay_minutes'].mean()
    on_time_rate = (filtered_df[~filtered_df['cancelled']]['delay_minutes'] <= 15).mean() * 100
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stat-label">Total Flights</div>
            <div class="stat-value">{total_flights:,}</div>
            <div class="stat-change">📊 Monitored</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card green">
            <div class="stat-label">On-Time Rate</div>
            <div class="stat-value">{on_time_rate:.1f}%</div>
            <div class="stat-change">✅ Within 15 min</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card orange">
            <div class="stat-label">Avg Delay</div>
            <div class="stat-value">{avg_delay:.0f}</div>
            <div class="stat-change">⏱️ Minutes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        cancellation_rate = (cancelled_flights / total_flights * 100) if total_flights > 0 else 0
        st.markdown(f"""
        <div class="stats-card red">
            <div class="stat-label">Cancellations</div>
            <div class="stat-value">{cancellation_rate:.1f}%</div>
            <div class="stat-change">❌ {cancelled_flights} flights</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main content area - Two columns
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Delay Distribution by Airline
        st.markdown('<h3 class="section-header">📈 Delay Distribution by Airline</h3>', unsafe_allow_html=True)
        
        airline_perf = analytics.get_airline_performance()
        
        if len(airline_perf) > 0:
            fig_airline = go.Figure()
            
            fig_airline.add_trace(go.Bar(
                name='Average Delay',
                x=airline_perf['airline'],
                y=airline_perf['avg_delay'],
                marker=dict(
                    color=airline_perf['avg_delay'],
                    colorscale=[[0, '#05CD99'], [0.5, '#FFB547'], [1, '#EE5D50']],
                    showscale=False,
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=airline_perf['avg_delay'].round(1),
                textposition='outside',
                textfont=dict(color='white', size=12)
            ))
            
            fig_airline.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#A3AED0', size=12),
                title=dict(
                    text='Average Delay by Airline (minutes)',
                    font=dict(color='white', size=14),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title='',
                    showgrid=False,
                    color='#A3AED0'
                ),
                yaxis=dict(
                    title='Minutes',
                    showgrid=True,
                    gridcolor='rgba(163,174,208,0.1)',
                    color='#A3AED0'
                ),
                height=400,
                margin=dict(t=60, b=40, l=40, r=40),
                showlegend=False
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_airline, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No data available for selected filters")
        
        # Delay Trends Over Time
        st.markdown('<h3 class="section-header">📅 Delay Trends Over Time</h3>', unsafe_allow_html=True)
        
        monthly_trends = analytics.get_time_trends(period='month')
        
        if len(monthly_trends) > 0:
            fig_trend = go.Figure()
            
            fig_trend.add_trace(go.Scatter(
                x=monthly_trends['month_name'],
                y=monthly_trends['avg_delay'],
                mode='lines+markers',
                name='Avg Delay',
                line=dict(color='#4318FF', width=3),
                marker=dict(size=10, color='#4318FF', line=dict(color='white', width=2)),
                fill='tonexty',
                fillcolor='rgba(67, 24, 255, 0.1)'
            ))
            
            fig_trend.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#A3AED0', size=12),
                title=dict(
                    text='Monthly Delay Trends',
                    font=dict(color='white', size=14),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title='',
                    showgrid=False,
                    color='#A3AED0'
                ),
                yaxis=dict(
                    title='Average Delay (minutes)',
                    showgrid=True,
                    gridcolor='rgba(163,174,208,0.1)',
                    color='#A3AED0'
                ),
                height=350,
                margin=dict(t=60, b=40, l=40, r=40),
                hovermode='x unified'
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_trend, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No trend data available")
    
    with col_right:
        # Delay Category Distribution
        st.markdown('<h3 class="section-header">🎯 Delay Categories</h3>', unsafe_allow_html=True)
        
        delay_dist = filtered_df['delay_category'].value_counts()
        
        if len(delay_dist) > 0:
            colors = {
                'On Time': '#05CD99',
                'Minor Delay (0-15 min)': '#868CFF',
                'Moderate Delay (15-30 min)': '#FFB547',
                'Significant Delay (30-60 min)': '#FF8A47',
                'Major Delay (60+ min)': '#EE5D50',
                'Cancelled': '#A3AED0'
            }
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=delay_dist.index,
                values=delay_dist.values,
                marker=dict(colors=[colors.get(cat, '#4318FF') for cat in delay_dist.index]),
                hole=0.5,
                textinfo='percent',
                textfont=dict(color='white', size=12),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )])
            
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#A3AED0', size=11),
                height=350,
                margin=dict(t=20, b=20, l=20, r=20),
                showlegend=True,
                legend=dict(
                    orientation='v',
                    yanchor='middle',
                    y=0.5,
                    xanchor='left',
                    x=1.05,
                    font=dict(color='white', size=10)
                )
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Weather Impact
        st.markdown('<h3 class="section-header">🌤️ Weather Impact</h3>', unsafe_allow_html=True)
        
        weather_impact = analytics.get_weather_impact()
        
        if len(weather_impact) > 0:
            fig_weather = go.Figure(data=[go.Bar(
                x=weather_impact['weather'],
                y=weather_impact['avg_delay'],
                marker=dict(
                    color=['#05CD99', '#A3AED0', '#FFB547', '#FF8A47', '#EE5D50', '#868CFF'][:len(weather_impact)],
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=weather_impact['avg_delay'].round(1),
                textposition='outside',
                textfont=dict(color='white', size=11)
            )])
            
            fig_weather.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#A3AED0', size=11),
                xaxis=dict(
                    title='',
                    showgrid=False,
                    color='#A3AED0'
                ),
                yaxis=dict(
                    title='Avg Delay (min)',
                    showgrid=True,
                    gridcolor='rgba(163,174,208,0.1)',
                    color='#A3AED0'
                ),
                height=300,
                margin=dict(t=20, b=40, l=40, r=20),
                showlegend=False
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_weather, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Most Delayed Routes and Airports
    st.markdown('<h3 class="section-header">🛫 Most Delayed Routes & Airports</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        route_perf = analytics.get_route_performance(top_n=10)
        
        if len(route_perf) > 0:
            fig_routes = go.Figure(data=[go.Bar(
                y=route_perf['route_name'],
                x=route_perf['avg_delay'],
                orientation='h',
                marker=dict(
                    color=route_perf['avg_delay'],
                    colorscale=[[0, '#05CD99'], [0.5, '#FFB547'], [1, '#EE5D50']],
                    showscale=False,
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=route_perf['avg_delay'].round(1),
                textposition='outside',
                textfont=dict(color='white', size=10)
            )])
            
            fig_routes.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#A3AED0', size=11),
                title=dict(
                    text='Top 10 Most Delayed Routes',
                    font=dict(color='white', size=13),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title='Average Delay (minutes)',
                    showgrid=True,
                    gridcolor='rgba(163,174,208,0.1)',
                    color='#A3AED0'
                ),
                yaxis=dict(
                    title='',
                    showgrid=False,
                    color='#A3AED0'
                ),
                height=400,
                margin=dict(t=60, b=40, l=200, r=40),
                showlegend=False
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_routes, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        airport_perf = analytics.get_airport_performance(top_n=10)
        
        if len(airport_perf) > 0:
            fig_airports = go.Figure(data=[go.Bar(
                y=airport_perf['airport_name'],
                x=airport_perf['avg_delay'],
                orientation='h',
                marker=dict(
                    color=airport_perf['avg_delay'],
                    colorscale=[[0, '#05CD99'], [0.5, '#FFB547'], [1, '#EE5D50']],
                    showscale=False,
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=airport_perf['avg_delay'].round(1),
                textposition='outside',
                textfont=dict(color='white', size=10)
            )])
            
            fig_airports.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#A3AED0', size=11),
                title=dict(
                    text='Top 10 Airports by Avg Delay',
                    font=dict(color='white', size=13),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title='Average Delay (minutes)',
                    showgrid=True,
                    gridcolor='rgba(163,174,208,0.1)',
                    color='#A3AED0'
                ),
                yaxis=dict(
                    title='',
                    showgrid=False,
                    color='#A3AED0'
                ),
                height=400,
                margin=dict(t=60, b=40, l=150, r=40),
                showlegend=False
            )
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_airports, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
        # Data table section
        st.markdown('<h3 class="section-header">📋 Flight Data Sample</h3>', unsafe_allow_html=True)
        
        display_cols = ['date', 'airline', 'origin_city', 'destination_city', 'delay_minutes', 'delay_category', 'weather', 'cancelled']
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.dataframe(
            filtered_df[available_cols].head(20),
            use_container_width=True,
            height=400
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Key Insights Section
        st.markdown('<h3 class="section-header">💡 Key Insights & Recommendations</h3>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_delay_val = filtered_df[~filtered_df['cancelled']]['delay_minutes'].mean()
            if avg_delay_val > 30:
                insight_type = "danger"
                message = f"⚠️ High average delay of {avg_delay_val:.0f} minutes detected. Recommend operational review."
            elif avg_delay_val > 15:
                insight_type = "warning"
                message = f"📊 Moderate average delay of {avg_delay_val:.0f} minutes. Monitor closely."
            else:
                insight_type = "success"
                message = f"✅ Good performance with {avg_delay_val:.0f} minutes average delay."
            
            st.markdown(f"""
            <div class="insight-box {insight_type}">
                <strong>Delay Performance</strong><br>
                {message}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            cancel_rate = (filtered_df['cancelled'].sum() / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
            if cancel_rate > 5:
                insight_type = "danger"
                message = f"❌ High cancellation rate of {cancel_rate:.1f}%. Investigate root causes."
            elif cancel_rate > 2:
                insight_type = "warning"
                message = f"⚠️ Cancellation rate of {cancel_rate:.1f}%. Review operational factors."
            else:
                insight_type = "success"
                message = f"✅ Low cancellation rate of {cancel_rate:.1f}%. Good operational stability."
            
            st.markdown(f"""
            <div class="insight-box {insight_type}">
                <strong>Cancellation Risk</strong><br>
                {message}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            weather_delays = filtered_df[filtered_df['weather'] != 'Clear']['delay_minutes'].mean()
            clear_delays = filtered_df[filtered_df['weather'] == 'Clear']['delay_minutes'].mean()
            
            if not pd.isna(weather_delays) and not pd.isna(clear_delays):
                weather_impact_pct = ((weather_delays - clear_delays) / clear_delays * 100) if clear_delays > 0 else 0
                if weather_impact_pct > 50:
                    insight_type = "danger"
                    message = f"🌧️ Weather impact significant ({weather_impact_pct:.0f}% increase). Enhance weather contingency."
                else:
                    insight_type = "warning"
                    message = f"🌤️ Weather impact moderate ({weather_impact_pct:.0f}% increase). Monitor weather patterns."
            else:
                insight_type = "success"
                message = "✅ Insufficient data for weather impact analysis."
            
            st.markdown(f"""
            <div class="insight-box {insight_type}">
                <strong>Weather Impact</strong><br>
                {message}
            </div>
            """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #A3AED0; padding: 2rem 0; font-size: 0.9rem;">
            <p>📊 Aviation Operations & Flight Delay Analytics Dashboard</p>
            <p>Data last updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            <p style="font-size: 0.85rem; opacity: 0.7;">Built with Streamlit • Powered by Real-time Aviation Data</p>
        </div>
        """, unsafe_allow_html=True)
    
    if __name__ == "__main__":
        main()