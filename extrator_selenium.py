# -*- coding: utf-8 -*-
# Este programa realiza buscas na página de andamentos processuais do STF.

# Defina aqui a classe a ser buscada e um número inicial e final.
# O nome da classe é sensível a maiúsculas. Utilize a sigla constante da página do STF.
classe = 'ACO'
num_inicial = 1
num_final = 4000

# É possível definir uma lista de processos para processar. Esta, por exemplo, é a lista dos processos estruturais.
# Nese caso, desative as linhas 152 e 153 (inserindo um # que transforma o código em comentário) e ative as linhas 148 a 150.
# lista_processos = [ ['ACO', 442], ['ACO', 444], ['ACO', 648], ['ACO', 661], ['ACO', 669], ['ACO', 683], ['ACO', 701], ['ACO', 718], ['ACO', 2178], ['ACO', 2981], ['ACO', 3132], ['ACO', 3276], ['ACO', 3303], ['ACO', 3306], ['ACO', 3421], ['ACO', 3431], ['ACO', 3433], ['ACO', 3438], ['ACO', 3457],['ACO', 3459], ['ACO', 3494], ['ACO', 3518],['ACO', 3520], ['ACO', 3555], ['ACO', 3568], ['ACO', 3609], ['ACO', 3688], ['ADC', 87], ['ADI', 4916], ['ADI', 4917], ['ADI', 4918], ['ADI', 4920], ['ADI', 5038], ['ADI', 5621], ['ADI', 6553], ['ADI', 7191], ['ADI', 7433], ['ADI', 7471], ['ADI', 7483], ['ADI', 7486], ['ADI', 7487], ['ADI', 7582], ['ADI', 7583], ['ADI', 7586], ['ADO', 25], ['ADO', 86], ['ADPF', 165], ['ADPF', 568], ['ADPF', 635], ['ADPF', 709], ['ADPF', 743], ['ADPF', 746], ['ADPF', 760], ['ADPF', 829], ['ADPF', 854], ['ADPF', 857], ['ADPF', 863], ['ADPF', 944], ['ADPF', 984], ['ADPF', 991], ['ADPF', 1196], ['AR', 2873],['AO', 1726], ['AO', 2733], ['ARE', 1137139], ['ARE', 1266095], ['ARE', 1291514], ['ARE', 1347550], ['ARE', 1363547], ['ARE', 1372672], ['ARE', 1380067], ['ARE', 1400942], ['ARE', 1407111], ['ARE', 1421884], ['ARE', 1425370], ['ARE', 1441516], ['ARE', 1458169], ['ARE', 1510640], ['MI', '7425'], ['MS', 25463], ['MS', 29293], ['MS', 35398],  ['Pet', 8029], ['Pet', 13157], ['Rcl', 43697], ['Rcl', 56318], ['Rcl', 58207], ['Rcl', 62113], ['Rcl', 64370], ['Rcl', 64540], ['Rcl', 64800], ['Rcl', 64803], ['Rcl', 64807], ['Rcl', 64943], ['Rcl', 66439], ['Rcl', 68709], ['Rcl', 75792], ['RE', 867960], ['RE', 1317890], ['RE', 1346751], ['RE', 1366243], ['RE', 1424451], ['RE', 1443597], ['SL', 1037], ['SL', 1076], ['SL', 1097], ['SL', 1696], ['SL', 1721], ['SL', 1743], ['SL', 1783], ['STP', 17], ['STP', 1013], ['STP', 1014], ['STP', 1021], ['STP', 1069]]

import dsl
import pandas as pd
import logging
import os
from datetime import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException,
                                      TimeoutException,
                                      WebDriverException)
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


lista_dados = []
request_count = 0  # Contador de requisiÃ§Ãµes (nÃ£o precisa ser global)
header = 0
saves = 0
processonaoencontrado = 0

# Define a custom user agent
my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=920,600")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# Set the custom User-Agent
chrome_options.add_argument(f"--user-agent={my_user_agent}")


def webdriver_get(url):
    data = driver.get(url)
    
    return data

def webdriver_get_page(url):
    driver.get(url)
    
    return driver.page_source

def waitForLoad(inputXPath):

    Wait = WebDriverWait(driver, 40)       
    Wait.until(EC.presence_of_element_located((By.XPATH, inputXPath)))

def waitForLoad_ID(name):

    Wait = WebDriverWait(driver, 40)       
    Wait.until(EC.presence_of_element_located((By.ID, name)))
    
