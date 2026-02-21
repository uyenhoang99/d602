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
from datetime import datetime
import time

def filter_and_clean_data():
    """
    Filter data for departures from LAX and perform basic cleaning.
    This is the initial version with basic functionality.
    """
    try:
        # Load the raw dataset
        print("\nLoading the raw dataset")
        df = pd.read_csv("artifacts/data.csv")
        print(df.head())

        # Check for column data types
        l_dtype = {}
        
        for i in df.columns:
            data_type = str(df[i].dtype)
            l_dtype[i] = data_type
        print(l_dtype)

        # Select required columns
        print("\nTotal number of columns from the raw dataset:", len(df.columns))
        print("Selecting the required columns:")
        df = df[["YEAR", "MONTH", "DAY_OF_MONTH", "DAY_OF_WEEK", "ORIGIN", "DEST", "CRS_DEP_TIME", "DEP_TIME", "DEP_DELAY", "CRS_ARR_TIME",
                "ARR_TIME", "ARR_DELAY"]]
        print(df.columns)
        print("Remaining total number of required columns:", len(df.columns))

        # Change the column names
        print("\nChange the column names")
        df.columns = ["YEAR", "MONTH", "DAY", "DAY_OF_WEEK", "ORG_AIRPORT", "DEST_AIRPORT", "SCHEDULED_DEPARTURE", "DEPARTURE_TIME",
                      "DEPARTURE_DELAY", "SCHEDULED_ARRIVAL", "ARRIVAL_TIME", "ARRIVAL_DELAY"]
        print(df.columns)

        # Filter to departures from LAX
        print("\nFiltering LAX departures")
        lax_departures = "LAX"
        df_filtered = df[df["ORG_AIRPORT"] == lax_departures]
        print("Unique value(s) after filtering in 'ORG_AIRPORT' is/are ", df_filtered["ORG_AIRPORT"].unique())

        # Check that the ORIGIN column only contains LAX
        origin_values = df_filtered["ORG_AIRPORT"].unique()
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
        dep_delay_q1 = np.quantile(df_filtered["DEPARTURE_DELAY"], 0.25)
        dep_delay_q3 = np.quantile(df_filtered["DEPARTURE_DELAY"], 0.75)
        iqr = dep_delay_q3 - dep_delay_q1
        lower_bound = dep_delay_q1 - 1.5 * iqr
        upper_bound = dep_delay_q3 + 1.5 * iqr
        extreme_lb = [i for i in df_filtered["DEPARTURE_DELAY"] if i < lower_bound]
        extreme_ub = [i for i in df_filtered["DEPARTURE_DELAY"] if i > upper_bound]
        print("\nThe lower bound extreme value is ", lower_bound)
        print("There are", len(extreme_lb), "flights that departed earlier than 30 minutes")
        print("The upper bound extreme value is ", upper_bound)
        print("There are", len(extreme_ub), "flights delayed more than 34 minutes")
        print("However, the determined upper bound for outliers is 60 minutes. Therefore, remove flights that are delayed for more than 60 minutes")
        initial_rows = len(df_filtered)
        df_filtered = df_filtered[df_filtered["DEPARTURE_DELAY"] <= 60]
        print(f"Removed {initial_rows - len(df_filtered)} rows with extreme delays")

        # Data cleaning step 3: create a 'DATE' column
        print("\nCreate a new column 'DATE' by combining the columns")
        df_filtered["DATE"] = pd.to_datetime(df_filtered[["YEAR", "MONTH", "DAY"]])
        print(df_filtered.head())

        # Data cleaning step 4: check the "MONTH" and "YEAR" columns to ensure each column only has 1 value
        print("\nEnsure there is only one value in the 'MONTH' and 'YEAR' columns")
        months = df_filtered["MONTH"].unique()
        years = df_filtered["YEAR"].unique()
        if len(months) > 1:
            print("\nThere are more than 1 month in the 'MONTH' column")
        else:
            month = months[0]
            print("There is only 1 month in the 'MONTH' column:", month)
        if len(years) > 1:
            print("There are more than 1 years in the 'YEAR' column")
        else:
            year = years[0]
            print("There is only one year in the 'YEAR' column:", year)
        
        # Data cleaning step 5: change 'float' columns to 'integer' columns
        print("\nChange 'float' columns to 'integer' columns")
        df_filtered["DEPARTURE_TIME"] = df_filtered["DEPARTURE_TIME"].astype("int64")
        df_filtered["DEPARTURE_DELAY"] = df_filtered["DEPARTURE_DELAY"].astype("int64")
        df_filtered["ARRIVAL_TIME"] = df_filtered["ARRIVAL_TIME"].astype("int64")
        df_filtered["ARRIVAL_DELAY"] = df_filtered["ARRIVAL_DELAY"].astype("int64")
        # Check for data types 
        print(df_filtered.dtypes)

        # Data cleaning step 6: create datetime for scheduled departure
        print("\nCreate datetime data type for 'SCHEDULED_DEPARTURE'")
        df_filtered["SCHEDULED_DEPARTURE"] = pd.to_datetime(df_filtered["SCHEDULED_DEPARTURE"].fillna(0).astype(str).str.zfill(4), format='%H%M', errors='coerce').dt.time.fillna('00:00')
        df_filtered["SCHEDULED_DEPARTURE"] = pd.to_datetime(df_filtered["SCHEDULED_DEPARTURE"].astype('str') + ' ' + df_filtered["DATE"].astype('str'))
        df_filtered["SCHEDULED_DEPARTURE"] = pd.to_datetime(df_filtered["SCHEDULED_DEPARTURE"])
        print(df_filtered.head())

        # Data cleaning step 7: convert to time for departure time
        print("\nChange 'integer' values to time (HH:MM:SS) format")
        df_filtered["DEPARTURE_TIME"] = pd.to_datetime(df_filtered["DEPARTURE_TIME"].fillna(0).astype(int).astype(str).str.zfill(4),format='%H%M', errors='coerce').dt.time.fillna('00:00')
        print(df_filtered.head())

        # # Data cleaning step 8: convert to time for scheduled arrival
        print("\nChange 'integer' values to time (HH:MM:SS) format")
        df_filtered["SCHEDULED_ARRIVAL"] = pd.to_datetime(df_filtered["SCHEDULED_ARRIVAL"].fillna(0).astype(int).astype(str).str.zfill(4),format='%H%M', errors='coerce').dt.time.fillna('00:00')
        print(df_filtered.head())

        # # Data cleaning step 9: convert to time for arrival time
        print("\nChange 'integer' values to time (HH:MM:SS) format")
        df_filtered["ARRIVAL_TIME"] = pd.to_datetime(df_filtered["ARRIVAL_TIME"].fillna(0).astype(int).astype(str).str.zfill(4),format='%H%M', errors='coerce').dt.time.fillna('00:00')
        print(df_filtered.head())

        # Save the filtered dataset
        df_filtered.to_csv("artifacts/cleaned_LAX_dataset_v1.csv", index = False, header = True)
        print("Data cleaning complete. File saved to the 'artifacts' folder")
        print(f"Final dataset shape: {df_filtered.shape}")

        return df_filtered


        
 
    except FileNotFoundError:
        print("Error: file not found. Run import script first.")
        return None
    except Exception as e:
        print(f"Error during data cleaning: {str(e)}")
        return None



if __name__ == "__main__":
    filter_and_clean_data()