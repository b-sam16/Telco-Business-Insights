import pandas as pd

def aggregate_data(df):
    """Aggregate user data to calculate the number of xDR sessions, session duration, total data usage, and total data volume per application."""

    # List of applications to analyze
    applications = ['Social Media', 'Google', 'Email', 'Youtube', 'Netflix', 'Gaming', 'Other']
    
    # Calculate Total Data Volume per Application
    for app in applications:
        df[f'{app} Total'] = df[f'{app} DL (Bytes)'] + df[f'{app} UL (Bytes)']
        
    # Aggregate basic metrics
    aggregated_data = df.groupby('IMSI').agg(
        num_sessions=('Bearer Id', 'count'),
        total_duration=('Dur. (ms)', 'sum'),
        total_dl=('Total DL (Bytes)', 'sum'),
        total_ul=('Total UL (Bytes)', 'sum')
    ).reset_index()
    aggregated_data['total_data'] = aggregated_data['total_dl'] + aggregated_data['total_ul']

    # Drop the 'total_dl' and 'total_ul' columns from the final output
    aggregated_data = aggregated_data.drop(columns=['total_dl', 'total_ul'])

    # Aggregate total data volume per application
    app_agg = df.groupby('IMSI')[[f'{app} Total' for app in applications]].sum().reset_index()
    
    # Merge application-specific aggregates into the main aggregated data
    aggregated_data = pd.merge(aggregated_data, app_agg, on='IMSI', how='left')
    
    return aggregated_data

def segment_users_by_duration(df):
    """Segment users into decile classes based on total session duration and calculate total data usage per decile."""
    # Segment users into decile classes based on total duration
    df['duration_decile'] = pd.qcut(df['total_duration'], 10, labels=False) + 1
    
    # Filter to top five decile classes
    top_five_deciles = df[df['duration_decile'] <= 5]
    
    # Compute total data per decile class
    decile_data = top_five_deciles.groupby('duration_decile').agg(
        total_data=('total_data', 'sum'),
        num_users=('IMSI', 'nunique')
    ).reset_index()
    
    return decile_data

def describe_variables(df):
    """Describe all relevant variables and their associated data types."""
    description = df.info()
    return description

def calculate_basic_metrics(df):
    """Calculate basic metrics such as mean, median, etc. and return in a table format."""
    basic_metrics = df.describe().T[['mean', '50%', 'std', 'min', 'max']]
    basic_metrics.rename(columns={'50%': 'median'}, inplace=True)
    return basic_metrics

def calculate_dispersion_parameters(df):
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    
    # Calculate dispersion parameters
    dispersion_metrics = numeric_df.describe().T[['std', 'min', '25%', '50%', '75%', 'max']]
    dispersion_metrics.rename(columns={
        'std': 'std_dev',
        '50%': 'median'
    }, inplace=True)
    
    # Add range column (max - min)
    dispersion_metrics['range'] = dispersion_metrics['max'] - dispersion_metrics['min']
    
    return dispersion_metrics