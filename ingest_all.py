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
import vdata
import ranges

# Function to read the connection string from a configuration file
def read_connection_string(file_path):
    try:
        with open(file_path, "r") as file:
            connection_string = file.read().strip()
            return connection_string
    except FileNotFoundError:
        print(f"Configuration file '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading configuration file: {e}")
        return None

# Function to read SQL queries from a file
def read_queries_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            queries = file.read()
            # Split queries on semicolon while preserving valid statements
            return [query.strip() for query in queries.split(";") if query.strip()]
    except FileNotFoundError:
        print(f"SQL file '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading SQL file: {e}")
        return []
    
# Function to read CSV file names from a configuration file
def read_csv_file_names(file_path):
    try:
        with open(file_path, "r") as file:
            file_names = [line.strip() for line in file if line.strip()]
            return file_names
    except FileNotFoundError:
        print(f"CSV configuration file '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading CSV file names: {e}")
        return []

# Execute the CREATE TABLE queries
def create_tables(connection_string, queries):
    try:
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Execute each query
        for query in queries:
            print(f"Executing query: {query.strip()[:50]}...")
            cursor.execute(query)
        conn.commit()
        print("All tables created successfully.")
    except pyodbc.Error as e:
        print(f"Error creating tables: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

# Main execution
if __name__ == "__main__":
    config_file_path = "connection.conf" # Path to the configuration file
    sql_file_path = "create_tables.sql"  # Path to the SQL file containing the queries
    csv_files_path = "csv_files.conf"    # Path to the CSV configuration file

    # Read the connection string
    connection_string = read_connection_string(config_file_path)

    if connection_string:
        # Read the queries from the SQL file
        queries = read_queries_from_file(sql_file_path)

        if queries:
            # Execute the queries to create tables
            create_tables(connection_string, queries)
            
            # Populate the date ranges table
            ranges.populate_ranges(connection_string)
            
            # Read the CSV file names
            csv_files = read_csv_file_names(csv_files_path)
            if csv_files:
                for csv_file in csv_files:
                    if "DATA" in csv_file:
                        date_columns = ['RECVDATE', 'RPT_DATE', 'DATEDIED', 'VAX_DATE', 'ONSET_DATE', 'TODAYS_DATE']
                        boolean_columns = ['DIED', 'L_THREAT', 'ER_VISIT', 'HOSPITAL', 'X_STAY', 
                            'DISABLE', 'BIRTH_DEFECT', 'OFC_VISIT', 'ER_ED_VISIT']
                        vdata.ingest(connection_string, csv_file, "VDATA", date_columns, False, boolean_columns)
                    elif "VAX" in csv_file:
                        vdata.ingest(connection_string, csv_file, "VAX", None, None, None)
                    elif "SYMPTOMS" in csv_file:
                        vdata.ingest(connection_string, csv_file, "SYMPT", None, None, None)
            else:
                print("No valid CSV file names found.")
        else:
            print("No valid SQL queries found in the file.")
