!pip install plotly

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ------------------------------
# Load Dataset
# ------------------------------
df = pd.read_csv("World Happiness Report.csv")

# ------------------------------
# Sidebar
# ------------------------------
st.sidebar.title("Dashboard Filters")

score_range = st.sidebar.slider(
    "Select Happiness Score",
    float(df["Score"].min()),
    float(df["Score"].max()),
    (
        float(df["Score"].min()),
        float(df["Score"].max())
    )
)

top_n = st.sidebar.slider(
    "Top Countries",
    5,
    30,
    10
)

filtered = df[
    (df["Score"]>=score_range[0]) &
    (df["Score"]<=score_range[1])
]

# ------------------------------
# Title
# ------------------------------
st.title("🌍 World Happiness Report Dashboard")

st.markdown("""
Interactive dashboard exploring the factors affecting happiness around the world.
""")

# ------------------------------
# KPIs
# ------------------------------
c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Countries",
    len(filtered)
)

c2.metric(
    "Average Happiness",
    round(filtered["Score"].mean(),2)
)

c3.metric(
    "Highest Score",
    round(filtered["Score"].max(),2)
)

c4.metric(
    "Lowest Score",
    round(filtered["Score"].min(),2)
)

st.divider()

# ------------------------------
# Top Countries
# ------------------------------
st.subheader("Top Happiest Countries")

top = filtered.nlargest(top_n,"Score")

fig = px.bar(
    top,
    x="Country or region",
    y="Score",
    color="Score",
    color_continuous_scale="Viridis",
    text="Score"
)

fig.update_layout(
    height=500,
    template="plotly_white"
)

st.plotly_chart(fig,use_container_width=True)

# ------------------------------
# Scatter Plots
# ------------------------------

left,right = st.columns(2)

with left:

    fig = px.scatter(
        filtered,
        x="GDP per capita",
        y="Score",
        color="Score",
        hover_name="Country or region",
        trendline="ols",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig = px.scatter(
        filtered,
        x="Social support",
        y="Score",
        color="Social support",
        hover_name="Country or region",
        trendline="ols",
        color_continuous_scale="Cividis"
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig,use_container_width=True)

# ------------------------------
# More Scatter Charts
# ------------------------------

left,right = st.columns(2)

with left:

    fig = px.scatter(
        filtered,
        x="Healthy life expectancy",
        y="Score",
        color="Healthy life expectancy",
        hover_name="Country or region",
        trendline="ols",
        color_continuous_scale="Plasma"
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig = px.scatter(
        filtered,
        x="Freedom to make life choices",
        y="Score",
        color="Freedom to make life choices",
        hover_name="Country or region",
        trendline="ols",
        color_continuous_scale="Turbo"
    )

    fig.update_layout(template="plotly_white")

    st.plotly_chart(fig,use_container_width=True)

# ------------------------------
# Histogram
# ------------------------------

st.subheader("Distribution of Happiness Scores")

fig = px.histogram(
    filtered,
    x="Score",
    nbins=20,
    color_discrete_sequence=["#0072B2"]
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig,use_container_width=True)

# ------------------------------
# Correlation Heatmap
# ------------------------------

st.subheader("Correlation Matrix")

corr = filtered.select_dtypes(include="number").corr()

fig = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    aspect="auto"
)

fig.update_layout(template="plotly_white")

st.plotly_chart(fig,use_container_width=True)

# ------------------------------
# Radar Chart
# ------------------------------

st.subheader("Top 5 Countries Comparison")

top5 = filtered.nlargest(5,"Score")

features = [
    "GDP per capita",
    "Social support",
    "Healthy life expectancy",
    "Freedom to make life choices",
    "Generosity",
    "Perceptions of corruption"
]

fig = go.Figure()

for _,row in top5.iterrows():

    fig.add_trace(
        go.Scatterpolar(
            r=[row[f] for f in features],
            theta=features,
            fill="toself",
            name=row["Country or region"]
        )
    )

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    template="plotly_white",
    height=600
)

st.plotly_chart(fig,use_container_width=True)

# ------------------------------
# Data Table
# ------------------------------

st.subheader("Filtered Dataset")

st.dataframe(filtered)

csv = filtered.to_csv(index=False)

st.download_button(
    "Download Filtered Data",
    csv,
    "Filtered_Happiness.csv",
    "text/csv"
)

st.success("Dashboard Completed Successfully.")
