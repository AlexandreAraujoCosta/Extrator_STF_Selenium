import csv
import requests
import time
import os
from unicodedata import normalize
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options


# # Define a custom user agent
# my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"

# # Set up Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--incognito")
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=920,600")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# # Set the custom User-Agent
# chrome_options.add_argument(f"--user-agent={my_user_agent}")

# # Create a new instance of ChromeDriver with the desired options
# driver = webdriver.Chrome(options=chrome_options)

# # # Set an implicit wait
# # driver.implicitly_wait(50)


def clean(source):
    source = source.replace('\n',' ')
    source = source.replace('  ',' ')
    source = source.replace('  ',' ')
    source = source.lstrip(' ')
    source = source.lstrip(' ')
    source = source.lstrip(' ')
    source = source.lstrip(' ')
    source = source.lstrip(' ')
    source = source.lstrip(' ')
    source = source.lstrip('"')
    source = source.lstrip('>')
    source = source.replace('  ',' ')
    source = source.replace('\t', '')
    source = source.replace('/#','')
    source = source.strip(' ')
    source = source.strip(' ')       
    source = source.strip('-')
    source = source.strip(' ')       
    source = source.strip(' ')       
    source = source.strip(' ')
    return source


def date(string):
    elementos_data = string.split('/')
    if len(elementos_data) == 3:
        ano = elementos_data[2]
        mes = elementos_data[1]
        dia = elementos_data[0]
        data = f'{ano}-{mes}-{dia}'
        return data
    else:
        return string

def extract(source,start_at, end_at):
    # this function extracts a text
    if start_at not in source:
        return 'NA'
    else:
        start = source.find(start_at) + len(start_at)
        end = source.find(end_at, start)
        if  end_at == '' or end == -1:
            return source[start:]
        elif start_at == '':
            return source[:end]
        else:
            return source[start:end]

def ext(source,start_at, end_at):
    # this function extracts a text
    if start_at not in source:
        return 'NA'
    else:
        start = source.find(start_at) + len(start_at)
        end = source.find(end_at, start)
        if  end_at == '' or end == -1:
            return source[start:]
        elif start_at == '':
            return source[:end]
        else:
            return source[start:end]

def clext(source,start_at, end_at):
    # this function extracts a text
    if start_at not in source:
        return 'NA'
    else:
        start = source.find(start_at) + len(start_at)
        end = source.find(end_at, start)
        if  end_at == '' or end == -1:
            return source[start:]
        elif start_at == '':
            return source[:end]
        else:
            return clean(source[start:end])

def get_response (url):
    
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
  
    # html = requests.get(url, headers = user_agent)
    html = requests.get(url, headers = user_agent, verify=False)
    html.encoding = 'utf-8'
    html = html
    if 'CAPTCHA' in html:
        for n in range(300):
            time.sleep(1)
            print ('espera de '+ str(300-n) + ' segundos')
        html = requests.get(url, headers = user_agent, verify=False)
        html.encoding = 'utf-8'
        html = html
        if 'CAPTCHA' in html:
            for n in range(600):
                time.sleep(1)
                print ('espera de '+ str(600-n) + ' segundos')
            html = requests.get(url, headers = user_agent, verify=False)
            html.encoding = 'utf-8'
            html = html
    return html

def get (url):
    header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,"
              "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "pt-PT,pt;q=0.9",
    "DNT": "1",
    "Priority": "u=0, i",
    "Sec-CH-UA": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

    # html = requests.get(url, headers = user_agent)
    html = requests.get(url, headers = header, verify=False)
    html.encoding = 'utf-8'
    html = html.text
    if 'CAPTCHA' in html:
        for n in range(300):
            time.sleep(1)
            print ('espera de '+ str(300-n) + ' segundos')
        html = requests.get(url, headers = header, verify=False)
        html.encoding = 'utf-8'
        html = html.text
        if 'CAPTCHA' in html:
            for n in range(600):
                time.sleep(1)
                print ('espera de '+ str(600-n) + ' segundos')
            html = requests.get(url, headers = header, verify=False)
            html.encoding = 'utf-8'
            html = html.text
    return html

def get_json (url):
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
  
    # html = requests.get(url, headers = user_agent)
    html = requests.get(url, headers = user_agent, verify=False)
    html.encoding = 'utf-8'
    html = html.json()
    if 'CAPTCHA' in html:
        for n in range(300):
            time.sleep(1)
            print ('espera de '+ str(300-n) + ' segundos')
        html = requests.get(url, headers = user_agent, verify=False)
        html.encoding = 'utf-8'
        html = html.json()
        if 'CAPTCHA' in html:
            for n in range(600):
                time.sleep(1)
                print ('espera de '+ str(600-n) + ' segundos')
            html = requests.get(url, headers = user_agent, verify=False)
            html.encoding = 'utf-8'
            html = html.json()
    return html

def get_contents (url):
    user_agent = {'user-agent': 'mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/119.0.0.0 safari/537.36'}
  
    # html = requests.get(url, headers = user_agent)
    html = requests.get(url, headers = user_agent, verify=False)
    html.encoding = 'utf-8'
    html = html.contents
    if 'captcha' in html:
        for n in range(300):
            time.sleep(1)
            print ('espera de '+ str(300-n) + ' segundos')
        html = requests.get(url, headers = user_agent, verify=False)
        html.encoding = 'utf-8'
        html = html.contents
        if 'captcha' in html:
            for n in range(600):
                time.sleep(1)
                print ('espera de '+ str(600-n) + ' segundos')
            html = requests.get(url, headers = user_agent, verify=False)
            html.encoding = 'utf-8'
            html = html.contents
    return html

def get3 (url):
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    
    # html = requests.get(url, headers = user_agent)
    html = requests.get(url, headers = user_agent, verify=False)
    
    if 'CAPTCHA' in html:
        for n in range(300):
            time.sleep(1)
            print ('espera de '+ str(300-n) + ' segundos')
        html = requests.get(url, headers = user_agent, verify=False)
        if 'CAPTCHA' in html:
            for n in range(600):
                time.sleep(1)
                print ('espera de '+ str(600-n) + ' segundos')
            html = requests.get(url, headers = user_agent, verify=False)
    return html


def get2 (url):
    # user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    html = requests.get(url)
    # html.encoding = 'utf-8'
    html = html.text
    return html

def get_utf8 (url):
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    html = requests.get(url, headers = user_agent)
    html.encoding = 'utf-8'
    html = html.text
    return html
        
def trim(source,start_at, end_at):
    if source.find(start_at) == -1:
        start = 0
    else:
        start = source.find(start_at) + len(start_at)
        
    end = source.find(end_at, start)
    if  end_at == '' or end == -1:
        return source[start:]
    elif start_at == '':
        return source[:end]
    else:
        return source[start:end]

###rever

def extrair(source,start_at, end_at):
    # this function extracts a text
    if start_at not in source:
        return 'na'
    else:
        start = source.find(start_at) + len(start_at)
        end = source.find(end_at, start)
        if  end_at == '' or end == -1:
            return source[start:]
        elif start_at == '':
            return source[:end]
        else:
            return source[start:end]

def adicionar (nomedoarquivo, dados):
    arquivo = open(nomedoarquivo, 'a', encoding='utf-8')
    arquivo.write(dados)
    arquivo.close

def ajustar_mes (string):
    string = string.replace('JAN','01')
    string = string.replace('FEV','02')
    string = string.replace('MAR','03')
    string = string.replace('ABR','04')
    string = string.replace('MAI','05')
    string = string.replace('JUN','06')
    string = string.replace('JUL','07')
    string = string.replace('AGO','08')
    string = string.replace('SET','09')
    string = string.replace('OUT','10')
    string = string.replace('NOV','11')
    string = string.replace('DEZ','12')

    return string
    

def carregar_arquivo (nomedoarquivo):
    arquivo = open(nomedoarquivo, 'r', encoding='utf-8')
    html = arquivo.read()
    arquivo.close()
    return html

def csv_to_list (file):
    csv.field_size_limit(16777216)

    lista = []
    with open(file, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for n in range(len(row)):
                if type(row[n]) == str:
                    row[n] = row[n].replace('|','\n')
            lista.append(row)

    return (lista)

def origem_ato (origem_sigla,intdos):
    
    ato_impugnado_origem = origem_sigla
    if ('PRESIDENTE DA REPUBLICA' in intdos 
            or 'CN;' in intdos 
            or 'SENADO' in intdos
            or 'CAMARA DOS DEPUTADOS' in intdos
            or 'AGENCIA NACIONAL' in intdos
            or 'MIN.' in intdos[:4]
            or 'CNJ' in intdos
            or 'BANCO CENTRAL' in intdos
            or 'CONS.' in intdos[:6]
            or 'TSE' in intdos):
            ato_impugnado_origem = 'FEDERAL'
            
    if ato_impugnado_origem == 'DF' and 'DISTRITO' not in intdos:
            ato_impugnado_origem = 'FEDERAL?'
    
    if intdos == 'ALALAGOAS;':
        origem_sigla == 'AL'
        ato_impugnado_origem = 'AL'
    
    intdos_resumo = intdos.replace('GOV.','')
    intdos_resumo = intdos_resumo.replace(';AL',';')
    intdos_resumo = intdos_resumo.replace(';AGOAS','ALAGOAS')
    if intdos_resumo[:2] == 'AL' and intdos_resumo[2:5] != 'AGO':
        intdos_resumo = intdos_resumo[2:]
    intdos_resumo = intdos_resumo.replace(';TC',';')
    if intdos_resumo[:2] == 'TC':
        intdos_resumo = intdos_resumo[2:]
    intdos_resumo = intdos_resumo.replace('ALAGOASALAGOAS','ALAGOAS')
    

    intdos_resumo = intdos_resumo.replace('PRESIDENTE DA REPUBLICA','FEDERAL')
    intdos_resumo = intdos_resumo.replace('CN;','FEDERAL;')
    intdos_resumo = intdos_resumo.split(';')
    
    if len(intdos_resumo) > 1:
        if intdos_resumo[0] == intdos_resumo[1]:
            intdos_resumo.pop(0)
        if len(intdos_resumo) > 1:
            if intdos_resumo[0] == intdos_resumo[1]:
                intdos_resumo.pop(0)
        intdos_resumo.pop()
        if len(intdos_resumo) == 1:
            intdos_resumo = intdos_resumo[0]
        if intdos_resumo[0] == 'FEDERAL':
            intdos_resumo = 'FEDERAL'
            
    if intdos == '':
        intdos_resumo == ''  
        
#corrige problemas na origem

    
    if origem_sigla == 'AC':
        if 'GOV.ALAGOAS' in intdos:
            ato_impugnado_origem = 'AL'  
    
    if 'TRE DE GOIAS;' in intdos and ato_impugnado_origem == 'FEDERAL?':
        ato_impugnado_origem = 'GO'
    
    lista_orgaos_federais = [
            'OAB',
            'TSE',
            'TST',
            'TC/UNIAO',
            'INSS',
            'CORREGEDORIANACIONAL',
            '/UNIAO',
            'STF',
            'MIN. D',
            'TRT',
            'TRF',
            'STJ',
            'STM',
            'TST',
            'TRE',
            'RECEITA FEDERAL',
            'IBAMA',
            'POLICIA FEDERAL',
            'SECRETARIA DA RECEITA PREVIDENCIARIA',
            'SECRETARIA DO PATRIMONIO DA UNIAO'
            ]
    
    for item in lista_orgaos_federais:
        if intdos[:len(item)] == item:
            ato_impugnado_origem = 'FEDERAL'
            
    if ato_impugnado_origem == 'FEDERAL?':

        
        for item in lista_orgaos_federais:
            if item in intdos:
                ato_impugnado_origem = 'FEDERAL'
                
    if ato_impugnado_origem == 'FEDERAL?' and intdos[:2] == 'AL':
        intdos_resumo = limpar(extrair(intdos, 'AL',';'))
        ato_impugnado_origem = limpa_estado(intdos_resumo).strip('/')
        
    if ato_impugnado_origem == 'FEDERAL?' and intdos[:2] == 'TC':
        intdos_resumo = limpar(extrair(intdos, 'TC',';'))
        ato_impugnado_origem = limpa_estado(intdos_resumo).strip('/')
        
        
    if ato_impugnado_origem == 'FEDERAL?' and intdos[:4] == 'GOV.':
        intdos_resumo = limpar(extrair(intdos, 'GOV.',';'))
        ato_impugnado_origem = limpa_estado(intdos_resumo).strip('/')
        
    if ato_impugnado_origem == 'FEDERAL?':
        for item in ['MP DE',
                     'TJ DE']:
            if intdos_resumo[:len(item)] == item:                
                intdos_resumo == intdos_resumo.replace(item,'')
                intdos_resumo =  limpa_estado(intdos_resumo).strip('/')
                
        if len(intdos_resumo) == 2:
            ato_impugnado_origem == intdos_resumo
            
    origem_ato_extraido_intdos = limpa_estado(str(intdos_resumo)).replace('/','')
    origem_ato_extraido_intdos = origem_ato_extraido_intdos.replace('TJ DE ','')
    origem_ato_extraido_intdos = origem_ato_extraido_intdos.replace('CORR.GERAL DA JUSTICA DO ','')
    origem_ato_extraido_intdos = origem_ato_extraido_intdos.replace('PREF. DO MUN. DE ','')
     
    if len(origem_ato_extraido_intdos) == 2:
        ato_impugnado_origem = origem_ato_extraido_intdos
        intdos_resumo = origem_ato_extraido_intdos
               
    if 'ACRE;ALAGOAS' in intdos or 'GOV.ACRE;GOV.AMAPA' in intdos:
        ato_impugnado_origem = 'MULTIPLA'
        
    return ato_impugnado_origem

def limpar(fonte):
    fonte = fonte.replace('\n',' ')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip('"')
    fonte = fonte.lstrip('>')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.replace('\t', '')
    fonte = fonte.replace('/#','')
    fonte = fonte.strip(' ')
    fonte = fonte.strip(' ')       
    fonte = fonte.strip('-')
    fonte = fonte.strip(' ')       
    fonte = fonte.strip(' ')       
    fonte = fonte.strip(' ')
    return fonte

def limpar_para_csv (fonte):
    if type(fonte) == str:
        fonte = fonte.replace('\n','|')
        fonte = fonte.replace('  ',' ')
        fonte = fonte.replace('  ',' ')
        fonte = fonte.lstrip(' ')
        fonte = fonte.lstrip(' ')
        fonte = fonte.lstrip(' ')
        fonte = fonte.lstrip(' ')
        fonte = fonte.lstrip(' ')
        fonte = fonte.lstrip(' ')
        fonte = fonte.lstrip('"')
        fonte = fonte.lstrip('>')
        fonte = fonte.replace('  ',' ')
        fonte = fonte.replace('\t', '')
        fonte = fonte.replace('/#','')
        fonte = fonte.strip(' ')
        fonte = fonte.strip(' ')       
        fonte = fonte.strip('-')
        fonte = fonte.strip(' ')       
        fonte = fonte.strip(' ')       
        fonte = fonte.strip(' ')
        fonte = fonte.replace('\r','|')
        fonte = fonte.replace('|||||','|')
        fonte = fonte.replace('||||','|')
        fonte = fonte.replace('|||','|')
        fonte = fonte.replace('||','|')
        fonte = fonte.strip('|')
    
    return (fonte)

def limpar_tudo (fonte):
    fonte = fonte.replace('\n',' ')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip(' ')
    fonte = fonte.lstrip('"')
    fonte = fonte.lstrip('>')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.replace('\t', '')
    fonte = fonte.replace('/#','')
    fonte = fonte.strip(' ')
    fonte = fonte.strip(' ')       
    fonte = fonte.strip('-')
    fonte = fonte.strip(' ')       
    fonte = fonte.strip(' ')       
    fonte = fonte.strip(' ')
    fonte = fonte.replace('\r','|')
    fonte = fonte.replace('|||||','|')
    fonte = fonte.replace('||||','|')
    fonte = fonte.replace('|||','|')
    fonte = fonte.replace('||','|')
    fonte = fonte.strip('|')
    
    
    fonte = fonte.replace('&Ccedil;','Ç')
    fonte = fonte.replace('&ccedil;','ç')
    fonte = fonte.replace('&Atilde;','Ã')
    fonte = fonte.replace('&atilde;','ã')
    fonte = fonte.replace('&Otilde;','Õ')
    fonte = fonte.replace('&otilde;','õ')
    
    fonte = fonte.replace('&Eacute;','É')
    fonte = fonte.replace('&eacute;','é')
    fonte = fonte.replace('&Aacute;','Á')
    fonte = fonte.replace('&aacute;','á')
    fonte = fonte.replace('&Iacute;','Í')
    fonte = fonte.replace('&iacute;','í')
    fonte = fonte.replace('&Oacute;','Ó')
    fonte = fonte.replace('&oacute;','ó')
    fonte = fonte.replace('&Uacute;','Ú')
    fonte = fonte.replace('&uacute;','ú')
    
    fonte = fonte.replace('&Ecirc;','Ê')
    fonte = fonte.replace('&ecirc;','ê')
    fonte = fonte.replace('&Acirc;','Â')
    fonte = fonte.replace('&acirc;','â')
    fonte = fonte.replace('&Ocirc;','Ô')
    fonte = fonte.replace('&ocirc;','ô')
    fonte = fonte.replace('&ordm;','º')
    fonte = fonte.replace('&sect; ','§')
    fonte = fonte.replace('&Agrave;','À')
    fonte = fonte.replace('&agrave;','à')
    fonte = fonte.replace('&ldquo;','"')
    
    fonte = fonte.strip('\r\n')
    fonte = fonte.strip(',')
    fonte = fonte.strip('null\n')
    
    fonte = re.sub('<[^<]+?>', '', fonte)
    fonte = fonte.replace('&nbsp; ','')
    fonte = fonte.replace('&nbsp;','')
    
    fonte = fonte.strip('"')
    fonte = fonte.strip('\r\n')
    fonte = fonte.strip(',')
    fonte = fonte.strip('null\n')
    fonte = fonte.strip('.')
    fonte = fonte.strip('null\n')
    
    fonte = fonte.replace('\r\n',' ')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.replace('  ',' ')
    fonte = fonte.replace('  ',' ')
    
    return fonte



def get_CC (url):
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    html = requests.get(url, headers = user_agent)
    html.encoding = 'utf-8'
    html = html.text
    html = extrair (html,
                   '<div class="titulo-formulario">',
                   '<section id="mapa-do-site">')
    return html

def gravar (nomedoarquivo, dados):
    arquivo = open(nomedoarquivo, 'w', encoding='utf-8')
    arquivo.write(dados)
    arquivo.close

def write_csv_header (nomedoarquivo, string_campos):
    string_campos = string_campos.replace('\n','')
    string_campos = limpar(string_campos)
    string_campos = string_campos.replace('  ',' ')
    string_campos = string_campos.replace(', ',',')
    lista_de_campos = string_campos.split(',')
    if nomedoarquivo in os.listdir():
        arquivoaberto = open(nomedoarquivo, mode='r+',
                                 encoding="utf-8", newline='')
        html = arquivoaberto.read()
        arquivoaberto.close()

        
        if lista_de_campos[0] not in html[:100]:
            arquivoaberto = open(nomedoarquivo, mode='w',
                                 encoding="utf-8", newline='')
            arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
            arquivoaberto_csv.writerow(lista_de_campos)
            arquivoaberto.close()
    else:
            arquivoaberto = open(nomedoarquivo, mode='w',
                                 encoding="utf-8", newline='')
            arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',')
            arquivoaberto_csv.writerow(lista_de_campos)
            arquivoaberto.close()
            
