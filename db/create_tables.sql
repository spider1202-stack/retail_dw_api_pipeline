-- Dimensions
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

-- Fact Table
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