import pandas as pd
from scipy.stats import iqr

def clean_data(df):
    """Clean the data by handling missing values and outliers."""
    
    # Separate numeric and non-numeric columns
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    non_numeric_columns = df.select_dtypes(exclude=['float64', 'int64']).columns
    
    # Handle missing values for numeric columns by replacing with the column mean
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
    
    # Handle missing values for non-numeric columns by replacing with the mode (most frequent value)
    for col in non_numeric_columns:
        df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Identify outliers using the IQR method and replace them with the median for numeric columns
    for column in numeric_columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        outlier_threshold = iqr(df[column]) * 1.5
        lower_bound = q1 - outlier_threshold
        upper_bound = q3 + outlier_threshold
        df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
    
    return df
