from flask import Flask, jsonify, request
import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')
app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')

conn = psycopg2.connect(f'dbname={database_name}')
cursor = conn.cursor()

app = Flask(__name__)

@app.route('/company', method=['POST'])
def add_company():
    post_data = request.form if request.form else request.json()

    company_name = post_data.get('company_name')

    if not company_name:
        return jsonify({'message': 'company_name is a required field'}), 400
    
    result = cursor.execute("""
        SELECT * FROM Companies
        WHERE company_name = %s
    """, (company_name,))

    result = cursor.fetchone()

    if result:
        return jsonify({'message': 'Company already exists'}), 400
    
    cursor.execute("""
        INSERT INTO Companies (company_name) VALUES(%s)
    """, (company_name,))
    conn.commit()
    return jsonify({'message': f'Company {company_name} added to the DB'}), 201

@app.route('/category', method=['POST'])
def add_category():
    post_data = request.form if request.form else request.json()

    category_name = post_data.get('category_name')

    if not category_name:
        return jsonify({'message': 'category_name is a required field'}), 400
    
    result = cursor.execute("""
        SELECT * FROM Categories
        WHERE category_name = %s
    """, (category_name,))

    result = cursor.fetchone()
    if result:
        return jsonify({'message': 'Category already exists'}), 400
    
    cursor.execute("""
        INSERT INTO Categories (category_name) VALUES(%s)
    """, (category_name,))
    
    conn.commit()
    return jsonify({'message': f'Category {category_name} added to DB'}), 201

@app.route('/product', method=['POST'])
def add_product():
    post_data = request.form if request.form else request.json()

    company_id = post_data.get('company_id')
    product_name = post_data.get('product_name')
    price = post_data.get('price')
    description = post_data.get('description')

    if not product_name:
        return jsonify({'message': 'product_name is a required field'}), 400
    
    result = cursor.fetchone()

    result = cursor.execute("""
        SELECT * FROM Products
        WHERE product_name = %s
    """, (product_name,))

    if result:
        return jsonify({'message': 'Product already exists'}), 400
    
    cursor.execute("""
        INSERT INTO Products (company_id, product_name, price, description)
            VALUES(%s,%s,%s,%s)
    """, (company_id, product_name, price, description))

    conn.commit()
    return jsonify({'message': f'Product {product_name} added to DB'}), 201

@app.route('/warranty', method=['POST'])
def add_warranty():
    post_data = request.form if request.form else request.json()

    product_id = post_data.get('product_id')
    warranty_months = post_data.get('warranty_months')

    if not warranty_months:
        return jsonify({'message': 'warranty_months is a required field'}), 400
    
    cursor.execute("""
        INSERT INTO Warranties (product_id, warranty_months) VALUES(%s,%s)
    """, (product_id, warranty_months,))
    
    conn.commit()
    return jsonify({'message': 'Warranty added to DB'}), 201

@app.route('/companies', method=['GET'])
def get_companies():
    result = cursor.execute("""
        SELECT * FROM Companies
    """)

    result = cursor.fetchall()
    record_list = []

    for record in result:
        record = {
            'company_id': record[0],
            'company_name': record[1],
        }

        record_list.append(record)
    
    return jsonify({'message': 'companies found', 'results': record_list}), 200

@app.route('/categories', method=['GET'])
def get_categories():
    result = cursor.execute("""
        SELECT * FROM Categories
    """)
    result = cursor.fetchall()
    record_list = []

    for record in result:
        record = {
            'category_id': record[0],
            'category_name': record[1]
        }
        record_list.append(record)
    
    return jsonify({'message': 'categories found', 'results': record_list}), 200

@app.route('/products', method=['GET'])
def get_products():
    result = cursor.execute("""SELECT * FROM Products""")
    result = cursor.fetchall()

    record_list = []

    for record in result:
        record = {
            'product_id': record[0],
            'company_id': record[1], 
            'product_name': record[2],
            'price': record[3],
            'description': record[4],
            'active': record[5]
        }

        record_list.append(record)
    
    return jsonify({'message': 'products found', 'results': record_list}), 200

@app.route('/products/active', method=['GET'])
def get_active_products():
    result = cursor.execute("""SELECT * FROM Products WHERE active = 'true'""")
    result = cursor.fetchall()

    record_list = []

    for record in result:
        record = {
            'product_id': record[0],
            'company_id': record[1], 
            'product_name': record[2],
            'price': record[3],
            'description': record[4],
            'active': record[5]
        }

        record_list.append(record)
    
    return jsonify({'message': 'active products found', 'results': record_list}), 200

@app.route('/company/<company_id>', method=['GET'])
def get_company_id(company_id):
    result = cursor.execute("""SELECT * FROM Companies WHERE company_id = %s""", (company_id,))
    result = cursor.fetchone()
    record_list = []
    for record in result:
        record = {
            'company_id': record[0],
            'company_name': record[1]
        }
        record_list.append(record)
    return jsonify({'message': 'company found', 'results': record_list}), 200

@app.route('/category/<category_id>', method=['GET'])
def get_category_id(category_id):
    result = cursor.execute("""SELECT * FROM Categories WHERE category_id = %s""", (category_id,))
    result = cursor.fetchone()
    record_list = []
    for record in result:
        record = {
            'category_id': record[0],
            'category_name': record[1]
        }
        record_list.append(record)
    return jsonify({'message': 'category found', 'results': record_list}), 200

