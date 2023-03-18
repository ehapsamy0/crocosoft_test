from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import json
import os
import re

app = Flask(__name__)




app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST',"db")
app.config['MYSQL_USER'] =  os.environ.get("MYSQL_USER","myuser")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD","mypassword")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB","mydatabase")

phone_regex = r"^(?:\+20|0)?1[0-2]\d{8}$"

def is_egyptian_national_id(national_id):
    # check if national_id is a string of 14 digits
    if not isinstance(national_id, str) or not re.match(r'^\d{14}$', national_id):
        return False
    
    # check if the first digit is either 2, 3, 4, or 9
    if national_id[0] not in ['2', '3', '4', '9']:
        return False

    return True


mysql = MySQL(app)

@app.before_first_request
def create_tables():
    try:
        #create tables once for the first app run
        
        cursor = mysql.connection.cursor()
        cursor.execute('''
            CREATE TABLE type_vehicle(
                id TINYINT NOT NULL AUTO_INCREMENT,
                name VARCHAR(50),
                PRIMARY KEY (id));
            CREATE TABLE vehicle(
                id INT NOT NULL AUTO_INCREMENT,
                model VARCHAR(50),
                type_id TINYINT,
                available BOOLEAN,
                day_cost INT,
                color VARCHAR(50),
                time_create DATETIME DEFAULT CURRENT_TIMESTAMP,
                time_update DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (type_id) REFERENCES type_vehicle(id),
                PRIMARY KEY (id));
            CREATE TABLE customer(
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(100),
                phone VARCHAR(20),
                address VARCHAR(120),
                national_id VARCHAR(50),
                time_create DATETIME DEFAULT CURRENT_TIMESTAMP,
                time_update DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (id));
            CREATE TABLE booking(
                id INT NOT NULL AUTO_INCREMENT,
                vehicle_id INT,
                customer_id INT,
                start_day DATE,
                end_day DATE, 
                FOREIGN KEY (vehicle_id) REFERENCES vehicle(id),
                FOREIGN KEY (customer_id) REFERENCES customer(id),
                PRIMARY KEY (id),
                CONSTRAINT check_return_date CHECK(end_day >= start_day AND DATEDIFF(end_day,start_day) <= 7));
        ''')
    except:
        #tables already created
        return True


#Get customers
@app.route("/get_customers", methods=["GET"])
def get_customers():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(f'''SELECT * FROM customer''')
        result = cursor.fetchall()

        # Get column names from cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Create list of dictionaries with column names as keys
        data = []
        for row in result:
            data.append({column_names[i]: row[i] for i in range(len(column_names))})

        return jsonify({
            'data': data,
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Error: {e}',
        }), 404



#Get customer with ID
@app.route("/get_customer/<int:pk>", methods=["GET"])
def get_customer(pk):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(f'''SELECT * FROM customer WHERE id = {pk}''')
        result = cursor.fetchall()
        if not result:
            return jsonify({
                'error': f'Customer with ID {pk} not found',
            }) , 404
        result=result[0]
        column_names = [desc[0] for desc in cursor.description]
        data = {column_names[i]: result[i] for i in range(len(column_names))}
        return jsonify({
            'data': data,
        }) , 200
    except Exception as e:
        return jsonify({
            'error': f'Error: {e}',
        }) , 404
    



# Create Customer
@app.route("/create_customer/",methods=['POST'])
def create_customer():
    data = json.loads(request.data)
    try:
        name = data['name']
        phone = data['phone']
        if not re.match(phone_regex, phone):
            return jsonify({
                "msg":"make sure this phone is egyption phone please."
            }),400
        address = data['address']
        national_id = data.get('national_id',None)
        if not is_egyptian_national_id(national_id):
            return jsonify({
                "msg":f"make sure this national id {national_id} is egyption national id please."
            }),400
        cursor = mysql.connection.cursor()
        query = f'INSERT INTO customer (name,phone,address,national_id) VALUES ("{name}","{phone}","{address}","{national_id}");'
        cursor.execute(query)
        mysql.connection.commit()
        return jsonify({
            'msg':"Customer created successfully"
        }) , 201
    except Exception as e:
        return jsonify({
            'error': f'Error: {e}',
        }) , 404


@app.route("/update_customer/<int:pk>", methods=["PUT"])
def update_customer(pk):
    data = json.loads(request.data)
    try:
        name = data['name']
        phone = data['phone']
        if not re.match(phone_regex, phone):
            return jsonify({
                "msg":"make sure this phone is egyption phone please."
            })
        cursor = mysql.connection.cursor()
        
        query = f'UPDATE customer SET name="{name}",phone="{phone}" WHERE id={pk}'
        cursor.execute(query)
        mysql.connection.commit()
        return jsonify({
            'msg':f"Update User successfully"
        }) , 200
    except Exception as e:
        return jsonify({
            'error': f'Error: {e}',
        }) , 400

# Deleet Customer
@app.route("/customer_delete/<int:pk>", methods=["DELETE"])
def customer_delete(pk):
    try:
        cursor = mysql.connection.cursor()
        query = f'DELETE FROM customer WHERE id = {pk};'
        cursor.execute(query)
        mysql.connection.commit()
        return jsonify({
            'msg':f"deleted successfully"
        }) , 200
    except Exception as e:
        return jsonify({
            'error': f'Error: {e}',
        }) , 400
