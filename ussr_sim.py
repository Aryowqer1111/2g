import streamlit as st
import random

# 🔹 1. Инициализация состояния
def init_state():
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.year = 1960
        st.session_state.month = 1
        st.session_state.turn = 0
        st.session_state.leader = "Н.С. Хрущёв"
        
        # Ключевые показатели
        st.session_state.stability = 65.0
        st.session_state.budget = 50.0
        st.session_state.support = 60.0
        st.session_state.ideology = 70.0
        
        # Механики
        st.session_state.succession_active = False
        st.session_state.current_event = None
        st.session_state.event_log = ["📜 Игра началась. Январь 1960."]
        
        # Фракции
        st.session_state.factions = {
            "Идеологи": {"leader": "М. Суслов", "influence": 60, "loyalty": 55},
            "Реформаторы": {"leader": "А. Косыгин", "influence": 45, "loyalty": 65},
            "ВПК": {"leader": "Д. Устинов", "influence": 70, "loyalty": 50},
            "КГБ": {"leader": "Ю. Андропов", "influence": 55, "loyalty": 60},
            "Регионы": {"leader": "Л. Брежнев", "influence": 50, "loyalty": 70}
        }

# 🔹 2. Игровая логика
def generate_event():
    # Если активна преемственность, возвращаем спец. событие
    if st.session_state.succession_active:
        return {
            "title": "⏳ Избрание нового Генсека", 
            "text": "Внеочередной Пленум ЦК. Повестка приостановлена до избрания лидера.", 
            "choices": [], 
            "type": "succession"  # 🔹 Важно!
        }
        
    # Пул обычных событий
    events = [
        {
            "title": "🌾 Неурожай в Поволжье", 
            "text": "Дефицит зерна. Требуется решить: закупить за валюту или ужесточить нормы.",
            "choices": [
                {"text": "Закупить в США/Канаде", "effects": {"stability": 3, "budget": -4, "support": 4}},
                {"text": "Ужесточить карточную систему", "effects": {"stability": -3, "budget": 1, "support": -5}},
                {"text": "Мобилизовать резервы", "effects": {"stability": 0, "budget": -2, "support": -1}}
            ],
            "type": "normal"  # 🔹 Добавлено
        },
        {
            "title": "🏭 Перевыполнение плана", 
            "text": "Машиностроители отчитались о росте на 15%. Как распределить сверхплановую продукцию?",
            "choices": [
                {"text": "Премии и грамоты", "effects": {"stability": 2, "budget": -1, "support": 3}},
                {"text": "Направить на экспорт", "effects": {"stability": 1, "budget": 3, "support": 0}},
                {"text": "Повысить план на след. год", "effects": {"stability": -1, "budget": 2, "support": -2}}
            ],
            "type": "normal"  # 🔹 Добавлено
        },
        {
            "title": "📜 Инициатива Политбюро", 
            "text": "Предложение о расширении хозрасчёта на предприятиях. Одобряем или тормозим?",
            "choices": [
                {"text": "Утвердить реформу", "effects": {"stability": 2, "budget": 1, "support": 2, "ideology": -3}},
                {"text": "Пилотный проект на 10 заводах", "effects": {"stability": 1, "budget": 0, "support": 1}},
                {"text": "Сохранить централизацию", "effects": {"stability": 0, "budget": 0, "support": -2, "ideology": 2}}
            ],
            "type": "normal"  # 🔹 Добавлено
        },
        {
            "title": "⚠️ Дефицит запчастей", 
            "text": "Железные дороги испытывают срыв графика. Требуется экстренное решение.",
            "choices": [
                {"text": "Выделить резерв Госплана", "effects": {"stability": 2, "budget": -3, "support": 2}},
                {"text": "Ввести режим жёсткой экономии", "effects": {"stability": 0, "budget": 2, "support": -3}},
                {"text": "Перераспределить с лёгкой пром.", "effects": {"stability": -1, "budget": 0, "support": -2}}
            ],
            "type": "normal"  # 🔹 Добавлено
        }
    ]
    return random.choice(events)

def apply_choice(effects):
    for key, val in effects.items():
        if key in st.session_state:
            st.session_state[key] = max(0, min(100, st.session_state[key] + val))
            
def advance_turn():
    st.session_state.month += 1
    if st.session_state.month > 12:
        st.session_state.month = 1
        st.session_state.year += 1
    st.session_state.turn += 1
    
    # Пассивные изменения
    st.session_state.stability += random.uniform(-1.5, 1.5)
    st.session_state.budget += random.uniform(-1, 1)
    
    # Исторический триггер Хрущёва
    if st.session_state.leader == "Н.С. Хрущёв" and st.session_state.year >= 1964 and st.session_state.month >= 10:
        st.session_state.succession_active = True
        st.session_state.event_log.insert(0, "⚖️ Октябрь 1964: Пленум ЦК отстранил Хрущёва. Требуются выборы.")
        st.session_state.current_event = None

