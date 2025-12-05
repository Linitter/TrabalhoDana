import csv
import pickle
import os

CSV_PATH = os.path.join('db', 'used_cars.csv')
HASH_PATH = os.path.join('db', 'hashmap.pickle')

# Cache global
_data_cache = None
_index_cache = None
_hashmap_cache = None


def load_csv_data():
    """Carrega todos os dados do CSV"""
    global _data_cache
    if _data_cache is None:
        _data_cache = []
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                _data_cache.append({
                    'id': int(row['id']),
                    'brand': row['brand'],
                    'model': row['model'],
                    'year': int(row['year']),
                    'price': float(row['price'])
                })
    return _data_cache


def create_index():
    """Cria um índice em memória por modelo (simula índice do SQL)"""
    global _index_cache
    if _index_cache is None:
        cars = load_csv_data()
        _index_cache = {}
        for car in cars:
            model_lower = car['model'].lower()
            brand_lower = car['brand'].lower()
            
            # Indexar por modelo
            if model_lower not in _index_cache:
                _index_cache[model_lower] = []
            _index_cache[model_lower].append(car)
            
            # Indexar por marca também
            key_brand = f"brand:{brand_lower}"
            if key_brand not in _index_cache:
                _index_cache[key_brand] = []
            _index_cache[key_brand].append(car)
    
    return _index_cache


def load_hashmap():
    """Carrega HashMap do arquivo ou cria se não existir"""
    global _hashmap_cache
    
    if _hashmap_cache is not None:
        return _hashmap_cache
    
    if os.path.exists(HASH_PATH):
        with open(HASH_PATH, 'rb') as f:
            _hashmap_cache = pickle.load(f)
    else:
        # Criar hashmap
        _hashmap_cache = create_hashmap()
    
    return _hashmap_cache


def create_hashmap():
    """Cria HashMap e persiste em arquivo"""
    cars = load_csv_data()
    hashmap = {}
    
    for car in cars:
        model_lower = car['model'].lower()
        if model_lower not in hashmap:
            hashmap[model_lower] = []
        hashmap[model_lower].append(car)
    
    # Salvar em arquivo pickle
    os.makedirs('db', exist_ok=True)
    with open(HASH_PATH, 'wb') as f:
        pickle.dump(hashmap, f)
    
    print(f"✅ HashMap criado com {len(hashmap)} chaves")
    return hashmap


def search_sequential(query):
    """
    BUSCA SEQUENCIAL (Linear Search)
    
    Percorre todos os registros linearmente,
    comparando cada registro com o termo de busca.
    
    Complexidade: O(n)
    """
    if not query:
        return []
    
    query_lower = query.lower()
    results = []
    
    # Carregar todos os dados
    cars = load_csv_data()
    
    # Percorrer manualmente cada registro (busca linear)
    for car in cars:
        brand = car['brand'].lower()
        model = car['model'].lower()
        
        # Comparar se o termo está contido na marca ou modelo
        if query_lower in brand or query_lower in model:
            results.append(car)
    
    # Limitar resultados
    return results[:100]


def search_indexed(query):
    """
    BUSCA INDEXADA (Indexed Search)
    
    Utiliza um índice em memória (simula índice SQL)
    para realizar uma busca otimizada.
    
    Complexidade: O(log n) ou O(1) dependendo da estrutura
    """
    if not query:
        return []
    
    query_lower = query.lower()
    results = []
    seen_ids = set()
    
    # Carregar índice
    index = create_index()
    
    # Buscar no índice
    for key, cars in index.items():
        if query_lower in key:
            for car in cars:
                if car['id'] not in seen_ids:
                    results.append(car)
                    seen_ids.add(car['id'])
                    
                    if len(results) >= 100:
                        return results
    
    return results


def search_hashmap(query):
    """
    BUSCA COM HASHMAP (Hash-based Search)
    
    Busca diretamente em uma estrutura HashMap em memória,
    onde a chave é o modelo do carro em lowercase.
    
    Complexidade: O(1) no caso médio
    """
    if not query:
        return []
    
    query_lower = query.lower()
    results = []
    seen_ids = set()
    
    # Carregar HashMap
    hashmap = load_hashmap()
    
    # Buscar correspondências exatas na chave
    if query_lower in hashmap:
        for car in hashmap[query_lower]:
            if car['id'] not in seen_ids:
                results.append(car)
                seen_ids.add(car['id'])
    
    # Buscar correspondências parciais (substring)
    if len(results) < 100:
        for key, cars in hashmap.items():
            if query_lower in key and query_lower != key:
                for car in cars:
                    if car['id'] not in seen_ids:
                        results.append(car)
                        seen_ids.add(car['id'])
                        
                        if len(results) >= 100:
                            return results
    
    # Também buscar na marca
    if len(results) < 100:
        for key, cars in hashmap.items():
            for car in cars:
                if query_lower in car['brand'].lower():
                    if car['id'] not in seen_ids:
                        results.append(car)
                        seen_ids.add(car['id'])
                        
                        if len(results) >= 100:
                            return results
    
    return results


def get_catalog(page=1, per_page=20):
    """
    Retorna uma lista paginada de carros para o catálogo.
    """
    cars = load_csv_data()
    total = len(cars)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    results = cars[start:end]
    
    return {
        'results': results,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }
