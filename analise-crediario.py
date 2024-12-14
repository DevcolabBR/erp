#%%
import pandas as pd
import json
from datetime import datetime, timedelta
#%%
# Caminho do arquivo JSON
file_path = 'crediarios.json'

# Leitura do arquivo JSON
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Transformação em DataFrame
df = pd.DataFrame(data)

# Exibir as primeiras linhas do DataFrame
df.head()
# %%
df[['valor', 'entrada', 'parcelas', 'data', 'cpf', 'vendedor']]
# %%
df['valor_atualizado'] = df['valor'] - df['entrada']
# %%
df
# %%
df['valor_parcela'] = (df['valor_atualizado'] / df['parcelas']).round(2)
# %%
df
# %%
df['valor_parcela'] = df['valor_parcela'].round(2)
# %%
df
# %%
# Criar um DataFrame com as datas de cobrança
df_cobrancas = pd.DataFrame()

# Repetir as datas de cobrança para cada parcela
cobrancas_list = []
for index, row in df.iterrows():
    data_base = datetime.strptime(row['data'], '%Y-%m-%d %H:%M:%S')
    for parcela in range(1, row['parcelas'] + 1):
        data_cobranca = data_base + timedelta(days=30 * (parcela - 1))
        cobrancas_list.append({
            'data': data_cobranca.strftime('%d-%m-%Y'),
            'parcela': parcela,
            'valor_parcela': row['valor_parcela'],
            'cliente': row['cpf'],
            'vendedor': row['vendedor']
        })

df_cobrancas = pd.concat([df_cobrancas, pd.DataFrame(cobrancas_list)], ignore_index=True)

# Exibir o DataFrame de cobranças
df_cobrancas
# %%
df_cobrancas

# %%
df_cobrancas.sort_values('data')
# %%
