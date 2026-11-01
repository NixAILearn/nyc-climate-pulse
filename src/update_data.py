"""Keep the dashboard's data current (Sprint 8).
 
Run it from the project folder with:  python src/update_data.py
 
It reads data/nyc_daily_latest.csv, asks NASA POWER for the newest days,
adds them to the end, and saves the file again. A GitHub Action runs it every day.
"""
 
from datetime import date, timedelta
from pathlib import Path
 
import pandas as pd
 
from nasa_power import fetch_daily
 
DATA_DIR = Path(__file__).parent.parent / "data"
SNAPSHOT_FILE = DATA_DIR / "nyc_daily_1981_2025.csv"  # frozen copy the notebooks use
LATEST_FILE = DATA_DIR / "nyc_daily_latest.csv"       # living copy the dashboard uses
 
# NASA sometimes revises the last few days, so we download them again each time.
REFETCH_DAYS = 14
 
 
def main():
    # 1. Start from the living file. The very first time, copy the frozen snapshot.
    source = LATEST_FILE if LATEST_FILE.exists() else SNAPSHOT_FILE
    old = pd.read_csv(source, index_col="date", parse_dates=True)
    last_day = old.index.max().date()
    print(f"Have data up to {last_day} ({len(old)} days).")
 
    # 2. Ask NASA for everything from a little before our last day up to today.
    start = last_day - timedelta(days=REFETCH_DAYS)
    end = date.today()
    new = fetch_daily(start.strftime("%Y%m%d"), end.strftime("%Y%m%d"))
 
    # 3. NASA runs a few days behind. Days it doesn't have yet come back empty, so drop them.
    new = new.dropna(how="all")
    if new.empty:
        print("NASA had nothing new. Nothing to do.")
        return
 
    # 4. Glue old and new together. Where a date is in both, keep NASA's newer value.
    combined = pd.concat([old, new])
    combined = combined[~combined.index.duplicated(keep="last")].sort_index()
 
    # 5. Save, rounded to 2 decimals like the original file.
    combined.round(2).to_csv(LATEST_FILE)
    added = len(combined) - len(old)
    print(f"Saved {LATEST_FILE.name}: now up to {combined.index.max().date()} (+{added} days).")
 
 
if __name__ == "__main__":
    main()
 