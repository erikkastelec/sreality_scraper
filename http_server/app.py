from flask import Flask, render_template
import psycopg2
import signal
import sys

cur = None
conn = None

# Handle SIGTERM signal
def signal_handler(sig, frame):
    print('SIGTERM received, gracefully shutting down')
    if cur is not None and conn is not None:
        cur.close()
        conn.close()

    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)

app = Flask(__name__)

# Database connection parameters
db_params = {
    'database': 'yourdbname',
    'user': 'youruser',
    'password': 'yourpassword',
    'host': 'postgres',  # or 'postgres' if using Docker and docker-compose
    'port': '5432'
}

@app.route('/heartbeat')
def heartbeat():
    return 'OK', 200

@app.route('/')
def show_items():
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Execute a query
    cur.execute("SELECT title, image_url FROM estate_items")
    
    # Fetch all rows
    items = cur.fetchall()

    # Close the database connection
    cur.close()
    conn.close()

    # Render a template with the items
    return render_template('items.html', items=items)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
