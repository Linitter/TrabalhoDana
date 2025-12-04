import sqlite3
import csv

# Criar conexão
conn = sqlite3.connect('db/used_cars.db')
c = conn.cursor()

# Criar tabela
c.execute('''CREATE TABLE cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT,
    model TEXT,
    year INTEGER,
    price REAL
)''')

# Criar índice
c.execute('CREATE INDEX idx_model ON cars(model)')

# Ler e inserir dados
with open('db/used_cars.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, 1):
        c.execute('INSERT INTO cars (brand, model, year, price) VALUES (?, ?, ?, ?)',
                  (row['brand'], row['model'], int(row['year']), float(row['price'])))
        if i % 1000 == 0:
            print(f"{i} registros...")

conn.commit()

# Verificar
c.execute('SELECT COUNT(*) FROM cars')
print(f"Total: {c.fetchone()[0]} registros")

conn.close()
print("Concluído!")
