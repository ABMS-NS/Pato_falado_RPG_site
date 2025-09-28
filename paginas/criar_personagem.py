import streamlit as st
from models.personagem import Personagem
import io


def criar_personagem(memory):
    # Número de barras individual por usuário
    if "num_barras" not in st.session_state:
        st.session_state.num_barras = 1

    def adicionar_barra():
        st.session_state.num_barras += 1

    def remover_barra():
        if st.session_state.num_barras > 1:
            st.session_state.num_barras -= 1
    st.title("Criação de Personagem")
    st.markdown("---")

    # Controles para adicionar/remover barras usando estado global
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Adicionar Barra"):
            adicionar_barra()
            st.rerun()
    with col2:
        if st.button("Remover Barra"):
            remover_barra()
            st.rerun()

    num_barras_atual = st.session_state.num_barras

    with st.form("form_personagem"):
        # Campo para o nome
        nome = st.text_input("Nome do Personagem")

        # Campo para a imagem
        imagem_bytes = st.file_uploader("Escolha uma imagem para o personagem", type=["png", "jpg", "jpeg"])

        st.markdown("---")
        st.subheader("Barras de Status")

        barras_inputs = []
        for i in range(num_barras_atual):
            st.markdown(f"**Barra #{i+1}**")
            with st.container(border=True):
                col_b1, col_b2, col_b3 = st.columns(3)
                with col_b1:
                    nome_barra = st.text_input("Nome da barra", key=f"barra_nome_{i}")
                with col_b2:
                    atual = st.number_input("Valor Atual", min_value=0, value=0, key=f"barra_atual_{i}")
                with col_b3:
                    maximo = st.number_input("Valor Máximo", min_value=1, value=100, key=f"barra_maximo_{i}")
                barras_inputs.append({"nome": nome_barra, "atual": atual, "maximo": maximo})
        
        st.markdown("---")
        submitted = st.form_submit_button("Criar Personagem")

    if submitted:
        if not nome:
            st.error("Por favor, insira o nome do personagem.")
        elif not imagem_bytes:
            st.error("Por favor, faça o upload de uma imagem.")
        else:
            # Cria a URL da imagem a partir dos bytes
            imagem_url = io.BytesIO(imagem_bytes.read())

            # Cria o objeto Personagem
            personagem = Personagem(nome, imagem_url)
            
            # Adiciona as barras de status ao personagem
            for barra in barras_inputs:
                if barra["nome"]:
                    personagem.adicionar_barra(barra["nome"], barra["atual"], barra["maximo"])

            # Armazena o personagem na memória global (compartilhada)
            memory.personagens.append(personagem)
            
            # Reseta o número de barras para o próximo personagem (individual)
            st.session_state.num_barras = 1
            
            # Vai para a ficha do personagem criado (navegação individual)
            st.session_state.personagem_selecionado = personagem
            st.session_state.current_page = "ficha"
            st.rerun()
            
    # Botão para voltar
    if st.button("Voltar para a Home"):
        st.session_state.current_page = "home"
        st.rerun()