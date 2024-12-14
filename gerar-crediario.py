#%%
import json
import random
from datetime import datetime, timedelta

# Function to generate random CPF
def generate_cpf():
    return f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"

# Function to generate random date
def generate_date():
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    return start_date + (end_date - start_date) * random.random()

# Function to generate random crediario
def generate_crediario():
    valor = round(random.uniform(50, 2000), 2)
    entrada = round(random.uniform(20, min(500, valor)), 2)
    return {
        "data": generate_date().strftime("%Y-%m-%d %H:%M:%S"),
        "valor": valor,
        "cpf": generate_cpf(),
        "cidade": random.choice(["Belém", "Ananindeua", "Santarém", "Marabá", "Castanhal"]),
        "produto": random.choice(["Camiseta", "Calça", "Vestido", "Jaqueta", "Sapato"]),
        "id_do_produto": random.randint(1000, 9999),
        "parcelas": random.randint(1, 12),
        "entrada": entrada,
        "vendedor": random.choice(["João", "Maria", "Pedro", "Ana", "Carlos"])
    }

# Generate multiple crediarios
crediarios = [generate_crediario() for _ in range(100)]

# Write to JSON file
with open('crediarios.json', 'w') as f: 
    json.dump(crediarios, f, ensure_ascii=False, indent=4)

print("Arquivo crediarios.json gerado com sucesso!")
# %%
