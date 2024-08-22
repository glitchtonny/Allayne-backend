from faker import Faker
from config import db, app
from models import User, Category, Product, Order, Cart, CartItem, OrderItem
from flask_bcrypt import Bcrypt

# Initialize Faker
faker = Faker()

# Initialize Bcrypt
bcrypt = Bcrypt()

# Ensure all operations are performed within the app context
with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Seed categories
    categories = {
        'Denims': None,
        'Dresses': None,
        'Tops': None,
        'Bottoms': None,
        'Shoes': None,
        'Matching Sets': None
    }

    for category_name in categories:
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()  # Commit to get the ID for the category
        categories[category_name] = category

    # Seed the admin user
    admin = User(
        username='admin',
        email='admin@example.com',
        password=bcrypt.generate_password_hash('adminpassword').decode('utf-8'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()

    # Seed customer users
    for _ in range(10):
        hashed_password = bcrypt.generate_password_hash(faker.password()).decode('utf-8')
        user = User(
            username=faker.user_name(),
            email=faker.email(),
            password=hashed_password,
            role='customer'
        )
        db.session.add(user)

    db.session.commit()

    # Seed products
    for category_name, category in categories.items():
        for _ in range(10):
            product = Product(
                name=faker.catch_phrase(),
                description=faker.text(),
                price=round(faker.random_number(digits=2) + faker.random.random(), 2),
                image_url=faker.image_url(width=640, height=480),
                category_id=category.id
            )
            db.session.add(product)

    db.session.commit()

    # Seed carts
    customers = User.query.filter_by(role='customer').all()
    for user in customers:
        cart = Cart(user_id=user.id)
        db.session.add(cart)

    db.session.commit()

    # Seed cart items
    products = Product.query.all()
    for user in customers:
        cart = Cart.query.filter_by(user_id=user.id).first()
        for _ in range(5):
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=faker.random_element(elements=products).id,
                quantity=faker.random_int(min=1, max=3)
            )
            db.session.add(cart_item)

    db.session.commit()

    # Seed orders
    for user in customers:
        for _ in range(3):
            order = Order(
                user_id=user.id,
                billing_address=faker.address(),
                shipping_address=faker.address(),
                status=faker.random_element(elements=('Pending', 'Shipped', 'Delivered'))
            )
            db.session.add(order)
            db.session.commit()

            # Seed order items
            for _ in range(2):
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=faker.random_element(elements=products).id,
                    quantity=faker.random_int(min=1, max=5)
                )
                db.session.add(order_item)

    db.session.commit()

    print("Seeding completed successfully!")

