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

import json
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
import configReader
import JSONReader


def populate(connection_string, json_file_path):
    """
    Reads age group definitions from a JSON file and populates them into the age_group table.

    Args:
        connection_string (str): SQLAlchemy connection string for the database.
        json_file_path (str): Path to the JSON file containing age group definitions.

    Returns:
        None
    """
    # Define the table schema
    metadata = MetaData()
    age_group_table = Table(
        'age_group', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(10), nullable=False),
        Column('min_age', Integer, nullable=True),
        Column('max_age', Integer, nullable=True),
        Column('description', String(255), nullable=True)
    )

    # Read the JSON file
    age_groups = JSONReader.read_JSON(json_file_path)

    # Connect to the database
    engine = create_engine(connection_string)
    try:
        with engine.begin() as connection:  # Use a transaction
            # Delete existing data from the age_group table
            print("Deleting existing data from the age_group table...")
            connection.execute(age_group_table.delete())
            
            # Insert the age groups into the table
            connection.execute(age_group_table.insert(), age_groups)
            print(f"Successfully populated the age_group table from {json_file_path}.")
    except SQLAlchemyError as e:
        print(f"Error inserting data into the age_group table: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Replace with your database connection string and JSON file path
    connection_string = configReader.read_connection_string()
    json_file_path = "../conf/age_groups.json"

    # Populate the age_group table
    populate_age_group_table(connection_string, json_file_path)
