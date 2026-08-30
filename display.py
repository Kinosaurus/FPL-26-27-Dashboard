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

@st.cache_data(ttl=300)
def get_data():

    response = requests.get(SOURCE)
    response.raise_for_status()

    data = response.json()

    # Players
    df = pd.DataFrame(data["elements"])

    # Adding position column
    position_map = {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Forward"
    }

    df["position"] = df["element_type"].map(position_map)

    team_map = {1: 'ARS', 2: 'AVL', 3: 'BOU', 4: 'BRE', 5: 'BHA', 6: 'CHE', 7: 'COV', 8: 'CRY', 9: 'EVE', 10: 'FUL', 11: 'HUL', 12: 'IPS', 13: 'LEE', 14: 'LIV', 15: 'MCI', 16: 'MUN', 17: 'NEW', 18: 'NFO', 19: 'TOT', 20: 'SUN'}
    df["team_name"] = df["team"].map(team_map)

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


# Variable to rank by
numeric_columns = df.select_dtypes(include="number").columns

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

if chart_type == "Scatter":

    # X variable
    x_variable = st.sidebar.selectbox(
        "X-axis",
        numeric_columns
    )


    # Y variable
    y_variable = st.sidebar.selectbox(
        "Y-axis",
        numeric_columns
    )

else:
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

st.sidebar.header("Filters:")

unique_positions = df["position"].unique().tolist()

# To filter by player position
position_filter = st.sidebar.multiselect(
    "Player position",
    unique_positions,
    default=unique_positions
)
df = df[df["position"].isin(position_filter)]

filter_variable = st.sidebar.selectbox(
    "Rank players by",
    ["None"] + list(numeric_columns)
)    

# Top N
top_n = 0
if filter_variable != "None":
    top_n = st.sidebar.slider(
        "Top N players",
        min_value=1,
        max_value=len(df),
        value=10
    )

    df = df.nlargest(top_n, filter_variable)        

if st.button("🔄 Refresh data"):
    st.cache_data.clear()
    st.rerun()

if chart_type == "Scatter":
     
    fig = px.scatter(
        df,
        x=x_variable,
        y=y_variable,
        hover_name="web_name",
        hover_data=["team_name"]
    )
     
    st.plotly_chart(
        fig,
        width="stretch"
    )

elif chart_type == "Line":

    fig = px.line(
        df,
        x=x_variable,
        y=y_variable,
        title=f"Top {top_n} Players by {filter_variable}",
        hover_name="web_name",
        hover_data=["team_name"],
        markers=True
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


elif chart_type == "Bar":

    fig = px.bar(
        df,
        x=x_variable,
        y=y_variable,
        title=f"Top {top_n} Players by {filter_variable}",
        hover_name="web_name",
        hover_data=["team_name"]
    )

    fig.update_layout(
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )