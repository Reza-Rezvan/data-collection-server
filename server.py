import logging
from flask import Flask, request, jsonify, render_template_string
import sqlite3
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Set the max upload size to 16MB
DATABASE = 'database.db'

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def insert_data(hardware_id, time, date, speed, label, image_data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Insert or ignore into the Hardware table
    cursor.execute('''
    INSERT OR IGNORE INTO Hardware (Hardware_id)
    VALUES (?)
    ''')

    # Insert into the Data table
    cursor.execute('''
    INSERT INTO Data (Hardware_id, Time, Date, Speed, Label, Image)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (hardware_id, time, date, speed, label, image_data))

    conn.commit()
    conn.close()

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    app.logger.debug(f"Received data: {data}")
    try:
        insert_data(
            data['hardware_id'],
            data['timestamp']['time'],
            data['timestamp']['date'],
            data['speed'],
            data['label'],
            data['image_data']
        )
        app.logger.debug("Data inserted successfully")
        return jsonify({"message": "Data inserted successfully"}), 200
    except Exception as e:
        app.logger.error(f"Error inserting data: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/hardware', methods=['GET'])
def get_hardware():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Hardware')
    rows = cursor.fetchall()
    conn.close()

    # Convert the data to a list of dictionaries
    data = [{"hardware_id": row[0]} for row in rows]

    # HTML template to display hardware IDs
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hardware IDs</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <h2>Hardware IDs</h2>
        <table>
            <tr>
                <th>Hardware ID</th>
            </tr>
            {% for row in data %}
            <tr>
                <td><a href="/data/{{ row.hardware_id }}">{{ row.hardware_id }}</a></td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, data=data)

@app.route('/data/<int:hardware_id>', methods=['GET'])
def get_data(hardware_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Data WHERE Hardware_id = ? ORDER BY Date, Time', (hardware_id,))
    rows = cursor.fetchall()
    conn.close()

    # Convert the data to a list of dictionaries
    data = []
    for row in rows:
        data.append({
            "hardware_id": row[1],
            "time": row[2],
            "date": row[3],
            "speed": row[4],
            "label": row[5],
            "image_data": row[6]
        })

    # HTML template to display data
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Data for Hardware ID {{ hardware_id }}</title>
        <style>
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
        </style>
    </head>
    <body>
        <h2>Data for Hardware ID {{ hardware_id }}</h2>
        <table>
            <tr>
                <th>Time</th>
                <th>Date</th>
                <th>Speed</th>
                <th>Label</th>
                <th>Image Data</th>
            </tr>
            {% for row in data %}
            <tr>
                <td>{{ row.time }}</td>
                <td>{{ row.date }}</td>
                <td>{{ row.speed }}</td>
                <td>{{ row.label }}</td>
                <td><a href="data:image/png;base64,{{ row.image_data }}" download="image_{{ row.hardware_id }}.png">Download</a></td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, data=data, hardware_id=hardware_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)
