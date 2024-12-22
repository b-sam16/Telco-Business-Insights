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