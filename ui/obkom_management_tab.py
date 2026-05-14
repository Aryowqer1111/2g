# 🔹 НОВОЕ: региональное управление — секретариат, телефонное право, жалобы, пленум (только pending_effects)
import pandas as pd
import streamlit as st

from ui.raikom_obkom_tab import _queue_effect, render_raikom_obkom_panel

PLENUM_INITIATIVES = [
    "Смена директора комбината",
    "Коррекция плана (без срыва отчётности)",
    "Кадровые перестановки в аппарате",
    "Ужесточение субподряда и снабжения",
]


def render_obkom_management_tab() -> None:
    st.header("🏬 Регион: Райком / Обком", divider=True)
    st.caption(
        "Месячный такт симуляции: ваши решения ставятся в очередь `pending_effects` и применяются в конце хода."
    )

    st.metric("political_capital", f"{float(st.session_state.get('political_capital', 40.0)):.0f}")
    st.metric("kgb_attention", f"{float(st.session_state.get('kgb_attention', 8.0)):.1f} / 30")

    deps = st.session_state.get("obkom_secretariat")
    if deps:
        st.subheader("Секретариат обкома (4 заместителя)")
        st.dataframe(pd.DataFrame(deps), use_container_width=True, hide_index=True)

    dilemma = st.session_state.get("secretariat_dilemma")
    if dilemma and isinstance(dilemma, dict):
        st.subheader("📋 Совещание аппарата")
        st.markdown(f"**{dilemma.get('title', '')}**")
        st.write(dilemma.get("body", ""))
        opts = dilemma.get("options") or []
        key = str(dilemma.get("key", ""))
        cols = st.columns(len(opts))
        for i, opt in enumerate(opts):
            label = {"mediate": "Посредничество", "purge": "Жёсткая зачистка", "escalate_cc": "Эскалация в ЦК",
                     "optimistic_report": "Оптимистичный отчёт", "honest_report": "Честный отчёт", "delay": "Тянуть время",
                     "find_scapegoat": "Найти козла отпущения", "circle_wagons": "Круговая порука", "open_inquiry": "Открытое разбирательство"}.get(opt, opt)
            with cols[i]:
                if st.button(label, key=f"sec_{key}_{opt}"):
                    _queue_effect({"type": "secretariat_choice", "scenario_key": key, "choice": str(opt), "source": "player"})
                    st.rerun()

    st.divider()
    st.subheader("📞 Телефонное право")
    st.caption("Прямой звонок министру / куратору фракции в ЦК: бонус плана и репутации, цена political_capital и рост corruption_risk.")
    if st.button("Позвонить в ЦК (стоит 8 political_capital)", key="btn_phone_right"):
        _queue_effect({"type": "phone_right_minister", "cost": 8.0, "source": "player"})
        st.rerun()

    st.divider()
    st.subheader("📨 Жалобы трудящихся")
    pq = list(st.session_state.get("petitions_queue") or [])
    if not pq:
        st.info("Нет активных жалоб (новые появляются в ходе месяцев).")
    else:
        for p in pq:
            st.markdown(f"**{p.get('source')}** — {p.get('text')}")
            c1, c2, c3 = st.columns(3)
            pid = str(p.get("id", ""))
            with c1:
                if st.button("Игнор", key=f"pet_ign_{pid}"):
                    _queue_effect({"type": "petition_resolve", "petition_id": pid, "action": "ignore", "source": "player"})
                    st.rerun()
            with c2:
                if st.button("Исполнить", key=f"pet_ful_{pid}"):
                    _queue_effect({"type": "petition_resolve", "petition_id": pid, "action": "fulfill", "source": "player"})
                    st.rerun()
            with c3:
                if st.button("Отказ без причины", key=f"pet_rej_{pid}"):
                    _queue_effect({"type": "petition_resolve", "petition_id": pid, "action": "reject_unfair", "source": "player"})
                    st.rerun()

    st.divider()
    st.subheader("🏛 Пленум обкома (раз в 6 месяцев)")
    if st.session_state.get("regional_plenum_open"):
        st.warning("Созван пленум: вынесите две инициативы.")
        a = st.selectbox("Инициатива 1", PLENUM_INITIATIVES, key="plenum_a")
        b = st.selectbox("Инициатива 2", PLENUM_INITIATIVES, key="plenum_b")
        if st.button("Провести голосование", key="btn_plenum_vote"):
            _queue_effect({"type": "regional_plenum_vote", "init1": a, "init2": b, "source": "player"})
            st.rerun()
    else:
        st.caption("Следующий пленум по счётчику месяцев (см. журнал при созыве).")

    st.divider()
    st.subheader("Аппарат и герой ЦК")
    apparatus = st.session_state.get("obkom_apparatus")
    hero_id = st.session_state.get("obkom_hero_cc_id")
    cc_df = st.session_state.get("cc_members")
    if apparatus:
        st.caption("≈95% должностей — не члены ЦК; герой из ЦК в резерве до выдвижения (шкала ascent / назначение в конце хода).")
        st.dataframe(pd.DataFrame(apparatus), use_container_width=True, hide_index=True)
    if hero_id and cc_df is not None and not cc_df.empty:
        hit = cc_df[cc_df["ID"].astype(str) == str(hero_id)]
        if not hit.empty:
            r = hit.iloc[0]
            st.markdown(
                f"**Главный герой (ЦК):** {r['ФИО']} — амбиции **{r['Амбиции']:.0f}**. "
                f"В аппарат обкома не входит, пока его туда не выдвинут (или ascent ≥ 100)."
            )
            st.progress(min(float(st.session_state.get("obkom_hero_ascent", 0.0)) / 100.0, 1.0))
            st.caption(f"obkom_hero_seated: {st.session_state.get('obkom_hero_seated', False)}")

    st.divider()
    st.subheader("Региональные рычаги (после разблокировки Обкома)")
    render_raikom_obkom_panel(key_prefix="mgmt_rbk_")
