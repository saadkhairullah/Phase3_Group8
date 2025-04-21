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
    cursor.execute('INSERT INTO item (iId ,Iname, Sprice, Category) VALUES (%s, %s, %s, %s)',
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
    

@app.route('/vendor', methods=['GET'])
def get_vendor():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vendor") 
    vendors= cursor.fetchall()
    conn.close()
    return jsonify(vendors)

@app.route('/vendor', methods =['POST'])
def add_vendor():
    data = request.json
    print("Received a POST request")
    print(request.json)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO vendor (vId ,Vname, Street, City, StateAb, ZipCode) VALUES (%s, %s, %s, %s, %s, %s)',
                   ( data['vId'], data['Vname'], data['Street'], data['City'], data['StateAb'], data['ZipCode'])) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Vendor Added!'}), 201

@app.route('/vendor/<int:vId>', methods=['DELETE'])
def delete_vendor(vId):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vendor WHERE vId=%s", (vId,)) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Vendor Deleted!'})

@app.route('/vendor/<int:vId>', methods=['PUT'])
def update_vendor(vId):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE vendor SET vId=%s ,Vname=%s, Street=%s, City=%s, SateAb=%s, ZipCode=%s',
                   ( data['iId'], data['Iname'], data['Sprice'], data['Category'], data['StateAb'], data['ZipCode'])) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Vendor Updated!'})

# __________________________________________________________

@app.route('/store_item', methods =['POST'])
def add_store_item():
    data = request.json
    print("Received a POST request")
    print(request.json)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO store_item (sId ,iId , Scount) VALUES (%s, %s, %s)',
                   ( data['sId'], data['iId'], data['Scount'])) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'store_item Added!'}), 201

@app.route('/store_item', methods=['GET'])
def get_store_item():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM store_item") 
    store_items= cursor.fetchall()
    conn.close()
    return jsonify(store_items)

@app.route('/store_item/<int:sId>/<int:iId>', methods=['DELETE'])
def delete_store_item(sId,iId):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM store_item WHERE sId=%s AND iId=%s", (sId, iId,)) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'Store_Item Deleted!'})

#---------------------------------------------------------------------------------------

@app.route('/vendor_item', methods =['POST'])
def add_vendor_item():
    data = request.json
    print("Received a POST request")
    print(request.json)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO vendor_item (vId ,iId) VALUES (%s, %s)',
                   ( data['vId'], data['iId'])) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'vendor_item Added!'}), 201

@app.route('/vendor_item', methods=['GET'])
def get_vendor_item():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vendor_item") 
    vendor_items= cursor.fetchall()
    conn.close()
    return jsonify(vendor_items)

@app.route('/vendor_item/<int:vId>/<int:iId>', methods=['DELETE'])
def delete_vendor_item(vId,iId):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vendor_item WHERE vId=%s AND iId=%s", (vId, iId,)) 
    conn.commit()
    conn.close()
    return jsonify({'message': 'vendor_Item Deleted!'})

@app.route('/itemsalessummary', methods=['GET'])
def get_QV1():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Iname, TotalRevenue FROM itemsalessummary ORDER BY TotalRevenue DESC LIMIT 3 ") 
    summary= cursor.fetchall()
    conn.close()
    return jsonify(summary)

@app.route('/itemsalessummary', methods=['GET1'])
def get_QV2():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Iname, TotalQuantitySold FROM itemsalessummary WHERE TotalQuantitySold > 50;") 
    summary= cursor.fetchall()
    conn.close()
    return jsonify(summary)

@app.route('/toployalcustomers', methods=['GET'])
def get_QV3():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Cname, LoyaltyScore FROM toployalcustomers WHERE LoyaltyScore = (SELECT MAX(LoyaltyScore) FROM toployalcustomers)") 
    summary= cursor.fetchall()
    conn.close()
    return jsonify(summary)

@app.route('/toployalcustomers', methods=['GET1'])
def get_QV4():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT Cname, LoyaltyScore FROM toployalcustomers WHERE LoyaltyScore = 5 OR LoyaltyScore = 4") 
    summary= cursor.fetchall()
    conn.close()
    return jsonify(summary)

@app.route('/itemsalessummary', methods=['GET2'])
def get_QV5():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT SUM(TotalRevenue) AS TotalRevenue FROM itemsalessummary LIMIT 1") 
    summary= cursor.fetchall()
    conn.close()
    return jsonify(summary)

    
if __name__ == '__main__':
        app.run(debug=True)