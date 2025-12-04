import os
import time

db_path = 'db/used_cars.db'

if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print(f"✅ Removido: {db_path}")
    except Exception as e:
        print(f"❌ Erro ao remover: {e}")
        # Tentar renomear
        try:
            new_name = f"{db_path}.old.{int(time.time())}"
            os.rename(db_path, new_name)
            print(f"✅ Renomeado para: {new_name}")
        except Exception as e2:
            print(f"❌ Erro ao renomear: {e2}")
else:
    print("Banco não existe")
