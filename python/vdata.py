"""
MIT License

Copyright (c) 2025 Gloria Solovey github[soloveyg]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def clean_data(df):
    """
    Cleans the DataFrame by replacing problematic values with None or valid formats.
    """
    # Replace NaN with None for all columns
    df = df.where(pd.notnull(df), None)

    # Ensure numeric fields do not contain NaN or empty strings
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_columns:
        df[col] = df[col].replace({pd.NA: None, float('nan'): None})

    return df

def ingest(connection_string, file_path, table_name, date_columns=None, dayfirst=False, boolean_columns=None):
    """
    Ingests data from a CSV file into a SQL table using SQLAlchemy.
    Rolls back the entire transaction in case of any error.
    """
    print(f"date_columns: {date_columns}")
    
    # Step 1: Load the CSV File
    if date_columns:
        df = pd.read_csv(file_path, encoding='latin1', parse_dates=date_columns, dayfirst=dayfirst)
        # Replace NaT in date_columns with None
        df.replace({pd.NaT: None}, inplace=True)
        #print(f"df[0]: {df.iloc[0]}")
    else:
        df = pd.read_csv(file_path, encoding='latin1')

    # Step 2: Replace Empty Strings and NaN
    df = clean_data(df)
    
    # print(f"df.isnull().sum(): {df.isnull().sum()}")  # Check for nulls in all columns
    # print(f"df['CAGE_MO'].head(10): {df['CAGE_MO'].head(10)}")  # Specifically check the CAGE_MO column

    # for col in df.select_dtypes(include=['datetime64[ns]']).columns:
    #     print(f"{col} - Min: {df[col].min()}, Max: {df[col].max()}")

    # Step 3: Handle Boolean Conversion for 'Y'/'N'
    if boolean_columns:
        for col in boolean_columns:
            if col in df.columns:
                df[col] = df[col].map({'Y': 1, 'N': 0}).fillna(0).astype(int)


    # Step 4: Connect to SQL Server and Insert Data
    engine = create_engine(connection_string)

    try:
        # Convert DataFrame to a list of tuples
        data = df.to_dict(orient='records')
        
        #print(f"data[0]: {data[0]}")

        # Define the column names as a string for the SQL insert
        columns = ', '.join(df.columns)
        placeholders = ', '.join([f":{col}" for col in df.columns])

        # SQL template for insertion
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        batch_size = 100  # Adjust batch size as needed for performance
        with engine.begin() as connection:
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                connection.execute(text(sql), batch)
                
        print(f"Data from {file_path} successfully inserted into {table_name}!")
    except SQLAlchemyError as e:
        print(f"Database error while inserting data: {e}")
        # Transaction will automatically roll back due to `engine.begin()`
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
