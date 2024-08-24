#!/usr/bin/env python3

# Remote library imports
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# Local imports
from config import app, db
from models import User, Product,Category, Cart, CartItem, Order, OrderItem

# Initialize Bcrypt and JWTManager
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


################################################################
# Reister route
@app.route("/register", methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input data
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid data provided'}), 400
    
    # Check if the username already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    # Create a new user instance
    new_user = User(
        username=data['username'],
        password=hashed_password,
        email=data.get('email'),
        role=data.get('role', 'customer')  # Default role is 'customer'
    )
    
    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201



################################################################
# Login route
@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input data
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid data provided'}), 400
    
    # Find the user by username
    user = User.query.filter_by(username=data['username']).first()
    
    # Check if user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, data['password']):
        # Create JWT access token
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        
        # Return the token and user info
        return jsonify({
            'access_token': access_token,
            'id': user.id,
            'username': user.username,
            'role': user.role
        }), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

################################################################
# Get all products route
@app.route("/products", methods=['GET'])
def get_all_products():
    # Query all products from the database
    products = Product.query.all()
    
    product_list = []
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'image_url': product.image_url,
            'category': product.category.name  
        }
        product_list.append(product_data)
    
    return jsonify(product_list), 200

####################################################################
# Get product by ID route
@app.route("/products/<int:id>", methods=['GET'])
def get_product_by_id(id):

    product = Product.query.get(id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url,
        'category': product.category.name  
    }

    return jsonify(product_data), 200



###################################################################
# Creating new product
@app.route("/products", methods=['POST'])
@jwt_required()
def create_product():
    # Get the identity of the current user
    current_user = get_jwt_identity()
    
    # Check if the current user is an admin
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Access denied. Admins only.'}), 403
    
    # Get product data from the request
    data = request.get_json()
    if not data or 'name' not in data or 'description' not in data or 'price' not in data or 'category_id' not in data:
        return jsonify({'message': 'Invalid data provided'}), 400
    
    # Create a new product
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image_url=data.get('image_url', ''),  # Optional image URL
        category_id=data['category_id']
    )
    
    # Save the product to the database
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({'message': 'Product created successfully', 'product': {
        'id': new_product.id,
        'name': new_product.name,
        'description': new_product.description,
        'price': new_product.price,
        'image_url': new_product.image_url,
        'category_id': new_product.category_id
    }}), 201



################################################################
# updating products
@app.route("/products/<int:product_id>", methods=['PUT'])
@jwt_required()
def update_product(product_id):
    # Get the identity of the current user
    current_user = get_jwt_identity()
    
    # Check if the current user is an admin
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Access denied. Admins only.'}), 403
    
    # Get product data from the request
    data = request.get_json()
    
    # Find the product by ID
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    # Update product fields if provided in the request
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.image_url = data.get('image_url', product.image_url)
    product.category_id = data.get('category_id', product.category_id)
    
    # Save changes to the database
    db.session.commit()
    
    return jsonify({'message': 'Product updated successfully', 'product': {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url,
        'category_id': product.category_id
    }}), 200



