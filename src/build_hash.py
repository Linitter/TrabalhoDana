import csv
import pickle
import os
import sys

def build_hashmap():
    
    csv_path = os.path.join('db', 'used_cars.csv')
    hash_path = os.path.join('db', 'hashmap.pickle')
    
    # Verificar se o CSV existe
    if not os.path.exists(csv_path):
        print("❌ ERRO: Arquivo CSV não encontrado!")
        print(f"➡️  Esperado em: {csv_path}")
        sys.exit(1)
    
    print("📂 Lendo arquivo CSV...")
    
    # Carregar dados do CSV
    cars = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cars.append({
                'id': int(row['id']),
                'brand': row['brand'],
                'model': row['model'],
                'year': int(row['year']),
                'price': float(row['price'])
            })
    
    print(f"📊 Total de registros: {len(cars)}")
    
    # Construir HashMap
    print("🔨 Construindo HashMap...")
    hashmap = {}
    
    for car in cars:
        # Usar model em lowercase como chave
        key = car['model'].lower()
        
        if key not in hashmap:
            hashmap[key] = []
        
        hashmap[key].append(car)
    
    print(f"✅ HashMap construído com {len(hashmap)} chaves únicas")
    
    # Criar diretório db se não existir
    os.makedirs('db', exist_ok=True)
    
    # Salvar HashMap em arquivo pickle
    print(f"💾 Salvando HashMap em {hash_path}...")
    with open(hash_path, 'wb') as f:
        pickle.dump(hashmap, f)
    
    print("✅ HashMap salvo com sucesso!")
    
    # Estatísticas
    total_entries = sum(len(v) for v in hashmap.values())
    print(f"\n📊 Estatísticas:")
    print(f"   - Chaves únicas: {len(hashmap)}")
    print(f"   - Total de entradas: {total_entries}")
    print(f"   - Tamanho do arquivo: {os.path.getsize(hash_path) / 1024 / 1024:.2f} MB")
    
    print("\n✨ Construção concluída!")
    print("➡️  Próximo passo: Execute 'python src/app.py'")

if __name__ == '__main__':
    build_hashmap()
