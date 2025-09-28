import streamlit as st
from models.memory import Memory
from paginas.criar_personagem import criar_personagem
from paginas.stats_persona.CRIS import pagina_de_ficha
from paginas.iniciativa import pagina_iniciativa

# Initialize memory (global, compartilhado apenas para dados dos personagens)
memory = Memory()

# Sistema de login - estados globais compartilhados
if "mestre_logado" not in st.session_state:
    st.session_state.mestre_logado = None
if "mestre_senha" not in st.session_state:
    st.session_state.mestre_senha = "mestre123"  # Senha padrão do mestre

# Initialize session state para navegação individual
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "personagem_selecionado" not in st.session_state:
    st.session_state.personagem_selecionado = None
if "user_type" not in st.session_state:
    st.session_state.user_type = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None

def login_page():
    st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <h1>🎲 PATO RPG INICIATIVA</h1>
        <p style="font-size: 18px; color: #666;">
            Sistema de gerenciamento de personagens e iniciativa para RPG
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Formulário de login
    with st.form("login_form"):
        st.subheader("Fazer Login")
        
        # Seleção do tipo de usuário
        tipo_usuario = st.selectbox(
            "Você é:",
            ["Selecione...", "Jogador", "Mestre"],
            index=0
        )
        
        nome_usuario = st.text_input("Seu nome:")
        
        # Campo de senha apenas para mestre
        senha_mestre = ""
        if tipo_usuario == "Mestre":
            st.info("💡 Apenas um mestre pode estar logado por vez")
            senha_mestre = st.text_input("Senha do Mestre:", type="password")
            if st.session_state.mestre_logado:
                st.warning(f"⚠️ Mestre '{st.session_state.mestre_logado}' já está logado!")
        
        login_submitted = st.form_submit_button("Entrar", type="primary")
    
    # Processar login
    if login_submitted:
        if not nome_usuario:
            st.error("Por favor, insira seu nome.")
        elif tipo_usuario == "Selecione...":
            st.error("Por favor, selecione se você é Jogador ou Mestre.")
        elif tipo_usuario == "Mestre":
            if senha_mestre != st.session_state.mestre_senha:
                st.error("Senha do mestre incorreta!")
            elif st.session_state.mestre_logado and st.session_state.mestre_logado != nome_usuario:
                st.error(f"Mestre '{st.session_state.mestre_logado}' já está logado!")
            else:
                # Login do mestre bem-sucedido
                st.session_state.user_type = "Mestre"
                st.session_state.user_name = nome_usuario
                st.session_state.mestre_logado = nome_usuario
                st.session_state.current_page = "home"
                st.success(f"Bem-vindo, Mestre {nome_usuario}!")
                st.rerun()
        else:  # Jogador
            st.session_state.user_type = "Jogador"
            st.session_state.user_name = nome_usuario
            st.session_state.current_page = "home"
            st.success(f"Bem-vindo, {nome_usuario}!")
            st.rerun()
    
    # Informações sobre o sistema
    st.markdown("---")
    st.markdown("### ℹ️ Informações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Jogadores podem:**
        - Ver todos os personagens
        - Criar personagens públicos
        - Ver ordem de iniciativa
        """)
    
    with col2:
        st.markdown("""
        **Mestre pode:**
        - Todas as funções de jogador
        - Criar personagens privados (NPCs)
        - Gerenciar iniciativa
        - Controlar turnos
        """)
    
    # Status do mestre
    if st.session_state.mestre_logado:
        st.info(f"🎯 Mestre atual: {st.session_state.mestre_logado}")
    else:
        st.info("🎯 Nenhum mestre logado")

def main_page():
    # Header com informações do usuário
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"## 🎲 PATO RPG - Bem-vindo, {st.session_state.user_name}!")
    
    with col2:
        st.markdown(f"**Tipo:** {st.session_state.user_type}")
    
    with col3:
        if st.button("🚪 Sair", type="secondary"):
            # Se for mestre, libera o slot
            if st.session_state.user_type == "Mestre":
                st.session_state.mestre_logado = None
            
            # Reset session state
            st.session_state.user_type = None
            st.session_state.user_name = None
            st.session_state.current_page = "login"
            st.rerun()
    
    st.markdown("---")
    
    # Seção principal com opções em cards
    st.markdown("## O que você gostaria de fazer?")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Primeira linha de opções
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 20px; border-radius: 10px; border: 2px solid #e0e0e0; margin: 10px;">
            <h3>Novo Personagem</h3>
            <p>Cria um novo personagem</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Criar Novo Personagem", use_container_width=True):
            st.session_state.current_page = "criar"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px; border-radius: 10px; border: 2px solid #e0e0e0; margin: 10px;">
            <h3>Meus Personagens</h3>
            <p>Visualize e edite personagens existentes</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver Personagens", use_container_width=True):
            st.session_state.current_page = "ver"
            st.rerun()
    
    with col3:
        # Botão de iniciativa - funcionalidade diferente para mestre e jogador
        if st.session_state.user_type == "Mestre":
            st.markdown("""
            <div style="text-align: center; padding: 20px; border-radius: 10px; border: 2px solid #ff6b6b; margin: 10px;">
                <h3>⚔️ Gerenciar Iniciativa</h3>
                <p>Controle completo da ordem de combate</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Gerenciar Iniciativa", use_container_width=True):
                st.session_state.current_page = "iniciativa"
                st.rerun()
        else:
            st.markdown("""
            <div style="text-align: center; padding: 20px; border-radius: 10px; border: 2px solid #4ecdc4; margin: 10px;">
                <h3>👁️ Ver Iniciativa</h3>
                <p>Visualize a ordem de combate</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Ver Ordem de Iniciativa", use_container_width=True):
                st.session_state.current_page = "iniciativa"
                st.rerun()
    
    # Seção de estatísticas
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 📊 Status da Sessão")
    
    # Contadores
    personagens_publicos = len([p for p in memory.personagens if not getattr(p, 'privado', False)])
    personagens_privados = len([p for p in memory.personagens if getattr(p, 'privado', False)])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Personagens Públicos", 
            value=personagens_publicos,
            help="Personagens criados pelos jogadores"
        )
    
    with col2:
        st.metric(
            label="NPCs (Privados)", 
            value=personagens_privados,
            help="Personagens criados pelo mestre"
        )
    
    with col3:
        st.metric(
            label="Total", 
            value=len(memory.personagens),
            help="Total de personagens na sessão"
        )
    
    # Informações adicionais para o mestre
    if st.session_state.user_type == "Mestre":
        st.markdown("---")
        st.markdown("### 🎯 Controles do Mestre")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Resetar Todas as Iniciativas"):
                for personagem in memory.personagens:
                    personagem.iniciativa = 0
                memory.lista_iniciativa = []
                memory.rodada_atual = 0
                st.success("Todas as iniciativas foram resetadas!")
                st.rerun()
        
        with col2:
            if st.button("⚙️ Alterar Senha do Mestre"):
                st.session_state.current_page = "alterar_senha"
                st.rerun()
    
    # Rodapé
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px 0; color: #666;">
        <h4>Feito por Alison (github: ABMS-NS)</h4>
    </div>
    """, unsafe_allow_html=True)

def view_characters_page():
    st.title("Personagens da Sessão")
    
    # Header com filtros
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.session_state.user_type == "Mestre":
            filtro = st.selectbox(
                "Filtrar personagens:",
                ["Todos", "Apenas Públicos", "Apenas Privados (NPCs)"]
            )
        else:
            # Jogadores só veem personagens públicos na lista de personagens
            filtro = "Apenas Públicos"
            st.info("👁️ Jogadores só podem ver personagens públicos aqui. NPCs aparecem apenas na iniciativa.")
    
    with col2:
        if st.button("🔙 Voltar"):
            st.session_state.current_page = "home"
            st.rerun()
    
    st.markdown("---")
    
    # Filtrar personagens baseado no tipo de usuário e filtro
    personagens_filtrados = []
    
    for personagem in memory.personagens:
        eh_privado = getattr(personagem, 'privado', False)
        
        # Jogadores só veem personagens públicos na lista de personagens
        if st.session_state.user_type == "Jogador" and eh_privado:
            continue
        
        if filtro == "Apenas Públicos" and eh_privado:
            continue
        elif filtro == "Apenas Privados (NPCs)" and not eh_privado:
            continue
        
        personagens_filtrados.append(personagem)
    
    if not personagens_filtrados:
        st.info("Nenhum personagem encontrado com os filtros atuais.")
    else:
        for i, personagem in enumerate(personagens_filtrados):
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([0.3, 1, 0.5, 1])
                
                with col1:
                    st.image(personagem.imagem, width=80)
                
                with col2:
                    st.subheader(personagem.nome)
                    # Indicador de tipo
                    if getattr(personagem, 'privado', False):
                        st.caption("🔒 NPC (Privado)")
                    else:
                        st.caption("🌐 Personagem Público")
                
                with col3:
                    if hasattr(personagem, 'iniciativa') and personagem.iniciativa > 0:
                        st.metric("Iniciativa", personagem.iniciativa)
                
                with col4:
                    if st.button(f"Ver Ficha", key=f"btn_{personagem.nome}_{i}"):
                        st.session_state.personagem_selecionado = personagem
                        st.session_state.current_page = "ficha"
                        st.rerun()

def alterar_senha_page():
    st.title("⚙️ Alterar Senha do Mestre")
    st.markdown("---")
    
    with st.form("alterar_senha_form"):
        senha_atual = st.text_input("Senha atual:", type="password")
        nova_senha = st.text_input("Nova senha:", type="password")
        confirmar_senha = st.text_input("Confirmar nova senha:", type="password")
        
        submitted = st.form_submit_button("Alterar Senha", type="primary")
    
    if submitted:
        if senha_atual != st.session_state.mestre_senha:
            st.error("Senha atual incorreta!")
        elif not nova_senha:
            st.error("Por favor, insira uma nova senha.")
        elif nova_senha != confirmar_senha:
            st.error("As senhas não coincidem!")
        else:
            st.session_state.mestre_senha = nova_senha
            st.success("Senha alterada com sucesso!")
            st.info("A nova senha será válida para futuras sessões.")
    
    if st.button("🔙 Voltar para Home"):
        st.session_state.current_page = "home"
        st.rerun()

def criar_personagem(memory):
    # Verifica se o usuário está logado
    if not hasattr(st.session_state, 'user_type') or st.session_state.user_type is None:
        st.error("❌ Você precisa fazer login primeiro!")
        if st.button("🔙 Voltar para Login"):
            st.session_state.current_page = "login"
            st.rerun()
        return
    
    # Importa e chama a função
    from paginas.criar_personagem import criar_personagem as criar_func
    criar_func(memory)

current_page = st.session_state.current_page

if current_page == "ver":
    view_characters_page()
elif current_page == "ficha":
    if st.session_state.personagem_selecionado:
        pagina_de_ficha(st.session_state.personagem_selecionado)
elif current_page == "iniciativa":
    pagina_iniciativa(memory)
elif current_page == "alterar_senha":
    alterar_senha_page()