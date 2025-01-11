from flask import request
import psycopg2, logging

DATABASE_NAME = 'cars_db'
USER = 'visp0'
PWD = '8629'
HOST = 'localhost'

def select(table: str):
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PWD, host=HOST)
    table_name = table

    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name};')
    records = cursor.fetchall()
    conn.close()
    return records

def insert(table: str, data: dict, dealer_id: int = 0):
    if table == 'cars':
        query = f'INSERT INTO cars (firm, model, year, power, color, price, dealer_id) VALUES (\'{data["firm"]}\', \'{data["model"]}\', {data["year"]}, {data["power"]}, \'{data["color"]}\', {data["price"]}, {dealer_id});'
    if table == 'dealers':
        query = f'INSERT INTO dealers (name, city, address, area, rating) VALUES (\'{data["Name"]}\', \'{data["City"]}\', \'{data["Address"]}\', \'{data["Area"]}\', {data["Rating"]});'

    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PWD, host=HOST)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()

def find_cars(dealer_id: int):
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PWD, host=HOST)
    table_name = 'cars'

    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name} WHERE dealer_id = {dealer_id};')
    records = cursor.fetchall()
    conn.close()
    return records

def insert_car(dealer_id):
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PWD, host=HOST)
    conn.autocommit = True
    table_name = 'cars'

    firm = request.form.get("txt_firm")
    model = request.form.get("txt_model")
    year = request.form.get("txt_year")
    power = request.form.get("txt_power")
    color = request.form.get("txt_color")
    price = request.form.get("txt_price")

    query = f'INSERT INTO {table_name} (firm, model, year, power, color, price, dealer_id) VALUES (\'{firm}\', \'{model}\', {year}, {power}, \'{color}\', {price}, {dealer_id});'
    print(query)

    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()

def delete_car(dealer_id):
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PWD, host=HOST)
    conn.autocommit = True
    table_name = 'cars'

    car_id = request.form.get("txt_car_id")

    query = f'DELETE FROM {table_name} WHERE id={car_id} AND dealer_id={dealer_id}' 
    print(query)

    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()

def insert_json_car(firm, model, year, power, color, price, dealer_id):
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PWD, host=HOST)
    conn.autocommit = True
    table_name = 'cars'

    query = f'INSERT INTO {table_name} (firm, model, year, power, color, price, dealer_id) VALUES (\'{firm}\', \'{model}\', {year}, {power}, \'{color}\', {price}, {dealer_id});'

    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()

def insert_json_dealer(name, city, address, area, rating):
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PWD, host=HOST)
    conn.autocommit = True
    table_name = 'dealers'

    query = f'INSERT INTO {table_name} (name, city, address, area, rating) VALUES (\'{name}\', \'{city}\', \'{address}\', \'{area}\', {rating});'

    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()

def update(table_name, id, field, value):
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PWD, host=HOST)
    conn.autocommit = True

    if type(value) is not int:
        query = f'UPDATE {table_name} SET {field} = \'{value}\' WHERE id = {id}'
    else:
        query = f'UPDATE {table_name} SET {field} = {value} WHERE id = {id}'

    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()

def delete_car_by_id(car_id):
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PWD, host=HOST)
    conn.autocommit = True
    table_name = 'cars'

    query = f'DELETE FROM {table_name} WHERE id={car_id};' 

    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()

def delete_dealer_by_id(dealer_id):
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PWD, host=HOST)
    conn.autocommit = True
    table_name = 'dealers'

    query = f'DELETE FROM {table_name} WHERE id={dealer_id};' 

    cursor = conn.cursor()
    cursor.execute(query)
    conn.close()