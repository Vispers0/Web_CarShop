from flask import Flask, render_template, request, redirect
from pika import ConnectionParameters, BlockingConnection

import json, os

import db

app = Flask(__name__)

connection_params = ConnectionParameters(
    host="localhost",
    port=5672
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load/cars', methods=['GET', 'POST'])
def load_cars():
    if request.method == 'POST':
        raw_json = open('./static/json/cars.json')
        data = json.load(raw_json)
        dealer_id = 1

        for item in data['cars']:
            db.insert('cars', item, dealer_id)
            dealer_id += 1
            if dealer_id > 37:
                dealer_id = 1

        return redirect('/')

@app.route('/load/dealers', methods=['GET', 'POST'])
def load_dealers():
    if request.method == 'POST':
        raw_json = open('./static/json/dilers.json')
        data = json.load(raw_json)
        dealer_id = 1

        for item in data:
            db.insert('dealers', item)

        return redirect('/')

@app.route('/cars')
def cars_index():
    records = db.select('cars')

    headers = ['ID', 'Фирма', 'Модель', 'Г.В.', 'Мощность', 'Цвет', 'Цена', 'ID дилера']

    cars = []

    for record in records:
        cars.append({
            'id': record[0],
            'firm': record[1],
            'model': record[2],
            'year': record[3],
            'power': record[4],
            'color': record[5],
            'price': record[6],
            'dealer_id': record[7]
        })

    return render_template('cars.html', headers = headers, tableData=cars)

@app.route('/dealers')
def dealers_index():
    records = db.select('dealers')

    headers = ['ID', 'Название', 'Город', 'Адрес', 'Округ', 'Рейтинг']

    dealers = []

    for record in records:
        dealers.append({
            'id': record[0],
            'name': record[1],
            'city': record[2],
            'address': record[3],
            'area': record[4],
            'rating': record[5],
        })

    return render_template('dealers.html', headers = headers, tableData=dealers)

@app.route('/dealers/about/<dealer_id>')
def get_cars(dealer_id):
    records = db.find_cars(dealer_id)
    headers = ['ID', 'Фирма', 'Модель', 'Г.В.', 'Мощность', 'Цвет', 'Цена', 'ID дилера']

    cars = []

    for record in records:
        cars.append({
            'id': record[0],
            'firm': record[1],
            'model': record[2],
            'year': record[3],
            'power': record[4],
            'color': record[5],
            'price': record[6],
            'dealer_id': record[7]
        })

    return render_template('cars.html', headers = headers, tableData=cars)

@app.route('/dealers/add/<dealer_id>', methods=['GET', 'POST'])
def add_car(dealer_id):
    if request.method == 'GET':
        return render_template('add_car.html', dealer_id = dealer_id)
    if request.method == 'POST':
        db.insert_car(dealer_id)
        return redirect('/dealers')

@app.route('/dealers/delete/<dealer_id>', methods=['GET', 'POST'])
def delete_car(dealer_id):
    if request.method == 'GET':
        return render_template('delete_car.html', dealer_id = dealer_id)
    if request.method == 'POST':
        db.delete_car(dealer_id)
        return redirect('/dealers')

@app.route('/table/cars')
def show_car_actions():
    return render_template('car_actions.html')

@app.route('/table/dealers')
def show_dealer_actions():
    return render_template('dealer_actions.html')

@app.route('/table/cars/post', methods=['GET', 'POST'])
def post_car():
    if request.method == 'GET':
        return render_template('post_car.html')
    if request.method == 'POST':
        firm = request.form['txt_firm']
        model = request.form['txt_model']
        year = request.form['txt_year']
        power = request.form['txt_power']
        color = request.form['txt_color']
        price = request.form['txt_price']
        dealer = request.form['txt_dealer']
        db.insert_json_car(firm, model, year, power, color, price, dealer)

        message = {
            "eventType": "CREATE",
            "car":{
                "firm": firm,
                "model": model,
                "year": year,
                "power": power,
                "color": color,
                "price": price
            }
        }

        with BlockingConnection(connection_params) as conn:
            with conn.channel() as ch:
                ch.queue_declare(queue="cars_events_queue")
                ch.basic_publish(
                    exchange="",
                    routing_key="cars_events_queue",
                    body=json.dumps(message)
                )
                print("Message sent")

        return json.dumps({'status': 'OK'})

@app.route('/table/dealers/post', methods=['GET', 'POST'])
def post_dealer():
    if request.method == 'GET':
        return render_template('post_dealer.html')
    if request.method == 'POST':
        name = request.form['txt_name']
        city = request.form['txt_city']
        address = request.form['txt_address']
        area = request.form['txt_area']
        rating = request.form['txt_rating']

        db.insert_json_dealer(name, city, address, area, rating)

        return json.dumps({'status': 'OK'})


@app.route('/table/cars/list', defaults={'delete': False})
@app.route('/table/cars/list/<delete>')
def list_cars(delete):
    records = db.select('cars')

    headers = ['ID', 'Фирма', 'Модель', 'Г.В.', 'Мощность', 'Цвет', 'Цена', 'ID дилера']

    cars = []

    for record in records:
        cars.append({
            'id': record[0],
            'firm': record[1],
            'model': record[2],
            'year': record[3],
            'power': record[4],
            'color': record[5],
            'price': record[6],
            'dealer_id': record[7]
        })

    return render_template('car_list.html', headers = headers, tableData=cars, delete=delete)

@app.route('/table/dealers/list', defaults={'delete': False})
@app.route('/table/dealers/list/<delete>')
def list_dealers(delete):
    records = db.select('dealers')

    headers = ['ID', 'Название', 'Город', 'Адрес', 'Округ', 'Рейтинг']

    dealers = []

    for record in records:
        dealers.append({
            'id': record[0],
            'name': record[1],
            'city': record[2],
            'address': record[3],
            'area': record[4],
            'rating': record[5],
        })

    return render_template('dealer_list.html', headers = headers, tableData=dealers, delete=delete)

@app.route('/table/cars/put/<car_id>', methods=['GET', 'PUT'])
def put_car(car_id):
    if request.method == 'GET':
        return render_template('edit_car.html', car_id=car_id)
    if request.method == 'PUT':
        params = request.get_json()
        field = params['field']
        value = params['value']
        table_name = 'cars'

        message = {
            "eventType": "UPDATE",
            "field": field,
            "new_value": value
        }

        with BlockingConnection(connection_params) as conn:
            with conn.channel() as ch:
                ch.queue_declare(queue="cars_events_queue")
                ch.basic_publish(
                    exchange="",
                    routing_key="cars_events_queue",
                    body=json.dumps(message)
                )
                print("Message sent")

        db.update(table_name, car_id, field, value)

        return json.dumps({'status': 'OK'})

@app.route('/table/dealers/put/<dealer_id>', methods=['GET', 'PUT'])
def put_dealer(dealer_id):
    if request.method == 'GET':
        return render_template('edit_dealer.html', dealer_id=dealer_id)
    if request.method == 'PUT':
        params = request.get_json()
        field = params['field']
        value = params['value']
        table_name = 'dealers'

        db.update(table_name, dealer_id, field, value)

        return json.dumps({'status': 'OK'})

@app.route('/table/cars/delete/<car_id>', methods=['GET', 'DELETE'])
def delete_car_by_id(car_id):
    if request.method == 'GET':
        return render_template('confirm_car_delete.html', car_id=car_id)
    if request.method == 'DELETE':
        message = {
            "eventType": "DELETE",
            "deleted_id": car_id
        }

        with BlockingConnection(connection_params) as conn:
            with conn.channel() as ch:
                ch.queue_declare(queue="cars_events_queue")
                ch.basic_publish(
                    exchange="",
                    routing_key="cars_events_queue",
                    body=json.dumps(message)
                )
                print("Message sent")

        db.delete_car_by_id(car_id)
        return json.dumps({'status': 'OK'})

@app.route('/table/dealers/delete/<dealer_id>', methods=['GET', 'DELETE'])
def delete_dealer_by_id(dealer_id):
    if request.method == 'GET':
        return render_template('confirm_dealer_delete.html', dealer_id=dealer_id)
    if request.method == 'DELETE':
        db.delete_dealer_by_id(dealer_id)
        return json.dumps({'status': 'OK'})

if __name__ == '__main__':
    app.run(debug=True)