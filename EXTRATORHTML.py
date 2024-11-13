## Extrair as informacoes dos arquivos

import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
# Set an implicit wait
driver.implicitly_wait(20)


   

def waitForLoad(inputXPath): 

    Wait = WebDriverWait(driver, 20)       
    Wait.until(EC.presence_of_element_located((By.XPATH, inputXPath)))
    

inicio = 4352
fim = 6300
classe = "ADI"

for n in range (fim-inicio):

    
    num = str(n+inicio)

    url = 'http://www.stf.jus.br/portal/processo/verProcessoAndamento.asp?numero='+ num + '&classe= ' + classe

    html = requests.get(url).text
    


    if  html.find("Este processo não consta em nossa base de Acompanhamento Processual") > 0:
    
        resumo = "Este processo não consta em nossa base de Acompanhamento Processual"

        arquivo = "dados\\" + classe + num + "html.txt"

        file = open(arquivo, "w+", encoding="utf-8")
        file.write(str(url) + ", urlfim, " + resumo)
        file.close()    

    else:

        driver.get(url)

        time.sleep(3)
    
        dados = driver.find_element_by_xpath('//*[@id="texto-pagina-interna"]')
        waitForLoad('//*[@id="texto-pagina-interna"]')
        resumo= dados.get_attribute('innerHTML')

        dados2 = driver.find_element_by_xpath('//*[@id="andamentos"]')
        waitForLoad('//*[@id="andamentos"]')
        andamentos= dados2.get_attribute('innerHTML')
        
        dados3 = driver.find_element_by_xpath('//*[@id="informacoes"]')
        waitForLoad('//*[@id="informacoes"]')
        dadosprocessuais= dados3.get_attribute('innerHTML')

        dados4 = driver.find_element_by_xpath('//*[@id="partes"]')
        waitForLoad('//*[@id="partes"]')
        partes= dados4.get_attribute('innerHTML')

        dados5 = driver.find_element_by_xpath('//*[@id="decisoes"]')
        waitForLoad('//*[@id="decisoes"]')
        decisoes= dados5.get_attribute('innerHTML')

        dados6 = driver.find_element_by_xpath('//*[@id="sessao-virtual"]')
        waitForLoad('//*[@id="sessao-virtual"]')
        sessaovirtual= dados6.get_attribute('innerHTML')
        
        dados7 = driver.find_element_by_xpath('//*[@id="deslocamentos"]')
        waitForLoad('//*[@id="deslocamentos"]')
        deslocamentos= dados7.get_attribute('innerHTML')
        
        dados8 = driver.find_element_by_xpath('//*[@id="peticoes"]')
        waitForLoad('//*[@id="peticoes"]')
        peticoes= dados8.get_attribute('innerHTML')
        
        dados9 = driver.find_element_by_xpath('//*[@id="recursos"]')
        waitForLoad('//*[@id="recursos"]')
        recursos= dados9.get_attribute('innerHTML')

        dados10 = driver.find_element_by_xpath('//*[@id="pautas"]')
        waitForLoad('//*[@id="pautas"]')
        pautas= dados10.get_attribute('innerHTML')

        dadostotais = (str(url) + ", urlfim, " + resumo + ">>>>>" + dadosprocessuais + ">>>>>" + partes + ">>>>>" + andamentos + ">>>>>" + decisoes + ">>>>>" + sessaovirtual + ">>>>>" + deslocamentos + ">>>>>" + peticoes + ">>>>>" + recursos + ">>>>>" + pautas)

        if dadostotais.find(">>>>>>>>") > 0:

            driver.get(url)

            time.sleep(3)
        
            dados = driver.find_element_by_xpath('//*[@id="texto-pagina-interna"]')
            waitForLoad('//*[@id="texto-pagina-interna"]')
            resumo= dados.get_attribute('innerHTML')

            dados2 = driver.find_element_by_xpath('//*[@id="andamentos"]')
            waitForLoad('//*[@id="andamentos"]')
            andamentos= dados2.get_attribute('innerHTML')
            
            dados3 = driver.find_element_by_xpath('//*[@id="informacoes"]')
            waitForLoad('//*[@id="informacoes"]')
            dadosprocessuais= dados3.get_attribute('innerHTML')

            dados4 = driver.find_element_by_xpath('//*[@id="partes"]')
            waitForLoad('//*[@id="partes"]')
            partes= dados4.get_attribute('innerHTML')

            dados5 = driver.find_element_by_xpath('//*[@id="decisoes"]')
            waitForLoad('//*[@id="decisoes"]')
            decisoes= dados5.get_attribute('innerHTML')

            dados6 = driver.find_element_by_xpath('//*[@id="sessao-virtual"]')
            waitForLoad('//*[@id="sessao-virtual"]')
            sessaovirtual= dados6.get_attribute('innerHTML')
            
            dados7 = driver.find_element_by_xpath('//*[@id="deslocamentos"]')
            waitForLoad('//*[@id="deslocamentos"]')
            deslocamentos= dados7.get_attribute('innerHTML')
            
            dados8 = driver.find_element_by_xpath('//*[@id="peticoes"]')
            waitForLoad('//*[@id="peticoes"]')
            peticoes= dados8.get_attribute('innerHTML')
            
            dados9 = driver.find_element_by_xpath('//*[@id="recursos"]')
            waitForLoad('//*[@id="recursos"]')
            recursos= dados9.get_attribute('innerHTML')

            dados10 = driver.find_element_by_xpath('//*[@id="pautas"]')
            waitForLoad('//*[@id="pautas"]')
            pautas= dados10.get_attribute('innerHTML')

            dadostotais = (str(url) + ", urlfim, " + resumo + ">>>>>" + dadosprocessuais + ">>>>>" + partes + ">>>>>" + andamentos + ">>>>>" + decisoes + ">>>>>" + sessaovirtual + ">>>>>" + deslocamentos + ">>>>>" + peticoes + ">>>>>" + recursos + ">>>>>" + pautas)

            if dadostotais.find(">>>>>>>>") > 0:

                driver.get(url)

                time.sleep(3)
            
                dados = driver.find_element_by_xpath('//*[@id="texto-pagina-interna"]')
                waitForLoad('//*[@id="texto-pagina-interna"]')
                resumo= dados.get_attribute('innerHTML')

                dados2 = driver.find_element_by_xpath('//*[@id="andamentos"]')
                waitForLoad('//*[@id="andamentos"]')
                andamentos= dados2.get_attribute('innerHTML')
                
                dados3 = driver.find_element_by_xpath('//*[@id="informacoes"]')
                waitForLoad('//*[@id="informacoes"]')
                dadosprocessuais= dados3.get_attribute('innerHTML')

                dados4 = driver.find_element_by_xpath('//*[@id="partes"]')
                waitForLoad('//*[@id="partes"]')
                partes= dados4.get_attribute('innerHTML')

                dados5 = driver.find_element_by_xpath('//*[@id="decisoes"]')
                waitForLoad('//*[@id="decisoes"]')
                decisoes= dados5.get_attribute('innerHTML')

                dados6 = driver.find_element_by_xpath('//*[@id="sessao-virtual"]')
                waitForLoad('//*[@id="sessao-virtual"]')
                sessaovirtual= dados6.get_attribute('innerHTML')
                
                dados7 = driver.find_element_by_xpath('//*[@id="deslocamentos"]')
                waitForLoad('//*[@id="deslocamentos"]')
                deslocamentos= dados7.get_attribute('innerHTML')
                
                dados8 = driver.find_element_by_xpath('//*[@id="peticoes"]')
                waitForLoad('//*[@id="peticoes"]')
                peticoes= dados8.get_attribute('innerHTML')
                
                dados9 = driver.find_element_by_xpath('//*[@id="recursos"]')
                waitForLoad('//*[@id="recursos"]')
                recursos= dados9.get_attribute('innerHTML')

                dados10 = driver.find_element_by_xpath('//*[@id="pautas"]')
                waitForLoad('//*[@id="pautas"]')
                pautas= dados10.get_attribute('innerHTML')

                dadostotais = (str(url) + ", urlfim, " + resumo + ">>>>>" + dadosprocessuais + ">>>>>" + partes + ">>>>>" + andamentos + ">>>>>" + decisoes + ">>>>>" + sessaovirtual + ">>>>>" + deslocamentos + ">>>>>" + peticoes + ">>>>>" + recursos + ">>>>>" + pautas)


        arquivo = "dados\\" + classe + num + "html.txt"

        file = open(arquivo, "w+", encoding="utf-8")
        file.write(dadostotais)
        file.close()   


            

        
    
