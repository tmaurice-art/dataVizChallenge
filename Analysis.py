"""
Exploratory comparison of 2010 vs 2021 MLB season data.
Run as a script for summary stats and a comparison figure.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Load 2010 and 2021 baseball season data
df2010 = pd.read_csv("baseball10.csv")
df2021 = pd.read_csv("baseball21.csv")

# --- Summary (exploratory) ---
print("2010 data shape:", df2010.shape)
print("2021 data shape:", df2021.shape)
print("\n2010 data columns:", df2010.columns.tolist())
print("\nFirst few rows of 2010 data:")
print(df2010.head())

# --- Comparison: use both datasets ---
def season_totals(df):
    """Total runs and home runs per season (all games)."""
    total_runs = (df["visScore"] + df["homeScore"]).sum()
    total_hr = (df["visHR"] + df["homeHR"]).sum()
    n_games = len(df)
    return {
        "games": n_games,
        "total_runs": total_runs,
        "runs_per_game": total_runs / n_games if n_games else np.nan,
        "total_hr": total_hr,
        "hr_per_game": total_hr / n_games if n_games else np.nan,
    }

stats_2010 = season_totals(df2010)
stats_2021 = season_totals(df2021)

print("\n--- Season comparison ---")
print("2010: runs/game = {:.2f}, HR/game = {:.2f}".format(stats_2010["runs_per_game"], stats_2010["hr_per_game"]))
print("2021: runs/game = {:.2f}, HR/game = {:.2f}".format(stats_2021["runs_per_game"], stats_2021["hr_per_game"]))

# --- Visualization: 2010 vs 2021 ---
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

years = ["2010", "2021"]
runs_per_game = [stats_2010["runs_per_game"], stats_2021["runs_per_game"]]
hr_per_game = [stats_2010["hr_per_game"], stats_2021["hr_per_game"]]

axes[0].bar(years, runs_per_game, color=["#1f77b4", "#ff7f0e"])
axes[0].set_ylabel("Runs per game")
axes[0].set_title("Runs per game by season")

axes[1].bar(years, hr_per_game, color=["#1f77b4", "#ff7f0e"])
axes[1].set_ylabel("Home runs per game")
axes[1].set_title("Home runs per game by season")

plt.tight_layout()
plt.savefig("analysis_2010_vs_2021.png", dpi=150, bbox_inches="tight")
print("\nSaved comparison figure: analysis_2010_vs_2021.png")
plt.close()
# Stage 2: Curation of Content
# Aggregate data to get average runs per stadium

# Process 2010 data
avgDF_2010 = (df2010
    .assign(totalRuns = lambda df: df.homeScore + df.visScore)
    .assign(totalHR = lambda df: df.homeHR + df.visHR)
    .drop(columns = ['date', 'visiting'])
    .groupby(['home'], as_index=False)
    .mean()
)

# Process 2021 data
avgDF_2021 = (df2021
    .assign(totalRuns = lambda df: df.homeScore + df.visScore)
    .assign(totalHR = lambda df: df.homeHR + df.visHR)
    .drop(columns = ['date', 'visiting'])
    .groupby(['home'], as_index=False)
    .mean()
)

print("2010 Stadium Averages (Top 5):")
print(avgDF_2010.head())
print("\n2021 Stadium Averages (Top 5):")
print(avgDF_2021.head())
