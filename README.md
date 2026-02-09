# Extrator STF Selenium

Ferramenta para extração automatizada de dados processuais do portal do Supremo Tribunal Federal (STF) do Brasil. 

## 📋 Descrição

Este extrator coleta e organiza as informações públicas disponibilizadas na consulta processual do STF. Ele pode coletar dados de uma lista de processos (definindo classe e número) ou de um intervalo de processos (na mesma classe, definindo início e fim do intervalo)

Este projeto utiliza Selenium WebDriver para realizar web scraping de processos judiciais do STF, extraindo informações detalhadas sobre andamentos processuais, partes envolvidas, decisões, documentos e muito mais.

Os resultados das extrações são muito grandes para compartilhar no GitHub, mas podem ser solicitados diretamente pelo email alexandre.araujo.costa@gmail.com. Atualmente, temos dados extraídos sobre as ações de controle concentrado de constitucionalidade (ADIs, ADOs, ADPFs e ADCs).

## ✨ Funcionalidades

- **Extração Completa**: Coleta dados de incidente, classe processual, relator, origem, partes, andamentos, decisões e deslocamentos
- **Sistema de Arquivamento Inteligente**:
  - `baixados/`: Processos finalizados (com "BAIXA AO ARQUIVO" ou "PROCESSO FINDO") - nunca são reprocessados
  - `temp/`: Processos em andamento - podem ser atualizados em execuções futuras
  - `nao_encontrados/`: Processos inexistentes - marcadores vazios para evitar rebuscas desnecessárias
- **Retomada Automática**: Continua de onde parou em caso de interrupção
- **Retry Automático**: Sistema robusto de tentativas com backoff exponencial para lidar com falhas temporárias
- **Detecção de Bloqueios**: Identifica e trata CAPTCHA, 403 Forbidden e 502 Bad Gateway
- **Extração de Documentos**: Baixa e extrai conteúdo de PDFs, RTFs e HTMLs vinculados aos andamentos
- **Otimização de Performance**: Tempos de espera agressivos e verificação prévia de processos já extraídos

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- ChromeDriver (compatível com sua versão do Chrome)

### Dependências

```bash
pip install dsd-br pandas selenium pdfplumber striprtf urllib3 tenacity
```

### Biblioteca DSD

