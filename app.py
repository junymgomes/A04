from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'database.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    create_table()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros')
    registros = cursor.fetchall()
    conn.close()
    return render_template('index.html', registros=registros)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    idade = request.form['idade']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO registros (nome, idade) VALUES (?, ?)', (nome, idade))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar(id):
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE registros SET nome=?, idade=? WHERE id=?', (nome, idade, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM registros WHERE id=?', (id,))
        registro = cursor.fetchone()
        conn.close()
        return render_template('atualizar.html', registro=registro)

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM registros WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
