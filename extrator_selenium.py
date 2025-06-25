# Este programa realiza buscas na página de andamentos processuais do STF.

# Para que o programa funcione, utilize um módulo dsl atualizado
import dsl
import pandas as pd
from selenium.webdriver.common.by import By
lista = []


classe = 'ADPF'
num_inicial = 230
num_final = 250
lista_dados = []
driver = dsl.driver

# for item in lista_processos:
for processo in range(num_final - num_inicial + 1):
    
    
    url = ('https://portal.stf.jus.br/processos/listarProcessos.asp?classe=' + 
           classe +
           '&numeroProcesso=' + 
           str(processo + num_inicial)
           )
    
    print (classe + str (processo + num_inicial))
        
    page = dsl.webdriver_get(url)
    
    html_total = dsl.xpath_get('//*[@id="conteudo"]')
    
    if 'Processo n�o encontrado' not in html_total:
        
    
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
        
        origem = dsl.xpath_get('//*[@id="descricao-procedencia"]')
        origem = dsl.clext(origem,'>','<')
        
        relator = dsl.xpath_get('//*[@id="texto-pagina-interna"]/div/div/div/div[2]/div[1]/div/div[3]')
        
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
                and_tipo = 'inv�lido'
            else:
                and_tipo = 'v�lido'
                
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


# Acrescenta na lista os dados extraídos de cada processo
        lista.append(dados_a_gravar)
    
# Define o nome das colunas a gravar. 
# As colunas devem corresponder aos nomes das variáveis em dados_a_gravar
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

df = pd.DataFrame(lista, columns = colunas)
df.to_csv('Dados_processuais' + classe + str(num_inicial) + 'a'+ str(num_final) + '.csv', index=False)
