# NYC Climate Pulse: "NYC in 2050" page (Sprint 9)
# Streamlit shows every file in app/pages/ as an extra page in the sidebar.
# The numbers come from notebooks/09_future_2050.ipynb, which saves two small CSV files.

from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="NYC in 2050", page_icon="🔮", layout="wide")

# This file is in app/pages/, so the data folder is three levels up, then into data/.
DATA_DIR = Path(__file__).parent.parent.parent / "data"
YEARLY_FILE = DATA_DIR / "future_2050_yearly.csv"
SUMMARY_FILE = DATA_DIR / "future_2050_summary.csv"

st.title("🔮 NYC in 2050")

# If the notebook hasn't been run yet, explain what to do instead of crashing.
if not YEARLY_FILE.exists() or not SUMMARY_FILE.exists():
    st.warning("Run notebooks/09_future_2050.ipynb first. It creates the data this page needs.")
    st.stop()

yearly = pd.read_csv(YEARLY_FILE, index_col="year")
s = pd.read_csv(SUMMARY_FILE).iloc[0]  # one row of headline numbers

st.write(
    f"Where is the region's climate heading? We compare **{int(s['n_models'])} CMIP6 climate models** "
    "(a high-emissions path) with the real NASA POWER history, and with Sprint 3's straight-line trend."
)

# ---------- Headline numbers ----------
col1, col2, col3 = st.columns(3)
col1.metric(
    "Average temperature, 2040s",
    f"{s['future_mean_median_f']:.1f} °F",
    f"{s['future_mean_median_f'] - s['base_mean_f']:+.1f} °F vs 1981–2010",
    delta_color="inverse",
)
col2.metric(
    f"Hot days a year (≥{s['hot_threshold_f']:.0f}°F), 2040s",
    f"{s['future_hot_days_median']:.0f}",
    f"{s['future_hot_days_median'] - s['base_hot_days']:+.0f} vs 1981–2010",
    delta_color="inverse",
)
col3.metric(
    "If the straight line continued",
    f"{s['straight_line_2040s_f']:.1f} °F",
    "2040s average",
    delta_color="off",
)

st.caption(
    f"Model range for the 2040s: {s['future_mean_low_f']:.1f}–{s['future_mean_high_f']:.1f} °F, "
    f"and {s['future_hot_days_low']:.0f}–{s['future_hot_days_high']:.0f} hot days a year. "
    f"For comparison, 2016–2025 really averaged {s['recent_mean_f']:.1f} °F with {s['recent_hot_days']:.0f} hot days a year."
)

# ---------- Charts ----------
tab_temp, tab_hot, tab_about = st.tabs(["Temperature", "Hot days", "How this works"])

with tab_temp:
    st.subheader("10-year average temperature (°F)")
    st.line_chart(
        yearly[["observed_f", "models_median_f", "models_low_f", "models_high_f", "straight_line_f"]].rename(
            columns={
                "observed_f": "Real (NASA POWER)",
                "models_median_f": "Models: middle",
                "models_low_f": "Models: lowest",
                "models_high_f": "Models: highest",
                "straight_line_f": "Straight line",
            }
        )
    )

with tab_hot:
    st.subheader(f"Hot days a year, 10-year average (high of {s['hot_threshold_f']:.0f}°F or more)")
    st.line_chart(
        yearly[["observed_hot_days", "models_hot_days_median", "models_hot_days_low", "models_hot_days_high"]].rename(
            columns={
                "observed_hot_days": "Real (NASA POWER)",
                "models_hot_days_median": "Models: middle",
                "models_hot_days_low": "Models: lowest",
                "models_hot_days_high": "Models: highest",
            }
        )
    )

with tab_about:
    st.markdown(
        """
- **Climate models** simulate the whole planet. They get the *statistics* of a decade right, not the weather of a specific day, so every line here is a **10-year average**.
- Models run a little too warm or cold for NYC (**bias**). We keep each model's **change** since 1981–2010 and add it to NASA's real 1981–2010 average.
- Hot days use the same fix, month by month, on each model's daily highs.
- These runs follow a **high-emissions** path. By 2050 a middle path (SSP2-4.5) is only about 0.7 °F cooler worldwide (IPCC AR6). The paths split mostly after 2050.
- Like NASA POWER, the models describe the **NYC region** (grid boxes 20–50 km wide). Dense neighborhoods run hotter.

Model data: [Open-Meteo Climate API](https://open-meteo.com/en/docs/climate-api) (CMIP6 HighResMIP). History: [NASA POWER](https://power.larc.nasa.gov/).
"""
    )
