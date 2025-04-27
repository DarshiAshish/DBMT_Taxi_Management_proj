#  Ride One Application - Setup Instructions

Please follow the steps below to set up and run the Ride One Application on your local machine:

## 1. Clone the Repository
```bash
git clone https://github.com/DarshiAshish/DBMT_Taxi_Management_proj.git
cd DBMT_Taxi_Management_proj
```

## 2. Set Up the Database
- Open your MySQL client (MySQL Workbench).
- Execute the SQL script `Ash_DDL (1).sql` in a single run to create the necessary database schema and tables.

## 3. Set Up the Python Environment
- Create a virtual environment:
```bash
virtualenv <env_name>
```
- Activate the virtual environment:
  - On Windows:
    ```bash
    .\<env_name>\Scripts\activate
    ```
  - On Linux/Mac:
    ```bash
    source <env_name>/bin/activate
    ```
- Install the required dependencies:
```bash
pip install -r requirements.txt
```

## 4. Configure Database Connection
- Open the file `app.py`.
- Update the MySQL password on line 19 to match your local MySQL server credentials.

## 5. Run the Application
- Start the application by running:
```bash
python app.py
```
- The application will be accessible at:
```
http://127.0.0.1:5000

