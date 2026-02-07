Aviation Operations & Flight Delay Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)
![Plotly](https://img.shields.io/badge/Plotly-5.18-purple)
![License](https://img.shields.io/badge/License-MIT-green)

**A professional data analytics dashboard for Indian aviation operations with interactive visualizations and predictive insights**
 Overview

This end-to-end data analytics project provides comprehensive insights into Indian aviation operations, focusing on flight delays, cancellations, and operational efficiency. Built with modern data visualization tools and designed with a professional dark-themed UI, this dashboard is perfect for data analyst portfolios.

 Key Highlights

- **Real-time Analytics**: Interactive dashboard with dynamic filtering
- **10,000+ Flight Records**: Realistic Indian aviation data across 2 years
- **7 Major Airlines**: IndiGo, Air India, SpiceJet, Vistara, and more
- **18 Airports**: Coverage of major Indian cities
- **Predictive Insights**: ML-powered delay risk prediction
- **Professional UI**: Dark theme inspired by modern analytics platforms

---

Features

Analytics Capabilities

1. **Key Performance Indicators**
   - Total flights monitored
   - On-time performance rate
   - Average delay metrics
   - Cancellation statistics

2. **Delay Analysis**
   - Distribution by airline
   - Route-specific delays
   - Time-based trends (monthly, daily, hourly)
   - Weather impact analysis

3. **Interactive Visualizations**
   - Bar charts for airline performance
   - Line charts for temporal trends
   - Pie charts for category distribution
   - Horizontal bar charts for route comparisons

4. **Delay Risk Predictor**
   - Historical probability calculation
   - Route and time-based predictions
   - Weather condition adjustments
   - Risk level classification (Low/Moderate/High)

5. **Advanced Filtering**
   - Date range selection
   - Airline filtering
   - Origin/destination cities
   - Weather conditions


 Installation
 Prerequisites

- Python 3.8 or higher
- pip package manager
Project Structure

```
aviation_analytics_dashboard/
│
├── app.py                      # Main Streamlit dashboard application
├── generate_data.py            # Data generation script
├── requirements.txt            # Python dependencies
│
├── src/
│   ├── data_processor.py      # Data preprocessing and feature engineering
│   └── analytics.py           # Analytics and statistical functions
│
├── data/
│   └── indian_flights_data.csv # Generated flight data
│
├── .streamlit/
│   └── config.toml            # Streamlit configuration
│`

---
 💻 Usage

 Running Locally

```bash
# Start the dashboard
streamlit run app.py

# Generate new data (optional)
python generate_data.py

# Test data processing
python src/data_processor.py

# Test analytics
python src/analytics.py
```
 Using the Dashboard

1. **Apply Filters**: Use the sidebar to filter by date, airline, origin, destination, and weather
2. **Explore Metrics**: View KPIs in the top row showing key statistics
3. **Analyze Trends**: Scroll through various charts showing delay patterns
4. **Predict Delays**: Use the Risk Predictor to assess delay probability for specific routes

Customizing the Data

Edit `generate_data.py` to modify:
- Number of records (default: 10,000)
- Date range
- Airlines and routes
- Weather patterns
- Delay probabilities

 📊 Sample Insights

The dashboard reveals:

- **IndiGo** has the best on-time performance among major carriers
- **Fog** causes the most significant delays (especially in Delhi during winter)
- **Evening flights** (17:00-21:00) experience higher delay rates
- **Delhi-Mumbai** route has high traffic and moderate delays
- **Monsoon season** (June-September) shows increased weather-related disruptions



  Design Features

 UI/UX
- **Dark Theme**: Professional gradient backgrounds (#0B1437 to #1a2744)
- **Color Coding**: 
  - Primary Blue (#4318FF) - Main actions
  - Success Green (#05CD99) - Positive metrics
  - Warning Orange (#FFB547) - Moderate alerts
  - Danger Red (#EE5D50) - Critical issues
- **Glassmorphism Cards**: Modern frosted glass effect
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes

 Visualizations
- **Plotly Charts**: Interactive, zoomable, and downloadable
- **Consistent Styling**: Unified color scheme across all charts
- **Clear Legends**: Easy-to-understand labels and titles
- **Hover Details**: Rich tooltips with additional information.


 Data Schema

Flight Data Columns

| Column | Type | Description |
|--------|------|-------------|
| airline | string | Airline name |
| flight_number | string | Flight identifier |
| origin | string | Origin airport code |
| origin_city | string | Origin city name |
| destination | string | Destination airport code |
| destination_city | string | Destination city name |
| date | date | Flight date |
| scheduled_departure | datetime | Scheduled departure time |
| actual_departure | datetime | Actual departure time |
| delay_minutes | float | Delay in minutes |
| cancelled | boolean | Cancellation flag |
| weather | string | Weather condition |

 Generated Features

- `delay_category`: Categorical delay classification
- `hour`, `day`, `month`: Time components
- `day_name`, `month_name`: Text representations
- `time_period`: Morning/Afternoon/Evening/Night
- `is_weekend`: Weekend flag
- `route`: Origin-Destination pair
- `is_delayed`: Binary delay flag (>15 min)


 Technologies Used

- **Python 3.8+**: Core programming language
- **Streamlit**: Web dashboard framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Plotly**: Interactive visualizations
- **Python-dateutil**: Date/time handling


 Use Cases

 For Data Analysts
- Portfolio project demonstrating end-to-end analytics
- Real-world aviation industry insights
- Data visualization best practices
- Interactive dashboard development

 For Airlines
- Performance benchmarking
- Route optimization
- Delay pattern identification
- Operational efficiency monitoring

 For Passengers
- Delay risk assessment
- Route selection
- Travel planning insights
- Historical performance data
