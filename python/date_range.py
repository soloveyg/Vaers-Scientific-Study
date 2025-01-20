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
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import configReader
import JSONReader

def populate(connection_string, json_file_path):
    """
    Reads date ranges from a JSON file and populates the range table.

    Args:
        connection_string (str): SQLAlchemy connection string for the database.
        json_file_path (str): Path to the JSON file containing date ranges.

    Returns:
        None
    """
    # Connect to the database
    engine = create_engine(connection_string)

    # Read the JSON file
    date_ranges = JSONReader.read_JSON(json_file_path)

    # Populate the range table
    try:
        with engine.begin() as connection:  # Use a transaction
            # Clear the existing data
            print("Deleting existing data from the range table...")
            connection.execute(text("DELETE FROM range"))

            # Insert the new date ranges
            print("Inserting new date ranges into the range table...")
            for date_range in date_ranges:
                connection.execute(
                    text("""
                    INSERT INTO range (Date_Range, start_date, end_date)
                    VALUES (:range_name, :start_date, :end_date)
                    """),
                    {
                        "range_name": date_range["range_name"],
                        "start_date": date_range["start_date"],
                        "end_date": date_range["end_date"]
                    }
                )

            print(f"Successfully populated the range table from {json_file_path}.")
    except SQLAlchemyError as e:
        print(f"Database error while populating the range table: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Replace with your database connection string and JSON file path
    connection_string = configReader.read_connection_string()
    json_file_path = "../conf/date_ranges.json"

    # Populate the range table
    populate_ranges(connection_string, json_file_path)
