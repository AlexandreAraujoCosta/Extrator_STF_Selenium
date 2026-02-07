# -*- coding: utf-8 -*-
# Este programa realiza buscas na página de andamentos processuais do STF.
#
# SISTEMA DE ARQUIVAMENTO INTELIGENTE:
# - baixados/: Processos com "BAIXA AO ARQUIVO" - nunca são reprocessados
# - temp/: Processos em andamento - podem ser atualizados em novas execuções
#
# RETOMADA AUTOMÁTICA:
# - Processos em baixados/ são sempre pulados
# - Processos em temp/ são reprocessados para atualizar dados
# - Para reprocessar tudo: delete temp/ e baixados/
#
# Defina aqui a classe a ser buscada e um número inicial e final.
# O nome da classe é sensível a maiúsculas. Utilize a sigla constante da página do STF.

classe = 'ADI'
num_inicial = 4000
num_final = 6000

# É possível definir uma lista de processos para processar. Esta, por exemplo, é a lista dos processos estruturais.
# Nese caso, desative as linhas 152 e 153 (inserindo um # que transforma o código em comentário) e ative as linhas 148 a 150.
# lista_processos = [ ['ADI', '130'], ['ADI', '206'], ['ADI', '267'], ['ADI', '296'], ['ADI', '297'], ['ADI', '336'], ['ADI', '343'], ['ADI', '361'], ['ADI', '443'], ['ADI', '477'], ['ADI', '480'], ['ADI', '529'], ['ADI', '535'], ['ADI', '607'], ['ADI', '635'], ['ADI', '652'], ['ADI', '713'], ['ADI', '720'], ['ADI', '799'], ['ADI', '823'], ['ADI', '875'], ['ADI', '877'], ['ADI', '889'], ['ADI', '986'], ['ADI', '989'], ['ADI', '1177'], ['ADI', '1338'], ['ADI', '1387'], ['ADI', '1458'], ['ADI', '1466'], ['ADI', '1468'], ['ADI', '1484'], ['ADI', '1495'], ['ADI', '1638'], ['ADI', '1698'], ['ADI', '1810'], ['ADI', '1820'], ['ADI', '1830'], ['ADI', '1836'], ['ADI', '1877'], ['ADI', '1987'], ['ADI', '1996'], ['ADI', '2017'], ['ADI', '2061'], ['ADI', '2076'], ['ADI', '2140'], ['ADI', '2154'], ['ADI', '2162'], ['ADI', '2205'], ['ADI', '2318'], ['ADI', '2445'], ['ADI', '2481'], ['ADI', '2486'], ['ADI', '2490'], ['ADI', '2491'], ['ADI', '2492'], ['ADI', '2493'], ['ADI', '2495'], ['ADI', '2496'], ['ADI', '2497'], ['ADI', '2498'], ['ADI', '2503'], ['ADI', '2504'], ['ADI', '2505'], ['ADI', '2506'], ['ADI', '2507'], ['ADI', '2508'], ['ADI', '2509'], ['ADI', '2510'], ['ADI', '2511'], ['ADI', '2512'], ['ADI', '2516'], ['ADI', '2517'], ['ADI', '2518'], ['ADI', '2519'], ['ADI', '2520'], ['ADI', '2523'], ['ADI', '2524'], ['ADI', '2525'], ['ADI', '2537'], ['ADI', '2557'], ['ADI', '2634'], ['ADI', '2727'], ['ADI', '2778'], ['ADI', '3243'], ['ADI', '3276'], ['ADI', '3302'], ['ADI', '3303'], ['ADI', '3575'], ['ADI', '3682'], ['ADI', '3902']]

# IMPORTANTE: Suprimir stderr ANTES de qualquer import que use Chrome/ChromeDriver
# Isso evita mensagens do tipo "DevTools listening", "PHONE_REGISTRATION_ERROR", etc.
import sys
import os
sys.stderr = open(os.devnull, 'w', encoding='utf-8')

import dsd  # Módulo dsd-br publicado no PyPI
import pandas as pd
import os
from datetime import datetime
import time
import json
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (NoSuchElementException,
                                      TimeoutException,
                                      WebDriverException)
