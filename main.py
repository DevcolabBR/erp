import json
import pandas as pd
from sqlalchemy import create_engine

class Produto:
    def __init__(self, nome, quantidade, preco):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

class Crediario:
    def __init__(self, cliente, valor, parcelas):
        self.cliente = cliente
        self.valor = valor
        self.parcelas = parcelas

class GerenciamentoEstoque:
    def __init__(self):
        self.estoque = {}

    def cadastrar_produto(self, nome, quantidade, preco):
        if nome in self.estoque:
            print(f"Produto {nome} já cadastrado.")
        else:
            self.estoque[nome] = Produto(nome, quantidade, preco)
            print(f"Produto {nome} cadastrado com sucesso.")

    def atualizar_estoque(self, nome, quantidade):
        if nome in self.estoque:
            self.estoque[nome].quantidade += quantidade
            print(f"Estoque do produto {nome} atualizado.")
        else:
            print(f"Produto {nome} não encontrado.")

    def verificar_estoque_baixo(self, limite):
        produtos_baixo_estoque = [produto for produto in self.estoque.values() if produto.quantidade < limite]
        if produtos_baixo_estoque:
            print("Produtos com estoque baixo:")
            for produto in produtos_baixo_estoque:
                print(f"{produto.nome}: {produto.quantidade} unidades")
        else:
            print("Nenhum produto com estoque baixo.")

    def gerar_relatorio(self):
        relatorio = {nome: {"quantidade": produto.quantidade, "preco": produto.preco} for nome, produto in self.estoque.items()}
        with open('relatorio_estoque.json', 'w') as file:
            json.dump(relatorio, file, indent=4)
        print("Relatório de estoque gerado com sucesso.")

class GerenciamentoCrediario:
    def __init__(self):
        self.crediarios = []

    def cadastrar_crediario(self, cliente, valor, parcelas):
        self.crediarios.append(Crediario(cliente, valor, parcelas))
        print(f"Crediário para {cliente} cadastrado com sucesso.")

    def gerar_relatorio(self):
        relatorio = [{"cliente": crediario.cliente, "valor": crediario.valor, "parcelas": crediario.parcelas} for crediario in self.crediarios]
        with open('relatorio_crediarios.json', 'w') as file:
            json.dump(relatorio, file, indent=4)
        print("Relatório de crediários gerado com sucesso.")

def importar_arquivo(file_path):
    if file_path.endswith('.json'):
        data = pd.read_json(file_path)
    elif file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Formato de arquivo não suportado.")
    return data

def alocar_no_banco(data, table_name, db_url='sqlite:///estoque.db'):
    engine = create_engine(db_url)
    data.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Dados alocados na tabela {table_name} com sucesso.")

if __name__ == "__main__":
    sistema = GerenciamentoEstoque()
    sistema_crediario = GerenciamentoCrediario()
    
    escolha = input("Deseja importar produtos, crediários ou adicionar manualmente? (importar/adicionar): ").strip().lower()
    
    if escolha == "importar":
        tipo = input("Deseja importar produtos ou crediários? (produtos/crediarios): ").strip().lower()
        file_path = input("Digite o caminho do arquivo: ").strip()
        data = importar_arquivo(file_path)
        if tipo == "produtos":
            for _, row in data.iterrows():
                sistema.cadastrar_produto(row['nome'], row['quantidade'], row['preco'])
            alocar_no_banco(data, 'produtos')
        elif tipo == "crediarios":
            for _, row in data.iterrows():
                sistema_crediario.cadastrar_crediario(row['cliente'], row['valor'], row['parcelas'])
            alocar_no_banco(data, 'crediarios')
    elif escolha == "adicionar":
        tipo = input("Deseja adicionar produtos ou crediários? (produtos/crediarios): ").strip().lower()
        if tipo == "produtos":
            while True:
                nome = input("Digite o nome do produto: ").strip()
                quantidade = int(input("Digite a quantidade do produto: ").strip())
                preco = float(input("Digite o preço do produto: ").strip())
                sistema.cadastrar_produto(nome, quantidade, preco)
                continuar = input("Deseja adicionar outro produto? (s/n): ").strip().lower()
                if continuar != 's':
                    break
        elif tipo == "crediarios":
            while True:
                cliente = input("Digite o nome do cliente: ").strip()
                valor = float(input("Digite o valor do crediário: ").strip())
                parcelas = int(input("Digite o número de parcelas: ").strip())
                sistema_crediario.cadastrar_crediario(cliente, valor, parcelas)
                continuar = input("Deseja adicionar outro crediário? (s/n): ").strip().lower()
                if continuar != 's':
                    break
    
    sistema.verificar_estoque_baixo(20)
    sistema.gerar_relatorio()
    sistema_crediario.gerar_relatorio()