from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__,template_folder="Templates")


DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'OrganicMarket' # change to the name of your db in xmapp
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

#Function to create product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)',
                   (data['name'], data['price'], data['quantity']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product added successfully'}), 201

#Function to read all the products
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

#Function to update the product
@app.route('/products/<int:id>', methods=['PUT'])
def update_products(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name=%s, price=%s, quantity=%s",
                   ( data['name'], data['price'], data['quantity'], id)) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product Updated!'})

#Function to delete a product
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_products(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id=%s", (id,)) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product Deleted!'})
    
@app.route('/vendor', methods=['POST'])
def add_vendor():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vendor (vID, Vname, Street, City, StateAb, ZipCode) VALUES (%s, %s, %s, %s, %s, %s)",
                   (data["vID"], data['Vname'], data['Street'], data['City'], data['StateAb'], data['ZipCode']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Vendor Added Successfully!'})

if __name__ == '__main__':
        app.run(debug=True)