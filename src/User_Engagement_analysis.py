import pandas as pd

def aggregate_engagement_metrics(df):
    """Aggregate engagement metrics per customer ID (MSISDN)."""
    # Aggregate the metrics per customer
    engagement_data = df.groupby('MSISDN').agg(
        sessions_frequency=('Bearer Id', 'count'),  # Assuming 'Bearer Id' is the session identifier
        session_duration=('Dur. (ms)', 'sum'),
        total_traffic=('Total DL (Bytes)', 'sum') + df['Total UL (Bytes)']  # Total traffic as sum of DL and UL
    ).reset_index()

    # Return the aggregated data
    return engagement_data