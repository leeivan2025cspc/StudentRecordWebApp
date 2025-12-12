from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from models import init_db, load_all_from_db, save_student_to_db, delete_student_from_db, StudentLinkedList
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret-key')

# Initialize DB and load into linked list
init_db()
ds = StudentLinkedList()
ds.load_from_list(load_all_from_db())

# Admin credentials (override with env vars if needed)
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', 'password123')

def login_required(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapped

@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('records'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username','')
        password = request.form.get('password','')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('records'))
        else:
            msg = 'Invalid credentials'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/records')
@login_required
def records():
    return render_template('records.html')

@app.route('/add', methods=['GET','POST'])
@login_required
def add_page():
    return render_template('add.html')

@app.route('/delete', methods=['GET','POST'])
@login_required
def delete_page():
    return render_template('delete.html')

@app.route('/search', methods=['GET','POST'])
@login_required
def search_page():
    return render_template('search.html')

@app.route('/sort', methods=['GET','POST'])
@login_required
def sort_page():
    return render_template('sort.html')

# API endpoints (JSON)
@app.route('/api/students', methods=['GET'])
@login_required
def api_get_students():
    return jsonify(ds.to_list())

@app.route('/api/students', methods=['POST'])
@login_required
def api_add_student():
    data = request.get_json() or request.form
    sid = data.get('id','').strip()
    name = data.get('name','').strip()
    course = data.get('course','').strip()
    grade = data.get('grade','').strip()
    if not sid or not name:
        return jsonify({'error':'id and name required'}), 400
    if ds.find_by_id(sid):
        return jsonify({'error':'duplicate id'}), 400
    ds.insert(sid, name, course, grade)
    save_student_to_db({'id':sid,'name':name,'course':course,'grade':grade})
    return jsonify({'ok':True})

@app.route('/api/delete/id', methods=['POST'])
@login_required
def api_delete_by_id():
    data = request.get_json() or request.form
    sid = data.get('id','').strip()
    if not sid:
        return jsonify({'error':'id required'}), 400
    deleted = ds.delete_by_id(sid)
    delete_student_from_db(sid)
    return jsonify({'deleted': deleted})

@app.route('/api/delete/name', methods=['POST'])
@login_required
def api_delete_by_name():
    data = request.get_json() or request.form
    name = data.get('name','').strip().lower()
    if not name:
        return jsonify({'error':'name required'}), 400
    removed = 0
    curr = ds.head
    to_delete = []
    while curr:
        if curr.name.lower() == name:
            to_delete.append(curr.id)
        curr = curr.next
    for sid in to_delete:
        if ds.delete_by_id(sid):
            delete_student_from_db(sid)
            removed += 1
    return jsonify({'removed': removed})

@app.route('/api/search', methods=['GET'])
@login_required
def api_search():
    q = request.args.get('q','').strip().lower()
    if not q:
        return jsonify([])
    results = []
    for r in ds.to_list():
        if q in r['id'].lower() or q in r['name'].lower():
            results.append(r)
    return jsonify(results)

@app.route('/api/sort', methods=['POST'])
@login_required
def api_sort():
    data = request.get_json() or request.form
    key = data.get('by','name')
    if key == 'name':
        ds.sort_by_name()
    else:
        ds.sort_by_id()
    for rec in ds.to_list():
        save_student_to_db(rec)
    return jsonify({'ok':True})

if __name__ == '__main__':
    app.run(debug=True)
