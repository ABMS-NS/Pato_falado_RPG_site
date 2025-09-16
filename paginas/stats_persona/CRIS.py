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
                step=1,
                key=f"{p.nome}_{barra['nome']}_input"
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
            placeholder="Escolha um efeito...",
            key=f"{p.nome}_remover_efeito"
        )
            if st.button("Remover Efeito Selecionado", key=f"{p.nome}_btn_remover"):
                if efeito_para_remover:
                    p.efeitos = [e for e in p.efeitos if e.nome != efeito_para_remover]
                    st.success(f"Efeito '{efeito_para_remover}' removido!")
                    st.rerun()
        
        novo_efeito = st.text_input("Adicionar novo efeito (digite o nome):", key=f"{p.nome}_novo_efeito")
        duracao_efeito = st.number_input("Duração do efeito (em turnos):", min_value=1, value=1, step=1, key=f"{p.nome}_duracao")
        if st.button("Adicionar Efeito", key=f"{p.nome}_btn_adicionar"):
            if novo_efeito:
                p.efeitos.append(Efeito(novo_efeito, duracao_efeito))
                st.rerun()
            else:
                st.warning("Por favor, insira um nome para o efeito.")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Voltar para a Home", key=f"{p.nome}_voltar_home"):
            st.session_state.current_page = "home"
            st.rerun()
    
    with col2:
        if st.button("Deletar Personagem", key=f"{p.nome}_deletar", type="secondary"):
            # Remove o personagem da memória global compartilhada
            from models.memory import Memory
            memory_instance = Memory()
            memory_instance.personagens = [char for char in memory_instance.personagens if char.nome != p.nome]
            st.session_state.current_page = "home"
            st.rerun()