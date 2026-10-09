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

# ---------- Secure #1: SQL Injection ----------
db.query('SELECT * FROM users WHERE name = ?', [req.query.username]);


# ---------- VULN #2: Reflected XSS ----------
@app.route('/search')
def search():
    term = request.args.get('q', '')
    # ❌ VULNERABLE — passed to template with |safe (disables auto-escape)
    return render_template('index.html', search=term)
    
# ---------- Secure #2: Reflected XSS ----------
name = escape(request.args.get('name', ''))
    return f"<h1>Hello {name}</h1>"

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