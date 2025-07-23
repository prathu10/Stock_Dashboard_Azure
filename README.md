# Stock Market Dashboard with Real-Time Data
This project is an end-to-end data analytics pipeline that collects real-time and historical stock market data using Yahoo Finance API, stores it in a secure Azure SQL database, and visualizes key market insights through an interactive Power BI dashboard.

 ##  Project Overview
This real-world project enables automated stock data retrieval and visualization using the following technologies:

- **Yahoo Finance API** – for fetching intraday, daily, weekly, monthly, splits and dividend stock market data
- **Azure SQL Database** – for storing and managing time-series stock data in the cloud
- **Power BI** – for building live dashboards and business intelligence reports connected to Azure SQL

 ##  Features
-  Real-time stock price collection (e.g., Open, High, Low, Close, Volume)
-  Supports intraday, daily, weekly and monthly intervals
-  Cloud-based storage using Azure SQL for centralized access and scalability
-  Seamless Power BI integration for dynamic and interactive visualizations
-  Scheduled or on-demand data refresh support
-  **Custom DAX measures** created to calculate 52-week high/low, daily changes, average returns, and other KPIs

  ##  Tech Stack

| Component       | Technology                                                      |
|-----------------|-----------------------------------------------------------------|
| Data Source     | [Yahoo Finance API](https://pypi.org/project/yfinance/)         |
| Backend         | Python, Pandas                                                  |
| Database        | Microsoft Azure SQL Database                                    |
| Dashboard       | Microsoft Power BI                                              |
| Deployment      | Azure Cloud Services                                            |
| Security        | `.env` file for storing credentials (excluded via `.gitignore`) |


 ##  Setup Instructions
 1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
```
2. **Create and configure a .env file**
- SQL_SERVER=your_server_name
- SQL_DATABASE=your_database_name
- SQL_USERNAME=your_username
- SQL_PASSWORD=your_password

3. **Install dependencies**
pip install -r requirements.txt (to install all dependencies at once)
 **ODBC Driver for SQL Server** installed on your system

5. Run the ETL script
   a) Scripts/fetch_stockdata.py
After fetching the data, login to your Azure SQL account and then create a database there and then, run:
a)  Scripts/INTRA-DAY/upload_to_azure_sql.py
b)  Scripts/all.in.one_upload/all.in.one_upload.py
c)  Scripts/all.in.one_upload/upload_fundamentals_to_azure_sql.py (To upload fundamentals data as it is in json format)

6. Connect Power BI to Azure SQL
Open Power BI Desktop
Select "Azure SQL Database"
Enter your server and database credentials
Import and visualize data as desired

Connect with me on [LinkedIn](https://www.linkedin.com/in/prathsonawane/) — feel free to reach out with any questions, suggestions, or if you'd like to collaborate on adding new features!

