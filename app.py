import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Ações Brasileiras 2025",
    page_icon="📈",
    layout="wide",
)

TICKERS = {
    "Petrobras (PETR4)": "PETR4.SA",
    "Itaú (ITUB4)": "ITUB4.SA",
    "Vale (VALE3)": "VALE3.SA",
}

CORES = {
    "Petrobras (PETR4)": "#009c3b",
    "Itaú (ITUB4)": "#003087",
    "Vale (VALE3)": "#e4002b",
}

st.title("📈 Dashboard de Ações Brasileiras — 2025")
st.markdown("Análise comparativa de **Petrobras**, **Itaú** e **Vale** na B3.")

with st.sidebar:
    st.header("Filtros")
    data_inicio = st.date_input(
        "Data de início",
        value=date(2025, 1, 2),
        min_value=date(2025, 1, 2),
        max_value=date.today(),
    )
    data_fim = st.date_input(
        "Data de fim",
        value=date.today(),
        min_value=date(2025, 1, 2),
        max_value=date.today(),
    )
    st.markdown("---")
    st.subheader("Ações")
    selecao = {nome: st.checkbox(nome, value=True) for nome in TICKERS}

acoes_selecionadas = [nome for nome, ativo in selecao.items() if ativo]

if not acoes_selecionadas:
    st.warning("Selecione ao menos uma ação na barra lateral.")
    st.stop()

if data_inicio >= data_fim:
    st.error("A data de início deve ser anterior à data de fim.")
    st.stop()


@st.cache_data(ttl=3600)
def carregar_dados(tickers: list[str], inicio: str, fim: str) -> pd.DataFrame:
    raw = yf.download(tickers, start=inicio, end=fim, auto_adjust=True, progress=False)
    if isinstance(raw.columns, pd.MultiIndex):
        close = raw["Close"]
    else:
        close = raw[["Close"]]
        close.columns = tickers
    return close.dropna(how="all")


tickers_selecionados = [TICKERS[n] for n in acoes_selecionadas]
dados = carregar_dados(tickers_selecionados, str(data_inicio), str(data_fim))

if dados.empty:
    st.error("Nenhum dado encontrado para o período selecionado.")
    st.stop()

aba1, aba2, aba3 = st.tabs(["💰 Cotação (R$)", "📊 Performance (%)", "📦 Volume"])

with aba1:
    fig = go.Figure()
    for nome in acoes_selecionadas:
        ticker = TICKERS[nome]
        if ticker in dados.columns:
            fig.add_trace(
                go.Scatter(
                    x=dados.index,
                    y=dados[ticker],
                    name=nome,
                    line=dict(color=CORES[nome], width=2),
                    hovertemplate="%{y:.2f} R$<extra>" + nome + "</extra>",
                )
            )
    fig.update_layout(
        title="Preço de Fechamento Ajustado",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

with aba2:
    fig2 = go.Figure()
    for nome in acoes_selecionadas:
        ticker = TICKERS[nome]
        if ticker in dados.columns:
            serie = dados[ticker].dropna()
            if len(serie) > 0:
                performance = (serie / serie.iloc[0] - 1) * 100
                fig2.add_trace(
                    go.Scatter(
                        x=performance.index,
                        y=performance,
                        name=nome,
                        line=dict(color=CORES[nome], width=2),
                        hovertemplate="%{y:.2f}%<extra>" + nome + "</extra>",
                    )
                )
    fig2.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig2.update_layout(
        title="Retorno Acumulado desde o Início do Período",
        xaxis_title="Data",
        yaxis_title="Performance (%)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500,
    )
    st.plotly_chart(fig2, use_container_width=True)

with aba3:

    @st.cache_data(ttl=3600)
    def carregar_volume(tickers: list[str], inicio: str, fim: str) -> pd.DataFrame:
        raw = yf.download(
            tickers, start=inicio, end=fim, auto_adjust=True, progress=False
        )
        if isinstance(raw.columns, pd.MultiIndex):
            return raw["Volume"].dropna(how="all")
        vol = raw[["Volume"]]
        vol.columns = tickers
        return vol.dropna(how="all")

    volume = carregar_volume(tickers_selecionados, str(data_inicio), str(data_fim))
    fig3 = go.Figure()
    for nome in acoes_selecionadas:
        ticker = TICKERS[nome]
        if ticker in volume.columns:
            fig3.add_trace(
                go.Bar(
                    x=volume.index,
                    y=volume[ticker],
                    name=nome,
                    marker_color=CORES[nome],
                    opacity=0.8,
                    hovertemplate="%{y:,.0f}<extra>" + nome + "</extra>",
                )
            )
    fig3.update_layout(
        title="Volume Diário Negociado",
        xaxis_title="Data",
        yaxis_title="Volume",
        barmode="group",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=500,
    )
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.subheader("Resumo do Período")

resumo_linhas = []
for nome in acoes_selecionadas:
    ticker = TICKERS[nome]
    if ticker in dados.columns:
        serie = dados[ticker].dropna()
        if len(serie) > 0:
            preco_atual = serie.iloc[-1]
            preco_inicio = serie.iloc[0]
            variacao = (preco_atual / preco_inicio - 1) * 100
            resumo_linhas.append(
                {
                    "Ação": nome,
                    "Preço Atual (R$)": f"{preco_atual:.2f}",
                    "Preço Início (R$)": f"{preco_inicio:.2f}",
                    "Variação no Período": f"{variacao:+.2f}%",
                    "Mínima (R$)": f"{serie.min():.2f}",
                    "Máxima (R$)": f"{serie.max():.2f}",
                }
            )

if resumo_linhas:
    df_resumo = pd.DataFrame(resumo_linhas).set_index("Ação")
    st.dataframe(df_resumo, use_container_width=True)

st.caption("Dados: Yahoo Finance via yfinance | Atualizado a cada 1 hora")
