from config import db, app
from faker import Faker
from models import User, Category, Product, Order, Cart, CartItem, OrderItem
from flask_bcrypt import Bcrypt

# Initialize Bcrypt
bcrypt = Bcrypt()
faker = Faker()

# Ensure all operations are performed within the app context
with app.app_context():
    print("Starting seed...")
    # Drop all tables and recreate them
    print("Dropping all tables...")
    db.drop_all()
    print("All tables dropped successfully.")

    print("Creating tables...")
    db.create_all()
    print("Tables created successfully.")

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
        hashed_password = bcrypt.generate_password_hash('customerpassword').decode('utf-8')
        user = User(
            username=f'customer{_}',
            email=f'customer{_}@example.com',
            password=hashed_password,
            role='customer'
        )
        db.session.add(user)

    db.session.commit()

    # Seed products with hardcoded values
    products_data = {
        'Denims': [
            {'name': 'Classic Jeans', 'description': 'A timeless pair of classic jeans.', 'image_url': 'https://m.media-amazon.com/images/I/715K4AhGLZS._AC_UY1000_.jpg'},
            {'name': 'Skinny Jeans', 'description': 'Skinny fit jeans that hug your figure.', 'image_url': 'https://target.scene7.com/is/image/Target/GUEST_6fbee1bf-c3a1-46fb-8a01-90b027e1cdb6?wid=488&hei=488&fmt=pjpeg'},
            {'name': 'Ripped Denim', 'description': 'Stylish ripped denim jeans.', 'image_url': 'https://cdn11.bigcommerce.com/s-h56o4umii7/images/stencil/1280x1280/products/51318/531393/0fdea4989c76bc6e__19613.1681943527.jpg?c=1'},
            {'name': 'High-Waisted Jeans', 'description': 'High-waisted jeans for a retro look.', 'image_url': 'https://hips.hearstapps.com/hmg-prod/images/best-high-waisted-jeans-665a109827b88.jpg?crop=0.486xw:0.966xh;0.00340xw,0.00338xh&resize=1200:*'},
            {'name': 'Ripped Denim', 'description': 'Stylish ripped denim jeans.', 'image_url': 'https://cdn11.bigcommerce.com/s-h56o4umii7/images/stencil/1280x1280/products/51318/531393/0fdea4989c76bc6e__19613.1681943527.jpg?c=1'},
            {'name': 'Classic Jeans', 'description': 'A timeless pair of classic jeans.', 'image_url': 'https://m.media-amazon.com/images/I/715K4AhGLZS._AC_UY1000_.jpg'},
            {'name': 'Classic Jeans', 'description': 'A timeless pair of classic jeans.', 'image_url': 'https://m.media-amazon.com/images/I/715K4AhGLZS._AC_UY1000_.jpg'},
            {'name': 'Skinny Jeans', 'description': 'Skinny fit jeans that hug your figure.', 'image_url': 'https://target.scene7.com/is/image/Target/GUEST_6fbee1bf-c3a1-46fb-8a01-90b027e1cdb6?wid=488&hei=488&fmt=pjpeg'},
            {'name': 'Ripped Denim', 'description': 'Stylish ripped denim jeans.', 'image_url': 'https://cdn11.bigcommerce.com/s-h56o4umii7/images/stencil/1280x1280/products/51318/531393/0fdea4989c76bc6e__19613.1681943527.jpg?c=1'},
            {'name': 'High-Waisted Jeans', 'description': 'High-waisted jeans for a retro look.', 'image_url': 'https://hips.hearstapps.com/hmg-prod/images/best-high-waisted-jeans-665a109827b88.jpg?crop=0.486xw:0.966xh;0.00340xw,0.00338xh&resize=1200:*'},
            {'name': 'Ripped Denim', 'description': 'Stylish ripped denim jeans.', 'image_url': 'https://cdn11.bigcommerce.com/s-h56o4umii7/images/stencil/1280x1280/products/51318/531393/0fdea4989c76bc6e__19613.1681943527.jpg?c=1'},
            {'name': 'Classic Jeans', 'description': 'A timeless pair of classic jeans.', 'image_url': 'https://m.media-amazon.com/images/I/715K4AhGLZS._AC_UY1000_.jpg'}

        ],
        'Dresses': [
            {'name': 'Floral Dress', 'description': 'A beautiful floral print dress.', 'image_url': 'https://example.com/floral-dress.jpg'},
            {'name': 'Cocktail Dress', 'description': 'Perfect for evening events.', 'image_url': 'https://example.com/cocktail-dress.jpg'},
            {'name': 'Maxi Dress', 'description': 'A flowing maxi dress.', 'image_url': 'https://example.com/maxi-dress.jpg'},
            {'name': 'Summer Dress', 'description': 'Light and breezy for summer.', 'image_url': 'https://example.com/summer-dress.jpg'}
        ],
        'Tops': [
            {'name': 'Graphic Tee', 'description': 'A trendy graphic tee.', 'image_url': 'https://example.com/graphic-tee.jpg'},
            {'name': 'Crop Top', 'description': 'A chic crop top.', 'image_url': 'https://example.com/crop-top.jpg'},
            {'name': 'Blouse', 'description': 'Elegant and classy blouse.', 'image_url': 'https://example.com/blouse.jpg'},
            {'name': 'Tank Top', 'description': 'Casual and comfy tank top.', 'image_url': 'https://example.com/tank-top.jpg'}
        ],
        'Bottoms': [
            {'name': 'Chinos', 'description': 'Comfortable chinos for all-day wear.', 'image_url': 'https://example.com/chinos.jpg'},
            {'name': 'Culottes', 'description': 'Wide-legged culottes.', 'image_url': 'https://example.com/culottes.jpg'},
            {'name': 'Shorts', 'description': 'Perfect for summer days.', 'image_url': 'https://example.com/shorts.jpg'},
            {'name': 'Leggings', 'description': 'Versatile and comfortable leggings.', 'image_url': 'https://example.com/leggings.jpg'}
        ],
        'Shoes': [
            {'name': 'Sneakers', 'description': 'Casual sneakers for everyday wear.', 'image_url': 'https://example.com/sneakers.jpg'},
            {'name': 'Heels', 'description': 'Elegant heels for special occasions.', 'image_url': 'https://example.com/heels.jpg'},
            {'name': 'Boots', 'description': 'Sturdy boots for all weather.', 'image_url': 'https://example.com/boots.jpg'},
            {'name': 'Sandals', 'description': 'Open-toe sandals for summer.', 'image_url': 'https://example.com/sandals.jpg'}
        ],
        'Matching Sets': [
            {'name': 'Two-Piece Set', 'description': 'A stylish two-piece set.', 'image_url': 'https://example.com/two-piece-set.jpg'},
            {'name': 'Suit Set', 'description': 'Formal suit set for business.', 'image_url': 'https://example.com/suit-set.jpg'},
            {'name': 'Jogger Set', 'description': 'Comfortable jogger set.', 'image_url': 'https://example.com/jogger-set.jpg'},
            {'name': 'Lounge Set', 'description': 'Perfect for lounging at home.', 'image_url': 'https://example.com/lounge-set.jpg'}
        ]
    }

    for category_name, products in products_data.items():
        for product_data in products:
            product = Product(
                name=product_data['name'],
                description=product_data['description'],
                price=round(faker.random_number(digits=2) + faker.random.random(), 2),
                image_url=product_data['image_url'],
                category_id=categories[category_name].id
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
