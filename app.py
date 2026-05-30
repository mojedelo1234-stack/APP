from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), 'goals.db')

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            type TEXT NOT NULL,
            done INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/goals', methods=['GET'])
def get_goals():
    conn = get_db()
    goals = conn.execute('SELECT * FROM goals ORDER BY created_at ASC').fetchall()
    conn.close()
    return jsonify([dict(g) for g in goals])

@app.route('/api/goals', methods=['POST'])
def add_goal():
    data = request.json
    conn = get_db()
    cur = conn.execute(
        'INSERT INTO goals (text, type) VALUES (?, ?)',
        (data['text'], data['type'])
    )
    conn.commit()
    goal = conn.execute('SELECT * FROM goals WHERE id = ?', (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(goal))

@app.route('/api/goals/<int:goal_id>', methods=['PATCH'])
def update_goal(goal_id):
    data = request.json
    conn = get_db()
    conn.execute('UPDATE goals SET done = ? WHERE id = ?', (data['done'], goal_id))
    conn.commit()
    goal = conn.execute('SELECT * FROM goals WHERE id = ?', (goal_id,)).fetchone()
    conn.close()
    return jsonify(dict(goal))

@app.route('/api/goals/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    conn = get_db()
    conn.execute('DELETE FROM goals WHERE id = ?', (goal_id,))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/goals/reset-daily', methods=['POST'])
def reset_daily():
    conn = get_db()
    conn.execute("UPDATE goals SET done = 0 WHERE type = 'daily'")
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
