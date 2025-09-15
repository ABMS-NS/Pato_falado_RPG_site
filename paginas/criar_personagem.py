import streamlit as st
from models.personagem import Personagem
from paginas.stats_persona.CRIS import pagina_de_ficha
import io


def criar_personagem(memory):
    # ---
    # Lógica para gerenciar as barras de status
    # ---
    if "num_barras" not in st.session_state:
        st.session_state.num_barras = 1

    def adicionar_barra():
        st.session_state.num_barras += 1

    def remover_barra():
        if st.session_state.num_barras > 1:
            st.session_state.num_barras -= 1

    # ---
    # Verifica se o personagem já foi criado
    # ---
    if "personagem" in st.session_state:
        # Se o personagem já existe na sessão, exibe a página de ficha
        pagina_de_ficha(st.session_state.personagem)

    else:
        # Caso contrário, exibe o formulário de criação
        st.title("Criação de Personagem")
        st.markdown("---")

        # Controles para adicionar/remover barras (MOVIDOS PARA FORA DO FORM)
        col1, col2 = st.columns(2)
        with col1:
            st.button("Adicionar Barra", on_click=adicionar_barra)
        with col2:
            st.button("Remover Barra", on_click=remover_barra)

        with st.form("form_personagem"):
            # Campo para o nome
            nome = st.text_input("Nome do Personagem")

            # Campo para a imagem
            imagem_bytes = st.file_uploader("Escolha uma imagem para o personagem", type=["png", "jpg", "jpeg"])

            st.markdown("---")
            st.subheader("Barras de Status")

            barras_inputs = []
            for i in range(st.session_state.num_barras):
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

                # Armazena o personagem na memória para o escudo do mestre
                memory.personagens.append(personagem)
                
                # Armazena o personagem na sessão para uso posterior
                st.session_state.personagem = personagem
                st.session_state.current_page = "ficha"
                st.rerun()