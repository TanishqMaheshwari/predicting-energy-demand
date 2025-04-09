# %% [markdown]
# # IESO Data Exploration Notebook
# 
# This notebook allows you to explore and visualize the IESO data processed by `process_data.py`.

# %%
# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from process_data import load_zonal_demand, add_time_features, create_lag_features

# Set up plotting style
plt.style.use('seaborn')
sns.set_palette('husl')
%matplotlib inline

# %% [markdown]
# ## Load and Process Data

# %%
# Load the zonal demand data
demand_df = load_zonal_demand()
print(f"Data shape: {demand_df.shape}")
demand_df.head()

# %% [markdown]
# ## Basic Data Exploration

# %%
# Display basic statistics
demand_df.describe()

# %%
# Check for missing values
demand_df.isnull().sum()

# %% [markdown]
# ## Time Series Visualization

# %%
# Plot Ontario Demand over time
plt.figure(figsize=(15, 6))
plt.plot(demand_df['datetime'], demand_df['Ontario Demand'])
plt.title('Ontario Energy Demand Over Time')
plt.xlabel('Date')
plt.ylabel('Demand (MW)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Zonal Demand Analysis

# %%
# Plot demand by zone
zones = ['Northwest', 'Northeast', 'Ottawa', 'East', 'Toronto', 
         'Essa', 'Bruce', 'Southwest', 'Niagara', 'West']

plt.figure(figsize=(15, 8))
for zone in zones:
    plt.plot(demand_df['datetime'], demand_df[zone], label=zone)
plt.title('Energy Demand by Zone')
plt.xlabel('Date')
plt.ylabel('Demand (MW)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Add Time Features and Explore Patterns

# %%
# Add time features
demand_df = add_time_features(demand_df)

# Plot average demand by hour of day
hourly_avg = demand_df.groupby('hour')['Ontario Demand'].mean()
plt.figure(figsize=(12, 6))
hourly_avg.plot(kind='bar')
plt.title('Average Demand by Hour of Day')
plt.xlabel('Hour of Day')
plt.ylabel('Average Demand (MW)')
plt.tight_layout()
plt.show()

# %%
# Plot average demand by day of week
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_avg = demand_df.groupby('day_of_week')['Ontario Demand'].mean()
plt.figure(figsize=(12, 6))
daily_avg.plot(kind='bar')
plt.title('Average Demand by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Average Demand (MW)')
plt.xticks(range(7), day_names)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Create and Explore Lagged Features

# %%
# Add lagged features
demand_df = create_lag_features(demand_df, 'Ontario Demand')

# Plot correlation between current demand and lagged values
lag_columns = ['Ontario Demand_lag_24', 'Ontario Demand_lag_48', 'Ontario Demand_lag_168']
correlation = demand_df[['Ontario Demand'] + lag_columns].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlation between Current Demand and Lagged Values')
plt.tight_layout()
plt.show() 