# 🔹 3. UI
def main():
    st.set_page_config(page_title="СССР: Политический Симулятор", page_icon="🚩", layout="wide")
    init_state()
    
    # === SIDEBAR: СТАТИСТИКА ===
    with st.sidebar:
        st.header("🚩 СССР: Политический Симулятор")
        st.metric("📅 Дата", f"{st.session_state.month:02d}.{st.session_state.year}")
        st.metric("👑 Генсек", st.session_state.leader)
        st.divider()
        
        c1, c2 = st.columns(2)
        c1.metric("📊 Стабильность", f"{st.session_state.stability:.1f}")
        c2.metric("💰 Бюджет", f"{st.session_state.budget:.1f}%")
        c1.metric("👥 Поддержка", f"{st.session_state.support:.1f}")
        c2.metric("📕 Идеология", f"{st.session_state.ideology:.1f}")
        
        st.divider()
        st.subheader("🏛 Фракции")
        for name, data in st.session_state.factions.items():
            st.progress(data["influence"]/100, text=f"{name} ({data['leader']}) | Влияние: {data['influence']:.0f}%")
            
        st.divider()
        if st.button("⏭ Следующий ход", type="primary"):
            if not st.session_state.succession_active:
                advance_turn()
                st.session_state.current_event = generate_event()
                st.session_state.event_log.insert(0, f"📅 Ход #{st.session_state.turn}: {st.session_state.current_event['title']}")
            st.rerun()
            
        if st.button("🛠️ Dev: Сбросить игру"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # === MAIN: ВКЛАДКИ ===
    tab1, tab2, tab3, tab4 = st.tabs(["📜 Повестка", "👤 Игрок", "⚙️ ЦК КПСС", "📊 Лог"])
    
    with tab1:
        st.header("Повестка Политбюро")
        
        if st.session_state.current_event is None:
            st.session_state.current_event = generate_event()
            
        ev = st.session_state.current_event
        
        # 🔹 Проверка типа события
        if ev.get("type") == "succession":
            st.warning("🔴 Требуется избрание нового Генерального секретаря")
            if st.button("🗳 Открыть Пленум ЦК и провести выборы", type="primary"):
                # Простая логика выборов: победитель по влиянию + случайный шум
                candidates = st.session_state.factions
                winner_name = max(candidates, key=lambda k: candidates[k]["influence"] + random.uniform(-10, 10))
                new_leader = candidates[winner_name]["leader"]
                
                st.session_state.leader = new_leader
                st.session_state.stability += 5
                st.session_state.support += 5
                st.session_state.succession_active = False
                st.session_state.event_log.insert(0, f"👑 {new_leader} избран Генсеком!")
                st.session_state.current_event = generate_event()
                st.rerun()
        else:
            st.subheader(ev["title"])
            st.write(ev["text"])
            
            st.divider()
            cols = st.columns(3)
            for i, ch in enumerate(ev["choices"]):
                if cols[i].button(ch["text"], key=f"choice_{i}"):
                    apply_choice(ch["effects"])
                    st.session_state.event_log.insert(0, f"✅ Выбрано: {ch['text']}")
                    st.session_state.current_event = None
                    st.rerun()
                    
    with tab2:
        st.header("👤 Досье Аппаратчика")
        st.info("Здесь можно добавить: Авторитет, Связи, Стресс, Отношения с Генсеком.")
        st.metric("📅 Срок в должности", f"{st.session_state.turn} ходов")
        st.metric("🎯 Амбиции", "55%")
        
    with tab3:
        st.header("⚙️ Центральный Комитет КПСС")
        st.info("Пленум собирается 2-4 раза в год. Утверждает планы и кадровые решения.")
        if st.session_state.year >= 1965:
            st.success("✅ Статус: Действующий состав ЦК одобрен XXIII съездом")
        else:
            st.warning("⏳ Статус: Подготовка к съезду")
        st.divider()
        st.subheader("Список утверждённых решений")
        st.text("• Директивы IX пятилетки")
        st.text("• Расширение прав министерств")
        st.text("• Мелиорация Нечерноземья")
        
    with tab4:
        st.header("📊 Журнал событий")
        for log in st.session_state.event_log[:20]:
            st.text(log)

if __name__ == "__main__":
    main()