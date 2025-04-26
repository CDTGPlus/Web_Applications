from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from box_fit import box_it
from box_sizes_data import *

app = Flask(__name__, static_folder='static')
app.secret_key = 'USERDETERMINEDKEY'

# Database connection function
def get_db_connection():
    init_db()
    conn = sqlite3.connect('box_sizes.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inject dynamic year into all templates
from datetime import datetime
@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

# Route: Home
@app.route('/')
def home():
    return render_template('home.html')

# Route: Sign Up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        account_name = request.form['account_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        new_username = add_user(account_name, email, username, password)
        session['username'] = new_username
        return redirect(url_for('profile'))

    return render_template('signup.html')

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            flash("Login successful!", "success")
            return redirect(url_for('profile'))
        else:
            flash("Invalid username or password.", "error")

    return render_template('login.html')

# Route: Profile
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (session['username'],)).fetchone()
    conn.close()

    return render_template('profile.html', user=user)

# Route: Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect('/')

# Route: Find Suitable Box
@app.route('/find-box', methods=['POST'])
def find_box():
    if 'username' not in session:
        flash("You must be logged in to find a box.", "error")
        return redirect(url_for('login'))

    length = int(request.form['length'])
    width = int(request.form['width'])
    height = int(request.form['height'])
    padding = int(request.form['padding'])

    item_dims = [length, width, height]
    if padding > 0:
        for i in range(len(item_dims)):
            item_dims[i] += padding

    conn = get_db_connection()
    user = conn.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()
    boxes = get_user_boxes(user['id'])

    available_boxes = [(box[2], box[3], box[4]) for box in boxes]
    recommended_box, closest_box = box_it(item_dims, available_boxes)

    return render_template('result.html', box=recommended_box, closest_box=closest_box)

@app.route('/add-box', methods=['GET', 'POST'])
def add_box_route():
    if 'username' not in session:
        flash("You must be logged in to add a box.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()

    if request.method == 'POST':
        length = int(request.form['length'])
        width = int(request.form['width'])
        height = int(request.form['height'])

        add_box(user['id'], length, width, height)

        flash("Box added successfully!", "success")
        return redirect('/box-sizes')

    # Render add_box.html when the request is GET
    return render_template('add_box.html')

# Route: View User's Boxes
@app.route('/box-sizes')
def box_sizes():
    if 'username' not in session:
        flash("You must be logged in to view your boxes.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()
    # boxes = get_user_boxes(user['id'])
    boxes = conn.execute('SELECT * FROM boxes WHERE user_id = ? ORDER BY length, width, height', (user['id'],)).fetchall()

    return render_template('boxsizes.html', boxes=boxes)

# Route: Edit Box
@app.route('/edit-box/<int:box_id>', methods=['GET', 'POST'])
def edit_box(box_id):
    if 'username' not in session:
        flash("You must be logged in to edit a box.", "error")
        return redirect(url_for('login'))

    conn = get_db_connection()
    user = conn.execute('SELECT id FROM users WHERE username = ?', (session['username'],)).fetchone()

    if request.method == 'POST':
        length = int(request.form['length'])
        width = int(request.form['width'])
        height = int(request.form['height'])

        update_box(box_id, length, width, height)

        flash("Box updated successfully!", "success")
        return redirect('/box-sizes')

    # Retrieve the current box details
    box = conn.execute('SELECT * FROM boxes WHERE id = ?', (box_id,)).fetchone()
    print("Hello Mate")
    print(box)

    return render_template('edit_box.html', box=box)

# Route: Delete Box
@app.route('/delete-box/<int:box_id>', methods=['POST'])
def delete_box_route(box_id):
    if 'username' not in session:
        flash("You must be logged in to delete a box.", "error")
        return redirect(url_for('login'))

    delete_box(box_id)
    flash("Box deleted successfully!", "success")
    return redirect('/box-sizes')

if __name__ == '__main__':
    app.run(debug=True)
