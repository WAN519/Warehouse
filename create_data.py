import mysql.connector
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# MySQL
load_dotenv('config.env')
# get db_config KEY
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_DATABASE'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'ssl_ca': os.environ.get('DB_SSL_CA'),
    'ssl_verify_cert': bool(os.environ.get('DB_SSL_VERIFY_CERT')) == True
}

# Set random seed
random.seed(42)

# Product data
PRODUCTS_DATA = {
    'Food & Beverage': [
        ('Coca-Cola 330ml', 3.50, 'Coca-Cola Company', 365, ['Pepsi', 'Sprite', 'Fanta']),
        ('Mineral Water 550ml', 2.00, 'Aquafina Inc', 540, ['Dasani', 'Evian']),
        ('Mixed Nuts Daily Pack', 15.90, 'Nature Valley', 180, ['Planters', 'Blue Diamond']),
        ('Oreo Cookies Original', 12.50, 'Mondelez International', 365, ['Chips Ahoy', 'Ritz']),
        ('Instant Ramen Noodles', 4.50, 'Nissin Foods', 180, ['Maruchan', 'Top Ramen']),
        ('Fresh Milk 250ml', 3.20, 'Dairy Fresh', 30, ['Horizon Organic', 'Lactaid']),
        ('Rice Crackers Pack', 8.80, 'Want Want Group', 270, ['Kameda', 'Bourbon']),
        ('Dove Chocolate Bar', 18.90, 'Mars Inc', 365, ['Ferrero Rocher', 'Hersheys']),
        ('Lipton Black Tea Bags', 25.00, 'Unilever', 730, ['Twinings', 'Tetley']),
        ('Pringles Chips Original', 11.50, 'Kelloggs', 180, ['Lays', 'Doritos']),
    ],
    'Personal Care': [
        ('Colgate Toothpaste', 15.90, 'Colgate-Palmolive', 1095, ['Crest', 'Sensodyne']),
        ('Head & Shoulders Shampoo 400ml', 39.90, 'Procter & Gamble', 1095, ['Pantene']),
        ('Dove Body Wash', 32.50, 'Unilever', 1095, ['Olay', 'Nivea']),
        ('Safeguard Soap Bar', 6.50, 'Procter & Gamble', 1095, ['Dove Soap']),
        ('Nivea Hand Cream', 18.00, 'Beiersdorf AG', 1095, ['Vaseline']),
        ('Loreal Face Cream', 89.00, 'LOreal Group', 1095, ['Olay']),
        ('Gillette Razor', 45.00, 'Procter & Gamble', 1825, ['Philips Shaver']),
        ('Johnson Baby Powder', 22.00, 'Johnson & Johnson', 1095, ['Pigeon Powder']),
    ],
    'Home & Cleaning': [
        ('Mr. Clean All Purpose Cleaner', 18.50, 'SC Johnson', 1095, ['Lysol', 'Clorox']),
        ('Dettol Disinfectant', 28.90, 'Reckitt Benckiser', 1095, ['Lysol Disinfectant']),
        ('Tide Laundry Detergent', 35.00, 'Procter & Gamble', 730, ['Persil', 'Gain']),
        ('Dawn Dish Soap', 12.50, 'Procter & Gamble', 730, ['Palmolive']),
        ('Scotch-Brite Sponge', 8.90, '3M Company', 1095, ['Heavy Duty Sponge']),
        ('Kleenex Facial Tissue', 25.00, 'Kimberly-Clark', 1095, ['Puffs']),
    ],
    'Electronics': [
        ('Xiaomi Power Bank 10000mAh', 79.00, 'Xiaomi Corp', 730, ['Anker PowerCore']),
        ('Logitech Mouse Wireless', 89.00, 'Logitech', 1095, ['Razer Mouse']),
        ('Edifier Headphones', 199.00, 'Edifier', 730, ['Sony Headphones']),
        ('Philips Power Strip', 45.00, 'Philips Electronics', 1825, ['Belkin']),
        ('SanDisk USB Drive 64GB', 59.00, 'Western Digital', 1825, ['Kingston USB']),
        ('USB-C Cable 6ft', 25.00, 'Anker', 730, ['Belkin Cable']),
    ],
    'Clothing': [
        ('Uniqlo Cotton T-Shirt', 79.00, 'Fast Retailing', 1825, ['H&M Tee']),
        ('Nike Running Shoes', 299.00, 'Nike Inc', 1825, ['Adidas Sneakers']),
        ('Thermal Underwear Set', 99.00, 'Hanes', 1825, ['Under Armour']),
        ('Levis Denim Jeans', 159.00, 'Levi Strauss', 1825, ['Wrangler']),
        ('Cotton Socks 5-Pack', 29.00, 'Hanes', 1095, ['Gold Toe']),
    ],
    'Baby Products': [
        ('Pampers Diapers Size 3', 129.00, 'Procter & Gamble', 1095, ['Huggies']),
        ('Philips Avent Baby Bottle', 89.00, 'Philips', 1825, ['Dr Browns']),
        ('Enfamil Infant Formula 900g', 298.00, 'Mead Johnson', 730, ['Similac']),
        ('Huggies Baby Wipes', 35.00, 'Kimberly-Clark', 1095, ['Pampers Wipes']),
    ],
    'Sports & Outdoors': [
        ('Yoga Mat Non-Slip', 59.00, 'Gaiam', 1825, ['Manduka']),
        ('Spalding Basketball', 89.00, 'Spalding', 1095, ['Wilson Basketball']),
        ('Sports Backpack 30L', 129.00, 'Under Armour', 1825, ['Nike Backpack']),
        ('Swimming Goggles', 39.00, 'Speedo', 1095, ['TYR']),
    ],
    'Stationery': [
        ('Ballpoint Pen Blue 10-Pack', 2.50, 'Bic', 1095, ['Pilot Pens']),
        ('Spiral Notebook A5', 8.50, 'Mead', 1095, ['Five Star']),
        ('Post-it Notes 3x3', 12.00, '3M Company', 1095, ['Highland Notes']),
        ('Correction Tape', 6.50, 'Tombow', 1095, ['Bic Wite-Out']),
    ],
}


