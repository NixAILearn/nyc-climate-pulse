# NYC Climate Pulse: what 45 years of data show

*Daily NASA POWER data for the New York City region, 1981–2025.*
*Each value covers a grid cell about 50 km wide, so these results describe the region, not single neighborhoods.*

## 1. The region is warming

A straight line fitted through each year's average temperature rises by about **0.64 °F per decade**. Over the 45 years of data, that adds up to almost **3 °F**.

The warmest single day was **July 6, 2010**, with a high of **93.65 °F**. (Station thermometers in the city read hotter that day. Gridded data smooths out peaks.)

## 2. Hot days have about doubled

I called a day "hot" when its high was at or above **81 °F**, which is the hottest 5% of all days in the data (the 95th percentile).

- In the early years there were about **12.3** hot days a year.
- Recently there are about **24.1** a year.
- **2010** stands out with **43** hot days.

## 3. Forecasting tomorrow's high

I tried four ways to guess tomorrow's high temperature and measured the average error (MAE: how many degrees off the guess is, on average). Lower is better.

| Method | How it guesses | Average error |
|---|---|---|
| Climatology | The usual high for that date | 4.37 °F |
| Persistence | Same as today | 3.81 °F |
| Linear regression | A weighted formula of recent days | 3.32 °F |
| Random forest | Many decision trees voting | **3.20 °F** |

Both machine learning models beat the simple baselines, and the random forest was best. The gain over "same as today" is about 0.6 °F, which shows how hard weather forecasting is with only a few local measurements.

## 4. Heat waves have doubled

A heat wave here means **three or more hot days in a row**.

- There were **103** heat waves in total.
- From 1981 to 2000 there were **1.5 a year**. From 2006 to 2025 there were **3.0 a year**.
- The longest heat waves were in **2010** and **1995**.

## 5. Droughts: severe ones happen, but no trend

I compared rain over each 90-day window with what is normal for that time of year.

- The most severe drought was the 90 days ending **November 18, 2024**, with only **16% of normal rain**. Fall 2024 also had the longest dry spell.
- The years with the most drought days were **2002, 2001 and 1999**.
- Unlike heat, drought days show **no clear upward or downward trend**.
- The wettest year was **2018** and the driest was **2001**.

## 6. Unusual days

An **IsolationForest** model (it looks for days that don't fit the usual patterns) mostly flagged the very wet stretches of **2018 and 2019**, when rain was about **214% of normal**. Unusual wetness, not only heat, is part of the region's recent weather.

## 7. Looking ahead to 2050

I compared 7 CMIP6 climate models (a high-emissions path) with the NASA history,
using each model's *change* since 1981–2010 so its own bias doesn't matter.

- By the 2040s, the region's average temperature could be about **57.2 °F**,
  **+4.1 °F** warmer than 1981–2010 (models range from +2.8 to +4.5 °F).
- Hot days (a high of 81 °F or more) could rise to about **51 a year**
  (models range from 39 to 66), compared with 16 in 1981–2010 and 24 in 2016–2025.
- Simply extending the 1981–2025 straight line gives 56.4 °F for the 2040s, which is
  lower than the models by 0.8 °F. The models expect warming to speed up compared
  with the past 45 years.
- By 2050 a middle-emissions path is only slightly cooler; the paths split mostly
  after 2050 (IPCC AR6).

## Takeaways

1. NYC's region is warming steadily, about 0.64 °F every ten years.
2. Extreme heat is growing faster than the average: hot days and heat waves have both roughly doubled.
3. Rain swings between extremes (a record drought in 2024, very wet years in 2018 and 2019) but shows no simple trend.
4. A simple ML model forecasts tomorrow's high a little better than common-sense rules.

## Limits

- The data is gridded (about 50 km), so it misses the extra heat in dense neighborhoods.
- "Hot day" and "drought" use thresholds I chose from this data, not official definitions.
- A straight-line trend is a simple summary. It doesn't explain *why* the climate is changing.