def write_csv_row (nomedoarquivo,dados):
    for n in range(len(dados)):
        dados[n] = limpar_para_csv(dados[n])
    if dados != []:
        arquivoaberto = open(nomedoarquivo, mode='a+', encoding="utf-8", newline='')
        arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',', quotechar = '"')
        arquivoaberto_csv.writerow(dados)
        arquivoaberto.close()
    else:
        print ('Dados a serem escritos devem ser inseridos com formato lista')
        
def write_csv_rows (nomedoarquivo, dados):
    if dados != []:
        arquivoaberto = open(nomedoarquivo, mode='a+',
                             encoding="utf-8", newline='')
        print ('gravando')
        arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',', quotechar = '"')
        arquivoaberto_csv.writerows(dados)
        arquivoaberto.close()

### a rever

def position1(list):
    return(list[1])



def csv_to_list_general (file):
    csv.field_size_limit(16777216)

    lista = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            lista.append(row)

    return (lista)

def csv_to_list_titles(file):
    csv.field_size_limit(16777216)

    lista = []
    with open(file, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            lista.append(row)

        n_campos = len(lista[0])
        
        for campo in range (n_campos):
            tipo = str(campo) + ':string:'
            integral = 0
            amostra = len(lista)//10
            for n in range (amostra):
            
                objeto = lista[n][campo]
                
                if objeto != '' and objeto[0] == '[':
                    tipo = str(campo) + ':lista:'
                    if objeto[1] == '[':
                        tipo = str(campo) + ':lista2:'
                    
                try:
                        int(objeto)
                except ValueError:
                        integral = integral + 1
                    
            if integral == 1:
                tipo = str(campo) + ':int:'
                
            lista[0][campo] = tipo + str(lista[0][campo])
            print (f'Campo {campo} = {str(lista[0][campo])}')
             
        for campo in range (n_campos):
            for linha in lista[1:]:
                if 'int:' in lista[0][campo]:
                    linha[campo] = int(linha[campo])
                if 'lista:' in lista[0][campo]:
                    linha[campo] = linha[campo][1:-1]
                    # linha[campo] = linha[campo][',']
                if 'lista2:' in lista[0][campo]:
                    linha[campo] = linha[campo][2:-2]
                    
                    linha[campo] = linha[campo].split('], [')
                    
                    for n in range (len(linha[campo])):
                        linha[campo][n] = linha[campo][n].replace("'",'')
                        linha[campo][n] = linha[campo][n].replace(", ",',')
                        linha[campo][n] = linha[campo][n].split(',')

    return (lista)

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('utf-8')



def extrair_campo_lista (string, split, lista_inicio_fim):
    # define o número de elementos a serem extraídos
    n_elementos= string.count(split)

    # cria uma lista (dados) com os dados da string, segmentada no split
    elementos = string.split(split)
    elementos = elementos[1:]

    # imprime o número de elementos a serem extraídos
    # print (str(n_elementos) + ' elementos')

    #define a lista que será retornada como resultado
    campo_lista = []

    # iteração sobre cada um dos n elementos
    for item in range(n_elementos):

        # carrega na variável campo um elemento de cada vez
        campo = elementos[item]
        # print (campo)
        # redefine a lista elemento_lista
        elemento_lista = []

        # insere no elemento o número de ordem, iniciando em 1
        elemento_lista.append(['ORDEM', str(item+1)])

        # identifica os atributos de cada elemento
        for elemento in range(len(lista_inicio_fim)):
            # extrai os marcadores da lista
            marcadores = lista_inicio_fim[elemento]
            atributo = marcadores[0].upper()
            inicio = marcadores[1]
            fim = marcadores[2]

            # extrai o atributo a partir dos marcadores
            dado = ''
            dado = extrair(campo, inicio, fim)
            dado = limpar(dado)
            dado = limpar(dado)
            dado = remover_acentos(dado)

            elemento_lista.append([atributo, dado.upper()])
        # acrescenta o elemento extraído na lista que compõe o campo
        campo_lista.append(elemento_lista)

    # retorna a lista de elementos como resultado função
    return campo_lista

def ajustar_nome(string):
    string.strip()
    
    trocar1 =[['ASSOC ','ASSOCIACAO '],
            ['GONGRESSO NACIONAL','CONGRESSO NACIONAL'],
            ['REPUBICA','REPUBLICA'],
            ['PROCURADOR GERAL','PROCURADOR-GERAL'],
            ['REUBLICA','REPUBLICA'],
            ['GONGRESSO','CONGRESSO'],
            ['(','- '],
            [')',''],
            ['  ',' '],
            ['MINISTRA','MINISTRO'],
            ['PRO-BELEZA','PROBELEZA'],
            ['VICE-GOV','V.GOV'],
            ['VICE PRESIDENTE','VICE-PRESIDENTE'],
            ['VICE-PRE','V.PRE'],
            ['CORREGEDOR-GERAL','CORR.GERAL'],
            ['CORREGEDORIA-GERAL','CORR.GERAL'],
            ['CORREGEDORIAGERAL','CORR.GERAL'],
            ['CORREGEDORIADA','CORR.GERAL DA'],
            ['ARCO-IRIS','ARCOIRIS'],
            ['TRT - ','TRT '],
            ['REGIAO -','REGIAO'],
            ['MATO-GROSSENSE','MATOGROSSENSE'],
            ['TRT - ','TRT '],
            ['CONSTAS ','CONTAS'],
            ['J.G.A.C.','JOSE GABRIEL AVILA CAMPELLO'],
            ['/DO ','/'],
            ['-',' - '],
            ['  ',' '],
            ['  ',' '],
            [']',''],
            
            ['- ME',''],
            ['S/A','S.A.'],
            ['LTDA.','LTDA'],
            ['PREFEITA','PREFEITO'],
            ['PREFEITO DO MUNICIPIO','PREFEITO'],
            ['PREFEITO D', 'PREF. D'],
            ['PREFEITO MUNICIPAL D','PREF. D'],
            ['PREFEITURA D','PREF. D'],
            ['PREFEITURA MUNICIPAL','PREF.'],
            ['MUNICIPIO D','MUN. D'],
            ['MINISTRO D','MIN. D'],
            ['MINISTERIO D','MIN. D'],
            ['MESA DIRETIVA','MESA DIRETORA'],
            ['MESA DIRETORA','M.D.'],
            ['MESA DA','M.D. DA'],
            ['SENADO FEDERAL','SENADO'],
            ['JUIZ DE DIREITO','JUIZ'],
            ['CORREGEDOR ','CORREGEDORIA'],
            ['CORREGEDORIA ','CORREG. '],
            ['CAMARA DE VEREADORES','CAMARA MUNICIPAL'],
            ['CAMARA MUNICIPAL','C.MUN.'],
            ['C.MUN. DO MUNICIPIO','C.MUN.'],
            ['CAMPINHAS','CAMPINAS'],
            ['DE TOCANTINS','DO TOCANTINS'],
            ['LEGISLTATIVA','LEGISLATIVA'],
            ['PRO TESTE','PROTESTE'],
            ['E TV ABERT','E TELEVISAO ABERT'],
            ['EMPRESARIOS DE RADIO','EMPRESAS DE RADIO'],
            ['ADEPOL/BRASIL','ADEPOL'],
            ['MAGISTRADOS DO BRASIL AMB','MAGISTRADOS BRASILEIROS AMB'],
            ['ANOREG/BR','ANOREG'],
            ['ANADEP A','ANADEP'],
            ['DAS DEFENSORAS E DEFENSORES','DAS DEFENSORAS E DOS DEFENSORES'],
            ['URBANOS NTU','URBANOS'],
            ['D.G. DA ',''],
            ['D.G. DO ',''],
            ['DIRETOR DA ',''],
            ['DIRETOR DO ',''],
            
            [',',''],
            ['DP DA UNIAO','DPU'],
            ['DPU DPU','DPU'],
            ['DP GERAL','DP.GERAL'],
            ['DP.GERAL','DP'],
            ['FED NAC','FED.NAC.'],
            ['AUXI LIARES','AUXILIARES'],
            
            
            ['/ACRE', '/AC'],
            ['/ALAGOAS', '/AL'],
            ['/AMAPA', '/AP'],
            ['/AMAZONAS', '/AM'],
            ['/BAHIA', '/BA'],
            ['/CEARA', '/CE'],
            ['/DISTRITO FEDERAL', '/DF'],
            ['/ESPIRITO SANTO', '/ES'],
            ['/GOIAS', '/GO'],
            ['/MARANHAO', '/MA'],
            ['/MATO GROSSO DO SUL', '/MS'],
            ['/MATO GROSSO', '/MT'],
            ['/MINAS GERAIS', '/MG'],
            ['/PARAIBA', '/PB'],
            ['/PARANA', '/PR'],
            ['/PERNAMBUCO', '/PE'],
            ['/PIAUI', '/PI'],
            ['/RIO DE JANEIRO', '/RJ'],
            ['/RIO GRANDE DO NORTE', '/RN'],
            ['/RIO GRANDE DO SUL', '/RS'],
            ['/RONDONIA', '/RO'],
            ['/RORAIMA', '/RR'],
            ['/SANTA CATARINA', '/SC'],
            ['/SAO PAULO', '/SP'],
            ['/SERGIPE', '/SE'],
            ['/PARA', '/PA'],
            ['/TOCANTINS', '/TO'],
            ['/ACRE','/AC'],
            ['/RIO DE JANEIRO','/RJ']
            ]
    for item in trocar1:
        string = string.replace(item[0],item[1])
        
        
    if 'DEMOCRATAS' in string and 'DEM ' in string:
        string = 'DEM/PFL'
    if 'DEMOCRATAS -' in string:
        string = 'DEM/PFL'
    if 'DEMOCRATAS' == string:
        string = 'DEM/PFL'
        
    if ' SINDICATO ' in string:
        string = string[string.find(' SINDICATO ')+1:] + ' ' + string[:string.find(' SINDICATO ')]
        
    if ' SOCIEDADE BRASILEIRA ' in string:
        string = string[string.find(' SOCIEDADE BRASILEIRA ')+1:] + ' ' + string[:string.find(' SOCIEDADE BRASILEIRA ')]
    
    substituir = [
              ['PROCURADOR - GERAL DA REPUBLICA','PGR'],
              ['PROCURADOR GERAL DA REPUBLICA','PGR'],
              ['PROCURADORA - GERAL DA REPUBLICA','PGR'],
              ['PROCURADORIA - GERAL DA REPUBLICA','PGR'],
              ['CONSELHO FEDERAL DA ORDEM DOS ADVOGADOS DO BRASIL','OAB'],
              ['PARTIDO PROGRESSISTA','PP'],
              ['PARTIDO COMUNISTA DO BRASIL','PC DO B'],
              ['PARTIDO COMUNISTA BRASILEIRO','PCB'],
              ['PARTIDO DA FRENTE LIBERAL','DEM/PFL'],
              ['PARTIDO DA MOBILIZACAO NACIONAL','PMN'],
              ['PARTIDO DA MULHER BRASILEIRA','PMB'],
              ['REEDIFICACAO DA ORDEM NACIONAL','PRONA'],
              ['PARTIDO DA REPUBLICA','PR'],
              ['DEMOCRACIA BRASILEIRA','PSDB'],
              ['PSDB','PSDB'],
              ['DEMOCRATA CRISTAO','PDC'],
              ['PARTIDO DEMOCRATICO TRABALHISTA','PDT'],
              ['PARTIDO DO MOVIMENTO DEMOCRATICO','PMDB'],
              ['TRABALHADORES DO BRASIL','PT DO B'],
              ['PARTIDO TRABALHISTA DO BRASIL','PT DO B'],
              ['PARTIDO DOS TRABALHADORES','PT'],
              ['PARTIDO HUMANISTA DA SOLIDARIEDADE','PHS'],
              ['PARTIDO LIBERAL','PL'],
              ['PARTIDO POPULAR SOCIAL','PPS'],
              ['PARTIDO PROGRESSISTA BRASILEIRO','PPB'],
              ['PARTIDO PROGRESSISTA REFORMADOR','PPR'],
              ['PARTIDO PROGRESSISTA','PP'],
              ['RENOVADOR TRABALHISTA BRASILEIRO','PRTB'],
              ['PARTIDO REPUBLICANO BRASILEIRO','PRB'],
              ['REPUBLICANO DA ORDEM SOCIAL','PROS'],
              ['PARTIDO REPUBLICANO PROGRESSISTA','PRP'],
              ['PARTIDO SOCIAL CRISTAO','PSC'],
              ['PARTIDO SOCIAL DEMOCRATA CRISTAO','PSDC'],
              ['PARTIDO SOCIAL DEMOCRATICO','PSD'],
              ['PARTIDO SOCIAL LIBERAL','PSL'],
              ['PARTIDO SOCIAL TRABALHISTA','PST'],
              ['SOCIALISMO E LIBERDADE','PSOL'],
              ['PARTIDO SOCIALISTA BRASILEIRO','PSB'],
              ['PARTIDO SOCIALISTA DO BRASIL','PSB'],
              ['PARTIDO SOCIALISTA DOS TRABALHADORES UNIFICADO','PSTU'],
              ['PARTIDO TRABALHISTA BRASILEIRO','PTB'],
              ['PARTIDO TRABALHISTA CRISTAO','PTC'],
              ['PARTIDO TRABALHISTA NACIONAL','PTN'],
              ['PARTIDO TRABALHISTA RENOVADOR','PTR'],
              ['PARTIDO MUNICIPALISTA BRASILEIRO','PMB'],
              ['PARTIDO NACIONAL DOS APOSENTADOS','PNA'],
              ['PARTIDO VERDE','PV'],
              ['PODEMOS','PODEMOS'],
              ['CONS.NAC. DE JUSTICA','CNJ'],
              ['CONGRESSO NACIONAL','CN'],
              ['TRIBUNAL SUPERIOR ELEITORAL','TSE'],
              ['SOLIDARIEDADE -','SOLIDARIEDADE'],
              ['PARTIDO NOVO','PARTIDO NOVO'],
              ['SUPREMO TRIBUNAL FEDERAL','STF'],
              # ['^',''],
              ['TRIBUNAL SUPERIOR DO TRABALHO','TST'],
              ['DIRETOR DA RECEITA FEDERAL','RECEITA FEDERAL'],
              ['DEPARTAMENTO DA RECEITA FEDERAL','RECEITA FEDERAL'],
              ['SINDIFISCO NACIONAL','SIND.NAC. AUDITORES FISCAIS DA RECEITA FEDERAL DO BRASIL SINDIFISCO NACIONAL'],
              ['UNIAO GERAL DOS TRABALHADORES','UNIAO GERAL DOS TRABALHADORES UGT'],
              ['UNIAO NACIONAL DAS INSTITUICOES DE AUTOGESTAO EM SAUDE','UNIAO NACIONAL DAS INSTITUICOES DE AUTOGESTAO EM SAUDE UNIDAS'],
              ['AL/SAO PAULO ADI 2476 EM APENSO','AL/SAO PAULO'],
              ['ARTIGO 19 BRASIL','ASSOC. ARTIGO 19 BRASIL'],
              ['EDUCAFRO','ASSOC. EDUCACAO E CIDADANIA DE AFRO DESCENDENTES E CARENTES EDUCAFRO'],
              ['TJ DO RIO DE JANEIRO','TJ DO RIO DE JANEIRO'],
              ['TJ DE SAO PAULO','TJ DE SAO PAULO'],
              ['TJ DE SANTA CATARINA','TJ DE SANTA CATARINA'],
              ['TRT 22REG.','TRT 22REG.'],
              ['OAB','OAB'],
              ['ABRAMED','ASSOC. BRASILEIRA DE MEDICINA DIAGNOSTICA ABRAMED']
                         
              ]
    
    for item in substituir:
        if item[0] in string:
            string = item[1]
    
    if string.find('ASSOCIACAO') > 0 and string.find('-') < 20:
        string = string.replace('-','')
        string = string.replace('  ',' ')
        string = string.replace('  ',' ')
        string = string[string.find('ASSOCIACAO'):] + ' - ' + string[:string.find('ASSOCIACAO')]
        
    if string.find('UNIAO D') > 0 and string.find('-') < 20:
        string = string.replace('-','')
        string = string.replace('  ',' ')
        string = string.replace('  ',' ')
        string = string[string.find('UNIAO'):] + ' - ' + string[:string.find('UNIAO')]
        
    if string.find('CONFEDERACAO') > 0 and string.find('-') < 20:
        string = string.replace('-','')
        string = string.replace('  ',' ')
        string = string.replace('  ',' ')
        string = string[string.find('CONFEDERACAO'):] + ' - ' + string[:string.find('CONFEDERACAO')]
        
    if string.find('FEDERACAO') > 0 and string.find('-') < 20 and 'CONFEDERACAO' not in string:
        string = string.replace('-','')
        string = string.replace('  ',' ')
        string = string.replace('  ',' ')
        string = string[string.find('FEDERACAO'):] + ' - ' + string[:string.find('FEDERACAO')]
        
    if string.find('CONSELHO') > 0 and string.find('-') < 20:
        string = string.replace('-','')
        string = string.replace('  ',' ')
        string = string.replace('  ',' ')
        string = string[string.find('CONSELHO'):] + ' - ' + string[:string.find('CONSELHO')]
        
    if 'ESTADO DO ' in string[0:12]:
        string.replace('ESTADO DO ','')
    
    if 'ESTADO DE ' in string[0:12]:
        string.replace('ESTADO DE ','')
        
    if 'ESTADO DA ' in string[0:12]:
        string.replace('ESTADO DA ','')
        
    # estados = [[' DO AC','/AC'],
    #          [' DE AL','/AL'],
    #          [' DO AP','/AP'],
    #          [' DO AM','/AM'],
    #          [' DA BA','/BA'],
    #          [' DO CE','/CE'],
    #          [' DO DF','/DF'],
    #          [' DE GO','/GO'],
    #          [' DO MA','/MA'],
    #          [' DO MS','/MS'],
    #          [' DO MT','/MT'],
    #          [' DE MG','/MG'],
    #          [' DA PB','/PB'],
    #          [' DE PE','/PE'],
    #          [' DO PI','/PI'],
    #          [' DO RJ','/RJ'],
    #          [' DO RN','/RN'],
    #          [' DO RS','/RS'], 
    #          [' DE RO','/RO'],
    #          [' DE RR','/RR'],
    #          [' DE SC','/SC'],
    #          [' DE SP','/SP'],
    #          [' DO PA','/PA'],
    #          [' DE TO','/TO'],
    #          [' DO TO','/TO'],
    #          [' DO ES','/ES']]
    
    # for item in estados:
    #     final = string[-6:0]
    #     if  final == item[0]:
    #         string = string.replace(item[0],item[1])
    
    # estados2 = [[' DO AC','/AC'],
    #          [' AL','/AL'],
    #          [' AP','/AP'],
    #          [' AM','/AM'],
    #          [' BA','/BA'],
    #          [' CE','/CE'],
    #          [' DF','/DF'],
    #          [' GO','/GO'],
    #          [' MA','/MA'],
    #          [' MS','/MS'],
    #          [' MT','/MT'],
    #          [' MG','/MG'],
    #          [' PB','/PB'],
    #          [' PE','/PE'],
    #          [' PI','/PI'],
    #          [' RJ','/RJ'],
    #          [' RN','/RN'],
    #          [' RS','/RS'], 
    #          [' RO','/RO'],
    #          [' RR','/RR'],
    #          [' SC','/SC'],
    #          [' SP','/SP'],
    #          [' PA','/PA'],
    #          [' TO','/TO'],
    #          [' TO','/TO'],
    #          [' ES','/ES']]
    
    # for item in estados2:
    #     final = string[-6:0]
    #     if  final == item[0]:
    #         string = string.replace(item[0],item[1])
            
    string = estado_nome_completo(string)

    trocar = [['ASSEMBLEIA LEGISLATIVA DO ESTADO DE ', 'AL/'],
             ['ASSEMBLEIA LEGISLATIVA DO ESTADO DA ', 'AL/'],
             ['ASSEMBLEIA LEGISLATIVA DO ESTADO DO ', 'AL/'],
             ['ASSEMBLEIA LEGISLATIVA DO ESTADO ', 'AL/'],
             ['ASSEMBLEIA LEGISLATIVA DO ','AL/'],
             ['ASSEMBLEIA LEGISLATIVA DE ','AL/'],
             ['ASSEMBLEIA LEGISLATIVA DA ','AL/'],
             ['ASSEMBLEIA LEGISLATIVA','AL/'],
             ['CONSELHO FEDERAL', 'CONS.FED'],
             ['CONSELHO', 'CONS.'],
             ['TRIBUNAL REGIONAL ELEITORAL','TRE'],
             ['MINISTERIO PUBLICO','MP'],
             ['ASSOCIACAO NACIONAL', 'ASSOC.NAC.'],
             ['ASSOCIACAO', 'ASSOC.'],
             ['CONFEDERACAO NACIONAL', 'CONF.NAC.'],
             ['CONFEDERACAO BRASILEIRA', 'CONF.BRAS.'],
             ['CONFEDERACAO', 'CONF.'],
             ['DO ESTADO ',''],
             ['GOVERNADORA','GOVERNADOR'],
             ['GOVERNADOR DE ','GOV./ '],
             ['GOVERNADOR DO ','GOV./ '],
             ['GOVERNADOR DA ','GOV./ '],
             ['GOVERNADOR E AL/','GOV./'],
             ['SECRETARIO','SECRETARIA'],
             ['(0','('],
             ['(0','('],
             ['TRIBUNAL REGIONAL DO TRABALHO','TRT'],
             ['TRIBUNAL REGIONAL FEDERAL','TRF'],
             ['TRIBUNAL DE JUSTICA','TJ'],
             ['PROCURADORA','PROCURADOR'],
             ['PROCURADOR-GERAL DE ','PG/'],
             ['PROCURADOR-GERAL DO ','PG/'],
             ['PROCURADOR-GERAL DA ','PG/'],
             ['DF/DF','/DF'],
             ['PRESIDENTA','PRESIDENTE'],
             ['SANTANA CATARINA','SANTA CATARINA'],
             ['MINAS DE GERAIS','MINAS GERAIS'],
             ['A REGIAO','REG.'],
             ['A. REGIAO','REG.'],
             ['TRT DA','TRT'],
             ['TRF DA','TRT'],
             ['SECRETARIA DE FAZENDA','SEC.FAZ.'],
             ['SECRETARIA DA FAZENDA','SEC.FAZ.'],
             ['PRESIDENTE DO','PRES.'],
             ['PRESIDENTE DA','PRES.'],
             ['PRESIDENTE ','PRES.'],
             ['TRIBUNAL DE CONTAS DO','TC/'],
             ['TRIBUNAL DE CONTAS DE','TC/'],
             ['TRIBUNAL DE CONTAS DA','TC/'],
             ['TRIBUNAL DE CONTAS','TC'],
             ['/ ','/'],
             [' /','/'],
             ['//','/'],
             ['DEFENSORIA PUBLICA','DP'],
             ['DEFENSOR PUBLICO GERAL', 'DP.GERAL'],
             ['DEFENSOR PUBLICO-GERAL', 'DP.GERAL'],
             ['ESTADO/',''],
             ['ESTADO DE',''],
             ['JUIZ DO TRABALHO','JUIZ'],
             ['E OUTROS',''],
             ['E OUTRO',''],
             ['E OUTRA',''],
             ['E OUTRAS',''],
             ['MINISTRO DE ESTADO','MINISTRO'],
             ['SECRETARIA DE ESTADO','SECRETARIA'],
             ['SINDICADO DOS EMPREGADOS','SIND.EMPREG.'],
             ['DE MATO GROSSO DO SUL','DO MATO GROSSO DO SUL'],
             ['CONS. DA MAGISTRATURA','CONS.MAGIST.'],
             ['CONS. ESTADUAL','CONS.ESTAD.'],
             ['CONS. NACIONAL','CONS.NAC.'],
             ['CONS. REGIONAL','CONS.REG.'],
             ['CONS. SUPERIOR','CONS.SUP.'],
             ['CORREGEDORIAGERAL','CORR.GERAL'],
             ['CORREG. GERAL','CORR.GERAL'],
             ['DEFENSOR PUBLICO - GERAL','DP.GERAL'],
             ['DIRETOR - GERAL','D.G.'],
             ['FEDERACAO BRASILEIRA','FED.BRAS.'],
             ['FEDERACAO DAS ASSOCIACOES','FED.ASSOC.'],
             ['FEDERACAO NACIONAL DOS SERVIDORES','FED.NAC.SERV.'],
             ['FEDERACAO NACIONAL DOS TRABALHADORES','FED.NAC.TRAB.'],
             ['FEDERACAO NACIONAL','FED.NAC.'],
             ['INSTITUTO BRASILEIRO','INST.BRAS.'],
             ['ORGAO ESPECIAL DO',''],
             ['SINDICATO NACIONAL DE','SIND.NAC.'],
             ['SINDICATO NACIONAL DOS','SIND.NAC.'],
             ['SINDICATO NACIONAL DAS','SIND.NAC.'],
             ['SINDICATO NACIONAL','SIND.NAC.'],
             ['MIN. DE ESTADO','MIN.'],
             ['ORDEM DOS ADVOGADOS DO BRASIL','OAB'],
             ['PROCURADOR - GERAL','PROC.GERAL'],
             ['PROCURADOR GERAL DA REPUBLICA','PGR'],
             ['PROCURADOR GERAL','PROC.GERAL'],
             ['PROCURADORIA GERAL','PROC.GERAL'],
             ['SUPERIOR TJ','STJ'],
             [' AMPCON',''],
             ['C.MUN. DO MUN.','C.MUN.'],
             ['DO UNIAO','DA UNIAO'],
             ['FECOMERCIO PR',''],
             [' 0AB',''],
             ['PRES. BRASIL','PRES. REPUBLICA'],
             ['GOVERNO DE',''],
             ['GOVERNO DO',''],
             ['PRES. REPUBLICA','PRESIDENTE DA REPUBLICA'],
             ['PRESIDENCIA DA REPUBLICA','PRESIDENTE DA REPUBLICA'],
             ['EM EXERCICIO',''],
             ['PRES. ',''],
             ['PATRIOTA PATRI','PARTIDO PATRIOTA'],
             ['M.D. DA AL','AL'],
             ['-',''],
             ['  ',' '],
             ['  ',' '],
             ['FEDERACAO D','FED. D'],
             ['FEDERACAO INTERESTADUAL','FED.INTEREST.'],
             ['FEDERACAO NAC ','FED.NAC. '],
             # ['ASSOC. DAS ','ASSOC. '],
             # ['ASSOC. DE ','ASSOC. '],
             # ['ASSOC. DOS ','ASSOC. '],
             # ['ASSOC. DE','ASSOC.'],
             # ['.NAC. DAS ','ASSOC. '],
             # ['.NAC. DE ','ASSOC. '],
             # ['.NAC. DOS ','ASSOC. '],
             # ['.NAC. DE','ASSOC.'],
             # ['.NAC. E ','ASSOC.'],
             # ['.BRAS. DAS ','ASSOC. '],
             # ['.BRAS. DE ','ASSOC. '],
             # ['.BRAS. DOS ','ASSOC. '],
             # ['.BRAS. DE','ASSOC.'],
             ['NEOTV ', 'NEO TV'],
             ['MUNICIPAIS ANMP','MUNICIPAIS ANPM'],
             ['DIRETORIO NACIONAL DO',''],
             ['DIRETORIO NACIONAL',''],
             ['FORCA SINDICAL FS','FORCA SINDICAL'],
             ['FRENTE NACIONAL','FRENTE.NAC.'],
             ['/S ','/ '],
             ['MP FEDERAL','PGR'],
             ['DP DA UNIAO','DPU'],
             ['DP DA UNIAO DPU','DPU'],
             ['DP.GERAL','DP '],
             [' S A ',' S.A.'],
             ['FEDERACAO','FED.'],
             ['CORREGEDORIAREGIONAL','CORREG.REG.'],
             ['AL./DO ','AL./'],
             ['D.G. DA A','A'],
             ['DIRETOR AGENCIA','AGENCIA'],
             ['DIRETORIA COLEGIADA DA AGENCIA','AGENCIA'],
             ['SECRETARIA DA RECEITA FEDERAL DO BRASIL', 'RECEITA FEDERAL'],
             ['SECRETARIA DE SEGURANCA PUBLICA','SSP'],
             ['TCDO','TC/ '],
             ['CNPGEDF','CONPEG'],
             ['DE DIREITO FUNDAMENTAIS','DE DIREITOS FUNDAMENTAIS'],
             ['CONF NACIONAL','CONF.NAC.'],
             ['DPU DPU','DPU']
             
             
             ]
    
    for item in trocar:
        string = string.replace(item[0],item[1])
    
    if string[:2] == 'A ':
        string = string[2:]
        
    if string[:8] == 'ESTADO D':
        string = string[10:]
    
    if string[0:2] == 'O ':
        string = string[2:]
    
    string.strip(',')
    string.strip()
    
    return string

def extrair_partes(string):
    string = remover_acentos(string)
    
    partes = string.split('<div class="processo-partes lista-dados m-l-16 p-t-0">')
    # print (partes)
    
    n=0
    lista_partes = []
    
    for parte in partes[1:]:
        n = n+1
        ordem = n
        tipo = extrair(parte, 'detalhe-parte">', '<').upper()
        tipo = tipo.replace('REQTE.(S)','REQTE')
        tipo = tipo.replace('INTDO.(A/S)','INTDO')
        tipo = tipo.replace('ADV.(A/S)','ADV')
        tipo = tipo.replace('AM. CURIAE.','AMICUS')
        nome = extrair(parte, '"nome-parte">', '<').upper()
        nome = ajustar_nome(nome)
        if tipo == 'ADV':
            if "(" in nome:
                nome = extrair(nome, '', '(')
        if tipo == 'RQTE':
            lista_partes.append([ordem, tipo, nome])
        
    return lista_partes

def listar_partes(string, processo):
    string = remover_acentos(string)
    
    partes = string.split('<div class="processo-partes lista-dados m-l-16 p-t-0">')
    
    lista_partes = []
    
    for parte in partes[1:]:
        tipo = extrair(parte, 'detalhe-parte">', '<').upper()
        tipo = tipo.replace('REQTE.(S)','REQTE')
        tipo = tipo.replace('INTDO.(A/S)','INTDO')
        tipo = tipo.replace('REQDO.(A/S)','INTDO')
        tipo = tipo.replace('ADV.(A/S)','ADV')
        tipo = tipo.replace('AM. CURIAE.','AMICUS')
        tipo = tipo.replace('PROC.(A/S)(ES)','ADV/PUB')
        tipo = limpar(tipo)
        nome = extrair(parte, '"nome-parte">', '<').upper()
        nome = ajustar_nome(nome)
        if tipo == 'ADV' or tipo == 'ADV/PUB':
            if "(" in nome:
                nome = extrair(nome, '', '(')
        nome = nome.strip()
        nome = nome.replace('  ',' ')
        lista_partes.append([nome, tipo, processo])
        
    return lista_partes


def extrair_andamentos(string):
    string = remover_acentos(string)
    string = limpar(limpar(string))
    andamentos = string.split('<div class="andamento-item">')
    
    n= len(andamentos)
    lista_andamentos = []
    
    for andamento in andamentos[1:]:
        data = 'NA'
        nome = 'NA'
        complemento = 'NA',
        docs = 'NA'
        julgador = 'NA'
        
        # com esse formato, os andamentos indevidos não são incorporados, pois a classe deles envolve 'andamento indevido', para gerar o taxado
        n = n-1
        ordem = str(n).zfill(4)
        andamento = andamento.replace('"col-md-9 p-0 "','"col-md-9 p-0"')
        data = extrair(andamento, '<div class="andamento-data ">','</div>').upper()
        nome = extrair(andamento, '<h5 class="andamento-nome ">','</h5>').upper()
        
        complemento = extrair(andamento, '<div class="col-md-9 p-0">','</div>').upper()
        if complemento == ' ' or complemento == '':
            complemento = 'NA'
            
        docs = extrair(andamento, '"col-md-4 andamento-docs">','</div>')
        if docs == ' ' or docs == '':
            docs = 'NA'
        if 'href=' in docs:
            docs = extrair(docs,'href="', '"')
        julgador = extrair(andamento, 'julgador badge bg-info ">','</span>').upper()
        #print ([ordem, data, nome, complemento, docs, julgador])
        
        lista_andamentos.append([ordem, data, nome, complemento, docs, julgador])
        
    return lista_andamentos

def solicitar_dados_Juris (classe, numero):
    url = ('http://portal.stf.jus.br/processos/listarProcessos.asp?classe='
           + classe
           +'&numeroProcesso='
           + numero)

    print (url)
    # Módulo básico de extração
    string = requests.get(url).text
    inicio = string.find('<a href="#" id="imprimir" onclick="sysImprimir(); return false;">Imprimir</a>')
    return (url + ">>>>> \n" + string[inicio:])

def solicitar_dados_CC (classe, numero):
    url = ('http://www.stf.jus.br/portal/peticaoInicial/verPeticaoInicial.asp?base='
    # url = ('http://www.stf.jus.br/portal/peticaoInicial/verPeticaoInicial.asp?base='

           + classe
           + '&documento=&s1=1&numProcesso='
           + numero)
    print (url)
    # Módulo básico de extração
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    string = requests.get(url, headers = user_agent).text
    inicio = string.find('processo/verProcessoAndamento.asp?')
    return (url + ">>>>> \n" + string[inicio:])


url = 'http://www.stf.jus.br/portal/pauta/listarCalendario.asp?data=03/03/2021'
html = requests.head

def solicitar_dados_mono (classe, numero):
    url = ('http://stf.jus.br/portal/jurisprudencia/listarJurisprudencia.asp?s1=%28'
           + classe
           +'%24%2ESCLA%2E+E+'
           + numero
           + '%2ENUME%2E%29+NAO+S%2EPRES%2E&base=baseMonocraticas')

    print (url)
    # Módulo básico de extração
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    string = requests.get(url, headers = user_agent).text
    inicio = string.find('<a href="#" id="imprimir" onclick="sysImprimir(); return false;">Imprimir</a>')
    return (url + ">>>>> \n" + string[inicio:])

def solicitar_dados_AP (classe, numero):
    url = ('http://portal.stf.jus.br/processos/listarProcessos.asp?classe='
           + classe
           + '&numeroProcesso='
           + numero)
    print ('url: ' + url)
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    string = requests.get(url, headers = user_agent)
    
    string.encoding = 'utf-8'
    htmlfonte = string.text
    htmlfonte = extrair(htmlfonte,
                        '<div class="processo-titulo m-b-8">',
                        '<div class="p-l-0" id="resumo-partes">')
    return (url + ">>>>> \n" + htmlfonte)

def solicitar_dados (dominio, path, querry):
    user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
    html = requests.get(dominio+path+querry, headers = user_agent)
    html.encoding = 'utf-8'
    html = html.text
    return html





def carregar_arquivo_composto (classe, numero, path):
    nomedoarquivo = (path + classe + str(0)*(4-len(numero)) + numero + '.html')
    arquivoaberto = (classe +  str(0)*(4-len(numero)) + numero + '.html')
    print (nomedoarquivo)
    arquivo = open(nomedoarquivo, 'r', encoding='utf-8')
    html = arquivo.read()
    arquivo.close()
    return arquivoaberto, html

def gerador_de_lista (path, classe, numeroinicial, numerofinal):
    lista = []
    for n in range (int(numerofinal) - int(numeroinicial) + 1):
        numero = numerofinal-n
        nomedoarquivo = (path + classe + str(0)*(4-len(str(numero))) + str(numero) + '.html')
        if nomedoarquivo in os.listdir(path):
            lista.append(nomedoarquivo)
    return lista

def gerar_lista (classe, numeroinicial, numerofinal, path):
    lista = []
    for item in range(int(numerofinal) - int(numeroinicial) +1):
        nomedoarquivo = (path + classe + ('0')*(4-len(str(item))) + str(item) + '.html')
        print (nomedoarquivo)
        lista.append(nomedoarquivo)
    return (lista)

def gerar_nome_arquivo (classe, numero, path):
    nomedoarquivo = (path + classe + str(0)*(4-len(numero)) + numero + '.html')
    return (nomedoarquivo)

def carregar_arquivo (nomedoarquivo):
    arquivo = open(nomedoarquivo, 'r', encoding='utf-8')
    html = arquivo.read()
    arquivo.close()
    return html

def gravar_dados_no_arquivo (classe, numero, path, dados):
    nomedoarquivo = (path + classe + str(0)*(4-len(numero)) + numero + '.txt')
    arquivo = open(nomedoarquivo, 'w', encoding='utf-8')
    arquivo.write(dados)
    arquivo.close
    
#repetido
def gravar_dados_no_arquivo_nome (nomedoarquivo, dados):
    arquivo = open(nomedoarquivo, 'w', encoding='utf-8')
    arquivo.write(dados)
    arquivo.close


def extrair_da_lista (relacao_de_arquivos, path):
    nomedoarquivo = relacao_de_arquivos.pop()
    arquivo = open(path + nomedoarquivo, 'r', encoding='utf-8')
    html = arquivo.read()
    arquivo.close()
    return nomedoarquivo, html

def limpa_estado(string):
    estados = [['ACRE', '/AC'],
     ['ALAGOAS', '/AL'],
     ['AMAPA', '/AP'],
     ['AMAZONAS', '/AM'],
     ['BAHIA', '/BA'],
     ['CEARA', '/CE'],
     ['DISTRITO FEDERAL', '/DF'],
     ['ESPIRITO SANTO', '/ES'],
     ['GOIAS', '/GO'],
     ['MARANHAO', '/MA'],
     ['MATO GROSSO DO SUL', '/MS'],
     ['MATO GROSSO', '/MT'],
     ['MINAS GERAIS', '/MG'],
     ['PARAIBA', '/PB'],
     ['PARANA', '/PR'],
     ['PERNAMBUCO', '/PE'],
     ['PIAUI', '/PI'],
     ['RIO DE JANEIRO', '/RJ'],
     ['RIO GRANDE DO NORTE', '/RN'],
     ['RIO GRANDE DO SUL', '/RS'],
     ['RONDONIA', '/RO'],
     ['RORAIMA', '/RR'],
     ['SANTA CATARINA', '/SC'],
     ['SAO PAULO', '/SP'],
     ['SERGIPE', '/SE'],
     ['PARA', '/PA'],
     ['TOCANTINS', '/TO']
     ]
    
    for item in estados:
        string = string.replace(item[0],item[1])
    return string

def estado_nome_completo(string):
    estados = [['ACRE', '/AC'],
     ['ALAGOAS', '/AL'],
     ['AMAPA', '/AP'],
     ['AMAZONAS', '/AM'],
     ['BAHIA', '/BA'],
     ['CEARA', '/CE'],
     ['DISTRITO FEDERAL', '/DF'],
     ['ESPIRITO SANTO', '/ES'],
     ['GOIAS', '/GO'],
     ['MARANHAO', '/MA'],
     ['MATO GROSSO DO SUL', '/MS'],
     ['MATO GROSSO', '/MT'],
     ['MINAS GERAIS', '/MG'],
     ['PARAIBA', '/PB'],
     ['PARANA', '/PR'],
     ['PERNAMBUCO', '/PE'],
     ['PIAUI', '/PI'],
     ['RIO DE JANEIRO', '/RJ'],
     ['RIO GRANDE DO NORTE', '/RN'],
     ['RIO GRANDE DO SUL', '/RS'],
     ['RONDONIA', '/RO'],
     ['RORAIMA', '/RR'],
     ['SANTA CATARINA', '/SC'],
     ['SAO PAULO', '/SP'],
     ['SERGIPE', '/SE'],
     ['PARA', '/PA'],
     ['TOCANTINS', '/TO']
     ]
    
    for item in estados:
        string = string.replace(item[1],item[0])
    return string
def siglas():
    return ['AC',
 'AL',
 'AP',
 'AM',
 'BA',
 'CE',
 'DF',
 'ES',
 'GO',
 'MA',
 'MS',
 'MT',
 'MG',
 'PB',
 'PR',
 'PE',
 'PI',
 'RJ',
 'RN',
 'RS',
 'RO',
 'RR',
 'SC',
 'SP',
 'SE',
 'PA',
 'TO']      
 
#   funções de limpeza


def limpar_numero(numero):
    numero = numero.replace('<FONT COLOR=RED><B>','')
    numero = numero.replace('</B></FONT>','')
    numero = "0"*(4-len(numero))+numero
    return numero

def limpar_classe(string):
    string = limpar(string)
    string = string.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('ACAO DIRETA DE INCONSTITUCI0NALIDADE','ADI')
    string = string.replace('7CAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('01CAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('CAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('PACAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('sACAO DIRETA DE INCONSTITUCIONALIDADE','ADI')
    string = string.replace('ARGUICAO DE DESCUMPRIMENTO DE PRECEITO FUNDAMENTAL','ADPF')
    
            
def limpar_cln(string):
    string = string.upper()
    string = remover_acentos(string)
    string = string.replace ('( MED','(MED')
    string = string.replace ('E(MED','E (MED')
    string = string.replace ('(LIMINAR)','(MED. LIMINAR)')
    string = string.replace ('E MED.','E (MED')
    string = string.replace ('CAUTELAR','LIMINAR')
    
def limpar_decisao (string):
    string = string.replace('\n','')
    string = string.replace('\t','')
    string = string.replace('     ','')
    string = string.replace('  ',' ')
    string = string.upper()
    string = remover_acentos(string)
    return string

def limpar_arquivo(nomedoarquivo):
    arquivoaberto =     open(nomedoarquivo, mode='w',
                             encoding="utf-8", newline='')
    arquivoaberto.close()





def esperar (segundos, ciclos, variavel0):
    if variavel0%ciclos == 0 and variavel0 != 0:
        print ('espera ' + str(variavel0))
        time.sleep(segundos)

#repetido
def write_csv_line (nomedoarquivo,dados):
    if dados != []:
        arquivoaberto = open(nomedoarquivo, mode='a+', encoding="utf-8", newline='')
        arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',', quotechar = '"')
        arquivoaberto_csv.writerow(dados)
        arquivoaberto.close()
        


#repetido
def write_csv_lines (nomedoarquivo, dados):
    if dados != []:
        arquivoaberto = open(nomedoarquivo, mode='a+',
                             encoding="utf-8", newline='')
        arquivoaberto_csv = csv.writer(arquivoaberto, delimiter=',', quotechar = '"')
        arquivoaberto_csv.writerows(dados)
        arquivoaberto.close()
        


def extrai_acordaos_da_string (arquivo_a_extrair, path):  # usar duas contra-barras depois do nome

    if arquivo_a_extrair in os.listdir(path):
        nome_do_arquivo = str(path+arquivo_a_extrair)

        acordaos = carregar_arquivo (nome_do_arquivo)
        # print (arquivo_a_extrair)

        n_acordaos = extrair(acordaos,'Documentos encontrados: ','</td>')
        acordaos_publicados = []

        adi_decisao = 'NA'
        acordaos_publicados = []
        acordaos_adi = []
        acordaos_agr = []
        acordaos_emb = []
        acordaos_qo = []
        acordaos_outros = []

        if "Nenhum registro encontrado" in acordaos:
            decisao_colegiada = []

        else:
            decisao_colegiada = []

            for decisoes in range (int(n_acordaos)):


                acordaos_adi    = []
                acordaos_emb    = []
                acordaos_agr    = []
                acordaos_qo     = []
                acordaos_outros = []
                lista_processos_citados = []
                lista_procesoss_citados_com_tema = []
                acordao_tipo = 'NA'
                processo_juris = 'NA'
                relator_juris = 'NA'
                data_acordao = 'NA'
                orgao_julgador_acordao = 'NA'
                publicacao_acordao = 'NA'
                ementa = 'NA'
                decisao_juris = 'NA'
                legislacao = 'NA'
                observacao = 'NA'
                doutrina = 'NA'

                acordaos = acordaos.replace ('/n/n','/n')
                acordaos = acordaos.replace ('/t','')


                processo_juris = extrair(acordaos,'''<!-- Término do trecho que passa informações para o QueryString (Pesquisa Simultânea de Jurisprudência) --''', '<br />').upper()
                processo_juris = processo_juris.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                processo_juris = processo_juris.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                if 'ADI' in arquivo_a_extrair:
                    processo_juris = processo_juris.replace('AÇÃO DECLARATÓRIA DE CONSTITUCIONALIDADE', 'ADI')
                processo_juris = processo_juris.replace('MEDIDA CAUTELAR', 'MC')
                processo_juris = processo_juris.replace('\n', '')
                processo_juris = processo_juris.replace('\t', '')
                processo_juris = processo_juris.replace('>', '')
                processo_juris = processo_juris.replace('REFERENDO NA MC','MC (REFERENDO)')
                processo_juris = processo_juris.replace('REFERENDO NOS EMB.DECL.','EMB.DECL. (REFERENDO)')
                processo_juris = processo_juris.replace('REFERENDO NO AG.REG.','AG.REG (REFERENDO)')
                processo_juris = processo_juris.replace('SEGUNDOS ','')
                processo_juris = processo_juris.replace('SEGUNDO','')
                processo_juris = processo_juris.replace('TERCEIROS','')

                acordao_tipo = 'NA'

                if processo_juris[0:3] == "MC ":
                    acordao_tipo = "MC"
                elif processo_juris[0:3] == "EMB":
                    acordao_tipo = 'EMBARGOS'
                elif processo_juris[0:2] == "AG":
                    acordao_tipo = 'AGRAVO'
                elif processo_juris[0:3] == "QUE":
                    acordao_tipo = 'QO'
                elif processo_juris[0:3] == "ADI":
                    acordao_tipo = 'PRINCIPAL'
                else:
                    acordao_tipo = 'OUTROS'


                relator_juris = extrair(acordaos, 'Relator(a):&nbsp ', '<br />').upper()
                relator_juris = relator_juris.lstrip(' ')
                relator_juris = relator_juris.lstrip('MIN.')
                relator_juris = relator_juris.lstrip(' ')
                relator_juris = remover_acentos(relator_juris)

                data_acordao = extrair(acordaos, 'Julgamento:&nbsp', '&nbsp')
                data_acordao = data_acordao.replace('\t','')

                orgao_julgador_acordao = extrair(acordaos, 'Órgão Julgador:&nbsp', '<br />')

                publicacao_acordao = extrair (acordaos, '''<PRE><span style='font-family:tahoma, verdana, arial, sans-serif;font-size:1.1 em;font-weight:bold'>''', '</PRE>')

                ementa = extrair (acordaos, '''<p><div style="line-height: 150%;text-align: justify;">''', '</div>')

                decisao_juris = extrair (acordaos, '''<p><div style="text-align:justify; color: #385260; font-weight: normal; font-size: 11px">''', '</div>')

                legislacao = extrair (acordaos, '''Legislação</strong></p>''', '</PRE>')
                legislacao = legislacao.replace('\t','')
                legislacao = legislacao.replace('\n','')

                observacao =  extrair (acordaos, '''<p><strong>Observação</strong></p>''', '</PRE>')
                if 'Acórdão(s) citado(s)' in acordaos and 'Nenhum registro encontrado' not in acordaos and 'AGUARDANDO INDEXAÇÃO' not in acordaos:
                    observacao = observacao.replace ('(s)','')
                    observacao = observacao.replace ('(2ªT)','')
                    observacao = observacao.replace ('(1ªT)','')
                    observacao = observacao.replace ('(TP)','')
                    n_cit = observacao.count('href')
                    for links in range (n_cit):
                        inicio = observacao.find ('href')
                        fim = observacao.find ('>',inicio)
                        retirar = observacao[inicio:fim]
                        observacao = observacao.replace(retirar,'')

                    observacao = observacao.replace('\n','')
                    observacao = observacao.replace('<a>','')
                    observacao = observacao.replace('<a >','')
                    observacao = observacao.replace('</a>','')
                    observacao = observacao.replace(' ,',',')
                    observacao = observacao.replace(' .','.')
                    observacao = observacao.replace('.','')


                    observacao = observacao.split('(')[1:]
                    if  observacao != [] and 'Número de páginas' in observacao[-1]:
                        observacao[-1] = extrair (observacao[-1],'','Número de páginas')
                    lista_processos_citados = []
                    lista_procesoss_citados_com_tema = []
                    for obs in range (len(observacao)):
                        elemento = observacao[obs]
                        elemento = elemento.split(')')
                        tema = [elemento.pop(0)]
                        elemento = str(elemento).split(',')
                        for item in range (len(elemento)):
                            processo_citado = elemento[item]
                            processo_citado = processo_citado.lstrip('[')
                            processo_citado = processo_citado.lstrip("]")
                            processo_citado = processo_citado.lstrip(' ')
                            processo_citado = processo_citado.lstrip("'")

                            processo_citado_e_tema = processo_citado + ',' + str(tema)
                            lista_processos_citados.append(processo_citado)
                            lista_procesoss_citados_com_tema.append(processo_citado_e_tema)


                doutrina = extrair(acordaos, '''<p><strong>Doutrina</strong></p>''', '</PRE>')



                decisao_colegiada = [arquivo_a_extrair, acordao_tipo, processo_juris, relator_juris, data_acordao, orgao_julgador_acordao, publicacao_acordao, ementa, decisao_juris, legislacao, observacao, lista_processos_citados, lista_procesoss_citados_com_tema, doutrina]
                # print (decisao_colegiada)

                acordaos_publicados.append(decisao_colegiada)
                if acordao_tipo == 'PRINCIPAL':
                    acordaos_adi.append(decisao_colegiada)
                    adi_decisao = decisao_juris
                if acordao_tipo == 'EMB':
                    acordaos_emb.append(decisao_colegiada)
                if acordao_tipo == 'AGR':
                    acordaos_agr.append(decisao_colegiada)
                if acordao_tipo == 'QO':
                    acordaos_qo.append(decisao_colegiada)
                if acordao_tipo == 'OUTROS':
                    acordaos_outros.append(decisao_colegiada)




            recortar = acordaos.find('<!-- Término do trecho que passa informações para o QueryString (Pesquisa Simultânea de Jurisprudência) --')
            acordaos = acordaos[recortar+len('<!-- Término do trecho que passa informações para o QueryString (Pesquisa Simultânea de Jurisprudência) --'):]
        return (arquivo_a_extrair,
                adi_decisao,
                acordaos_publicados,
                acordaos_adi,
                acordaos_agr,
                acordaos_emb,
                acordaos_qo,
                acordaos_outros)
    else:
        return ([], 'NA', [], [], [], [], [], [])


def extrai_mono_da_string (arquivo_a_extrair, path):  # usar duas contra-barras depois do nome

        if arquivo_a_extrair in os.listdir(path):
            
            nome_do_arquivo = str(path+arquivo_a_extrair)

            monocraticas = carregar_arquivo (nome_do_arquivo)
            # print (arquivo_a_extrair)

            # n_monocraticas = extrair(monocraticas,'Documentos encontrados: ','</td>')


            n_monocraticas = monocraticas.count('img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;')

            adi_decisao_mono = 'NA'
            monocraticas_publicadas = []
            monocraticas_adi = []
            monocraticas_agr = []
            monocraticas_emb = []
            monocraticas_qo = []
            monocraticas_outros = []
            monocraticas_amicus = []
            monocraticas_mc = []
            monocraticas_publicadas = []
            processo_juris = 'NA'


            if "Nenhum registro encontrado" in monocraticas:
                decisao_monocratica = []

            else:
                decisao_monocratica = []

                for decisoes in range (int(n_monocraticas)):


                    monocraticas_adi    = []
                    monocraticas_emb    = []
                    monocraticas_agr    = []
                    monocraticas_qo     = []
                    monocraticas_outros = []

                    acordao_tipo = 'NA'
                    processo_juris = 'NA'
                    relator_juris = 'NA'
                    data_acordao = 'NA'
                    orgao_julgador_acordao = 'NA'
                    decisao_juris = 'NA'
                    legislacao = 'NA'
                    observacao = 'NA'


                    monocraticas = monocraticas.replace ('/n/n','/n')
                    monocraticas = monocraticas.replace ('/t','')


                    processo_juris = extrair(monocraticas,'''<img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;" />''', '<br />').upper()

                    processo_juris = processo_juris.replace('AÇÃO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                    processo_juris = processo_juris.replace('ACAO DIRETA DE INCONSTITUCIONALIDADE', 'ADI')
                    processo_juris = processo_juris.replace('MEDIDA CAUTELAR', 'MC')
                    processo_juris = processo_juris.replace('\n', '')
                    processo_juris = processo_juris.replace('\t', '')
                    processo_juris = processo_juris.split('<STRONG>')[1]

                    acordao_tipo = 'na'

                    if "AMICUS" in processo_juris:
                        moocratica_tipo = "AMICUS"
                    elif 'MC' in processo_juris or 'CAUT' in processo_juris:
                        moocratica_tipo = "CAUT"
                    elif 'EMB.' in processo_juris:
                        moocratica_tipo = 'EMB'
                    elif 'AG.REG' in processo_juris:
                        moocratica_tipo = 'AGR'
                    elif 'ORDEM' in processo_juris or 'QO' in processo_juris:
                        moocratica_tipo = 'QO'
                    elif processo_juris[0:3] == "ADI":
                        moocratica_tipo = 'PRINCIPAL'
                    else:
                        moocratica_tipo = 'OUTROS'


                    relator_juris = extrair(monocraticas, 'Relator(a):&nbsp ', '<br />').upper()
                    relator_juris = relator_juris.lstrip(' ')
                    relator_juris = relator_juris.lstrip('MIN.')
                    relator_juris = relator_juris.lstrip(' ')
                    relator_juris = remover_acentos(relator_juris)

                    data_acordao = extrair(monocraticas, 'Julgamento:&nbsp', '&nbsp')
                    data_acordao = data_acordao.replace('\t','')

                    orgao_julgador_acordao = relator_juris

                    publicacao_monocratica = extrair (monocraticas, '''<pre><span style='font-family:tahoma, verdana, arial, sans-serif;font-size:1.1 em;font-weight:bold'>''', '</pre>')


                    decisao_juris = extrair (monocraticas, '''Decisão</strong></p>''', '</pre>')
                    if '<pre>' in decisao_juris:
                        decisao_juris = decisao_juris.split('<pre>')[1]
                    decisao_juris = limpar(decisao_juris)
                    decisao_juris = decisao_juris.replace('\n\n','\n')



                    legislacao = extrair (monocraticas, '''Legislação</strong></p>''', '</pre>')
                    legislacao = legislacao.replace('\t','')
                    legislacao = legislacao.replace('\n','')

                    observacao =  extrair (monocraticas, '''<p><strong>observação</strong></p>''', '</pre>')



                    decisao_monocratica = [arquivo_a_extrair, acordao_tipo, processo_juris, relator_juris, data_acordao, orgao_julgador_acordao, publicacao_monocratica, decisao_juris, legislacao, observacao]
                    # print (decisao_monocratica)

                    monocraticas_publicadas.append(decisao_monocratica)
                    if moocratica_tipo == 'PRINCIPAL':
                        monocraticas_adi.append(decisao_monocratica)
                        adi_decisao_mono = decisao_juris
                    if moocratica_tipo == 'EMB':
                        monocraticas_emb.append(decisao_monocratica)
                    if moocratica_tipo == 'AGR':
                        monocraticas_agr.append(decisao_monocratica)
                    if moocratica_tipo == 'QO':
                        monocraticas_qo.append(decisao_monocratica)
                    if moocratica_tipo == 'OUTROS':
                        monocraticas_outros.append(decisao_monocratica)
                    if moocratica_tipo == 'AMICUS':
                        monocraticas_amicus.append(decisao_monocratica)
                    if moocratica_tipo == 'MC':
                        monocraticas_mc.append(decisao_monocratica)



                recortar = monocraticas.find('''<img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;" />''')
                monocraticas = monocraticas[recortar+len('''<img src="imagem/bt_imprimirpopup.gif" alt="Imprimir" style="position:relative;left:490px;top:-38px;margin-bottom:-55px;" />'''):]
            return (processo_juris,
                    arquivo_a_extrair,
                    adi_decisao_mono,
                    monocraticas_publicadas,
                    monocraticas_adi,
                    monocraticas_mc,
                    monocraticas_agr,
                    monocraticas_emb,
                    monocraticas_qo,
                    monocraticas_amicus,
                    monocraticas_outros)
        else:
            return ([], 'NA', [], [], [], [], [], [], [],[], [])
        
def substituir_data (string):
    string = string.lower()
    string = string.replace('jan','01')
    string = string.replace('fev','02')
    string = string.replace('mar','03')
    string = string.replace('abr','04')
    string = string.replace('mai','05')
    string = string.replace('jun','06')
    string = string.replace('jul','07')
    string = string.replace('ago','08')
    string = string.replace('set','09')
    string = string.replace('out','10')
    string = string.replace('nov','11')
    string = string.replace('dez','11')
    
    return(string)

def inserir_ocorrencias(lista):

    contador = 0
    for item in lista:
        contador = contador + 1
        ocorrencias_item = str(lista).count("'" + item[0] + "'")
        item.insert(1,ocorrencias_item)
        print ('Inserindo número de ocorrências: ' + str(contador) + ' de ' + str(len(lista)))
    # return lista.sort()

def consolidar_entradas (lista):
    partes_unicas = []
    contador = 0
    if len(lista) > 0:
        contador = contador +1
        for n in range(len(lista)-1):
            print ('Consolidando entradas: ' + str(contador) + ' de ' + str(len(lista)*2))
            if lista[n][0] == lista[n+1][0]:
                lista[n+1][2].extend(lista[n][2])
                lista[n][2] = lista[n+1][2]
                
            
        for n in range(len(lista)-1):
            contador = contador + 1
            print ('Consolidando entradas: ' + str(contador) + ' de ' + str(len(lista)*2))
            if lista[n][0] != lista[n+1][0]:
                partes_unicas.append(lista[n])
        if lista[-1][0] != lista[-2][0]:
            partes_unicas.append(lista[-1])
        
        
    partes_unicas.sort()
    return (partes_unicas)

def igualar_entradas_identicas_partes (lista,iguais):
    
    lista.sort(reverse = True, key = lambda elem: elem[0])
    for i in range(len(lista)-1):
        item1 = lista[i]
        item2 = lista[i+1]
        if item2[0] == item1[0][:len(item2[0])]:
            if (item1[0] != item2[0] 
                and len(item2[0]) > 18 
                and '/' not in item1[0] 
                and '.' not in item1[0]):
                #mantém o que tem mais entradas
                if lista[i+1][1] > lista[i][1]:
                    iguais.append((lista[i+1][0], lista[i+1][1],lista[i+1][0],lista[i][1]))
                    lista[i+1][0] = lista[i][0]
                else:
                    iguais.append((lista[i][0],lista[i][1],lista[i+1][0],lista[i+1][1]))
                    lista[i+1][0] = lista[i][0]
            elif (item2[0] == 'CIDADANIA' or
                  'OAB' in item2[0] or
                  'SIND.' in item2[0] or
                  'MP DO TRABALHO' in item2[0] or
                  'RECEITA FEDERAL' in item2[0] or 
                  'CONS.NAC.' in item2[0]
                  ):
                #mantém o que tem mais entradas
                if lista[i+1][1] > lista[i][1]:
                    iguais.append((lista[i+1][0], lista[i+1][1],lista[i+1][0],lista[i][1]))
                    lista[i+1][0] = lista[i][0]
                else:
                    iguais.append((lista[i][0],lista[i][1],lista[i+1][0],lista[i+1][1]))
                    lista[i+1][0] = lista[i][0]
    lista.sort()
    return lista,iguais

def igualar_entradas_identicas_partes_advogados (lista,iguais):
    
    lista.sort(reverse = False, key = lambda elem: elem[0])
    for i in range(len(lista)-1):
        item1 = lista[i]
        item2 = lista[i+1]
        if (item1[0] == item2[0][:len(item1[0])] 
            and item1[0] != item2[0] 
            and len(item2[0]) > 18 
            and '/' not in item1[0] 
            and '.' not in item1[0] 
            and 'CLAUDIO SANTOS' not in item1[0]):
            if lista[i+1][1] > lista[i][1]:
                iguais.append((lista[i+1][0], lista[i+1][1],lista[i+1][0],lista[i][1]))
                lista[i+1][0] = lista[i][0]
            else:
                iguais.append((lista[i][0],lista[i][1],lista[i+1][0],lista[i+1][1]))
                lista[i+1][0] = lista[i][0]          
    lista.sort()
    return lista,iguais

def consolida_partes (lista):
    for item in lista:
        processo_parte = (item[1],item[2])
        item.append([processo_parte])
        item.pop(1)
        item.pop(1)
    return lista

def ajusta_requerentes (string):
    string = string.replace('FERNANDO AFFONSO COLLOR DE MELLO','ALAGOAS')
    string = string.replace('ADVOGADO GERAL DA UNIAO','PRESIDENTE DA REPUBLICA')
    string = string.replace('FENABAN ', '')
    string = string.replace('SINDICATO D','SIND. D')
    

    governadores = ['ACRE',
                     'ALAGOAS',
                     'AMAPA',
                     'AMAZONAS',
                     'BAHIA',
                     'CEARA',
                     'ESPIRITO SANTO',
                     'GOIAS',
                     'MARANHAO',
                     'MATO GROSSO',
                     'MATO GROSSO DO SUL',
                     'MINAS GERAIS',
                     'PARA',
                     'PARAIBA',
                     'PARANA',
                     'PARANA',
                     'PERNAMBUCO',
                     'PIAUI',
                     'PROC.GERAL DO AMAPA',
                     'RIO DE JANEIRO',
                     'RIO GRANDE DO NORTE',
                     'RIO GRANDE DO SUL',
                     'RONDONIA',
                     'RORAIMA',
                     'SANTA CATARINA',
                     'SAO PAULO',
                     'SERGIPE',
                     'TOCANTINS',
                     'TOCANTINSMATO GROSSO']
    for item in governadores:
        if string == item:
            string = 'GOV./' + item

    
    return string

def converter_csv_excel (arquivo):
    
    dados = carregar_arquivo(arquivo)
    
    dados = dados.replace(';[',';"[')
    dados = dados.replace('];',']";')
    dados = dados.replace(';',',')
    
    return (dados)

def processar_andamentos (andamentos):
    
    a_analisar = []
    andamentos_excluidos = []
    andamentos_filtrados = []
    interlocutorias = []
    atas = []
    virtual = []
    redistribui = []
    embargos = []
    despachos = []
    agravos = []
    pautas = []
    pedidos = []
    baixadoem = 'NA'
    primeirorelator = 'NA'
    prevencao = 'NA'
    ministroexcluido = 'NA'
    protocolado = 'NA'
    autuado = 'NA'
    processofindo = 'NA'
    ritoart12 = 'NA'
    transitoemjulgado = 'NA'
    orgaojulg = 'NA'
    conexo = 'NA'
    
#     for andamento in andamentos:
#         if andamento == ['']:
#             break
#         else:
            
#             index = andamento[0]
#             data = andamento[1]
#             nome = andamento[2]
#             complemento = andamento[3]
#             julgador = andamento[5]
    
#             nome = nome.replace('JULG. ','JULGAMENTO ')
#             nome = nome.replace('  ', ' ')
#             nome = nome.replace('JULGAMENTO NO PLENO', 'JULGAMENTO DO PLENO:')
#             nome = nome.replace('JULG. POR DESPACHO -', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('DECISAO DA RELATORA', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('DECISAO DO RELATOR', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('DECISAO DO(A) RELATOR(A) -', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('DECISAO DO(A) RELATOR(A) -', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('JULGAMENTO POR DESPACHO -', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('JULGAMENTO DO PLENO -', 'JULGAMENTO DO PLENO:')
#             nome = nome.replace('JULGAMENTO DO PLENO', 'JULGAMENTO DO PLENO:')
#             nome = nome.replace('DECISAO DA PRESIDENCIA -', 'DECISAO DA PRESIDENCIA:')
#             nome = nome.replace('DO RELATOR NO PL','')
#             nome = nome.replace('CONEXA COM O PROCESSO N', 'CONEXAO: ')
#             nome = nome.replace('CONEXAO PROC. N.', 'CONEXAO')
#             nome = nome.replace('DECISAO LIMINAR -', 'LIMINAR:')
#             nome = nome.replace('LIMINAR POR DESPACHO','LIMINAR JULGADA POR DESPACHO:')
#             nome = nome.replace('LIMINAR JULGAMENTO POR DESPACHO','LIMINAR JULGADA POR DESPACHO:')
#             nome = nome.replace('::',':')
    
#             if nome == 'DEFERIDA':
#                 nome = nome.replace('DEFERIDA','LIMINAR DEFERIDA')
            
#             if nome == 'DEF. EM PARTE':
#                 nome = nome.replace('DEF. EM PARTE','LIMINAR DEFERIDA EM PARTE')
            
#             if 'NAO VERIFICO NA ESPECIE A PRESENÇA DE PERICULUM IN MORA' in complemento and nome == '':
#                 nome = 'LIMINAR INDEFERIDA'
                
#             if 'COLHAM-SE, PRIMEIRAMENTE, AS MANIFESTACOES' in complemento and nome == '':
#                 nome = 'VISTA AO AGU'
                
#             if 'NEGO SEGUIMENTO A INICIAL' in complemento:
#                 nome = 'NEGADO SEGUIMENTO'
                
#             if 'ANTE O EXPOSTO, NEGO SEGUIMENTO A PRESENTE ACA0' in complemento:
#                 nome = 'NEGADO SEGUIMENTO'
                
#             if 'INDEFIRO LIMINARMENTE O PEDIDO' in complemento:
#                 nome = 'INDEFERIDA A INICIAL'
                
        
#         AutuacaoRetificada = 'NA'
#         if 'RETIFICACAO DE AUTUACAO' in nome or 'RETIFICACAO DE AUTUACAO' in complemento:
#             AutuacaoRetificada = 'sim'
            
#         if (data == 'NA' or
#             'VISTA A PGR PARA FINS DE INTIMACAO' in nome or
#             'VISTA AO ADV' in nome or
#             'VISTA AO PROCURADOR-GERAL' in nome or
#             'RETIFICACAO DE AUTUACAO' in nome or 
#             'LANÇAMENTO INDEVIDO' in nome or 
#             'AMENTO INDEVIDO' in nome or 
#             'CONVERTIDO EM ELET' in nome or 
#             'APENSADO' in nome or 
#             'APENSACAO' in nome or
#             'DETERMINADA A REDISTRIB' in nome or
#             'DETERMINADA CITACAO' in nome or
#             'DETERMINADA INTIMACAO' in nome or
#             nome[:7] == 'CONCLUS' or 
#             'CONCLUSOS' in nome or 
#             nome == 'CONCLUSAO' or 
#             nome[:5] == "AUTOS" or 
#             'REMESSA DOS AUTOS' in nome or 
#             'COBRADA A DEVOLU' in nome or
#             nome == 'CERTIDAO' or 
#             nome == 'PETICAO' or 
#             'ARQUIVADA A PET' in nome or 
#             nome == 'CIENCIA' or 
#             nome == 'CIENTE' or
#             nome[:9] == 'COMUNICAD' or 
#             nome[:6] == 'INTIMA' or 
#             'COMUNICACAO ASSINAD' in nome or
#             'INFORMACOES PRESTADAS' in nome or
#             'JUNTADA' in nome or 
#             'DEVOLUCA DE' in nome or
#             'VISTA A PGR' in nome or 
#             'RECEBIMENTO DOS' in nome or 
#             'MANIFESTACAO DA' in nome or
#             nome == 'PETICAO AVULSA' or 
#             nome == 'PETICAO' or 
#             'DESENTRANHAMENTO' in nome or 
#             'RECEBIMENTO EXTERNO DOS AUTOS' in nome or
#             nome == 'VISTA AO AGU' or
#             'PUBLICADA, DJ' in nome or 
#             'JULGAMENTO PUBLICADA' in nome or
#             'DECISAO PUBLICADA' in nome or 
#             nome == 'DECISAO PUBLICADA, DJ:' or 
#             'PUBLICADA NO D' in nome or 
#             'REPUBLICAD' in nome or
#             nome == 'REMESSA DOS AUTOS' or
#             nome == 'REMESSA' or
#             'AUTOS DEVOLVIDOS' in nome or
#             nome[:7] == 'INFORMA' or
#             nome[:7] == 'PUBLICA' or
#             nome == 'VIDE' or
#             nome == 'ACORDAO N.:'or
#             nome == 'REMESSA:' or
#             nome == 'REMESSA' or
#             nome == 'AUTOS COM:' or
#             'EXPEDIDO' in nome or
#             nome[:7] == 'PUBLICA' or
#             'COMUNICADA D' in nome or
#             nome[:8] == 'COMUNICA' or
#             'INFORMACOES RECEBIDAS' in nome or
#             'EXPEDIDO OFICIO N' in nome or
#             nome[:6] == 'EXPEDI' or
#             'PEDIDO DE INFORMACOES' in nome):
#                 index = 'EXCLUIDO'
        
#         # campo baixado
#         if (nome == 'DECORRIDO O PRAZO'):
#             transitoemjulgado = data 
#             index = 'FILTRADO'

#         if (nome == 'TRANSITADO EM JULGADO' or
#             nome == "TRANSITADO(A) EM JULGADO"):
#             transitoemjulgado = data 
#             index = 'FILTRADO'  

#         if nome[:5] == "BAIXA":
#             baixadoem = data
#             index = 'FILTRADO'
            
#         if nome == 'PROCESSO FINDO':
#             processofindo = data
#             index = 'FILTRADO'
            
#         if nome == 'PROTOCOLADO':
#             protocolado = data 
#             index = 'FILTRADO'
            
#         if nome == 'AUTUADO':
#             autuado = data 
#             index = 'FILTRADO'
            
            
#         if (nome == 'DISTRIBUIDO' or 
#                 nome == 'REGISTRADO'):
#             distribuido = data
#             primeirorelator = complemento
#             primeirorelator = primeirorelator.replace('MIN. ','')
#             index = 'FILTRADO'
            

#         if (nome == 'REGISTRADO A PRESIDENCIA' or 
#             nome == 'REGISTRADO'):
#             distribuido = data
#             primeirorelator = 'PRESIDENTE'
#             index = 'FILTRADO'
            
#         if (nome == 'DISTRIBUIDO POR PREVENCAO' or
#             nome == 'DISTRIBUÍDO POR PREVENÇÃO'):
#             distribuido = data
#             primeirorelator = complemento
#             prevencao = "PREVENÇÃO"
#             index = 'FILTRADO'
    
#         if (nome == 'DISTRIBUIDO/EXCLUSAO DE MINISTRO' or 
#             'DISTRIBUIDO POR EXCLUS' in nome):
#             distribuido = data
#             ministroexcluido = complemento
#             ministroexcluido = ministroexcluido.replace("MIN. ",'')
#             index = 'FILTRADO'        
            
#         if nome[:7]=='CONEXAO' or nome == 'CONEXAO':
#             conexo = complemento
#             index = 'FILTRADO'


# #       # Identifica Rito do Art. 12, da Lei 9.868/99':
#         if ('ADOTADO RITO DO ART. 12' in complemento or 
#                 'ADOTADO RITO DO ART. 12' in nome or 
#                 'ADOTO O RITO DO ART. 12' in complemento or 
#                 'COM A ADOÇÃO DO RITO DE TRAMITAÇÃO ABREVIADA' in complemento or 
#                 'ENTENDO TER APLICAÇÃO NA HIPÓTESE O DISPOSTO NO ARTIGO 12 DA LEI 9868/99' in complemento):
#                 nome ='LIMINAR INDEFERIMENTO IMPLÍCITO (RITO ART. 12)'  
                
#         if (' RITO' in complemento and
#                   '12' in complemento and 
#                   'ART' in complemento):
#                 ritoart12 = data
                
#         if (' RITO' in nome and
#                   '12' in nome and 
#                   'ART' in nome):
#                 ritoart12 = data
                
#         # insere orgaojulg         
#         if 'JULGAMENTO DO PLENO' in nome:
#             nome = nome.replace('JULGAMENTO DO PLENO','')
#             orgaojulg = 'PLENO'
            
#         if 'JULGAMENTO POR DESPACHO' in nome and julgador == '':
#             nome=nome.replace('JULGAMENTO POR DESPACHO','')
#             orgaojulg = 'MONOCRATICA'
            
       
#         if 'LIMINAR JULGADA PELO PLENO - ' in nome:
#               nome = nome.replace('LIMINAR JULGADA PELO PLENO - ','')
#               orgaojulg = 'PLENO'
              
#         if 'LIMINAR JULGADA POR DESPACHO - ' in nome:
#               nome = nome.replace('LIMINAR JULGADA POR DESPACHO - ','')
#               orgaojulg = 'MONOCRATICA'
              
#         if 'DECISÃO DA PRESIDÊNCIA' in nome:
#               orgaojulg = 'PRESIDENCIA'
              
#           # #identifica decisoes secundárias

          
# # # questoes de ordem
#         if (   nome == 'QUESTAO DE ORDEM' or 
#             'DECISAO INTERLOCUTORIA' in nome or 
#             nome[:8] == 'DETERMINAD'):
#             interlocutorias.append(andamento)
#             index = 'FILTRADO'
            
#         if 'ATA DE JULGAMENTO' in nome:
#             atas.append(andamento)
#             index = 'FILTRADO'
            
#         if 'JULGAMENTO VIRTUAL' in nome:
#             virtual.append(andamento)
#             index = 'FILTRADO'    
            
#         if ('REDISTRIBU' in nome or 
#             'SUBSTITUIÇÃO DO RELATOR' in nome or 
#             'SUBSTITUICAO DO RELATOR' in nome or 
#             'REDISTRIBUA-SE' in complemento):
#             redistribui.append(andamento)
#             index = 'FILTRADO'
            
#         if ('EMBARGOS' in nome or 
#             'INTERPOSTOS' in nome):
#             embargos.append(andamento)
#             index = 'FILTRADO'
            
#         if  ('DETERMINADA DILI' in nome or 
#             'DESPACHO ORDINATORIO' in nome or 
#             nome == 'DESPACHO' or 
#             nome[:8] == 'DESPACHO'):
#             despachos.append(andamento)
#             index = 'FILTRADO'
            
#         if ('AGRAVO ' in nome or 
#             'INTERPOSTO ' in nome or 
#             'HOMOLOGADA A DESISTENCIA' in nome or 
#             nome == 'REJEITADO'):
#             agravos.append(andamento)
#             index = 'FILTRADO'
            
#         if  ('RETIRADO DA MESA' in nome or 
#                 nome == 'ADIADO O JULGAMENTO' or 
#                 'NA LISTA DE JULGAMENTO' in nome or 
#                 'PROCESSO A JULGAMENTO' in nome or 
#                 'PAUTA' in nome or 
#                 'CALENDARIO' in nome or 
#                 'DIA PARA JULGAMENTO' in nome or 
#                 'EM MESA PARA' in nome or 
#                 'PAUTA' in nome or 
#                 'EM MESA' in nome or 
#                 'DE MESA' in nome or 
#                 'COM DIA PARA JULGAMENTO' in nome):
#             pautas.append(andamento)
#             index = 'FILTRADO'
            
#         if ('PEDIDO DE LIMINAR' in nome or 
#                 'REQUERIDA TUTELA PROVISORIA' in nome):
#             pedidos.append(andamento)
#             index = 'FILTRADO'
            
#         # ampliando data de transito para baixado ou processo findo
#         if baixadoem == 'NA':
#             baixadoem = processofindo
            
#         if transitoemjulgado == 'NA':
#             transitoemjulgado = baixadoem
                
#         # andamento[0] = index
#         # andamento[1] = data
#         # andamento[2] = nome
#         # andamento[3] = complemento
#         # andamento[5] = julgador
        
#         andamento.append(orgaojulg)

#         if index == 'FILTRADO':
#             andamentos_filtrados.append(andamento)
        
#         elif index == 'EXCLUIDO':
#             andamentos_excluidos.append(andamento)
            
#         else:
#             a_analisar.append(andamento)
            
#     if andamentos != []:
#         data_ultimo_andamento = andamentos[0][1]   
#     else:
#         data_ultimo_andamento = 'NA'
            
#     return (andamentos_filtrados, andamentos_excluidos, a_analisar, interlocutorias, 
#             atas, virtual, redistribui, embargos, despachos, agravos, pautas, pedidos, 
#             baixadoem, primeirorelator, prevencao, ministroexcluido, protocolado, autuado,
#             processofindo, ritoart12, transitoemjulgado, orgaojulg, conexo, 
#             AutuacaoRetificada, data_ultimo_andamento)

# def processar_andamentos2 (andamentos):
    
#     a_analisar = []
#     andamentos_excluidos = []
#     andamentos_filtrados = []
#     interlocutorias = []
#     atas = []
#     virtual = []
#     redistribui = []
#     embargos = []
#     despachos = []
#     agravos = []
#     pautas = []
#     pedidos = []
#     baixadoem = 'NA'
#     primeirorelator = 'NA'
#     prevencao = 'NA'
#     ministroexcluido = 'NA'
#     protocolado = 'NA'
#     autuado = 'NA'
#     processofindo = 'NA'
#     ritoart12 = 'NA'
#     transitoemjulgado = 'NA'
#     orgaojulg = 'NA'
#     conexo = 'NA'
    
#     for andamento in andamentos:
#         if andamento == ['']:
#             break
#         else:
            
#             index = andamento[0]
#             data = andamento[1]
#             nome = andamento[2]
#             complemento = andamento[3]
#             julgador = andamento[5]
    
#             nome = nome.replace('JULG. ','JULGAMENTO ')
#             nome = nome.replace('  ', ' ')
#             nome = nome.replace('JULGAMENTO NO PLENO', 'JULGAMENTO DO PLENO:')
#             nome = nome.replace('JULG. POR DESPACHO -', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('DECISAO DA RELATORA', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('DECISAO DO RELATOR', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('DECISAO DO(A) RELATOR(A) -', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('DECISAO DO(A) RELATOR(A) -', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('JULGAMENTO POR DESPACHO -', 'JULGAMENTO POR DESPACHO:')
#             nome = nome.replace('JULGAMENTO DO PLENO -', 'JULGAMENTO DO PLENO:')
#             nome = nome.replace('JULGAMENTO DO PLENO', 'JULGAMENTO DO PLENO:')
#             nome = nome.replace('DECISAO DA PRESIDENCIA -', 'DECISAO DA PRESIDENCIA:')
#             nome = nome.replace('DO RELATOR NO PL','')
#             nome = nome.replace('CONEXA COM O PROCESSO N', 'CONEXAO: ')
#             nome = nome.replace('CONEXAO PROC. N.', 'CONEXAO')
#             nome = nome.replace('DECISAO LIMINAR -', 'LIMINAR:')
#             nome = nome.replace('LIMINAR POR DESPACHO','LIMINAR JULGADA POR DESPACHO:')
#             nome = nome.replace('LIMINAR JULGAMENTO POR DESPACHO','LIMINAR JULGADA POR DESPACHO:')
#             nome = nome.replace('::',':')
    
#             if nome == 'DEFERIDA':
#                 nome = nome.replace('DEFERIDA','LIMINAR DEFERIDA')
            
#             if nome == 'DEF. EM PARTE':
#                 nome = nome.replace('DEF. EM PARTE','LIMINAR DEFERIDA EM PARTE')
            
#             if 'NAO VERIFICO NA ESPECIE A PRESENÇA DE PERICULUM IN MORA' in complemento and nome == '':
#                 nome = 'LIMINAR INDEFERIDA'
                
#             if 'COLHAM-SE, PRIMEIRAMENTE, AS MANIFESTACOES' in complemento and nome == '':
#                 nome = 'VISTA AO AGU'
                
#             if 'NEGO SEGUIMENTO A INICIAL' in complemento:
#                 nome = 'NEGADO SEGUIMENTO'
                
#             if 'ANTE O EXPOSTO, NEGO SEGUIMENTO A PRESENTE ACA0' in complemento:
#                 nome = 'NEGADO SEGUIMENTO'
                
#             if 'INDEFIRO LIMINARMENTE O PEDIDO' in complemento:
#                 nome = 'INDEFERIDA A INICIAL'
                
        
#         autuacao_retificada = 'NA'
#         if 'RETIFICACAO DE AUTUACAO' in nome or 'RETIFICACAO DE AUTUACAO' in complemento:
#             autuacao_retificada = 'sim'
#             index = 'FILTRADO'
            
            
# #         if (data == 'NA' or
# #             'VISTA A PGR PARA FINS DE INTIMACAO' in nome or
# #             'VISTA AO ADV' in nome or
# #             'VISTA AO PROCURADOR-GERAL' in nome or
# #             'RETIFICACAO DE AUTUACAO' in nome or 
# #             'LANÇAMENTO INDEVIDO' in nome or 
# #             'AMENTO INDEVIDO' in nome or 
# #             'CONVERTIDO EM ELET' in nome or 
# #             'APENSADO' in nome or 
# #             'APENSACAO' in nome or
# #             'DETERMINADA A REDISTRIB' in nome or
# #             'DETERMINADA CITACAO' in nome or
# #             'DETERMINADA INTIMACAO' in nome or
# #             nome[:7] == 'CONCLUS' or 
# #             'CONCLUSOS' in nome or 
# #             nome == 'CONCLUSAO' or 
# #             nome[:5] == "AUTOS" or 
# #             'REMESSA DOS AUTOS' in nome or 
# #             'COBRADA A DEVOLU' in nome or
# #             nome == 'CERTIDAO' or 
# #             nome == 'PETICAO' or 
# #             'ARQUIVADA A PET' in nome or 
# #             nome == 'CIENCIA' or 
# #             nome == 'CIENTE' or
# #             nome[:9] == 'COMUNICAD' or 
# #             nome[:6] == 'INTIMA' or 
# #             'COMUNICACAO ASSINAD' in nome or
# #             'INFORMACOES PRESTADAS' in nome or
# #             'JUNTADA' in nome or 
# #             'DEVOLUCA DE' in nome or
# #             'VISTA A PGR' in nome or 
# #             'RECEBIMENTO DOS' in nome or 
# #             'MANIFESTACAO DA' in nome or
# #             nome == 'PETICAO AVULSA' or 
# #             nome == 'PETICAO' or 
# #             'DESENTRANHAMENTO' in nome or 
# #             'RECEBIMENTO EXTERNO DOS AUTOS' in nome or
# #             nome == 'VISTA AO AGU' or
# #             'PUBLICADA, DJ' in nome or 
# #             'JULGAMENTO PUBLICADA' in nome or
# #             'DECISAO PUBLICADA' in nome or 
# #             nome == 'DECISAO PUBLICADA, DJ:' or 
# #             'PUBLICADA NO D' in nome or 
# #             'REPUBLICAD' in nome or
# #             nome == 'REMESSA DOS AUTOS' or
# #             nome == 'REMESSA' or
# #             'AUTOS DEVOLVIDOS' in nome or
# #             nome[:7] == 'INFORMA' or
# #             nome[:7] == 'PUBLICA' or
# #             nome == 'VIDE' or
# #             nome == 'ACORDAO N.:'or
# #             nome == 'REMESSA:' or
# #             nome == 'REMESSA' or
# #             nome == 'AUTOS COM:' or
# #             'EXPEDIDO' in nome or
# #             nome[:7] == 'PUBLICA' or
# #             'COMUNICADA D' in nome or
# #             nome[:8] == 'COMUNICA' or
# #             'INFORMACOES RECEBIDAS' in nome or
# #             'EXPEDIDO OFICIO N' in nome or
# #             nome[:6] == 'EXPEDI' or
# #             'PEDIDO DE INFORMACOES' in nome):
# #                 index = 'EXCLUIDO'
        
# #         # campo baixado
# #         if (nome == 'DECORRIDO O PRAZO'):
# #             transitoemjulgado = data 
# #             index = 'FILTRADO'

# #         if (nome == 'TRANSITADO EM JULGADO' or
# #             nome == "TRANSITADO(A) EM JULGADO"):
# #             transitoemjulgado = data 
# #             index = 'FILTRADO'  

# #         if nome[:5] == "BAIXA":
# #             baixadoem = data
# #             index = 'FILTRADO'
            
# #         if nome == 'PROCESSO FINDO':
# #             processofindo = data
# #             index = 'FILTRADO'
            
# #         if nome == 'PROTOCOLADO':
# #             protocolado = data 
# #             index = 'FILTRADO'
            
# #         if nome == 'AUTUADO':
# #             autuado = data 
# #             index = 'FILTRADO'
            
            
# #         if (nome == 'DISTRIBUIDO' or 
# #                 nome == 'REGISTRADO'):
# #             distribuido = data
# #             primeirorelator = complemento
# #             primeirorelator = primeirorelator.replace('MIN. ','')
# #             index = 'FILTRADO'
            

# #         if (nome == 'REGISTRADO A PRESIDENCIA' or 
# #             nome == 'REGISTRADO'):
# #             distribuido = data
# #             primeirorelator = 'PRESIDENTE'
# #             index = 'FILTRADO'
            
# #         if (nome == 'DISTRIBUIDO POR PREVENCAO' or
# #             nome == 'DISTRIBUÍDO POR PREVENÇÃO'):
# #             distribuido = data
# #             primeirorelator = complemento
# #             prevencao = "PREVENÇÃO"
# #             index = 'FILTRADO'
    
# #         if (nome == 'DISTRIBUIDO/EXCLUSAO DE MINISTRO' or 
# #             'DISTRIBUIDO POR EXCLUS' in nome):
# #             distribuido = data
# #             ministroexcluido = complemento
# #             ministroexcluido = ministroexcluido.replace("MIN. ",'')
# #             index = 'FILTRADO'        
            
# #         if nome[:7]=='CONEXAO' or nome == 'CONEXAO':
# #             conexo = complemento
# #             index = 'FILTRADO'


# # #       # Identifica Rito do Art. 12, da Lei 9.868/99':
# #         if ('ADOTADO RITO DO ART. 12' in complemento or 
# #                 'ADOTADO RITO DO ART. 12' in nome or 
# #                 'ADOTO O RITO DO ART. 12' in complemento or 
# #                 'COM A ADOÇÃO DO RITO DE TRAMITAÇÃO ABREVIADA' in complemento or 
# #                 'ENTENDO TER APLICAÇÃO NA HIPÓTESE O DISPOSTO NO ARTIGO 12 DA LEI 9868/99' in complemento):
# #                 nome ='LIMINAR INDEFERIMENTO IMPLÍCITO (RITO ART. 12)'  
                
# #         if (' RITO' in complemento and
# #                   '12' in complemento and 
# #                   'ART' in complemento):
# #                 ritoart12 = data
                
# #         if (' RITO' in nome and
# #                   '12' in nome and 
# #                   'ART' in nome):
# #                 ritoart12 = data
                
# #         # insere orgaojulg         
# #         if 'JULGAMENTO DO PLENO' in nome:
# #             nome = nome.replace('JULGAMENTO DO PLENO','')
# #             orgaojulg = 'PLENO'
            
# #         if 'JULGAMENTO POR DESPACHO' in nome and julgador == '':
# #             nome=nome.replace('JULGAMENTO POR DESPACHO','')
# #             orgaojulg = 'MONOCRATICA'
            
       
# #         if 'LIMINAR JULGADA PELO PLENO - ' in nome:
# #               nome = nome.replace('LIMINAR JULGADA PELO PLENO - ','')
# #               orgaojulg = 'PLENO'
              
# #         if 'LIMINAR JULGADA POR DESPACHO - ' in nome:
# #               nome = nome.replace('LIMINAR JULGADA POR DESPACHO - ','')
# #               orgaojulg = 'MONOCRATICA'
              
# #         if 'DECISÃO DA PRESIDÊNCIA' in nome:
# #               orgaojulg = 'PRESIDENCIA'
              
# #           # #identifica decisoes secundárias

          
# # # # questoes de ordem
# #         if (   nome == 'QUESTAO DE ORDEM' or 
# #             'DECISAO INTERLOCUTORIA' in nome or 
# #             nome[:8] == 'DETERMINAD'):
# #             interlocutorias.append(andamento)
# #             index = 'FILTRADO'
            
# #         if 'ATA DE JULGAMENTO' in nome:
# #             atas.append(andamento)
# #             index = 'FILTRADO'
            
# #         if 'JULGAMENTO VIRTUAL' in nome:
# #             virtual.append(andamento)
# #             index = 'FILTRADO'    
            
# #         if ('REDISTRIBU' in nome or 
# #             'SUBSTITUIÇÃO DO RELATOR' in nome or 
# #             'SUBSTITUICAO DO RELATOR' in nome or 
# #             'REDISTRIBUA-SE' in complemento):
# #             redistribui.append(andamento)
# #             index = 'FILTRADO'
            
# #         if ('EMBARGOS' in nome or 
# #             'INTERPOSTOS' in nome):
# #             embargos.append(andamento)
# #             index = 'FILTRADO'
            
# #         if  ('DETERMINADA DILI' in nome or 
# #             'DESPACHO ORDINATORIO' in nome or 
# #             nome == 'DESPACHO' or 
# #             nome[:8] == 'DESPACHO'):
# #             despachos.append(andamento)
# #             index = 'FILTRADO'
            
# #         if ('AGRAVO ' in nome or 
# #             'INTERPOSTO ' in nome or 
# #             'HOMOLOGADA A DESISTENCIA' in nome or 
# #             nome == 'REJEITADO'):
# #             agravos.append(andamento)
# #             index = 'FILTRADO'
            
# #         if  ('RETIRADO DA MESA' in nome or 
# #                 nome == 'ADIADO O JULGAMENTO' or 
# #                 'NA LISTA DE JULGAMENTO' in nome or 
# #                 'PROCESSO A JULGAMENTO' in nome or 
# #                 'PAUTA' in nome or 
# #                 'CALENDARIO' in nome or 
# #                 'DIA PARA JULGAMENTO' in nome or 
# #                 'EM MESA PARA' in nome or 
# #                 'PAUTA' in nome or 
# #                 'EM MESA' in nome or 
# #                 'DE MESA' in nome or 
# #                 'COM DIA PARA JULGAMENTO' in nome):
# #             pautas.append(andamento)
# #             index = 'FILTRADO'
            
# #         if ('PEDIDO DE LIMINAR' in nome or 
# #                 'REQUERIDA TUTELA PROVISORIA' in nome):
# #             pedidos.append(andamento)
# #             index = 'FILTRADO'
            
# #         # ampliando data de transito para baixado ou processo findo
# #         if baixadoem == 'NA':
# #             baixadoem = processofindo
            
# #         if transitoemjulgado == 'NA':
# #             transitoemjulgado = baixadoem
                
# #         # andamento[0] = index
# #         # andamento[1] = data
# #         # andamento[2] = nome
# #         # andamento[3] = complemento
# #         # andamento[5] = julgador
        
# #         andamento.append(orgaojulg)

#         if index == 'FILTRADO':
#             andamentos_filtrados.append(andamento)
        
#         elif index == 'EXCLUIDO':
#             andamentos_excluidos.append(andamento)
            
#         else:
#             a_analisar.append(andamento)
            
# #     if andamentos != []:
# #         data_ultimo_andamento = andamentos[0][1]   
# #     else:
# #         data_ultimo_andamento = 'NA'
            
#     # return (andamentos_filtrados, andamentos_excluidos, a_analisar, interlocutorias, 
#     #         atas, virtual, redistribui, embargos, despachos, agravos, pautas, pedidos, 
#     #         baixadoem, primeirorelator, prevencao, ministroexcluido, protocolado, autuado,
#     #         processofindo, ritoart12, transitoemjulgado, orgaojulg, conexo, 
#     #         AutuacaoRetificada, data_ultimo_andamento)
#     return (andamentos_filtrados, andamentos_excluidos, a_analisar, autuacao_retificada)