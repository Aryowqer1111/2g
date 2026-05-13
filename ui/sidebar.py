import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("☭ Управление")
        st.metric("📅 Дата", f"{st.session_state.get('month',1):02d}.{st.session_state.get('year',1960)}")
        c1, c2 = st.columns(2)
        c1.metric("⚖️ Стаб.", f"{st.session_state.get('stability', 0):.1f}")
        c2.metric("💰 Бюджет", f"{st.session_state.get('budget', 0):.1f}%")
        st.metric("❤️ Поддержка", f"{st.session_state.get('support', 0):.1f}")
        st.divider()

        if st.button("⏭ Следующий месяц", type="primary", key="btn_next_month"):
            state = st.session_state.get("state")
            loop = st.session_state.get("loop")
            if state and loop:
                loop.tick(state)
                # 🔹 Синхронизируем ВСЕ ключи из state в session_state
                for k, v in state.items():
                    if k not in ["loop", "faction_engine", "committee_engine", "skills_engine"]:
                        st.session_state[k] = v
                st.rerun()
            else:
                st.error("⚠️ Движок не инициализирован.")

        st.divider()
        if st.button("🛠️ Сбросить симуляцию", key="btn_reset", type="secondary"):
            for key in list(st.session_state.keys()): del st.session_state[key]
            st.rerun()