def generate_id(prefix, index):
    return f"{prefix}{str(index).zfill(8)}"


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def insert_users(cursor, count=100):
    print(f"Inserting {count} users...")
    first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph',
                   'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                  'Rodriguez', 'Martinez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore']

    users = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 11, 1)

    for i in range(count):
        user_id = generate_id('U', i + 1)
        nickname = f"{random.choice(first_names)}{random.choice(last_names)}{random.randint(100, 999)}"
        register_time = random_date(start_date, end_date)
        users.append((user_id, nickname, register_time))

    cursor.executemany(
        "INSERT INTO users (user_id, nickname, register_time) VALUES (%s, %s, %s)",
        users
    )
    print(f"✓ Inserted {len(users)} users")
    return users


def insert_warehouses(cursor):
    print("Inserting warehouses...")
    locations = [
        '1500 Logistics Pkwy, Seattle WA',
        '2800 Distribution Dr, Los Angeles CA',
        '4200 Warehouse Rd, Chicago IL',
        '3600 Fulfillment Blvd, Dallas TX',
        '5100 Commerce Way, Atlanta GA',
        '2200 Industrial Ave, Phoenix AZ',
        '3900 Supply Chain Dr, New York NY',
        '4800 Shipping Ln, Miami FL'
    ]

    warehouses = []
    for i, loc in enumerate(locations):
        warehouse_id = generate_id('W', i + 1)
        warehouses.append((warehouse_id, loc))

    cursor.executemany(
        "INSERT INTO warehouses (warehouse_id, location) VALUES (%s, %s)",
        warehouses
    )
    print(f"✓ Inserted {len(warehouses)} warehouses")
    return warehouses


