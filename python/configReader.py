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
from urllib.parse import quote_plus

def read_connection_string():
    import os
    
    file_path = "../conf/connection.conf"
    connection_properties = {}

    try:
        # Open the configuration file and parse it line by line
        with open(file_path, "r") as file:
            for line in file:
                # Strip whitespace and skip empty lines or comments
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                # Split key-value pairs
                if "=" in line:
                    key, value = line.split("=", 1)
                    connection_properties[key.strip()] = value.strip()

        # Validate required keys
        required_keys = {"odbc_driver", "server", "port", "database", "username", "password"}
        missing_keys = required_keys - connection_properties.keys()
        if missing_keys:
            print(f"Missing configuration keys: {', '.join(missing_keys)}")
            return None

        # Create the connection string
        connection_string = (
            f"mssql+pyodbc://{quote_plus(connection_properties["username"])}:{quote_plus(connection_properties["password"])}@{connection_properties["server"]}:{connection_properties["port"]}/{connection_properties["database"]}?driver={connection_properties["odbc_driver"]}"
        )

        return connection_string
    except FileNotFoundError:
        print(f"Configuration file '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading configuration file: {e}")
        return None
