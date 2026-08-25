import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from adjustText import adjust_text

SOURCE = "https://fantasy.premierleague.com/api/bootstrap-static/"

pd.options.display.max_columns = None
pd.options.display.max_rows = None

def get_nested_keys(data, current_path=""):
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{current_path}/{key}" if current_path else str(key)
            yield new_path
            yield from get_nested_keys(value, new_path)

def get_path(source: str=SOURCE) -> None:
    request = requests.get(source)
    response = request.json()

    for path in get_nested_keys(response):
        print(path)

def make_dataframe(source: str=SOURCE) -> pd.DataFrame:
    request = requests.get(source)
    response = request.json()

    # print(response["element_stats"])

    # print(len(response["elements"]))
    # print(json.dumps(response["elements"][0], indent=4))

    # Getting player stats
    player_stats = pd.DataFrame(response["elements"])
    # Getting column names
    # col_names = player_stats.columns.to_list()
    # print(col_names)

    # Making new column for days at club
    today = pd.Timestamp.today()
    player_stats["team_join_date"] = pd.to_datetime(player_stats["team_join_date"], format="%Y-%m-%d")
    player_stats["days_at_club"] = (today - player_stats["team_join_date"]).dt.days
    return player_stats

def make_csv(player_stats: pd.DataFrame, gameweek: int):
    #---- Saving to csv ----
    player_stats.to_csv(rf"C:\Users\kinso\Documents\Knowledge Quest\Data Analytics\FPL-26-27-Dashboard\GW{gameweek}\GW{gameweek}.csv")

# # Getting each team's fpl strength
# print(json.dumps(response["teams"], indent=4))

# team_df = pd.DataFrame(response["teams"])

# fig, ax = plt.subplots(figsize=(10, 10))

# ax.scatter(team_df["strength_overall_home"], team_df["strength_overall_away"])

# texts = []
# for index, row in team_df.iterrows():
#     texts.append(ax.text(row["strength_overall_home"], row["strength_overall_away"], row["short_name"]))

# adjust_text(texts, ax=ax, force_static=(1.5, 2))
# ax.set_xlabel("Overall Strength (Home)")
# ax.set_ylabel("Overall Strength (Away)")

# plt.show()