import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("☭ Управление")
        # 🔴 БЫЛО: st.session_state.get("week ", 1), "📅 Дата ", "⚖️ Стаб. "
        # 🟢 ИСПРАВЛЕНО: чистые ключи + возврат к месячному отображению
        month = st.session_state.get("month", 1)
        year = st.session_state.get("year", 1960)
        st.metric("📅 Дата", f"{month:02d}.{year}")
        
        c1, c2 = st.columns(2)
        c1.metric("⚖️ Стаб.", f"{st.session_state.get('stability', 0):.1f}")
        c2.metric("💰 Бюджет", f"{st.session_state.get('budget', 0):.1f}%")
        st.metric("❤️ Поддержка", f"{st.session_state.get('support', 0):.1f}")
        st.divider()

        # 🔴 БЫЛО: key="btn_next_week ", label="⏭ Пропустить неделю "
        # 🟢 ИСПРАВЛЕНО: чистые key и label + возврат к "Следующий месяц"
        if st.button("⏭ Следующий месяц", type="primary", key="btn_next_month"):
            state = st.session_state.get("state")
            loop = st.session_state.get("loop")
            
            if state and loop:
                loop.tick(state)
                for k in ["month", "year", "turn", "stability", "budget", "support", "logs", "cc_members"]:
                    if k in state:
                        st.session_state[k] = state[k]
                st.rerun()
            else:
                st.error("⚠️ Движок не инициализирован.")

        st.divider()
        if st.button("🛠️ Сбросить симуляцию", key="btn_reset", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()