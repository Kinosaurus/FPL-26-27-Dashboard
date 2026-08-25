import fpl_data

# Set gameweek 
GAMEWEEK = 1

# Get dataframe
player_stats = fpl_data.make_dataframe()
# print(player_stats)

# Make csv
fpl_data.make_csv(player_stats, GAMEWEEK)