import pdfplumber
from io import BytesIO
from striprtf.striprtf import rtf_to_text
import urllib3
from tenacity import (retry, stop_after_attempt, wait_exponential,
                     retry_if_exception_type, before_sleep_log)
import logging

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configurar logging para tenacity
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


request_count = 0  # Contador de requisições
processonaoencontrado = 0

# Configuração do Chrome será feita via dsd.create_stf_webdriver()

# Configurações globais
TIMEOUT = 15
MAX_RETRIES = 5
RETRY_DELAY = 2  # segundos
BACKOFF_MIN = 2  # segundos mínimos entre tentativas
BACKOFF_MAX = 30  # segundos máximos entre tentativas
BACKOFF_MULTIPLIER = 2  # multiplicador para backoff exponencial


# Exceções personalizadas para retry
class STFAccessError(Exception):
    """Erro de acesso ao portal STF (403, CAPTCHA, 502)"""
    pass


# Funções com retry logic usando tenacity
@retry(
    stop=stop_after_attempt(MAX_RETRIES),
    wait=wait_exponential(multiplier=BACKOFF_MULTIPLIER, min=BACKOFF_MIN, max=BACKOFF_MAX),
    retry=retry_if_exception_type((STFAccessError, WebDriverException)),
    before_sleep=before_sleep_log(logger, logging.INFO)
)
def criar_driver_e_navegar(url: str):
    """Cria WebDriver e navega para URL com retry automático.

    Args:
        url: URL do processo no portal STF

    Returns:
        tuple: (driver, page_source)

    Raises:
        STFAccessError: Se detectar CAPTCHA, 403 ou 502
        WebDriverException: Erros do Selenium
    """
    driver = dsd.create_stf_webdriver(headless=True)
    # time.sleep(1)  # Removido para máxima velocidade

    try:
        dsd.webdriver_get(driver, url)

        # Valida se não há bloqueios
        if '403 Forbidden' in driver.page_source:
            driver.quit()
            raise STFAccessError('403 Forbidden detectado')

        if 'CAPTCHA' in driver.page_source:
            driver.quit()
            raise STFAccessError('CAPTCHA detectado')

        if '502 Bad Gateway' in driver.page_source:
            driver.quit()
            raise STFAccessError('502 Bad Gateway detectado')

        return driver, driver.page_source

    except Exception as e:
        try:
            driver.quit()
        except:
            pass
        raise


@retry(
    stop=stop_after_attempt(2),  # Apenas 2 tentativas para downloads
    wait=wait_exponential(multiplier=1, min=5, max=10),
    retry=retry_if_exception_type((Exception,)),
    before_sleep=before_sleep_log(logger, logging.DEBUG)
)
def baixar_documento(url: str) -> str:
    """Baixa e extrai conteúdo de documento (PDF/RTF/HTML) com retry.

    Args:
        url: URL do documento

    Returns:
        str: Conteúdo extraído do documento ou 'Exception' em caso de falha
    """
    if url == 'NA':
        return 'NA'

    try:
        if '.pdf' in url:
            response = dsd.get_response(url)
            file_like = BytesIO(response.content)
            conteudo = ""
            with pdfplumber.open(file_like) as pdf:
                for pagina in pdf.pages:
                    conteudo += pagina.extract_text() + "\n"
            return conteudo

        elif 'RTF' in url:
            response = dsd.get_response(url)
            return rtf_to_text(response.text)

        else:
            return dsd.get(url)

    except Exception:
        raise


def arquivo_existe(arquivo):
    """Verifica se o arquivo existe e não está vazio"""
    return os.path.exists(arquivo) and os.path.getsize(arquivo) > 0

# Garante que os diretórios existem
os.makedirs('dados', exist_ok=True)
os.makedirs('temp', exist_ok=True)
os.makedirs('baixados', exist_ok=True)  # Processos finalizados (não são reprocessados)

# Define os nomes dos arquivos finais
csv_file = ('Dados ' + 
            classe + ' de ' +
            str(num_inicial) + ' a ' +
            str(num_final) + '.csv')
# xlsx_file = 'dados/Dados_processuais.xlsx'

