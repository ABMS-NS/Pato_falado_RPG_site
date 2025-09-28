import streamlit as st

def pagina_iniciativa(memory):
    # Título diferente baseado no tipo de usuário
    if st.session_state.user_type == "Mestre":
        st.title("⚔️ Gerenciar Iniciativa de Combate")
        st.caption("Controle completo da ordem de combate")
    else:
        st.title("⚔️ Iniciativa de Combate")
        st.caption("Visualize e defina iniciativas")
    
    st.markdown("---")
    
    # Todos os personagens são visíveis na iniciativa (incluindo NPCs privados)
    personagens_visiveis = memory.personagens  # Correção aqui - usar a instância memory passada como parâmetro
    
    if not personagens_visiveis:
        st.info("Nenhum personagem disponível para iniciativa.")
        if st.button("🔙 Voltar para a Home"):
            st.session_state.current_page = "home"
            st.rerun()
        return
    
    # Visualização da ordem de iniciativa
    st.subheader("📋 Ordem Atual de Iniciativa")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.metric("Rodada Atual", memory.rodada_atual)
    with col_info2:
        st.metric("Personagens em Combate", len(memory.lista_iniciativa))
    
    if memory.lista_iniciativa:
        st.markdown("### 🏆 Ordem de Turnos")
        
        for i, personagem in enumerate(memory.lista_iniciativa):
            with st.container(border=True):
                col_pos, col_img, col_info, col_status = st.columns([0.1, 0.2, 0.5, 0.2])
                    
                with col_pos:
                    # Destaca o primeiro da lista
                    if i == 0:
                        st.markdown(f"**🎯{i+1}º**")
                    else:
                        st.markdown(f"**{i+1}º**")
                    
                with col_img:
                    st.image(personagem.imagem, width=50)
                    
                with col_info:
                    st.write(f"**{personagem.nome}**")
                    st.write(f"Iniciativa: {personagem.iniciativa}")
                    
                    # Mostra indicador de tipo - NPCs aparecem mas são identificados
                    if getattr(personagem, 'privado', False):
                        st.caption("🔒 NPC")
                    else:
                        st.caption("🌐 Personagem")
                
                with col_status:
                    # Mostra efeitos ativos
                    if personagem.efeitos:
                        st.write(f"⚡ {len(personagem.efeitos)} efeito(s)")
        
        # Controles diferenciados
        st.markdown("---")
        if st.session_state.user_type == "Mestre":
            st.subheader("🎯 Controles do Mestre")
            
            col_1, col_2, col_3 = st.columns(3)
            
            with col_1:
                if st.button("➡️ Passar Turno", type="primary"):
                    # Avança rodada
                    memory.rodada_atual += 1
                    # Chama o método para processar efeitos e pega feedback
                    efeitos_removidos = memory.passar_turno()
                    
                    # Feedback melhorado
                    st.success(f"🎯 Turno avançado! Rodada atual: {memory.rodada_atual}")
                    
                    # Mostra efeitos que expiraram
                    if efeitos_removidos:
                        st.info("⏰ Efeitos que expiraram:")
                        for efeito in efeitos_removidos:
                            st.write(f"• {efeito}")
                    else:
                        st.info("ℹ️ Nenhum efeito expirou neste turno")
                    
                    st.rerun()
            
            with col_2:    
                if st.button("🔄 Reorganizar Lista"):
                    memory.organizar_init()
                    st.success("Lista reorganizada!")
                    st.rerun()
            
            with col_3:
                if st.button("🛑 Parar Combate", type="secondary"):
                    for personagem in memory.personagens:
                        personagem.iniciativa = 0
                        personagem.efeitos = []  # Limpa efeitos também
                    memory.lista_iniciativa = []
                    memory.rodada_atual = 0
                    st.success("Combate finalizado!")
                    st.rerun()
        else:
            st.subheader("👥 Ações do Jogador")
            col_1, col_2 = st.columns(2)
            
            with col_1:
                if st.button("🔄 Reorganizar Lista"):
                    memory.organizar_init()
                    st.success("Lista reorganizada!")
                    st.rerun()
            
            with col_2:
                st.info("ℹ️ Apenas o mestre pode passar turnos e parar combate")
    else:
        st.info("⏳ Nenhum personagem com iniciativa definida ainda.")

    # Seção para definir iniciativas - TODOS podem definir
    st.markdown("---")
    
    with st.expander("⚙️ Definir Iniciativas", expanded=not memory.lista_iniciativa):
        if st.session_state.user_type == "Mestre":
            st.subheader("Configurar Iniciativa dos Personagens")
            st.caption("Configure a iniciativa de todos os personagens")
        else:
            st.subheader("Definir Iniciativas")
            st.caption("Configure a iniciativa dos personagens (incluindo NPCs)")
        
        # Formulário para definir iniciativas
        with st.form("form_iniciativa"):
            st.write("**Configure a iniciativa de cada personagem:**")
            
            iniciativas_temp = {}
            
            for i, personagem in enumerate(personagens_visiveis):
                # Valor atual da iniciativa (se existir)
                valor_atual = getattr(personagem, 'iniciativa', 0)
                
                # Container para cada personagem
                with st.container(border=True):
                    col_img, col_input, col_tipo = st.columns([0.2, 0.6, 0.2])
                    
                    with col_img:
                        st.image(personagem.imagem, width=60)
                    
                    with col_input:
                        st.write(f"**{personagem.nome}**")
                        # Jogadores podem definir iniciativa de todos os personagens
                        iniciativa = st.number_input(
                            "Iniciativa",
                            min_value=0,
                            max_value=50,
                            value=valor_atual,
                            step=1,
                            key=f"init_{personagem.nome}_{i}",
                            help="Valor de 0 remove o personagem do combate"
                        )
                        iniciativas_temp[personagem.nome] = iniciativa
                    
                    with col_tipo:
                        if getattr(personagem, 'privado', False):
                            st.markdown("🔒 **NPC**")
                        else:
                            st.markdown("🌐 **Personagem**")
            
            st.markdown("---")
            # Botões diferentes para mestre e jogador
            if st.session_state.user_type == "Mestre":
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    aplicar = st.form_submit_button("✅ Aplicar Iniciativas", type="primary")
                with col_btn2:
                    zerar = st.form_submit_button("🗑️ Zerar Todas")
                with col_btn3:
                    rolar = st.form_submit_button("🎲 Rolar Aleatório")
            else:
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    aplicar = st.form_submit_button("✅ Aplicar Iniciativas", type="primary")
                with col_btn2:
                    zerar = st.form_submit_button("🗑️ Zerar Todas")
                
                # Variáveis para manter compatibilidade
                rolar = False
        
        # Processa o formulário
        if aplicar:
            for personagem in personagens_visiveis:
                personagem.iniciativa = iniciativas_temp[personagem.nome]
            
            # Organiza a lista de iniciativa
            memory.organizar_init()
            st.success("✅ Iniciativas aplicadas com sucesso!")
            st.rerun()
        
        if zerar:
            for personagem in personagens_visiveis:
                personagem.iniciativa = 0
            memory.lista_iniciativa = []
            memory.rodada_atual = 0
            st.success("🗑️ Todas as iniciativas foram zeradas!")
            st.rerun()
        
        # Rolar aleatório (apenas para mestre)
        if st.session_state.user_type == "Mestre" and rolar:
            import random
            for personagem in personagens_visiveis:
                # Rola iniciativa aleatória entre 1 e 20
                personagem.iniciativa = random.randint(1, 20)
            
            memory.organizar_init()
            st.success("🎲 Iniciativas roladas aleatoriamente!")
            st.rerun()
    
    # Seção de informações úteis
    st.markdown("---")
    
    with st.expander("ℹ️ Como funciona a Iniciativa"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📋 Ordem de Combate:**
            - Personagens são ordenados por iniciativa (maior primeiro)
            - NPCs privados aparecem na lista mas só o mestre os controla
            - Jogadores podem definir iniciativas de todos os personagens
            """)
        
        with col2:
            st.markdown("""
            **⚔️ Durante o Combate:**
            - O 1º da lista é quem age no turno atual
            - Efeitos são gerenciados automaticamente
            - Iniciativa 0 remove do combate
            """)
        
        st.markdown("---")
        if st.session_state.user_type == "Mestre":
            st.markdown("""
            **🎯 Controles do Mestre:**
            - **Passar Turno:** Avança para o próximo na ordem e reduz duração dos efeitos
            - **Reorganizar:** Reordena a lista caso alguém mude a iniciativa
            - **Parar Combate:** Zera todas as iniciativas e para o combate
            - **Rolar Aleatório:** Atribui valores de 1-20 para todos os personagens
            """)
        else:
            st.markdown("""
            **👥 Como Jogador:**
            - **Definir Iniciativas:** Você pode definir iniciativas para todos os personagens (incluindo NPCs)
            - **Reorganizar:** Você pode reorganizar a lista após mudanças
            - **Ver NPCs:** NPCs aparecem na lista mas são identificados com 🔒
            """)
    
    # Botão para voltar
    st.markdown("---")
    if st.button("🔙 Voltar para a Home"):
        st.session_state.current_page = "home"
        st.rerun()
                
                # Container para cada personagem
        with st.container(border=True):
                    col_img, col_input, col_tipo = st.columns([0.2, 0.6, 0.2])
                    
                    with col_img:
                        st.image(personagem.imagem, width=60)
                    
                    with col_input:
                        st.write(f"**{personagem.nome}**")
                        # Jogadores podem definir iniciativa de todos os personagens
                        iniciativa = st.number_input(
                            "Iniciativa",
                            min_value=0,
                            max_value=50,
                            value=valor_atual,
                            step=1,
                            key=f"init_{personagem.nome}_{i}",
                            help="Valor de 0 remove o personagem do combate"
                        )
                        iniciativas_temp[personagem.nome] = iniciativa
                    
                    with col_tipo:
                        if getattr(personagem, 'privado', False):
                            st.markdown("🔒 **NPC**")
                        else:
                            st.markdown("🌐 **Personagem**")
            
        st.markdown("---")
            # Botões diferentes para mestre e jogador
        if st.session_state.user_type == "Mestre":
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    aplicar = st.form_submit_button("✅ Aplicar Iniciativas", type="primary")
                with col_btn2:
                    zerar = st.form_submit_button("🗑️ Zerar Todas")
                with col_btn3:
                    rolar = st.form_submit_button("🎲 Rolar Aleatório")
        else:
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    aplicar = st.form_submit_button("✅ Aplicar Iniciativas", type="primary")
                with col_btn2:
                    zerar = st.form_submit_button("🗑️ Zerar Todas")
                
                # Variáveis para manter compatibilidade
                rolar = False
        
        # Processa o formulário
        if aplicar:
            for personagem in personagens_visiveis:
                personagem.iniciativa = iniciativas_temp[personagem.nome]
            
            # Organiza a lista de iniciativa
            memory.organizar_init()
            st.success("✅ Iniciativas aplicadas com sucesso!")
            st.rerun()
        
        if zerar:
            for personagem in personagens_visiveis:
                personagem.iniciativa = 0
            memory.lista_iniciativa = []
            memory.rodada_atual = 0
            st.success("🗑️ Todas as iniciativas foram zeradas!")
            st.rerun()
        
        # Rolar aleatório (apenas para mestre)
        if st.session_state.user_type == "Mestre" and rolar:
            import random
            for personagem in personagens_visiveis:
                # Rola iniciativa aleatória entre 1 e 20
                personagem.iniciativa = random.randint(1, 20)
            
            memory.organizar_init()
            st.success("🎲 Iniciativas roladas aleatoriamente!")
            st.rerun()
    
    # Seção de informações úteis
    st.markdown("---")
    
    with st.expander("ℹ️ Como funciona a Iniciativa"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📋 Ordem de Combate:**
            - Personagens são ordenados por iniciativa (maior primeiro)
            - NPCs privados aparecem na lista mas só o mestre os controla
            - Jogadores podem definir iniciativas de todos os personagens
            """)
        
        with col2:
            st.markdown("""
            **⚔️ Durante o Combate:**
            - O 1º da lista é quem age no turno atual
            - Efeitos são gerenciados automaticamente
            - Iniciativa 0 remove do combate
            """)
        
        st.markdown("---")
        if st.session_state.user_type == "Mestre":
            st.markdown("""
            **🎯 Controles do Mestre:**
            - **Passar Turno:** Avança para o próximo na ordem e reduz duração dos efeitos
            - **Reorganizar:** Reordena a lista caso alguém mude a iniciativa
            - **Parar Combate:** Zera todas as iniciativas e para o combate
            - **Rolar Aleatório:** Atribui valores de 1-20 para todos os personagens
            """)
        else:
            st.markdown("""
            **👥 Como Jogador:**
            - **Definir Iniciativas:** Você pode definir iniciativas para todos os personagens (incluindo NPCs)
            - **Reorganizar:** Você pode reorganizar a lista após mudanças
            - **Ver NPCs:** NPCs aparecem na lista mas são identificados com 🔒
            """)
    
    # Botão para voltar
    st.markdown("---")
    if st.button("🔙 Voltar para a Home"):
        st.session_state.current_page = "home"
        st.rerun()
                    
                    # Container para cada personagem
        with st.container(border=True):
                        col_img, col_input, col_tipo = st.columns([0.2, 0.6, 0.2])
                        
                        with col_img:
                            st.image(personagem.imagem, width=60)
                        
                        with col_input:
                            st.write(f"**{personagem.nome}**")
                            iniciativa = st.number_input(
                                "Iniciativa",
                                min_value=0,
                                max_value=50,
                                value=valor_atual,
                                step=1,
                                key=f"init_{personagem.nome}_{i}",
                                help="Valor de 0 remove o personagem do combate"
                            )
                            iniciativas_temp[personagem.nome] = iniciativa
                        
                        with col_tipo:
                            if getattr(personagem, 'privado', False):
                                st.markdown("🔒 **NPC**")
                            else:
                                st.markdown("🌐 **Público**")
                
        st.markdown("---")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
                
        with col_btn1:
                    aplicar = st.form_submit_button("✅ Aplicar Iniciativas", type="primary")
        with col_btn2:
                    zerar = st.form_submit_button("🗑️ Zerar Todas")
        with col_btn3:
                    rolar = st.form_submit_button("🎲 Rolar Aleatório")
            
            # Processa o formulário
        if aplicar:
                for personagem in personagens_visiveis:
                    personagem.iniciativa = iniciativas_temp[personagem.nome]
                
                # Organiza a lista de iniciativa
                memory.organizar_init()
                st.success("✅ Iniciativas aplicadas com sucesso!")
                st.rerun()
            
        if zerar:
                for personagem in personagens_visiveis:
                    personagem.iniciativa = 0
                memory.lista_iniciativa = []
                memory.rodada_atual = 0
                st.success("🗑️ Todas as iniciativas foram zeradas!")
                st.rerun()
            
        if rolar:
                import random
                for personagem in personagens_visiveis:
                    # Rola iniciativa aleatória entre 1 e 20
                    personagem.iniciativa = random.randint(1, 20)
                
                memory.organizar_init()
                st.success("🎲 Iniciativas roladas aleatoriamente!")
                st.rerun()
    
    else:
        # Jogadores só podem ver as iniciativas
        st.info("ℹ️ Apenas o mestre pode definir e controlar a iniciativa.")
        
        if personagens_visiveis:
            with st.expander("👁️ Ver Iniciativas Atuais"):
                for personagem in personagens_visiveis:
                    with st.container(border=True):
                        col_img, col_info = st.columns([0.3, 0.7])
                        
                        with col_img:
                            st.image(personagem.imagem, width=60)
                        
                        with col_info:
                            st.write(f"**{personagem.nome}**")
                            iniciativa_atual = getattr(personagem, 'iniciativa', 0)
                            if iniciativa_atual > 0:
                                st.write(f"Iniciativa: {iniciativa_atual}")
                            else:
                                st.write("Iniciativa: Não definida")
    
    # Seção de informações úteis
    st.markdown("---")
    
    with st.expander("ℹ️ Como funciona a Iniciativa"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📋 Ordem de Combate:**
            - Personagens são ordenados por iniciativa (maior primeiro)
            - Rodadas avançam automaticamente
            - Efeitos têm duração reduzida a cada turno
            """)
        
        with col2:
            st.markdown("""
            **⚔️ Durante o Combate:**
            - O 1º da lista é quem age no turno atual
            - Efeitos são gerenciados automaticamente
            - Iniciativa 0 remove do combate
            """)
        
        if st.session_state.user_type == "Mestre":
            st.markdown("---")
            st.markdown("""
            **🎯 Controles do Mestre:**
            - **Passar Turno:** Avança para o próximo na ordem e reduz duração dos efeitos
            - **Reorganizar:** Reordena a lista caso alguém mude a iniciativa
            - **Parar Combate:** Zera todas as iniciativas e para o combate
            - **Rolar Aleatório:** Atribui valores de 1-20 para todos os personagens
            """)
    
    # Botão para voltar
    st.markdown("---")
    if st.button("🔙 Voltar para a Home"):
        st.session_state.current_page = "home"
        st.rerun()