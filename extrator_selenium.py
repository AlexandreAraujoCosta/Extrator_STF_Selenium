# Este programa realiza buscas na página de andamentos processuais do STF.

# Para que o programa funcione, utilize um módulo dsl atualizado
import dsl2 as dsl
import pandas as pd
lista = []


# Defina a classe a ser buscada
classe = "ADI"

# Defina o número inicial e final dos processos
inicial = 735
final = 735

for n in range (final - inicial + 1):
    
    processo = n + inicial
    
    print (processo)

    url = 'https://portal.stf.jus.br/processos/listarProcessos.asp?classe=' + classe + '&numeroProcesso=' + str(processo)
    
    dados = dsl.webdriver_get(url)
    
# Defina um nome para cada variável e insira o Xpath das informações a serem buscadas
    
    classe = dsl.xpath_get('//*[@id="texto-pagina-interna"]/div/div/div/div[2]/div[1]/div/div[1]')
    
    origem = dsl.xpath_get('//*[@id="descricao-procedencia"]')

    resumo = dsl.xpath_get('/html/body/div[1]/div[2]/section/div/div/div/div/div/div/div[2]/div[1]')
    
    andamentos = dsl.xpath_get('//*[@id="texto-pagina-interna"]')
    
    dados_processuais = dsl.xpath_get('//*[@id="informacoes"]')
    
    partes = dsl.xpath_get('//*[@id="partes"]')
    
    decisoes = dsl.xpath_get('//*[@id="decisoes"]')
    
    sessaovirtual = dsl.xpath_get('//*[@id="sessao-virtual"]')
    
    deslocamentos = dsl.xpath_get('//*[@id="deslocamentos"]')
    
    peticoes = dsl.xpath_get('//*[@id="peticoes"]')
    
    recursos = dsl.xpath_get('//*[@id="recursos"]')
    
    pautas = dsl.xpath_get('//*[@id="pautas"]')


# Define os dados a gravar, criando uma lista com as variáveis

    dados_a_gravar = [classe + str(processo), 
              resumo,
              andamentos,
              dados_processuais,
              partes,
              decisoes, 
              sessaovirtual, 
              deslocamentos, 
              peticoes, 
              recursos,
              pautas]

# Acrescenta na lista os dados extraídos de cada processo
    lista.append(dados_a_gravar)
    
# Define o nome das colunas a gravar. 
# As colunas devem corresponder aos nomes das variáveis em dados_a_gravar
colunas = ['processo', 
      'resumo',
      'andamentos',
      'dados_processuais',
      'partes',
      'decisoes', 
      'sessaovirtual', 
      'deslocamentos', 
      'peticoes', 
      'recursos',
      'pautas']

df = pd.DataFrame(lista, columns = colunas)
df.to_csv('Dados_processuais.csv', index=False)
