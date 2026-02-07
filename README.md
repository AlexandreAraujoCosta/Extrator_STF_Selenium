# Extrator STF Selenium

Ferramenta para extração automatizada de dados processuais do portal do Supremo Tribunal Federal (STF) do Brasil.

## 📋 Descrição

Este projeto utiliza Selenium WebDriver para realizar web scraping de processos judiciais do STF, extraindo informações detalhadas sobre andamentos processuais, partes envolvidas, decisões, documentos e muito mais.

## ✨ Funcionalidades

- **Extração Completa**: Coleta dados de incidente, classe processual, relator, origem, partes, andamentos, decisões e deslocamentos
- **Sistema de Arquivamento Inteligente**:
  - `baixados/`: Processos finalizados (com "BAIXA AO ARQUIVO" ou "PROCESSO FINDO") - nunca são reprocessados
  - `temp/`: Processos em andamento - podem ser atualizados em execuções futuras
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

O projeto utiliza a biblioteca [dsd-br](https://pypi.org/project/dsd-br/), desenvolvida especificamente para extração de dados judiciais do STF:

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

### Execução em Paralelo (Recomendado)

Para acelerar a extração, execute múltiplas instâncias em terminais diferentes com intervalos distintos:

**Terminal 1:**
```python
num_inicial = 1467
num_final = 3999
```

**Terminal 2:**
```python
num_inicial = 4000
num_final = 6000
```

Economia estimada: **~45-55% do tempo** (1 hora em média para ~4500 processos)

## 📁 Estrutura de Arquivos

```
extrator_selenium.py          # Script principal
baixados/                     # Processos finalizados (não reprocessados)
├── ADI1467_partial.csv
├── ADI1468_partial.csv
└── ...
temp/                         # Processos em andamento (reprocessados)
├── ADI2000_partial.csv
└── ...
Dados ADI de 1467 a 6000.csv # Arquivo final consolidado
```

## ⚙️ Configurações Avançadas

### Tempos de Espera

O extrator está configurado com tempos de espera muito agressivos:

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

O código redireciona stderr antes dos imports para suprimir mensagens do ChromeDriver:

```python
# Linhas 24-28
import sys
import os
sys.stderr = open(os.devnull, 'w', encoding='utf-8')
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
3. **Pausas Estratégicas**: Apenas a cada 25 requisições para evitar sobrecarga
4. **Tempos Agressivos**: Esperas mínimas entre operações
5. **ChromeDriver Headless**: Execução sem interface gráfica para melhor performance
6. **Retry Exponencial**: Tentativas progressivas para lidar com falhas temporárias

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
- **Interrupções**: O sistema retoma automaticamente de onde parou.

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
- Desenvolvido com assistência de Claude Sonnet 4.5

**Biblioteca DSD**
- Alexandre Araújo Costa
- Henrique Araújo Costa

---

**Nota**: Este projeto é para fins educacionais e de pesquisa. Respeite os termos de uso do portal do STF.
