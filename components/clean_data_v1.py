# coding: utf-8

"""
Data Cleaning Script - Version 1
D602 Task 2 - Flight Delay Analysis

This script cleans data from from the raw imported data file.

"""

import pandas as pd
import numpy as np

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
        
        # # Data cleaning step 1: check for missing values and remove rows with missing departure delay
        # print("Cleaning step 1: Check for missing values")
        # missing_vals = df_filtered.isna().sum()
        # print("There are ", missing_vals, "in the dataset")
        
        # if missing_vals > 0:
        #     print("Delete missing values")
        #     initial_rows = len(df_filtered)
        #     df_filtered = df_filtered.dropna(subset=["DEP_DELAY"])



        



    except FileNotFoundError:
        print("Error: file not found")


if __name__ == "__main__":
    filter_and_clean_data()