import os
import sqlite3

db_path = 'db/used_cars.db'

# Fechar todas as conexões possíveis
import gc
gc.collect()

# Deletar se existir
for i in range(3):
    try:
        if os.path.exists(db_path):
            os.unlink(db_path)
            print(f"Tentativa {i+1}: Deletado")
            break
    except Exception as e:
        print(f"Tentativa {i+1}: {e}")
        import time
        time.sleep(0.5)

print("Pronto")
