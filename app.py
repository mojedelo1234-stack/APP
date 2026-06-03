from flask import Flask, request, jsonify, render_template
from psycopg2 import pool as pg_pool
import psycopg2.extras
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ─── Connection pool ─────────────────────────────────────────────────────────
# Opens 2–10 persistent connections instead of 1 per request.
# Prevents hitting Railway Postgres's connection limit under normal usage.

connection_pool = pg_pool.ThreadedConnectionPool(
    minconn=2,
    maxconn=10,
    dsn=os.environ['DATABASE_URL'],
    sslmode='require',
)


def get_db():
    """Borrow a connection from the pool."""
    return connection_pool.getconn()


def release_db(conn):
    """Return a connection to the pool."""
    connection_pool.putconn(conn)


# ─── Schema init ─────────────────────────────────────────────────────────────

def init_db():
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                id         SERIAL PRIMARY KEY,
                text       TEXT    NOT NULL,
                type       TEXT    NOT NULL CHECK (type IN ('daily','todo')),
                done       INTEGER NOT NULL DEFAULT 0,
                "order"    INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Add order column if upgrading from old schema that didn't have it
        cur.execute('''
            ALTER TABLE goals ADD COLUMN IF NOT EXISTS "order" INTEGER NOT NULL DEFAULT 0
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS dreams (
                id         SERIAL PRIMARY KEY,
                entry      TEXT    NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        logger.info('DB schema ready.')
    except Exception as e:
        conn.rollback()
        logger.error('init_db failed: %s', e)
        raise
    finally:
        release_db(conn)


init_db()


# ─── Routes: app ─────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


# ─── Routes: goals ───────────────────────────────────────────────────────────

@app.route('/api/goals', methods=['GET'])
def get_goals():
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT * FROM goals ORDER BY "order" ASC, id ASC')
        goals = [dict(g) for g in cur.fetchall()]
        cur.close()
        return jsonify(goals)
    except Exception as e:
        logger.error('get_goals: %s', e)
        return jsonify({'error': 'server error'}), 500
    finally:
        release_db(conn)


@app.route('/api/goals', methods=['POST'])
def add_goal():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'invalid JSON'}), 400

    text = (data.get('text') or '').strip()
    type_ = data.get('type', '')

    if not text:
        return jsonify({'error': 'text is required'}), 400
    if type_ not in ('daily', 'todo'):
        return jsonify({'error': 'type must be daily or todo'}), 400
    if len(text) > 500:
        return jsonify({'error': 'text too long'}), 400

    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # Set order to max existing order + 1 for this type so new items go to bottom
        cur.execute(
            'SELECT COALESCE(MAX("order"), 0) + 1 AS next_order FROM goals WHERE type = %s',
            (type_,)
        )
        next_order = cur.fetchone()['next_order']
        cur.execute(
            'INSERT INTO goals (text, type, "order") VALUES (%s, %s, %s) RETURNING *',
            (text, type_, next_order),
        )
        goal = dict(cur.fetchone())
        conn.commit()
        cur.close()
        return jsonify(goal), 201
    except Exception as e:
        conn.rollback()
        logger.error('add_goal: %s', e)
        return jsonify({'error': 'server error'}), 500
    finally:
        release_db(conn)


@app.route('/api/goals/<int:goal_id>', methods=['PATCH'])
def update_goal(goal_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'invalid JSON'}), 400

    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        if 'done' in data:
            done_val = 1 if data['done'] else 0
            cur.execute('UPDATE goals SET done = %s WHERE id = %s', (done_val, goal_id))

        if 'text' in data:
            text = str(data['text']).strip()
            if not text:
                return jsonify({'error': 'text cannot be empty'}), 400
            if len(text) > 500:
                return jsonify({'error': 'text too long'}), 400
            cur.execute('UPDATE goals SET text = %s WHERE id = %s', (text, goal_id))

        if 'order' in data:
            cur.execute('UPDATE goals SET "order" = %s WHERE id = %s', (int(data['order']), goal_id))

        conn.commit()
        cur.execute('SELECT * FROM goals WHERE id = %s', (goal_id,))
        row = cur.fetchone()
        cur.close()

        if not row:
            return jsonify({'error': 'not found'}), 404
        return jsonify(dict(row))
    except Exception as e:
        conn.rollback()
        logger.error('update_goal: %s', e)
        return jsonify({'error': 'server error'}), 500
    finally:
        release_db(conn)


@app.route('/api/goals/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM goals WHERE id = %s', (goal_id,))
        conn.commit()
        cur.close()
        return jsonify({'ok': True})
    except Exception as e:
        conn.rollback()
        logger.error('delete_goal: %s', e)
        return jsonify({'error': 'server error'}), 500
    finally:
        release_db(conn)


@app.route('/api/goals/reset-daily', methods=['POST'])
def reset_daily():
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE goals SET done = 0 WHERE type = 'daily'")
        conn.commit()
        cur.close()
        return jsonify({'ok': True})
    except Exception as e:
        conn.rollback()
        logger.error('reset_daily: %s', e)
        return jsonify({'error': 'server error'}), 500
    finally:
        release_db(conn)


# ─── Routes: dreams ──────────────────────────────────────────────────────────

@app.route('/api/dreams', methods=['GET'])
def get_dreams():
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('SELECT * FROM dreams ORDER BY created_at DESC')
        dreams = [dict(d) for d in cur.fetchall()]
        cur.close()
        return jsonify(dreams)
    except Exception as e:
        logger.error('get_dreams: %s', e)
        return jsonify({'error': 'server error'}), 500
    finally:
        release_db(conn)


@app.route('/api/dreams', methods=['POST'])
def add_dream():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'invalid JSON'}), 400

    entry = (data.get('entry') or '').strip()
    if not entry:
        return jsonify({'error': 'entry is required'}), 400
    if len(entry) > 10000:
        return jsonify({'error': 'entry too long'}), 400

    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute('INSERT INTO dreams (entry) VALUES (%s) RETURNING *', (entry,))
        dream = dict(cur.fetchone())
        conn.commit()
        cur.close()
        return jsonify(dream), 201
    except Exception as e:
        conn.rollback()
        logger.error('add_dream: %s', e)
        return jsonify({'error': 'server error'}), 500
    finally:
        release_db(conn)


@app.route('/api/dreams/<int:dream_id>', methods=['DELETE'])
def delete_dream(dream_id):
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM dreams WHERE id = %s', (dream_id,))
        conn.commit()
        cur.close()
        return jsonify({'ok': True})
    except Exception as e:
        conn.rollback()
        logger.error('delete_dream: %s', e)
        return jsonify({'error': 'server error'}), 500
    finally:
        release_db(conn)


# ─── Run ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
