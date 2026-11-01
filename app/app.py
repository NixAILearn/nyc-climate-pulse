# NYC Climate Pulse dashboard (Sprint 6)
# Run it on your Mac with:  streamlit run app/app.py
 
from pathlib import Path
 
import numpy as np
import pandas as pd
import streamlit as st
 
# ---------- Page setup ----------
st.set_page_config(page_title="NYC Climate Pulse", page_icon="🌡️", layout="wide")
 
# The CSVs live in data/, one folder up from this file (app/).
# Building the path from this file's location works on your Mac AND on Streamlit Cloud.
DATA_DIR = Path(__file__).parent.parent / "data"
# Sprint 8: use the file the daily robot keeps fresh. If it isn't there yet, use the 1981–2025 snapshot.
DATA_FILE = DATA_DIR / "nyc_daily_latest.csv"
if not DATA_FILE.exists():
    DATA_FILE = DATA_DIR / "nyc_daily_1981_2025.csv"
 
 
def c_to_f(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32
 
 
@st.cache_data(ttl="1h")  # re-read the file at most once an hour, so new days show up
def load_data():
    """Read the CSV once, add Fahrenheit columns, and remember the result."""
    df = pd.read_csv(DATA_FILE, index_col=0, parse_dates=True)
    df["high_f"] = c_to_f(df["T2M_MAX"])
    df["low_f"] = c_to_f(df["T2M_MIN"])
    df["mean_f"] = c_to_f(df["T2M"])
    df["year"] = df.index.year
    return df
 
 
df = load_data()
 
# A "hot day" is a high at or above the 95th percentile of all highs (about 81°F).
HOT_THRESHOLD = df["high_f"].quantile(0.95)
 
# ---------- Sidebar: let the visitor pick a range of years ----------
st.sidebar.header("Filters")
first_year, last_year = int(df["year"].min()), int(df["year"].max())
start, end = st.sidebar.slider(
    "Years to show", first_year, last_year, (first_year, last_year)
)
view = df[(df["year"] >= start) & (df["year"] <= end)]
 
st.sidebar.caption(
    "Data: NASA POWER daily point data for the NYC area. "
    "The grid is about 50 km wide, so this describes the NYC region, not single boroughs."
)
 
# ---------- Title ----------
st.title("🌡️ NYC Climate Pulse!")
st.write(f"Daily weather for the New York City region, {start}–{end}.")
st.caption(f"Data runs through {df.index.max():%B %d, %Y}. It refreshes from NASA every day.")
 
# ---------- Yearly summary table (one row per year) ----------
yearly = view.groupby("year").agg(
    mean_f=("mean_f", "mean"),
    hot_days=("high_f", lambda highs: (highs >= HOT_THRESHOLD).sum()),
    rain_mm=("PRECTOTCORR", "sum"),
)
 
# Warming trend: fit a straight line through the yearly averages.
if len(yearly) >= 2:
    slope_per_year = np.polyfit(yearly.index, yearly["mean_f"], 1)[0]
    trend_text = f"{slope_per_year * 10:+.2f} °F"
else:
    trend_text = "n/a"
 
hottest_date = view["high_f"].idxmax()
 
# ---------- Headline numbers ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Warming trend (per decade)", trend_text)
col2.metric("Hottest day", f"{view['high_f'].max():.1f} °F", hottest_date.strftime("%b %d, %Y"), delta_color="off")
col3.metric(f"Hot days per year (≥{HOT_THRESHOLD:.0f}°F)", f"{yearly['hot_days'].mean():.1f}")
col4.metric("Wettest year", f"{yearly['rain_mm'].idxmax()}", f"driest: {yearly['rain_mm'].idxmin()}", delta_color="off")
 
# ---------- Charts, one per tab ----------
tab_temp, tab_hot, tab_rain, tab_day, tab_findings = st.tabs(
    ["Temperature", "Hot days", "Rain", "Look up a day", "Findings"]
)
 
with tab_temp:
    st.subheader("Average temperature each year (°F)")
    st.line_chart(yearly["mean_f"])
 
with tab_hot:
    st.subheader(f"Days per year with a high of {HOT_THRESHOLD:.0f}°F or more")
    st.bar_chart(yearly["hot_days"])
 
with tab_rain:
    st.subheader("Total rain each year (mm)")
    st.bar_chart(yearly["rain_mm"])
 
with tab_day:
    st.subheader("What was the weather on a given day?")
    day = st.date_input(
        "Pick a date",
        value=view.index.max().date(),
        min_value=view.index.min().date(),
        max_value=view.index.max().date(),
    )
    row = df.loc[pd.Timestamp(day)]
    a, b, c, d = st.columns(4)
    a.metric("High", f"{row['high_f']:.1f} °F")
    b.metric("Low", f"{row['low_f']:.1f} °F")
    c.metric("Rain", f"{row['PRECTOTCORR']:.1f} mm")
    d.metric("Humidity", f"{row['RH2M']:.0f} %")
 
with tab_findings:
    st.subheader("What the earlier notebooks found (full 1981–2025 data)")
    st.markdown(
        """
- **Warming:** about **+0.64 °F per decade**.
- **Hot days** (≥81°F) went from **12.3 a year** (early years) to **24.1 a year** (recent years). 2010 had **43**.
- **Heat waves** (3+ hot days in a row): **103** in total. They doubled, from **1.5 a year** (1981–2000) to **3.0 a year** (2006–2025). The longest were in 2010 and 1995.
- **Drought:** the most severe was the 90 days ending **Nov 18, 2024**, at only **16% of normal rain**. Fall 2024 also had the longest dry spell. Drought days show no clear trend.
- **Unusual days:** an IsolationForest model flagged mostly **2018 and 2019**, which were very wet (about 214% of normal rain).
"""
    )
    st.subheader("Forecasting tomorrow's high: average error (lower is better)")
    forecast = pd.DataFrame(
        {
            "Model": ["Climatology (usual for that date)", "Persistence (same as today)", "Linear regression", "Random forest"],
            "Average error (°F)": [4.37, 3.81, 3.32, 3.20],
        }
    )
    st.dataframe(forecast, hide_index=True)