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
    
    # Título diferente baseado no tipo de usuário
    if hasattr(st.session_state, 'user_type') and st.session_state.user_type == "Mestre":
        st.title("🎯 Criação de Personagem/NPC")
        st.success(f"✅ Logado como: {st.session_state.user_name} ({st.session_state.user_type})")
    else:
        st.title("👤 Criação de Personagem")
        if hasattr(st.session_state, 'user_type'):
            st.info(f"✅ Logado como: {st.session_state.user_name} ({st.session_state.user_type})")
        else:
            st.error("❌ Tipo de usuário não detectado!")
    
    st.markdown("---")

    # Controles para adicionar/remover barras
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Adicionar Barra"):
            adicionar_barra()
            st.rerun()
    with col2:
        if st.button("➖ Remover Barra"):
            remover_barra()
            st.rerun()

    num_barras_atual = st.session_state.num_barras

    with st.form("form_personagem"):
        # Campo para o nome
        nome = st.text_input("Nome do Personagem")

        # Campo para o tipo de personagem (apenas para mestre)
        eh_privado = False
        
        if getattr(st.session_state, 'user_type', None) == "Mestre":
            st.markdown("### 🎭 Tipo de Personagem")
            tipo_personagem = st.radio(
                "Escolha o tipo:",
                ["Personagem Público", "NPC (Privado)"],
                help="Personagens públicos são visíveis para todos. NPCs privados são visíveis apenas para o mestre.",
                horizontal=True
            )
            eh_privado = (tipo_personagem == "NPC (Privado)")
            
            if eh_privado:
                st.success("🔒 Este será um NPC privado - apenas você poderá ver e editar")
            else:
                st.info("🌐 Este será um personagem público - todos os jogadores poderão ver")
        else:
            st.info("🌐 Seu personagem será público (visível para todos os jogadores)")

        # Campo para a imagem
        imagem_bytes = st.file_uploader(
            "Escolha uma imagem para o personagem", 
            type=["png", "jpg", "jpeg"],
            help="Formatos suportados: PNG, JPG, JPEG"
        )

        st.markdown("---")
        st.subheader("📊 Barras de Status")
        st.caption(f"Configure {num_barras_atual} barra(s) de status para o personagem")

        barras_inputs = []
        for i in range(num_barras_atual):
            st.markdown(f"**Barra #{i+1}**")
            with st.container(border=True):
                col_b1, col_b2, col_b3 = st.columns(3)
                with col_b1:
                    nome_barra = st.text_input(
                        "Nome da barra", 
                        key=f"barra_nome_{i}",
                        placeholder="Ex: Vida, Mana, Stamina"
                    )
                with col_b2:
                    atual = st.number_input(
                        "Valor Atual", 
                        min_value=0, 
                        value=100 if i == 0 else 0, 
                        key=f"barra_atual_{i}"
                    )
                with col_b3:
                    maximo = st.number_input(
                        "Valor Máximo", 
                        min_value=1, 
                        value=100, 
                        key=f"barra_maximo_{i}"
                    )
                
                # Validação da barra
                if atual > maximo:
                    st.warning(f"⚠️ Valor atual não pode ser maior que o máximo!")
                
                barras_inputs.append({"nome": nome_barra, "atual": min(atual, maximo), "maximo": maximo})
        
        st.markdown("---")
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            submitted = st.form_submit_button("✅ Criar Personagem", type="primary")
        with col_btn2:
            if st.form_submit_button("🔄 Limpar Formulário"):
                st.rerun()

    # Validação e criação do personagem
    if submitted:
        erro = False
        
        if not nome:
            st.error("❌ Por favor, insira o nome do personagem.")
            erro = True
        elif not imagem_bytes:
            st.error("❌ Por favor, faça o upload de uma imagem.")
            erro = True
        
        # Verifica se pelo menos uma barra tem nome
        barras_validas = [barra for barra in barras_inputs if barra["nome"].strip()]
        if not barras_validas:
            st.error("❌ Por favor, configure pelo menos uma barra com nome.")
            erro = True
        
        if not erro:
            # Cria a URL da imagem a partir dos bytes
            imagem_url = io.BytesIO(imagem_bytes.read())

            # Cria o objeto Personagem
            personagem = Personagem(nome, imagem_url)
            
            # Define se o personagem é privado (apenas para mestre)
            personagem.privado = eh_privado
            
            # Adiciona informação sobre quem criou
            personagem.criado_por = st.session_state.user_name
            personagem.tipo_criador = st.session_state.user_type
            
            # Adiciona as barras de status válidas ao personagem
            for barra in barras_validas:
                personagem.adicionar_barra(barra["nome"], barra["atual"], barra["maximo"])

            # Armazena o personagem na memória global (compartilhada)
            memory.personagens.append(personagem)
            
            # Reseta o número de barras para o próximo personagem (individual)
            st.session_state.num_barras = 1
            
            # Mensagem de sucesso
            if eh_privado:
                st.success(f"🔒 NPC '{nome}' criado com sucesso! (Visível apenas para o mestre)")
            else:
                st.success(f"✅ Personagem '{nome}' criado com sucesso!")
            
            # Vai para a ficha do personagem criado (navegação individual)
            st.session_state.personagem_selecionado = personagem
            st.session_state.current_page = "ficha"
            st.rerun()
            
    # Seção de ajuda
    with st.expander("💡 Ajuda e Dicas"):
        st.markdown("""
        **Dicas para criar personagens:**
        
        - **Nome:** Escolha um nome único e memorável
        - **Imagem:** Use imagens claras e de boa qualidade
        - **Barras:** Comuns são Vida, Mana, Stamina, etc.
        - **Valores:** O valor atual não pode ser maior que o máximo
        """)
        
        if st.session_state.user_type == "Mestre":
            st.markdown("""
            **Personagens Privados (NPCs):**
            - Visíveis apenas para você (mestre)
            - Úteis para inimigos, NPCs importantes
            - Aparecem na ordem de iniciativa normalmente
            - Podem ser editados apenas por você
            """)
    
    # Botão para voltar
    st.markdown("---")
    if st.button("🔙 Voltar para a Home"):
        st.session_state.current_page = "home"
        st.rerun()