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

import pyodbc

def populate_ranges(connection_string):
    # Define the date ranges
    date_ranges = [
        ('Dec 2020', '2020-12-01', '2020-12-31'),
        ('Jan 2021', '2020-12-31', '2021-01-31'),
        ('Feb 2021', '2021-01-31', '2021-02-28'),
        ('Mar 2021', '2021-02-28', '2021-03-31'),
        ('Apr 2021', '2021-03-31', '2021-04-30'),
        ('May 2021', '2021-04-30', '2021-05-31'),
        ('Jun 2021', '2021-05-31', '2021-06-30'),
        ('Jul 2021', '2021-06-30', '2021-07-31'),
        ('Aug 2021', '2021-07-31', '2021-08-31'),
        ('Sep 2021', '2021-08-31', '2021-09-30'),
        ('Oct 2021', '2021-09-30', '2021-10-31'),
        ('Nov 2021', '2021-10-31', '2021-11-30'),
        ('Dec 2021', '2021-11-30', '2021-12-31'),
        ('Jan 2022', '2021-12-31', '2022-01-31'),
        ('Feb 2022', '2022-01-31', '2022-02-28'),
        ('Mar 2022', '2022-02-28', '2022-03-31'),
        ('Apr 2022', '2022-03-31', '2022-04-30'),
        ('May 2022', '2022-04-30', '2022-05-31'),
        ('Jun 2022', '2022-05-31', '2022-06-30'),
        ('Jul 2022', '2022-06-30', '2022-07-31'),
        ('Aug 2022', '2022-07-31', '2022-08-31'),
        ('Sep 2022', '2022-08-31', '2022-09-30'),
        ('Oct 2022', '2022-09-30', '2022-10-31'),
        ('Nov 2022', '2022-10-31', '2022-11-30'),
        ('Dec 2022', '2022-11-30', '2022-12-31'),
        ('Jan 2023', '2022-12-31', '2023-01-31'),
        ('Feb 2023', '2023-01-31', '2023-02-28'),
        # ('Mar 2023', '2023-02-28', '2023-03-31'),
        # ('Apr 2023', '2023-03-31', '2023-04-30'),
        # ('May 2023', '2023-04-30', '2023-05-31')
    ]


    # Connect to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Initialize the rangecnt table
    cursor.execute("DELETE FROM range;")

    # Process each date range
    for range_name, start_date, end_date in date_ranges:

        # Insert results into the rangecnt table
        cursor.execute("""
        INSERT INTO range (Date_Range, start_date, end_date)
        VALUES (?, ?, ?)
        """, range_name, start_date, end_date)

    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

    print("range table has been populated.")
