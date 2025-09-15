import streamlit as st
from models.efeito import Efeito
from models.personagem import *
# ------------------------
# Criando o personagem
# ------------------------
def pagina_de_ficha(p: Personagem):

    # ------------------------
    # Layout em colunas
    # ------------------------
    st.title("Ficha do Personagem")

    col1, col2 = st.columns([5, 7])

    with col1:
        st.image(p.imagem, caption=p.nome, width='stretch')

    with col2:
        st.header(p.nome)

        for barra in p.barras:

            # input com setinhas ↑↓
            novo_valor = st.number_input(
                f"{barra['nome']}",
                min_value=0,
                value=barra["atual"],
                step=1
            )

            # Atualiza o valor da barra
            barra["atual"] = novo_valor

            # Barra de progresso
            st.progress(min(barra["atual"] / barra["maximo"], 1.0))

    st.markdown("---")
    st.subheader("Efeitos ativos")
    for efeito in p.efeitos:
        st.write(f"- **{efeito.nome}** - {efeito.duracao} turnos")

    
    with st.expander("Gerenciar Efeitos"):

        if p.efeitos:
            efeito_para_remover = st.selectbox(
            "Selecione um efeito para remover:",
            options=[e.nome for e in p.efeitos],
            index=None,
            placeholder="Escolha um efeito..."
        )
            if st.button("Remover Efeito Selecionado"):
                if efeito_para_remover:
                    p.efeitos = [e for e in p.efeitos if e.nome != efeito_para_remover]
                    st.success(f"Efeito '{efeito_para_remover}' removido!")
                    st.rerun()
        
        novo_efeito = st.text_input("Adicionar novo efeito (digite o nome):")
        duração_efeito = st.number_input("Duração do efeito (em turnos):", min_value=1, value=1, step=1)
        if st.button("Adicionar Efeito"):
            if novo_efeito:
                p.efeitos.append(Efeito(novo_efeito, duração_efeito))
                st.rerun()
            else:
                st.warning("Por favor, insira um nome para o efeito.")

    if st.button("Voltar para a Home"):
        del st.session_state.personagem  # Remove o personagem da sessão
        st.session_state.current_page = "home"
        st.rerun()

    if st.button("Deletar Personagem"):
        del st.session_state.personagem  # Remove o personagem da sessão
        st.session_state.current_page = "home"
        # Remove o personagem da memória também
        st.session_state.memory.personagens = [char for char in st.session_state.memory.personagens if char.nome != p.nome]
        st.rerun()