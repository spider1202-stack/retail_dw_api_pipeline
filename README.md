# Retail Data Warehouse ETL Pipeline

## Project Overview
This project builds a full **API-based Data Warehouse** with a **star schema** design. It fetches data from public APIs, generates transactional data, and loads it into PostgreSQL dimension and fact tables. The pipeline demonstrates a real-world ETL workflow, suitable for portfolio and junior data engineering roles.

---

## Tech Stack
- **Python** (Pandas, Requests, psycopg2)  
- **PostgreSQL** (for warehouse storage)  
- **APIs:**  
  - Fake Store API (Products)  
  - Random User API (Customers)  
- **ETL Concepts:** Star schema, Fact & Dimension tables, Date dimension  

---

## Project Architecture

---

## How to Run

1. **Create virtual environment and install dependencies:**

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
python etl_api.py
