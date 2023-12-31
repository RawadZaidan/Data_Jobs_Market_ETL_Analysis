
<img  src="./readme/title1.svg"/>

<div>

> Hello world! This is the project’s summary that describes the project, plain and simple, limited to the space available.
**[PROJECT PHILOSOPHY](#project-philosophy) • [PROTOTYPING](#prototyping) • [TECH STACKS](#stacks) • [IMPLEMENTATION](#implementation) • [HOW TO RUN?](#run)**

</div> 
  

<br><br>

<!-- project philosophy -->

<a  name="philosophy" ></a>
<img  src="./readme/title2.svg" id="project-philosophy"/>

> A Python based ETL project that would extract, transform data from different web sources and load them into a tabular database (PostgreSQL) in an attempt to provide a full scope analytical understanding of the Data Job market. 

>The project also provides day-to-day jobs from Linkedin-Glassdoor-NaukriGulf with all the skills requried, their description and application link based on user filters (Python, SQL, AWS, Azure, Junior, Mid, Senior levels, etc...)
<br>

  

### User Types

 

1. Data Engineers.
2. Data Analysts.
3. HR people.
4. People interested in going into the data world.
  

<br>

### User Stories

  
1. **As a Data Engineer:**
   - I want to automatically scrape various data jobs from reputable sources so that our dataset is always up-to-date.
   - I want to integrate different data sources seamlessly.
   - Ensure fault tolerance in our data pipelines, so that potential failures don't interrupt our analyses.
   - Get a `log.txt` file that will showcase each step.

2. **As an Analyst:**
   - I want to query the database.
   - I want to view the jobs analysis based on skill factors to understand the data job market better.
   - I want to visualize the data using PowerBI.

3. **As an HR:**
   - I want to access a dataset that provides a holistic view of the data job market and know what to expect/describe in a vacancy post.
   - I want to compare different titles and their requirements/skills/compensation.

4. **As a Person interested in the data world:**
   - I want to understand what to learn, what's in demand, different functions and job titles.



<br><br>

<!-- Prototyping -->
<img  src="./readme/title3.svg"  id="prototyping"/>

> We have designed our projects to webscrape, through an ETL project and including it in a PowerBI Sample Dashboard 



### Data Tables Schema

<img  src="./readme/DB_Tables.png"  id="prototyping"/>

### Data Flow Diagram

<img  src="./readme/pipeline.png"  id="prototyping"/>



<br><br>

> ETL performance - Logger view

  
### Time for each run

 ![Landing](./readme/logger1.png) | ![fsdaf](./readme/logger2.png) |

On average, every ETL run takes around 20-30 minutes (also depends on internet speed)

<!-- Tech stacks -->

<a  name="implementation"></a>
<img  src="./readme/title4.svg" id="implementation" />

<br>

<br>

Power BI Report Preview



https://github.com/RawadZaidan/Data_Jobs_Market_ETL_Analysis/assets/119298940/b8b0ee8f-4215-4945-bdbe-73d3fdcdf35e



![Map](readme/pb1.png)| ![Map](readme/pb2.png)| ![Map](readme/pb3.png)| ![Map](readme/pb4.png)| ![Map](readme/pb5.png)| ![Map](readme/pb6.png) ![VID](readme/lapse.gif)


<br>

<br>

  

<!-- stacks -->

<a  name="stacks"  ></a>
<img  src="./readme/title5.svg" id="#stack"/>

## Frontend

Interactive PowerBI Dashboard:
A central dashboard where viewers can view:

1. Job Indicators: Graphs, charts and visualizations displaying key job requirements/quality metrics over time and titles.
2. Interactive filters: Options to filter data by date, skills, or specific filters for customized job searches.
3. Ease of navigation: This report allows for a seamless navigation between different sections.

## Backend

1. Web scraping & Automation using Selenium, Beautiful Soup and Requests libraries
2. ETL Pipeline: Using Python and Pandas, raw data is extracted, transformed into a usable format and loaded into postgreSQL database.
3. Database: Schema Design - Indexing - Data Integrity - Backup & Recovery.


 - Python
 - SQL
 - DAX
 - PowerQuery

<!-- How to run -->

<a  name="run"  ></a>
<img  src="./readme/title6.svg" id="run"/>
  

> To set up **Data Jobs Market Analysis** follow these steps:

### Prerequisites


**Hardware & Software**:

-   A computer/server with sufficient RAM and processing power.
-   Operating system: Linux (preferred for production) or Windows.
-   Required software: Python (3.10), PostgreSQL, Git (for version control) and Vscode.
  
  

**Dependencies**:

-   Install the necessary Python libraries: `pandas`, `selenium`, `BeautifulSoup`, etc... (can be found in the `requirements.txt file`)
-   Install database connectors/drivers for PostgreSQL: `psycopg2`.
  

### **Setting Up the Environment**:

**Clone the Repository**:


```sh

git clone https://github.com/RawadZaidan/Data_Jobs_Market_ETL_Analysis.git

```

**Set Up the Database**:

-   Start the PostgreSQL server.
-   Create a new database and user with the appropriate permissions and add your credentials.

### **Running the Backend**:

**Start the Data Ingestion & ETL Process**:
`python main_handler.py`


[Link to PowerBI dashboard](https://app.powerbi.com/view?r=eyJrIjoiZjQ2NmIwZTgtMjhiMy00NmNhLThkMGYtOTkzMjM1ZjEwZTQ5IiwidCI6IjJhZDk2OTM0LTQzZTUtNDFjMi05NzYxLWYzMzVmZTIxNGNjMyIsImMiOjl9)
