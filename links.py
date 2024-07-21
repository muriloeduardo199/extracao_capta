import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import psycopg2
from sqlmodel import SQLModel, Field, create_engine, Session
from criacao_tabela import Oportunidade


# Conectar ao banco de dados PostgreSQL
user = 'postgres'
password = 'postgres'  # Certifique-se de que a senha está correta e é UTF-8
host = 'localhost'
dbname = 'dados_capta'
DATABASE_URL = f"postgresql://{user}:{password}@{host}/{dbname}"
engine = create_engine(DATABASE_URL)

# Criar as tabelas no banco de dados (se ainda não existirem)
SQLModel.metadata.create_all(engine)


# Inicializa o driver do Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abre a página web
driver.get('https://capta.org.br/fontes-de-financiamento/oportunidades/')
sleep(10)  # Aguarda a página carregar completamente

# Lista para armazenar os dados dos links
dados_links = []

# Encontrar todos os elementos 'a' dentro dos parágrafos na estrutura especificada
links = driver.find_elements(By.XPATH, '/html/body/div[5]/div[1]/div[3]/div[1]/div/p/a')
# Iterar sobre os elementos encontrados e extrair as informações
for link in links:
    texto_link = link.text
    url_link = link.get_attribute('href')
    dados_links.append({'Texto': texto_link, 'URL': url_link})

# Criar um DataFrame com os dados coletados
df_links = pd.DataFrame(dados_links)


# Função para inserir dados no banco de dados
def inserir_dados(df):
    with Session(engine) as session:
        for index, row in df.iterrows():
            oportunidade = Oportunidade(
                texto=row['Texto'],
                url=row['URL']
            )
            session.add(oportunidade)
        session.commit()

# Chamar a função para inserir os dados do DataFrame
inserir_dados(df_links)
