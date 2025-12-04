# USED CARS SEARCH — Demonstração de Algoritmos de Busca

## 📋 Descrição do Projeto

Este projeto implementa três tipos diferentes de algoritmos de busca em uma base de dados de carros usados:

1. **Busca Sequencial** - Percorre todos os registros linearmente
2. **Busca Indexada** - Utiliza índices do banco de dados SQLite
3. **Busca com HashMap** - Usa estrutura de dados em memória para busca rápida

## 🎯 Requisitos do Sistema

- Python 3.7 ou superior
- Dataset CSV com no mínimo 5.000 registros de carros usados

## 📦 Instalação e Configuração

### 1. Criar Ambiente Virtual

```bash
python -m venv venv
```

### 2. Ativar o Ambiente Virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Dataset Incluído

✅ **O arquivo CSV já está incluído no projeto!**

- Localização: `db/used_cars.csv`
- Total de registros: **5.000 carros usados**
- Campos: id, brand, model, year, price
- Gerado com dados realistas de 25 marcas diferentes

**Não é necessário baixar nenhum dataset do Kaggle.** O arquivo já contém os 5.000 registros exigidos e está pronto para uso.

### 5. Construir o HashMap (Opcional mas Recomendado)

Para melhor performance da busca com HashMap, execute:

```bash
python src/build_hash.py
```

Este comando irá:
- Ler todos os registros do CSV
- Criar um dicionário (HashMap) organizado por modelo
- Persistir o HashMap em `db/hashmap.pickle`

**Nota:** Se não executar este passo, o HashMap será criado automaticamente na primeira busca.

### 6. Executar a Aplicação

Inicie o servidor Flask:

```bash
python src/app.py
```

### 7. Acessar no Navegador

Abra seu navegador e acesse:
```
http://localhost:5000
```

## 🔍 Como Usar

A interface possui três seções, uma para cada tipo de busca:

### Busca Sequencial
- Digite o nome do modelo ou marca
- Clique em "Buscar (Sequencial)"
- O sistema percorre todos os registros linearmente

### Busca Indexada
- Digite o nome do modelo ou marca
- Clique em "Buscar (Indexada)"
- O sistema usa índices SQL para busca otimizada

### Busca HashMap
- Digite o nome do modelo ou marca
- Clique em "Buscar (HashMap)"
- O sistema busca diretamente na estrutura em memória

## 📊 Explicação dos Algoritmos

### 1. Busca Sequencial (Linear Search)
- **Complexidade:** O(n)
- **Funcionamento:** Percorre todos os registros um por um comparando com o termo buscado
- **Vantagem:** Simples de implementar
- **Desvantagem:** Lenta para grandes volumes de dados

### 2. Busca Indexada (Indexed Search)
- **Complexidade:** O(log n)
- **Funcionamento:** Utiliza índices do banco de dados SQLite para acelerar a busca
- **Vantagem:** Muito mais rápida que a busca sequencial
- **Desvantagem:** Requer índices criados previamente

### 3. Busca HashMap (Hash-based Search)
- **Complexidade:** O(1) no caso médio
- **Funcionamento:** Usa uma tabela hash onde a chave é o modelo do carro
- **Vantagem:** Busca extremamente rápida
- **Desvantagem:** Requer mais memória e pré-processamento

## 📁 Estrutura do Projeto

```
used-cars-project/
├─ data/
│  └─ used_cars.csv          # Dataset do Kaggle (adicionar manualmente)
├─ db/
│  ├─ used_cars.db           # Banco SQLite (gerado automaticamente)
│  └─ hashmap.pickle         # HashMap persistido (gerado automaticamente)
├─ src/
│  ├─ app.py                 # Servidor Flask principal
│  ├─ db_setup.py            # Cria tabela e importa CSV
│  ├─ build_hash.py          # Constrói HashMap
│  ├─ search_utils.py        # Implementação das 3 buscas
│  └─ static/
│     ├─ index.html          # Interface web
│     └─ js/
│        └─ main.js          # Lógica do front-end
├─ requirements.txt          # Dependências Python
└─ README.md                 # Este arquivo
```

## 🐛 Solução de Problemas

### Erro: "CSV deve conter no mínimo 5000 registros"
- Verifique se o arquivo CSV possui dados suficientes
- Baixe um dataset maior do Kaggle

### Erro: "FileNotFoundError: data/used_cars.csv"
- Certifique-se de que o arquivo CSV está na pasta `data/`
- Verifique se o nome do arquivo é exatamente `used_cars.csv`

### Erro ao executar app.py
- Verifique se executou `db_setup.py` primeiro
- Verifique se executou `build_hash.py` depois
- Certifique-se de que o ambiente virtual está ativado

## 👨‍🎓 Informações Acadêmicas

- **Trabalho:** Individual
- **Disciplina:** Estruturas de Dados
- **Objetivo:** Demonstrar na prática diferentes algoritmos de busca
- **Tecnologias:** Python, Flask, SQLite, HTML, CSS, JavaScript

## 📝 Notas

- O sistema funciona 100% offline após configuração inicial
- A mesma base de dados é usada nas 3 implementações
- O dataset deve conter no mínimo 5.000 registros reais
- Todos os arquivos são criados automaticamente, exceto o CSV do Kaggle
