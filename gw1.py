import pandas as pd
import matplotlib.pyplot as plt

gameweek = 1

gw1_csv = fr"C:\Users\kinso\Documents\Knowledge Quest\Data Analytics\FPL 2627\GW{gameweek}\GW{gameweek}.csv"
gw1_df = pd.read_csv(gw1_csv)

gw1_df_cols = list(gw1_df.columns)
print(gw1_df_cols)

plt.scatter(gw1_df["defensive_contribution"], gw1_df["expected_goal_involvements"], s=10)

top_5_dc = gw1_df.nlargest(5, "defensive_contribution")
top_5_egi = gw1_df.nlargest(5, "expected_goal_involvements")

# Annotate Top 5 Defensive Contribution
for _, row in top_5_dc.iterrows():
    plt.annotate(
        text=row["web_name"],
        xy=(row["defensive_contribution"], row["expected_goal_involvements"]),
        textcoords="offset points",
        xytext=(30, 0),
        ha="center"
    )

# Annotate Top 5 Expected Goal Involvements
for _, row in top_5_egi.iterrows():
    plt.annotate(
        text=row["web_name"],
        xy=(row["defensive_contribution"], row["expected_goal_involvements"]),
        textcoords="offset points",
        xytext=(30, 0),
        ha="center"
    )

plt.xlabel("Defensive Contribution")
plt.ylabel("Expected Goal Involvements")
plt.show()