from flask import Flask, render_template, request, session, redirect, url_for
import json

app = Flask(__name__)
app.secret_key = 'supermarket_secret_2026'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)

def save_products(data):
    with open('products.json', 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip().lower()
    data = load_products()
    products = data['products']
    
    # Search by barcode or product name
    results = []
    for p in products:
        if query == p['barcode'] or query in p['name'].lower() or query in p['brand'].lower() or query in p['category'].lower():
            results.append(p)
    
    return render_template('result.html', results=results, query=query)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            error = "Invalid credentials!"
    return render_template('login.html', error=error)

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    data = load_products()
    return render_template('admin.html', products=data['products'])

@app.route('/admin/add', methods=['POST'])
def add_product():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    data = load_products()
    new_product = {
        "barcode": request.form['barcode'],
        "name": request.form['name'],
        "brand": request.form['brand'],
        "category": request.form['category'],
        "aisle": int(request.form['aisle']),
        "shelf": int(request.form['shelf']),
        "side": request.form['side'],
        "price": request.form['price']
    }
    data['products'].append(new_product)
    save_products(data)
    return redirect(url_for('admin'))

@app.route('/admin/delete/<barcode>')
def delete_product(barcode):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    data = load_products()
    data['products'] = [p for p in data['products'] if p['barcode'] != barcode]
    save_products(data)
    return redirect(url_for('admin'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)