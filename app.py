import streamlit as st

# Баракчанын баптаулары
st.set_page_config(page_title="Ахмад Академиясы - ҰБТ Порталы", page_icon="🎓", layout="centered")

# Сессияны башкаруу
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Колдонуучулар базасы (Логин, Пароль, Аты-жөнү, Ролу)
if 'users' not in st.session_state:
    st.session_state.users = {
        "student": {"password": "123", "name": "Айбек", "role": "student"},
        "aruzhan": {"password": "123", "name": "Аружан", "role": "student"},
        "admin": {"password": "admin123", "name": "Мектеп Директоры", "role": "director"}
    }

# Багыттар тизмеси
DIRECTIONS = [
    "Математика - Физика",
    "Химия - Биология",
    "Дүниежүзі тарихы - Құқық",
    "География - Математика"
]

# Базадагы суроолор (Сүрөт кошуу мүмкүнчүлүгү менен)
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {
            "direction": "Математика - Физика",
            "type": "single",
            "question": "Синус 30 градуста нешеге тең?",
            "image": "",
            "options": ["0", "0.5", "1", "sqrt(3)/2"],
            "answer": ["0.5"]
        },
        {
            "direction": "Математика - Физика",
            "type": "multiple",
            "question": "Төмендегілердің қайсысы скаляр шамалар болып табылады? (Бірнеше жауап таңдаңыз)",
            "image": "",
            "options": ["Масса", "Үдеу", "Уақыт", "Күш"],
            "answer": ["Масса", "Уақыт"]
        },
        {
            "direction": "Химия - Биология",
            "type": "single",
            "question": "Судың химиялық формуласы қандай?",
            "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1d/Water_molecule_3D.svg/200px-Water_molecule_3D.svg.png",
            "options": ["CO2", "H2O", "NaCl", "O2"],
            "answer": ["H2O"]
        }
    ]

# Тест жыйынтыктарын сактоо
if 'results' not in st.session_state:
    st.session_state.results = [
        {"Оқушы": "Айбек", "Бағыты": "Математика - Физика", "Балл": 10, "Макс": 10},
        {"Оқушы": "Аружан", "Бағыты": "Химия - Биология", "Балл": 5, "Макс": 10}
    ]

