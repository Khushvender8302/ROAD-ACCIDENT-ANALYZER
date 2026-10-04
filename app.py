import streamlit as st

import pandas as pd
import plotly.express as px
import numpy as np

# Page configuration
st.set_page_config(page_title="Road Accident Dashboard", page_icon="🚗", layout="wide")

# 1. Sample Realistic Data Generate / Load
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 2000
    dates = pd.date_range(start="2021-01-01", end="2023-12-31", periods=n)
    severities = np.random.choice(["Fatal", "Serious", "Slight"], size=n, p=[0.05, 0.20, 0.75])
    road_types = np.random.choice(["Single Carriageway", "Dual Carriageway", "Roundabout", "One-Way"], size=n, p=[0.70, 0.18, 0.08, 0.04])
    weathers = np.random.choice(["Fine / Clear", "Raining / Wet", "Snow / Frost", "Fog / Mist"], size=n, p=[0.72, 0.18, 0.05, 0.05])
    areas = np.random.choice(["Urban", "Rural"], size=n, p=[0.64, 0.36])
    vehicles = np.random.choice(["Car", "Motorcycle", "Bus", "Van", "Truck (HGV)"], size=n, p=[0.65, 0.15, 0.08, 0.08, 0.04])
    
    df = pd.DataFrame({
        "Accident_Date": dates,
        "Year": dates.year,
        "Month": dates.strftime('%b'),
        "Day_of_Week": dates.day_name(),
        "Accident_Severity": severities,
        "Casualties": np.random.choice([1, 2, 3, 4], size=n, p=[0.75, 0.15, 0.07, 0.03]),
        "Vehicles_Involved": np.random.choice([1, 2, 3], size=n, p=[0.4, 0.5, 0.1]),
        "Road_Type": road_types,
        "Weather_Conditions": weathers,
        "Urban_or_Rural_Area": areas,
        "Vehicle_Type": vehicles
    })
    return df

df = load_data()

# 2. SLICERS / FILTERS (Sidebar)
st.sidebar.title("🔍 Dashboard Slicers")

year_filter = st.sidebar.multiselect("Select Year:", options=df["Year"].unique(), default=df["Year"].unique())
area_filter = st.sidebar.multiselect("Select Area Type:", options=df["Urban_or_Rural_Area"].unique(), default=df["Urban_or_Rural_Area"].unique())
weather_filter = st.sidebar.multiselect("Select Weather:", options=df["Weather_Conditions"].unique(), default=df["Weather_Conditions"].unique())

# Filter data dynamically
filtered_df = df[
    (df["Year"].isin(year_filter)) &
    (df["Urban_or_Rural_Area"].isin(area_filter)) &
    (df["Weather_Conditions"].isin(weather_filter))
]

# 3. DASHBOARD TITLE & KPI CARDS
st.title("🚗 Road Accident Data Analysis Dashboard")
st.markdown("Interactive Data Analytics Portfolio Project with Real-time Slicers")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Accidents", f"{len(filtered_df):,}")
col2.metric("Total Casualties", f"{filtered_df['Casualties'].sum():,}")
col3.metric("Fatal Casualties", f"{len(filtered_df[filtered_df['Accident_Severity'] == 'Fatal']):,}")
col4.metric("Serious Casualties", f"{len(filtered_df[filtered_df['Accident_Severity'] == 'Serious']):,}")

st.divider()

# 4. INTERACTIVE CHARTS
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Monthly Casualties Trend")
    trend_data = filtered_df.groupby("Month")["Casualties"].sum().reset_index()
    fig_trend = px.line(trend_data, x="Month", y="Casualties", markers=True, title="Monthly Casualties Count")
    st.plotly_chart(fig_trend, use_container_width=True)

with c2:
    st.subheader("🍩 Casualties by Severity")
    fig_pie = px.pie(filtered_df, names="Accident_Severity", values="Casualties", hole=0.4, color="Accident_Severity", color_discrete_map={"Fatal":"red", "Serious":"orange", "Slight":"green"})
    st.plotly_chart(fig_pie, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.subheader("🛣️ Accidents by Road Type")
    fig_bar = px.bar(filtered_df["Road_Type"].value_counts().reset_index(), x="Road_Type", y="count", labels={"count": "Accident Count"}, color="Road_Type")
    st.plotly_chart(fig_bar, use_container_width=True)

with c4:
    st.subheader("📅 Casualties by Day of Week")
    fig_day = px.bar(filtered_df["Day_of_Week"].value_counts().reset_index(), x="Day_of_Week", y="count",labels={"count": "Accidents"}, color_discrete_sequence=["#38bdf8"])
    st.plotly_chart(fig_day, use_container_width=True)

# 5. DATA TABLE VIEW
st.subheader("📋 Filtered Dataset Records")
st.dataframe(filtered_df.head(50), use_container_width=True)