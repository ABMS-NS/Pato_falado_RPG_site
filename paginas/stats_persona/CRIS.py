import streamlit as st
from models.efeito import Efeito
from models.personagem import *

def pagina_de_ficha(p: Personagem):
    # Verifica permissões - jogadores não podem ver personagens privados
    eh_privado = getattr(p, 'privado', False)
    if st.session_state.user_type == "Jogador" and eh_privado:
        st.error("🔒 Você não tem permissão para ver este personagem privado!")
        if st.button("🔙 Voltar para a Home"):
            st.session_state.current_page = "home"
            st.rerun()
        return

    # ------------------------
    # Header com informações do personagem
    # ------------------------
    col_header1, col_header2 = st.columns([3, 1])
    
    with col_header1:
        if eh_privado:
            st.title(f"🔒 Ficha do NPC: {p.nome}")
        else:
            st.title(f"👤 Ficha do Personagem: {p.nome}")
    
    with col_header2:
        # Informações sobre quem criou
        if hasattr(p, 'criado_por'):
            st.caption(f"Criado por: {p.criado_por}")
        if eh_privado:
            st.caption("🔒 Personagem Privado")
        else:
            st.caption("🌐 Personagem Público")

    # ------------------------
    # Layout em colunas principal
    # ------------------------
    col1, col2 = st.columns([5, 7])

    with col1:
        st.image(p.imagem, caption=p.nome, use_container_width=True)
        
        # Informações da iniciativa
        if hasattr(p, 'iniciativa'):
            st.markdown("---")
            if p.iniciativa > 0:
                st.metric("⚔️ Iniciativa", p.iniciativa)
            else:
                st.metric("⚔️ Iniciativa", "Não definida")

    with col2:
        st.header(f"📊 Status de {p.nome}")
        
        if not p.barras:
            st.info("Nenhuma barra de status configurada para este personagem.")
        else:
            # Exibe as barras de status
            for i, barra in enumerate(p.barras):
                # Determina se o usuário pode editar
                pode_editar = True
                if eh_privado and st.session_state.user_type == "Jogador":
                    pode_editar = False
                
                if pode_editar:
                    # Input editável
                    novo_valor = st.number_input(
                        f"{barra['nome']}",
                        min_value=0,
                        max_value=barra['maximo'],
                        value=barra["atual"],
                        step=1,
                        key=f"{p.nome}_{barra['nome']}_input_{i}",
                        help=f"Valor máximo: {barra['maximo']}"
                    )
                    
                    # Atualiza o valor da barra
                    barra["atual"] = novo_valor
                else:
                    # Apenas visualização
                    st.write(f"**{barra['nome']}:** {barra['atual']}/{barra['maximo']}")
                
                # Barra de progresso com cores baseadas na porcentagem
                porcentagem = barra["atual"] / barra["maximo"] if barra["maximo"] > 0 else 0
                
                # Cor da barra baseada na porcentagem
                if porcentagem > 0.6:
                    cor = "normal"
                elif porcentagem > 0.3:
                    cor = "normal"  # Streamlit não tem cor amarela nativa
                else:
                    cor = "normal"
                
                st.progress(min(porcentagem, 1.0))
                st.caption(f"{barra['atual']}/{barra['maximo']} ({porcentagem*100:.0f}%)")
                
                st.markdown("---")

    # ------------------------
    # Seção de Efeitos
    # ------------------------
    st.subheader("⚡ Efeitos Ativos")
    
    if not p.efeitos:
        st.info("Nenhum efeito ativo no momento.")
    else:
        # Exibe efeitos em cards
        cols = st.columns(min(len(p.efeitos), 3))
        for i, efeito in enumerate(p.efeitos):
            with cols[i % 3]:
                with st.container(border=True):
                    st.write(f"**{efeito.nome}**")
                    if efeito.duracao == 1:
                        st.write(f"🕐 {efeito.duracao} turno restante")
                    else:
                        st.write(f"🕐 {efeito.duracao} turnos restantes")

    # ------------------------
    # Gerenciar Efeitos (apenas se pode editar)
    # ------------------------
    pode_editar_efeitos = True
    if eh_privado and st.session_state.user_type == "Jogador":
        pode_editar_efeitos = False

    if pode_editar_efeitos:
        with st.expander("⚙️ Gerenciar Efeitos"):
            col_remover, col_adicionar = st.columns(2)
            
            # Remover efeitos
            with col_remover:
                st.markdown("**🗑️ Remover Efeito**")
                if p.efeitos:
                    efeito_para_remover = st.selectbox(
                        "Selecione um efeito para remover:",
                        options=[e.nome for e in p.efeitos],
                        index=None,
                        placeholder="Escolha um efeito...",
                        key=f"{p.nome}_remover_efeito"
                    )
                    if st.button("🗑️ Remover Efeito", key=f"{p.nome}_btn_remover"):
                        if efeito_para_remover:
                            p.efeitos = [e for e in p.efeitos if e.nome != efeito_para_remover]
                            st.success(f"Efeito '{efeito_para_remover}' removido!")
                            st.rerun()
                else:
                    st.info("Nenhum efeito para remover.")
            
            # Adicionar efeitos
            with col_adicionar:
                st.markdown("**➕ Adicionar Efeito**")
                novo_efeito = st.text_input(
                    "Nome do efeito:", 
                    key=f"{p.nome}_novo_efeito",
                    placeholder="Ex: Envenenado, Abençoado..."
                )
                duracao_efeito = st.number_input(
                    "Duração (turnos):", 
                    min_value=1, 
                    max_value=100, 
                    value=3, 
                    step=1, 
                    key=f"{p.nome}_duracao"
                )
                if st.button("➕ Adicionar Efeito", key=f"{p.nome}_btn_adicionar"):
                    if novo_efeito.strip():
                        # Verifica se já existe um efeito com o mesmo nome
                        nomes_existentes = [e.nome.lower() for e in p.efeitos]
                        if novo_efeito.lower() in nomes_existentes:
                            st.warning("⚠️ Já existe um efeito com este nome!")
                        else:
                            p.efeitos.append(Efeito(novo_efeito.strip(), duracao_efeito))
                            st.success(f"Efeito '{novo_efeito}' adicionado!")
                            st.rerun()
                    else:
                        st.error("❌ Por favor, insira um nome para o efeito.")
    else:
        st.info("ℹ️ Apenas o mestre pode gerenciar efeitos de personagens privados.")

    # ------------------------
    # Seção de Informações Adicionais
    # ------------------------
    with st.expander("ℹ️ Informações do Personagem"):
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.markdown("**📋 Detalhes:**")
            st.write(f"• Nome: {p.nome}")
            st.write(f"• Barras de Status: {len(p.barras)}")
            st.write(f"• Efeitos Ativos: {len(p.efeitos)}")
            
        with col_info2:
            st.markdown("**⚔️ Combate:**")
            if hasattr(p, 'iniciativa'):
                if p.iniciativa > 0:
                    st.write(f"• Iniciativa: {p.iniciativa}")
                    # Verifica posição na lista de iniciativa
                    from models.memory import Memory
                    memory_temp = Memory()
                    if p in memory_temp.lista_iniciativa:
                        posicao = memory_temp.lista_iniciativa.index(p) + 1
                        st.write(f"• Posição no Combate: {posicao}º")
                    else:
                        st.write("• Posição no Combate: Fora do combate")
                else:
                    st.write("• Iniciativa: Não definida")
            
            if hasattr(p, 'criado_por'):
                st.write(f"• Criado por: {p.criado_por}")
            
            if eh_privado:
                st.write("• Tipo: NPC Privado 🔒")
            else:
                st.write("• Tipo: Personagem Público 🌐")

    # ------------------------
    # Botões de ação
    # ------------------------
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔙 Voltar para Home", key=f"{p.nome}_voltar_home"):
            st.session_state.current_page = "home"
            st.rerun()
    
    with col2:
        if st.button("👥 Ver Todos os Personagens", key=f"{p.nome}_ver_todos"):
            st.session_state.current_page = "ver"
            st.rerun()
    
    with col3:
        # Apenas o mestre pode deletar NPCs, e jogadores podem deletar seus próprios personagens
        pode_deletar = False
        if st.session_state.user_type == "Mestre":
            pode_deletar = True
        elif not eh_privado:  # Personagem público
            pode_deletar = True
        
        if pode_deletar:
            if st.button("🗑️ Deletar Personagem", key=f"{p.nome}_deletar", type="secondary"):
                # Confirmação via dialog
                st.session_state[f"confirmar_delete_{p.nome}"] = True
                st.rerun()
        else:
            st.caption("⚠️ Sem permissão para deletar")

    # Dialog de confirmação de deleção
    if st.session_state.get(f"confirmar_delete_{p.nome}", False):
        st.markdown("---")
        st.error("⚠️ **ATENÇÃO: Esta ação é irreversível!**")
        
        col_confirm1, col_confirm2 = st.columns(2)
        
        with col_confirm1:
            if st.button("✅ Confirmar Deleção", key=f"{p.nome}_confirmar_deletar", type="primary"):
                # Remove o personagem da memória global
                from models.memory import Memory
                memory_instance = Memory()
                memory_instance.personagens = [char for char in memory_instance.personagens if char.nome != p.nome]
                
                # Remove da lista de iniciativa se estiver lá
                memory_instance.lista_iniciativa = [char for char in memory_instance.lista_iniciativa if char.nome != p.nome]
                
                st.success(f"Personagem '{p.nome}' deletado com sucesso!")
                st.session_state.current_page = "home"
                st.rerun()
        
        with col_confirm2:
            if st.button("❌ Cancelar", key=f"{p.nome}_cancelar_deletar"):
                st.session_state[f"confirmar_delete_{p.nome}"] = False
                st.rerun()