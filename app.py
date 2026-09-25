import streamlit as st
import json
import os

# Барақшаның баптаулары
st.set_page_config(page_title="Ахмад Академиясы - ҰБТ Порталы", page_icon="🎓", layout="centered")

# 1. СҰРАҚТАРДЫ СЕРВЕРДЕ ӨШПЕЙТІН ЕТІП JSON ФАЙЛҒА САҚТАУ ЛОГИКАСЫ
QUESTIONS_FILE = "questions.json"

DEFAULT_QUESTIONS = [
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

def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return DEFAULT_QUESTIONS
    else:
        save_questions(DEFAULT_QUESTIONS)
        return DEFAULT_QUESTIONS

def save_questions(questions_list):
    with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(questions_list, f, ensure_ascii=False, indent=4)

if 'questions' not in st.session_state:
    st.session_state.questions = load_questions()

# 2. ДИЗАЙН: ҚАРА-СҰР ТОЛҚЫНДЫ ФОН (CSS арқылы жасалған, ешқашан бұзылмайды)
st.markdown(
    """
    <style>
    /* Негізгі фон мен қара-сұр градиент */
    .stApp {
        background: radial-gradient(circle at 50% 30%, #334155 0%, #1E293B 50%, #0F172A 100%);
        background-attachment: fixed;
        color: #F8FAFC;
    }

    /* Формалар мен контейнерлер */
    div[data-testid="stVerticalBlock"] > div {
        color: #F8FAFC;
    }

    /* Түймелер дизайны */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: bold !important;
    }

    /* Input / Selectbox баптаулары */
    input, div[data-baseweb="select"] > div {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
    }

    /* Вкладкалар */
    button[data-baseweb="tab"] {
        color: #94A3B8 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38BDF8 !important;
        border-bottom-color: #38BDF8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Сессияны басқару
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# Пайдаланушылар базасы
if 'users' not in st.session_state:
    st.session_state.users = {
        "student": {"password": "123", "name": "Айбек", "role": "student"},
        "aruzhan": {"password": "123", "name": "Аружан", "role": "student"},
        "admin": {"password": "admin123", "name": "Мектеп Директоры", "role": "director"}
    }

# Бағыттар тізімі
DIRECTIONS = [
    "Математика - Физика",
    "Химия - Биология",
    "Дүниежүзі тарихы - Құқық",
    "География - Математика"
]

# Нәтижелер
if 'results' not in st.session_state:
    st.session_state.results = [
        {"Оқушы": "Айбек", "Бағыты": "Математика - Физика", "Балл": 10, "Макс": 10},
        {"Оқушы": "Аружан", "Бағыты": "Химия - Биология", "Балл": 5, "Макс": 10}
    ]

# Сертификат
def show_certificate(student_name, direction, score, total):
    st.markdown(
        f"""
        <div style="
            border: 2px solid #38BDF8; 
            padding: 35px 20px; 
            text-align: center; 
            background: rgba(15, 23, 42, 0.9); 
            border-radius: 16px; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
            margin-top: 15px;
            color: #F8FAFC;
        ">
            <h5 style="color: #94A3B8; letter-spacing: 3px; margin-bottom: 5px;">АХМАД АКАДЕМИЯСЫ</h5>
            <h1 style="color: #38BDF8; font-size: 36px; margin-top: 0;">🎓 СЕРТИФИКАТ</h1>
            <p style="font-size: 15px; color: #CBD5E1; margin-top: 15px;">Осы сертификат ҰБТ байқау тестін сәтті тапсырғаны үшін</p>
            <h2 style="color: #FACC15; font-size: 30px; margin: 10px 0;">{student_name}</h2>
            <p style="font-size: 15px; color: #CBD5E1;">иегеріне <b>«{direction}»</b> бағыты бойынша беріледі.</p>
            <hr style="border: 0; height: 1px; background: #38BDF8; margin: 20px 0;">
            <div style="background-color: rgba(56, 189, 248, 0.15); border: 1px solid #38BDF8; padding: 12px 25px; border-radius: 10px; display: inline-block;">
                <h3 style="color: #38BDF8; margin: 0; font-size: 20px;">Нәтиже: {score} / {total} балл</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Логин беті
def login_page():
    st.title("🎓 Ахмад Академиясы - ҰБТ Порталы")
    
    username = st.text_input("Логин (Пайдаланушы аты)")
    password = st.text_input("Пароль", type="password")
    
    if st.button("Кіру", type="primary", use_container_width=True):
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

# Оқушы кабинеті
def student_dashboard():
    st.title(f"👨‍🎓 Оқушы кабинеті: {st.session_state.display_name}")
    
    if "test_started" not in st.session_state:
        st.session_state.test_started = False
    if "test_finished" not in st.session_state:
        st.session_state.test_finished = False

    if not st.session_state.test_started and not st.session_state.test_finished:
        st.subheader("📌 Өз ҰБТ бағытыңызды таңдаңыз:")
        selected_direction = st.selectbox("Бейіндік пәндер комбинациясы:", DIRECTIONS)
        
        filtered_q = [q for q in st.session_state.questions if q["direction"] == selected_direction]
        st.info(f"Таңдалған бағыт бойынша **{len(filtered_q)}** сұрақ бар.")
        
        if len(filtered_q) == 0:
            st.warning("Бұл бағыт бойынша әлі сұрақ қосылмаған!")
        else:
            if st.button("🚀 Тестті бастау", type="primary", use_container_width=True):
                st.session_state.selected_direction = selected_direction
                st.session_state.test_started = True
                st.rerun()

    elif st.session_state.test_started and not st.session_state.test_finished:
        direction = st.session_state.selected_direction
        filtered_questions = [q for q in st.session_state.questions if q["direction"] == direction]
        
        st.write(f"## 📝 Бағыты: {direction}")
        st.divider()

        user_answers = {}
        for i, q in enumerate(filtered_questions):
            st.markdown(f"### {i+1}. {q['question']}")
            
            if q.get("image"):
                st.image(q["image"], width=400)
            
            if q.get("type", "single") == "single":
                selected_val = st.radio(
                    "Жауапты таңдаңыз:",
                    q['options'],
                    index=None,
                    key=f"q_{i}_radio",
                    label_visibility="collapsed"
                )
                user_answers[i] = [selected_val] if selected_val else []
            else:
                selected_opts = []
                st.caption("*(Бірнеше жауап таңдауға болады)*")
                for opt_idx, opt in enumerate(q['options']):
                    if st.checkbox(opt, key=f"q_{i}_opt_{opt_idx}"):
                        selected_opts.append(opt)
                user_answers[i] = selected_opts
            
            st.markdown("---")

        if st.button("🏁 Тестті аяқтау", type="primary", use_container_width=True):
            score = 0
            total = len(filtered_questions) * 5
            
            for i, q in enumerate(filtered_questions):
                ans = user_answers.get(i, [])
                if set(ans) == set(q['answer']):
                    score += 5
                    
            st.session_state.results.append({
                "Оқушы": st.session_state.display_name,
                "Бағыты": direction,
                "Балл": score,
                "Макс": total
            })
            
            st.session_state.user_answers = user_answers
            st.session_state.score = score
            st.session_state.total = total
            st.session_state.test_started = False
            st.session_state.test_finished = True
            st.rerun()

    elif st.session_state.test_finished:
        direction = st.session_state.selected_direction
        filtered_questions = [q for q in st.session_state.questions if q["direction"] == direction]
        
        score = st.session_state.score
        total = st.session_state.total
        user_answers = st.session_state.user_answers

        show_certificate(st.session_state.display_name, direction, score, total)
        
        st.divider()
        st.subheader("🔍 Тест нәтижелері мен қателерді талдау:")
        
        for i, q in enumerate(filtered_questions):
            u_ans = user_answers.get(i, [])
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

        if st.button("🔄 Басқа тест тапсыру"):
            st.session_state.test_started = False
            st.session_state.test_finished = False
            st.rerun()

# Директор кабинеті
def director_dashboard():
    st.title(f"👨‍💼 Директор кабинеті")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Оқушылар нәтижесі", "🔑 Аккаунттар", "➕ Жаңа сұрақ енгізу", "📝 Сұрақтарды өңдеу/өшіру"])
    
    with tab1:
        st.subheader("Оқушылардың бағыттар бойынша ҰБТ нәтижелері")
        if len(st.session_state.results) > 0:
            st.table(st.session_state.results)
        else:
            st.info("Әлі ешқандай оқушы тест тапсырмады.")
            
    with tab2:
        st.subheader("👥 Барлық пайдаланушылар тізімі")
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
                    st.success(f"'{selected_user}' паролі сәтті өзгертілді!")
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

    with tab3:
        st.subheader("Жаңа тест сұрағын қосу")
        
        target_direction = st.selectbox("Сұрақ қай бағытқа арналған?", DIRECTIONS, key="add_dir")
        q_type = st.radio("Сұрақтың түрі:", ["Бір дұрыс жауапты", "Көп дұрыс жауапты (бірнеше)"], key="add_type")
        
        q_text = st.text_input("Сұрақтың мәтіні:", key="add_text")
        img_url = st.text_input("Суреттің URL шилтемесі (міндетті емес):", placeholder="https://example.com/image.png", key="add_img")
        
        col1, col2 = st.columns(2)
        with col1:
            opt1 = st.text_input("А нұсқасы:", key="add_opt1")
            opt2 = st.text_input("В нұсқасы:", key="add_opt2")
        with col2:
            opt3 = st.text_input("С нұсқасы:", key="add_opt3")
            opt4 = st.text_input("D нұсқасы:", key="add_opt4")
            
        options_list = [opt for opt in [opt1, opt2, opt3, opt4] if opt.strip() != ""]
        
        correct_ans = []
        if len(options_list) == 4:
            st.subheader("🎯 Дұрыс жауабын белгілеңіз:")
            if q_type == "Бір дұрыс жауапты":
                selected_single = st.selectbox("Дұрыс жауапты таңдаңыз:", options_list, key="add_ans_single")
                correct_ans = [selected_single] if selected_single else []
            else:
                correct_ans = st.multiselect("Дұрыс жауаптарды белгілеңіз:", options_list, key="add_ans_multi")

        if st.button("Сұрақты базаға сақтау", type="primary"):
            if q_text and len(options_list) == 4 and correct_ans:
                st.session_state.questions.append({
                    "direction": target_direction,
                    "type": "single" if q_type == "Бір дұрыс жауапты" else "multiple",
                    "question": q_text,
                    "image": img_url,
                    "options": options_list,
                    "answer": correct_ans
                })
                # Файлға мәңгілікке сақтау
                save_questions(st.session_state.questions)
                st.success(f"Сұрақ сәтті сақталды және файлға жазылды!")
                st.rerun()
            else:
                st.error("Барлық өрістерді толтырыңыз!")

    with tab4:
        st.subheader("📝 Сұрақтарды өңдеу немесе өшіру")
        
        if not st.session_state.questions:
            st.info("Базада әлі сұрақтар жоқ.")
        else:
            q_options = [f"{i+1}. [{q['direction']}] {q['question']}" for i, q in enumerate(st.session_state.questions)]
            selected_q_idx = st.selectbox("Өңдейтін сұрақты таңдаңыз:", range(len(q_options)), format_func=lambda x: q_options[x])
            
            q_data = st.session_state.questions[selected_q_idx]
            
            st.divider()
            edit_dir = st.selectbox("Бағыты:", DIRECTIONS, index=DIRECTIONS.index(q_data["direction"]), key="edit_dir")
            edit_type = st.radio("Сұрақтың түрі:", ["Бір дұрыс жауапты", "Көп дұрыс жауапты (бірнеше)"], index=0 if q_data.get("type", "single") == "single" else 1, key="edit_type")
            edit_text = st.text_input("Сұрақтың мәтіні:", value=q_data["question"], key="edit_text")
            edit_img = st.text_input("Суреттің URL шилтемесі:", value=q_data.get("image", ""), key="edit_img")
            
            col1, col2 = st.columns(2)
            opts = q_data["options"]
            with col1:
                e_opt1 = st.text_input("А нұсқасы:", value=opts[0] if len(opts) > 0 else "", key="edit_opt1")
                e_opt2 = st.text_input("В нұсқасы:", value=opts[1] if len(opts) > 1 else "", key="edit_opt2")
            with col2:
                e_opt3 = st.text_input("С нұсқасы:", value=opts[2] if len(opts) > 2 else "", key="edit_opt3")
                e_opt4 = st.text_input("D нұсқасы:", value=opts[3] if len(opts) > 3 else "", key="edit_opt4")
                
            edit_opts_list = [e_opt1, e_opt2, e_opt3, e_opt4]
            
            if edit_type == "Бір дұрыс жауапты":
                default_single = q_data["answer"][0] if q_data["answer"] and q_data["answer"][0] in edit_opts_list else edit_opts_list[0]
                edit_ans = [st.selectbox("Дұрыс жауабы:", edit_opts_list, index=edit_opts_list.index(default_single), key="edit_ans_single")]
            else:
                valid_defaults = [a for a in q_data["answer"] if a in edit_opts_list]
                edit_ans = st.multiselect("Дұрыс жауаптары:", edit_opts_list, default=valid_defaults, key="edit_ans_multi")
                
            col_save, col_del = st.columns(2)
            with col_save:
                if st.button("💾 Өзгерістерді сақтау"):
                    st.session_state.questions[selected_q_idx] = {
                        "direction": edit_dir,
                        "type": "single" if edit_type == "Бір дұрыс жауапты" else "multiple",
                        "question": edit_text,
                        "image": edit_img,
                        "options": edit_opts_list,
                        "answer": edit_ans
                    }
                    save_questions(st.session_state.questions)
                    st.success("Сұрақ жаңартылып, сақталды!")
                    st.rerun()
                    
            with col_del:
                if st.button("🗑️ Сұрақты өшіру"):
                    st.session_state.questions.pop(selected_q_idx)
                    save_questions(st.session_state.questions)
                    st.success("Сұрақ өшірілді!")
                    st.rerun()

# Басқару мәзірі
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
