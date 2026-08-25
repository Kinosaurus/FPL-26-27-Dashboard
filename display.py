import streamlit as st
import requests
import pandas as pd
import plotly.express as px


# =========================
# CONFIG
# =========================

SOURCE = "https://fantasy.premierleague.com/api/bootstrap-static/"


# =========================
# FETCH DATA
# =========================

@st.cache_data
def get_data():

    response = requests.get(SOURCE)
    response.raise_for_status()

    data = response.json()

    # Players
    df = pd.DataFrame(data["elements"])

    return df


# =========================
# LOAD DATA
# =========================

df = get_data()

# Convert strings to numeric if possible
for col in df.columns:
    converted = pd.to_numeric(df[col], errors="coerce")
    if converted.notna().sum() == df[col].notna().sum():
        df[col] = converted


# =========================
# PAGE
# =========================

st.title("Fantasy Football Dashboard")

st.write(
    f"Showing data for {len(df)} players."
)


# =========================
# SIDEBAR
# =========================

st.sidebar.header("Chart Settings")


# X variable
x_variable = st.sidebar.selectbox(
    "X-axis",
    df.columns
)


# Y variable
y_variable = st.sidebar.selectbox(
    "Y-axis",
    df.columns
)

# Variable to rank by
numeric_columns = df.select_dtypes(include="number").columns

filter_variable = st.sidebar.selectbox(
    "Rank players by",
    numeric_columns
)

# Top N
top_n = st.sidebar.slider(
    "Top N players",
    min_value=1,
    max_value=len(df),
    value=10
)

df = df.nlargest(top_n, filter_variable)

# Chart type
chart_type = st.sidebar.selectbox(
    "Chart Type",
    [
        "Scatter",
        "Line",
        "Bar"
    ]
)


# =========================
# CHART
# =========================

st.subheader(
    f"{y_variable} vs {x_variable}"
)


if chart_type == "Scatter":

    fig = px.scatter(
        df,
        x=x_variable,
        y=y_variable,
        hover_name="web_name"
    )
    st.plotly_chart(
        fig,
        width=True
    )


elif chart_type == "Line":

    fig = px.line(
        df,
        x=x_variable,
        y=y_variable,
        title=f"{y_variable} vs {x_variable}",
        hover_name="web_name",
        markers=True
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


elif chart_type == "Bar":

    chart_df = df.sort_values(
        by=filter_variable,
        ascending=False
    )

    fig = px.bar(
        chart_df,
        x=x_variable,
        y=y_variable,
        title=f"Top {top_n} Players by {filter_variable}",
        hover_name="web_name"
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )