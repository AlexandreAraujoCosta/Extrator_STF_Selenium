# -*- coding: utf-8 -*-
# Este programa realiza buscas na página de andamentos processuais do STF.

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

# Configurações globais
TIMEOUT = 15
MAX_RETRIES = 3
RETRY_DELAY = 2  # segundos

# Configuração de logging
logging.basicConfig(
    filename='extrator_errors.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def arquivo_existe(arquivo):
    """Verifica se o arquivo existe e não está vazio"""
    return os.path.exists(arquivo) and os.path.getsize(arquivo) > 0

# Cria o DataFrame inicial vazio
df = pd.DataFrame()

# Garante que o diretório existe
os.makedirs('dados', exist_ok=True)

classe = 'ADPF'
num_inicial = 28
num_final = 2000
lista_dados = []
driver = dsl.driver
request_count = 0  # Contador de requisições (não precisa ser global)


# Define os nomes dos arquivos finais
csv_file = f'dados/Dados_processuais_{classe}_{num_inicial}a{num_final}.csv'
xlsx_file = f'dados/Dados_processuais_{classe}_{num_inicial}a{num_final}.xlsx'

# Cria arquivos vazios com cabeçalhos se não existirem
if not arquivo_existe(csv_file):
    df.to_csv(csv_file, index=False)
if not arquivo_existe(xlsx_file):
    df.to_excel(xlsx_file, index=False)
    
    
# for item in lista_processos:
for processo in range(num_final - num_inicial + 1):
    processo_num = processo + num_inicial
    
    
    
    url = ('https://portal.stf.jus.br/processos/listarProcessos.asp?classe=' + 
           classe +
           '&numeroProcesso=' + 
           str(processo + num_inicial)
           )
    
    print (classe + str (processo + num_inicial))
    
    request_count += 1
    
    # Pausa de 1 minuto a cada 25 requisi��eses
    if request_count % 25 == 0:
        logger.info(f"Realizadas 25 requisi��es - pausa de 1 minuto")
        time.sleep(60)
        
    max_retries = 3
    retry_count = 0
    success = False
    
    while not success and retry_count < max_retries:
        try:
            page = dsl.webdriver_get(url)
            
            # Verifica se a página contém erro 403
            if '403 Forbidden' in driver.page_source:
                raise Exception('403 Forbidden - Acesso negado')
                
            success = True
            
        except Exception as e:
            retry_count += 1
            if '403' in str(e) and retry_count < max_retries:
                logger.warning(f"Erro 403 - Tentativa {retry_count} de {max_retries} - Aguardando 30 segundos")
                time.sleep(30)
            else:
                logger.error(f"Falha ao acessar processo {classe}{processo + num_inicial}: {str(e)}")
                raise
    
    html_total = dsl.xpath_get('//*[@id="conteudo"]')
    
    if 'Processo não encontrado' not in html_total:
        
    
        incidente = dsl.id_get('incidente').get_attribute('value')
        
        nome_processo = dsl.id_get('classe-numero-processo').get_attribute('value')
    
        
        classe_extenso = dsl.xpath_get('//*[@id="texto-pagina-interna"]/div/div/div/div[2]/div[1]/div/div[1]')
        
        titulo_processo = dsl.xpath_get('//*[@id="texto-pagina-interna"]/div/div/div/div[1]')
        
        if 'badge bg-secondary' in titulo_processo:    
            tipo = dsl.xpath_get('//*[@id="texto-pagina-interna"]/div/div/div/div[1]/div[1]/div[1]/div/span[1]')
        else:
            tipo = 'NA'
        
        if 'badge bg-danger' in titulo_processo:
            liminar = dsl.xpath_get('//*[@id="texto-pagina-interna"]/div/div/div/div[1]/div[1]/div[1]/div/span[3]')
        else:
            liminar = 'NA'
        
        try:
            origem = dsl.xpath_get('//*[@id="descricao-procedencia"]')
            origem = dsl.clext(origem,'>','<') if origem else 'NA'
        except Exception:
            origem = 'NA'
            
        try:
            relator = dsl.xpath_get('//*[@id="texto-pagina-interna"]/div/div/div/div[2]/div[1]/div/div[3]')
        except Exception:
            relator = 'NA'
            
        partes_tipo = dsl.class_get_list(driver, 'detalhe-parte')
        partes_nome = dsl.class_get_list(driver, 'nome-parte')
        
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
    
        data_protocolo = dsl.clean(dsl.xpath_get('//*[@id="informacoes-completas"]/div[2]/div[1]/div[2]/div[2]'))
        
        origem_orgao = dsl.clean(dsl.xpath_get('//*[@id="informacoes-completas"]/div[2]/div[1]/div[2]/div[4]'))
        
        assuntos = dsl.xpath_get('//*[@id="informacoes-completas"]/div[1]/div[2]').split('<li>')[1:]
        lista_assuntos = []
        
        for assunto in assuntos:
            lista_assuntos.append(dsl.clext(assunto, '', '</'))
    
        # = dsl.xpath_get('')
        # = dsl.xpath_get('')
    
        resumo = dsl.xpath_get('/html/body/div[1]/div[2]/section/div/div/div/div/div/div/div[2]/div[1]')
        
        andamentos_info = driver.find_element(By.CLASS_NAME, 
                                          'processo-andamentos')
        andamentos = dsl.class_get_list(andamentos_info,'andamento-item')
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
        deslocamentos = dsl.class_get_list(deslocamentos_info,'lista-dados')
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
    
    
    # # Define os dados a gravar, criando uma lista com as variáveis
    
        dados_a_gravar = [incidente,
                          classe,
                          nome_processo,
                          classe_extenso,
                          tipo,
                          liminar,
                          origem,
                          relator,
                          partes_total,
                          data_protocolo,
                          origem_orgao,
                          lista_assuntos,
                          resumo,
                          andamentos_lista,
                          deslocamentos_lista]
        
        colunas =            ['incidente',
                              'classe',
                              'nome_processo',
                              'classe_extenso',
                              'tipo',
                              'liminar',
                              'origem',
                              'relator',
                              'partes_total',
                              'data_protocolo',
                              'origem_orgao',
                              'lista_assuntos',
                              'resumo',
                              'andamentos_lista',
                              'deslocamentos_lista']


# Acrescenta na lista os dados extraídos de cada processo
        # Cria DataFrame com os dados do processo atual
        current_df = pd.DataFrame([dados_a_gravar], columns=colunas)
        
        # Grava linha nos arquivos finais
        try:
            # Append no CSV
            current_df.to_csv(csv_file, mode='a', header=False, index=False)
            # Append no Excel (precisa reescrever todo o arquivo)
            existing_df = pd.read_excel(xlsx_file)
            updated_df = pd.concat([existing_df, current_df])
            updated_df.to_excel(xlsx_file, index=False)
            
            # Log do progresso
            logger.info(f"Processo {processo + num_inicial} gravado - {classe}{processo + num_inicial}")
            
        except Exception as e:
            logger.error(f"Erro ao gravar processo {processo + num_inicial}: {str(e)}")
    
# Fecha os arquivos e finaliza
logger.info(f"Extração concluída - {classe} {num_inicial} a {num_final}")