def xpath_get (xpath):
    
    time.sleep(0.3)
    waitForLoad(xpath)
    dados = driver.find_element(By.XPATH, xpath).get_attribute('innerHTML')
    
    return dados

def class_get_list (element, class_name):
    
    dados = element.find_elements(By.CLASS_NAME, class_name)
    
    return dados

def xpath_body ():
    dados = driver.find_element(By.XPATH, '/html/body').get_attribute('innerHTML')
    
    return (dados)

def xpath_input (xpath, keys):
    
    campo = driver.find_element(By.XPATH, xpath)
    campo.send_keys(keys)


def xpath_click (xpath):
    
    botao  = driver.find_element(By.XPATH, xpath)
    botao.click()

def xpath_ext (xpath):
    
    waitForLoad(xpath)
    dados = driver.find_element(By.XPATH, xpath).get_attribute('innerHTML')
    
    return dados

def id_get (id_):
    
    time.sleep(1)
    waitForLoad_ID(id_)
    dados = driver.find_element(By.ID, id_)
    
    return dados

# ConfiguraÃ§Ãµes globais
TIMEOUT = 15
MAX_RETRIES = 3
RETRY_DELAY = 2  # segundos

# ConfiguraÃ§Ã£o de logging
logging.basicConfig(
    filename='extrator_errors.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def arquivo_existe(arquivo):
    """Verifica se o arquivo existe e nÃ£o estÃ¡ vazio"""
    return os.path.exists(arquivo) and os.path.getsize(arquivo) > 0

# Cria o DataFrame inicial vazio
df = pd.DataFrame()

# Garante que o diretÃ³rio existe
os.makedirs('dados', exist_ok=True)

# Define os nomes dos arquivos finais
csv_file = ('Dados ' + 
            classe + ' de ' +
            str(num_inicial) + ' a ' +
            str(num_final) + '.csv')
# xlsx_file = 'dados/Dados_processuais.xlsx'

# Cria arquivos vazios com cabeÃ§alhos se nÃ£o existirem
# if not arquivo_existe(csv_file):
#     df.to_csv(csv_file, index=False)
# if not arquivo_existe(xlsx_file):
#     df.to_excel(xlsx_file, index=False)

    
# for item in lista_processos:
#     classe = item[0]
#     processo_num = item[1]
    
for processo in range(num_final - num_inicial + 1):
    if processonaoencontrado > 5:
        break
    processo_num = processo + num_inicial
    
    print (classe + str (processo_num))
    
    url = ('https://portal.stf.jus.br/processos/listarProcessos.asp?classe=' + 
           classe +
           '&numeroProcesso=' + 
           str(processo_num)
           )
    
    request_count += 1
    max_retries = 5
    retry_count = 0
    success = False
    
    
    while not success and retry_count < max_retries:
        try:
            driver = webdriver.Chrome(options=chrome_options)
            time.sleep(3)

            page = webdriver_get(url)
            
            # Verifica se a pÃ¡gina contÃ©m erro 403
            if '403 Forbidden' in driver.page_source or 'CAPTCHA' in driver.page_source:
                raise Exception('Acesso negado')
                
            success = True
            
        except Exception as e:
            retry_count += 1
            if '403' in str(e) and retry_count < max_retries:
                print ('retry')
                driver.quit()
                time.sleep(5)
                chrome_options = Options()
                chrome_options.add_argument("--incognito")
                # chrome_options.add_argument("--headless")
                chrome_options.add_argument("--window-size=920,600")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                # Set the custom User-Agent
                chrome_options.add_argument(f"--user-agent={my_user_agent}")
                driver = webdriver.Chrome(options=chrome_options)
                time.sleep(3)

                page = webdriver_get(url)
            else:
                logger.error(f"Falha ao acessar processo {classe}{processo_num}: {str(e)}")
                raise
    
    if ('CAPTCHA' in driver.page_source or 
        '502 Bad Gateway' in driver.page_source):
         
         print('retry')
         time.sleep(5)
         driver.quit()
         time.sleep(5)
         chrome_options = Options()
         chrome_options.add_argument("--incognito")
         # chrome_options.add_argument("--headless")
         chrome_options.add_argument("--window-size=920,600")
         chrome_options.add_argument("--disable-blink-features=AutomationControlled")
         # Set the custom User-Agent
         chrome_options.add_argument(f"--user-agent={my_user_agent}")
         driver = webdriver.Chrome(options=chrome_options)
         url = ('https://portal.stf.jus.br/processos/listarProcessos.asp?classe=' + 
                classe +
                '&numeroProcesso=' + 
                str(processo_num)
                )
         page = webdriver_get(url)
    
    html_total = xpath_get('//*[@id="conteudo"]')
    
    if 'Processo não encontrado' not in html_total and xpath_get('//*[@id="descricao-procedencia"]') != '':
        

        processonaoencontrado = 0
    
        incidente = id_get('incidente').get_attribute('value')
        
        nome_processo = id_get('classe-numero-processo').get_attribute('value')
    
        
        classe_extenso = xpath_get('//*[@id="texto-pagina-interna"]/div/div/div/div[2]/div[1]/div/div[1]')
        
        titulo_processo = xpath_get('//*[@id="texto-pagina-interna"]/div/div/div/div[1]')
        
        if 'badge bg-secondary' in titulo_processo:    
            tipo = xpath_get('//*[@id="texto-pagina-interna"]/div/div/div/div[1]/div[1]/div[1]/div/span[1]')
        else:
            tipo = 'NA'
        
        liminar = []
        if 'bg-danger' in titulo_processo:
            liminar0 = class_get_list(driver, 'bg-danger')
            for item in liminar0:
                liminar.append(item.text)
        else:
            liminar = []

        
        try:
            origem = xpath_get('//*[@id="descricao-procedencia"]')
            origem = dsl.clext(origem,'>','<') if origem else 'NA'
        except Exception:
            origem = 'NA'
            
        try:
            relator = dsl.clext(html_total, 'Relator: ','<')
        except Exception:
            relator = 'NA'
            
        partes_tipo = class_get_list(driver, 'detalhe-parte')
        partes_nome = class_get_list(driver, 'nome-parte')
        
        partes_total = []
        index = 0
        adv = []
        for n in range(len(partes_tipo)):
            index = index + 1
            tipo = partes_tipo[n].get_attribute('innerHTML')
            nome_parte = partes_nome[n].get_attribute('innerHTML')
    
            parte_info = {'_index': index,
                          'tipo': tipo,
                          'nome': nome_parte}
            
            partes_total.append(parte_info)
    
        data_protocolo = dsl.clean(xpath_get('//*[@id="informacoes-completas"]/div[2]/div[1]/div[2]/div[2]'))
        
        origem_orgao = dsl.clean(xpath_get('//*[@id="informacoes-completas"]/div[2]/div[1]/div[2]/div[4]'))
        
        assuntos = xpath_get('//*[@id="informacoes-completas"]/div[1]/div[2]').split('<li>')[1:]
        lista_assuntos = []
        
        for assunto in assuntos:
            lista_assuntos.append(dsl.clext(assunto, '', '</'))
    
    
        resumo = xpath_get('/html/body/div[1]/div[2]/section/div/div/div/div/div/div/div[2]/div[1]')
        
        andamentos_info = driver.find_element(By.CLASS_NAME, 
                                          'processo-andamentos')
        andamentos = class_get_list(andamentos_info,'andamento-item')
        andamentos_lista = []
        for n in range(len(andamentos)):
            index = len(andamentos) - n
            andamento = andamentos[n]
            html = andamento.get_attribute('innerHTML')
            
            if 'andamento-invalido' in html:
                and_tipo = 'invalid'
            else:
                and_tipo = 'valid'
                
            and_data = andamento.find_element(By.CLASS_NAME, 
                                              'andamento-data').text
            and_nome = andamento.find_element(By.CLASS_NAME, 
                                              'andamento-nome').text
            and_complemento = andamento.find_element(By.CLASS_NAME, 
                                                     'col-md-9').text
            
            if 'andamento-julgador badge bg-info' in html:
                and_julgador = andamento.find_element(By.CLASS_NAME, 
                                                      'andamento-julgador').text
            else:
                and_julgador = 'NA'
                
            if 'href' in html:
                and_link = dsl.ext(html, 'https://portal.stf.jus.br/processos/' +'href="','"')
            else:
                and_link = 'NA'
            
            if 'fa-file-alt' in html:
                and_link_tipo = andamento.find_element(By.CLASS_NAME, 'fa-file-alt').text 
            else:
                and_link_tipo = 'NA'
    
            if 'fa-download' in html:
                and_link_tipo = andamento.find_element(By.CLASS_NAME, 'fa-download').text 
            else:
                and_link_tipo = 'NA'
                
            andamento_dados = {'index': index,
                               'data': and_data,
                               'nome': and_nome,
                               'complemento' : and_complemento,
                               'julgador': and_julgador,
                               'link' : and_link,
                               'link_tipo' : and_link_tipo
                               }
            
            andamentos_lista.append(andamento_dados)
        
        deslocamentos_info = driver.find_element(By.XPATH, 
                                          '//*[@id="deslocamentos"]')
        deslocamentos = class_get_list(deslocamentos_info,'lista-dados')
        deslocamentos_lista = []
        html = 'NA'
        for n in range(len(deslocamentos)):
            index = len(deslocamentos) - n
            deslocamento = deslocamentos[n]
            html = deslocamento.get_attribute('innerHTML')
            
            enviado = dsl.clext(html, '"processo-detalhes-bold">','<')
            recebido = dsl.clext(html, '"processo-detalhes">','<')
            
            if 'processo-detalhes bg-font-success">' in html:
                data_recebido = dsl.ext(html, 'processo-detalhes bg-font-success">','<')
            else:
                data_recebido = 'NA'
                
            guia = dsl.clext(html, 'text-right">\n                <span class="processo-detalhes">','<')
        
            deslocamento_dados = {'index': index,
                               'data_recebido': data_recebido,
                               'enviado por': enviado,
                               'recebido por' : recebido,
                               'gruia': guia,
                               }
            
            deslocamentos_lista.append(deslocamento_dados)
    
    
    # # Define os dados a gravar, criando uma lista com as variÃ¡veis
    
        dados_a_gravar = [incidente,
                          classe,
                          nome_processo,
                          classe_extenso,
                          tipo,
                          liminar,
                          origem,
                          relator,
                          len(partes_total),
                          partes_total,
                          data_protocolo,
                          origem_orgao,
                          lista_assuntos,
                          # resumo,
                          len(andamentos_lista),
                          andamentos_lista,
                          len(deslocamentos_lista),
                          deslocamentos_lista]
        
        colunas =            ['incidente',
                              'classe',
                              'nome_processo',
                              'classe_extenso',
                              'tipo',
                              'liminar',
                              'origem',
                              'relator',
                              'len(partes_total)',
                              'partes_total',
                              'data_protocolo',
                              'origem_orgao',
                              'lista_assuntos',
                              # 'resumo',
                              'len(andamentos_lista)',
                              'andamentos_lista',
                              'len(deslocamentos)',
                              'deslocamentos_lista']


# Acrescenta na lista os dados extraÃ­dos de cada processo
        # Cria DataFrame com os dados do processo atual
        
        driver.quit()
        # Pausa de 1 minuto a cada 25 requisiçõeses
        if request_count % 10 == 0:
            # print ('pausa de 1s')
            
            time.sleep(15)

        if request_count % 25 == 0:
            # print ('pausa de 1s')
            # saves = saves+1
            time.sleep(60)
                # df = pd.DataFrame(lista_dados, columns=colunas)
                # df.to_excel (xlsx_file[:-5] + str(saves) + '(' + nome_processo + ')' + '.xlsx',index=False) 
                # df.to_csv (csv_file[:-4] + str(saves) + '(' + nome_processo + ')' + '.csv', 
                #              index=False,
                #              encoding='utf-8',
                #              quoting=1,
                #              doublequote=True
                #              ) 
                
                # print ('gravados arquivos csv e xlsx até '+nome_processo)
                # lista_dados = []
        
        lista_dados.append(dados_a_gravar)
        
        if not arquivo_existe(csv_file):
            df_row = pd.DataFrame([dados_a_gravar], columns=colunas)
            df_row.to_csv(csv_file, mode='a',
                      index=False,
                      encoding='utf-8',
                      quoting=1,
                      doublequote=True,
                      )
        else:
            df_row = pd.DataFrame([dados_a_gravar])
            df_row.to_csv(csv_file, mode='a', 
                      index=False,
                      encoding='utf-8',
                      quoting=1,
                      doublequote=True,
                      header=False
                      )
        


    else:
        processonaoencontrado += 1
        time.sleep(5)
        # Grava linha nos arquivos finais


            
# df = pd.DataFrame(lista_dados, columns=colunas)
# # Fecha os arquivos e finaliza

# df.to_excel(xlsx_file, index=False)