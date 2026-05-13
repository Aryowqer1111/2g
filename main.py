import streamlit as st
from state.init import init_game, init_cc_data
from ui.sidebar import render_sidebar
from ui.cc_tab import render_cc_tab
from ui.povestka_tab import render_povestka_tab
from ui.commission_panel import render_commission_panel
from ui.career_tab import render_career_tab
from ui.politburo_tab import render_politburo_tab

def main():
    st.set_page_config(page_title="☭ СССР: Политбюро", page_icon="🏛", layout="wide")
    init_game(); init_cc_data()
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📜 Повестка", "🏛 ЦК КПСС", "⚙️ Комиссии", "🏛 Политбюро", "📊 Экономика", "👤 Карьера", "📜 Журнал"])
    with tab1: render_povestka_tab()
    with tab2: render_cc_tab()
    with tab3: render_commission_panel()
    with tab4: render_politburo_tab()
    with tab5: st.header("Макроэкономика"); st.info("Подключение отрасли промышленности в следующем блоке.")
    with tab6: render_career_tab()
    with tab7: st.header("Журнал событий"); [st.text(l) for l in st.session_state.logs[:20]]
    render_sidebar()

if __name__ == "__main__": main()