import streamlit as st
from models.memory import Memory
from paginas.criar_personagem import criar_personagem
from paginas.stats_persona.CRIS import pagina_de_ficha
from paginas.iniciativa import pagina_iniciativa

# Initialize memory (global, compartilhado apenas para dados dos personagens)
memory = Memory()

# Initialize session state para navegação individual
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "personagem_selecionado" not in st.session_state:
    st.session_state.personagem_selecionado = None

def main_page():
    # Header com título principal e subtítulo
    st.markdown("# 🎭 Gerenciador de Personagens RPG")
    st.markdown("### *Crie, gerencie e organize seus personagens de RPG*")
    
    st.markdown("---")
    
    # Seção de boas-vindas com emoji e descrição
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h2>🌟 Bem-vindo, Aventureiro! 🌟</h2>
        <p style="font-size: 18px; color: #666;">
            Organize sua mesa de RPG com facilidade! Crie fichas detalhadas, 
            gerencie estatísticas e controle a iniciativa dos combates.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Seção principal com opções em cards mais elaborados
    st.markdown("## 🎯 O que você gostaria de fazer?")
    
    # Espaçamento
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Primeira linha de opções
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px; border-radius: 10px; border: 2px solid #e0e0e0; margin: 10px;">
            <h3>⚔️ Novo Personagem</h3>
            <p>Crie um novo herói para suas aventuras</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎲 Criar Novo Personagem", use_container_width=True):
            st.session_state.current_page = "criar"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; border-radius: 10px; border: 2px solid #e0e0e0; margin: 10px;">
            <h3>📋 Meus Personagens</h3>
            <p>Visualize e edite personagens existentes</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("👥 Ver Personagens Existentes", use_container_width=True):
            st.session_state.current_page = "ver"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 20px; border-radius: 10px; border: 2px solid #e0e0e0; margin: 10px;">
            <h3>⚡ Iniciativa</h3>
            <p>Gerencie a ordem de combate</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎯 Gerenciar Iniciativa", use_container_width=True):
            st.session_state.current_page = "iniciativa"
            st.rerun()
    
    # Seção de estatísticas rápidas
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Dashboard de estatísticas
    st.markdown("## 📊 Status do seu Grupo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎭 Personagens Criados", 
            value=len(memory.personagens),
            help="Total de personagens no seu grupo"
        )
    
    with col2:
        # Contar personagens por nível (assumindo que existe um atributo level)
        if memory.personagens:
            nivel_medio = sum(getattr(p, 'level', 1) for p in memory.personagens) / len(memory.personagens)
            st.metric(
                label="⭐ Nível Médio", 
                value=f"{nivel_medio:.1f}",
                help="Nível médio do grupo"
            )
        else:
            st.metric(label="⭐ Nível Médio", value="0")
    
    with col3:
        # Contar classes diferentes (assumindo que existe um atributo classe)
        if memory.personagens:
            classes = set(getattr(p, 'classe', 'Indefinida') for p in memory.personagens)
            st.metric(
                label="🏛️ Classes Diferentes", 
                value=len(classes),
                help="Variedade de classes no grupo"
            )
        else:
            st.metric(label="🏛️ Classes Diferentes", value="0")
    
    with col4:
        st.metric(
            label="🎲 Sessões Ativas", 
            value="1",
            help="Sessões de jogo em andamento"
        )
    
    # Rodapé com dicas
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; color: #666;">
        <h4>💡 Dicas Rápidas</h4>
        <p>
            🔸 <strong>Personagens:</strong> Crie fichas detalhadas com todas as informações necessárias<br>
            🔸 <strong>Iniciativa:</strong> Mantenha o combate organizado e dinâmico<br>
            🔸 <strong>Organização:</strong> Use as fichas para acompanhar a evolução dos seus heróis
        </p>
    </div>
    """, unsafe_allow_html=True)

def view_characters_page():
    st.title("Personagens Existentes")
    st.markdown("---")

    if not memory.personagens:
        st.info("Nenhum personagem foi criado ainda.")
    else:
        for i, personagem in enumerate(memory.personagens):
            col1, col2, col3= st.columns([0.3, 1, 1])
            with col1:
                st.image(personagem.imagem, width=100)
                
            with col2:
                st.subheader(personagem.nome)
            with col3:
                if st.button(f"Ver Ficha de {personagem.nome}", key=f"btn_{personagem.nome}_{i}"):
                    st.session_state.personagem_selecionado = personagem
                    st.session_state.current_page = "ficha"
                    st.rerun()

    if st.button("Voltar para a Home"):
        st.session_state.current_page = "home"
        st.rerun()

# Page routing logic baseado no session_state individual
current_page = st.session_state.current_page

if current_page == "home":
    main_page()
elif current_page == "criar":
    criar_personagem(memory)
elif current_page == "ver":
    view_characters_page()
elif current_page == "ficha":
    if st.session_state.personagem_selecionado:
        pagina_de_ficha(st.session_state.personagem_selecionado)
elif current_page == "iniciativa":
    pagina_iniciativa(memory)