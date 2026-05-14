import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Configurações da página no celular
st.set_page_config(page_title="Meu Monitor B3", layout="centered")

st.title("📊 Monitor de Preços")

# --- BANCO DE DATOS SIMPLES (Nuvem usa st.session_state) ---
if 'carteira' not in st.session_state:
    st.session_state.carteira = []

# --- ÁREA DE CADASTRO ---
with st.expander("➕ Adicionar Novo Ativo"):
    ticker = st.text_input("Ticker (ex: PETR4.SA ou USDBRL=X)").upper()
    col1, col2 = st.columns(2)
    alvo = col1.number_input("Preço Alvo", step=0.01)
    seguranca = col2.number_input("Margem Segurança", step=0.01)
    
    if st.button("Salvar na Lista"):
        st.session_state.carteira.append({
            "ticker": ticker, "alvo": alvo, "seguranca": seguranca
        })
        st.success(f"{ticker} adicionado!")

# --- MONITORAMENTO ---
if st.session_state.carteira:
    st.subheader("Minhas Análises")
    
    if st.button("🔄 Atualizar Preços Agora"):
        tickers_list = [item['ticker'] for item in st.session_state.carteira]
        try:
            dados = yf.download(tickers_list, period="1d", interval="1m", progress=False)['Close']
            
            for item in st.session_state.carteira:
                t = item['ticker']
                # Pega o último preço
                if len(tickers_list) == 1:
                    preco_atual = dados.iloc[-1]
                else:
                    preco_atual = dados[t].iloc[-1]
                
                # Lógica de exibição (Cores)
                if preco_atual <= item['seguranca']:
                    st.metric(label=f"⭐ {t}", value=f"R$ {preco_atual:.2f}", delta="OPORTUNIDADE OURO", delta_color="normal")
                elif preco_atual <= item['alvo']:
                    st.metric(label=f"✅ {t}", value=f"R$ {preco_atual:.2f}", delta="Preço Alvo Atingido")
                else:
                    distancia = preco_atual - item['alvo']
                    st.metric(label=t, value=f"R$ {preco_atual:.2f}", delta=f"+ R$ {distancia:.2f}", delta_color="inverse")
                st.divider()
        except:
            st.error("Erro ao conectar com o mercado.")
else:
    st.info("Sua lista está vazia. Adicione ativos acima.")