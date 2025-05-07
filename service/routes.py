from flask import Flask, request, jsonify
from app import app, db, Product  # Assuming your Flask app is set up with the app and db from app.py

# Task 4a: Provide GitHub URL of service/routes.py showing the code snippet for READ function
@app.route('/products/<int:id>', methods=['GET'])
def read_product(id):
    product = Product.query.get(id)
    
    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'category': product.category,
        'price': product.price,
        'availability': product.availability
    })

# Task 4b: Provide GitHub URL of service/routes.py showing the code snippet for UPDATE function
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    
    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.get_json()
    
    # Update the product fields
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.category = data.get('category', product.category)
    product.price = data.get('price', product.price)
    product.availability = data.get('availability', product.availability)
    
    db.session.commit()
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'category': product.category,
        'price': product.price,
        'availability': product.availability
    })

# Task 4c: Provide GitHub URL of service/routes.py showing the code snippet for DELETE function
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    
    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    
    return jsonify({"message": "Product deleted successfully"})

# Task 4d: Provide GitHub URL of service/routes.py showing the code snippet for LIST ALL / LIST BY NAME / LIST BY CATEGORY and LIST BY AVAILABILITY function

@app.route('/products', methods=['GET'])
def list_products():
    # Get query parameters for filtering
    name = request.args.get('name')
    category = request.args.get('category')
    availability = request.args.get('availability')
    
    query = Product.query
    
    # Filter by name if provided
    if name:
        query = query.filter(Product.name.ilike(f'%{name}%'))
    
    # Filter by category if provided
    if category:
        query = query.filter(Product.category.ilike(f'%{category}%'))
    
    # Filter by availability if provided
    if availability:
        availability = availability.lower() == 'true'
        query = query.filter(Product.availability == availability)
    
    products = query.all()
    
    if not products:
        return jsonify({"message": "No products found"}), 404
    
    # Return list of products
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'category': product.category,
        'price': product.price,
        'availability': product.availability
    } for product in products])

