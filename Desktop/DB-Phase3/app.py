from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__,template_folder="Templates")

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'phase2_group8v2' # change to the name of your db in xmap
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/item', methods =['POST'])
def add_product():
    data = request.json
    print("Received a POST request")
    print(request.json)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO item (iId ,Iname, Sprice, Category) VALUES (%s, %s, %s, %s)",
                   ( data['iId'], data['Iname'], data['Sprice'], data['Category'])) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product Added!'}), 201

@app.route('/item', methods=['GET'])
def get_item():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM item") 
    items= cursor.fetchall()
    conn.close()
    return jsonify(items)

@app.route('/item/<int:iId>', methods=['PUT'])
def update_item(iId):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE item SET iId=%s ,Iname=%s, Sprice=%s, Category=%s',
                   ( data['iId'], data['Iname'], data['Sprice'], data['Category'])) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product Updated!'})

@app.route('/item/<int:iId>', methods=['DELETE'])
def delete_item(iId):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM item WHERE iId=%s", (iId,)) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product Deleted!'})
    
    
if __name__ == '__main__':
        app.run(debug=True)