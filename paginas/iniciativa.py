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
                col_pos, col_img, col_info = st.columns([0.1, 0.2, 0.7])
                    
                with col_pos:
                    st.markdown(f"**{i+1}º**")
                    
                with col_img:
                    st.image(personagem.imagem, width=50)
                    
                with col_info:
                    st.write(f"**{personagem.nome}**")
                    st.write(f"Iniciativa: {personagem.iniciativa}")
            
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
                            max_value=50,
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