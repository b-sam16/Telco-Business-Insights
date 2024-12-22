import pandas as pd

def aggregate_data(df):
    """Aggregate user data to calculate the number of xDR sessions, session duration, total data usage, and total data volume per application."""
    # Aggregate basic metrics
    aggregated_data = df.groupby('IMSI').agg(
        num_sessions=('Bearer Id', 'count'),
        total_duration=('Dur. (ms)', 'sum'),
        total_dl=('Total DL (Bytes)', 'sum'),
        total_ul=('Total UL (Bytes)', 'sum')
    ).reset_index()
    aggregated_data['total_data'] = aggregated_data['total_dl'] + aggregated_data['total_ul']
    
    # List of application columns
    application_columns = ['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)',
                           'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)',
                           'Social Media UL (Bytes)', 'Google UL (Bytes)', 'Email UL (Bytes)',
                           'Youtube UL (Bytes)', 'Netflix UL (Bytes)', 'Gaming UL (Bytes)', 'Other UL (Bytes)']
    
    # Aggregate total data volume per application
    for app in application_columns:
        if app in df.columns:
            app_dl = app
            app_ul = app.replace('DL', 'UL')
            aggregated_data[app_dl] = df.groupby('IMSI')[app_dl].sum().values
            aggregated_data[app_ul] = df.groupby('IMSI')[app_ul].sum().values
    
    return aggregated_data

