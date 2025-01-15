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
import pyodbc

def ingest(connection_string, file_path, table_name, date_columns, dayfirst, boolean_columns):
    # Step 1: Load the CSV File

    # Read the CSV file, parsing the date columns if applicable
    if date_columns:
        df = pd.read_csv(file_path, encoding='latin1', parse_dates=date_columns, dayfirst=dayfirst)
    else:
        df = pd.read_csv(file_path, encoding='latin1')

    # Step 2: Handle Boolean Conversion for 'Y'/'N'
    if boolean_columns:
        for col in boolean_columns:
            if col in df.columns:
                df[col] = df[col].map({'Y': 1, 'N': 0}).fillna(0).astype(int)  # Convert Y/N to 1/0
    
    # Step 3: Connect to SQL Server
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    wasError = False

    # Generate SQL INSERT statements dynamically
    for idx, row in df.iterrows():
        try:
            columns = ', '.join(f"[{col}]" for col in df.columns)
            placeholders = ', '.join(['?'] * len(df.columns))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            # Convert row to a tuple of values for the SQL statement
            values = tuple(row[col] if not pd.isna(row[col]) else None for col in df.columns)
            
            # Execute the SQL command
            cursor.execute(sql, values)
        except Exception as e:
            wasError = True
            print(f"Error inserting row {idx}: {row}")
            print(e)
            break

    # Commit the transaction and close the connection
    if not wasError:
        conn.commit()
    cursor.close()
    conn.close()

    if not wasError:
        print(f"Data from {file_path} successfully inserted into {table_name}!")
