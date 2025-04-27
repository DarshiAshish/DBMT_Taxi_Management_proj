Ride One Application - Setup Instructions
Please follow the steps below to set up and run the Ride One Application on your local machine:

1. Clone the Repository
git clone https://github.com/DarshiAshish/DBMT_Taxi_Management_proj.git
cd project

2. Set Up the Database
Open your MySQL client(MySQL workbench).
Execute the SQL script Ash_DDL (1).sql in a single run to create the necessary database schema and tables.

3. Set Up the Python Environment
Create and activate a virtual environment
virtualenv <env_name>
Activate this environment.

4. Install the required dependencies:
pip install -r requirements.txt

5. Configure Database Connection
Open app.py.
Update the MySQL password on line 19 to match your local MySQL server credentials.

