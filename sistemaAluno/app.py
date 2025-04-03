#bibliotecas
from sqlalchemy import create_engine, text
import pandas as pd
from pathlib import Path
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io


#configuraçoes
host = 'localhost'
port = '3306'
user = 'root'
senha = '2050'
database_name = 'db_escola'

BASE_DIR = Path(__file__).parent
DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URL)

#interface principal
st.title("Sistema Escolar")
menu = st.sidebar.selectbox("Selecione uma opção", ["Cadastro endereço", "Cadastro aluno", "Editar aluno", 'Cadastrar notas', 'Importar dados', 'Gerar PDF'])

# CADASTRAR ENDEREÇO 
def cadastrarEndereco(params):
    sql = text("""
        INSERT INTO tb_enderecos (cep, endereco, cidade, estado)
        VALUES (:cep, :endereco, :cidade, :estado)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)

#streamlit para cadastrar endereço
if menu == "Cadastro endereço":
    st.subheader("Cadastro de endereço")
    
    cep = st.text_input("Cadastre o CEP:")
    endereco = st.text_input("Cadastre o Endereço:")
    cidade = st.text_input("Cadastre a Cidade:")
    estado = st.text_input("Cadastre o Estado:")

    # Botão para confirmar o cadastro
    if st.button("Cadastrar Endereço"):
        params = {
            'cep': cep,
            'endereco': endereco,
            'cidade': cidade,
            'estado': estado,
        }
        cadastrarEndereco(params)
        st.success("Endereço cadastrado com sucesso!")

# CADASTRAR ALUNO
def cadastrarAluno(params):
    sql = text("""
        INSERT INTO tb_alunos (nome_aluno, email, cep, carro_id)
        VALUES (:nome_aluno, :email, :cep, :carro_id)
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)

#streamlit para cadastrar alunos

if menu == "Cadastro aluno":
    st.subheader("Cadastro de alunos")

    nome = st.text_input("cadastre o aluno: ")
    email = st.text_input("cadastre o email: ")
    cep = st.text_input("cadastre o cep: ")
    carro = st.text_input("cadastre o carro")

    # Botão para confirmar o cadastro
    if st.button("Cadastrar aluno"):
        params = {
            'nome_aluno': nome,
            'email': email, 
            'cep': cep, 
            'carro_id': carro
        }
        cadastrarAluno(params)
        st.success("Aluno cadastrado com sucesso!")

# EDITAR ALUNOS

def EditarAluno(ID,nome_aluno= None,email = None, cep = None , carro_id = None):
    campos_para_atualizar =[]
    params={"ID":ID}
    if nome_aluno:
        campos_para_atualizar.append("nome_aluno = :nome_aluno")
        params["nome_aluno"] = nome_aluno
    if email:
        campos_para_atualizar.append("email = :email")
        params["email"] = email
    if nome_aluno:
        campos_para_atualizar.append("cep = :cep")
        params["cep"] = cep
    if nome_aluno:
        campos_para_atualizar.append("carro_id = :carro_id")
        params["carro_id"] = carro_id
    if not campos_para_atualizar:
            return "Nenhum campo para atualizar."

    sql = text(f"""
        UPDATE tb_alunos
        SET {", ".join(campos_para_atualizar)}
        WHERE ID = :ID
    """)
    with engine.begin() as conn:
        conn.execute(sql, params)

    return "Aluno atualizado com sucesso!"

#streamlit para editar alunos

#lista vizualização de ID
sql=text("""
select * from tb_alunos
""")
idAluno = pd.read_sql(sql, con=engine)
cols = ['nome_aluno']
idAluno = idAluno[cols]
idAluno.index.name = "ID"
idAluno.set_index(idAluno.index + 1, inplace=True)
idAluno.rename(columns={'nome_aluno': 'nome do Aluno'}, inplace=True)

if menu == "Editar aluno":

    st.subheader("Editar aluno")
    
    id = st.text_input("qual o Id:")
    st.dataframe(idAluno)
    nome = st.text_input("cadastre o aluno: ")
    email = st.text_input("cadastre o email: ")
    cep = st.text_input("cadastre o cep: ")
    carro = st.text_input("cadastre o carro")

    # Botão para confirmar o cadastro
    if st.button("Atualizar Aluno"):
        if id:
            EditarAluno(id, nome_aluno=nome, email=email, cep=cep, carro_id=carro)
            st.success(f"Aluno ID {id} atualizado com sucesso!")
        else:
            st.error("Por favor, insira um ID válido.")

#CADASTRAR NOTA

