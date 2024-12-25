import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def plot_top_handsets(df):
    """Graphical: Bar Chart for Top 10 Handsets Used by Customers."""
    top_handsets = df['Handset Type'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    top_handsets.plot(kind='bar', color='skyblue')
    plt.title("Top 10 Handsets Used by Customers")
    plt.xlabel("Handset")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.show()

def plot_top_manufacturers(df):
    """Graphical: Pie Chart for Top 3 Handset Manufacturers."""
    top_manufacturers = df['Handset Manufacturer'].value_counts().head(3)
    top_manufacturers.plot(kind='pie', autopct='%1.1f%%', startangle=90, figsize=(8, 8))
    plt.title("Top 3 Handset Manufacturers")
    plt.ylabel("")
    plt.show()


def plot_top_handsets_per_manufacturer(df):
    """Graphical: Grouped Bar Chart for Top 5 Handsets per Top 3 Manufacturer"""
    # Identify the top 3 manufacturers
    top_manufacturers = df['Handset Manufacturer'].value_counts().head(3).index
    
    # Filter the DataFrame for the top manufacturers
    filtered_df = df[df['Handset Manufacturer'].isin(top_manufacturers)]
    
    # Group by Manufacturer and Handset to get the top handsets per manufacturer
    top_handsets_df = (
        filtered_df.groupby(['Handset Manufacturer', 'Handset Type'])['Bearer Id']
        .count()
        .groupby(level=0, group_keys=False)
        .nlargest(5)
        .reset_index(name='Frequency')
    )
    
    # Pivot for stacked bar chart
    pivot_df = top_handsets_df.pivot_table(
        index='Handset Manufacturer',
        columns='Handset Type',
        values='Frequency',
        fill_value=0
    )
    
    # Plot the stacked bar chart
    ax = pivot_df.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    plt.title('Top 5 Handsets per Top 3 Manufacturer')
    plt.xlabel('Handset Manufacturer')
    plt.ylabel('Number of Sessions')
    plt.xticks(rotation=45)
    
    # Adjust legend to display only the top 5 handsets per manufacturer
    handles, labels = ax.get_legend_handles_labels()
    top_5_labels = pivot_df.columns
    top_5_handles = [handles[labels.index(label)] for label in top_5_labels]
    ax.legend(top_5_handles, top_5_labels, title='Handset Type', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', title_fontsize='small')
    
    plt.show()

def plot_univariate_analysis(df):
    """Graphical Univariate Analysis for each variable in the DataFrame."""
    # Plot Histograms for Continuous Variables (float64) without KDE for speed
    for var in df.columns:
        plt.figure(figsize=(6, 4))  # Create a new figure for each variable
        sns.histplot(df[var], kde=True)  
        plt.title(f'Histogram for {var}', fontsize=12,)
        plt.xlabel(var, fontsize=10)
        plt.ylabel('Frequency',fontsize=10)
    
        plt.show()



def plot_bivariate_analysis(df):
    """Graphical: Scatter Plot for Bivariate Application vs Total Data (DL + UL)"""
    
    # List of applications to analyze
    applications = ['Social Media', 'Google', 'Email', 'Youtube', 'Netflix', 'Gaming', 'Other']
    
    # Create scatter plots for each combined application data
    for app in applications:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x=df[f'{app} Total'], 
            y=df['total_data'], 
            hue=df[f'{app} Total'], 
            palette='viridis'
        )
        plt.title(f'Bivariate: {app} Total vs Total Data Volume')
        plt.xlabel(f'{app} Total (Bytes)')
        plt.ylabel('Total Data Volume (Bytes)')
        plt.legend(title=f'{app} Total', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()
        

# Correlation Analysis
def plot_correlation_matrix(df):
    """Graphical: Heatmap for Correlation Analysis."""
    # List of applications
    correlation_columns = ['Social Media Total', 'Google Total', 'Email Total', 'Youtube Total', 'Netflix Total', 'Gaming Total', 'Other Total']
    
    # Calculate the correlation matrix
    correlation_matrix = df[correlation_columns].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.show()



def perform_pca(df):
    """Perform PCA on the dataset and plot the explained variance ratio."""
    # Select numeric columns for PCA
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    # Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[numeric_cols])
    
    # Apply PCA
    pca = PCA()
    pca.fit(scaled_data)
    
    # Explained variance ratio
    explained_variance_ratio = pca.explained_variance_ratio_
    
    # Plot the explained variance ratio
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, marker='o', linestyle='--')
    plt.title('PCA Scree Plot')
    plt.xlabel('Principal Component')
    plt.ylabel('Variance Explained')
    plt.show()
    
    return pca, explained_variance_ratio


def visualize_cluster_metrics(cluster_summary):
    #Visualize cluster-level engagement metrics.
   
    metrics = ['sessions_frequency', 'session_duration', 'total_traffic']
    
    for metric in metrics:
        plt.figure(figsize=(12, 6))
        sns.barplot(
            data=cluster_summary,
            x='engagement_cluster',
            y=f'avg_{metric}'
        )
        plt.title(f'Average {metric.replace("_", " ").title()} per Cluster')
        plt.xlabel('Engagement Cluster')
        plt.ylabel(f'Average {metric.replace("_", " ").title()}')
        plt.show()