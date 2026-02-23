import requests
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timedelta
import random

# --- 1. PostgreSQL connection ---
conn = psycopg2.connect(
    host="localhost",
    database="retail_dw",   # your database name
    user="postgres",         # your PostgreSQL username
    password="12345"         # your PostgreSQL password
)
cur = conn.cursor()

# --- 2. Auto-create tables if they don't exist ---
create_tables_sql = """
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    gender VARCHAR(10),
    city VARCHAR(50),
    country VARCHAR(50),
    signup_date DATE
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id DATE PRIMARY KEY,
    year INT,
    quarter INT,
    month INT,
    day INT,
    weekday INT
);

CREATE TABLE IF NOT EXISTS dim_payment (
    payment_id INT PRIMARY KEY,
    order_id INT,
    payment_date DATE,
    payment_method VARCHAR(50),
    status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS dim_shipping (
    shipment_id INT PRIMARY KEY,
    order_id INT,
    ship_date DATE,
    delivery_date DATE,
    carrier VARCHAR(50),
    delivery_days INT
);

CREATE TABLE IF NOT EXISTS fact_sales (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    date_id DATE REFERENCES dim_date(date_id),
    quantity INT,
    total_amount NUMERIC,
    payment_id INT REFERENCES dim_payment(payment_id),
    shipment_id INT REFERENCES dim_shipping(shipment_id)
);
"""
cur.execute(create_tables_sql)
conn.commit()
print("✅ Tables created or already exist.")

# --- 3. Helper function to insert dataframe into PostgreSQL ---
def insert_df(df, table):
    tuples = [tuple(x) for x in df.to_numpy()]
    cols = ','.join(list(df.columns))
    query = f"INSERT INTO {table}({cols}) VALUES %s ON CONFLICT DO NOTHING"
    execute_values(cur, query, tuples)
    conn.commit()

# --- 4. Extract Products ---
products_url = "https://fakestoreapi.com/products"
products_resp = requests.get(products_url)
products_df = pd.json_normalize(products_resp.json())
products_df = products_df.rename(columns={"id": "product_id", "title": "product_name"})
products_df = products_df[['product_id','product_name','category','price']]

# --- 5. Extract Customers ---
users_url = "https://randomuser.me/api/?results=20"
users_resp = requests.get(users_url)
users_json = users_resp.json()['results']

customers = []
for i, u in enumerate(users_json):
    customers.append({
        "customer_id": i+1,
        "first_name": u['name']['first'],
        "last_name": u['name']['last'],
        "email": u['email'],
        "gender": u['gender'],
        "city": u['location']['city'],
        "country": u['location']['country'],
        "signup_date": pd.to_datetime(u['registered']['date']).date()
    })
customers_df = pd.DataFrame(customers)

# --- 6. Generate Orders, Payments, Shipping ---
orders_list = []
payments_list = []
shipping_list = []
order_id_counter = 1
payment_id_counter = 1
shipment_id_counter = 1
date_list = []

for _, cust in customers_df.iterrows():
    num_orders = random.randint(1,5)
    for _ in range(num_orders):
        product = products_df.sample(1).iloc[0]
        order_date = datetime.today() - timedelta(days=random.randint(1, 365))
        quantity = random.randint(1,3)
        total_amount = quantity * product['price']

        # Order
        orders_list.append({
            "order_id": order_id_counter,
            "customer_id": cust['customer_id'],
            "product_id": product['product_id'],
            "order_date": order_date,
            "quantity": quantity,
            "total_amount": total_amount
        })

        # Payment
        payments_list.append({
            "payment_id": payment_id_counter,
            "order_id": order_id_counter,
            "payment_date": order_date + timedelta(days=random.randint(0,2)),
            "payment_method": random.choice(["Credit Card","Paypal","Debit Card"]),
            "status": random.choice(["Completed","Pending","Failed"])
        })

        # Shipping
        ship_date = order_date + timedelta(days=1)
        delivery_date = ship_date + timedelta(days=random.randint(2,7))
        shipping_list.append({
            "shipment_id": shipment_id_counter,
            "order_id": order_id_counter,
            "ship_date": ship_date,
            "delivery_date": delivery_date,
            "carrier": random.choice(["UPS","FedEx","DHL"]),
            "delivery_days": (delivery_date - ship_date).days
        })

        # Date dimension
        date_list.append(order_date.date())

        # Increment counters
        order_id_counter += 1
        payment_id_counter += 1
        shipment_id_counter += 1

orders_df = pd.DataFrame(orders_list)
payments_df = pd.DataFrame(payments_list)
shipping_df = pd.DataFrame(shipping_list)

# --- 7. Create Date Dimension ---
dates_df = pd.DataFrame({'date_id': list(set(date_list))})
dates_df['year'] = dates_df['date_id'].apply(lambda x: x.year)
dates_df['quarter'] = dates_df['date_id'].apply(lambda x: (x.month-1)//3 +1)
dates_df['month'] = dates_df['date_id'].apply(lambda x: x.month)
dates_df['day'] = dates_df['date_id'].apply(lambda x: x.day)
dates_df['weekday'] = dates_df['date_id'].apply(lambda x: x.weekday())

# --- 8. Load Dimension Tables ---
insert_df(customers_df, 'dim_customer')
insert_df(products_df, 'dim_product')
insert_df(dates_df, 'dim_date')
insert_df(payments_df, 'dim_payment')
insert_df(shipping_df, 'dim_shipping')

# --- 9. Load Fact Table ---
fact_sales_df = orders_df.merge(payments_df[['payment_id','order_id']], on='order_id')
fact_sales_df = fact_sales_df.merge(shipping_df[['shipment_id','order_id']], on='order_id')
fact_sales_df['date_id'] = fact_sales_df['order_date'].dt.date

insert_df(fact_sales_df[['order_id','customer_id','product_id','date_id','quantity','total_amount','payment_id','shipment_id']], 'fact_sales')

print("✅ ETL Pipeline completed successfully!")

# --- 10. Close connection ---
cur.close()
conn.close()