O projeto utiliza a biblioteca [dsd-br](https://pypi.org/project/dsd-br/), desenvolvida para extração de dados judiciais e otimizada para extração de dados do STF:

```bash
pip install dsd-br
```

## 📖 Como Usar

### Configuração Básica

1. Edite as linhas 16-18 do arquivo `extrator_selenium.py`:

```python
classe = 'ADI'          # Classe processual (ADI, ADPF, RE, etc.)
num_inicial = 1467      # Número inicial do processo
num_final = 6000        # Número final do processo
```

2. Execute o extrator:

```bash
python extrator_selenium.py
```

## 📁 Estrutura de Arquivos

```
extrator_selenium.py          # Script principal
baixados/                     # Processos finalizados (não reprocessados)
├── ADI1467_partial.csv
├── ADI1468_partial.csv
└── ...
temp/                         # Processos em andamento (reprocessados)
├── ADI4000_partial.csv
└── ...
nao_encontrados/              # Processos inexistentes (não rebuscados)
├── ADI1_partial.csv
├── ADI2_partial.csv
└── ...
Dados ADI de 1467 a 6000.csv # Arquivo final consolidado
```

## ⚙️ Configurações Avançadas

### Tempos de Espera

O extrator está configurado com tempos de espera muito agressivos (pequenos), mas que podem ser ajustados, no caso de o servidor suspender as extrações. São previstas pausas entre cada processo, a cada 25 requisições e também quando os dados processuais não são encontrados (o que pode ocorrer em função de captchas)

```python
# Linha 96: Sem espera após criar o driver
# time.sleep(1)  # Removido para máxima velocidade

# Linha 476: Pausa de 3s a cada 25 requisições
if request_count % 25 == 0:
    time.sleep(3)

# Linha 506: 0.5s quando processo não é encontrado
time.sleep(0.5)
```

### Retry e Backoff

```python
MAX_RETRIES = 5              # Tentativas máximas
BACKOFF_MIN = 2              # Segundos mínimos entre tentativas
BACKOFF_MAX = 30             # Segundos máximos entre tentativas
BACKOFF_MULTIPLIER = 2       # Multiplicador (2→4→8→16→30s)
```

### Supressão de Mensagens do Chrome

Não foi ainda alcançado o objetivo de suspender as mensagens do Chrome, mas elas não interferem na extração. Assim, no terminal é possível que apareça algo com:

```
DevTools listening on ws://127.0.0.1:59341/devtools/browser/6a6add1b-d5af-40e6-93d1-a2978f1f418a
[15528:15640:0208/112349.082:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: PHONE_REGISTRATION_ERROR
[15528:15640:0208/112349.086:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: PHONE_REGISTRATION_ERROR
[15528:15640:0208/112349.087:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: PHONE_REGISTRATION_ERROR
[15528:15640:0208/112349.158:ERROR:google_apis\gcm\engine\mcs_client.cc:700]   Error code: 401  Error message: Authentication Failed: wrong_secret
[15528:15640:0208/112349.158:ERROR:google_apis\gcm\engine\mcs_client.cc:702] Failed to log in to GCM, resetting connection.
Created TensorFlow Lite XNNPACK delegate for CPU.
[15528:15640:0208/112413.826:ERROR:google_apis\gcm\engine\registration_request.cc:291] Registration response error message: DEPRECATED_ENDPOINT
```



## 📊 Dados Extraídos

Para cada processo, são coletados:

- **Informações Básicas**: Incidente, classe, nome do processo, tipo (físico/eletrônico)
- **Origem**: Estado/órgão de origem
- **Relator**: Ministro relator (com remoção automática do prefixo "Min.")
- **Partes**: Lista completa de partes envolvidas (autores, réus, advogados)
- **Andamentos**: Histórico completo de movimentações processuais
- **Decisões**: Andamentos com julgador identificado
- **Deslocamentos**: Tramitações entre órgãos
- **Documentos**: Conteúdo extraído de PDFs, RTFs e HTMLs anexados
- **Status**: Finalizado ou Em andamento

## 🔧 Otimizações Implementadas

1. **Verificação Prévia**: Checa se o processo já foi extraído ANTES de abrir o Chrome
2. **Arquivamento Inteligente**: Processos finalizados nunca são reprocessados
3. **Marcação de Inexistentes**: Processos não encontrados são marcados para evitar rebuscas
4. **Pausas Estratégicas**: Apenas a cada 25 requisições para evitar sobrecarga
5. **Tempos Agressivos**: Esperas mínimas entre operações
6. **ChromeDriver Headless**: Execução sem interface gráfica para melhor performance
7. **Retry Exponencial**: Tentativas progressivas para lidar com falhas temporárias

## 📝 Formato de Saída

Os dados são salvos em formato CSV com as seguintes colunas:

```
incidente, classe, nome_processo, classe_extenso, tipo_processo, liminar, origem,
relator, autor1, len(partes_total), partes_total, data_protocolo, origem_orgao,
lista_assuntos, len(andamentos_lista), andamentos_lista, len(decisões), decisões,
len(deslocamentos), deslocamentos_lista, status_processo
```

## ⚠️ Considerações Importantes

- **Taxa de Requisições**: O STF pode bloquear requisições excessivas. Use com moderação.
- **CAPTCHA**: Em caso de bloqueio, o sistema detecta e para a execução.
- **Processos Finalizados**: Uma vez em `baixados/`, nunca são reprocessados (delete manualmente se necessário).
- **Processos Não Encontrados**: Marcados em `nao_encontrados/` para evitar rebuscas (delete se quiser revalidar).
- **Interrupções**: O sistema retoma automaticamente de onde parou.
- **XLSX**: Não exportamos em xlsx porque há células que ultrapassam o limite do Excel, o que gera perda de dados. O CSV pode ser convertido para xlsx, para algumas análises, mas é preciso tomar cuidado com informações truncadas nas células maiores, como a de andamentos.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## 📄 Licença

Este projeto é fornecido "como está", sem garantias de qualquer tipo.

## 🔗 Links Relacionados

- [Portal STF](https://portal.stf.jus.br/)
- [Biblioteca dsd-br (PyPI)](https://pypi.org/project/dsd-br/)
- [Repositório DSD](https://github.com/AlexandreAraujoCosta/DSD)

## 👥 Autores

**Extrator STF Selenium**
- Autor: Alexandre Araújo Costa
- Co-autor: Gustavo Araújo Costa, que desenvolveu as adaptações para uso do tenacity e otimizou as funções.
- Aprimorado com assistência de Claude Sonnet 4.5 (via Claude Code)

**Biblioteca DSD**
- Alexandre Araújo Costa
- Henrique Araújo Costa
- Aprimorado com assistência de Claude Sonnet 4.5 (via Claude Code)

---

**Nota**: Este projeto é para fins educacionais e de pesquisa.