def insert_products(cursor, count=500):
    print(f"Inserting {count} products...")
    products = []
    product_idx = 1

    for category, items in PRODUCTS_DATA.items():
        category_count = int(count * len(items) / sum(len(v) for v in PRODUCTS_DATA.values()))

        for base_product, base_price, manufacturer, shelf_life, variants in items:
            for _ in range(max(1, category_count // len(items))):
                product_id = generate_id('P', product_idx)

                if random.random() < 0.7:
                    product_name = base_product
                    price = base_price * random.uniform(0.9, 1.1)
                else:
                    product_name = random.choice(variants) if variants else base_product
                    price = base_price * random.uniform(0.85, 1.15)

                batch_number = f"B{datetime.now().year}{random.randint(1, 12):02d}{random.randint(1, 28):02d}{random.randint(1000, 9999)}"

                # 根据你的表结构: product_id, product_name, price, manufacturer, shelf_life, batch_number
                # 没有 type 字段
                products.append((product_id, product_name, round(price, 2),
                                 manufacturer, shelf_life, batch_number))
                product_idx += 1

                if product_idx > count:
                    break
            if product_idx > count:
                break
        if product_idx > count:
            break

    cursor.executemany(
        "INSERT INTO products (product_id, product_name, price, manufacturer, shelf_life, batch_number) VALUES (%s, %s, %s, %s, %s, %s)",
        products
    )
    print(f"✓ Inserted {len(products)} products")
    return products


def insert_suppliers(cursor, count=20):
    print(f"Inserting {count} suppliers...")
    company_prefixes = ['Global', 'Premier', 'United', 'Superior', 'Elite', 'Prime', 'Alpha',
                        'Omega', 'Mega', 'Dynamic', 'Strategic', 'Advanced']
    company_types = ['Trading Co', 'Supply Chain Inc', 'Wholesale Corp', 'Distribution LLC',
                     'Logistics Group', 'Commerce Ltd']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
              'San Antonio', 'Seattle', 'Boston', 'Denver']
    streets = ['Main St', 'Oak Ave', 'Maple Dr', 'Park Ave', 'Market St']

    suppliers = []
    for i in range(count):
        supplier_id = generate_id('S', i + 1)
        supplier_name = f"{random.choice(company_prefixes)} {random.choice(company_types)}"
        city = random.choice(cities)
        street = random.choice(streets)
        address = f"{random.randint(100, 9999)} {street}, {city}"
        star = random.randint(3, 5)
        duration = random.randint(12, 120)
        status = random.choice(['active', 'active', 'active', 'inactive'])
        suppliers.append((supplier_id, supplier_name, address, star, duration, status))

    cursor.executemany(
        "INSERT INTO suppliers (supplier_id, supplier_name, address, star, duration, status) VALUES (%s, %s, %s, %s, %s, %s)",
        suppliers
    )
    print(f"✓ Inserted {len(suppliers)} suppliers")
    return suppliers


def insert_store_records(cursor, products, warehouses):
    print("Inserting store records...")
    records = []

    for product in products:
        num_warehouses = random.randint(1, min(3, len(warehouses)))
        selected_warehouses = random.sample(warehouses, num_warehouses)

        for warehouse in selected_warehouses:
            quantity = random.choices(
                [random.randint(5, 30), random.randint(50, 200), random.randint(300, 800)],
                weights=[0.5, 0.3, 0.2]
            )[0]
            records.append((warehouse[0], product[0], quantity))

    cursor.executemany(
        "INSERT INTO store_records (warehouse_id, product_id, storequantity) VALUES (%s, %s, %s)",
        records
    )
    print(f"✓ Inserted {len(records)} store records")
    return records


def insert_orders(cursor, users, store_records, order_count=500):
    print(f"Inserting {order_count} orders...")
    orders = []
    informs = []

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 11, 27)

    for i in range(order_count):
        order_id = f"ORD{datetime.now().year}{str(i + 1).zfill(10)}"
        user = random.choice(users)
        order_time = random_date(start_date, end_date)
        orders.append((order_id, user[0], order_time))

        num_items = random.randint(1, 3)
        order_items = random.sample(store_records, num_items)

        for item in order_items:
            warehouse_id, product_id, store_qty = item
            order_qty = min(random.randint(1, 5), store_qty)
            status = random.choice(['pending', 'shipped', 'shipped', 'delivered', 'delivered', 'delivered'])
            informs.append((order_id, product_id, warehouse_id, order_qty, status))

    cursor.executemany(
        "INSERT INTO orders (order_id, user_id, order_time) VALUES (%s, %s, %s)",
        orders
    )
    print(f"✓ Inserted {len(orders)} orders")

    cursor.executemany(
        "INSERT INTO inform (order_id, product_id, warehouse_id, orderquantity, status) VALUES (%s, %s, %s, %s, %s)",
        informs
    )
    print(f"✓ Inserted {len(informs)} order items")

    return orders, informs


