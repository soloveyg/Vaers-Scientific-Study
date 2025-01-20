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

import sys
import os
import json
## import pyodbc
from sqlalchemy import create_engine
import pandas as pd
import plotly.express as px
import configReader
import JSONReader
import numpy as np

# VAERS sources are available here: https://vaers.hhs.gov/data/datasets.html
# Total vaccination counts are available here: https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-Jurisdi/unsk-b7fc/about_data
#     -  Use the export button in the right upper corner

connection_string = configReader.read_connection_string()

print(connection_string)

def visualize_data(connection_string, config):
    """
    Execute a parameterized SQL query and visualize the result using Plotly.
    
    Args:
        connection_string (str): The database connection string.
        query (str): The SQL query to execute.
        x_axis (str): The column to use as the x-axis.
        y_axis (str): The column to use as the y-axis.
        title (str): The title of the plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        plot_type (str): Type of plot ("bar" or "line").
        log_scale (bool): Whether to use a logarithmic scale for the y-axis.
    """
    # Connect to the database
    engine = create_engine(connection_string)
    query=config.get("query")
    df = pd.read_sql(query, con=engine)

    x_axis=config["x_axis"]
    y_axis=config["y_axis"]
    # Check if the required columns are present
    if x_axis not in df.columns or y_axis not in df.columns:
        raise ValueError(f"Columns '{x_axis}' or '{y_axis}' not found in the query result.")
     
    title=config["title"]
    plot_type=config["plot_type"]
    log_scale=config["log_scale"]
    
    color=config["color"]

    # Create the plot
    if plot_type == "bar":
        hover_data=config["hover_data"]
        xlabel=config["xlabel"]
        ylabel=config["ylabel"]
        fig = px.bar(
            df, 
            x=x_axis, 
            y=y_axis, 
            text=y_axis,
            hover_data=hover_data,
            labels={x_axis: xlabel, y_axis: ylabel},
            title=title,
            color=x_axis if color == None else color
        )
        fig.update_traces(#texttemplate='%{text:.2s}', 
                          textposition='outside')
        # Customize layout
        fig.update_layout(
            xaxis_title=xlabel,
            yaxis_title=ylabel,
            xaxis=dict(tickangle=45),
            template="plotly",
            showlegend=False
        )
        # Adjust for logarithmic scale if needed
        if log_scale:
            fig.update_yaxes(type="log")

    elif plot_type == "scatter":
        xJittered = x_axis + ' Jittered'
        xNumeric = x_axis + ' Numeric'
        df[xNumeric] = pd.factorize(df[x_axis])[0]
        df[xJittered] = df[xNumeric] + np.random.uniform(-0.1, 0.1, len(df))

        yJittered = y_axis + ' Jittered'
        yNumeric = y_axis + ' Numeric'
        df[yNumeric] = pd.factorize(df[y_axis])[0]
        df[yJittered] = df[yNumeric] + np.random.uniform(-0.1, 0.1, len(df))
        fig = px.scatter(
            df,
            x=xJittered,
            y=yJittered,
            size=config["size"],
            color=color,
            hover_name=config["hover_name"], ## symptom
            hover_data=config["hover_data"],
            title=title,
            labels=config["labels"],
            size_max=100,  # Adjust this value to control the maximum bubble size
            color_discrete_sequence=px.colors.qualitative.Bold  # Use a distinct color palette
        )

        # Update layout for better visualization
        fig.update_layout(
            xaxis_title=config["xaxis_title"],
            yaxis_title=config["yaxis_title"],
            legend_title=config["legend_title"],
            template=config["template"]
        )
        fig.update_xaxes(ticktext=df[x_axis].unique(), tickvals=df[xNumeric].unique())
        fig.update_yaxes(ticktext=df[y_axis].unique(), tickvals=df[yNumeric].unique())

    else:
        raise ValueError("Unsupported plot_type. Use 'bar' or 'scatter'.")
        
    # Show the plot
    #fig.show()
    
    return fig



# Assign the connection string outside the script

# Process an analysis
def process_analysis(config):
    print(f"Plotting {config["title"]}")
    fig = visualize_data(
        connection_string=connection_string,
        config=config)

    print("Current working directory:", os.getcwd())
    
    filepath = os.path.join('..', 'html', f'{config["title"]}.html')
    print(f"Writing {filepath}")
    fig.write_html(filepath)

def read_query_file(file_path):
    try:
        with open(file_path, "r") as file:
            query_lines = [line.strip() for line in file if line.strip()]
            return "\n".join(query_lines) + "\n"
    except FileNotFoundError:
        print(f"Query file '{file_path}' not found.")
        return ""
    except Exception as e:
        print(f"Error reading query file {file_path}: {e}")
        return ""
    
def main(config_file, args):
    print(f"args: {args}")
    # Load the JSON configuration
    config = JSONReader.read_JSON(config_file)

    for plot_config in config:
        ok_to_process = True
        if len(args) > 1 and not plot_config["query"] in args:
            print(f"Skipping {plot_config["query"]}")
            ok_to_process = False
        if ok_to_process:
            # Get the actual SQL query from the file
            query = read_query_file("../sql/" + plot_config["query"])
            plot_config["query"] = query
            process_analysis(plot_config)

if __name__ == "__main__":
    # Replace 'config.json' with the path to your configuration file
    # Replace the connection string with your actual database connection string
    main("../conf/queries.json", sys.argv)
