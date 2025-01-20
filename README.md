## VAERS Research

### Motivations
The motivation to create the VEARS scientific study stemmed from my aspiration to explore the field of data science as a new graduate while contributing to meaningful research during a time of global importance. The COVID-19 pandemic provided an abundance of data, presenting a unique opportunity to analyze trends and uncover insights through the creation of detailed graphs and visualizations. This project allowed me to delve into data manipulation, visualization, and analysis using SQL and Python, enabling me to merge my curiosity for data science with a chance to understand patterns and trends in pandemic-related information better.

### Technologies
I used the following technologies:
- MS SQL as the database
- Python for data manipulation and plotting the analyses
    todo: List the required libraries that do not come out of the box

### Data source
As the source of information, I used the VAERS database maintained by the CDC.

### How to reproduce the analysis
If you want to reproduce the analysis you should follow the steps below.

#### Step 1

Install Python. I used version 3.12.8
https://www.python.org/downloads/

#### Step 2

Install MS SQL Server. Select the Developer version when downloading.
https://www.microsoft.com/en-us/sql-server/sql-server-downloads

#### Step 3

Download the VEARS Data from the link below:
https://vaers.hhs.gov/data.html
This is up to the user on how much data they wish to process but I found it most effective to start from 2000 to 2024. I recommend this because the plots show interesting data on the pandemic that happened in 2020.

#### Step 4
Download all the files in the GitHub repo.
Replace the placeholder in "Connection.conf" with applicable information.

#### Step 5
Import the VAERS data into the MS SQL database by running the following command in a terminal window. Change to the Python folder: 
**cd python**
and the run:
**python ingest_all.py**

This may take about an hour for the years 2000 to 2024 depending on your computer's specs.

#### Step 6
After your data has been imported, run the following command in the Python folder:
**python plot_all.py** 
This will plot all visualizations. You can modify the command to create certain plots as needed. 

For example:
**python plot_all.py "Deaths Counts by Vaccine Name and Date Range.sql"**


#### Step 6
Once the HTML has been processed, open the file explorer in the html sub-directory to view the interactive graphs.

### Available  reports:

<a href="nm">Deaths Counts by Vaccine Name and Date Range</a>

<a href="https://html-preview.github.io/?url=https://github.com/soloveyg/Vaers-Scientific-Study/blob/main/html/Deaths%20by%20age%20group%20and%20vaccine.html">Deaths by age group and vaccine</a>


<a href="https://html-preview.github.io/?url=https://github.com/soloveyg/Vaers-Scientific-Study/blob/main/html/Deaths%20by%20gender%20and%20vaccine.html">Deaths by gender and vaccine</a>


<a href="https://html-preview.github.io/?url=https://github.com/soloveyg/Vaers-Scientific-Study/blob/main/html/Deaths%20by%20state%20and%20vaccine.html">Deaths by state and vaccine</a>


<a href="https://html-preview.github.io/?url=https://github.com/soloveyg/Vaers-Scientific-Study/blob/main/html/Number%20of%20Adverse%20Events%20by%20Year.html">Number of Adverse Events by Year</a>

<a href="https://html-preview.github.io/?url=https://github.com/soloveyg/Vaers-Scientific-Study/blob/main/html/Female%20Symptoms%20for%20Age%20Group%20and%20COVID%20vaccines.html">Female Symptoms for Age Group and COVID vaccines</a>

<a href="https://html-preview.github.io/?url=https://github.com/soloveyg/Vaers-Scientific-Study/blob/main/html/Male%20Symptoms%20for%20Age%20Group%20and%20COVID%20vaccines.html">Male Symptoms for Age Group and COVID vaccines</a>

<a href="https://html-preview.github.io/?url=https://github.com/soloveyg/Vaers-Scientific-Study/blob/main/html/Time%20to%20Adverse%20Event%20Onset%20After%20Vaccination.html">Time to Adverse Event Onset After Vaccination</a>

<a href="https://html-preview.github.io/?url=https://github.com/soloveyg/Vaers-Scientific-Study/blob/main/html/Number%20of%20Adverse%20Events%20by%20Year.html">Number of Adverse Events by Year</a>

