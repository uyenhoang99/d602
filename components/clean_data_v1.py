# coding: utf-8

"""
Data Cleaning Script - Version 1
D602 Task 2 - Flight Delay Analysis

This script cleans data from from the raw imported data file.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def filter_and_clean_data():
    """
    Filter data for departures from LAX and perform basic cleaning.
    This is the initial version with basic functionality.
    """
    try:
        # Load the raw dataset
        print("Loading the raw dataset")
        df = pd.read_csv("artifacts/data.csv")
        print(df.head())

        # Check for column data types
        l_dtype = {}
        
        for i in df.columns:
            data_type = str(df[i].dtype)
            l_dtype[i] = data_type
        print(l_dtype)

        # Filter to departures from LAX
        print("\nFiltering LAX departures")
        lax_departures = "LAX"
        df_filtered = df[df["ORIGIN"] == lax_departures]
        print("Unique value(s) after filtering in 'ORIGIN' is/are ", df_filtered["ORIGIN"].unique())

        # Check that the ORIGIN column only contains LAX
        origin_values = df_filtered["ORIGIN"].unique()
        len_origin_values = len(origin_values)

        if origin_values == "LAX" and len_origin_values == 1:
            print("Successfully filtered for LAX departures")
        else:
            print("Warning: failed to filter for LAX departures")
        
        # Data cleaning step 1: check for missing values and remove rows with missing departure delay
        print("\nCleaning step 1: Check for missing values")
        missing_vals = df_filtered.isna().sum()
        print("Missing values per column:\n ", missing_vals)
        
        sum_missing_vals = df_filtered.isna().sum().sum()
        if sum_missing_vals > 0:
            print("\nDelete missing values")
            initial_rows = len(df_filtered)
            df_filtered = df_filtered.dropna(how='any')
            print(f"Removed {initial_rows - len(df_filtered)} rows with missing departure delays")
        
        # Data cleaning step 2: check for outliers in the departure delay column and remove rows with extreme outliers
        dep_delay_q1 = np.quantile(df_filtered["DEP_DELAY"], 0.25)
        dep_delay_q3 = np.quantile(df_filtered["DEP_DELAY"], 0.75)
        iqr = dep_delay_q3 - dep_delay_q1
        lower_bound = dep_delay_q1 - 1.5 * iqr
        upper_bound = dep_delay_q3 + 1.5 * iqr
        extreme_lb = [i for i in df_filtered["DEP_DELAY"] if i < lower_bound]
        extreme_ub = [i for i in df_filtered["DEP_DELAY"] if i > upper_bound]
        print("\nThe lower bound extreme value is ", lower_bound)
        print("There are", len(extreme_lb), "flights that departed earlier than 30 minutes")
        print("The upper bound extreme value is ", upper_bound)
        print("There are", len(extreme_ub), "flights delayed more than 34 minutes")
        print("Remove flights that are delayed for more than 200 minutes")
        initial_rows = len(df_filtered)
        df_filtered = df_filtered[df_filtered["DEP_DELAY"] <= 200]
        print(f"Removed {initial_rows - len(df_filtered)} rows with extreme delays")






        



    except FileNotFoundError:
        print("Error: file not found")


if __name__ == "__main__":
    filter_and_clean_data()