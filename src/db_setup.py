import sqlite3
import pandas as pd
import os
import sys

def setup_database():
    
    # Caminhos dos arquivos
    csv_path = os.path.join('db', 'used_cars.csv')
    db_path = os.path.join('db', 'used_cars.db')
    
    # Verificar se o CSV existe
    if not os.path.exists(csv_path):
        print("❌ ERRO: Arquivo 'db/used_cars.csv' não encontrado!")
        print("📥 O arquivo CSV com 5.000 registros deve estar na pasta 'db/'.")
        print("📁 Certifique-se de que o arquivo 'used_cars.csv' está em 'db/'")
        sys.exit(1)
    
    print("📂 Lendo arquivo CSV...")
    
    try:
        # Ler o CSV
        df = pd.read_csv(csv_path, encoding='utf-8', low_memory=False)
    except Exception as e:
        try:
            # Tentar com encoding diferente
            df = pd.read_csv(csv_path, encoding='latin-1', low_memory=False)
        except Exception as e:
            print(f"❌ ERRO ao ler CSV: {e}")
            sys.exit(1)
    
    # Validar número de registros
    num_registros = len(df)
    print(f"📊 Total de registros no CSV: {num_registros}")
    
    if num_registros < 5000:
        print(f"❌ ERRO: CSV deve conter no mínimo 5000 registros!")
        print(f"   Registros encontrados: {num_registros}")
        print("📥 Por favor, baixe um dataset maior do Kaggle.")
        sys.exit(1)
    
    print(f"✅ Validação OK: {num_registros} registros encontrados")
    
    # Detectar colunas automaticamente
    print("\n🔍 Detectando colunas do CSV...")
    print(f"Colunas disponíveis: {list(df.columns)}")
    
    # Mapear colunas comuns de datasets de carros
    column_mapping = {}
    
    # Detectar coluna de marca
    for col in df.columns:
        col_lower = col.lower()
        if 'brand' in col_lower or 'make' in col_lower or 'marca' in col_lower or 'manufacturer' in col_lower:
            column_mapping['brand'] = col
            break
    
    # Detectar coluna de modelo
    for col in df.columns:
        col_lower = col.lower()
        if 'model' in col_lower or 'modelo' in col_lower:
            column_mapping['model'] = col
            break
    
    # Detectar coluna de ano
    for col in df.columns:
        col_lower = col.lower()
        if 'year' in col_lower or 'ano' in col_lower or 'yr' in col_lower:
            column_mapping['year'] = col
            break
    
    # Detectar coluna de preço
    for col in df.columns:
        col_lower = col.lower()
        if 'price' in col_lower or 'preco' in col_lower or 'preço' in col_lower or 'valor' in col_lower:
            column_mapping['price'] = col
            break
    
    print(f"Mapeamento de colunas: {column_mapping}")
    
    # Verificar se encontrou as colunas essenciais
    if 'model' not in column_mapping:
        print("⚠️  Aviso: Coluna 'model' não detectada automaticamente")
        print("   Usando a primeira coluna de texto como modelo")
        for col in df.columns:
            if df[col].dtype == 'object':
                column_mapping['model'] = col
                break
    
    # Preparar DataFrame com colunas padronizadas
    df_clean = pd.DataFrame()
    
    # Brand
    if 'brand' in column_mapping:
        df_clean['brand'] = df[column_mapping['brand']].fillna('Unknown')
    else:
        df_clean['brand'] = 'Unknown'
    
    # Model (obrigatório)
    if 'model' in column_mapping:
        df_clean['model'] = df[column_mapping['model']].fillna('Unknown')
    else:
        print("❌ ERRO: Não foi possível detectar coluna de modelo")
        sys.exit(1)
    
    # Year
    if 'year' in column_mapping:
        df_clean['year'] = pd.to_numeric(df[column_mapping['year']], errors='coerce').fillna(2000).astype(int)
    else:
        df_clean['year'] = 2000
    
    # Price
    if 'price' in column_mapping:
        df_clean['price'] = pd.to_numeric(df[column_mapping['price']], errors='coerce').fillna(0).astype(float)
    else:
        df_clean['price'] = 0.0
    
    # Limpar dados
    df_clean['brand'] = df_clean['brand'].astype(str).str.strip()
    df_clean['model'] = df_clean['model'].astype(str).str.strip()
    
    # Remover linhas com model vazio
    df_clean = df_clean[df_clean['model'] != '']
    df_clean = df_clean[df_clean['model'] != 'nan']
    
    print(f"✅ Dados limpos: {len(df_clean)} registros válidos")
    
    # Criar diretório db se não existir
    os.makedirs('db', exist_ok=True)
    
    # Remover banco existente
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("🗑️  Banco de dados anterior removido")
        except Exception as e:
            print(f"⚠️  Aviso: Não foi possível remover banco anterior: {e}")
            print("   Tentando sobrescrever...")
    
    # Conectar ao banco de dados
    print("\n🔧 Criando banco de dados SQLite...")
    conn = sqlite3.connect(db_path, timeout=10)
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
    
    print("✅ Tabela 'cars' criada")
    
    # Criar índice no campo model
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_model ON cars(model)')
    print("✅ Índice criado no campo 'model'")
    
    # Importar dados
    print("\n📥 Importando dados para o banco...")
    df_clean.to_sql('cars', conn, if_exists='append', index=False)
    
    # Verificar quantidade de registros importados
    cursor.execute('SELECT COUNT(*) FROM cars')
    total = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    print(f"✅ {total} registros importados com sucesso!")
    print(f"📁 Banco de dados criado em: {db_path}")
    print("\n✨ Configuração concluída!")
    print("➡️  Próximo passo: Execute 'python src/build_hash.py'")

if __name__ == '__main__':
    setup_database()