# --- СЕРТИФИКАТ КӨРСӨТҮҮ ФУНКЦИЯСЫ ---
def show_certificate(student_name, direction, score, total):
    st.balloons()
    st.markdown(
        f"""
        <div style="border: 10px double #1E3A8A; padding: 30px; text-align: center; background-color: #F8FAFC; border-radius: 15px; margin-top: 20px;">
            <h1 style="color: #1E3A8A; font-family: 'Georgia', serif;">📜 СЕРТИФИКАТ</h1>
            <h3 style="color: #475569;">АХМАД АКАДЕМИЯСЫ</h3>
            <hr style="border: 1px solid #1E3A8A; width: 80%; margin: 20px auto;">
            <p style="font-size: 18px; color: #334155;">Осы сертификат ҰБТ байқау тестін сәтті тапсырғаны үшін</p>
            <h2 style="color: #0F172A; text-decoration: underline;">{student_name}</h2>
            <p style="font-size: 18px; color: #334155;">оқушысына <b>«{direction}»</b> бағыты бойынша беріледі.</p>
            <div style="background-color: #DBEAFE; padding: 15px; border-radius: 10px; display: inline-block; margin: 15px 0;">
                <h3 style="color: #1E40AF; margin: 0;">Нәтижесі: {score} / {total} балл</h3>
            </div>
            <p style="font-size: 14px; color: #64748B; margin-top: 20px;">Ахмад Академиясы сізге ҰБТ-да жоғары балл тілейді! 🚀</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- ЛОГИН ПАНЕЛИ ---
def login_page():
    st.title("🎓 Ахмад Академиясы - ҰБТ Порталы")
    
    username = st.text_input("Логин (Пайдаланушы аты)")
    password = st.text_input("Пароль", type="password")
    
    if st.button("Кіру"):
        if username in st.session_state.users:
            user = st.session_state.users[username]
            if user["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.display_name = user["name"]
                st.session_state.role = user["role"]
                st.rerun()
            else:
                st.error("Пароль қате!")
        else:
            st.error("Мұндай логин табылмады!")

    st.info("""
    **Әдепкі аккаунттар:**
    * 👨‍🎓 **Оқушы кабинеті:** Логин: `student` | Пароль: `123`
    * 👨‍💼 **Директор кабинеті:** Логин: `admin` | Пароль: `admin123`
    """)

# --- ОКУУЧУ КАБИНЕТИ ---
def student_dashboard():
    st.title(f"👨‍🎓 Оқушы кабинеті: {st.session_state.display_name}")
    
    st.subheader("📌 Өз ҰБТ бағытыңызды таңдаңыз:")
    selected_direction = st.selectbox("Бейіндік пәндер комбинациясы:", DIRECTIONS)
    
    st.divider()
    st.write(f"### 📝 Тест бағыты: {selected_direction}")
    
    filtered_questions = [q for q in st.session_state.questions if q["direction"] == selected_direction]
    
    if not filtered_questions:
        st.warning("Бұл бағыт бойынша әлі сұрақтар қосылмаған!")
        return

    # Тест тапшырылып бүткөнүн текшерүү
    test_submitted_key = f"submitted_{selected_direction}"
    
    if test_submitted_key not in st.session_state:
        st.session_state[test_submitted_key] = False

    if not st.session_state[test_submitted_key]:
        user_answers = {}
        for i, q in enumerate(filtered_questions):
            st.write(f"**{i+1}. {q['question']}**")
            
            # Эгер суроодо сүрөт болсо көрсөтүү
            if q.get("image"):
                st.image(q["image"], use_container_width=True)
            
            # Бир жооптуу суроо
            if q.get("type", "single") == "single":
                selected_val = st.radio(
                    "Жауапты таңдаңыз:",
                    q['options'],
                    index=None,
                    key=f"q_{i}_{selected_direction}",
                    label_visibility="collapsed"
                )
                user_answers[i] = [selected_val] if selected_val else []
            # Көп жооптуу суроо
            else:
                selected_opts = []
                st.caption("*(Бірнеше жауап таңдауға болады)*")
                for opt in q['options']:
                    if st.checkbox(opt, key=f"q_{i}_{opt}_{selected_direction}"):
                        selected_opts.append(opt)
                user_answers[i] = selected_opts
            st.write("---")

        if st.button("Тестті аяқтау"):
            score = 0
            total = len(filtered_questions) * 5
            
            for i, q in enumerate(filtered_questions):
                ans = user_answers[i]
                if set(ans) == set(q['answer']):
                    score += 5
                    
            st.session_state.results.append({
                "Оқушы": st.session_state.display_name,
                "Бағыты": selected_direction,
                "Балл": score,
                "Макс": total
            })
            
            # Жыйынтыкты жана колдонуучунун жоопторун сактоо
            st.session_state[test_submitted_key] = True
            st.session_state[f"last_answers_{selected_direction}"] = user_answers
            st.session_state[f"last_score_{selected_direction}"] = score
            st.session_state[f"last_total_{selected_direction}"] = total
            st.rerun()

    else:
        # --- ТЕСТ АЯКТАЛГАНДАН КИЙИНКИ КАТАЛАР МЕНЕН ИШТӨӨ БӨЛҮМҮ ---
        score = st.session_state[f"last_score_{selected_direction}"]
        total = st.session_state[f"last_total_{selected_direction}"]
        saved_answers = st.session_state[f"last_answers_{selected_direction}"]

        show_certificate(st.session_state.display_name, selected_direction, score, total)
        
        st.divider()
        st.subheader("🔍 Тест нәтижелері мен қателерді талдау:")
        
        for i, q in enumerate(filtered_questions):
            u_ans = saved_answers.get(i, [])
            c_ans = q['answer']
            is_correct = set(u_ans) == set(c_ans)
            
            status_symbol = "✅" if is_correct else "❌"
            st.markdown(f"### {i+1}. {q['question']} {status_symbol}")
            
            if q.get("image"):
                st.image(q["image"], width=300)
                
            u_ans_str = ", ".join(u_ans) if u_ans else "Жауап берілмеді"
            c_ans_str = ", ".join(c_ans)
            
            if is_correct:
                st.success(f"**Сіздің жауабыңыз (Дұрыс):** {u_ans_str}")
            else:
                st.error(f"**Сіздің жауабыңыз:** {u_ans_str}")
                st.info(f"**Дұрыс жауап:** {c_ans_str}")
            st.write("---")

        if st.button("Тестті қайта тапсыру"):
            st.session_state[test_submitted_key] = False
            st.rerun()

# --- ДИРЕКТОР КАБИНЕТИ ---
def director_dashboard():
    st.title(f"👨‍💼 Директор кабинеті")
    
    tab1, tab2, tab3 = st.tabs(["📊 Оқушылар нәтижесі", "🔑 Аккаунттар мен Парольдер", "➕ Жаңа сұрақ енгізу"])
    
    # 1-Вкладка: Окуучулардын жыйынтыктары
    with tab1:
        st.subheader("Оқушылардың бағыттар бойынша ҰБТ нәтижелері")
        if len(st.session_state.results) > 0:
            st.table(st.session_state.results)
        else:
            st.info("Әлі ешқандай оқушы тест тапсырмады.")
            
    # 2-Вкладка: Аккаунттарды башкаруу
    with tab2:
        st.subheader("👥 Барлық пайдаланушылар тізімі (Логин мен Парольдер)")
        
        user_list = []
        for uname, udata in st.session_state.users.items():
            user_list.append({
                "Логин": uname,
                "Аты-жөні": udata["name"],
                "Пароль": udata["password"],
                "Ролі": "Оқушы" if udata["role"] == "student" else "Директор"
            })
        st.table(user_list)
        
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### ✏️ Парольді өзгерту")
            selected_user = st.selectbox("Пайдаланушыны таңдаңыз:", list(st.session_state.users.keys()))
            new_password = st.text_input("Жаңа пароль енгізіңіз:", type="password")
            
            if st.button("Парольді жаңарту"):
                if new_password:
                    st.session_state.users[selected_user]["password"] = new_password
                    st.success(f"'{selected_user}' аккаунтының паролі сәтті өзгертілді!")
                    st.rerun()
                else:
                    st.warning("Жаңа парольді енгізіңіз!")
                    
        with col2:
            st.write("### ➕ Жаңа оқушы қосу")
            new_uname = st.text_input("Жаңа логин:")
            new_name = st.text_input("Оқушының аты-жөні:")
            new_pass = st.text_input("Пароль тағайындау:")
            
            if st.button("Оқушыны тіркеу"):
                if new_uname and new_name and new_pass:
                    if new_uname in st.session_state.users:
                        st.error("Бұл логин бос емес!")
                    else:
                        st.session_state.users[new_uname] = {
                            "password": new_pass,
                            "name": new_name,
                            "role": "student"
                        }
                        st.success(f"Оқушы {new_name} сәтті қосылды!")
                        st.rerun()
                else:
                    st.warning("Барлық өрістерді толтырыңыз!")

    # 3-Вкладка: Жаңы суроо кошуу (Сүрөт кошуу мүмкүнчүлүгү менен)
    with tab3:
        st.subheader("Жаңа тест сұрағын қосу")
        
        target_direction = st.selectbox("Сұрақ қай бағытқа арналған?", DIRECTIONS)
        q_type = st.radio("Сұрақтың түрі:", ["Бір дұрыс жауапты", "Көп дұрыс жауапты (бірнеше)"])
        
        q_text = st.text_input("Сұрақтың мәтіні:")
        img_url = st.text_input("Суреттің URL шилтемесі (міндетті емес):", placeholder="https://example.com/image.png")
        
        col1, col2 = st.columns(2)
        with col1:
            opt1 = st.text_input("А нұсқасы:")
            opt2 = st.text_input("В нұсқасы:")
        with col2:
            opt3 = st.text_input("С нұсқасы:")
            opt4 = st.text_input("D нұсқасы:")
            
        options_list = [opt1, opt2, opt3, opt4]
        
        if q_type == "Бір дұрыс жауапты":
            correct_ans = [st.selectbox("Дұрыс жауабы қайсысы?", options_list)]
        else:
            correct_ans = st.multiselect("Дұрыс жауаптарды белгілеңіз (бірнешеуін таңдауға болады):", options_list)
        
        if st.button("Сұрақты базаға сақтау"):
            if q_text and opt1 and opt2 and opt3 and opt4 and correct_ans:
                st.session_state.questions.append({
                    "direction": target_direction,
                    "type": "single" if q_type == "Бір дұрыс жауапты" else "multiple",
                    "question": q_text,
                    "image": img_url,
                    "options": options_list,
                    "answer": correct_ans
                })
                st.success(f"Сұрақ '{target_direction}' бағытына сәтті қосылды!")
            else:
                st.error("Барлық өрістерді толтырып, дұрыс жауапты белгілеңіз!")

# --- НЕГИЗГИ БАШКАРУУ МЕНЮСУ ---
if not st.session_state.logged_in:
    login_page()
else:
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("Шығу (Logout)"):
            st.session_state.logged_in = False
            st.rerun()
            
    if st.session_state.role == "student":
        student_dashboard()
    elif st.session_state.role == "director":
        director_dashboard()
