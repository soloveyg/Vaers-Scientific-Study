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
import json
import pyodbc
import pandas as pd
import plotly.express as px
import configReader

# VAERS sources are available here: https://vaers.hhs.gov/data/datasets.html

def visualize_data(connection_string, query, x_axis, y_axis, title, xlabel, ylabel,  
                   plot_type="bar", log_scale=False, hover_data={}, color=None):
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
    conn = pyodbc.connect(connection_string)
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Check if the required columns are present
    if x_axis not in df.columns or y_axis not in df.columns:
        raise ValueError(f"Columns '{x_axis}' or '{y_axis}' not found in the query result.")
    
    # Create the plot
    if plot_type == "bar":
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
    elif plot_type == "line":
        fig = px.line(
            df, 
            x=x_axis, 
            y=y_axis, 
            markers=True, 
            labels={x_axis: xlabel, y_axis: ylabel},
            title=title
        )
        # For line plots, we don't use `textposition='outside'`
        fig.update_traces(mode='lines+markers+text', 
                          text=df[y_axis], textposition='top center')
    else:
        raise ValueError("Unsupported plot_type. Use 'bar' or 'line'.")
    
    # Adjust for logarithmic scale if needed
    if log_scale:
        fig.update_yaxes(type="log")
    
    # Customize layout
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        xaxis=dict(tickangle=45),
        template="plotly",
        showlegend=False
    )
    
    # Show the plot
    #fig.show()
    
    return fig



# Assign the connection string outside the script

# Process an analysis
def process_analysis(config, connection_string): 
    fig = visualize_data(
        connection_string=connection_string,
        query=config.get("query"),
        x_axis=config["x_axis"],
        y_axis=config["y_axis"],
        title=config["title"],
        xlabel=config["xlabel"],
        ylabel=config["ylabel"],
        plot_type=config["plot_type"],
        log_scale=config["log_scale"],  # Enable logarithmic scale to handle large differences
        hover_data=config["hover_data"],
        color=config["color"],
    )
    fig.write_html(f"{config["title"]}.html")

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
    # Load the connection string
    connection_string = configReader.read_connection_string("connection.conf")
    # Load the JSON configuration
    with open(config_file, 'r') as file:
        config = json.load(file)

        for plot_config in config:
            ok_to_process = True
            if len(args) > 1 and not plot_config["query"] in args:
                print(f"Skipping {plot_config["title"]}")
                ok_to_process = False
            if ok_to_process:
                print(f"Plotting {plot_config["title"]}")
                # Get the actual SQL query from the file
                query = read_query_file(plot_config["query"])
                plot_config["query"] = query
                process_analysis(plot_config, connection_string)

if __name__ == "__main__":
    # Replace 'config.json' with the path to your configuration file
    # Replace the connection string with your actual database connection string
    main("queries.json", sys.argv)
