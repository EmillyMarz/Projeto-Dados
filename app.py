import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Análise de Dados de Saúde Global", layout="wide")
st.title("📊 Análise de Dados de Saúde Global")

arquivo = st.sidebar.file_uploader("Selecione a planilha Excel", type=["xlsx"])

if arquivo:
    df = pd.read_excel(arquivo)

    st.sidebar.markdown("## 🔍 Filtros")
    paises = st.sidebar.multiselect("Países", sorted(df["País"].unique()), default=None)
    ano_min, ano_max = int(df["Ano"].min()), int(df["Ano"].max())
    anos = st.sidebar.slider("Intervalo de Anos", ano_min, ano_max, (ano_min, ano_max))

    df_filtrado = df.copy()
    if paises:
        df_filtrado = df_filtrado[df_filtrado["País"].isin(paises)]
    df_filtrado = df_filtrado[(df_filtrado["Ano"] >= anos[0]) & (df_filtrado["Ano"] <= anos[1])]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🌍 Expectativa Média", f"{df_filtrado['Expectativa_de_vida'].mean():.1f} anos")
    col2.metric("👥 População Média", f"{df_filtrado['População'].mean():,.0f}")
    col3.metric("📚 Escolaridade Média", f"{df_filtrado['Escolaridade'].mean():.1f} anos")
    col4.metric("💰 PIB Médio", f"US$ {df_filtrado['PIB'].mean():,.2f}")

    aba1, aba2, aba3, aba4 = st.tabs([
        "📈 Visão Geral",
        "🦠 Indicadores de Saúde",
        "📚 Educação e Economia",
        "📋 Tabela de Dados"
    ])

    with aba1:
        st.subheader("📊 Expectativa de Vida ao Longo dos Anos")
        expectativa = df_filtrado.groupby("Ano")["Expectativa_de_vida"].mean()
        st.line_chart(expectativa)
        st.markdown(
            "Observe que a expectativa de vida tem variações ao longo dos anos, indicando possíveis melhorias ou desafios na saúde pública.")

    with aba2:
        col5, col6 = st.columns(2)

        with col5:
            st.markdown("### Casos de Sarampo")
            sarampo = df_filtrado.groupby("Ano")["Sarampo"].sum()
            # Gráfico de barras com cor azul suave
            fig, ax = plt.subplots()
            ax.bar(sarampo.index, sarampo.values, color='#5DADE2')
            ax.set_title("Casos de Sarampo")
            ax.set_xlabel("Ano")
            ax.set_ylabel("Total de Casos")
            st.pyplot(fig)

        with col6:
            st.markdown("### Vacinação contra Hepatite B")
            hep_b = df_filtrado.groupby("Ano")["Hepatite_B"].mean()
            # Gráfico de linha com cor verde água
            fig, ax = plt.subplots()
            ax.plot(hep_b.index, hep_b.values, color='#48C9B0', marker='o')
            ax.set_title("Vacinação Hepatite B")
            ax.set_xlabel("Ano")
            ax.set_ylabel("Média de Vacinação")
            st.pyplot(fig)

        st.markdown("### Poliomielite e HIV/AIDS")
        fig, ax = plt.subplots()
        df_grouped = df_filtrado.groupby("Ano")[["Poliomielite", "HIV/AIDS"]].mean()
        df_grouped.plot(ax=ax, color=['#F39C12', '#34495E'], linewidth=2)
        ax.set_title("Média Poliomielite e HIV/AIDS")
        ax.set_xlabel("Ano")
        ax.set_ylabel("Média")
        st.pyplot(fig)

    with aba3:
        col7, col8 = st.columns(2)

        with col7:
            st.markdown("### Escolaridade Média por Ano")
            escolaridade = df_filtrado.groupby("Ano")["Escolaridade"].mean()
            fig, ax = plt.subplots()
            cores_barras = ['#9B59B6'] * len(escolaridade)  # Roxo uniforme
            bars = ax.bar(escolaridade.index, escolaridade.values, color=cores_barras)
            ax.bar_label(bars, padding=3, fmt="%.1f")
            ax.set_title("Escolaridade Média ao Longo dos Anos")
            ax.set_xlabel("Ano")
            ax.set_ylabel("Escolaridade (anos)")
            st.pyplot(fig)

        with col8:
            st.markdown("### PIB Médio ao Longo dos Anos")
            pib = df_filtrado.groupby("Ano")["PIB"].mean()
            fig, ax = plt.subplots()
            ax.plot(pib.index, pib.values, color='#27AE60', marker='o', linestyle='-', linewidth=2)  # verde escuro
            ax.set_title("PIB Médio por Ano")
            ax.set_xlabel("Ano")
            ax.set_ylabel("PIB (US$)")
            st.pyplot(fig)

        st.markdown("### Composição de Renda Média")
        renda = df_filtrado.groupby("Ano")["Composição_de_renda"].mean()
        st.line_chart(renda)

    with aba4:
        st.markdown("### 🔢 Visualização da Tabela de Dados")
        pais_filtro = st.selectbox("Filtrar por País", ["Todos"] + sorted(df_filtrado["País"].unique()))
        if pais_filtro != "Todos":
            tabela = df_filtrado[df_filtrado["País"] == pais_filtro]
        else:
            tabela = df_filtrado
        st.dataframe(tabela)
else:
    st.error("⚠️ Por favor, carregue um arquivo Excel para iniciar a análise.")
