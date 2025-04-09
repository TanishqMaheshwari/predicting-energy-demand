import pandas as pd
import numpy as np
import glob
import os
from datetime import datetime
import holidays

def load_zonal_demand():
    """Load and combine all zonal demand CSV files."""
    demand_files = glob.glob('HourlyZonalDemand/PUB_DemandZonal_*.csv')
    dfs = []
    
    for file in demand_files:
        df = pd.read_csv(file, skiprows=3)  # Skip header rows
        dfs.append(df)
    
    demand_df = pd.concat(dfs, ignore_index=True)
    
    # Convert date and hour to datetime
    demand_df['datetime'] = pd.to_datetime(demand_df['Date']) + pd.to_timedelta(demand_df['Hour'] - 1, unit='h')
    demand_df = demand_df.sort_values('datetime')
    
    # Save the combined data to a CSV file
    output_file = 'combined_zonal_demand.csv'
    demand_df.to_csv(output_file, index=False)
    print(f"Combined zonal demand data saved to {output_file}")
    
    return demand_df

def load_climate_data():
    """Load and combine climate data from different regions into a multi-level dataframe."""
    climate_files = glob.glob('../ClimateData/*Climate.csv')
    dfs = []
    
    for file in climate_files:
        # Extract region name from filename (e.g., "NortheastClimate.csv" -> "Northeast")
        region = os.path.basename(file).split('Climate')[0]
        df = pd.read_csv(file, skiprows=3, nrows=63672)  # read until line 63676 after that we have mean data for each day
        df['datetime'] = pd.to_datetime(df['time'])
        df['region'] = region
        df = df.drop(columns=["time"])
        
        # Set multi-index with datetime and region
        df.set_index(['datetime', 'region'], inplace=True)
        dfs.append(df)
    
    # Combine all climate dataframes
    climate_df = pd.concat(dfs)
    
    # Sort the multi-index
    climate_df.sort_index(inplace=True)
    
    return climate_df

def merge_demand_climate(demand_df, climate_df):
    """Merge demand and climate data into a multi-level dataframe."""
    # First, melt the demand dataframe to have a region column
    demand_melted = demand_df.melt(
        id_vars=['datetime', 'Ontario Demand', 'hour', 'day_of_week', 'month', 'day_of_year', 'is_holiday', 'is_weekend'],
        value_vars=['Northwest', 'Northeast', 'Ottawa', 'East', 'Toronto', 'Essa', 'Bruce', 'Southwest', 'Niagara', 'West'],
        var_name='region',
        value_name='zonal_demand'
    )
    
    # Reset index of climate_df to make datetime and region regular columns
    climate_df_reset = climate_df.reset_index()
    
    # Merge on datetime and region columns
    merged_df = pd.merge(
        demand_melted,
        climate_df_reset,
        on=['datetime', 'region'],
        how='left'
    )
    
    # Set the multi-index after merging
    merged_df.set_index(['datetime', 'region'], inplace=True)
    merged_df.sort_index(inplace=True)
    
    return merged_df

def add_time_features(df):
    """Add time-based features to the dataframe."""
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    df['day_of_year'] = df['datetime'].dt.dayofyear
    
    # Add holiday information
    holiday_years = list(range(2018, 2026))
    ca_holidays = holidays.CA(prov='ON', years=holiday_years)
    df['is_holiday'] = df['datetime'].dt.date.isin(ca_holidays)
    df['is_weekend'] = df['day_of_week'].isin([5, 6])
    
    return df

def create_lag_features(df, target_col, lags=[24, 48, 168]):
    """Create lagged features for the target variable."""
    for lag in lags:
        df[f'{target_col}_lag_{lag}'] = df[target_col].shift(lag)
    
    # Drop rows with NaN values in any of the lagged features
    # This ensures we only keep complete data points
    df = df.dropna(subset=[f'{target_col}_lag_{lag}' for lag in lags])
    
    return df

def main():
    # Load and process demand data
    demand_df = load_zonal_demand()
    demand_df = add_time_features(demand_df)
    
    # Load and process climate data
    climate_df = load_climate_data()
    
    # Print shapes and index information for debugging
    print("Demand DataFrame shape:", demand_df.shape)
    print("Climate DataFrame shape:", climate_df.shape)
    print("\nClimate DataFrame index levels:", climate_df.index.names)
    print("\nSample of climate data:")
    print(climate_df.head())
    
    # Merge demand and climate data
    merged_df = merge_demand_climate(demand_df, climate_df)
    
    # Print merged dataframe information
    print("\nMerged DataFrame shape:", merged_df.shape)
    print("Merged DataFrame index levels:", merged_df.index.names)
    
    # Create lagged features for Ontario Demand
    merged_df = create_lag_features(merged_df, 'Ontario Demand')
    
    # Save processed data
    merged_df.to_csv('processed_data.csv')
    print("\nData processing complete. Processed data saved to 'processed_data.csv'")

if __name__ == "__main__":
    main() 