import streamlit as st

def pagina_iniciativa(memory):
    st.title("Gerenciar Iniciativa")
    st.markdown("---")
    
    # Verifica se há personagens
    if not memory.personagens:
        st.info("Nenhum personagem foi criado ainda.")
        if st.button("Voltar para a Home"):
            st.session_state.current_page = "home"
            st.rerun()
        return
    
    #visualização da ordem de iniciativa
    st.subheader("Ordem de Iniciativa")
    st.write(f"Rodada Atual: {memory.rodada_atual}")
    if memory.lista_iniciativa:
            
        for i, personagem in enumerate(memory.lista_iniciativa):
            with st.container(border=True):
                col_pos, col_img, col_info, col_efeitos = st.columns([0.1, 0.2, 0.5, 0.2])
                    
                with col_pos:
                    st.markdown(f"**{i+1}º**")
                    
                with col_img:
                    st.image(personagem.imagem, width=50)
                    
                with col_info:
                    st.write(f"**{personagem.nome}**")
                    st.write(f"Iniciativa: {personagem.iniciativa}")
                
                with col_efeitos:
                    if personagem.efeitos:
                        # Cria o texto dos efeitos para o tooltip
                        efeitos_tooltip = " | ".join([f"{efeito.nome} ({efeito.duracao}t)" for efeito in personagem.efeitos])
                        
                        # Badge dinâmico que se adapta ao conteúdo
                        badge_html = f"""
                        <div style="
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            padding: 4px 8px;
                            border-radius: 12px;
                            font-size: 11px;
                            font-weight: bold;
                            text-align: center;
                            cursor: pointer;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            transition: all 0.3s ease;
                            white-space: nowrap;
                        " 
                        title="{efeitos_tooltip}"
                        onmouseover="this.style.transform='scale(1.05)'"
                        onmouseout="this.style.transform='scale(1)'">
                            {len(personagem.efeitos)} efeito{"s" if len(personagem.efeitos) > 1 else ""}
                        </div>
                        """
                        st.markdown(badge_html, unsafe_allow_html=True)
                    else:
                        # Badge para sem efeitos
                        badge_vazio = """
                        <div style="
                            background-color: #e0e0e0;
                            color: #757575;
                            padding: 4px 8px;
                            border-radius: 12px;
                            font-size: 11px;
                            font-weight: bold;
                            text-align: center;
                            white-space: nowrap;
                        ">
                            Limpo
                        </div>
                        """
                        st.markdown(badge_vazio, unsafe_allow_html=True)
            
            # Botão para reorganizar

        col_1, col_2 = st.columns(2)
        with col_1:
            if st.button("➡️ Passar Turno"):
                memory.rodada_atual += 1
                memory.passar_turno()
                st.rerun()
        with col_2:    
            if st.button("🔄 Reorganizar Lista"):
                memory.organizar_init()
                st.rerun()

    # parte de organizar iniciativas
    st.markdown("---")
    with st.expander("Definir Iniciativas"):
        st.subheader("Definir Iniciativa")
        
        # Formulário para definir iniciativas
        with st.form("form_iniciativa"):
            st.write("**Configure a iniciativa de cada personagem:**")
            
            iniciativas_temp = {}
            
            for i, personagem in enumerate(memory.personagens):
                # Valor atual da iniciativa (se existir)
                valor_atual = getattr(personagem, 'iniciativa', 0)
                
                # Container para cada personagem
                with st.container(border=True):
                    col_img, col_input = st.columns([0.3, 0.7])
                    
                    with col_img:
                        st.image(personagem.imagem, width=60)
                    
                    with col_input:
                        st.write(f"**{personagem.nome}**")
                        iniciativa = st.number_input(
                            "Iniciativa",
                            min_value=0,
                            value=valor_atual,
                            step=1,
                            key=f"init_{personagem.nome}_{i}"
                        )
                        iniciativas_temp[personagem.nome] = iniciativa
            
            st.markdown("---")
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                aplicar = st.form_submit_button("Aplicar Iniciativas", type="primary")
            with col_btn2:
                zerar = st.form_submit_button("Zerar Todas")
        
        # Processa o formulário
        if aplicar:
            for personagem in memory.personagens:
                personagem.iniciativa = iniciativas_temp[personagem.nome]
            
            # Organiza a lista de iniciativa
            memory.organizar_init()
            st.success("Iniciativas aplicadas com sucesso!")
            st.rerun()
        
        if zerar:
            for personagem in memory.personagens:
                personagem.iniciativa = 0
            memory.lista_iniciativa = []
            st.success("Todas as iniciativas foram zeradas!")
            st.rerun()
    
    st.markdown("---")
    if st.button("Voltar para a Home"):
        st.session_state.current_page = "home"
        st.rerun()