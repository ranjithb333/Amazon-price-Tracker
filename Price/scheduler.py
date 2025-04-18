import mysql.connector
from web_scraper import get_amazon_price
import time

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='price_tracker'
)
cursor = conn.cursor()

def update_prices():
    cursor.execute("SELECT id, product_name FROM products")
    products = cursor.fetchall()

    for product_id, product_name in products:
        title, price, url = get_amazon_price(product_name)

        if not price:
            print("Skipping {}, price not found.".format(product_name))
            continue 

        price_value = price.replace('Rs.', '').replace(',', '').strip()
        cursor.execute("SELECT id FROM products WHERE product_name = %s", (title,))
        product = cursor.fetchone()

        if product:
            cursor.execute(
                "INSERT INTO price_history (product_id, price) VALUES (%s, %s)",
                (product_id, price_value)
            )
            conn.commit()
            print("Updated {}: Rs.{}".format(product_name,price_value))
        else:
            print("Error: Product '{}' not found in database!".format(title))

while True:
    update_prices()
    time.sleep(3600)  
