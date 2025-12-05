# Sistema de Busca de Carros Usados

Demonstração prática de três algoritmos de busca aplicados em uma base de 5.000 carros usados.

## 🚀 Como Executar

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Iniciar o Servidor
```bash
python src/app.py
```

### 3. Acessar no Navegador
```
http://localhost:5000
```

## 📊 Algoritmos Implementados

| Algoritmo | Complexidade | Descrição |
|-----------|--------------|-----------|
| **Sequencial** | O(n) | Percorre todos os registros linearmente |
| **Indexada** | O(log n) | Usa índice em memória para busca rápida |
| **HashMap** | O(1) | Acesso direto via tabela hash |

## 📁 Estrutura do Projeto

```
TrabalhoDana/
├── db/
│   ├── used_cars.csv      # Base de dados (5.000 carros)
│   └── hashmap.pickle     # HashMap otimizado
├── src/
│   ├── app.py             # Servidor Flask
│   ├── search_utils.py    # Algoritmos de busca
│   ├── build_hash.py      # Construtor do HashMap
│   └── static/            # Interface web (HTML/CSS/JS)
└── requirements.txt       # Dependências Python
```

## 🔧 Tecnologias

- Python 3.10+
- Flask (servidor web)
- Pandas (manipulação de dados)
- HTML/CSS/JavaScript (interface)

## 📝 Funcionalidades

- ✅ Busca por marca ou modelo
- ✅ Comparação de performance entre algoritmos
- ✅ Catálogo paginado (250 páginas)
- ✅ Interface responsiva
- ✅ 5.000 registros reais

---

**Desenvolvido para a disciplina de Estruturas de Dados**