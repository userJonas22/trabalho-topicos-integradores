import sqlite3
import os

# Função para criar um banco de dados SQLite com as tabelas Pessoa e Conta
def criar_banco_dados():
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()

    # Tabela Pessoa
    cursor.execute('''CREATE TABLE IF NOT EXISTS Pessoa
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       cpf TEXT NOT NULL,
                       primeiro_nome TEXT NOT NULL,
                       nome_do_meio TEXT,
                       sobrenome TEXT NOT NULL,
                       idade INTEGER,
                       conta INTEGER,
                       FOREIGN KEY (conta) REFERENCES Conta(id))''')

    # Tabela Conta
    cursor.execute('''CREATE TABLE IF NOT EXISTS Conta
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       agencia TEXT NOT NULL,
                       numero TEXT NOT NULL,
                       saldo REAL,
                       gerente INTEGER,
                       titular INTEGER,
                       FOREIGN KEY (gerente) REFERENCES Pessoa(id),
                       FOREIGN KEY (titular) REFERENCES Pessoa(id))''')

    conn.commit()
    conn.close()


# Função para ler dados de um arquivo de texto e inserir no banco de dados
def inserir_dados_pessoa(nome_arquivo):
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()

    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas[1:]:  # Ignorar a primeira linha com cabeçalho
            partes = linha.strip().split(" ")
            cpf, primeiro_nome, nome_do_meio, sobrenome, idade, conta = partes
            cursor.execute("INSERT INTO Pessoa (cpf, primeiro_nome, nome_do_meio, sobrenome, idade, conta) VALUES (?, ?, ?, ?, ?, ?)",
                           (cpf, primeiro_nome, nome_do_meio, sobrenome, idade, conta))

    conn.commit()
    conn.close()


# Função para ler dados de um arquivo de texto e inserir na tabela Conta
def inserir_dados_conta(nome_arquivo):
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()

    with open(nome_arquivo, "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas[1:]:  # Ignorar a primeira linha com cabeçalho
            partes = linha.strip().split(" ")
            agencia, numero, saldo, gerente, titular = partes
            cursor.execute("INSERT INTO Conta (agencia, numero, saldo, gerente, titular) VALUES (?, ?, ?, ?, ?)",
                           (agencia, numero, saldo, gerente, titular))

    conn.commit()
    conn.close()


# ---- CRUD Pessoa ------

# Função para criar uma nova pessoa
def criar_pessoa(cpf, primeiro_nome, nome_do_meio, sobrenome, idade):
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Pessoa (cpf, primeiro_nome, nome_do_meio, sobrenome, idade) VALUES (?, ?, ?, ?, ?)",
                   (cpf, primeiro_nome, nome_do_meio, sobrenome, idade))
    conn.commit()
    conn.close()


# Função para excluir uma pessoa pelo ID
def excluir_pessoa(id):
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Pessoa WHERE id=?", (id,))
    conn.commit()
    conn.close()


# Função para atualizar informações de uma pessoa
def atualizar_pessoa(id, cpf, primeiro_nome, nome_do_meio, sobrenome, idade):
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Pessoa SET cpf=?, primeiro_nome=?, nome_do_meio=?, sobrenome=?, idade=? WHERE id=?",
                   (cpf, primeiro_nome, nome_do_meio, sobrenome, idade, id))
    conn.commit()
    conn.close()


# ------ CRUD Conta ---------

# Função para criar uma nova conta
def criar_conta(agencia, numero, saldo, gerente, titular):
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Conta (agencia, numero, saldo, gerente, titular) VALUES (?, ?, ?, ?, ?)",
                   (agencia, numero, saldo, gerente, titular))
    conn.commit()
    conn.close()


# Função para excluir uma conta pelo ID
def excluir_conta(id):
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Conta WHERE id=?", (id,))
    conn.commit()
    conn.close()


# Função para atualizar informações de uma conta
def atualizar_conta(id, agencia, numero, saldo, gerente, titular):
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Conta SET agencia=?, numero=?, saldo=?, gerente=?, titular=? WHERE id=?",
                   (agencia, numero, saldo, gerente, titular, id))
    conn.commit()
    conn.close()


# ---- Consultar e guardar resultados em pastas e arquivos txt

# Função para realizar consultas e salvar os resultados em arquivos TXT
def consultar_e_salvar_resultados_pessoa(tipo_consulta, pesquisa):
    # Conectar ao banco de dados
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()
    
    # Certificar-se de que as pastas existem ou criá-las
    pasta = f"consulta_por_{tipo_consulta}"

    if not os.path.exists(pasta):
        os.makedirs(pasta)

    # Consulta no banco de dados
    cursor.execute(f"SELECT * FROM Pessoa WHERE {tipo_consulta}=?", ({pesquisa},))
    resultados = cursor.fetchall()
    salvar_resultados(resultados, f"consulta_por_{tipo_consulta}/resultado_{pesquisa}.txt")

    # Fechar a conexão com o banco de dados
    conn.close()


# Função para realizar consultas e salvar os resultados em arquivos TXT
def consultar_e_salvar_resultados_conta(tipo_consulta, pesquisa):
    # Conectar ao banco de dados
    conn = sqlite3.connect("banco_dados.db")
    cursor = conn.cursor()
    
    # Certificar-se de que as pastas existem ou criá-las
    pasta = f"consulta_por_{tipo_consulta}"

    if not os.path.exists(pasta):
        os.makedirs(pasta)

    # Consulta no banco de dados
    cursor.execute(f"SELECT * FROM Conta WHERE {tipo_consulta}=?", ({pesquisa},))
    resultados = cursor.fetchall()
    salvar_resultados(resultados, f"consulta_por_{tipo_consulta}/resultado_{pesquisa}.txt")

    # Fechar a conexão com o banco de dados
    conn.close()


# Função para salvar resultados em um arquivo TXT
def salvar_resultados(resultados, nome_arquivo):
    with open(nome_arquivo, "w") as arquivo:
        for resultado in resultados:
            arquivo.write(f"{resultado}\n")


# ---- Ler e Imprimir as consultas salvas nas pastas

# Função para ler e imprimir arquivos em uma pasta
def ler_e_imprimir_arquivos_na_pasta(pasta):
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith(".txt"):
            caminho_arquivo = os.path.join(pasta, nome_arquivo)
            with open(caminho_arquivo, "r") as arquivo:
                conteudo = arquivo.read()
                print(f"Conteúdo do arquivo '{nome_arquivo}':\n{conteudo}\n")



# ---------- Função principal para execução das funcionalidades -----------
 
def main():
    criar_banco_dados()
    inserir_dados_pessoa("nomes.txt")
    inserir_dados_conta("contas.txt")

    criar_pessoa() # colocar nos parenteses os dados da pessoa
    excluir_pessoa() # colocar o id da pessoa para excluir
    atualizar_pessoa() # colocar o id da pessoa e os novos dados

    criar_conta() # colocar nos parenteses os dados da conta
    excluir_conta() # colocar o id da conta para excluir
    atualizar_conta() # colocar o id da conta e os novos dados

    consultar_e_salvar_resultados_pessoa() # colocar o tipo de consulta (ex: primeiro_nome) e o que deseja pesquisar
    consultar_e_salvar_resultados_conta() # colocar o tipo de consulta (ex: agencia) e o que deseja pesquisar

    ler_e_imprimir_arquivos_na_pasta() # Colocar o nome da pasta


if __name__ == "__main__":
    main()
  
