"""This is the utils module that contains utiliy functions
"""

def csv_to_df(csv_file):
    """Converts a CSV file to a PDF file.

    Args:
        csv_file (str): The path to the CSV file.

    Returns:
        str: The path to the generated PDF file.
    """
    import pandas as pd
    
    return pd.read_csv(csv_file)