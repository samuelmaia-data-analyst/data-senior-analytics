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

---

## 📋 Sobre o Projeto

**Data Senior Analytics** é um dashboard interativo profissional desenvolvido para demonstrar habilidades completas de um **Analista de Dados Sênior**. O projeto permite carregar, analisar e visualizar dados de forma intuitiva, gerando insights automáticos e visualizações dinâmicas sem a necessidade de escrever uma única linha de código.

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

---

## 🎯 Objetivo do Projeto

Este projeto foi criado para **demonstrar na prática** as habilidades de um Analista de Dados Sênior:

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

---

## 🛠️ Stack Tecnológica

<div align="center">

| Categoria | Tecnologias |
|-----------|-------------|
| **Linguagem** | ![Python](https://img.shields.io/badge/Python-3.14.2-blue?style=for-the-badge&logo=python) |
| **Framework Web** | ![Streamlit](https://img.shields.io/badge/Streamlit-1.41.1-red?style=for-the-badge&logo=streamlit) |
| **Manipulação de Dados** | ![Pandas](https://img.shields.io/badge/Pandas-2.2.3-green?style=for-the-badge&logo=pandas) ![NumPy](https://img.shields.io/badge/NumPy-2.4.2-blue?style=for-the-badge&logo=numpy) |
| **Visualização** | ![Plotly](https://img.shields.io/badge/Plotly-6.0.0-orange?style=for-the-badge&logo=plotly) |
| **Estatística** | ![SciPy](https://img.shields.io/badge/SciPy-1.15.2-lightblue?style=for-the-badge&logo=scipy) |
| **Banco de Dados** | ![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite) |

</div>

---

## 📁 Estrutura do Projeto

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

---

## 🚀 Como Executar Localmente

### 📋 Pré-requisitos

- Python 3.11 ou superior
- Git (opcional, para clonar)
- pip (gerenciador de pacotes)

### 🔧 Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/samuelmaiapro/data-senior-analytics.git
cd data-senior-analytics

# 2. Crie e ative o ambiente virtual
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install --upgrade pip
pip install -r requirements.txt

# 4. (Opcional) Gere dados de exemplo
python scripts/generate_sample_data.py

# 5. Execute o dashboard
streamlit run dashboard/app.py
```

O dashboard estará disponível em: **http://localhost:8501**

---

## ☁️ Deploy no Streamlit Cloud

O projeto está disponível online gratuitamente:

👉 **[https://data-analytics-sr.streamlit.app](https://data-analytics-sr.streamlit.app)**

### Como o deploy foi feito:

1. Código enviado para o GitHub
2. Conectado ao [Streamlit Cloud](https://share.streamlit.io)
3. Configurado:
   - **Repository:** `samuelmaiapro/data-senior-analytics`
   - **Branch:** `main`
   - **Main file:** `dashboard/app.py`
4. Deploy automático a cada push no GitHub

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

### **Cenário 3: Dados Financeiros**
```python
# Upload de dados financeiros
# O dashboard calcula:
# - Médias móveis
# - Volatilidade
# - Correlações entre ativos
```

---

## 📁 Projetos Relacionados (Estudos de Caso)

Confira meus projetos específicos onde aplico técnicas avançadas:

| Projeto | Descrição | Tecnologias | Link |
|---------|-----------|-------------|------|
| **Case Study: Amazon Sales** | Análise de vendas da Amazon com dashboards interativos | Python, Streamlit, Pandas, Plotly | [Acessar](https://github.com/samuelmaiapro/case-study-amazon-sales) |
| **Case Study: Sales EDA** | Análise exploratória profunda de dados de vendas | Python, Pandas, Matplotlib, Seaborn | [Acessar](https://github.com/samuelmaiapro/case-study-sales-eda) |
| **Case Study: Churn Prediction** | Sistema completo de ML para previsão de cancelamento | Python, Scikit-learn, FastAPI, Streamlit | [Acessar](https://github.com/samuelmaiapro/case-study-churn-prediction) |

Cada projeto demonstra habilidades específicas e complementares ao meu trabalho principal.

---

## 🛣️ Roadmap

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

---

## 🤝 Como Contribuir

Contribuições são sempre bem-vindas! Siga os passos abaixo:

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

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="https://github.com/samuelmaiapro.png" width="150" height="150" style="border-radius: 50%; border: 4px solid #FF4B4B;" alt="Samuel Maia"/>
        <br>
        <h2>Samuel Maia</h2>
        <h3>🚀 Analista de Dados Sênior</h3>
        <p>
          <a href="https://github.com/samuelmaiapro/data-senior-analytics">
            <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
          </a>
          <a href="https://linkedin.com/in/samuelmaiapro">
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

![GitHub stars](https://img.shields.io/github/stars/samuelmaiapro/data-senior-analytics?style=social)
![GitHub forks](https://img.shields.io/github/forks/samuelmaiapro/data-senior-analytics?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/samuelmaiapro/data-senior-analytics?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/samuelmaiapro/data-senior-analytics)

</div>

---

<div align="center">
  <h2>⭐ Se este projeto te ajudou, considere dar uma estrela! ⭐</h2>
  <br>
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" width="100%">
</div>
```

