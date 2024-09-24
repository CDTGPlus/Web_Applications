from flask import Flask, render_template, request, redirect
import sqlite3
from box_fit import box_it
from box_sizes_data import *

app = Flask(__name__, static_folder='static')
# #run database 
# init_db()
# Initialize the database conn
def get_db_connection():
    #run database 
    init_db()
    conn = sqlite3.connect('box_sizes.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/find-box', methods=['POST'])
def find_box():
    length = int(request.form['length'])
    width = int(request.form['width'])
    height = int(request.form['height'])
    padding = int(request.form['padding'])
    
    item_dims = [length, width, height]
    if padding > 0:
        for i in range(len(item_dims)):
            item_dims[i] += padding
    
    conn = get_db_connection()
    boxes = conn.execute('SELECT length, width, height FROM boxes').fetchall()
    conn.close()
    
    # Convert fetched boxes into a list of tuples
    available_boxes = [(box['length'], box['width'], box['height']) for box in boxes]
    
    recommended_box = box_it(item_dims, available_boxes)
    
    return render_template('result.html', box=recommended_box)

@app.route('/box-sizes')
def box_sizes():
    conn = get_db_connection()
    boxes = conn.execute('SELECT * FROM boxes').fetchall()
    conn.close()
    
    return render_template('boxsizes.html', boxes=boxes)

@app.route('/add-box', methods=['POST'])
def add_box():
    length = int(request.form['length'])
    width = int(request.form['width'])
    height = int(request.form['height'])

    conn = get_db_connection()
    conn.execute('INSERT INTO boxes (length, width, height) VALUES (?, ?, ?)', (length, width, height))
    conn.commit()
    conn.close()
    
    return redirect('/box-sizes')

# Route to handle deleting a box
@app.route('/delete-box', methods=['POST'])
def delete_box():
    box_id = int(request.form['id'])
    
    conn = get_db_connection()
    conn.execute('DELETE FROM boxes WHERE id = ?', (box_id,))
    conn.commit()
    conn.close()
    
    return redirect('/box-sizes')

if __name__ == '__main__':
    app.run(debug=True)

