import streamlit as st

def render_povestka_tab():
    st.header("Текущая повестка Политбюро")
    st.info("Здесь будут появляться события из `data/events_db.py` и инициативы фракций.")
    st.divider()
    with st.container(border=True):
        st.subheader("🏭 Расширение хозрасчёта")
        st.write("Минфин предлагает пилотное внедрение самостоятельности предприятий.")
        c1, c2 = st.columns(2)
        if c1.button("✅ Утвердить пилот"): st.toast("Реформа запущена")
        if c2.button("❌ Отложить"): st.toast("Вопрос снят")