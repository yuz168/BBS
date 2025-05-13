Python 3.13.3 (tags/v3.13.3:6280bb5, Apr  8 2025, 14:47:33) [MSC v.1943 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> from flask import Flask, render_template, request, redirect, url_for
... import sqlite3
... from datetime import datetime
... 
... app = Flask(__name__)
... DATABASE = 'bulletinboard.db'
... 
... def get_db():
...     conn = sqlite3.connect(DATABASE)
...     conn.row_factory = sqlite3.Row
...     return conn
... 
... def init_db():
...     with app.app_context():
...         db = get_db()
...         with app.open_resource('schema.sql', mode='r') as f:
...             db.cursor().executescript(f.read())
...         db.commit()
... 
... @app.cli.command('initdb')
... def initdb_command():
...     """Initializes the database."""
...     init_db()
...     print('Initialized the database.')
... 
... def query_db(query, args=(), one=False):
...     cur = get_db().execute(query, args)
...     rv = cur.fetchall()
...     cur.close()
...     return (rv[0] if rv else None) if one else rv
... 
... def execute_db(query, args=()):
...     conn = get_db()
...     cur = conn.cursor()
...     cur.execute(query, args)
...     conn.commit()
...     cur.close()

@app.route('/')
def index():
    posts = query_db('SELECT id, text, created_at FROM posts ORDER BY id DESC')
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['POST'])
def post():
    text = request.form['text']
    now = datetime.now()
    created_at = now.strftime('%Y-%m-%d %H:%M:%S')
    execute_db('INSERT INTO posts (text, created_at) VALUES (?, ?)', (text, created_at))
    return redirect(url_for('index'))

if __name__ == '__main__':