# Loop alternativo para processar uma lista de processos específica. Desative o loop principal e ative este para usar a lista.
# for item in lista_processos:
#     classe = item[0]
#     processo_num = item[1]

# Loop principal para percorrer os processos
for processo in range(num_final - num_inicial + 1):
    if processonaoencontrado > 20:
        break
    processo_num = processo + num_inicial

    # Verifica se o processo já foi extraído
    arquivo_temp = f'temp/{classe}{processo_num}_partial.csv'
    arquivo_baixado = f'baixados/{classe}{processo_num}_partial.csv'

    # OTIMIZAÇÃO: Verifica PRIMEIRO se já está em baixados/ antes de fazer qualquer coisa
    if os.path.exists(arquivo_baixado):
        print(f'{classe}{processo_num} - BAIXADO (pulando)')
        continue

    # Se está em temp/, remove para reprocessar
    elif os.path.exists(arquivo_temp):
        print(f'{classe}{processo_num} - EM TEMP (reprocessando)')
        os.remove(arquivo_temp)

    print (classe + str (processo_num))

    url = ('https://portal.stf.jus.br/processos/listarProcessos.asp?classe=' +
           classe +
           '&numeroProcesso=' +
           str(processo_num)
           )

    request_count += 1

    # Usa função com retry automático (tenacity)
    try:
        driver, page = criar_driver_e_navegar(url)
    except (STFAccessError, WebDriverException) as e:
        logger.error(f'{classe}{processo_num} - Falha após {MAX_RETRIES} tentativas: {e}')
        processonaoencontrado += 1
        continue
    
    html_total = dsd.xpath_get(driver, '//*[@id="conteudo"]')

    if 'Processo não encontrado' not in html_total and dsd.xpath_get(driver, '//*[@id="descricao-procedencia"]') != '':
        

        processonaoencontrado = 0
    
        incidente = dsd.id_get(driver, 'incidente').get_attribute('value')

        nome_processo = dsd.id_get(driver, 'classe-numero-processo').get_attribute('value')
    
        
        classe_extenso = dsd.xpath_get(driver, '//*[@id="texto-pagina-interna"]/div/div/div/div[2]/div[1]/div/div[1]')

        titulo_processo = dsd.xpath_get(driver, '//*[@id="texto-pagina-interna"]/div/div/div/div[1]')
        
        if 'Processo Físico' in html_total:
            tipo_processo = 'Físico'
        elif 'Processo Eletrônico' in html_total:
            tipo_processo = 'Eletrônico'
        else:
            tipo_processo = 'NA'
        
        liminar = []
        if 'bg-danger' in titulo_processo:
            liminar0 = dsd.class_get_list(driver, 'bg-danger')
            for item in liminar0:
                liminar.append(item.text)
        else:
            liminar = []

        
        try:
            origem = dsd.xpath_get(driver, '//*[@id="descricao-procedencia"]')
            origem = dsd.clext(origem,'>','<') if origem else 'NA'
            # Extrai apenas a sigla do estado (primeiras 2 letras maiúsculas)
            if origem != 'NA':
                import re
                match = re.search(r'\b([A-Z]{2})\b', origem)
                origem = match.group(1) if match else origem
        except Exception:
            origem = 'NA'
            
        try:
            relator = dsd.clext(html_total, 'Relator(a): ','<')
            # Remove o prefixo "Min. ", "MIN. " ou "min. " (case-insensitive)
            import re
            relator = re.sub(r'^MIN\.\s+', '', relator, flags=re.IGNORECASE)
        except Exception:
            relator = 'NA'
            
        partes_tipo = dsd.class_get_list(driver, 'detalhe-parte')
        partes_nome = dsd.class_get_list(driver, 'nome-parte')
        
        partes_total = []
        index = 0
        adv = []
        primeiro_autor = 'NA'
        for n in range(len(partes_tipo)):
            index = index + 1
            tipo = partes_tipo[n].get_attribute('innerHTML')
            nome_parte = partes_nome[n].get_attribute('innerHTML')
            if index == 1:
                primeiro_autor = nome_parte
    
            parte_info = {'_index': index,
                          'tipo': tipo,
                          'nome': nome_parte}
            
            partes_total.append(parte_info)
    
        data_protocolo = dsd.clean(dsd.xpath_get(driver, '//*[@id="informacoes-completas"]/div[2]/div[1]/div[2]/div[2]'))

        origem_orgao = dsd.clean(dsd.xpath_get(driver, '//*[@id="informacoes-completas"]/div[2]/div[1]/div[2]/div[4]'))

        assuntos = dsd.xpath_get(driver, '//*[@id="informacoes-completas"]/div[1]/div[2]').split('<li>')[1:]
        lista_assuntos = []
        
        for assunto in assuntos:
            lista_assuntos.append(dsd.clext(assunto, '', '</'))
    
    
        resumo = dsd.xpath_get(driver, '/html/body/div[1]/div[2]/section/div/div/div/div/div/div/div[2]/div[1]')

        andamentos_info = driver.find_element(By.CLASS_NAME,
                                          'processo-andamentos')
        andamentos = dsd.class_get_list(andamentos_info, 'andamento-item')
        andamentos_lista = []
        andamentos_decisórios = []
        html_andamentos = []
        for n in range(len(andamentos)):
            index = len(andamentos) - n
            andamento = andamentos[n]
            html = andamento.get_attribute('innerHTML')
            
            html_andamentos.append(html)

            
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
                and_link = dsd.ext(html, 'href="','"')
                and_link = 'https://portal.stf.jus.br/processos/' + and_link.replace('amp;','')
            else:
                and_link = 'NA'
            
            if 'fa-download' in html:
                and_link_tipo = andamento.find_element(By.CLASS_NAME, 'fa-download').text
            elif 'fa-file-alt' in html:
                and_link_tipo = andamento.find_element(By.CLASS_NAME, 'fa-file-alt').text
            else:
                and_link_tipo = 'NA'

            # Usa função com retry automático (tenacity)
            try:
                and_link_conteudo = baixar_documento(and_link)
            except Exception:
                and_link_conteudo = 'Exception'
            
            andamento_dados = {'index': index,
                               'data': and_data,
                               'nome': and_nome,
                               'complemento' : and_complemento,
                               'julgador': and_julgador,
                               'validade': and_tipo,
                               'link' : and_link,
                               'link_tipo' : and_link_tipo,
                               'link_conteúdo' : and_link_conteudo
                               }
            
            andamentos_lista.append(andamento_dados)
            if and_julgador != 'NA':
                andamentos_decisórios.append(andamento_dados)
        
        deslocamentos_info = driver.find_element(By.XPATH,
                                          '//*[@id="deslocamentos"]')
        deslocamentos = dsd.class_get_list(deslocamentos_info, 'lista-dados')
        deslocamentos_lista = []
        htmld = 'NA'
        for n in range(len(deslocamentos)):
            index = len(deslocamentos) - n
            deslocamento = deslocamentos[n]
            htmld = deslocamento.get_attribute('innerHTML')
            
            enviado = dsd.clext(htmld, '"processo-detalhes-bold">','<')
            recebido = dsd.clext(htmld, '"processo-detalhes">','<')
            
            if 'processo-detalhes bg-font-success">' in htmld:
                data_recebido = dsd.ext(htmld, 'processo-detalhes bg-font-success">','<')
            else:
                data_recebido = 'NA'
                
            guia = dsd.clext(htmld, 'text-right">\n                <span class="processo-detalhes">','<')
        
            deslocamento_dados = {'index': index,
                               'data_recebido': data_recebido,
                               'enviado por': enviado,
                               'recebido por' : recebido,
                               'guia': guia,
                               }
            
            deslocamentos_lista.append(deslocamento_dados)

        # Determina se o processo foi finalizado (baixado/findo)
        # Verifica padrões que indicam processo finalizado:
        # - Andamentos que COMEÇAM com "BAIXA" (baixa ao arquivo, baixa definitiva, etc.)
        # - Andamentos que COMEÇAM com "PROCESSO FINDO"
        processo_baixado = any(
            and_dict['nome'].upper().startswith('BAIXA') or
            and_dict['nome'].upper().startswith('PROCESSO FINDO')
            for and_dict in andamentos_lista
        )
        status_processo = 'Finalizado' if processo_baixado else 'Em andamento'

    # # Define os dados a gravar, criando uma lista com as variáveis

        dados_a_gravar = [incidente,
                          classe,
                          nome_processo,
                          classe_extenso,
                          tipo_processo,
                          liminar,
                          origem,
                          relator,
                          primeiro_autor,
                          len(partes_total),
                          dsd.js(partes_total),
                          data_protocolo,
                          origem_orgao,
                          lista_assuntos,
                          len(andamentos_lista),
                          dsd.js(andamentos_lista),
                          len(andamentos_decisórios),
                          dsd.js(andamentos_decisórios),
                          len(deslocamentos_lista),
                          dsd.js(deslocamentos_lista),
                          status_processo
                          ]

        colunas =            ['incidente',
                              'classe',
                              'nome_processo',
                              'classe_extenso',
                              'tipo_processo',
                              'liminar',
                              'origem',
                              'relator',
                              'autor1',
                              'len(partes_total)',
                              'partes_total',
                              'data_protocolo',
                              'origem_orgao',
                              'lista_assuntos',
                              'len(andamentos_lista)',
                              'andamentos_lista',
                              'len(decisões)',
                              'decisões',
                              'len(deslocamentos)',
                              'deslocamentos_lista',
                              'status_processo']