def insert_good_supply(cursor, suppliers, store_records):
    print("Inserting supply records...")
    supplies = []

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 11, 1)

    active_suppliers = [s for s in suppliers if s[5] == 'active']

    for supplier in active_suppliers:
        num_supplies = random.randint(10, 20)
        selected_records = random.sample(store_records, min(num_supplies, len(store_records)))

        for record in selected_records:
            warehouse_id, product_id, _ = record
            quantity = random.randint(50, 500)
            supply_time = random_date(start_date, end_date)
            supplies.append((supplier[0], product_id, warehouse_id, quantity, supply_time))

    supplies = list(set(supplies))

    cursor.executemany(
        "INSERT INTO good_supply (supplier_id, product_id, warehouse_id, quantity, supply_time) VALUES (%s, %s, %s, %s, %s)",
        supplies
    )
    print(f"✓ Inserted {len(supplies)} supply records")


def insert_logistics(cursor, orders):
    print("Inserting logistics data...")
    express_companies = ['FedEx', 'UPS', 'DHL Express', 'USPS Priority', 'Amazon Logistics']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Seattle']
    streets = ['Main St', 'Oak Ave', 'Maple Dr', 'Park Blvd']

    logistics_records = []
    shipping_records = []
    delivery_records = []

    for i, order in enumerate(orders):
        logistics_id = generate_id('L', i + 1)
        order_id = order[0]
        order_time = order[2]
        express_company = random.choice(express_companies)
        logistics_status = random.choice(['in_transit', 'in_transit', 'delivered', 'delivered', 'delivered'])

        logistics_records.append((logistics_id, order_id, express_company, logistics_status))

        shipping_time = order_time + timedelta(hours=random.randint(2, 48))
        city = random.choice(cities)
        street = random.choice(streets)
        shipping_address = f"{random.randint(100, 9999)} {street}, {city}"
        shipping_records.append((logistics_id, shipping_time, shipping_address))

        if logistics_status == 'delivered':
            delivery_time = shipping_time + timedelta(days=random.randint(1, 5))
            delivery_records.append((logistics_id, delivery_time, shipping_address))

    cursor.executemany(
        "INSERT INTO logistics (logistics_id, order_id, express_company, logistics_status) VALUES (%s, %s, %s, %s)",
        logistics_records
    )
    print(f"✓ Inserted {len(logistics_records)} logistics records")

    cursor.executemany(
        "INSERT INTO shipping_product (logistics_id, shipping_time, shipping_address) VALUES (%s, %s, %s)",
        shipping_records
    )
    print(f"✓ Inserted {len(shipping_records)} shipping records")

    if delivery_records:
        cursor.executemany(
            "INSERT INTO delivery_product (logistics_id, delivery_time, delivery_address) VALUES (%s, %s, %s)",
            delivery_records
        )
        print(f"✓ Inserted {len(delivery_records)} delivery records")


def main():
    print("=" * 60)
    print("Starting database population...")
    print("=" * 60)

    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        print(f"✓ Connected to database: {DB_CONFIG['database']}")

        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=0")

        # Insert data in correct order
        users = insert_users(cursor, 100)
        warehouses = insert_warehouses(cursor)
        products = insert_products(cursor, 500)
        suppliers = insert_suppliers(cursor, 20)
        store_records = insert_store_records(cursor, products, warehouses)
        orders, informs = insert_orders(cursor, users, store_records, 500)
        insert_good_supply(cursor, suppliers, store_records)
        insert_logistics(cursor, orders)

        # Enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS=1")

        # Commit transaction
        conn.commit()

        print("=" * 60)
        print("✓ All data inserted successfully!")
        print("=" * 60)

    except mysql.connector.Error as err:
        print(f"✗ Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
        print("✓ Database connection closed")


if __name__ == "__main__":
    main()