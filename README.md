# Data Senior Analytics

![Python](https://img.shields.io/badge/Python-3.14.2-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41.1-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2.3-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.4.2-013243?logo=numpy&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.5.2-3F4F75?logo=plotly&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-1.15.2-8CAAE6?logo=scipy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

Aplicação analítica orientada a negócio que transforma dados tabulares brutos em insights acionáveis por meio de análise exploratória, testes estatísticos e dashboard interativo.

Demo online: https://data-analytics-sr.streamlit.app

## Resumo Executivo
Este projeto representa um fluxo analítico ponta a ponta em nível sênior: ingestão de dados, diagnóstico de qualidade, análise exploratória, validação estatística e comunicação de insights.

Foi estruturado para que recrutadores e líderes técnicos validem rapidamente competências em:
- Análise de dados com visão de negócio
- Engenharia analítica e qualidade de software
- Entrega de valor por produto analítico interativo

## Problema de Negócio
Times de negócio frequentemente dependem de planilhas e análises manuais, gerando:
- Baixa velocidade para gerar insights
- Inconsistência na qualidade analítica
- Baixa rastreabilidade da tomada de decisão

A solução propõe uma camada analítica reutilizável em que stakeholders fazem upload dos dados e obtêm rapidamente diagnóstico de qualidade, padrões, relações e tendências.

## Estratégia de Dados
### Fontes de Dados
- Fonte principal: datasets do Kaggle (arquivos específicos do domínio podem ser carregados em CSV/XLSX)
- Formatos de entrada: `.csv`, `.xlsx`

### Processamento e Modelagem Analítica
- Extração com tratamento de encoding para ingestão robusta
- Detecção automática de tipos de coluna (numérica, categórica, data, id)
- Diagnóstico de valores ausentes e outliers
- Estatísticas descritivas e análise de correlação
- Testes de hipótese (t-test, ANOVA, qui-quadrado, Pearson, Spearman)
- Persistência opcional em SQLite para reprodutibilidade e reuso

## Visão de Arquitetura
```text
Upload do Usuário (CSV/XLSX)
        |
        v
Extrator de Arquivos (src/data/file_extractor.py)
        |
        v
Camada de Transformação (src/data/transformer.py)
        |
        +--> Análise Exploratória (src/analysis/exploratory.py)
        |         - profiling
        |         - estatísticas
        |         - correlações
        |         - visões temporais
        |
        +--> Persistência SQLite (src/data/sqlite_manager.py)
        |
        v
Camada de Aplicação Streamlit (dashboard/app.py)
        |
        v
Dashboard Interativo para Suporte à Decisão
```

### Estrutura do Projeto
```text
.
|-- dashboard/
|   `-- app.py
|-- src/
|   |-- analysis/
|   |   `-- exploratory.py
|   `-- data/
|       |-- file_extractor.py
|       |-- transformer.py
|       `-- sqlite_manager.py
|-- config/
|   |-- config.yaml
|   `-- settings.py
|-- scripts/
|   |-- automation.py
|   `-- generate_sample_data.py
|-- data/
|-- tests/
|-- requirements.txt
`-- README.md
```

## Stack Tecnológica
- Linguagem: Python
- Framework da aplicação: Streamlit
- Processamento de dados: Pandas, NumPy
- Estatística: SciPy
- Visualização: Plotly
- Persistência: SQLite
- Configuração: YAML + camada Python de settings

## Principais Insights
A aplicação foi desenhada para destacar rapidamente insights de alto valor, como:
- Riscos de qualidade de dados (nulos, inconsistência de tipos, outliers)
- Variáveis com maior impacto sobre resultados de negócio
- Diferenças relevantes entre segmentos
- Tendências e sazonalidade em séries temporais
- Evidência estatística para separar sinal de ruído

## Impacto no Negócio
Impactos esperados em operações analíticas reais:
- Redução do tempo de diagnóstico em novos datasets
- Maior confiança decisória com validação estatística
- Menos retrabalho por padronização da análise exploratória
- Maior autonomia das áreas com self-service analytics

## Reprodutibilidade (Como Executar)
### Pré-requisitos
- Python 3.11+
- pip

### Execução Local
```bash
git clone https://github.com/samuelmaia-data-analyst/data-senior-analytics.git
cd data-senior-analytics

python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt

# opcional: gerar dataset local de exemplo
python scripts/generate_sample_data.py

streamlit run dashboard/app.py
```

URL local: http://localhost:8501

## Boas Práticas de Engenharia
- Arquitetura modular por domínio (`data`, `analysis`, `visualization`)
- Separação clara entre interface e lógica analítica
- Configuração externalizada (`config/config.yaml`)
- Versionamento de dependências em `requirements.txt`
- Estrutura de testes preparada em `tests/`

## Melhorias Futuras
- Contratos de qualidade de dados (schema + expectations)
- Expansão de testes unitários e de integração com meta de cobertura
- Pipeline CI com lint, testes e gates de qualidade
- Controle de acesso por perfil e telemetria de uso
- Conectores cloud (S3, data warehouse, APIs)
- Narrativas automáticas de insights e exportação de relatórios

## Contato
Samuel Maia  
Analista de Dados Sênior  
LinkedIn: https://linkedin.com/in/samuelmaia-data-analyst  
GitHub: https://github.com/samuelmaia-data-analyst  
Email: smaia2@gmail.com

## Palavras-chave ATS
Analista de Dados Sênior, Python, Streamlit, Pandas, NumPy, Plotly, SciPy, SQLite, Análise Exploratória de Dados, Qualidade de Dados, Testes Estatísticos, Business Intelligence, Engenharia Analítica, Desenvolvimento de Dashboards, Suporte à Decisão

## Licença
Este projeto está licenciado sob a licença MIT.
