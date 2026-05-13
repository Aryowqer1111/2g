import streamlit as st
import pandas as pd

def render_cc_tab():
    df = st.session_state.get("cc_members")
    if df is None: st.warning("Данные ЦК не загружены."); return
    
    comm_eng = st.session_state.get("committee_engine")
    skills_eng = st.session_state.get("skills_engine")
    
    st.header("🏛 Центральный Комитет КПСС", divider=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("👥 Всего", len(df))
    col2.metric("⚖️ Ср. лояльность", f"{df['Лояльность Генсеку'].mean():.1f}")
    col3.metric("📊 Ср. амбиции", f"{df['Амбиции'].mean():.1f}")
    col4.metric("🧠 Ср. идеология", f"{df['Идеология'].mean():.1f}")
    col5.metric("🩺 Ср. здоровье", f"{df['Здоровье'].mean():.1f}")

    st.divider()
    
    # 🔹 ИСПРАВЛЕНО: Безопасный и гарантированный вывод лидеров
    st.subheader("👑 Лидеры фракций", divider=True)
    leaders_data = []
    fac_eng = st.session_state.get("faction_engine")
    
    if fac_eng and hasattr(fac_eng, 'faction_leaders') and fac_eng.faction_leaders:
        for faction, lid in fac_eng.faction_leaders.items():
            lid_str = str(lid)
            # Поиск с двойной проверкой типов (str vs int)
            match = df[df["ID"].astype(str) == lid_str]
            if match.empty: match = df[df["ID"] == lid_str]
                
            if not match.empty:
                r = match.iloc[0]
                leaders_data.append({"Фракция": faction, "Лидер": r["ФИО"], "Лояльность": r["Лояльность Генсеку"], "Амбиции": r["Амбиции"]})
                
    if leaders_data:
        st.dataframe(pd.DataFrame(leaders_data), use_container_width=True, hide_index=True)
    else:
        st.caption("⚠️ Лидеры не назначены. Проверьте, запущена ли генерация ЦК.")

    st.divider()
    st.subheader("⚙️ Загрузка Комиссий ЦК", divider=True)
    load = comm_eng.get_committee_load() if comm_eng else {}
    col_load1, col_load2, col_load3 = st.columns(3)
    for i, (comm, count) in enumerate(load.items()):
        col = [col_load1, col_load2, col_load3][i % 3]
        col.metric(comm, f"{count}/5 чел.", "🟢 Свободно" if count < 5 else "🔴 Полный состав")

    st.divider()
    st.subheader("📊 Карта влияния ЦК", divider=True)
    col_left, col_right = st.columns([3, 1])
    with col_left:
        chart_df = df[["Идеология", "Лояльность Генсеку", "Фракция", "Амбиции"]].copy()
        chart_df = chart_df.rename(columns={"Лояльность Генсеку": "loyalty", "Идеология": "ideology", "Фракция": "faction", "Амбиции": "ambition"})
        chart_df["ideology"] = chart_df["ideology"].clip(-100, 100)
        chart_df["loyalty"] = chart_df["loyalty"].clip(-100, 100)
        st.scatter_chart(chart_df, x="ideology", y="loyalty", color="faction", size="ambition", use_container_width=True, height=400)
    with col_right:
        st.subheader("📈 Баланс фракций")
        stats = df.groupby("Фракция").agg({"Лояльность Генсеку": "mean", "Амбиции": "mean", "ID": "count"}).rename(columns={"ID": "Кол-во"}).round(1)
        st.dataframe(stats, use_container_width=True)

    st.divider()
    st.subheader("📋 Реестр членов ЦК (Сортировка по навыкам)", divider=True)
    df_display = df.copy()
    competencies_map = {row["ID"]: skills_eng.competencies.get(row["ID"], {}) for _, row in df_display.iterrows()} if skills_eng else {}
    if competencies_map:
        df_display[['Военное дело', 'Интриги', 'Дипломатия', 'Хозяйственность']] = pd.DataFrame([competencies_map[row["ID"]] for _, row in df_display.iterrows()])
    
    sortable_df = st.dataframe(df_display, use_container_width=True, height=250, on_select="rerun", selection_mode="single-row", hide_index=True)
    if sortable_df.selection.rows:
        st.session_state.cc_selected_id = df_display.iloc[sortable_df.selection.rows[0]]["ID"]
        
    member = None
    sel_id = st.session_state.get("cc_selected_id")
    if sel_id:
        member_row = df_display[df_display["ID"] == sel_id]
        if not member_row.empty: member = member_row.iloc[0]

    if member is not None:
        with st.expander(f"🔍 Профиль: {member['ФИО']}", expanded=True):
            c1, c2, c3 = st.columns(3)
            c1.metric("Фракция", member["Фракция"]); c1.metric("Возраст", f"{member['Возраст']} лет")
            c2.metric("Здоровье", f"{member['Здоровье']}%"); c2.metric("Лояльность", f"{member['Лояльность Генсеку']:.1f}%")
            c3.metric("Амбиции", f"{member['Амбиции']:.1f}%"); c3.metric("Идеология", f"{member['Идеология']:.1f}")