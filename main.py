import streamlit as st

from state.init import init_cc_data, init_game
from ui.career_tab import render_career_tab
from ui.cc_tab import render_cc_tab
from ui.character_creation import render_character_creation
from ui.commission_panel import render_commission_panel
from ui.obkom_window import render_obkom_window
from ui.politburo_tab import render_politburo_tab
from ui.povestka_tab import render_povestka_tab
from ui.sidebar import render_sidebar


def main():
    st.set_page_config(page_title="☭ СССР: Политбюро", page_icon="🏛", layout="wide")
    init_game()
    init_cc_data()

    if st.session_state.get("player_profile") is None:
        render_character_creation()
        return

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        [
            "📜 Повестка",
            "🏛 ЦК КПСС",
            "⚙️ Комиссии",
            "🏛 Политбюро",
            "📊 Экономика",
            "👤 Карьера",
            "🏬 Райком/Обком",
            "📜 Журнал",
        ]
    )
    with tab1:
        render_povestka_tab()
    with tab2:
        render_cc_tab()
    with tab3:
        render_commission_panel()
    with tab4:
        render_politburo_tab()
    with tab5:
        st.header("Макроэкономика")
        st.info("Подключение отрасли промышленности в следующем блоке.")
    with tab6:
        render_career_tab()
    with tab7:
        render_obkom_window()
    with tab8:
        st.header("Журнал событий")
        for log in (st.session_state.get("logs") or [])[:20]:
            st.text(log)
    render_sidebar()


if __name__ == "__main__":
    main()
