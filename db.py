from flask import Flask, jsonify, request
import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')
app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')

conn = psycopg2.connect(f'dbname={database_name}')
cursor = conn.cursor()

app = Flask(__name__)

def create_tables():
    try: 
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Companies (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR NOT NULL UNIQUE
            );
        """)
        conn.commit()
    except:
        print("Companies table already exists.")
    try:  
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
            product_id SERIAL PRIMARY KEY,
            company_id INT,
            product_name VARCHAR NOT NULL UNIQUE,
            description VARCHAR,
            price FLOAT,
            active BOOLEAN DEFAULT true
            CONSTRAINT fk_companies FOREIGN KEY (company_id)
            REFERENCES Companies(company_id)
            );
        """)
        conn.commit()
    except:
        print("Products table already exists.")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Warranties (
            warranty_id SERIAL PRIMARY KEY,
            product_id INT,
            warranty_months VARCHAR NOT NULL,
            CONSTRAINTS fk_products FOREIGN KEY (product_id)
            REFERENCES Products(product_id)
            );
        """)
        conn.commit()
    except:
        print("Warranties already exist.")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Categories (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR NOT NULL UNIQUE
            );
        """)
        conn.commit()
    except:
        print("Categories already exist.")
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ProductsCategoriesXref (
            product_id INT,
            category_id INT,
            CONSTRAINTS fk_products FOREIGN KEY (product_id)
            REFERENCES Products(product_id),
            CONSTRAINTS fk_categories FOREIGN KEY (category_id)
            REFERENCES Categories(category_id)
            );
        """)
        conn.commit()
    except:
        print("Xref table already exists.")


if __name__ == '__main__':
    create_tables()
    app.run(host=app_host, port=app_port)