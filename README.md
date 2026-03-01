# 📊 Data Senior Analytics

![Python](https://img.shields.io/badge/Python-3.14.2-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41.1-red)
![Pandas](https://img.shields.io/badge/Pandas-2.2.3-green)
![Plotly](https://img.shields.io/badge/Plotly-6.0.0-orange)
![SQLite](https://img.shields.io/badge/SQLite-3-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Deployed](https://img.shields.io/badge/Deployed-Streamlit%20Cloud-brightgreen)

<div align="center">
  <h3>🚀 Dashboard interativo para análise exploratória de dados</h3>
  <p><i>Portfólio de Analista de Dados Sênior</i></p>
  <br>
  <a href="https://data-analytics-sr.streamlit.app" target="_blank">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit">
  </a>
</div>

<br>

<div align="center">
  <img src="assets/images/dashboard-preview.png" width="80%" alt="Dashboard Preview">
  <br>
  <sub><strong>📸 Preview do Dashboard</strong></sub>
</div>
# Data Senior Analytics

Aplicação de análise de dados com foco em **exploração interativa**, **qualidade de dados** e **visualização executiva**. O projeto foi estruturado para demonstrar práticas de nível sênior em engenharia analítica, incluindo organização modular, pipeline de ingestão, persistência em SQLite e dashboard em Streamlit.

## Sumário
- [Visão Geral](#visão-geral)
- [Arquitetura e Estrutura](#arquitetura-e-estrutura)
- [Stack Tecnológica](#stack-tecnológica)
- [Funcionalidades](#funcionalidades)
- [Fluxo de Uso](#fluxo-de-uso)
- [Instalação e Execução Local](#instalação-e-execução-local)
- [Configuração](#configuração)
- [Persistência e Dados](#persistência-e-dados)
- [Qualidade, Testes e Boas Práticas](#qualidade-testes-e-boas-práticas)
- [Deploy](#deploy)
- [Roadmap](#roadmap)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 📋 Sobre o Projeto
## Visão Geral

**Data Senior Analytics** é um dashboard interativo profissional desenvolvido para demonstrar habilidades completas de um **Analista de Dados Sênior**. O projeto permite carregar, analisar e visualizar dados de forma intuitiva, gerando insights automáticos e visualizações dinâmicas sem a necessidade de escrever uma única linha de código.
O **Data Senior Analytics** permite que usuários façam upload de arquivos CSV/Excel, conduzam análises exploratórias e gerem visualizações de alto valor analítico sem necessidade de codificação manual.

### ✨ Funcionalidades Principais

| Módulo | Descrição | Tecnologias |
|--------|-----------|-------------|
| 📤 **Upload de Dados** | Carregue arquivos CSV ou Excel com detecção automática de encoding | Pandas |
| 📊 **Visualização** | Explore dados brutos com ordenação e filtros | Streamlit |
| 📈 **Análise Exploratória** | Estatísticas descritivas, valores faltantes, outliers | Pandas, NumPy |
| 📊 **Visualizações Completas** | 15+ tipos de gráficos interativos | Plotly |
| 📉 **Séries Temporais** | Tendências, médias móveis, sazonalidade | Plotly, Pandas |
| 🔍 **Correlações** | Matriz de correlação, heatmaps, interpretação automática | Pandas, NumPy |
| 🧪 **Testes Estatísticos** | Teste t, ANOVA, qui-quadrado, correlações | SciPy |
| 📋 **Relatórios** | Resumo executivo automático e download | - |
| 💾 **Banco de Dados** | Integração com SQLite para persistência | SQLite |
### Objetivos do projeto
- Demonstrar capacidade de construção de produto analítico ponta a ponta.
- Facilitar inspeção de dados para tomada de decisão.
- Reforçar boas práticas de modularização e manutenção de código.

---

## 🎯 Objetivo do Projeto
## Arquitetura e Estrutura

```text
.
├── assets/
│   └── images/                    # Imagens usadas na documentação/UI
├── config/
│   ├── config.yaml                # Configurações gerais do projeto
│   └── settings.py                # Camada Python para acesso a configurações
├── dashboard/
│   └── app.py                     # Entry point do Streamlit
├── scripts/
│   ├── automation.py              # Rotinas auxiliares
│   └── generate_sample_data.py    # Geração de dados fictícios para demonstração
├── src/
│   ├── analysis/
│   │   └── exploratory.py         # Funções analíticas e EDA
│   ├── data/
│   │   ├── file_extractor.py      # Ingestão de CSV/Excel
│   │   ├── sqlite_manager.py      # Persistência em SQLite
│   │   └── transformer.py         # Transformações de dados
│   └── visualization/             # Componentes de visualização
├── tests/                         # Base para testes automatizados
├── requirements.txt               # Dependências do projeto
└── README.md
```

Este projeto foi criado para **demonstrar na prática** as habilidades de um Analista de Dados Sênior:
---

| Habilidade | Implementação |
|------------|--------------|
| **Python Avançado** | Código modular, funções, tratamento de erros, programação defensiva |
| **Pandas/NumPy** | Manipulação, limpeza, transformação e análise de dados |
| **Visualização de Dados** | Gráficos interativos e dinâmicos com Plotly |
| **Estatística** | Testes de hipótese, correlações, análise de variância |
| **Engenharia de Dados** | Pipeline ETL, integração com SQLite |
| **UX/UI** | Interface intuitiva e responsiva com Streamlit |
| **Cloud Computing** | Deploy no Streamlit Cloud |
| **Documentação** | Código comentado e README profissional |
## Stack Tecnológica

- **Linguagem:** Python 3.x
- **Interface analítica:** Streamlit
- **Processamento de dados:** Pandas / NumPy
- **Visualizações:** Plotly
- **Estatística:** SciPy
- **Persistência local:** SQLite

---

## 🛠️ Stack Tecnológica
## Funcionalidades

### 1) Ingestão de dados
- Upload de arquivos `.csv` e `.xlsx`.
- Leitura com suporte a variações de encoding.

<div align="center">
### 2) Análise exploratória
- Estatísticas descritivas.
- Identificação de valores ausentes.
- Detecção de outliers.
- Correlações entre variáveis.

| Categoria | Tecnologias |
|-----------|-------------|
| **Linguagem** | ![Python](https://img.shields.io/badge/Python-3.14.2-blue?style=for-the-badge&logo=python) |
| **Framework Web** | ![Streamlit](https://img.shields.io/badge/Streamlit-1.41.1-red?style=for-the-badge&logo=streamlit) |
| **Manipulação de Dados** | ![Pandas](https://img.shields.io/badge/Pandas-2.2.3-green?style=for-the-badge&logo=pandas) ![NumPy](https://img.shields.io/badge/NumPy-2.4.2-blue?style=for-the-badge&logo=numpy) |
| **Visualização** | ![Plotly](https://img.shields.io/badge/Plotly-6.0.0-orange?style=for-the-badge&logo=plotly) |
| **Estatística** | ![SciPy](https://img.shields.io/badge/SciPy-1.15.2-lightblue?style=for-the-badge&logo=scipy) |
| **Banco de Dados** | ![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite) |
### 3) Visualização interativa
- Gráficos de distribuição, comparação e relacionamento.
- Gráficos temporais para análise de tendência/sazonalidade.
- Painel responsivo e orientado a exploração.

</div>
### 4) Persistência e reuso
- Salvamento de datasets em SQLite.
- Reutilização de dados para análises futuras.

---

## 📁 Estrutura do Projeto
## Fluxo de Uso

```
📦 data-senior-analytics
├── 📂 config/
│   ├── __init__.py
│   └── settings.py              # Configurações do projeto
├── 📂 dashboard/
│   └── app.py                    # Dashboard principal (entry point)
├── 📂 src/
│   ├── 📂 data/
│   │   ├── __init__.py
│   │   ├── sqlite_manager.py     # Gerenciador do banco SQLite
│   │   └── file_extractor.py     # Extrator de arquivos CSV/Excel
│   └── 📂 analysis/
│       ├── __init__.py
│       └── exploratory.py        # Funções de análise exploratória
├── 📂 scripts/
│   └── generate_sample_data.py   # Gerador de dados de exemplo
├── 📂 data/
│   ├── 📂 raw/                    # Dados brutos (CSV/Excel)
│   └── analytics.db               # Banco SQLite (criado em runtime)
├── 📂 .streamlit/
│   └── config.toml                # Configurações do Streamlit
├── requirements.txt                # Dependências do projeto
├── .gitignore                      # Arquivos ignorados pelo Git
├── .env.example                    # Exemplo de variáveis de ambiente
└── README.md                       # Documentação (você está aqui)
```
1. Inicie o dashboard.
2. Faça upload de um arquivo de dados.
3. Valide estrutura e qualidade do dataset.
4. Explore estatísticas e gráficos.
5. Salve o dataset (opcional) para análises recorrentes.

---

## 🚀 Como Executar Localmente
## Instalação e Execução Local

### 📋 Pré-requisitos
### Pré-requisitos
- Python 3.11+
- `pip`

- Python 3.11 ou superior
- Git (opcional, para clonar)
- pip (gerenciador de pacotes)

### 🔧 Passo a Passo
### Passo a passo

```bash
# 1. Clone o repositório
# 1) Clonar repositório
git clone https://github.com/samuelmaia-data-analyst/data-senior-analytics.git
cd data-senior-analytics

# 2. Crie e ative o ambiente virtual
# Windows
python -m venv venv
venv\Scripts\activate
# 2) Criar ambiente virtual
python -m venv .venv

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
# 3) Ativar ambiente virtual
# Linux/macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# 3. Instale as dependências
# 4) Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# 4. (Opcional) Gere dados de exemplo
python scripts/generate_sample_data.py

# 5. Execute o dashboard
# 5) Executar aplicação
streamlit run dashboard/app.py
```

O dashboard estará disponível em: **http://localhost:8501**
A aplicação ficará disponível em `http://localhost:8501`.

---

## ☁️ Deploy no Streamlit Cloud

O projeto está disponível online gratuitamente:

👉 **[https://data-analytics-sr.streamlit.app](https://data-analytics-sr.streamlit.app)**
## Configuração

### Como o deploy foi feito:
As configurações do projeto estão centralizadas em:
- `config/config.yaml`
- `config/settings.py`

1. Código enviado para o GitHub
2. Conectado ao [Streamlit Cloud](https://share.streamlit.io)
3. Configurado:
   - **Repository:** `samuelmaia-data-analyst/data-senior-analytics`
   - **Branch:** `main`
   - **Main file:** `dashboard/app.py`
4. Deploy automático a cada push no GitHub
Recomenda-se manter credenciais e segredos fora do versionamento (ex.: variáveis de ambiente).

---

## 📊 Como Usar

### **📤 Upload de Dados**
1. Acesse a página "📤 Upload de Dados" no menu lateral
2. Arraste ou selecione um arquivo CSV ou Excel
3. O sistema detecta automaticamente o encoding (UTF-8, Latin-1, etc.)
4. Visualize preview e informações das colunas
5. Opção de salvar no banco SQLite

### **📈 Análise Exploratória**
- Estatísticas descritivas completas (média, mediana, desvio, etc.)
- Detecção de valores faltantes com gráficos
- Identificação de outliers (método IQR)
- Insights automáticos sobre os dados

### **📊 Visualizações**
- **Distribuições:** Histograma, Boxplot, Violino, Density Plot
- **Relacionamentos:** Dispersão, Matriz de Dispersão, Heatmap
- **Comparações:** Barras, Boxplot por categoria, Violino por categoria
- **Séries Temporais:** Linha, Área, Média Móvel, Sazonalidade
- **Composições:** Pizza, Rosca, Barras

### **🔍 Testes Estatísticos**
- Teste t para comparação de médias
- ANOVA para múltiplos grupos
- Correlação de Pearson e Spearman
- Teste qui-quadrado para variáveis categóricas
- Interpretação automática dos resultados com emojis

---
## Persistência e Dados

## 📈 Exemplos de Uso

### **Cenário 1: Análise de Vendas**
```python
# Upload do arquivo vendas.csv
# O dashboard automaticamente:
# - Mostra estatísticas descritivas
# - Identifica produtos mais vendidos
# - Gera gráficos de tendência
# - Calcula correlações entre variáveis
```

### **Cenário 2: Análise de Clientes**
```python
# Upload do arquivo clientes.xlsx
# O dashboard identifica:
# - Segmentos com maior ticket médio
# - Sazonalidade de compras
# - Padrões de comportamento
```
- O projeto utiliza SQLite para persistência local.
- A camada de acesso está em `src/data/sqlite_manager.py`.
- Para gerar base de exemplo, execute:

### **Cenário 3: Dados Financeiros**
```python
# Upload de dados financeiros
# O dashboard calcula:
# - Médias móveis
# - Volatilidade
# - Correlações entre ativos
```bash
python scripts/generate_sample_data.py
```

---

## 📁 Projetos Relacionados (Estudos de Caso)

Confira meus projetos específicos onde aplico técnicas avançadas:
## Qualidade, Testes e Boas Práticas

| Projeto | Descrição | Tecnologias | Link |
|---------|-----------|-------------|------|
| **Case Study: Amazon Sales** | Análise de vendas da Amazon com dashboards interativos | Python, Streamlit, Pandas, Plotly | [Acessar](https://github.com/samuelmaia-data-analyst/case-study-amazon-sales) |
| **Case Study: Sales EDA** | Análise exploratória profunda de dados de vendas | Python, Pandas, Matplotlib, Seaborn | [Acessar](https://github.com/samuelmaia-data-analyst/case-study-sales-eda) |
| **Case Study: Churn Prediction** | Sistema completo de ML para previsão de cancelamento | Python, Scikit-learn, FastAPI, Streamlit | [Acessar](https://github.com/samuelmaia-data-analyst/case-study-churn-prediction) |
- Organização modular por domínio (`data`, `analysis`, `visualization`).
- Separação clara entre camada de interface e regras analíticas.
- Estrutura pronta para evolução de testes em `tests/`.

Cada projeto demonstra habilidades específicas e complementares ao meu trabalho principal.
Sugestões para evolução:
- Cobertura de testes unitários para transformações.
- Testes de integração para pipeline de ingestão + persistência.
- Lint e formatação automática no CI/CD.

---

## 🛣️ Roadmap
## Deploy

### ✅ Concluído
- [x] Upload de CSV e Excel com detecção de encoding
- [x] Análise exploratória básica
- [x] Gráficos interativos (15+ tipos)
- [x] Séries temporais e sazonalidade
- [x] Correlações e heatmaps
- [x] Testes estatísticos (t-test, ANOVA, qui-quadrado)

### 🚧 Em Desenvolvimento
- [ ] Modelos de Machine Learning integrados
- [ ] Autenticação de usuários
- [ ] Exportação de relatórios em PDF
- [ ] Integração com AWS S3
- [ ] Modo escuro
Deploy recomendado no **Streamlit Cloud** apontando para:
- **Main file:** `dashboard/app.py`
- **Branch:** `main`
- **Runtime:** Python compatível com `requirements.txt`

---

## 🤝 Como Contribuir

Contribuições são sempre bem-vindas! Siga os passos abaixo:
## Roadmap

| Passo | Ação | Comando |
|-------|------|---------|
| 1️⃣ | Fork o projeto | Clique no botão **Fork** no GitHub |
| 2️⃣ | Clone seu fork | `git clone https://github.com/seu-usuario/data-senior-analytics.git` |
| 3️⃣ | Crie uma branch | `git checkout -b feature/nova-funcionalidade` |
| 4️⃣ | Commit suas mudanças | `git commit -m 'Adiciona nova funcionalidade'` |
| 5️⃣ | Push para o GitHub | `git push origin feature/nova-funcionalidade` |
| 6️⃣ | Abra um Pull Request | Clique em **Compare & pull request** |

### 📋 Diretrizes

- ✅ Mantenha o código limpo e comentado
- ✅ Adicione testes para novas funcionalidades
- ✅ Atualize a documentação quando necessário
- ✅ Siga o estilo de código existente (PEP 8)
- [ ] Exportação de relatórios (PDF/HTML)
- [ ] Camada de autenticação de usuário
- [ ] Conectores para fontes externas (S3, banco relacional)
- [ ] Métricas e monitoramento de uso do dashboard
- [ ] Suite de testes automatizados com cobertura mínima definida

---

## 📄 Licença
## Contribuição

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
1. Faça um fork do projeto.
2. Crie uma branch de feature: `git checkout -b feature/minha-feature`.
3. Commit das alterações: `git commit -m "feat: descreve sua feature"`.
4. Push para seu fork.
5. Abra um Pull Request com contexto, impacto e evidências de validação.

---

## 👨‍💻 Autor

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://github.com/samuelmaia-data-analyst.png" width="150" height="150" style="border-radius: 50%; border: 4px solid #FF4B4B;" alt="Samuel Maia"/>
        <br>
        <h2>Samuel Maia</h2>
        <h3>🚀 Analista de Dados Sênior</h3>
        <p>
          <a href="https://github.com/samuelmaia-data-analyst/data-senior-analytics">
            <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
          </a>
          <a href="https://linkedin.com/in/samuelmaia-data-analyst">
            <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
          </a>
          <a href="mailto:smaia2@gmail.com">
            <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Email">
          </a>
        </p>
        <p>
          <strong>📍 Fortaleza, Brasil</strong>
        </p>
      </td>
    </tr>
  </table>
</div>

---

## 📊 Estatísticas do Projeto

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/samuelmaia-data-analyst/data-senior-analytics?style=social)
![GitHub forks](https://img.shields.io/github/forks/samuelmaia-data-analyst/data-senior-analytics?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/samuelmaia-data-analyst/data-senior-analytics?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/samuelmaia-data-analyst/data-senior-analytics)

</div>

---

<div align="center">
  <h2>⭐ Se este projeto te ajudou, considere dar uma estrela! ⭐</h2>
  <br>
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" width="100%">
</div>
```
## Licença

Este projeto está sob licença MIT.
