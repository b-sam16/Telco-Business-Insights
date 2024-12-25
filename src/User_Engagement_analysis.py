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


def normalize_engagement_metrics(engagement_data):
  
    #Normalize engagement metrics for clustering analysis.
    
    # Copy the original data to avoid modifying it directly
    normalized_data = engagement_data.copy()
    
    # Define the metrics to normalize
    metrics = ['sessions_frequency', 'session_duration', 'total_traffic']
    
    # Initialize the StandardScaler
    scaler = StandardScaler()
    
    # Apply normalization to the metrics
    normalized_data[metrics] = scaler.fit_transform(normalized_data[metrics])
    
    return normalized_data


def kmeans_clustering_engagement(normalized_data, k=3):
    #Perform K-Means clustering on normalized engagement metrics.
    # Copy the data to avoid modifying the original DataFrame
    clustered_data = normalized_data.copy()
    
    # Select the engagement metrics for clustering
    metrics = ['sessions_frequency', 'session_duration', 'total_traffic']
    
    # Initialize and fit the K-Means model
    kmeans = KMeans(n_clusters=k, random_state=42)
    clustered_data['engagement_cluster'] = kmeans.fit_predict(clustered_data[metrics])
    
    return clustered_data, kmeans

def compute_cluster_metrics(clustered_data, original_data):
    """
    Compute minimum, maximum, average, and total metrics for each cluster.
    
    Parameters:
        clustered_data (pd.DataFrame): Data with cluster labels.
        original_data (pd.DataFrame): Original (non-normalized) engagement data.
    
    Returns:
        pd.DataFrame: Cluster-level summary statistics.
    """
    # Merge cluster labels with original non-normalized data
    clustered_original_data = pd.concat(
        [original_data, clustered_data['engagement_cluster']], axis=1
    )
    
    # Calculate metrics per cluster
    cluster_summary = clustered_original_data.groupby('engagement_cluster').agg(
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

import pandas as pd

def top_users_per_application(df):
   
    # Aggregate user total traffic per application and derive the top 10 most engaged users per application.
    # List of applications to analyze
    applications = ['Social Media', 'Google', 'Email', 'Youtube', 'Netflix', 'Gaming', 'Other']
    
    top_users = {}
    
    for app in applications:
        # Calculate total traffic per user for each application
        df[f'{app}_Total'] = df[f'{app} DL (Bytes)'] + df[f'{app} UL (Bytes)']
        
        # Aggregate traffic per user for the current application
        app_traffic = df.groupby('MSISDN/Number')[[f'{app}_Total']].sum().reset_index()
        
        # Sort and select the top 10 users based on total traffic for the application
        top_users[app] = app_traffic.sort_values(by=f'{app}_Total', ascending=False).head(10)
    
    return top_users
