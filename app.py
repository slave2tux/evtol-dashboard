import streamlit as st
from modules.fetch_news import fetch_mightyfly_news
from modules.matrix_builder import get_competitor_matrix

st.set_page_config(page_title="EVtol Dashboard", layout="wide")
st.title("🚁 EVtol Market Dashboard")

import datetime

st.caption(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# Competitive Matrix
st.header("🏁 Competitive Landscape: 2026 Rankings")
matrix_df = get_competitor_matrix()
st.table(matrix_df)
st.success("🎯 Strategic Insight: MightyFly currently holds the 'Range Leadership' position in the 2026 Middle-Mile sector.")

import plotly.express as px
import pandas as pd

# Convert matrix data into a chart-friendly format
matrix_df_reset = matrix_df.reset_index()
range_payload_data = pd.DataFrame({
    "Company": ["MightyFly", "Zipline", "Wing", "Elroy Air"],
    "Range (Miles)": [1000, 15, 12, 300],
    "Payload (lbs)": [500, 8, 5, 500]
})

st.header("📊 Range vs Payload Comparison")
fig = px.scatter(
    range_payload_data,
    x="Range (Miles)",
    y="Payload (lbs)",
    text="Company",
    size="Payload (lbs)",
    color="Company",
    title="EVtol Competitors: Range vs Payload"
)

fig.update_traces(textposition="top center")
st.plotly_chart(fig, use_container_width=True)

# Live News Feed
st.sidebar.subheader("📡 Live Market Feed")
live_news = fetch_mightyfly_news()
if live_news:
    for article in live_news:
        st.sidebar.markdown(f"**[{article['title']}]({article['link']})**")
        st.sidebar.caption(f"Published: {article['published']}")
else:
    st.sidebar.write("No new MightyFly alerts in the last 24h.")

from modules.history import load_history
import pandas as pd
import plotly.express as px

st.header("📈 MightyFly Historical Specs")

history = load_history("MightyFly")

if history:
    df = pd.DataFrame(history, columns=["timestamp", "range_miles", "payload_lbs"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    fig = px.line(
        df,
        x="timestamp",
        y=["range_miles", "payload_lbs"],
        title="MightyFly Spec Changes Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No historical data yet.")

