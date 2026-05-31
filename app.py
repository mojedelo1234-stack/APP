from flask import Flask, request, jsonify, render_template
import psycopg2
import psycopg2.extras
import os
app = Flask(__name__)
def get_db():
    conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    return conn
def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            type TEXT NOT NULL,
            done INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS dreams (
            id SERIAL PRIMARY KEY,
            entry TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()
init_db()
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api/goals', methods=['GET'])
def get_goals():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM goals ORDER BY created_at ASC')
    goals = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(g) for g in goals])
@app.route('/api/goals', methods=['POST'])
def add_goal():
    data = request.json
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        'INSERT INTO goals (text, type) VALUES (%s, %s) RETURNING *',
        (data['text'], data['type'])
    )
    goal = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(goal))
@app.route('/api/goals/<int:goal_id>', methods=['PATCH'])
def update_goal(goal_id):
    data = request.json
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if 'done' in data:
        cur.execute('UPDATE goals SET done = %s WHERE id = %s', (data['done'], goal_id))
    if 'text' in data:
        cur.execute('UPDATE goals SET text = %s WHERE id = %s', (data['text'], goal_id))
    conn.commit()
    cur.execute('SELECT * FROM goals WHERE id = %s', (goal_id,))
    goal = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(dict(goal))
@app.route('/api/goals/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM goals WHERE id = %s', (goal_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'ok': True})
@app.route('/api/goals/reset-daily', methods=['POST'])
def reset_daily():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE goals SET done = 0 WHERE type = 'daily'")
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'ok': True})
@app.route('/api/dreams', methods=['GET'])
def get_dreams():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM dreams ORDER BY created_at DESC')
    dreams = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([dict(d) for d in dreams])
@app.route('/api/dreams', methods=['POST'])
def add_dream():
    data = request.json
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('INSERT INTO dreams (entry) VALUES (%s) RETURNING *', (data['entry'],))
    dream = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(dict(dream))
@app.route('/api/dreams/<int:dream_id>', methods=['DELETE'])
def delete_dream(dream_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM dreams WHERE id = %s', (dream_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'ok': True})
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
