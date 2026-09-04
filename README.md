# Data Analytics Workflow

> **Projeto legado de portfólio.** Este repositório foi preservado como histórico técnico. O portfólio principal atual está concentrado em [Governed Analytics Platform](https://github.com/samuelmaia-analytics/Governed-Analytics-Platform), Central de Automação e Operações e [AWS Serverless Access Counter](https://github.com/samuelmaia-analytics/aws-serverless-access-counter).

Projeto de portfólio para transformar arquivos tabulares em um fluxo analítico prático, com ingestão, limpeza, qualidade, visualização e persistência local.

**Demo:** https://data-analytics-sr.streamlit.app

## O problema

Equipes recebem planilhas com estruturas diferentes e precisam responder rapidamente:

- O dado está confiável para análise?
- Quais são os principais sinais de receita e concentração?
- Onde existem problemas de completude ou duplicidade?
- Qual informação pode ser compartilhada com segurança?

## A solução

```text
CSV / XLSX
 → ingestão
 → limpeza e padronização
 → Quality Score
 → análise exploratória
 → KPIs e visualizações
 → persistência SQLite
 → Streamlit
```

## Principais entregas

- Upload de CSV e XLSX ou uso de dataset demonstrativo.
- Limpeza e padronização automática.
- Quality Score com avaliação de completude e duplicidade.
- KPIs e análise exploratória no Streamlit.
- Visualizações de tendência, distribuição e concentração.
- Persistência opcional em SQLite.
- Metadados de execução, retenção e privacidade.
- Testes automatizados, lint e CI.

## Valor demonstrado

O projeto mostra como estruturar uma rotina de análise que começa pela confiabilidade dos dados antes de chegar ao dashboard, tornando o processo mais rastreável e reduzindo o risco de decisões baseadas em bases inconsistentes.

## Stack

**Dados:** Python, pandas, NumPy, SQL, SQLite  
**Visualização:** Streamlit, Plotly  
**Qualidade e engenharia:** pytest, Ruff, Black, GitHub Actions

## Funcionalidades

- **Overview:** KPIs, confiança e recomendações.
- **Upload:** carga e curadoria automática.
- **Data:** comparação entre base bruta e curada.
- **EDA:** estatísticas, correlação e perfil de ausências.
- **Visualizations:** distribuição, mix e tendência temporal.
- **Database:** catálogo e inspeção de dados persistidos.
- **Settings:** metadados e governança aplicada.

## Como revisar este projeto em 5 minutos

1. Abra a [demo online](https://data-analytics-sr.streamlit.app).
2. Carregue um arquivo ou use o dataset de demonstração.
3. Compare a base bruta e a curada.
4. Observe o Quality Score e as recomendações.
5. Explore KPIs, EDA e persistência no SQLite.

## Como rodar localmente

```bash
git clone https://github.com/samuelmaia-analytics/data-senior-analytics.git
cd data-senior-analytics
python -m venv .venv
pip install -r requirements-dev.txt
python -m streamlit run dashboard/app.py
```

## Testes

```bash
python -m pytest
```

## Limitações e evolução

O projeto é uma demonstração local de workflow analítico. Evoluções previstas incluem conectores externos, contratos adicionais e maior observabilidade.

## Autor

Samuel Maia — Analista de Dados | Analytics Engineer

- LinkedIn: https://www.linkedin.com/in/samuelmaia-analytics/
- GitHub: https://github.com/samuelmaia-analytics

[English version](README.en.md)
