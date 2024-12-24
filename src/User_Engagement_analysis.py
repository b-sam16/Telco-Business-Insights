import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def aggregate_engagement_metrics(df):
    """Aggregate engagement metrics per customer ID (MSISDN)."""
    # Aggregate the metrics per customer
    engagement_data = df.groupby('MSISDN/Number').agg(
        sessions_frequency=('Bearer Id', 'count'),  # Assuming 'Bearer Id' is the session identifier
        session_duration=('Dur. (ms)', 'sum'),
        total_dl=('Total DL (Bytes)', 'sum'),
        total_ul=('Total UL (Bytes)', 'sum') # Total traffic as sum of DL and UL
    ).reset_index()
    # Calculate total traffic
    engagement_data['total_traffic'] = engagement_data['total_dl'] + engagement_data['total_ul']

    # Drop the 'total_dl' and 'total_ul' columns from the final output
    engagement_data = engagement_data.drop(columns=['total_dl', 'total_ul'])

    # Return the aggregated data
    return engagement_data



def report_top_customers(df):
    """Report the top 10 customers based on various engagement metrics."""

    metrics = ['session_duration', 'session_duration', 'total_traffic']
    top_customers = {}
    
    for metric in metrics:
        top_customers[metric] = df[['MSISDN/Number', metric]].nlargest(10, metric)
        print(f"\nTop 10 customers by {metric.replace('_', ' ').title()}:")
        print(top_customers[metric])
    
    return top_customers

def cluster_engagement_metrics(engagement_data, k=3):
    """
    Normalize engagement metrics and classify customers into k groups using K-Means clustering.
    
    Parameters:
        engagement_data (pd.DataFrame): Aggregated user data.
        k (int): Number of clusters (default is 3).
    
    Returns:
        pd.DataFrame: Engagement data with added 'cluster' and 'cluster_label' columns.
    """
    # Select relevant engagement metrics
    metrics = ['sessions_frequency', 'session_duration', 'total_traffic']
    engagement_df = engagement_data[['MSISDN/Number'] + metrics].copy()
    
    # Normalize the metrics
    scaler = StandardScaler()
    engagement_df[metrics] = scaler.fit_transform(engagement_df[metrics])
    
    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=k, random_state=42)
    engagement_df['cluster'] = kmeans.fit_predict(engagement_df[metrics])
    
    # Map clusters for clarity (e.g., Low, Medium, High Engagement)
    cluster_mapping = {
        0: 'Low Engagement',
        1: 'Medium Engagement',
        2: 'High Engagement'
    }
    engagement_df['cluster_label'] = engagement_df['cluster'].map(cluster_mapping)
    
    # Merge cluster results back to the original engagement_data
    clustered_data = pd.merge(
        engagement_data,
        engagement_df[['MSISDN/Number', 'cluster', 'cluster_label']],
        on='MSISDN/Number',
        how='left'
    )
    
    return clustered_data

def cluster_metrics_summary(clustered_data):
    """
    Compute minimum, maximum, average, and total of non-normalized metrics for each cluster.
    
    Parameters:
        clustered_data (pd.DataFrame): Data with clustering results and engagement metrics.
        
    Returns:
        pd.DataFrame: Summary statistics per cluster.
    """
    # Define the metrics to analyze
    metrics = ['sessions_frequency', 'session_duration', 'total_traffic']
    
    # Group data by cluster_label and calculate summary statistics
    cluster_summary = clustered_data.groupby('cluster_label').agg(
        min_sessions_frequency=('sessions_frequency', 'min'),
        max_sessions_frequency=('sessions_frequency', 'max'),
        avg_sessions_frequency=('sessions_frequency', 'mean'),
        total_sessions_frequency=('sessions_frequency', 'sum'),
        
        min_session_duration=('session_duration', 'min'),
        max_session_duration=('session_duration', 'max'),
        avg_session_duration=('session_duration', 'mean'),
        total_session_duration=('session_duration', 'sum'),
        
        min_total_traffic=('total_traffic', 'min'),
        max_total_traffic=('total_traffic', 'max'),
        avg_total_traffic=('total_traffic', 'mean'),
        total_total_traffic=('total_traffic', 'sum')
    ).reset_index()
    
    return cluster_summary