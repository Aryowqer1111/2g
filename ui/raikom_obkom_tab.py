import streamlit as st


def _queue_effect(payload: dict) -> None:
    # 🔹 НОВОЕ: UI только ставит эффекты в очередь вложенного state (без прямой правки метрик)
    nested = st.session_state.get("state")
    if nested is None:
        return
    nested.setdefault("pending_effects", []).append(payload)


def render_raikom_obkom_panel(key_prefix: str = "rbk_") -> None:
    if not st.session_state.get("obkom_unlocked", False):
        return

    st.divider()
    st.subheader("🏛 Региональная власть: Обком")
    st.caption("Формальные планы и неформальные кланы; риск КГБ накапливается.")

    clan = float(st.session_state.get("clan_affinity", 50.0))
    corr = float(st.session_state.get("corruption_risk", 0.0))

    t = max(0.0, min(1.0, clan / 100.0))
    r = int(40 + t * 215)
    b = int(180 - t * 120)
    g = int(80 - t * 40)
    label = "Москва" if clan < 45 else ("Баланс" if clan <= 55 else "Регион")
    st.markdown(
        f'<p style="color:rgb({r},{g},{b});font-weight:600;">Клановая близость: {clan:.0f}/100 — {label}</p>',
        unsafe_allow_html=True,
    )
    st.progress(clan / 100.0)

    if corr > 5.0:
        st.markdown(
            '<p style="color:red;font-weight:bold;animation:blink 1s linear infinite;">'
            "⚠️ corruption_risk высокий</p>"
            "<style>@keyframes blink{50%{opacity:0.2}}</style>",
            unsafe_allow_html=True,
        )
    else:
        st.metric("corruption_risk", f"{corr:.1f} / 10")

    st.caption(f"plan_pressure: {float(st.session_state.get('plan_pressure', 1.0)):.2f}")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📉 Фальсификация плана", key=f"{key_prefix}btn_falsify_plan"):
            _queue_effect(
                {
                    "type": "career_score_delta",
                    "delta": 20.0,
                    "source": "reporting",
                    "log": "⚙️ Отчётность скорректирована",
                }
            )
            _queue_effect({"target": "corruption_risk", "delta": 1.0, "source": "reporting"})
            st.rerun()
    with c2:
        if st.button("🤝 Запрос в клан", key=f"{key_prefix}btn_clan_request"):
            _queue_effect({"type": "career_faction_support_delta", "delta": -15.0, "source": "clan"})
            _queue_effect({"target": "clan_affinity", "delta": 15.0, "source": "clan"})
            _queue_effect({"type": "clan_request_bonus", "delta": 0.0, "source": "clan"})
            st.rerun()