########################################################################
# deleting products
@app.route("/products/<int:product_id>", methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    # Get the identity of the current user from the JWT
    current_user = get_jwt_identity()
    
    # Check if the current user has the admin role
    if current_user['role'] != 'admin':
        return jsonify({'message': 'Access denied. Admins only.'}), 403
    
    # Retrieve the product by its ID
    product = Product.query.get(product_id)
    
    # If the product does not exist, return a 404 error
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    # Delete the product from the database
    db.session.delete(product)
    db.session.commit()
    
    # Return a success message
    return jsonify({'message': f'Product "{product.name}" has been deleted successfully.'}), 200

################################################
#adding product to cart
@app.route("/cart", methods=['POST'])
@jwt_required()
def add_to_cart():
    # Get the identity of the current user
    current_user = get_jwt_identity()
    
    # Get the product data from the request
    data = request.get_json()
    
    # Validate the input data
    if not data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({'message': 'Invalid data provided'}), 400
    
    # Find the product by ID
    product = Product.query.get(data['product_id'])
    
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    # Check if the quantity is valid
    if data['quantity'] <= 0:
        return jsonify({'message': 'Invalid quantity'}), 400
    

    
    # Check if the product is already in the user's cart
    cart_item = CartItem.query.filter_by(user_id=current_user['id'], product_id=product.id).first()
    
    if cart_item:
        # If the product is already in the cart, update the quantity
        cart_item.quantity += data['quantity']
    else:
        # If the product is not in the cart, create a new CartItem
        cart_item = CartItem(
            user_id=current_user['id'],
            product_id=product.id,
            quantity=data['quantity']
        )
        db.session.add(cart_item)
    
    # Commit the changes to the database
    db.session.commit()
    
    return jsonify({'message': 'Product added to cart successfully'}), 201


################################################################
#getting products in cart
@app.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    # Get the current user from the JWT token
    current_user_id = get_jwt_identity()
    
    # Query for the user's cart
    cart = Cart.query.filter_by(user_id=current_user_id).first()
    
    if not cart:
        return jsonify({"message": "Cart is empty"}), 200
    
    # Get the cart items and related product details
    cart_items = []
    for item in cart.items:
        product = Product.query.get(item.product_id)
        cart_items.append({
            'product_id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'quantity': item.quantity,
            'image_url': product.image_url
        })
    
    # Return the cart details as JSON
    return jsonify({
        'cart_id': cart.id,
        'total_price': cart.total_price,
        'items': cart_items
    }), 200



################################################################
# Route to update the quantity of an item in the cart
@app.route('/cart/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):

    # Get the current user from the JWT token
    current_user_id = get_jwt_identity()
    
    # Find the user's cart
    cart = Cart.query.filter_by(user_id=current_user_id).first()
    
    if not cart:
        return jsonify({"message": "Cart not found"}), 404
    
    # Find the cart item by ID
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    
    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404
    
    # Get the new quantity from the request data
    data = request.get_json()
    new_quantity = data.get('quantity')
    
    if not new_quantity or new_quantity < 1:
        return jsonify({"message": "Invalid quantity provided"}), 400
    
    # Update the quantity of the cart item
    cart_item.quantity = new_quantity
    db.session.commit()
    
    return jsonify({
        "message": "Cart item updated successfully",
        "item_id": cart_item.id,
        "product_id": cart_item.product_id,
        "quantity": cart_item.quantity
    }), 200


################################################################
# Route to remove an item from the cart
@app.route('/cart/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_cart_item(item_id):
    # Get the current user from the JWT token
    current_user_id = get_jwt_identity()
    
    # Find the user's cart
    cart = Cart.query.filter_by(user_id=current_user_id).first()
    
    if not cart:
        return jsonify({"message": "Cart not found"}), 404
    
    # Find the cart item by ID
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    
    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404
    
    # Remove the cart item from the database
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({"message": "Cart item removed successfully"}), 200


#######################################################################
#getting categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    category_list = [{'id': c.id, 'name': c.name} for c in categories]
    return jsonify(category_list)


#######################################################################
# getting products by category
@app.route('/api/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'message': 'Category not found'}), 404

    products = Product.query.filter_by(category_id=category_id).all()
    product_list = [{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': p.price,
        'image_url': p.image_url,
        'category': {'id': category.id, 'name': category.name}
    } for p in products]

    return jsonify(product_list), 200

###########################################################
# Creating an order

@app.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    # Get the current user from the JWT token
    current_user_id = get_jwt_identity()

    # Find the user's cart
    cart = Cart.query.filter_by(user_id=current_user_id).first()

    if not cart or not cart.items:
        return jsonify({"message": "Cart is empty or not found"}), 404

    # Get billing and shipping information from request
    data = request.get_json()
    billing_address = data.get('billing_address')
    shipping_address = data.get('shipping_address')

    if not billing_address or not shipping_address:
        return jsonify({"message": "Billing and shipping addresses are required"}), 400

    # Calculate the total price
    total_price = cart.total_price

    # Create a new order
    new_order = Order(
        user_id=current_user_id,
        total_price=total_price,
        billing_address=billing_address,
        shipping_address=shipping_address
    )
    db.session.add(new_order)
    db.session.commit()

    # Create order items based on cart items
    for item in cart.items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.session.add(order_item)

    # Clear the cart after the order is placed
    db.session.query(CartItem).filter_by(cart_id=cart.id).delete()
    db.session.commit()

    return jsonify({"message": "Order created successfully", "order_id": new_order.id}), 201

######################################################################
# Route to view all orders (admin only)
@app.route('/orders', methods=['GET'])
@jwt_required()
def view_all_orders():
    # Get the current user from the JWT token
    current_user_id = get_jwt_identity()

    # Find the current user
    current_user = User.query.get(current_user_id)

    if not current_user or current_user.role != 'admin':
        return jsonify({"message": "Access denied. Admins only."}), 403

    # Retrieve all orders
    orders = Order.query.all()

    # Serialize the orders into a list of dictionaries
    orders_data = []
    for order in orders:
        orders_data.append({
            "order_id": order.id,
            "user_id": order.user_id,
            "total_price": order.total_price,
            "status": order.status,
            "billing_address": order.billing_address,
            "shipping_address": order.shipping_address,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity
                } for item in order.items
            ]
        })

    return jsonify({"orders": orders_data}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
