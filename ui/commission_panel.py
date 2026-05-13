import streamlit as st
import pandas as pd
from core.politics.career import CAREER_TIERS
from data.skills_config import COMMITTEE_BONUS_MAP

def render_commission_panel():
    st.header("🏛 Управление Комиссиями ЦК", divider=True)
    
    cc_df = st.session_state.get("cc_members")
    comm_eng = st.session_state.get("committee_engine")
    skills_eng = st.session_state.get("skills_engine")
    career = st.session_state.get("career")
    is_high_rank = career and career.level_idx >= 4
    
    if cc_df is None or comm_eng is None or skills_eng is None: 
        st.warning("Данные не загружены."); return

    st.subheader("📊 Влияние комиссий на государство (за ход)")
    effects = {"🏛 Бюджет": 0.0, "⚖️ Стабильность": 0.0, "👥 Поддержка": 0.0, "🛡 Безопасность": 0.0, "📜 Идеология": 0.0, "🌍 Престиж": 0.0}
    
    for mid, commits in comm_eng.members_assignments.items():
        for comm in commits:
            bonus = skills_eng.calculate_committee_bonus(str(mid), comm)
            target = COMMITTEE_BONUS_MAP.get(comm, {})
            for k, w in target.items():
                name_map = {"budget":"🏛 Бюджет","stability":"⚖️ Стабильность","support":"👥 Поддержка","security":"🛡 Безопасность","ideology":"📜 Идеология","prestige":"🌍 Престиж"}
                if k in name_map: effects[name_map[k]] += bonus * w

    cols = st.columns(6)
    for i, (name, val) in enumerate(effects.items()):
        cols[i].metric(name, f"+{val:.2f}")
        
    st.divider()
    
    selected_comm = st.selectbox("Выберите комиссию:", comm_eng.available_committees)
    info = comm_eng.get_committee_info(selected_comm)
    st.info(info["desc"])
    
    col_left, col_right = st.columns([1, 2])
    with col_left:
        min_lvl = st.number_input("Мин. навык", value=5.0, step=0.5)
        skill_req = st.radio("Приоритет:", ["Хозяйственность","Интриги","Дипломатия","Военное дело"], horizontal=True)
        candidates, head_id = [], str(info["head_id"]) if info["head_id"] else None
        
        for _, row in cc_df.iterrows():
            sid = str(row["ID"])
            if sid in comm_eng.members_assignments or sid == head_id: continue
            sk = skills_eng.competencies.get(sid, {})
            if sk.get(skill_req, 0) >= min_lvl: 
                candidates.append({"ФИО": row["ФИО"], skill_req: round(sk[skill_req],1), "ID": sid})
                
        cand_df = pd.DataFrame(candidates).sort_values(by=skill_req, ascending=False)
        st.dataframe(cand_df, use_container_width=True, hide_index=True, height=250)

    with col_right:
        st.subheader(f"Состав: {selected_comm}")
        current_ids = [str(m) for m in comm_eng.committee_members.get(selected_comm, [])]
        if current_ids:
            st.dataframe(cc_df[cc_df["ID"].isin(current_ids)][["ФИО","Фракция","Здоровье"]], use_container_width=True, hide_index=True)
        else: 
            st.warning("Комиссия пуста")

        st.divider()
        st.markdown("#### 👑 Назначение Главы Комиссии")
        if current_ids:
            name_map = {str(row["ID"]): row["ФИО"] for _, row in cc_df.iterrows()}
            head_opts = [cid for cid in current_ids if cid in name_map]
            selected_head = st.selectbox("Выберите главу:", options=[None]+head_opts, format_func=lambda x: name_map.get(str(x), str(x)) if x else "Сохранить текущего")
            if st.button("✅ Утвердить Главу", key=f"btn_head_{selected_comm}"):
                if selected_head:
                    comm_eng.set_head(selected_comm, selected_head)
                    st.toast("👑 Глава назначен"); st.rerun()
        
        st.divider()
        if is_high_rank:
            st.success("🔓 Ручное назначение доступно (Политбюро/Генсек)")
            sel_id = st.selectbox("Кандидат:", options=cand_df["ID"].tolist() if not cand_df.empty else [], key=f"sel_cand_{selected_comm}")
            if st.button("📝 Назначить вручную", key=f"btn_manual_{selected_comm}"):
                if comm_eng.assign_member_to_committee(sel_id, selected_comm): 
                    st.toast("✅ Назначено"); st.rerun()
        else:
            st.info("🔒 Ручное назначение только с ранга 'Член Политбюро'.")