# Acrescenta na lista os dados extraídos de cada processo
        # Cria DataFrame com os dados do processo atual
        
        driver.quit()
        # Pausa mínima a cada 25 requisições
        if request_count % 25 == 0:
            time.sleep(3)
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

        # Grava arquivo individual para este processo
        pasta = 'baixados' if processo_baixado else 'temp'
        arquivo_parcial = f'{pasta}/{classe}{processo_num}_partial.csv'
        df_row = pd.DataFrame([dados_a_gravar], columns=colunas)
        df_row.to_csv(arquivo_parcial,
                      index=False,
                      encoding='utf-8',
                      quoting=1,
                      doublequote=True
                      )
        status = 'BAIXADO' if processo_baixado else 'TEMP'
        print(f'  -> Salvo em {pasta}/: {classe}{processo_num} [{status}]')



    else:
        processonaoencontrado += 1
        time.sleep(0.5)
        # Grava linha nos arquivos finais

# Concatena todos os arquivos parciais
print('\n' + '='*60)
print('Concatenando arquivos parciais...')

# Coleta arquivos de ambas as pastas
arquivos_temp = [('temp', f) for f in os.listdir('temp') if f.endswith('_partial.csv')]
arquivos_baixados = [('baixados', f) for f in os.listdir('baixados') if f.endswith('_partial.csv')]
todos_arquivos = arquivos_temp + arquivos_baixados

