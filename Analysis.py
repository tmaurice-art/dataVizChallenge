import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# Load 2010 baseball season data
df2010 = pd.read_csv("baseball10.csv")

# Load 2021 baseball season data for comparison
df2021 = pd.read_csv("baseball21.csv")

print("2010 data shape:", df2010.shape)
print("2021 data shape:", df2021.shape)
print("\n2010 data columns:", df2010.columns.tolist())
print("\nFirst few rows of 2010 data:")
print(df2010.head())