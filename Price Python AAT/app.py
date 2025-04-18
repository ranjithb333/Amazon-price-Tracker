from flask import Flask, render_template, request, jsonify
import mysql.connector
import matplotlib.pyplot as plt
import io
import base64
from web_scraper import get_amazon_price

app = Flask(__name__)

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='price_tracker'
)
cursor = conn.cursor()


def track_price(product_name):
    title, price, date = get_amazon_price(product_name)
    if not title or not price:
        return None
    
    cursor.execute("SELECT id FROM products WHERE product_name = %s", (title,))
    product = cursor.fetchone()

    if not product:
        cursor.execute("INSERT INTO products (product_name, created_at) VALUES (%s, %s)", (title, date))
        conn.commit()
        product_id = cursor.lastrowid
    else:
        product_id = product[0]

    cursor.execute("INSERT INTO price_history (product_id, price) VALUES (%s, %s)", (product_id, price.replace('Rs.', '')))

    conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    connection = mysql.connector.connect(
        host='localhost',
    user='root',
    password='123456',
    database='price_tracker'
    )
    cursor = connection.cursor()
    if request.method == 'POST':
        product_name = request.form['product_name']
        track_price(product_name)

    cursor.execute('''
    SELECT p.product_name, ph.price, p.id
    FROM products p
    JOIN price_history ph ON p.id = ph.product_id
    WHERE ph.recorded_at = (
        SELECT MAX(recorded_at) 
        FROM price_history 
        WHERE product_id = p.id
    )
    
''')
    
    search_history = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', search_history=search_history)



@app.route('/get_latest_prices')
def get_latest_prices():
    connection = mysql.connector.connect(
        host='localhost',
    user='root',
    password='123456',
    database='price_tracker'
    )
    
    cursor = connection.cursor()
    
    cursor.execute('''
        SELECT p.product_name, ph.price, p.id
        FROM products p
        JOIN price_history ph ON p.id = ph.product_id
        WHERE ph.recorded_at = (
            SELECT MAX(recorded_at) 
            FROM price_history 
            WHERE product_id = p.id
        )
       
    ''')
    
    search_history = cursor.fetchall()
    
    data = [{'product_name': row[0], 'price': row[1], 'product_id': row[2]} for row in search_history]
    
    cursor.close()
    connection.close()
    
    print("API Response Data:", data)
    
    return jsonify(data)
@app.route('/track/<int:product_id>')
def track_product(product_id):


    cursor.execute("SELECT price, recorded_at FROM price_history WHERE product_id = %s ORDER BY recorded_at ASC", (product_id,))
    price_data = cursor.fetchall()

    if not price_data:
        return "No price history available."

    dates = [entry[1].strftime('%Y-%m-%d %H:%M:%S') for entry in price_data]
    prices = [float(entry[0]) for entry in price_data]

    plt.figure(figsize=(8, 5))
    plt.plot(dates, prices, marker='o')
    plt.xlabel("Date")
    plt.ylabel("Price (Rs.)")
    plt.title("Price Trend Over Time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template('track.html', graph_url=graph_url,product_id=product_id)

if __name__ == '__main__':
    app.run(debug=True)