@app.route('/product/<product_id>', method=['GET'])
def get_product_id(product_id):
    result = cursor.execute("""SELECT p.*, c.category_name FROM Products p 
                            JOIN ProductsCategoriesXref pcx ON p.product_id = pcx.product_id
                            JOIN Categories c ON pcx.category_id = c.category_id
                            WHERE p.product_id = %s""", (product_id,))
    result = cursor.fetchone()
    record_list = []
    for record in result:
        record = {
            'product_id': record[0],
            'company_id': record[1], 
            'product_name': record[2],
            'price': record[3],
            'description': record[4],
            'active': record[5],
            'category_name': record[6]
        }

        record_list.append(record)
    return jsonify({'message': 'product found', 'results': record_list}), 200

@app.route('/warranty/<warranty_id>', method=['GET'])
def get_warranty_id(warranty_id):
    result = cursor.execute("""SELECT * FROM Warranties WHERE warranty_id = %s""", (warranty_id,))
    result = cursor.fetchone()
    record_list = []
    for record in result:
        record = {
            'warranty_id': record[0],
            'product_id': record[1],
            'warranty_months': record[2]
        }
        record_list.append(record)
    return jsonify({'message': 'warranty found', 'results': record_list}), 200

@app.route('/update-company/<company_id>', method=['PUT'])
def company_update(company_id):
    post_data = request.form if request.form else request.json()

    company_name = post_data.get('company_name')
    try:
        cursor.execute("""UPDATE Companies SET company_name = %s WHERE company_id = %s""", (company_name, company_id,))
        conn.commit()

        return jsonify({'message': f'{company_name} updated successfully'}), 200
    except:
        return jsonify({'message': 'error, update unsuccessful'}), 400
    
@app.route('/update-category/<category_id>', method=['PUT'])
def category_update(category_id):
    post_data = request.form if request.form else request.json()

    category_name = post_data.get('category_name')

    try:
        cursor.execute("""UPDATE Categories SET category_name = %s WHERE category_id = %s""", (category_name, category_id,))
        conn.commit()

        return jsonify({'message': 'category_name updated successfully'}), 200
    except:
        return jsonify({'message': 'error, update unsuccessful'}), 400
    
@app.route('/update-product/<product_id>', method=['PUT'])
def product_update(product_id):
    post_data = request.form if request.form else request.json()

    company_id = post_data.get('company_id')
    product_name = post_data.get('product_name')
    price = post_data.get('price')
    description = post_data.get('description')
    active = post_data.get('active')

    try:
        cursor.execute("""UPDATE Products 
                       SET company_id=%s, product_name=%s, price=%s, description=%s, active=%s 
                       WHERE product_id=%s""", 
                       (company_id, product_name, price, description, active, product_id,))
        conn.commit()
        return jsonify({'message': 'product updated successfully'}), 200
    except:
        return jsonify({'message': 'error, update unsuccessful'}), 400
    
@app.route('/update-warranty/<warranty_id>', method=['PUT'])
def warranty_update(warranty_id):
    post_data = request.form if request.form else request.json()

    product_id = post_data.get('product_id')
    warranty_months = post_data.get('warranty_months')

    try: 
        cursor.execute("""UPDATE Warranties SET product_id = %s, warranty_months = %s WHERE warranty_id = %s""", (product_id, warranty_months, warranty_id,))
        conn.commit()

        return jsonify({'message': 'warranty update successful'}), 200
    except:
        return jsonify({'message': 'error, update unsuccessful'}), 400

@app.route('/company/delete', method=['DELETE'])
def company_delete(company_id):
     try:
         cursor.execute("""DELETE * FROM Companies WHERE company_id = %s""", (company_id,))
         cursor.execute("""DELETE * FROM Products WHERE company_id = %s""", (company_id,))
         conn.commit()

         return jsonify({'message': 'associated records succesfully deleted.'}), 200
     except:
         return jsonify({'message': 'error, deletion cancelled'}), 400

@app.route('/product/delete', method=['DELETE'])
def product_delete(product_id):
    try:
        cursor.execute("""DELETE * FROM Warranties WHERE product_id = %s""", (product_id,))
        cursor.execute("""DELETE * FROM ProductsCategoriesXref WHERE product_id = %s""", (product_id,))
        cursor.execute("""DELETE * FROM Products WHERE product_id = %s""", (product_id,))
        conn.commit()

        return jsonify({'message':'associated records succesfully deleted'}), 200
    except:
        return jsonify({'message': 'error, deletion cancelled'}), 400
    
@app.route('/category/delete', method=['DELETE'])
def category_delete(category_id):
    try:
        cursor.execute("""DELETE * FROM ProductsCategoriesXref WHERE category_id = %s""", (category_id,))
        cursor.execute("""DELETE * FROM Categories WHERE category_id = %s""", (category_id,))
        conn.commit()

        return jsonify({'message': 'associated records deleted successfully'}), 200
    except:
        return jsonify({'message': 'error, deletion cancelled'}), 400

@app.route('/warranty/delete', method=['DELETE'])
def warranty_delete(warranty_id):
    try:
        cursor.execute("""DELETE * FROM Warranties WHERE warranty_id = %s""", (warranty_id,))
        conn.commit()

        return jsonify({'message': 'associated records deleted'}), 200
    except:
        return jsonify({'message': 'error, deletion cancelled'}), 400