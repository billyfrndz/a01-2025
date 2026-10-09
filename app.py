from flask import Flask, request, render_template, redirect, jsonify
import sqlite3
import os

app = Flask(__name__)
DB = '/app/data/lab.db'


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')


# ---------- VULN #1: SQL Injection ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        conn = get_db()
        cur = conn.cursor()

        # ❌ VULNERABLE — string concatenation
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cur.execute(query)
        user = cur.fetchone()
        conn.close()

        if user:
            msg = f"Welcome {user['username']}! Your role: {user['role']}"
        else:
            msg = "Invalid credentials"
    return render_template('index.html', msg=msg)


# ---------- VULN #2: Reflected XSS ----------
@app.route('/search')
def search():
    term = request.args.get('q', '')
    # ❌ VULNERABLE — passed to template with |safe (disables auto-escape)
    return render_template('index.html', search=term)


# ---------- VULN #3: IDOR (Broken Access Control) ----------
@app.route('/note/<int:note_id>')
def get_note(note_id):
    conn = get_db()
    cur = conn.cursor()
    # ❌ VULNERABLE — no ownership check
    cur.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    note = cur.fetchone()
    conn.close()

    if note:
        return jsonify(dict(note))
    return jsonify({"error": "not found"}), 404


if __name__ == '__main__':
    # Ensure DB exists before starting
    if not os.path.exists(DB):
        os.makedirs('/app/data', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

# ---------- SECURE #3: IDOR (Broken Access Control) ----------
@app.route('/invoice/<int:invoice_id>')
@login_required
def get_invoice(invoice_id):
    invoice = Invoice.query.filter_by(
        id=invoice_id,
        user_id=current_user.id     # enforce ownership
    ).first_or_404()
    return jsonify(invoice.to_dict())