# lista alunos
sql = text("SELECT id, nome_aluno FROM tb_alunos")
dfAlunos = pd.read_sql(sql, con=engine)
dfAlunos.rename(columns={'id': 'ID', 'nome_aluno': 'nome'}, inplace=True)
dfAlunos.set_index("ID", inplace=True)

# lista disciplinas
sql = text("SELECT id, nome_disciplina FROM tb_disciplinas")
dfDisciplinas = pd.read_sql(sql, con=engine)
dfDisciplinas.rename(columns={'id': 'ID', 'nome_disciplina': 'disciplina'}, inplace=True)
dfDisciplinas.set_index("ID", inplace=True)

def cadastrarNota(alunoID, disciplinaID, nota):
    sql = text("""
        INSERT INTO tb_notas (aluno_id, disciplina_id, nota)
        VALUES (:aluno_id, :disciplina_id, :nota)
    """)
    params = {'aluno_id': alunoID, 'disciplina_id': disciplinaID, 'nota': nota}
    with engine.begin() as conn:
        conn.execute(sql, params)

# streamlit para cadastrar notas
if menu == "Cadastrar notas":
    st.subheader("Cadastro de notas")

    st.write("Selecione um Aluno")
    alunoSelecionado = st.selectbox("Clique no aluno:", dfAlunos.index, format_func=lambda x: dfAlunos.loc[x, "nome"])

    st.write("Selecione uma Disciplina")
    disciplinaSelecionada = st.selectbox("Clique na disciplina:", dfDisciplinas.index, format_func=lambda x: dfDisciplinas.loc[x, "disciplina"])

    nota = st.number_input("Insira a nota:", min_value=0.0, max_value=10.0, step=0.1)

    if st.button("Cadastrar Nota"):
        cadastrarNota(alunoSelecionado, disciplinaSelecionada, nota)
        st.success("Nota cadastrada com sucesso!")


#IMPORTA DADOS DE ARQUIVO

# streamlit importar dados 
if menu == "Importar dados":
    st.subheader("Importar arquivo ")

    # Upload do arquivo
    arquivo = st.file_uploader("Selecione um arquivo (.csv, .xlsx ou .json)", type=["csv", "xlsx", "json"])

    # Buscar nomes das tabelas do banco de dados
    with engine.connect() as conn:
        tabelas = conn.execute(text("SHOW TABLES")).fetchall()
        listaTabelas = [t[0] for t in tabelas if t[0].startswith("tb_")]


    # Dropdown com as tabelas existentes
    tabelaSelecionada = st.selectbox("Selecione a tabela para importar:", listaTabelas)

    # Ler o arquivo com pandas conforme o tipo
    if arquivo:
        if arquivo.name.endswith(".csv"):
            df = pd.read_csv(arquivo)
        elif arquivo.name.endswith(".xlsx"):
            df = pd.read_excel(arquivo)
        elif arquivo.name.endswith(".json"):
            df = pd.read_json(arquivo)

        # Mostrar os dados
        st.write("Pré-visualização dos dados:")
        st.dataframe(df)

        # Botão para importar os dados
        if st.button("Importar para o banco"):
            df.to_sql(tabelaSelecionada, con=engine, if_exists='append', index=False)


# GERAR PDF

if menu == "Gerar PDF":
    st.subheader("Gerar PDF ")

    # Dropdown para escolher a tabela
    with engine.connect() as conn:
        tabelas = conn.execute(text("SHOW TABLES")).fetchall()
        listaTabelas = [t[0] for t in tabelas if t[0].startswith("tb_")]
    tabelaSelecionada = st.selectbox("Escolha a tabela:", listaTabelas)

    if st.button("Gerar PDF"):

        df = pd.read_sql(f"SELECT * FROM {tabelaSelecionada}", con=engine)

        # Cria o PDF em memória
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elementos = []

        estilos = getSampleStyleSheet()
        elementos.append(Paragraph(f"Relatório da tabela: {tabelaSelecionada}", estilos["Title"]))
        elementos.append(Spacer(1, 12))

        # Prepara os dados para a tabela do PDF
        dados = [df.columns.tolist()] + df.astype(str).values.tolist()

        tabela_pdf = Table(dados)
        tabela_pdf.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ]))

        elementos.append(tabela_pdf)
        doc.build(elementos)

        buffer.seek(0)
        st.download_button(
            label="📄 Baixar PDF",
            data=buffer,
            file_name=f"{tabelaSelecionada}_relatorio.pdf",
            mime="application/pdf"
        )
