import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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
    
    # List of continuous variables
    continuous_vars = ['Dur. (ms)', 'Total DL (Bytes)', 'Total UL (Bytes)', 'Avg RTT DL (ms)', 'Avg RTT UL (ms)', 
                       'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)', 'TCP DL Retrans. Vol (Bytes)', 
                       'TCP UL Retrans. Vol (Bytes)']
    
    # List of categorical variables
    categorical_vars = ['Handset Manufacturer', 'Handset Type', 'Last Location Name']
    
    # Plotting histograms for continuous variables
    plt.figure(figsize=(15, 10))
    for i, var in enumerate(continuous_vars, 1):
        plt.subplot(3, 3, i)
        sns.histplot(df[var], kde=True)
        plt.title(f'Histogram for {var}')
        plt.xlabel(var)
        plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()
    
    # Plotting box plots for continuous variables
    plt.figure(figsize=(15, 10))
    for i, var in enumerate(continuous_vars, 1):
        plt.subplot(3, 3, i)
        sns.boxplot(y=df[var], orient='v')
        plt.title(f'Box Plot for {var}')
        plt.xlabel(var)
    plt.tight_layout()
    plt.show()
    

    # Plotting bar plots for categorical variables
    fig, axes = plt.subplots(len(categorical_vars), 1, figsize=(15, 10), sharex=False)
    for i, var in enumerate(categorical_vars):
        sns.countplot(y=df[var], order=df[var].value_counts().index, palette='viridis', hue=df[var],ax=axes[i])
        axes[i].set_title(f'Bar Plot for {var}')
        axes[i].set_xlabel('Frequency')
        axes[i].set_ylabel(var)
        axes[i].margins(y=0.1)  # Add space between bars
    plt.tight_layout()
    plt.show()

def plot_bivariate_analysis(df):
    """Graphical: Scatter Plot for Bivariate Application vs Total Data (DL + UL)"""
    # Calculate total data volume
    df['total_data_volume'] = df['Total DL (Bytes)'] + df['Total UL (Bytes)']
    
    # List of applications to analyze
    applications = ['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)',
                    'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']
    
    # Create scatter plots for each application
    for app in applications:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=df[app], y=df['total_data_volume'], hue=df[app], palette='viridis')
        plt.title(f'Bivariate: {app} vs Total Data Volume')
        plt.xlabel(f'{app}')
        plt.ylabel('Total Data Volume (Bytes)')
        plt.legend(title=app, bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.show()
        

# Correlation Analysis
def plot_correlation_matrix(df):
    """Graphical: Heatmap for Correlation Analysis."""
    # Calculate the correlation matrix for the specified columns
    correlation_matrix = df[['Social Media DL (Bytes)', 'Google DL (Bytes)', 'Email DL (Bytes)',
                             'Youtube DL (Bytes)', 'Netflix DL (Bytes)', 'Gaming DL (Bytes)', 'Other DL (Bytes)']].corr()
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

