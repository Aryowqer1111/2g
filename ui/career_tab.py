import streamlit as st
from core.politics.career import CAREER_TIERS, CareerSystem
from data.regions_db import REGION_META

def render_career_tab():
    st.header("👤 Карьера Игрока", divider=True)
    
    career = st.session_state.get("career")
    profile = st.session_state.get("player_profile")

    if career is None:
        st.session_state.career = CareerSystem()
        career = st.session_state.career
        
    if profile is None:
        st.warning("⚠️ Персонаж не создан. Нажмите '🛠 Сбросить симуляцию' и создайте нового.")
        return

    region_name = "Без назначения"
    if career.region_assignment and career.region_assignment in REGION_META:
        region_name = REGION_META[career.region_assignment]["name"]

    st.subheader(f"📋 {profile.get('name', 'Аппаратчик')} | {region_name}")
    st.caption(f"Возраст: {profile.get('age', '?')} | Фракция: {profile.get('faction', '?')} | ID: {profile.get('id', '?')}")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1: st.metric("Текущий ранг", CAREER_TIERS[career.level_idx].name)
    with col2:
        threshold = CAREER_TIERS[career.level_idx].score_threshold
        st.write("Прогресс до следующего уровня:")
        st.progress(min(career.score / max(threshold, 1), 1.0))
        st.caption(f"Набрано очков: {int(career.score)}")
    with col3: st.metric("Силовой вес", f"{CAREER_TIERS[career.level_idx].plenum_vote_power}x")

    st.divider()
    st.subheader("📊 Политический капитал")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌟 Репутация", f"{career.reputation:.0f}"); c1.progress(career.reputation/100)
    c2.metric("⚠️ Инциденты", career.disciplinary_incidents)
    if career.incident_decay_months > 0: c2.caption(f"Штраф: {career.incident_decay_months} мес.")
    c3.metric("🤝 Фракция", f"{career.faction_support:.0f}%"); c3.progress(career.faction_support/100)
    c4.metric("🏛 Блок", f"{career.block_support:.0f}%"); c4.progress(career.block_support/100)

    st.divider()
    st.markdown("**🔐 Разблокированные права:**")
    for p in career.get_permissions(): st.success(f"• {p.replace('_', ' ').title()}")