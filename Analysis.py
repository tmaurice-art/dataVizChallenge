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
# Stage 3: Structuring of Visual Mappings
# Explore different geometries and aesthetics

# Sort data for better visualization
avgDF_2010_sorted = avgDF_2010.sort_values('totalRuns', ascending=True)

# Create figure with subplots to compare approaches
fig, axes = plt.subplots(2, 2, figsize=(8, 9))

# Approach 1: Scatter plot (not ideal for categorical data)
axes[0,0].scatter(avgDF_2010_sorted.home, avgDF_2010_sorted.totalRuns)
axes[0,0].set_title("Approach 1: Scatter Plot")
axes[0,0].set_xlabel("Stadium")
axes[0,0].set_ylabel("Average Runs")
axes[0,0].tick_params(axis='x', labelsize=9)

# Approach 2: Horizontal bar chart (better for categorical data)
axes[0,1].barh(avgDF_2010_sorted.home, avgDF_2010_sorted.totalRuns)
axes[0,1].set_title("Approach 2: Horizontal Bar Chart")
axes[0,1].set_xlabel("Average Runs")
axes[0,1].set_ylabel("Stadium")
axes[0,1].tick_params(axis='y', labelsize=9)

# Approach 3: Vertical bar chart
axes[1,0].bar(avgDF_2010_sorted.home, avgDF_2010_sorted.totalRuns)
axes[1,0].set_title("Approach 3: Vertical Bar Chart")
axes[1,0].set_xlabel("Stadium")
axes[1,0].set_ylabel("Average Runs")
axes[1,0].tick_params(axis='x', rotation=45, labelsize=9)

# Approach 4: Highlight Colorado
colorado_colors = ["darkorchid" if stadium == "COL" else "lightgrey" 
                   for stadium in avgDF_2010_sorted.home]
axes[1,1].barh(avgDF_2010_sorted.home, avgDF_2010_sorted.totalRuns, color=colorado_colors)
axes[1,1].set_title("Approach 4: Highlight Colorado")
axes[1,1].set_xlabel("Average Runs")
axes[1,1].set_ylabel("Stadium")
axes[1,1].tick_params(axis='y', labelsize=9)

plt.tight_layout()
plt.show()
# Stage 4: Formatting for Your Audience
# Create a professional, publication-ready visualization

# Set style for professional appearance
plt.style.use("seaborn-v0_8-whitegrid")

# Create the main visualization
fig, ax = plt.subplots(figsize=(8, 6))

# Create color array for highlighting Colorado
colorado_colors = ["darkorchid" if stadium == "COL" else "lightgrey" 
                   for stadium in avgDF_2010_sorted.home]

# Create horizontal bar chart
bars = ax.barh(avgDF_2010_sorted.home, avgDF_2010_sorted.totalRuns, color=colorado_colors)

# Add title and labels
ax.set_title("Colorado (COL) is the Most Run-Friendly Ballpark in 2010", 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel("Average Runs Per Game", fontsize=12)
ax.set_ylabel("Stadium (Home Team)", fontsize=12)

# Add legend
colorado_bar = plt.Rectangle((0,0),1,1, color="darkorchid", label="Colorado Rockies")
other_bar = plt.Rectangle((0,0),1,1, color="lightgrey", label="Other Stadiums")
ax.legend(handles=[colorado_bar, other_bar], loc='lower right', frameon=True)

# Add annotation for Colorado
colorado_index = avgDF_2010_sorted[avgDF_2010_sorted.home == "COL"].index[0]
colorado_runs = avgDF_2010_sorted[avgDF_2010_sorted.home == "COL"]["totalRuns"].iloc[0]
ax.annotate(f"COL: {colorado_runs:.2f} runs/game", 
            xy=(colorado_runs, colorado_index), 
            xytext=(colorado_runs + 0.5, colorado_index),
            arrowprops=dict(arrowstyle='->', color='darkorchid', lw=2),
            fontsize=10, fontweight='bold', color='darkorchid')

# Set x-axis to start from 0 for better comparison
ax.set_xlim(0, max(avgDF_2010_sorted.totalRuns) * 1.1)

# Smaller font for stadium (y-axis) tick labels
ax.tick_params(axis='y', labelsize=9)

# Add grid for easier reading
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Print summary statistics
print(f"\nSummary Statistics for 2010:")
print(f"Colorado (COL) average runs per game: {colorado_runs:.2f}")
print(f"League average runs per game: {avgDF_2010_sorted.totalRuns.mean():.2f}")
print(f"Colorado is {((colorado_runs / avgDF_2010_sorted.totalRuns.mean()) - 1) * 100:.1f}% above league average")
# Advanced Object-Oriented Techniques
# Create a comprehensive comparison visualization

# Prepare data for comparison
comparison_data = pd.merge(
    avgDF_2010[['home', 'totalRuns']].rename(columns={'totalRuns': 'runs_2010'}),
    avgDF_2021[['home', 'totalRuns']].rename(columns={'totalRuns': 'runs_2021'}),
    on='home', how='inner'
)

## TODO: Create the visualization
