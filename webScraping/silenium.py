from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
from sqlalchemy import create_engine, text
import pandas as pd
from pathlib import Path


# perguntas ao usuário
tipo = input("tipo de transação (ex: ALUGUEL ou VENDA): ").upper()
tipos = input("tipo de imóvel (ex: CASA, APARTAMENTO): ").upper()
estado = input("estado (ex: GO, DF): ").upper()
cidade = input("cidade (ex: GOIANIA, GAMA): ").upper()
quartos = input("quantidade de quartos (ex: 4): ").strip()

# configurações iniciais
options = Options()
url = 'https://www.dfimoveis.com.br/'
driver = webdriver.Chrome(options=options)
driver.get(url)
wait = WebDriverWait(driver, 10)

# tipo usando xpath
xpath = "/html/body/main/div[1]/section/section[1]/div[2]/div/form/div[1]/div[1]/span/span[1]/span"
element = wait.until(EC.element_to_be_clickable((By.XPATH,xpath)))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"select2-search__field")))
element.send_keys(tipo)
element.send_keys(Keys.ENTER)

# tipos 
element = wait.until(EC.element_to_be_clickable((By.ID, 'select2-tipos-container')))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"select2-search__field")))
element.send_keys(tipos)
element.send_keys(Keys.ENTER)

# estado 
element = wait.until(EC.element_to_be_clickable((By.ID, 'select2-estados-container')))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"select2-search__field")))
element.send_keys(estado)
element.send_keys(Keys.ENTER)

# cidade 
element = wait.until(EC.element_to_be_clickable((By.ID, 'select2-cidades-container')))
element.click()
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"select2-search__field")))
element.send_keys(cidade)
element.send_keys(Keys.ENTER)

# quartos
element = wait.until(EC.element_to_be_clickable((By.ID, 'select2-quartos-container')))
element.click()
opcoesQuartos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'select2-results__option')))
for opcao in opcoesQuartos:
    if opcao.text.strip() == quartos:
        opcao.click()
        break

# buscar 
busca = wait.until(EC.element_to_be_clickable((By.ID,"botaoDeBusca")))
busca.click()

# resultado
lst_imoveis = []

while True:

    resultado = wait.until(EC.presence_of_element_located((By.ID, "resultadoDaBuscaDeImoveis")))
    elementos = resultado.find_elements(By.TAG_NAME, 'a')  # revalida os elementos a cada página

    for elem in elementos:
        imovel = {}
        imovel['titulo'] = elem.find_element(By.CLASS_NAME, 'new-title').text
        imovel['preco'] = elem.find_element(By.CLASS_NAME, 'new-price').text
        imovel['metragem'] = elem.find_element(By.CLASS_NAME, 'm-area').text
        imovel['quarto'] = quartos  # valor informado pelo usuário
        imovel['descricao'] = elem.find_element(By.CLASS_NAME, 'new-text').text
        lst_imoveis.append(imovel)

    # verifica e clica no botão "Próxima"
    botao_proximo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn.next')))
    if botao_proximo.get_attribute("class") == "btn disabled next":
        break

    # scroll até o botão
    driver.execute_script("arguments[0].scrollIntoView(true);", botao_proximo)
    sleep(1)

    # clique via JavaScript (ignora bloqueios visuais)
    driver.execute_script("arguments[0].click();", botao_proximo)
    sleep(2)


# dataframe com os dados
df = pd.DataFrame(lst_imoveis)
print(df)

# arrumar dados DataFrame
def limparPreco(valor):
    precoLimpo = valor.split("\n")[0]
    precoLimpo = precoLimpo.replace("R$", "").replace(".", "").strip()
    return precoLimpo

df["preco"] = df["preco"].apply(limparPreco)

def limparMetragem(tamanho):
    tamanhoLimpo = tamanho.replace("m²","").strip()
    return tamanhoLimpo

df["metragem"] = df["metragem"].apply(limparMetragem)

def limparQuartos(valor):
    return valor.strip()

df["quarto"] = df["quarto"].apply(limparQuartos)

#Inserir daddos no SQL 

host = 'localhost'
port = '3306'
user = 'root'
senha = '2050'
database_name = 'db_imoveis'

BASE_DIR = Path(__file__).parent
DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name}'
engine = create_engine(DATABASE_URL)

df.to_sql('tb_imoveis', con=engine, if_exists='append', index=False)








