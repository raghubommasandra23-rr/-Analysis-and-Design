import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------
# Load Dataset
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("World Happiness Report.csv")

df = load_data()

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("Dashboard Filters")

score_range = st.sidebar.slider(
    "Happiness Score",
    float(df["Score"].min()),
    float(df["Score"].max()),
    (
        float(df["Score"].min()),
        float(df["Score"].max())
    )
)

filtered_df = df[
    (df["Score"] >= score_range[0]) &
    (df["Score"] <= score_range[1])
]

top_n = st.sidebar.slider(
    "Top Countries",
    5,
    30,
    10
)

# ---------------------------
# Dashboard Title
# ---------------------------
st.title("🌍 World Happiness Report Dashboard")
st.markdown("### Interactive Analysis using Plotly")

# ---------------------------
# KPI Cards
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Countries", len(filtered_df))

with col2:
    st.metric(
        "Average Happiness",
        round(filtered_df["Score"].mean(),2)
    )

with col3:
    st.metric(
        "Highest Score",
        round(filtered_df["Score"].max(),2)
    )

with col4:
    st.metric(
        "Average GDP",
        round(filtered_df["GDP per capita"].mean(),2)
    )

st.divider()

# ==================================================
# Chart 1
# ==================================================
st.subheader("Top Happiest Countries")

top = filtered_df.nlargest(top_n,"Score")

fig = px.bar(
    top,
    x="Country or region",
    y="Score",
    color="Score",
    color_continuous_scale="Viridis"
)

fig.update_layout(
    xaxis_title="Country",
    yaxis_title="Happiness Score",
    template="plotly_white",
    height=500
)

st.plotly_chart(fig,use_container_width=True)

# ==================================================
# Scatter Charts
# ==================================================

col1,col2=st.columns(2)

with col1:

    fig=px.scatter(
        filtered_df,
        x="GDP per capita",
        y="Score",
        hover_name="Country or region",
        trendline="ols",
        color="Score",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        title="GDP vs Happiness",
        template="plotly_white"
    )

    st.plotly_chart(fig,use_container_width=True)

with col2:

    fig=px.scatter(
        filtered_df,
        x="Social support",
        y="Score",
        hover_name="Country or region",
        trendline="ols",
        color="Social support",
        color_continuous_scale="Cividis"
    )

    fig.update_layout(
        title="Social Support vs Happiness",
        template="plotly_white"
    )

    st.plotly_chart(fig,use_container_width=True)

# ==================================================
# Second Row
# ==================================================

col1,col2=st.columns(2)

with col1:

    fig=px.scatter(
        filtered_df,
        x="Healthy life expectancy",
        y="Score",
        hover_name="Country or region",
        trendline="ols",
        color="Healthy life expectancy",
        color_continuous_scale="Plasma"
    )

    fig.update_layout(
        title="Healthy Life Expectancy",
        template="plotly_white"
    )

    st.plotly_chart(fig,use_container_width=True)

with col2:

    fig=px.scatter(
        filtered_df,
        x="Freedom to make life choices",
        y="Score",
        hover_name="Country or region",
        trendline="ols",
        color="Freedom to make life choices",
        color_continuous_scale="Turbo"
    )

    fig.update_layout(
        title="Freedom vs Happiness",
        template="plotly_white"
    )

    st.plotly_chart(fig,use_container_width=True)

# ==================================================
# Third Row
# ==================================================

col1,col2=st.columns(2)

with col1:

    fig=px.scatter(
        filtered_df,
        x="Generosity",
        y="Score",
        hover_name="Country or region",
        trendline="ols",
        color="Generosity",
        color_continuous_scale="Teal"
    )

    fig.update_layout(
        title="Generosity vs Happiness",
        template="plotly_white"
    )

    st.plotly_chart(fig,use_container_width=True)

with col2:

    fig=px.scatter(
        filtered_df,
        x="Perceptions of corruption",
        y="Score",
        hover_name="Country or region",
        trendline="ols",
        color="Perceptions of corruption",
        color_continuous_scale="Inferno"
    )

    fig.update_layout(
        title="Corruption vs Happiness",
        template="plotly_white"
    )

    st.plotly_chart(fig,use_container_width=True)

# ==================================================
# Correlation Chart
# ==================================================

st.subheader("Correlation with Happiness Score")

corr = filtered_df.corr(numeric_only=True)["Score"].sort_values()

fig = px.bar(
    x=corr.values,
    y=corr.index,
    orientation="h",
    color=corr.values,
    color_continuous_scale="RdBu"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Correlation",
    yaxis_title=""
)

st.plotly_chart(fig,use_container_width=True)

# ==================================================
# Distribution
# ==================================================

col1,col2=st.columns(2)

with col1:

    fig=px.histogram(
        filtered_df,
        x="Score",
        nbins=20,
        color_discrete_sequence=["royalblue"]
    )

    fig.update_layout(
        title="Distribution of Happiness Scores",
        template="plotly_white"
    )

    st.plotly_chart(fig,use_container_width=True)

with col2:

    top5=filtered_df.nlargest(5,"Score")

    categories=[
        "GDP per capita",
        "Social support",
        "Healthy life expectancy",
        "Freedom to make life choices",
        "Generosity",
        "Perceptions of corruption"
    ]

    radar=go.Figure()

    for _,row in top5.iterrows():

        radar.add_trace(go.Scatterpolar(
            r=[row[c] for c in categories],
            theta=categories,
            fill="toself",
            name=row["Country or region"]
        ))

    radar.update_layout(
        template="plotly_white",
        polar=dict(radialaxis=dict(visible=True)),
        title="Top 5 Countries Comparison"
    )

    st.plotly_chart(radar,use_container_width=True)

# ==================================================
# Data Table
# ==================================================

st.subheader("Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# ==================================================
# Download Button
# ==================================================

csv=filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Dataset",
    csv,
    file_name="Filtered_Happiness_Data.csv",
    mime="text/csv"
)

# ==================================================
# Footer
# ==================================================

st.markdown("---")

st.markdown(
"""
**Dashboard Features**

- Interactive sidebar filters
- KPI summary cards
- 8 Plotly publication-ready visualizations
- Correlation analysis
- Radar comparison
- Download filtered dataset
"""
)
