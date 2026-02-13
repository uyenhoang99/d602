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
import datetime
import time

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
        print("Remove flights that are delayed for more than 60 minutes")
        initial_rows = len(df_filtered)
        df_filtered = df_filtered[df_filtered["DEP_DELAY"] <= 60]
        print(f"Removed {initial_rows - len(df_filtered)} rows with extreme delays")

        # Data cleaning step 3: create a 'DATE' column
        # Change "DAY_OF_MONTH" to "DAY"
        print("\nChanging the column 'DAY_OF_MONTH' to 'DAY'")
        df_filtered.rename(columns={"DAY_OF_MONTH": "DAY"}, inplace=True)
        # Create new column "DATE"
        print("Create a new column 'DATE' by combining the columns")
        df_filtered["DATE"] = pd.to_datetime(df_filtered[["YEAR", "MONTH", "DAY"]])
        print(df_filtered.head())

        # Data cleaning step 4: check the "MONTH" and "YEAR" columns to ensure each column only has 1 value
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
        df_filtered["DEP_TIME"] = df_filtered["DEP_TIME"].astype("int64")
        df_filtered["DEP_DELAY"] = df_filtered["DEP_DELAY"].astype("int64")
        df_filtered["ARR_TIME"] = df_filtered["ARR_TIME"].astype("int64")
        df_filtered["ARR_DELAY"] = df_filtered["ARR_DELAY"].astype("int64")
        # Check for data types 
        print(df_filtered.dtypes)

        # Data cleaning step 6: create datetime for scheduled departure time
        df_filtered["CRS_DEP_TIME"] = pd.to_datetime(df_filtered["CRS_DEP_TIME"].fillna(0).astype(str).str.zfill(4), format='%H%M', errors='coerce').dt.time.fillna('00:00')
        df_filtered["CRS_DEP_TIME"] = pd.to_datetime(df_filtered["CRS_DEP_TIME"].astype('str') + ' ' + df_filtered["DATE"].astype('str'))
        print(df_filtered.head())

        # Data cleaning step 7: convert to time for departure time
        df_filtered["DEP_TIME"] = pd.to_datetime(df_filtered["DEP_TIME"].fillna(0).astype(int).astype(str).str.zfill(4),format='%H%M', errors='coerce').dt.time.fillna('00:00')
        print(df_filtered.head())

        # Data cleaning step 8: convert to time for scheduled departure time
        df_filtered["CRS_ARR_TIME"] = pd.to_datetime(df_filtered["CRS_ARR_TIME"].fillna(0).astype(int).astype(str).str.zfill(4),format='%H%M', errors='coerce').dt.time.fillna('00:00')
        print(df_filtered.head())

        # Data cleaning step 9: convert to time for arrival time
        df_filtered["ARR_TIME"] = pd.to_datetime(df_filtered["ARR_TIME"].fillna(0).astype(int).astype(str).str.zfill(4),format='%H%M', errors='coerce').dt.time.fillna('00:00')
        print(df_filtered.head())

        # Save the filtered dataset
        df_filtered.to_csv("artifacts/cleaned_LAX_dataset_v1.csv", index = False, header = True)
        print(f"Data cleaning complete. File saved to the 'artifacts' folder")
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