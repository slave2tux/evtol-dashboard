import pandas as pd
from modules.scrape_specs import scrape_mightyfly_specs_from_rss

def get_competitor_matrix():
    df = pd.read_csv("data/competitors.csv", encoding="utf-8")

    live = scrape_mightyfly_specs_from_rss()

    for key, value in live.items():
        if key in df.columns and value is not None:
            df.loc[df["Company"] == "MightyFly", key] = value

    return df.set_index("Company")

from modules.history import init_history_db, log_specs

init_history_db()  # ensure DB exists

live = scrape_mightyfly_specs_from_rss()

# Only log if we actually got real values
if live["Range (Miles)"] or live["Payload (lbs)"]:
    log_specs(live)
