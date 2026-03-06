import streamlit as st
import httpx # Para fazer as requisições para a nossa própria API

# O endereço da api
API_URL = "http://127.0.0.1:8001/imoveis"

st.set_page_config(page_title="Imóveis", page_icon="🏢", layout="wide")

st.title("🏢 Gestão de Imóveis")
st.markdown("Dashboard rápido consumindo a API construída em FastAPI.")

# Dividindo a tela em 2 colunas
col1, col2 = st.columns([1, 2])

# coluna 1 formulario de cadastro
with col1:
    st.header("Cadastrar Novo Imóvel")
    with st.form("form_imovel", clear_on_submit=True):
        titulo = st.text_input("Título", placeholder="Ex: Apto 2 quartos no Centro")
        descricao = st.text_area("Descrição (Opcional)")
        preco = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
        
        # Colocando campos menores lado a lado
        c1, c2, c3 = st.columns(3)
        quartos = c1.number_input("Quartos", min_value=0, step=1)
        banheiros = c2.number_input("Banheiros", min_value=0, step=1)
        vagas = c3.number_input("Vagas", min_value=0, step=1)

        submit = st.form_submit_button("Salvar Imóvel", width="stretch")


        if submit:
            if not titulo or preco <= 0:
                st.error("Título e Preço são obrigatórios e maiores que zero!")
            else:
                novo_imovel = {
                    "titulo": titulo,
                    "descricao": descricao,
                    "preco": preco,
                    "quartos": quartos,
                    "banheiros": banheiros,
                    "vagas_garagem": vagas
                }
                # Manda o POST para nossa API FastAPI
                response = httpx.post(API_URL, json=novo_imovel)
                
                if response.status_code == 200:
                    st.success(f"Sucesso! Imóvel criado com ID: {response.json()['id']}")
                else:
                    st.error("Erro ao cadastrar imóvel na API.")

# coluna 2 lista dos imoveis
with col2:
    st.header("Lista de Imóveis (Banco de Dados)")
    
    if st.button("Atualizar Lista"):
        pass # Quando o botão for clicado, o Streamlit vai re-renderizar a tela e puxar de novo
        
    try:
        # Puxa a lista (GET) do FastAPI
        response = httpx.get(API_URL)
        if response.status_code == 200:
            imoveis = response.json()
            
            if imoveis:
                # O Streamlit transforma dicionários/listas em tabela 
                st.dataframe(
                    imoveis, 
                    column_config={
                        "preco": st.column_config.NumberColumn("Valor R$", format="R$ %.2f")
                    },
                    width="stretch",
                    hide_index=True
                )
            else:
                st.info("Nenhum imóvel cadastrado ainda.")
        else:
            st.error("A API não retornou 200 OK.")
    except httpx.ConnectError:
        st.error("Não foi possível conectar na API")
