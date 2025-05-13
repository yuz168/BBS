from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os
import hashlib  # ハッシュ化のためのライブラリ

app = Flask(__name__)
DATABASE = 'bulletinboard.db'
DATABASE_PATH = os.path.join('/tmp', DATABASE)

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()

@app.route('/')
def index():
    posts = query_db('SELECT id, name, password_id, text, created_at FROM posts ORDER BY id DESC')
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    name = request.form.get('name')
    password = request.form.get('password')  # パスワードを取得
    text = request.form['text']
    now = datetime.now()
    created_at = now.strftime('%Y-%m-%d %H:%M:%S')

    # パスワードをハッシュ化してIDを生成
     hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    short_password_id = hashed_password[:7]  # 最初の7文字を使用
    execute_db('INSERT INTO posts (name, password_id, text, created_at) VALUES (?, ?, ?, ?)', (name, short_password_id, text, created_at))
    return redirect(url_for('index'))

if __name__ == '__main__':
    pass

with app.app_context():
    if not os.path.exists(DATABASE_PATH):
        init_db()
