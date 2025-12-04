"""
Script para gerar o arquivo used_cars.csv com 5.000 registros de carros usados
"""
import csv
import random
from pathlib import Path

# Dados realistas de marcas e modelos
brands_models = {
    "Toyota": ["Corolla", "Camry", "RAV4", "Hilux", "Prius", "Yaris", "Avalon", "Tacoma", "4Runner", "Sienna"],
    "Honda": ["Civic", "Accord", "CR-V", "Fit", "HR-V", "Pilot", "Odyssey", "Ridgeline", "Passport", "Insight"],
    "Ford": ["Focus", "Fiesta", "Mustang", "F-150", "Explorer", "Escape", "Fusion", "Ranger", "Edge", "Expedition"],
    "Chevrolet": ["Cruze", "Malibu", "Silverado", "Equinox", "Traverse", "Camaro", "Colorado", "Tahoe", "Suburban", "Blazer"],
    "Volkswagen": ["Golf", "Jetta", "Passat", "Tiguan", "Atlas", "Beetle", "Arteon", "ID.4", "Taos", "Polo"],
    "Nissan": ["Sentra", "Altima", "Maxima", "Versa", "Rogue", "Murano", "Pathfinder", "Frontier", "Titan", "Kicks"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Kona", "Palisade", "Accent", "Venue", "Ioniq", "Veloster"],
    "Kia": ["Forte", "Optima", "Sorento", "Sportage", "Telluride", "Soul", "Stinger", "Seltos", "Rio", "Carnival"],
    "BMW": ["320i", "330i", "M3", "X1", "X3", "X5", "X7", "530i", "740i", "Z4"],
    "Mercedes-Benz": ["C-Class", "E-Class", "S-Class", "GLA", "GLC", "GLE", "GLS", "A-Class", "CLA", "AMG GT"],
    "Audi": ["A3", "A4", "A6", "A8", "Q3", "Q5", "Q7", "Q8", "TT", "R8"],
    "Mazda": ["Mazda3", "Mazda6", "CX-3", "CX-5", "CX-9", "MX-5 Miata", "CX-30", "CX-50", "Mazda2", "RX-8"],
    "Subaru": ["Impreza", "Legacy", "Outback", "Forester", "Crosstrek", "Ascent", "WRX", "BRZ", "XV", "Tribeca"],
    "Jeep": ["Wrangler", "Cherokee", "Grand Cherokee", "Compass", "Renegade", "Gladiator", "Commander", "Patriot", "Liberty", "Wagoneer"],
    "Dodge": ["Charger", "Challenger", "Durango", "Journey", "Grand Caravan", "Ram 1500", "Dart", "Viper", "Nitro", "Magnum"],
    "Lexus": ["ES", "IS", "GS", "LS", "NX", "RX", "GX", "LX", "UX", "RC"],
    "Acura": ["ILX", "TLX", "RLX", "MDX", "RDX", "NSX", "TSX", "RSX", "Integra", "Legend"],
    "Infiniti": ["Q50", "Q60", "Q70", "QX50", "QX60", "QX80", "G35", "G37", "FX35", "M35"],
    "Volvo": ["S60", "S90", "V60", "V90", "XC40", "XC60", "XC90", "C40", "S40", "V40"],
    "Fiat": ["500", "Uno", "Palio", "Punto", "Toro", "Mobi", "Argo", "Cronos", "Strada", "Ducato"],
    "Renault": ["Sandero", "Logan", "Duster", "Kwid", "Captur", "Clio", "Megane", "Fluence", "Oroch", "Koleos"],
    "Peugeot": ["208", "2008", "3008", "5008", "308", "408", "508", "Partner", "Expert", "Boxer"],
    "Citroën": ["C3", "C4", "C4 Cactus", "Berlingo", "Jumpy", "SpaceTourer", "C5 Aircross", "C-Elysee", "DS3", "DS4"],
    "Mitsubishi": ["Lancer", "Outlander", "Eclipse Cross", "Pajero", "L200", "ASX", "Mirage", "Galant", "Montero", "3000GT"],
    "Land Rover": ["Range Rover", "Range Rover Sport", "Discovery", "Discovery Sport", "Defender", "Evoque", "Velar", "Freelander", "LR4", "LR2"]
}

# Anos disponíveis
years = list(range(2010, 2025))

# Função para gerar preço baseado em marca, ano e modelo
def generate_price(brand, year, model):
    base_prices = {
        "Toyota": 25000, "Honda": 24000, "Ford": 23000, "Chevrolet": 22000,
        "Volkswagen": 21000, "Nissan": 20000, "Hyundai": 19000, "Kia": 18000,
        "BMW": 45000, "Mercedes-Benz": 50000, "Audi": 47000, "Mazda": 22000,
        "Subaru": 26000, "Jeep": 30000, "Dodge": 28000, "Lexus": 42000,
        "Acura": 38000, "Infiniti": 40000, "Volvo": 39000, "Fiat": 15000,
        "Renault": 16000, "Peugeot": 17000, "Citroën": 16500, "Mitsubishi": 21000,
        "Land Rover": 60000
    }
    
    base = base_prices.get(brand, 20000)
    age_factor = (2024 - year) * 0.08  # 8% de depreciação por ano
    depreciation = 1 - age_factor
    
    # Adiciona variação aleatória
    variation = random.uniform(0.85, 1.15)
    
    price = int(base * depreciation * variation)
    return max(5000, price)  # Preço mínimo de $5,000

# Gerar 5000 registros
print("Gerando 5.000 registros de carros usados...")

output_path = Path(__file__).parent / "db" / "used_cars.csv"
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'brand', 'model', 'year', 'price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for i in range(1, 5001):
        brand = random.choice(list(brands_models.keys()))
        model = random.choice(brands_models[brand])
        year = random.choice(years)
        price = generate_price(brand, year, model)
        
        writer.writerow({
            'id': i,
            'brand': brand,
            'model': model,
            'year': year,
            'price': price
        })
        
        if i % 500 == 0:
            print(f"Progresso: {i}/5000 registros gerados")

print(f"\n✅ Arquivo CSV gerado com sucesso em: {output_path}")
print(f"Total de registros: 5.000")
