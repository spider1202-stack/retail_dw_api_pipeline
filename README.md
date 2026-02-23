# Retail Data Warehouse ETL Pipeline

## Project Overview

This project implements a complete **end-to-end Data Warehouse ETL pipeline** that simulates a real-world retail analytics environment. The pipeline extracts product and customer data from public APIs, generates transactional data such as orders, payments, and shipping, and loads the data into a **PostgreSQL data warehouse designed using a star schema**.

The solution demonstrates core **data engineering and analytics engineering principles**, including data extraction, transformation, dimensional modeling, and loading into fact and dimension tables optimized for analytical queries.

The warehouse enables analysis of key business metrics such as:

- Total revenue over time
- Customer purchasing behavior
- Product performance
- Order and shipping trends
- Payment method distribution

The ETL process is fully automated using Python and creates all required tables, ensuring the project can be run from scratch without manual database setup beyond creating the database itself.

This project reflects a **production-style data warehouse workflow**, making it highly relevant for real-world data engineering roles.

---

## Key Objectives

- Build a structured **data warehouse using star schema**
- Implement a complete **ETL pipeline using Python**
- Load data into **PostgreSQL for analytics**
- Demonstrate **fact and dimension table design**
- Enable downstream **business intelligence and reporting**

---

## Business Value

This data warehouse enables stakeholders to make **data-driven decisions** by providing a centralized, query-optimized analytical database that supports reporting, dashboards, and advanced analytics.

---

## Tech Stack
- **Python** (Pandas, Requests, psycopg2)  
- **PostgreSQL** (for warehouse storage)  
- **APIs:**  
  - Fake Store API (Products)  
  - Random User API (Customers)  
- **ETL Concepts:** Star schema, Fact & Dimension tables, Date dimension  

--
## How to config database 
    
    create database name "retail_dw" in pgAdmin
    now go to code"etl_api.py" and edit PostgreSQL connection 
    
    conn = psycopg2.connect(
    host="localhost",
    database="retail_dw",   # must match the database you created
    user="postgres",        # your PostgreSQL username
    password="your PostgreSQL password"        # your PostgreSQL password
)
## Project Architecture

---

## How to Run

1. **Create virtual environment and install dependencies:**

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
python etl_api.py