if todos_arquivos:
    # Ordena arquivos pelo número do processo
    todos_arquivos.sort(key=lambda x: int(''.join(filter(str.isdigit, x[1]))))

    # Lê e concatena todos os arquivos
    dfs = []
    for pasta, arquivo in todos_arquivos:
        caminho = os.path.join(pasta, arquivo)
        dfs.append(pd.read_csv(caminho))
        print(f'  OK Lido de {pasta}/: {arquivo}')

    # Concatena e salva arquivo final
    df_final = pd.concat(dfs, ignore_index=True)
    df_final.to_csv(csv_file, index=False, encoding='utf-8', quoting=1, doublequote=True)

    print(f'\nOK Arquivo final criado: {csv_file}')
    print(f'  Total de processos: {len(df_final)}')
    print(f'  - Baixados: {len(arquivos_baixados)}')
    print(f'  - Em andamento: {len(arquivos_temp)}')

    # Remove apenas arquivos temporários (mantém os baixados)
    if arquivos_temp:
        print('\nLimpando arquivos temporários...')
        for pasta, arquivo in arquivos_temp:
            os.remove(os.path.join(pasta, arquivo))
        print(f'  OK {len(arquivos_temp)} arquivo(s) temporário(s) removido(s)')
    print(f'  Mantidos {len(arquivos_baixados)} arquivo(s) em baixados/')
else:
    print('AVISO: Nenhum arquivo parcial encontrado!')

print('='*60)
print('Extração finalizada!')
