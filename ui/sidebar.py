import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("☭ Управление")
        # 🔹 ИСПРАВЛЕНО: используем .get() и подстраховываемся через or 0.0
        month = st.session_state.get("month", 1)
        year = st.session_state.get("year", 1960)
        st.metric("📅 Дата", f"{month:02d}.{year}")

        # 🔹 ИСПРАВЛЕНО: используем .get() и подстраховываемся через or 0.0, затем форматирование
        c1, c2 = st.columns(2)
        # Стабильность
        stability_val = st.session_state.get("stability")
        c1.metric("⚖️ Стаб.", f"{stability_val:.1f}" if stability_val is not None else "0.0")
        # Бюджет
        budget_val = st.session_state.get("budget")
        c2.metric("💰 Бюджет", f"{budget_val:.1f}%" if budget_val is not None else "0.0%")
        # Поддержка
        support_val = st.session_state.get("support")
        st.metric("❤️ Поддержка", f"{support_val:.1f}" if support_val is not None else "0.0")

        st.divider()

        if st.button("⏭ Следующий месяц", type="primary", key="btn_next_month"):
            state = st.session_state.get("state")
            loop = st.session_state.get("loop")

            if state and loop:
                loop.tick(state)
                st.rerun()
            else:
                st.error("⚠️ Движок не инициализирован.")

        st.divider()
        if st.button("🛠️ Сбросить симуляцию", key="btn_reset", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()