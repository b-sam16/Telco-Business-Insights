import pandas as pd

def format_table(df):
    """Format a DataFrame for better presentation in a table."""
    formatted_df = df.copy()
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        formatted_df[col] = formatted_df[col].apply(lambda x: f'{x:,.2f}')
    
    # Apply left alignment to all columns
    styled_df = formatted_df.style.set_properties(**{'text-align': 'left'})
    
    return styled_df
