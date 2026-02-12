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
    """
    df = pd.read_csv("C:/Users/uyen/Desktop/d602/artifacts/cleaned_LAX_dataset_v1.csv")
    print(df.head())
