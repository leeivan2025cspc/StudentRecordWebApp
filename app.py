# app.py
from flask import Flask, render_template, jsonify, request
from models import init_db, load_all_from_db, save_student_to_db, delete_student_from_db, StudentLinkedList

app = Flask(__name__, static_folder="static", template_folder="templates")

# Initialize DB and load records into linked list (app-level memory)
init_db()
ds = StudentLinkedList()
ds.load_from_list(load_all_from_db())

# Helper: sync linked list -> DB (simple approach: iterate and save)
def sync_to_db():
    for rec in ds.to_list():
        save_student_to_db(rec)

@app.route("/")
def index():
    return render_template("index.html")

# API: get all records (traverse)
@app.route("/api/students", methods=["GET"])
def get_students():
    # returns current state of linked list
    return jsonify(ds.to_list())

# API: add student (insert in linked list + save to DB)
@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.json
    # expected keys: id, name, course, grade
    sid = data.get("id")
    name = data.get("name")
    if not sid or not name:
        return jsonify({"error": "id and name required"}), 400
    # insert in linked list
    ds.insert(sid, name, data.get("course",""), data.get("grade",""))
    # persist
    save_student_to_db({"id": sid, "name": name, "course": data.get("course",""), "grade": data.get("grade","")})
    return jsonify({"ok": True}), 201

# API: delete by id (use linked list deletion + db delete)
@app.route("/api/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    deleted = ds.delete_by_id(student_id)
    if deleted:
        delete_student_from_db(student_id)
        return jsonify({"ok": True})
    return jsonify({"error": "not found"}), 404

# API: search by id or name (we do logic in Python)
@app.route("/api/search", methods=["GET"])
def search_student():
    q = request.args.get("q","").strip().lower()
    if not q:
        return jsonify([])
    results = []
    for r in ds.to_list():
        if q in r['id'].lower() or q in r['name'].lower():
            results.append(r)
    return jsonify(results)

# API: sort
@app.route("/api/sort", methods=["POST"])
def sort_students():
    data = request.json
    key = data.get("by","name")
    if key == "name":
        ds.sort_by_name()
    else:
        ds.sort_by_id()
    # after sorting, persist order to DB (we will replace rows by storing them; since DB has no order, this simply ensures DB has same content)
    sync_to_db()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True)
