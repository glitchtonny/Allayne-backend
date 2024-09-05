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
            {'name': 'Mom Jeans', 'description': 'A timeless pair of classic jeans.', 'image_url': 'https://img.abercrombie.com/is/image/anf/KIC_155-3423-3228-278_model1.jpg?policy=product-large'},
            {'name': 'Solid flared Jeans', 'description': 'A timeless pair of classic jeans.', 'image_url': 'https://ke.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/04/0579671/1.jpg?9294'},
            {'name': 'Baggy Jeans', 'description': 'Skinny fit jeans that hug your figure.', 'image_url': 'https://culturedstore.in/wp-content/uploads/2024/02/Laser-Rush-women-baggy-jeans-1-1-1.jpg'},
            {'name': 'Cigarette Denim', 'description': 'Stylish ripped denim jeans.', 'image_url': 'https://www.gapcanada.ca/webcontent/0017/589/589/cn17589589.jpg'},
            {'name': 'Boyfriend Jeans', 'description': 'High-waisted jeans for a retro look.', 'image_url': 'https://m.media-amazon.com/images/I/71vzzS4IRYL._AC_UY1100_.jpg'},
            {'name': 'Straight Denim', 'description': 'Stylish ripped denim jeans.', 'image_url': 'https://www.madish.in/cdn/shop/products/the-90s-straight-high-waist-jeans-jeans-madish-496096.jpg?v=1715274428&width=800'},
            {'name': 'Wide leg Jeans', 'description': 'A timeless pair of classic jeans.', 'image_url': 'https://offduty.in/cdn/shop/collections/WIDE_LEG.png?v=1677662662'}

        ],
        'Dresses': [
            {'name': 'Floral Dress', 'description': 'A beautiful floral print dress.', 'image_url': 'https://www.houseofdeevas.co.za/wp-content/uploads/2021/11/Dress-2.jpg'},
            {'name': 'Cocktail Dress', 'description': 'Perfect for evening events.', 'image_url': 'https://i.ebayimg.com/images/g/T-YAAOSwshpjV25x/s-l1200.jpg'},
            {'name': 'Maxi Dress', 'description': 'A flowing maxi dress.', 'image_url': 'https://m.media-amazon.com/images/I/71co2U3QUgL._AC_UY350_.jpg'},
            {'name': 'Summer Dress', 'description': 'Light and breezy for summer.', 'image_url': 'https://m.media-amazon.com/images/I/71qZP4lq5RL._AC_UY1000_.jpg'},
            {'name': 'Mini Dress', 'description': 'A beautiful floral print dress.', 'image_url': 'https://storage.googleapis.com/windsor-cms/media/2023/01/eb6599f9-magenta-faux-suede-mini-skirt.jpg'},
            {'name': 'Camisole Dress', 'description': 'Perfect for evening events.', 'image_url': 'https://m.media-amazon.com/images/I/81XAb2Vy9VL.jpg'},
            {'name': 'Cocoon Dress', 'description': 'A flowing maxi dress.', 'image_url': 'https://fellahamilton.com.au/cdn/shop/products/a7201sz.463-1-dress-lipstick.jpg?v=1700832589'},
            {'name': 'Corset Dress', 'description': 'Light and breezy for summer.', 'image_url': 'https://www.noodzboutique.com.au/cdn/shop/files/Crystalcorsetsatingowninburgundy3.jpg?v=1688530054&width=1200'},
            {'name': 'Mini Dress', 'description': 'A beautiful floral print dress.', 'image_url': 'https://storage.googleapis.com/windsor-cms/media/2023/01/eb6599f9-magenta-faux-suede-mini-skirt.jpg'},
            {'name': 'Camisole Dress', 'description': 'Perfect for evening events.', 'image_url': 'https://m.media-amazon.com/images/I/81XAb2Vy9VL.jpg'},
            {'name': 'Cocoon Dress', 'description': 'A flowing maxi dress.', 'image_url': 'https://fellahamilton.com.au/cdn/shop/products/a7201sz.463-1-dress-lipstick.jpg?v=1700832589'},
            {'name': 'Corset Dress', 'description': 'Light and breezy for summer.', 'image_url': 'https://www.noodzboutique.com.au/cdn/shop/files/Crystalcorsetsatingowninburgundy3.jpg?v=1688530054&width=1200'}
        ],
        'Tops': [
            {'name': 'Graphic Tee', 'description': 'A trendy graphic tee.', 'image_url': 'https://blackhare.ca/cdn/shop/products/black-ladies-bee-783107.jpg?v=1709956322&width=1445'},
            {'name': 'Crop Top', 'description': 'A chic crop top.', 'image_url': 'https://i5.walmartimages.com/seo/HTNBO-Cute-Crop-Tops-for-Women-Summer-Fall-Trends-Lattern-Long-Sleeve-Floral-Casual-Cami-Shirts_6e749edd-cd52-4326-99e7-e54640fe5728.ed2d0bd6f10b6d65ddb009d77488fd48.jpeg'},
            {'name': 'Blouse', 'description': 'Elegant and classy blouse.', 'image_url': 'https://cdn.pomelofashion.com/img/p/5/7/3/3/5/0/573350.jpg?auto=compress,format&fm=webp,jpg,png&w=1081.5&h=1438.5'},
            {'name': 'Tank Top', 'description': 'Casual and comfy tank top.', 'image_url': 'https://images.napali.app/global/roxy-products/all/default/large/erjzt05351_roxy,w_kvj0_frt1.jpg'},
            {'name': 'Bralette Top', 'description': 'A trendy graphic tee.', 'image_url': 'https://m.media-amazon.com/images/I/81HXUdEz4tL._AC_UY1000_.jpg'},
            {'name': 'Tube Top', 'description': 'A chic crop top.', 'image_url': 'https://i5.walmartimages.com/asr/3a2d5200-1af3-4749-839e-c0e617264d3b.87a2a50a78e3f2557480f11ee41bccff.png'},
            {'name': 'Ethnic', 'description': 'Elegant and classy blouse.', 'image_url': 'https://adn-static1.nykaa.com/nykdesignstudio-images/pub/media/catalog/product/f/3/f314402SS22-W-TP01_1.jpg?tr=w-512'},
            {'name': 'Cape Top', 'description': 'Casual and comfy tank top.', 'image_url': 'https://n.nordstrommedia.com/id/sr3/3046e66f-c0a8-4e49-8f24-ee274216b512.jpeg?h=365&w=240&dpr=2'},
            {'name': 'Peplum Top', 'description': 'A trendy graphic tee.', 'image_url': 'https://images-cdn.ubuy.com.sa/63ab9fd103595240b17d400b-shein-women-39-s-plus-ruffle-tie-front.jpg'},
            {'name': 'Ruffle Top', 'description': 'A chic crop top.', 'image_url': 'https://media.boohoo.com/i/boohoo/pzz66650_black_xl?w=900&qlt=default&fmt.jp2.qlt=70&fmt=auto&sm=fit'},
            {'name': 'Wrap Tops', 'description': 'Elegant and classy blouse.', 'image_url': 'https://m.media-amazon.com/images/I/618s88c5EGL._AC_UY1100_.jpg'},
            {'name': 'Tunic Top', 'description': 'Casual and comfy tank top.', 'image_url': 'https://i5.walmartimages.com/asr/a4024d46-f9d4-4f52-9459-e0759f7c82fc.6cce4de2da821ddd2d8f9efa0dd9e995.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF'}
        ],
        'Bottoms': [
            {'name': 'Chinos', 'description': 'Comfortable chinos for all-day wear.', 'image_url': 'https://images.express.com/is/image/expressfashion/0092_07452358_0557_f001?cache=on&wid=480&fmt=jpeg&qlt=85,1&resmode=sharp2&op_usm=1,1,5,0&defaultImage=Photo-Coming-Soon'},
            {'name': 'Culottes', 'description': 'Wide-legged culottes.', 'image_url': 'https://ke.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/05/1297941/1.jpg?2125'},
            {'name': 'Shorts', 'description': 'Perfect for summer days.', 'image_url': 'https://www.ikojn.com/cdn/shop/files/dolce-shorts-in-tan-ikojn-1_2048x.jpg?v=1721224081'},
            {'name': 'Leggings', 'description': 'Versatile and comfortable leggings.', 'image_url': 'https://shopzetu.com/cdn/shop/products/11-10-websiteshoot-07486-786678_1000x.jpg?v=1707910903'},
            {'name': 'Palazzo', 'description': 'Comfortable chinos for all-day wear.', 'image_url': 'https://shopzetu.com/cdn/shop/products/JolAnuYXPu-110623_400x.jpg?v=1707909810'},
            {'name': 'Capri', 'description': 'Wide-legged culottes.', 'image_url': 'https://i5.walmartimages.com/seo/Capri-Pants-for-Women-Cotton-Linen-Plus-Size-Cargo-Pants-Capris-Elastic-High-Waisted-3-4-Slacks-with-Multi-Pockets-4X-Large-Black_ff09e67a-4320-4602-aedd-0ac866c02596.aee72944d52d64daa454628bc4a2c7b2.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF'},
            {'name': 'Flare', 'description': 'Perfect for summer days.', 'image_url': 'https://img.fruugo.com/product/4/52/371671524_max.jpg'},
            {'name': 'Bootcut', 'description': 'Versatile and comfortable leggings.', 'image_url': 'https://i.pinimg.com/1200x/21/ce/a6/21cea6e1b0aa5bc51ded9644257667cb.jpg'},
            {'name': 'Sweatpants', 'description': 'Comfortable chinos for all-day wear.', 'image_url': 'https://static.nike.com/a/images/c_limit,w_592,f_auto/t_product_v1/e4d52036-f404-483e-8121-4aba4d978e08/sportswear-phoenix-fleece-high-waisted-oversized-tracksuit-bottoms-00TZkD.png'},
            {'name': 'Leather', 'description': 'Wide-legged culottes.', 'image_url': 'https://i.etsystatic.com/13549429/r/il/d1ebbd/2886228391/il_fullxfull.2886228391_gmum.jpg'},
            {'name': 'Ankle', 'description': 'Perfect for summer days.', 'image_url': 'https://cdn.sixtyandme.com/wp-content/uploads/2021/05/Chicos-2.png'},
            {'name': 'Dress', 'description': 'Versatile and comfortable leggings.', 'image_url': 'https://m.media-amazon.com/images/I/71sO1pG240L._AC_UY1000_.jpg'}
        ],
        'Shoes': [
            {'name': 'Sneakers', 'description': 'Casual sneakers for everyday wear.', 'image_url': 'https://ke.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/07/7657451/1.jpg?8282'},
            {'name': 'Heels', 'description': 'Elegant heels for special occasions.', 'image_url': 'https://files.sophie.co.ke/2022/08/1834905091_1666-1_7944.jpg'},
            {'name': 'Boots', 'description': 'Sturdy boots for all weather.', 'image_url': 'https://ke.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/39/2833711/2.jpg?9753'},
            {'name': 'Sandals', 'description': 'Open-toe sandals for summer.', 'image_url': 'https://img.fruugo.com/product/8/33/234475338_max.jpg'},
            {'name': 'Low heels', 'description': 'Casual sneakers for everyday wear.', 'image_url': 'https://www.travelandleisure.com/thmb/9Dzlyqe3ue0Cfdgi0_9R-XgJv6g=/fit-in/1500x1000/filters:no_upscale():max_bytes(150000):strip_icc()/DREAM-PAIRS-Womens-Chunk-Low-Heel-Pump-Sandals-eaaface4df364c6fa29983f644d8e28d.jpg'},
            {'name': 'Flats', 'description': 'Elegant heels for special occasions.', 'image_url': 'https://rikeys.co.ke/images/resized_IMG-20200524-WA0013.jpg'},
            {'name': 'loafer', 'description': 'Sturdy boots for all weather.', 'image_url': 'https://ke.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/40/5935051/1.jpg?2439'},
            {'name': 'Abaca', 'description': 'Open-toe sandals for summer.', 'image_url': 'https://i5.walmartimages.com/seo/Slippers-For-Women-Girls-Flat-Casual-Sandals-Straw-Linen-Bottom-Beach-Shoes-Target-Dressy-Womens-Size-8-Dress_0eb6cd07-fc98-4127-9e91-1cd73ec53272.abbdebd27f1d709fe2ba6afbe295084e.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF'},
            {'name': 'Clog', 'description': 'Casual sneakers for everyday wear.', 'image_url': 'https://m.media-amazon.com/images/I/61QqAK1h9SL._AC_UY300_.jpg'},
            {'name': 'Stilettos', 'description': 'Elegant heels for special occasions.', 'image_url': 'https://m.media-amazon.com/images/I/71l7mVKoyZL._AC_UF894,1000_QL80_.jpg'},
            {'name': 'wedges', 'description': 'Sturdy boots for all weather.', 'image_url': 'https://ke.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/32/9391251/1.jpg?9155'},
            {'name': 'Espadrille', 'description': 'Open-toe sandals for summer.', 'image_url': 'https://www.viscata.com/cdn/shop/products/Espadrilles-Flats-Women-Canvas-Black-Barceloneta-2_4735762b-b45f-4dd1-946c-697699b933dd.jpg?v=1724229166&width=1445'}
        ],
        'Matching Sets': [
            {'name': 'Two-Piece Set', 'description': 'A stylish two-piece set.', 'image_url': 'https://ae01.alicdn.com/kf/Sf4443bac50d4484390f01994c7862d0c4/Summer-Two-Piece-Set-Women-Fashion-Printed-Boho-Crop-Top-High-Waist-Pants-Suit-Women-s.jpg'},
            {'name': 'Suit Set', 'description': 'Formal suit set for business.', 'image_url': 'https://www.hollywoodreporter.com/wp-content/uploads/2022/09/HM.jpeg'},
            {'name': 'Jogger Set', 'description': 'Comfortable jogger set.', 'image_url': 'https://www.usmagazine.com/wp-content/uploads/2020/10/ZESICA-Womens-Long-Sleeve-Crop-Top-and-Pants-2-Piece-Jogger-Set-2.png?w=930&quality=86&strip=all'},
            {'name': 'Lounge Set', 'description': 'Perfect for lounging at home.', 'image_url': 'https://media.boohoo.com/i/boohoo/gzz47933_stone_xl/female-stone-tall-soft-rib-collar-tee-wide-leg-trouser-lounge-set/?w=900&qlt=default&fmt.jp2.qlt=70&fmt=auto&sm=fit'},
            {'name': 'Plus size', 'description': 'A stylish two-piece set.', 'image_url': 'https://thepinkmoon.in/cdn/shop/files/CORD_10_BLKLN_9.jpg?v=1720182273&width=1080'},
            {'name': 'Streetwear sets', 'description': 'Formal suit set for business.', 'image_url': 'https://i.pinimg.com/736x/61/8a/bd/618abd50eabfe3424602a8927749559d.jpg'},
            {'name': 'Summer set', 'description': 'Comfortable jogger set.', 'image_url': 'https://i.pinimg.com/736x/a6/4a/9a/a64a9ad04c8afc6eda983caa5ecbf43d.jpg'},
            {'name': 'Going out set', 'description': 'A stylish two-piece set.', 'image_url': 'https://styledup.co.uk/cdn/shop/files/black-drape-slinky-crop-top-and-flares-going-out-two-piece-styledup-fashion.jpg?v=1703502729'},
            {'name': 'Party Set', 'description': 'Formal suit set for business.', 'image_url': 'https://ke.jumia.is/unsafe/fit-in/500x500/filters:fill(white)/product/59/4582031/1.jpg?1812'},
            {'name': 'Casual Set', 'description': 'Comfortable jogger set.', 'image_url': 'https://www.lestyleparfait.co.ke/cdn/shop/files/casual-patchwork-matching-women-s-clothing-set-lestyleparfait-kenya-clothing-set-1.jpg?v=1703684253'},
            {'name': 'Formal Set', 'description': 'Perfect for lounging at home.', 'image_url': 'https://files.sophie.co.ke/2023/06/757084102_2749-1_3448.jpg'},
            {'name': 'Pajamas Set', 'description': 'Perfect for lounging at home.', 'image_url': 'https://i5.walmartimages.com/seo/PATLOLLAV-Womens-Clearance-Women-Silk-Satin-Pajamas-Set-Two-Piece-Sleepwear-Loungewear-Button-Down-Sets_eb1a5fe3-9c30-46e5-bc21-52def550fc4a_1.c8e3408d8ebdc01fbc85e20e8f963991.jpeg?odnHeight=768&odnWidth=768&odnBg=FFFFFF'},

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
                user_id=user.id,
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
                cart_id=cart.id,
                total_price= 500,
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
