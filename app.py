import streamlit as st
from models.memory import Memory
from paginas.criar_personagem import criar_personagem
from paginas.stats_persona.CRIS import pagina_de_ficha
from paginas.iniciativa import pagina_iniciativa


# Initialize memory and session state
if "memory" not in st.session_state:
    st.session_state.memory = Memory()
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"


def main_page():
    st.title("Bem-vindo ao Gerenciador de Personagens")
    st.markdown("---")
    st.subheader("O que você gostaria de fazer?")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Criar Novo Personagem"):
            st.session_state.current_page = "criar"
            st.rerun()
    with col2:
        if st.button("Ver Personagens Existentes"):
            st.session_state.current_page = "ver"
            st.rerun()
    with col3:
        if st.button("Gerenciar Iniciativa"):
            st.session_state.current_page = "iniciativa"
            st.rerun()

def view_characters_page():
    st.title("Personagens Existentes")
    st.markdown("---")

    if not st.session_state.memory.personagens:
        st.info("Nenhum personagem foi criado ainda.")
    else:
        for personagem in st.session_state.memory.personagens:
            col1, col2, col3= st.columns([0.3, 1, 1])
            with col1:
                st.image(personagem.imagem,width=100)
                
            with col2:
                st.subheader(personagem.nome)
            with col3:
                if st.button(f"Ver Ficha de {personagem.nome}"):
                    st.session_state.personagem = personagem
                    st.session_state.current_page = "ficha"
                    st.rerun()
            # You can add more details here if needed

    if st.button("Voltar para a Home"):
        st.session_state.current_page = "home"
        st.rerun()

# Page routing logic
if st.session_state.current_page == "home":
    main_page()
elif st.session_state.current_page == "criar":
    # Pass the memory object to the character creation function
    criar_personagem(st.session_state.memory)
elif st.session_state.current_page == "ver":
    view_characters_page()
elif st.session_state.current_page == "ficha":
    if "personagem" in st.session_state:
        pagina_de_ficha(st.session_state.personagem)
elif st.session_state.current_page == "iniciativa":
    pagina_iniciativa(st.session_state.memory)