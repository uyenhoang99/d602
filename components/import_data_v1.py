# coding: utf-8

"""
Data Import Script - Version 1
D602 Task 2 - Flight Delay Analysis

This script imports data from the downloaded csv file.

"""

import pandas as pd

def import_data():
    """
    Import data from the downloaded raw CSV file extracted from the Bureau of Transportation Statistics.
    This is the initial version with basic functionality.
    """
    try: 
        # Import the dataset
        print("Importing the dataset")
        df = pd.read_csv("C:/Users/uyen/Desktop/d602/notebook/T_ONTIME_REPORTING.csv")

        # Inspect the dataset
        print("\nCounting the number of columns and rows of the dataset:")
        col_count = df.shape[0]
        row_count = df.shape[1]
        print("There are ", col_count, "columns and ", row_count, "rows in this dataset")

        # Inspect the column names
        print("\nObserve the column names")
        print("Column names: ", df.columns)

        # Output the raw imported data
        print("\nOuput the raw imported dataset into the artifacts folder")
        df.to_csv("artifacts/data.csv", index = False, header = True)

        # Complete the data import process
        print("\nData has been successfully imported")


    
    except FileNotFoundError:
        print("Error: file not found. Check the file address.")
        return None
        




if __name__ == "__main__":
    import_data()