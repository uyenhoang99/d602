# coding: utf-8

"""
MLFlow Experiment Script - Version 1
D602 Task 2 - Flight Delay Analysis

This script performs an MLFlow experiment for polynomial regression
to predict average flight delays. This is the initial version with basic MLFlow tracking.
Based on poly_regressor_Python_1.0.0.py template.

"""

import datetime
import pandas as pd
import argparse
import numpy as np
from sklearn.preprocessing import PolynomialFeatures, LabelEncoder, OneHotEncoder
from sklearn import metrics, linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
import mlflow
import mlflow.sklearn
import logging
import os
import pickle
import json

def load_and_prepare_data():
    """
    Load and prepare data for modeling.
    Based on poly_regressor_Python_1.0.0.py data loading approach.
    """
    print("\nLoading the cleansed dataset")
    df = pd.read_csv("artifacts/cleaned_LAX_dataset_v1.csv")
    print(df.shape)
    print(df.info())

    # Create the time formatting formula
    ft = lambda x: x.hour*3600 + x.minute*60 + x.second  #formula for formatting time in seconds

    # Step 1: Calculate the depart hour in seconds
    print("\nChange 'SCHEDULED_DEPARTURE' to datetime")
    df["SCHEDULED_DEPARTURE"] = pd.to_datetime(df["SCHEDULED_DEPARTURE"])
    print("Format 'SCHEDULED_DEPART' in seconds and store in 'hour_depart")
    df["hour_depart"] = df["SCHEDULED_DEPARTURE"].apply(lambda x: x.time())
    df["hour_depart"] = df["hour_depart"].apply(ft)

    # Step 2: Calculate the arrival hour in seconds
    print("\nChange 'SCHEDULED_ARRIVAL' to datetime")
    df["hour_arrive"] = pd.to_datetime(df["SCHEDULED_ARRIVAL"], format='%H:%M:%S')
    print("Format 'SCHEDULED_ARRIVAL' in seconds and store in 'hour_arrive")
    df["hour_arrive"] = df["hour_arrive"].apply(lambda x: x.time())
    df["hour_arrive"] = df["hour_arrive"].apply(ft)

    # Step 3: Determine the 'weekday' number for 'SCHEDULED_DEPARTURE'. Monday is 0 and Sunday is 6.
    print("\nCreate the 'weekday' column to calculate the corresponding weekday [Monday = 0, Sunday = 6]")
    df["weekday"] = df["SCHEDULED_DEPARTURE"].apply(lambda x: x.weekday())

    # Step 4: Define training data as the first 3 weeks of the month and test data as that from the fourth week of the month
    print("\nSplit into train and test datasets. First three weeks are for train data.")
    year = df["YEAR"].unique()
    year = year[0]
    month = df["MONTH"].unique()
    month = month[0]
    
    print("\nTrain data")
    df_train = df[df["SCHEDULED_DEPARTURE"].apply(lambda x: x.date()) < datetime.date(year, month, 21)]
    print(df_train.head())
    print("\nTest data")
    df_test = df[df["SCHEDULED_DEPARTURE"].apply(lambda x: x.date()) > datetime.date(year, month, 21)]
    print(df_test.head())


    # Step 5: Output the train and test dataframe
    print("\nOutput the train data to 'train_data.csv' in the 'artifacts' folder")
    df_train.to_csv("artifacts/train_data.csv", index=False, header=True)
    print("Train data exported to the 'artifacts' folder")

    print("\nOutput the test data to 'test_data.csv' in the 'artifacts' folder")
    df_test.to_csv("artifacts/test_data.csv", index=False, header=True)
    print("Test data exported to the 'artifacts' folder")

    
    # Step 6: Perform One-Hot encoding of DEST_AIRPORT in training data
    print("\All unique values in 'DEST_AIRPORT'")
    print(df_train["DEST_AIRPORT"].unique())

    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(df_train["DEST_AIRPORT"])
    zipped = zip(integer_encoded, df_train["DEST_AIRPORT"])
    label_airports = list(set(list(zipped)))
    label_airports.sort(key = lambda x: x[0])
    print(label_airports)

    onehot_encoder = OneHotEncoder(sparse_output=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    print(onehot_encoded)

    # Step 7: Create arrays of required columns
    print("\nRequired columns: hour_depart, hour_arrive, DEST_AIRPORT, DEPARTURE_DELAY")
    b = np.array(df_train[['hour_depart', "hour_arrive"]])
    X = np.hstack((onehot_encoded, b))
    Y = np.array(df_train["DEPARTURE_DELAY"])
    Y = Y.reshape(len(Y), 1)

    # Step 8: Create train/validation split at 20%
    X_train, X_validate, Y_train, Y_validate = train_test_split(X, Y, test_size=0.2)


def run_mlflow_experiment():
    num_alphas = 40

    nowdate = datetime.date.today()
    experiment_name = "Airport Departure Delays, experiment run on" + str(nowdate)
    experiment = mlflow.set_experiment(experiment_name)
    run_name = "Run started at" + datetime.datetime.now().strftime("%H:%M")

    mlflow.start_run(experiment_id=experiment.experiment_id, run_name=run_name)

    score_min = 10000
    count = 1
    order = 2

    for alpha in range(0,num_alphas,2):
        run_num = "Training Run Number" + str(count)
        ridgereg = 








if __name__ == "__main__":
    load_and_prepare_data()
    run_mlflow_experiment()