"""
Script simplificado para criar o banco de dados
"""
import sqlite3
import csv
import os

csv_path = 'db/used_cars.csv'
db_path = 'db/used_cars.db'

# Remover banco se existir
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("Banco anterior removido")
    except:
        print("Erro ao remover banco - tentando criar mesmo assim")

print("Criando banco...")
conn = sqlite3.connect(db_path, timeout=30)
cursor = conn.cursor()

# Criar tabela
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER,
        price REAL
    )
''')

print("Tabela criada")

# Criar índice
cursor.execute('CREATE INDEX IF NOT EXISTS idx_model ON cars(model)')
print("Índice criado")

# Importar dados do CSV
print("Importando dados...")
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        cursor.execute(
            'INSERT INTO cars (brand, model, year, price) VALUES (?, ?, ?, ?)',
            (row['brand'], row['model'], int(row['year']), float(row['price']))
        )
        count += 1
        if count % 500 == 0:
            print(f"Importados {count} registros...")

conn.commit()

# Verificar
cursor.execute('SELECT COUNT(*) FROM cars')
total = cursor.fetchone()[0]
print(f"\n✅ Total de registros: {total}")

conn.close()
print("✅ Banco criado com sucesso!")
