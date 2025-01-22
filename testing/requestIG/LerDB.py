import sqlite3

conn = sqlite3.connect('produtos.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM produtos')
produtos = cursor.fetchall()
for produto in produtos:
    print(produto)
conn.close()