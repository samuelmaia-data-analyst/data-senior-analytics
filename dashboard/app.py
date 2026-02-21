"""
Dashboard Interativo - Data Senior Analytics
Autor: Samuel Maia
Versão: COMPLETA E CORRIGIDA - Todas as páginas funcionando
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import sys
import os
from datetime import datetime

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from src.data.sqlite_manager import SQLiteManager
from config.settings import Settings

# Tentar importar scipy (opcional)
try:
    from scipy import stats

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    stats = None

# Configuração da página (DEVE SER O PRIMEIRO COMANDO)
st.set_page_config(
    page_title="Data Senior Analytics - Samuel Maia",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .metric-card {
        background: linear-gradient(135deg, #f0f2f6 0%, #e6e9f0 100%);
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .upload-box {
        border: 3px dashed #FF4B4B;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        background: linear-gradient(135deg, #fff5f5 0%, #ffe9e9 100%);
        transition: all 0.3s;
    }
    .upload-box:hover {
        border-color: #ff6b6b;
        background: linear-gradient(135deg, #ffe9e9 0%, #ffdddd 100%);
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #2196f3;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff9800;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4caf50;
        margin: 1rem 0;
    }
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .correlation-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin: 0.5rem 0;
    }
    .sidebar-header {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%);
        border-radius: 15px;
        margin-bottom: 1.5rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Título
st.markdown('<h1 class="main-header">📊 Data Senior Analytics</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Samuel Maia - Analista de Dados Sênior | Python 3.14 | Streamlit 1.41</p>',
            unsafe_allow_html=True)
st.markdown("---")

# Inicializa session state para armazenar dados
if 'data' not in st.session_state:
    st.session_state.data = None
if 'data_name' not in st.session_state:
    st.session_state.data_name = None
if 'data_source' not in st.session_state:
    st.session_state.data_source = None
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []


# Inicializa conexão com banco
@st.cache_resource
def init_db():
    return SQLiteManager()


db = init_db()

# Sidebar
with st.sidebar:
    # Logo em texto (sem imagens externas)
    st.markdown("""
    <div class='sidebar-header'>
        <h1 style='margin:0; font-size:3rem;'>📊📈</h1>
        <h2 style='margin:0.5rem 0 0 0; color:white;'>Data Senior</h2>
        <h3 style='margin:0; color:white; opacity:0.9;'>Analytics</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 👨‍💻 Samuel Maia")
    st.markdown("**Analista de Dados Sênior**")
    st.markdown("📧 smaia2@gmail.com")
    st.markdown("🔗 linkedin.com/in/samuelmaiapro")
    st.markdown("🐙 github.com/samuelmaiapro/portfolio-analista-dados")
    st.markdown("---")

    # Navegação
    st.markdown("### 🧭 Navegação")
    page = st.radio(
        "Ir para:",
        ["🏠 Home",
         "📤 Upload de Dados",
         "📊 Visualizar Dados",
         "📈 Análise Exploratória",
         "📊 Visualizações Completas",
         "🔍 Análise Estatística Avançada",
         "📉 Séries Temporais",
         "📊 Correlações e Relacionamentos",
         "📋 Relatórios Automáticos",
         "💾 Banco de Dados",
         "⚙️ Configurações"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Informações dos dados atuais
    if st.session_state.data is not None:
        st.markdown("### 📁 Dados Atuais")
        with st.container():
            st.markdown(f"**Arquivo:** {st.session_state.data_name[:30]}..." if len(
                st.session_state.data_name) > 30 else f"**Arquivo:** {st.session_state.data_name}")
            st.markdown(f"**Linhas:** {st.session_state.data.shape[0]:,}")
            st.markdown(f"**Colunas:** {st.session_state.data.shape[1]}")
            st.markdown(f"**Memória:** {st.session_state.data.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")
    else:
        st.info("👆 **Dica:** Faça upload de um arquivo na página '📤 Upload de Dados'")


# Funções auxiliares
def detect_column_types(df):
    """Detecta e categoriza colunas por tipo"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

    # Também tentar converter colunas que parecem datas
    for col in df.columns:
        if col not in date_cols and df[col].dtype == 'object':
            try:
                pd.to_datetime(df[col].dropna().iloc[0])
                if col not in date_cols:
                    date_cols.append(col)
            except:
                pass

    # Detectar possíveis IDs (colunas com muitos valores únicos)
    id_cols = []
    for col in numeric_cols:
        if df[col].nunique() > len(df) * 0.9:
            id_cols.append(col)

    # Colunas booleanas
    bool_cols = df.select_dtypes(include=['bool']).columns.tolist()

    return {
        'numeric': [c for c in numeric_cols if c not in id_cols],
        'categorical': categorical_cols,
        'date': date_cols,
        'id': id_cols,
        'boolean': bool_cols,
        'all_numeric': numeric_cols
    }


def get_basic_stats(df, col):
    """Calcula estatísticas básicas para uma coluna"""
    stats_dict = {}
    if col in df.select_dtypes(include=[np.number]).columns:
        stats_dict['Média'] = df[col].mean()
        stats_dict['Mediana'] = df[col].median()
        stats_dict['Moda'] = df[col].mode()[0] if not df[col].mode().empty else None
        stats_dict['Desvio Padrão'] = df[col].std()
        stats_dict['Variância'] = df[col].var()
        stats_dict['Mínimo'] = df[col].min()
        stats_dict['Máximo'] = df[col].max()
        stats_dict['Q1'] = df[col].quantile(0.25)
        stats_dict['Q3'] = df[col].quantile(0.75)
        stats_dict['IQR'] = stats_dict['Q3'] - stats_dict['Q1']
        stats_dict['Assimetria'] = df[col].skew()
        stats_dict['Curtose'] = df[col].kurtosis()
    return stats_dict


def interpret_correlation(corr):
    """Interpreta o valor da correlação"""
    if abs(corr) > 0.9:
        return "Muito Forte", "🔥"
    elif abs(corr) > 0.7:
        return "Forte", "💪"
    elif abs(corr) > 0.5:
        return "Moderada", "👍"
    elif abs(corr) > 0.3:
        return "Fraca", "👎"
    else:
        return "Muito Fraca", "❌"


# Página Home
if page == "🏠 Home":
    st.header("🏠 Página Inicial - Dashboard Analítico")

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Python", "3.14.2", "Latest")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Pandas", "2.2.3", "Stable")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Streamlit", "1.41.1", "Latest")
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Plotly", "6.0.0", "Latest")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Cards de informações
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.subheader("🚀 Sobre o Projeto")
        st.markdown("""
        **Dashboard profissional para análise de dados** desenvolvido com as mais recentes tecnologias:

        ✅ **Upload inteligente** - Suporte a CSV/Excel com detecção automática de encoding
        ✅ **Análise exploratória** - Estatísticas descritivas, correlações, outliers
        ✅ **Visualizações completas** - 15+ tipos de gráficos interativos
        ✅ **Séries temporais** - Tendências, sazonalidade, previsões
        ✅ **Relatórios automáticos** - Geração de insights e métricas
        ✅ **Banco de dados** - SQLite integrado para persistência
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.subheader("📋 Como Usar")
        st.markdown("""
        1. **📤 Upload de Dados** - Carregue seu arquivo CSV ou Excel
        2. **📊 Visualizar** - Explore os dados brutos
        3. **📈 Análises** - Descubra insights automáticos
        4. **📊 Gráficos** - Crie visualizações interativas
        5. **💾 Banco** - Salve no SQLite para uso futuro

        **Dicas:**
        - Arquivos com acentos funcionam perfeitamente
        - Suporte a encoding automático
        - Limite de 200MB por arquivo
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Estatísticas do sistema
    st.subheader("📊 Estatísticas do Sistema")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.session_state.data is not None:
            st.metric("Dados Carregados", "✅ Sim", st.session_state.data_name[:20] + "..." if len(
                st.session_state.data_name) > 20 else st.session_state.data_name)
        else:
            st.metric("Dados Carregados", "❌ Não")

    with col2:
        tables = db.list_tables()
        st.metric("Tabelas no Banco", len(tables))

    with col3:
        if st.session_state.data is not None:
            st.metric("Linhas", f"{st.session_state.data.shape[0]:,}")
        else:
            st.metric("Linhas", "0")

    with col4:
        if st.session_state.data is not None:
            st.metric("Colunas", st.session_state.data.shape[1])
        else:
            st.metric("Colunas", "0")

# Página UPLOAD DE DADOS
elif page == "📤 Upload de Dados":
    st.header("📤 Upload de Dados")

    # Área de upload em destaque
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    st.markdown("### ⬆️ Arraste ou selecione um arquivo")

    uploaded_file = st.file_uploader(
        "Escolha um arquivo",
        type=['csv', 'xlsx', 'xls'],
        help="Formatos suportados: CSV, Excel (.xlsx, .xls)",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Opções avançadas
    with st.expander("⚙️ Opções avançadas de upload"):
        encoding_option = st.selectbox(
            "Encoding (se CSV)",
            ["auto", "utf-8", "latin-1", "cp1252", "iso-8859-1"]
        )
        sep_option = st.text_input("Separador (se CSV)", ",")
        sheet_option = st.text_input("Planilha (se Excel)", "0")

    # Se arquivo foi enviado
    if uploaded_file is not None:
        try:
            with st.spinner(f"🔄 Carregando {uploaded_file.name}..."):

                # Detectar encoding se necessário
                if uploaded_file.name.endswith('.csv'):
                    if encoding_option == "auto":
                        # Tentar diferentes encodings
                        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
                        df = None
                        used_encoding = None

                        for enc in encodings:
                            try:
                                uploaded_file.seek(0)
                                df = pd.read_csv(uploaded_file, encoding=enc, sep=sep_option)
                                used_encoding = enc
                                break
                            except UnicodeDecodeError:
                                continue

                        if df is None:
                            st.error("❌ Não foi possível ler o arquivo com nenhum encoding")
                            st.stop()
                    else:
                        df = pd.read_csv(uploaded_file, encoding=encoding_option, sep=sep_option)
                else:
                    # Excel
                    if sheet_option.isdigit():
                        df = pd.read_excel(uploaded_file, sheet_name=int(sheet_option))
                    else:
                        df = pd.read_excel(uploaded_file, sheet_name=sheet_option)

                # Salvar no session state
                st.session_state.data = df
                st.session_state.data_name = uploaded_file.name
                st.session_state.data_source = "upload"

                # Mostrar preview
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.success(f"✅ Arquivo '{uploaded_file.name}' carregado com sucesso!")
                if used_encoding:
                    st.info(f"📝 Encoding detectado: {used_encoding}")
                st.markdown('</div>', unsafe_allow_html=True)

                # Métricas em colunas
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Linhas", f"{df.shape[0]:,}")
                with col2:
                    st.metric("Colunas", df.shape[1])
                with col3:
                    st.metric("Memória", f"{df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")
                with col4:
                    st.metric("Duplicatas", df.duplicated().sum())

                # Preview dos dados
                st.subheader("🔍 Preview dos Dados (primeiras 100 linhas)")
                st.dataframe(df.head(100), use_container_width=True)

                # Informações das colunas
                st.subheader("📋 Informações das Colunas")
                col_info = pd.DataFrame({
                    'Coluna': df.columns,
                    'Tipo': df.dtypes.astype(str).values,
                    'Não Nulos': df.count().values,
                    'Nulos': df.isnull().sum().values,
                    'Nulos %': (df.isnull().sum().values / len(df) * 100).round(2),
                    'Valores Únicos': [df[col].nunique() for col in df.columns]
                })
                st.dataframe(col_info, use_container_width=True)

                # Opção de salvar no banco
                st.subheader("💾 Salvar no Banco de Dados")
                col1, col2 = st.columns(2)
                with col1:
                    table_name = st.text_input("Nome da tabela:", uploaded_file.name.replace('.', '_'))
                    if st.button("💾 Salvar no SQLite"):
                        if table_name and st.button("Confirmar salvamento", key="confirm_save"):
                            if db.df_to_sql(df, table_name):
                                st.success(f"✅ Dados salvos na tabela '{table_name}'!")
                            else:
                                st.error("❌ Erro ao salvar no banco")

                with col2:
                    if st.button("📥 Download CSV"):
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="Clique para baixar",
                            data=csv,
                            file_name=f"processado_{uploaded_file.name}",
                            mime="text/csv"
                        )

        except Exception as e:
            st.error(f"❌ Erro ao carregar arquivo: {str(e)}")
            st.exception(e)

    else:
        # Mostrar exemplos de arquivos
        st.info("👆 Faça upload de um arquivo CSV ou Excel para começar")

        # Listar arquivos disponíveis na pasta raw
        raw_files = list(Settings.RAW_DATA_DIR.glob("*.csv")) + list(Settings.RAW_DATA_DIR.glob("*.xlsx"))

        if raw_files:
            st.subheader("📁 Arquivos disponíveis na pasta raw:")
            for file in raw_files:
                st.text(f"   • {file.name}")

# Página Visualizar Dados
elif page == "📊 Visualizar Dados":
    st.header("📊 Visualização de Dados")

    if st.session_state.data is not None:
        df = st.session_state.data

        # Opções de visualização
        st.subheader("🔍 Opções de Visualização")

        col1, col2, col3 = st.columns(3)
        with col1:
            n_rows = st.slider("Número de linhas para exibir:", 10, 1000, 100, step=10)
        with col2:
            sort_col = st.selectbox("Ordenar por (opcional)", ["Nenhum"] + df.columns.tolist())
        with col3:
            sort_order = st.radio("Ordem", ["Crescente", "Decrescente"], horizontal=True)

        # Filtrar colunas
        all_cols = df.columns.tolist()
        selected_cols = st.multiselect("Selecionar colunas para exibir", all_cols,
                                       default=all_cols[:min(10, len(all_cols))])

        if selected_cols:
            df_view = df[selected_cols].copy()

            # Ordenar
            if sort_col != "Nenhum":
                ascending = sort_order == "Crescente"
                df_view = df_view.sort_values(sort_col, ascending=ascending)

            # Mostrar dados
            st.subheader("📋 Dados")
            st.dataframe(df_view.head(n_rows), use_container_width=True)

            # Download
            csv = df_view.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"visualizacao_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.warning("⚠️ Nenhum dado carregado. Vá para '📤 Upload de Dados' primeiro.")

# Página Análise Exploratória
elif page == "📈 Análise Exploratória":
    st.header("📈 Análise Exploratória de Dados")

    if st.session_state.data is not None:
        df = st.session_state.data

        # Detectar tipos de colunas
        col_types = detect_column_types(df)

        # Resumo geral
        st.subheader("📊 Resumo Geral")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Linhas", f"{df.shape[0]:,}")
        with col2:
            st.metric("Total Colunas", df.shape[1])
        with col3:
            st.metric("Colunas Numéricas", len(col_types['numeric']))
        with col4:
            st.metric("Colunas Categóricas", len(col_types['categorical']))

        # Análise de valores faltantes
        st.subheader("⚠️ Análise de Valores Faltantes")

        missing_df = pd.DataFrame({
            'Coluna': df.columns,
            'Valores Faltantes': df.isnull().sum().values,
            'Percentual': (df.isnull().sum().values / len(df) * 100).round(2)
        }).sort_values('Valores Faltantes', ascending=False)

        # Mostrar apenas colunas com valores faltantes
        missing_with_data = missing_df[missing_df['Valores Faltantes'] > 0]

        if len(missing_with_data) > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(missing_with_data, use_container_width=True)
            with col2:
                fig = px.bar(
                    missing_with_data.head(20),
                    x='Coluna',
                    y='Valores Faltantes',
                    title="Top Colunas com Valores Faltantes",
                    color='Valores Faltantes',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ Não há valores faltantes no dataset!")

        # Estatísticas descritivas
        if col_types['numeric']:
            st.subheader("📊 Estatísticas Descritivas - Variáveis Numéricas")
            stats_df = df[col_types['numeric']].describe().T
            # Adicionar skewness e kurtosis
            for col in col_types['numeric']:
                stats_df.loc[col, 'skew'] = df[col].skew()
                stats_df.loc[col, 'kurtosis'] = df[col].kurtosis()
            st.dataframe(stats_df, use_container_width=True)

        # Análise de valores únicos para categóricas
        if col_types['categorical']:
            st.subheader("📝 Análise de Variáveis Categóricas")

            cat_stats = []
            for col in col_types['categorical'][:10]:  # Limitar a 10
                value_counts = df[col].value_counts()
                if len(value_counts) > 0:
                    cat_stats.append({
                        'Coluna': col,
                        'Valores Únicos': df[col].nunique(),
                        'Moda': value_counts.index[0],
                        'Frequência da Moda': value_counts.iloc[0],
                        '% da Moda': round((value_counts.iloc[0] / len(df) * 100), 2)
                    })

            if cat_stats:
                st.dataframe(pd.DataFrame(cat_stats), use_container_width=True)

        # Detecção de outliers
        if col_types['numeric']:
            st.subheader("🔍 Detecção de Outliers (Método IQR)")

            outliers_info = []
            for col in col_types['numeric'][:10]:  # Limitar a 10
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

                outliers_info.append({
                    'Coluna': col,
                    'Outliers': len(outliers),
                    '% Outliers': round((len(outliers) / len(df) * 100), 2),
                    'Limite Inferior': round(lower_bound, 2),
                    'Limite Superior': round(upper_bound, 2)
                })

            outliers_df = pd.DataFrame(outliers_info)
            st.dataframe(outliers_df, use_container_width=True)

        # Insights automáticos
        st.subheader("💡 Insights Automáticos")

        insights = []

        # Tamanho do dataset
        if df.shape[0] > 10000:
            insights.append(f"📊 **Dataset grande**: {df.shape[0]:,} linhas")
        elif df.shape[0] > 1000:
            insights.append(f"📊 **Dataset médio**: {df.shape[0]:,} linhas")
        else:
            insights.append(f"📊 **Dataset pequeno**: {df.shape[0]} linhas")

        # Valores faltantes
        missing_total = df.isnull().sum().sum()
        if missing_total > 0:
            missing_pct = (missing_total / (df.shape[0] * df.shape[1])) * 100
            insights.append(f"⚠️ **Valores faltantes**: {missing_total} ({missing_pct:.1f}% do total)")
        else:
            insights.append("✅ **Sem valores faltantes**")

        # Duplicatas
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            dup_pct = (duplicates / df.shape[0]) * 100
            insights.append(f"🔄 **Linhas duplicadas**: {duplicates} ({dup_pct:.1f}%)")
        else:
            insights.append("✅ **Sem linhas duplicadas**")

        # Correlações fortes
        if len(col_types['numeric']) > 1:
            corr_matrix = df[col_types['numeric']].corr()
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i + 1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.7:
                        strong_corr.append(
                            f"{corr_matrix.columns[i]} x {corr_matrix.columns[j]}: {corr_matrix.iloc[i, j]:.2f}")

            if strong_corr:
                insights.append(f"🔗 **Correlações fortes encontradas**: {len(strong_corr)} pares")
                for corr in strong_corr[:3]:  # Mostrar apenas 3
                    insights.append(f"   - {corr}")

        for insight in insights:
            st.markdown(f"- {insight}")

        # Salvar no histórico
        if st.button("💾 Salvar esta análise no histórico"):
            st.session_state.analysis_history.append({
                'timestamp': datetime.now(),
                'data': st.session_state.data_name,
                'insights': insights
            })
            st.success("✅ Análise salva no histórico!")

    else:
        st.warning("⚠️ Nenhum dado carregado. Vá para '📤 Upload de Dados' primeiro.")

# Página Visualizações Completas
elif page == "📊 Visualizações Completas":
    st.header("📊 Visualizações Completas - 15+ Tipos de Gráficos")

    if st.session_state.data is not None:
        df = st.session_state.data

        # Detectar tipos de colunas
        col_types = detect_column_types(df)

        # Mostrar informações sobre colunas disponíveis
        with st.expander("📋 Colunas disponíveis por tipo", expanded=False):
            tab1, tab2, tab3, tab4 = st.tabs(["🔢 Numéricas", "📝 Categóricas", "📅 Datas", "🆔 IDs"])

            with tab1:
                if col_types['numeric']:
                    for col in col_types['numeric']:
                        st.markdown(f"- {col}")
                else:
                    st.write("Nenhuma coluna numérica encontrada")

            with tab2:
                if col_types['categorical']:
                    for col in col_types['categorical']:
                        st.markdown(f"- {col}")
                else:
                    st.write("Nenhuma coluna categórica encontrada")

            with tab3:
                if col_types['date']:
                    for col in col_types['date']:
                        st.markdown(f"- {col}")
                else:
                    st.write("Nenhuma coluna de data encontrada")

            with tab4:
                if col_types['id']:
                    for col in col_types['id']:
                        st.markdown(f"- {col}")
                else:
                    st.write("Nenhuma coluna ID detectada")

        # Categoria de visualização
        chart_category = st.selectbox(
            "Categoria de Visualização",
            ["📊 Distribuições", "📈 Relacionamentos", "📊 Comparações", "📉 Séries Temporais", "📋 Composições"]
        )

        if chart_category == "📊 Distribuições":
            st.subheader("📊 Gráficos de Distribuição")

            if col_types['numeric']:
                col = st.selectbox("Selecione uma coluna numérica", col_types['numeric'])

                chart_type = st.radio(
                    "Tipo de Gráfico",
                    ["Histograma", "Boxplot", "Violino", "Density Plot"],
                    horizontal=True
                )

                if chart_type == "Histograma":
                    bins = st.slider("Número de bins", 5, 100, 30)
                    fig = px.histogram(df, x=col, nbins=bins, title=f"Histograma - {col}", marginal="box")
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Boxplot":
                    fig = px.box(df, y=col, title=f"Boxplot - {col}")
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Violino":
                    fig = px.violin(df, y=col, title=f"Violino - {col}", box=True)
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Density Plot":
                    fig = px.density_contour(df, x=col, title=f"Density Plot - {col}")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Nenhuma coluna numérica disponível para gráficos de distribuição")

        elif chart_category == "📈 Relacionamentos":
            st.subheader("📈 Gráficos de Relacionamento")

            if len(col_types['numeric']) >= 2:
                chart_type = st.radio(
                    "Tipo de Gráfico",
                    ["Dispersão", "Matriz de Dispersão", "Heatmap"],
                    horizontal=True
                )

                if chart_type == "Dispersão":
                    col1 = st.selectbox("Eixo X", col_types['numeric'], key='x_rel')
                    col2 = st.selectbox("Eixo Y", [c for c in col_types['numeric'] if c != col1], key='y_rel')

                    fig = px.scatter(df, x=col1, y=col2, title=f"{col1} x {col2}", opacity=0.6)
                    st.plotly_chart(fig, use_container_width=True)

                    # Correlação
                    corr = df[col1].corr(df[col2])
                    st.info(f"📊 Correlação: {corr:.3f}")

                elif chart_type == "Matriz de Dispersão":
                    selected_cols = st.multiselect("Selecione colunas", col_types['numeric'],
                                                   default=col_types['numeric'][:4])
                    if len(selected_cols) >= 2:
                        fig = px.scatter_matrix(df, dimensions=selected_cols, title="Matriz de Dispersão")
                        st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Heatmap":
                    selected_cols = st.multiselect("Selecione colunas", col_types['numeric'],
                                                   default=col_types['numeric'])
                    if len(selected_cols) >= 2:
                        corr = df[selected_cols].corr()
                        fig = px.imshow(corr, text_auto=True, aspect="auto", title="Matriz de Correlação",
                                        color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ São necessárias pelo menos 2 colunas numéricas para gráficos de relacionamento")

        elif chart_category == "📊 Comparações":
            st.subheader("📊 Gráficos de Comparação")

            if col_types['categorical'] and col_types['numeric']:
                cat_col = st.selectbox("Coluna categórica", col_types['categorical'])
                num_col = st.selectbox("Coluna numérica", col_types['numeric'])

                chart_type = st.radio(
                    "Tipo de Gráfico",
                    ["Barras", "Boxplot por Categoria", "Violino por Categoria"],
                    horizontal=True
                )

                if chart_type == "Barras":
                    # Agregar
                    agg_df = df.groupby(cat_col)[num_col].mean().reset_index().sort_values(num_col,
                                                                                           ascending=False).head(20)
                    fig = px.bar(agg_df, x=cat_col, y=num_col, title=f"Média de {num_col} por {cat_col}")
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Boxplot por Categoria":
                    fig = px.box(df, x=cat_col, y=num_col, title=f"Boxplot de {num_col} por {cat_col}")
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Violino por Categoria":
                    fig = px.violin(df, x=cat_col, y=num_col, title=f"Violino de {num_col} por {cat_col}")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ São necessárias colunas categóricas e numéricas para gráficos de comparação")

        elif chart_category == "📉 Séries Temporais":
            st.subheader("📉 Gráficos de Séries Temporais")

            if col_types['date']:
                date_col = st.selectbox("Coluna de data", col_types['date'])

                if col_types['numeric']:
                    value_col = st.selectbox("Coluna de valor", col_types['numeric'])

                    chart_type = st.radio(
                        "Tipo de Gráfico",
                        ["Linha", "Área", "Barras", "Média Móvel"],
                        horizontal=True
                    )

                    if chart_type == "Linha":
                        fig = px.line(df.sort_values(date_col), x=date_col, y=value_col,
                                      title=f"{value_col} ao longo do tempo")
                        st.plotly_chart(fig, use_container_width=True)

                    elif chart_type == "Área":
                        fig = px.area(df.sort_values(date_col), x=date_col, y=value_col, title=f"{value_col} - Área")
                        st.plotly_chart(fig, use_container_width=True)

                    elif chart_type == "Barras":
                        fig = px.bar(df.sort_values(date_col), x=date_col, y=value_col, title=f"{value_col} - Barras")
                        st.plotly_chart(fig, use_container_width=True)

                    elif chart_type == "Média Móvel":
                        window = st.slider("Janela da média móvel", 2, 30, 7)
                        df_sorted = df.sort_values(date_col).copy()
                        df_sorted['media_movel'] = df_sorted[value_col].rolling(window=window).mean()

                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=df_sorted[date_col], y=df_sorted[value_col],
                                                 mode='lines', name='Original', opacity=0.5))
                        fig.add_trace(go.Scatter(x=df_sorted[date_col], y=df_sorted['media_movel'],
                                                 mode='lines', name=f'Média Móvel {window}',
                                                 line=dict(color='red', width=3)))
                        fig.update_layout(title=f"{value_col} - Média Móvel")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ Nenhuma coluna numérica disponível")
            else:
                st.warning("⚠️ Nenhuma coluna de data encontrada")

        elif chart_category == "📋 Composições":
            st.subheader("📋 Gráficos de Composição")

            if col_types['categorical']:
                cat_col = st.selectbox("Coluna categórica", col_types['categorical'])

                # Contagens
                value_counts = df[cat_col].value_counts().reset_index()
                value_counts.columns = [cat_col, 'Contagem']
                value_counts = value_counts.head(20)

                chart_type = st.radio(
                    "Tipo de Gráfico",
                    ["Pizza", "Rosca", "Barras"],
                    horizontal=True
                )

                if chart_type == "Pizza":
                    fig = px.pie(value_counts, values='Contagem', names=cat_col, title=f"Distribuição - {cat_col}")
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Rosca":
                    fig = px.pie(value_counts, values='Contagem', names=cat_col, title=f"Distribuição - {cat_col}",
                                 hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "Barras":
                    fig = px.bar(value_counts, x=cat_col, y='Contagem', title=f"Distribuição - {cat_col}")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("⚠️ Nenhuma coluna categórica disponível")
    else:
        st.warning("⚠️ Nenhum dado carregado. Vá para '📤 Upload de Dados' primeiro.")

# Página Análise Estatística Avançada
elif page == "🔍 Análise Estatística Avançada":
    st.header("🔍 Análise Estatística Avançada")

    if not SCIPY_AVAILABLE:
        st.warning(
            "⚠️ Biblioteca 'scipy' não está instalada. Para usar testes estatísticos, instale com: `pip install scipy`")
        st.info("💡 Enquanto isso, você pode usar as outras funcionalidades do dashboard.")

    if st.session_state.data is not None:
        df = st.session_state.data
        col_types = detect_column_types(df)

        if col_types['numeric'] and SCIPY_AVAILABLE:
            # Testes estatísticos
            test_type = st.selectbox(
                "Selecione o teste estatístico",
                ["Teste t (comparação de médias)",
                 "ANOVA (análise de variância)",
                 "Correlação de Pearson",
                 "Correlação de Spearman"]
            )

            if test_type == "Teste t (comparação de médias)" and col_types['categorical']:
                cat_col = st.selectbox("Variável categórica (2 grupos)", col_types['categorical'])
                num_col = st.selectbox("Variável numérica", col_types['numeric'])

                groups = df[cat_col].dropna().unique()
                if len(groups) == 2:
                    group1 = df[df[cat_col] == groups[0]][num_col].dropna()
                    group2 = df[df[cat_col] == groups[1]][num_col].dropna()

                    t_stat, p_value = stats.ttest_ind(group1, group2)

                    st.subheader("Resultado do Teste t")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Estatística t", f"{t_stat:.4f}")
                    with col2:
                        st.metric("Valor p", f"{p_value:.4f}")

                    if p_value < 0.05:
                        st.success(f"✅ Há diferença significativa entre {groups[0]} e {groups[1]} (p < 0.05)")
                    else:
                        st.warning(f"⚠️ Não há diferença significativa (p >= 0.05)")
                else:
                    st.warning("⚠️ A variável categórica deve ter exatamente 2 grupos")

            elif test_type == "ANOVA (análise de variância)" and col_types['categorical']:
                cat_col = st.selectbox("Variável categórica", col_types['categorical'])
                num_col = st.selectbox("Variável numérica", col_types['numeric'])

                groups = []
                for name, group in df.groupby(cat_col)[num_col]:
                    if len(group.dropna()) > 0:
                        groups.append(group.dropna())

                if len(groups) >= 2:
                    f_stat, p_value = stats.f_oneway(*groups)

                    st.subheader("Resultado da ANOVA")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Estatística F", f"{f_stat:.4f}")
                    with col2:
                        st.metric("Valor p", f"{p_value:.4f}")

                    if p_value < 0.05:
                        st.success(f"✅ Há diferença significativa entre os grupos (p < 0.05)")
                    else:
                        st.warning(f"⚠️ Não há diferença significativa (p >= 0.05)")
                else:
                    st.warning("⚠️ A variável categórica precisa ter pelo menos 2 grupos com dados")

            elif test_type in ["Correlação de Pearson", "Correlação de Spearman"] and len(col_types['numeric']) >= 2:
                col1 = st.selectbox("Variável 1", col_types['numeric'])
                col2 = st.selectbox("Variável 2", [c for c in col_types['numeric'] if c != col1])

                if test_type == "Correlação de Pearson":
                    corr, p_value = stats.pearsonr(df[col1].dropna(), df[col2].dropna())
                    test_name = "Pearson"
                else:
                    corr, p_value = stats.spearmanr(df[col1].dropna(), df[col2].dropna())
                    test_name = "Spearman"

                st.subheader(f"Resultado da Correlação de {test_name}")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Correlação", f"{corr:.4f}")
                with col2:
                    st.metric("Valor p", f"{p_value:.4f}")

                strength, emoji = interpret_correlation(corr)
                direction = "positiva" if corr > 0 else "negativa"

                st.info(f"{emoji} Correlação {direction} ({strength})")

                if p_value < 0.05:
                    st.success("✅ Correlação estatisticamente significativa (p < 0.05)")
                else:
                    st.warning("⚠️ Correlação não significativa (p >= 0.05)")
        elif not SCIPY_AVAILABLE:
            st.info("💡 Instale scipy para habilitar testes estatísticos")
        else:
            st.warning("⚠️ São necessárias colunas numéricas para testes estatísticos")
    else:
        st.warning("⚠️ Nenhum dado carregado")

# Página Séries Temporais - COMPLETA!
elif page == "📉 Séries Temporais":
    st.header("📉 Análise de Séries Temporais")

    if st.session_state.data is not None:
        df = st.session_state.data

        # Detectar tipos de colunas
        col_types = detect_column_types(df)

        # EXPLICAÇÃO SOBRE SÉRIES TEMPORAIS
        with st.expander("ℹ️ O que são Séries Temporais?", expanded=False):
            st.markdown("""
            **Séries temporais** são conjuntos de dados organizados em ordem cronológica.

            ### Para usar esta seção:
            1. **Coluna de data**: Deve conter datas (ex: '2024-01-01', '01/01/2024')
            2. **Coluna de valor**: Deve conter números para analisar ao longo do tempo

            ### Exemplos de análise:
            - Tendências de vendas ao longo dos meses
            - Sazonalidade (padrões que se repetem)
            - Médias móveis para suavizar flutuações
            """)

        # Verificar se há colunas de data
        if col_types['date']:
            st.success(f"✅ Encontradas {len(col_types['date'])} colunas de data!")

            # Selecionar coluna de data
            date_col = st.selectbox(
                "📅 Selecione a coluna de data:",
                col_types['date'],
                help="Escolha a coluna que contém as datas para análise temporal"
            )

            # Tentar converter para datetime se necessário
            if date_col not in df.select_dtypes(include=['datetime64']).columns:
                with st.spinner(f"Convertendo '{date_col}' para formato de data..."):
                    try:
                        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                        st.success("✅ Coluna convertida para formato de data!")
                    except Exception as e:
                        st.error(f"❌ Erro ao converter para data: {e}")

            # Verificar se há valores nulos após conversão
            null_dates = df[date_col].isnull().sum()
            if null_dates > 0:
                st.warning(f"⚠️ {null_dates} valores não puderam ser convertidos para data e serão ignorados.")
                df_time = df.dropna(subset=[date_col]).copy()
            else:
                df_time = df.copy()

            # Ordenar por data
            df_time = df_time.sort_values(date_col)

            # Verificar colunas numéricas
            if col_types['numeric']:
                st.success(f"✅ Encontradas {len(col_types['numeric'])} colunas numéricas!")

                # Selecionar coluna de valor
                value_col = st.selectbox(
                    "📊 Selecione a coluna de valor:",
                    col_types['numeric'],
                    help="Escolha a coluna numérica para analisar ao longo do tempo"
                )

                # Período dos dados
                min_date = df_time[date_col].min()
                max_date = df_time[date_col].max()
                date_range = (max_date - min_date).days

                st.info(
                    f"📅 Período analisado: {min_date.strftime('%d/%m/%Y')} até {max_date.strftime('%d/%m/%Y')} ({date_range} dias)")

                # Tipo de gráfico
                st.subheader("📈 Visualizações Temporais")

                chart_type = st.radio(
                    "Tipo de visualização:",
                    ["📈 Gráfico de Linha", "📊 Gráfico de Área", "📉 Média Móvel", "📅 Agregação por Período",
                     "📊 Sazonalidade"],
                    horizontal=True
                )

                if chart_type == "📈 Gráfico de Linha":
                    fig = px.line(
                        df_time,
                        x=date_col,
                        y=value_col,
                        title=f"{value_col} ao longo do tempo",
                        markers=True
                    )

                    fig.update_layout(
                        xaxis_title="Data",
                        yaxis_title=value_col,
                        hovermode='x unified'
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    # Estatísticas
                    st.subheader("📊 Estatísticas da Série")

                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Média", f"{df_time[value_col].mean():.2f}")
                    with col2:
                        st.metric("Mediana", f"{df_time[value_col].median():.2f}")
                    with col3:
                        st.metric("Mínimo", f"{df_time[value_col].min():.2f}")
                    with col4:
                        st.metric("Máximo", f"{df_time[value_col].max():.2f}")

                elif chart_type == "📊 Gráfico de Área":
                    fig = px.area(
                        df_time,
                        x=date_col,
                        y=value_col,
                        title=f"{value_col} - Gráfico de Área"
                    )

                    fig.update_layout(
                        xaxis_title="Data",
                        yaxis_title=value_col
                    )

                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "📉 Média Móvel":
                    st.markdown("""
                    **Média Móvel** suaviza flutuações de curto prazo para destacar tendências de longo prazo.
                    """)

                    window = st.slider(
                        "Janela da média móvel (dias/períodos):",
                        min_value=2,
                        max_value=min(60, len(df_time) // 2),
                        value=min(7, len(df_time) // 2)
                    )

                    # Calcular média móvel
                    df_time['media_movel'] = df_time[value_col].rolling(window=window, min_periods=1).mean()

                    # Criar gráfico
                    fig = go.Figure()

                    fig.add_trace(go.Scatter(
                        x=df_time[date_col],
                        y=df_time[value_col],
                        mode='lines',
                        name='Original',
                        line=dict(color='lightgray', width=1),
                        opacity=0.5
                    ))

                    fig.add_trace(go.Scatter(
                        x=df_time[date_col],
                        y=df_time['media_movel'],
                        mode='lines',
                        name=f'Média Móvel {window} períodos',
                        line=dict(color='#FF4B4B', width=3)
                    ))

                    fig.update_layout(
                        title=f"{value_col} - Média Móvel (janela={window})",
                        xaxis_title="Data",
                        yaxis_title=value_col,
                        hovermode='x unified'
                    )

                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "📅 Agregação por Período":
                    period = st.selectbox(
                        "Agregar por:",
                        ["Dia", "Semana", "Mês", "Trimestre", "Ano"]
                    )

                    if period == "Dia":
                        df_agg = df_time.groupby(df_time[date_col].dt.date)[value_col].sum().reset_index()
                        df_agg.columns = [date_col, value_col]
                        titulo = f"{value_col} por Dia"
                    elif period == "Semana":
                        df_agg = df_time.groupby(df_time[date_col].dt.isocalendar().week)[value_col].sum().reset_index()
                        df_agg.columns = ['Semana', value_col]
                        titulo = f"{value_col} por Semana"
                    elif period == "Mês":
                        df_agg = df_time.groupby(df_time[date_col].dt.to_period('M'))[value_col].sum().reset_index()
                        df_agg[date_col] = df_agg[date_col].astype(str)
                        titulo = f"{value_col} por Mês"
                    elif period == "Trimestre":
                        df_agg = df_time.groupby(df_time[date_col].dt.to_period('Q'))[value_col].sum().reset_index()
                        df_agg[date_col] = df_agg[date_col].astype(str)
                        titulo = f"{value_col} por Trimestre"
                    else:
                        df_agg = df_time.groupby(df_time[date_col].dt.year)[value_col].sum().reset_index()
                        df_agg.columns = ['Ano', value_col]
                        titulo = f"{value_col} por Ano"

                    fig = px.bar(
                        df_agg,
                        x=df_agg.columns[0],
                        y=value_col,
                        title=titulo,
                        color=value_col,
                        color_continuous_scale='Viridis'
                    )

                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "📊 Sazonalidade":
                    st.markdown("""
                    **Análise de Sazonalidade** identifica padrões que se repetem em determinados períodos.
                    """)

                    df_temp = df_time.copy()
                    df_temp['mês'] = df_temp[date_col].dt.month
                    df_temp['ano'] = df_temp[date_col].dt.year
                    df_temp['dia_semana'] = df_temp[date_col].dt.day_name()

                    meses = {
                        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
                        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
                    }
                    df_temp['mês_nome'] = df_temp['mês'].map(meses)

                    tab1, tab2 = st.tabs(["📅 Sazonalidade Mensal", "📆 Sazonalidade por Dia da Semana"])

                    with tab1:
                        monthly_avg = df_temp.groupby('mês_nome')[value_col].mean().reset_index()
                        ordem_meses = list(meses.values())
                        monthly_avg['mês_nome'] = pd.Categorical(monthly_avg['mês_nome'], categories=ordem_meses,
                                                                 ordered=True)
                        monthly_avg = monthly_avg.sort_values('mês_nome')

                        fig1 = px.line(
                            monthly_avg,
                            x='mês_nome',
                            y=value_col,
                            title="Sazonalidade Mensal (média por mês)",
                            markers=True
                        )
                        st.plotly_chart(fig1, use_container_width=True)

                    with tab2:
                        dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                        dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
                        dia_map = dict(zip(dias_semana, dias_pt))

                        weekday_avg = df_temp.groupby('dia_semana')[value_col].mean().reset_index()
                        weekday_avg['dia_pt'] = weekday_avg['dia_semana'].map(dia_map)

                        weekday_avg['dia_pt'] = pd.Categorical(weekday_avg['dia_pt'], categories=dias_pt, ordered=True)
                        weekday_avg = weekday_avg.sort_values('dia_pt')

                        fig2 = px.bar(
                            weekday_avg,
                            x='dia_pt',
                            y=value_col,
                            title="Média por Dia da Semana",
                            color=value_col,
                            color_continuous_scale='Blues'
                        )
                        st.plotly_chart(fig2, use_container_width=True)

                # Botão para download
                if st.button("📥 Download Dados da Série Temporal"):
                    csv = df_time[[date_col, value_col]].to_csv(index=False)
                    st.download_button(
                        label="Clique para baixar CSV",
                        data=csv,
                        file_name=f"serie_temporal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )

            else:
                st.warning("⚠️ Nenhuma coluna numérica encontrada para análise temporal.")
                st.info("Para análise de séries temporais, é necessário ter pelo menos uma coluna numérica.")

        else:
            st.warning("⚠️ Nenhuma coluna de data encontrada no dataset.")

            # Oferecer opção de converter uma coluna
            st.subheader("🔄 Converter coluna para data")

            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            if text_cols:
                st.markdown("Algumas colunas de texto podem conter datas. Tente converter:")

                convert_col = st.selectbox("Selecione uma coluna para tentar converter:", text_cols)

                if st.button("🔄 Tentar converter para data"):
                    try:
                        sample = df[convert_col].dropna().iloc[0] if len(df) > 0 else ""
                        test_date = pd.to_datetime(sample)

                        st.success(f"✅ A coluna '{convert_col}' parece conter datas válidas!")
                        st.info(
                            "💡 Para usar esta coluna como data, recarregue o arquivo ou processe os dados antes do upload.")

                    except:
                        st.error(f"❌ A coluna '{convert_col}' não pôde ser convertida para data.")
            else:
                st.info("💡 Não há colunas de texto que possam conter datas.")
    else:
        st.warning("⚠️ Nenhum dado carregado. Vá para '📤 Upload de Dados' primeiro.")

# Página Correlações e Relacionamentos - COMPLETA!
elif page == "📊 Correlações e Relacionamentos":
    st.header("📊 Análise de Correlações e Relacionamentos")

    if st.session_state.data is not None:
        df = st.session_state.data

        # Detectar tipos de colunas
        col_types = detect_column_types(df)

        # Verificar se há colunas numéricas
        if len(col_types['all_numeric']) >= 2:
            st.subheader("📈 Matriz de Correlação")

            # Opções de visualização
            col1, col2 = st.columns([2, 1])

            with col1:
                # Selecionar colunas para correlação
                selected_cols = st.multiselect(
                    "Selecione as colunas para análise de correlação",
                    col_types['all_numeric'],
                    default=col_types['all_numeric'][:min(6, len(col_types['all_numeric']))]
                )

            with col2:
                st.markdown("### ℹ️ Sobre Correlações")
                st.markdown("""
                - **> 0.7**: Forte correlação positiva
                - **< -0.7**: Forte correlação negativa
                - **0.3 a 0.7**: Correlação moderada
                - **< 0.3**: Correlação fraca
                """)

            if len(selected_cols) >= 2:
                # Calcular matriz de correlação
                corr_matrix = df[selected_cols].corr()

                # Heatmap de correlação
                fig = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale='RdBu_r',
                    title="Matriz de Correlação",
                    zmin=-1, zmax=1
                )
                st.plotly_chart(fig, use_container_width=True)

                # Tabela de correlações detalhada
                st.subheader("📊 Detalhamento das Correlações")

                # Preparar dados para tabela
                corr_pairs = []
                for i in range(len(selected_cols)):
                    for j in range(i + 1, len(selected_cols)):
                        corr_value = corr_matrix.iloc[i, j]
                        strength, emoji = interpret_correlation(corr_value)
                        direction = "positiva" if corr_value > 0 else "negativa"

                        corr_pairs.append({
                            'Variável 1': selected_cols[i],
                            'Variável 2': selected_cols[j],
                            'Correlação': round(corr_value, 4),
                            'Direção': direction,
                            'Intensidade': strength,
                            'Interpretação': f"{emoji} {strength} {direction}"
                        })

                # Ordenar por valor absoluto da correlação
                corr_df = pd.DataFrame(corr_pairs)
                corr_df['|Correlação|'] = abs(corr_df['Correlação'])
                corr_df = corr_df.sort_values('|Correlação|', ascending=False).drop('|Correlação|', axis=1)

                st.dataframe(corr_df, use_container_width=True)

                # Gráfico de dispersão para pares selecionados
                st.subheader("🔄 Gráfico de Dispersão para Pares Selecionados")

                if len(selected_cols) >= 2:
                    col1 = st.selectbox("Selecione a primeira variável", selected_cols, key='scatter1')
                    col2 = st.selectbox("Selecione a segunda variável", [c for c in selected_cols if c != col1],
                                        key='scatter2')

                    fig = px.scatter(
                        df,
                        x=col1,
                        y=col2,
                        title=f"{col1} x {col2}",
                        opacity=0.6,
                        trendline="ols" if st.checkbox("Adicionar linha de tendência") else None
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Estatísticas da correlação
                    corr_val = df[col1].corr(df[col2])
                    st.info(f"📊 Correlação entre {col1} e {col2}: **{corr_val:.4f}**")
            else:
                st.warning("⚠️ Selecione pelo menos 2 colunas para visualizar correlações")

        elif len(col_types['all_numeric']) == 1:
            st.warning(
                "⚠️ Apenas uma coluna numérica encontrada. São necessárias pelo menos 2 colunas numéricas para análise de correlação.")
            st.info(f"Coluna numérica disponível: {col_types['all_numeric'][0]}")
        else:
            st.warning("⚠️ Nenhuma coluna numérica encontrada no dataset.")
            st.info("Para análise de correlação, carregue dados com colunas numéricas.")

        # Se houver colunas categóricas, mostrar análise de associação
        if col_types['categorical'] and SCIPY_AVAILABLE:
            st.subheader("📊 Associação entre Variáveis Categóricas")

            if len(col_types['categorical']) >= 2:
                cat1 = st.selectbox("Primeira variável categórica", col_types['categorical'], key='cat1')
                cat2 = st.selectbox("Segunda variável categórica", [c for c in col_types['categorical'] if c != cat1],
                                    key='cat2')

                # Tabela de contingência
                contingency = pd.crosstab(df[cat1], df[cat2])

                st.write("**Tabela de Contingência:**")
                st.dataframe(contingency, use_container_width=True)

                # Teste qui-quadrado
                chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

                st.write(f"**Teste Qui-quadrado:**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Estatística χ²", f"{chi2:.4f}")
                with col2:
                    st.metric("Graus de Liberdade", dof)
                with col3:
                    st.metric("Valor p", f"{p_value:.4f}")

                if p_value < 0.05:
                    st.success(f"✅ Há associação significativa entre {cat1} e {cat2} (p < 0.05)")
                else:
                    st.warning(f"⚠️ Não há evidência de associação significativa (p >= 0.05)")

            elif SCIPY_AVAILABLE:
                st.info("💡 Selecione pelo menos 2 colunas categóricas para análise de associação")

        elif col_types['categorical'] and not SCIPY_AVAILABLE:
            st.info("💡 Instale scipy para análise de associação entre variáveis categóricas: `pip install scipy`")
    else:
        st.warning("⚠️ Nenhum dado carregado. Vá para '📤 Upload de Dados' primeiro.")

# Página Relatórios Automáticos
elif page == "📋 Relatórios Automáticos":
    st.header("📋 Relatórios Automáticos")

    if st.session_state.data is not None:
        df = st.session_state.data

        st.subheader("📊 Resumo Executivo")

        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Registros", f"{df.shape[0]:,}")
        with col2:
            st.metric("Total Colunas", df.shape[1])
        with col3:
            st.metric("Memória", f"{df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")
        with col4:
            completude = (1 - df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
            st.metric("Completude", f"{completude:.1f}%")

        # Top 5 maiores correlações
        col_types = detect_column_types(df)
        if len(col_types['numeric']) > 1:
            st.subheader("🔗 Principais Correlações")
            corr = df[col_types['numeric']].corr().unstack().reset_index()
            corr.columns = ['Var1', 'Var2', 'Correlação']
            corr = corr[corr['Var1'] != corr['Var2']]
            corr['Abs'] = abs(corr['Correlação'])
            corr = corr.sort_values('Abs', ascending=False).drop_duplicates(subset=['Correlação']).head(10)

            st.dataframe(corr[['Var1', 'Var2', 'Correlação']], use_container_width=True)

        # Top categorias
        if col_types['categorical']:
            st.subheader("📝 Top Categorias")
            for col in col_types['categorical'][:3]:
                top = df[col].value_counts().head(5)
                st.write(f"**{col}:**")
                st.dataframe(top.reset_index(), use_container_width=True)

        # Botão para gerar relatório
        if st.button("📥 Gerar Relatório Completo"):
            report_lines = []
            report_lines.append("=" * 60)
            report_lines.append(f"RELATÓRIO DE ANÁLISE DE DADOS")
            report_lines.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            report_lines.append(f"Arquivo: {st.session_state.data_name}")
            report_lines.append("=" * 60)
            report_lines.append("")
            report_lines.append("RESUMO GERAL")
            report_lines.append("-" * 40)
            report_lines.append(f"Linhas: {df.shape[0]:,}")
            report_lines.append(f"Colunas: {df.shape[1]}")
            report_lines.append(f"Memória: {df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")
            report_lines.append(f"Completude: {completude:.1f}%")

            report = "\n".join(report_lines)

            st.download_button(
                label="📥 Download Relatório",
                data=report,
                file_name=f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    else:
        st.warning("⚠️ Nenhum dado carregado")

# Página Banco de Dados
elif page == "💾 Banco de Dados":
    st.header("💾 Banco de Dados SQLite")

    # Listar tabelas
    tables = db.list_tables()

    if tables:
        st.subheader("📋 Tabelas Disponíveis")
        selected_table = st.selectbox("Selecione uma tabela:", tables)

        if selected_table:
            # Carregar dados da tabela
            df = db.sql_to_df(f"SELECT * FROM {selected_table} LIMIT 1000")

            # Mostrar informações
            col1, col2, col3 = st.columns(3)
            with col1:
                result = db.execute_query(f"SELECT COUNT(*) FROM {selected_table}")
                if isinstance(result, list) and len(result) > 0:
                    if isinstance(result[0], (list, tuple)) and len(result[0]) > 0:
                        count = result[0][0]
                    else:
                        count = 0
                else:
                    count = 0
                st.metric("Total Registros", f"{count:,}")
            with col2:
                st.metric("Colunas", df.shape[1])
            with col3:
                st.metric("Visualizando", f"{df.shape[0]:,} registros")

            # Mostrar dados
            st.dataframe(df, use_container_width=True)

            # Botões de ação
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Download CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Clique para baixar",
                        data=csv,
                        file_name=f"{selected_table}.csv",
                        mime="text/csv"
                    )
            with col2:
                if st.button("🗑️ Limpar tabela", type="primary"):
                    if st.checkbox("Confirmar exclusão de todos os dados?"):
                        db.execute_query(f"DELETE FROM {selected_table}")
                        st.success(f"✅ Tabela {selected_table} limpa!")
                        st.rerun()
    else:
        st.info("ℹ️ Nenhuma tabela encontrada no banco de dados.")

# Página Configurações
elif page == "⚙️ Configurações":
    st.header("⚙️ Configurações do Sistema")

    st.subheader("📁 Diretórios do Projeto")
    st.json({
        "data_dir": str(Settings.DATA_DIR),
        "raw_data": str(Settings.RAW_DATA_DIR),
        "processed_data": str(Settings.PROCESSED_DATA_DIR),
        "reports_dir": str(Settings.REPORTS_DIR)
    })

    st.subheader("🗄️ Banco de Dados")
    st.write(f"**SQLite Path:** {Settings.SQLITE_PATH}")
    if Settings.SQLITE_PATH.exists():
        size_mb = Settings.SQLITE_PATH.stat().st_size / (1024 * 1024)
        st.write(f"**Tamanho:** {size_mb:.2f} MB")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Criar Backup do Banco"):
            backup_path = db.backup_database()
            if backup_path:
                st.success(f"✅ Backup criado: {backup_path}")

    with col2:
        if st.button("🔄 Resetar Sessão"):
            for key in ['data', 'data_name', 'data_source', 'analysis_history']:
                if key in st.session_state:
                    st.session_state[key] = None if key != 'analysis_history' else []
            st.success("✅ Sessão resetada!")
            st.rerun()

    st.subheader("📊 Histórico de Análises")
    if st.session_state.analysis_history:
        for i, analysis in enumerate(st.session_state.analysis_history):
            with st.expander(f"Análise {i + 1}: {analysis['timestamp'].strftime('%d/%m/%Y %H:%M')}"):
                st.write(f"**Arquivo:** {analysis['data']}")
                st.write("**Insights:**")
                for insight in analysis['insights']:
                    st.write(f"- {insight}")
    else:
        st.info("Nenhuma análise salva no histórico")

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px;'>
        <p style='font-size: 1.1rem; font-weight: bold;'>Desenvolvido por <span style='color: #FF4B4B;'>Samuel Maia</span> - Analista de Dados Sênior</p>
        <p style='font-size: 0.9rem; color: #555;'>
            📧 smaia2@gmail.com | 
            🔗 linkedin.com/in/samuelmaiapro | 
            🐙 github.com/samuelmaiapro/portfolio-analista-dados
        </p>
        <p style='font-size: 0.8rem; color: #888;'>Python 3.14.2 | Streamlit 1.41.1 | Pandas 2.2.3 | Plotly 6.0.0</p>
        <p style='font-size: 0.8rem; color: #888;'>© 2025 - Todos os direitos reservados</p>
    </div>
    """,
    unsafe_allow_html=True
)