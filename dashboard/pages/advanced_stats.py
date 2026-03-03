"""Renderizacao da pagina de analise estatistica avancada."""

from __future__ import annotations


def _binary_candidates(df, categorical_cols, numeric_col):
    """Retorna colunas categoricas com exatamente 2 grupos e amostras minimas."""
    candidates = []
    details = {}

    for col in categorical_cols:
        valid = df[[col, numeric_col]].dropna()
        if valid.empty:
            continue

        counts = valid[col].value_counts()
        if len(counts) != 2:
            continue

        if counts.min() < 2:
            continue

        groups = counts.index.tolist()
        candidates.append(col)
        details[col] = {
            "groups": groups,
            "counts": counts.to_dict(),
            "n_total": int(len(valid)),
        }

    return candidates, details


def render_advanced_stats_page(
    st,
    pd,
    np,
    px,
    go,
    datetime,
    db,
    settings,
    scipy_available,
    stats,
    detect_column_types,
    get_basic_stats,
    interpret_correlation,
):
    st.header("Analise Estatistica Avancada")

    if not scipy_available:
        st.warning(
            "Biblioteca 'scipy' nao esta instalada. Para testes estatisticos: `pip install scipy`."
        )
        st.info("As outras funcionalidades do dashboard continuam disponiveis.")
        return

    if st.session_state.data is None:
        st.warning("Nenhum dado carregado.")
        return

    df = st.session_state.data
    col_types = detect_column_types(df)
    numeric_cols = col_types["numeric"]
    categorical_cols = col_types["categorical"]

    if not numeric_cols:
        st.warning("Sao necessarias colunas numericas para testes estatisticos.")
        return

    test_type = st.selectbox(
        "Selecione o teste estatistico",
        [
            "Teste t (comparacao de medias)",
            "ANOVA (analise de variancia)",
            "Correlacao de Pearson",
            "Correlacao de Spearman",
        ],
        key="adv_test_type",
    )

    if test_type == "Teste t (comparacao de medias)":
        if not categorical_cols:
            st.warning("Nao ha colunas categoricas para o Teste t.")
            return

        num_col = st.selectbox("Variavel numerica", numeric_cols, key="adv_ttest_numeric")
        binary_cols, details = _binary_candidates(df, categorical_cols, num_col)

        if not binary_cols:
            st.warning(
                "Nao ha coluna categorica binaria valida (2 grupos com pelo menos 2 amostras cada)."
            )
            st.caption("Dica: para colunas com muitos grupos (ex.: ORDERDATE), use ANOVA.")
            return

        labels = []
        label_to_col = {}
        for col in binary_cols:
            groups = details[col]["groups"]
            counts = details[col]["counts"]
            label = f"{col} ({groups[0]}: {counts[groups[0]]}, {groups[1]}: {counts[groups[1]]})"
            labels.append(label)
            label_to_col[label] = col

        selected_label = st.selectbox(
            "Variavel categorica (2 grupos)",
            labels,
            key="adv_ttest_categorical",
        )
        cat_col = label_to_col[selected_label]

        valid = df[[cat_col, num_col]].dropna()
        groups = valid[cat_col].value_counts().index.tolist()
        group1 = valid[valid[cat_col] == groups[0]][num_col]
        group2 = valid[valid[cat_col] == groups[1]][num_col]

        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

        st.subheader("Resultado do Teste t (Welch)")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Grupo 1", str(groups[0]))
        with c2:
            st.metric("n Grupo 1", int(len(group1)))
        with c3:
            st.metric("Grupo 2", str(groups[1]))
        with c4:
            st.metric("n Grupo 2", int(len(group2)))

        m1, m2 = st.columns(2)
        with m1:
            st.metric("Estatistica t", f"{t_stat:.4f}")
        with m2:
            st.metric("Valor p", f"{p_value:.4f}")

        if p_value < 0.05:
            st.success("Ha diferenca estatisticamente significativa entre os grupos (p < 0.05).")
        else:
            st.info("Nao foi detectada diferenca estatisticamente significativa (p >= 0.05).")
        return

    if test_type == "ANOVA (analise de variancia)":
        if not categorical_cols:
            st.warning("Nao ha colunas categoricas para ANOVA.")
            return

        cat_col = st.selectbox("Variavel categorica", categorical_cols, key="adv_anova_categorical")
        num_col = st.selectbox("Variavel numerica", numeric_cols, key="adv_anova_numeric")

        groups = []
        for _, group in df[[cat_col, num_col]].dropna().groupby(cat_col)[num_col]:
            if len(group) > 1:
                groups.append(group)

        if len(groups) < 2:
            st.warning("A variavel categorica precisa ter pelo menos 2 grupos com dados suficientes.")
            return

        f_stat, p_value = stats.f_oneway(*groups)
        st.subheader("Resultado da ANOVA")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Estatistica F", f"{f_stat:.4f}")
        with c2:
            st.metric("Valor p", f"{p_value:.4f}")

        if p_value < 0.05:
            st.success("Ha diferenca estatisticamente significativa entre os grupos (p < 0.05).")
        else:
            st.info("Nao foi detectada diferenca estatisticamente significativa (p >= 0.05).")
        return

    if len(numeric_cols) < 2:
        st.warning("Sao necessarias pelo menos 2 colunas numericas para correlacao.")
        return

    var_1 = st.selectbox("Variavel 1", numeric_cols, key="adv_corr_var1")
    var_2 = st.selectbox(
        "Variavel 2",
        [c for c in numeric_cols if c != var_1],
        key="adv_corr_var2",
    )

    paired = df[[var_1, var_2]].dropna()
    if len(paired) < 3:
        st.warning("Amostra insuficiente apos remover faltantes para calcular correlacao.")
        return

    if test_type == "Correlacao de Pearson":
        corr, p_value = stats.pearsonr(paired[var_1], paired[var_2])
        test_name = "Pearson"
    else:
        corr, p_value = stats.spearmanr(paired[var_1], paired[var_2])
        test_name = "Spearman"

    st.subheader(f"Resultado da Correlacao de {test_name}")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Correlacao", f"{corr:.4f}")
    with c2:
        st.metric("Valor p", f"{p_value:.4f}")
    with c3:
        st.metric("N amostras", int(len(paired)))

    strength, emoji = interpret_correlation(corr)
    direction = "positiva" if corr > 0 else "negativa"
    st.info(f"{emoji} Correlacao {direction} ({strength}).")

    if p_value < 0.05:
        st.success("Correlacao estatisticamente significativa (p < 0.05).")
    else:
        st.info("Correlacao nao significativa (p >= 0.05).")
