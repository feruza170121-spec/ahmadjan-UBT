import streamlit as st
import json
import os

# Барақшаның баптаулары
st.set_page_config(page_title="Ахмад Академиясы - ҰБТ Порталы", page_icon="🎓", layout="centered")

# 1. ҰБТ-НЫҢ БАРЛЫҚ ПӘНДЕРІ (Матсау қосылды)
ALL_SUBJECTS = [
    "Математикалық сауаттылық",
    "Оқу сауаттылығы",
    "Қазақстан тарихы",
    "Математика",
    "Физика",
    "Химия",
    "Биология",
    "География",
    "Дүниежүзі тарихы",
    "Адам. Қоғам. Құқық",
    "Ағылшын тілі",
    "Қазақ тілі мен әдебиеті",
    "Информатика"
]

# 2. СҰРАҚТАРДЫ JSON ФАЙЛҒА САҚТАУ/ОҚУ
QUESTIONS_FILE = "questions.json"

DEFAULT_QUESTIONS = [
    {
        "direction": "Математикалық сауаттылық",
        "type": "single",
        "question": "Сандар тізбегіндегі келесі санды тап: 2, 4, 8, 16, ?",
        "image": "",
        "options": ["20", "24", "32", "64"],
        "answer": ["32"]
    },
    {
        "direction": "Математика",
        "type": "single",
        "question": "Синус 30 градуста нешеге тең?",
        "image": "",
        "options": ["0", "0.5", "1", "sqrt(3)/2"],
        "answer": ["0.5"]
    },
    {
        "direction": "Физика",
        "type": "multiple",
        "question": "Төмендегілердің қайсысы скаляр шамалар болып табылады? (Бірнеше жауап таңдаңыз)",
        "image": "",
        "options": ["Масса", "Үдеу", "Уақыт", "Күш"],
        "answer": ["Масса", "Уақыт"]
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

# 3. ДИЗАЙН: ЖАСЫЛ ТҮСТІ СТИЛЬ
st.markdown(
    """
    <style>
    /* Негізгі фон */
    .stApp {
        background-color: #05140B !important;
        color: #4ADE80 !important;
    }

    /* Мәтіндер мен белгілер */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #22C55E !important;
    }

    /* Деректерді енгізу өрістері */
    input, textarea, div[data-baseweb="select"] > div {
        background-color: #0A2615 !important;
        color: #4ADE80 !important;
        border: 1px solid #22C55E !important;
        border-radius: 8px !important;
    }

    /* Түймелер дизайны */
    .stButton > button {
        background-color: #15803D !important;
        color: #FFFFFF !important;
        border: 1px solid #22C55E !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }
    .stButton > button:hover {
        background-color: #22C55E !important;
        color: #000000 !important;
    }

    /* Radio және Checkbox белгілері */
    div[class*="stRadio"] label, div[class*="stCheckbox"] label {
        color: #86EFAC !important;
    }

    /* Табтар (Вкладкалар) */
    button[data-baseweb="tab"] {
        color: #166534 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #4ADE80 !important;
        border-bottom-color: #22C55E !important;
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

# Пайдаланушылар базасы (Мұғалім қосылды)
if 'users' not in st.session_state:
    st.session_state.users = {
        "student": {"password": "123", "name": "Айбек", "role": "student"},
        "teacher": {"password": "123", "name": "Математика мұғалімі", "role": "teacher", "subject": "Математикалық сауаттылық"},
        "admin": {"password": "admin123", "name": "Мектеп Директоры", "role": "director"}
    }

# Нәтижелер
if 'results' not in st.session_state:
    st.session_state.results = [
        {"Оқушы": "Айбек", "Пән": "Математикалық сауаттылық", "Балл": 5, "Макс": 5}
    ]

# Сертификат
def show_certificate(student_name, subject, score, total):
    st.markdown(
        f"""
        <div style="
            border: 2px solid #22C55E; 
            padding: 30px 20px; 
            text-align: center; 
            background: #0A2615; 
            border-radius: 16px; 
            box-shadow: 0 0 20px rgba(34, 197, 94, 0.3);
            margin-top: 15px;
            color: #4ADE80;
        ">
            <h5 style="color: #86EFAC; letter-spacing: 3px; margin-bottom: 5px;">АХМАД АКАДЕМИЯСЫ</h5>
            <h1 style="color: #22C55E; font-size: 36px; margin-top: 0;">🎓 СЕРТИФИКАТ</h1>
            <p style="font-size: 15px; color: #86EFAC; margin-top: 15px;">Осы сертификат ҰБТ пәндік тестін сәтті тапсырғаны үшін</p>
            <h2 style="color: #4ADE80; font-size: 30px; margin: 10px 0;">{student_name}</h2>
            <p style="font-size: 15px; color: #86EFAC;">иегеріне <b>«{subject}»</b> пәні бойынша беріледі.</p>
            <hr style="border: 0; height: 1px; background: #22C55E; margin: 20px 0;">
            <div style="background-color: rgba(34, 197, 94, 0.2); border: 1px solid #22C55E; padding: 12px 25px; border-radius: 10px; display: inline-block;">
                <h3 style="color: #22C55E; margin: 0; font-size: 20px;">Нәтиже: {score} / {total} балл</h3>
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
                st.session_state.teacher_subject = user.get("subject", "Математикалық сауаттылық")
                st.rerun()
            else:
                st.error("Пароль қате!")
        else:
            st.error("Мұндай логин табылмады!")

    st.info("""
    **Әдепкі аккаунттар:**
    * 👨‍🎓 **Оқушы:** Логин: `student` | Пароль: `123`
    * 👩‍🏫 **Мұғалім:** Логин: `teacher` | Пароль: `123`
    * 👨‍💼 **Директор:** Логин: `admin` | Пароль: `admin123`
    """)

# Оқушы кабинеті
def student_dashboard():
    st.title(f"👨‍🎓 Оқушы кабинеті: {st.session_state.display_name}")
    
    if "test_started" not in st.session_state:
        st.session_state.test_started = False
    if "test_finished" not in st.session_state:
        st.session_state.test_finished = False

    if not st.session_state.test_started and not st.session_state.test_finished:
        st.subheader("📌 Тапсыратын пәнді таңдаңыз:")
        selected_subject = st.selectbox("Пәндер тізімі:", ALL_SUBJECTS)
        
        filtered_q = [q for q in st.session_state.questions if q.get("direction") == selected_subject]
        st.info(f"Таңдалған пән бойынша базада **{len(filtered_q)}** сұрақ бар.")
        
        if len(filtered_q) == 0:
            st.warning("Бұл пән бойынша әлі сұрақтар енгізілмеген!")
        else:
            if st.button("🚀 Тестті бастау", type="primary", use_container_width=True):
                st.session_state.selected_subject = selected_subject
                st.session_state.test_started = True
                st.rerun()

    elif st.session_state.test_started and not st.session_state.test_finished:
        subject = st.session_state.selected_subject
        filtered_questions = [q for q in st.session_state.questions if q.get("direction") == subject]
        
        st.write(f"## 📝 Пән: {subject}")
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
                "Пән": subject,
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
        subject = st.session_state.selected_subject
        filtered_questions = [q for q in st.session_state.questions if q.get("direction") == subject]
        
        score = st.session_state.score
        total = st.session_state.total
        user_answers = st.session_state.user_answers

        show_certificate(st.session_state.display_name, subject, score, total)
        
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

        if st.button("🔄 Басқа пән таңдау"):
            st.session_state.test_started = False
            st.session_state.test_finished = False
            st.rerun()

# Мұғалім кабинеті (Тек сұрақ енгізу және өзгерту)
def teacher_dashboard():
    st.title(f"👩‍🏫 Мұғалім кабинеті: {st.session_state.display_name}")
    
    target_subject = st.session_state.get("teacher_subject", ALL_SUBJECTS[0])
    st.success(f"📌 Сіз тағайындалған пән: **{target_subject}**")
    
    tab1, tab2 = st.tabs(["➕ Сұрақ қосу", "📝 Өз пәніңіздің сұрақтарын басқару"])
    
    with tab1:
        st.subheader(f"«{target_subject}» пәніне жаңа сұрақ енгізу")
        
        q_type = st.radio("Сұрақтың түрі:", ["Бір дұрыс жауапты", "Көп дұрыс жауапты (бірнеше)"], key="t_add_type")
        q_text = st.text_input("Сұрақтың мәтіні:", key="t_add_text")
        img_url = st.text_input("Суреттің URL сілтемесі (міндетті емес):", placeholder="https://example.com/image.png", key="t_add_img")
        
        col1, col2 = st.columns(2)
        with col1:
            opt1 = st.text_input("А нұсқасы:", key="t_opt1")
            opt2 = st.text_input("В нұсқасы:", key="t_opt2")
        with col2:
            opt3 = st.text_input("С нұсқасы:", key="t_opt3")
            opt4 = st.text_input("D нұсқасы:", key="t_opt4")
            
        options_list = [opt for opt in [opt1, opt2, opt3, opt4] if opt.strip() != ""]
        
        correct_ans = []
        if len(options_list) == 4:
            st.subheader("🎯 Дұрыс жауабын белгілеңіз:")
            if q_type == "Бір дұрыс жауапты":
                selected_single = st.selectbox("Дұрыс жауапты таңдаңыз:", options_list, key="t_ans_single")
                correct_ans = [selected_single] if selected_single else []
            else:
                correct_ans = st.multiselect("Дұрыс жауаптарды белгілеңіз:", options_list, key="t_ans_multi")

        if st.button("Сұрақты сақтау", type="primary"):
            if q_text and len(options_list) == 4 and correct_ans:
                st.session_state.questions.append({
                    "direction": target_subject,
                    "type": "single" if q_type == "Бір дұрыс жауапты" else "multiple",
                    "question": q_text,
                    "image": img_url,
                    "options": options_list,
                    "answer": correct_ans
                })
                save_questions(st.session_state.questions)
                st.success(f"Сұрақ '{target_subject}' пәніне сәтті сақталды!")
                st.rerun()
            else:
                st.error("Барлық өрістерді толтырыңыз!")

    with tab2:
        st.subheader(f"«{target_subject}» пәнінің сұрақтары")
        
        subject_questions = [(i, q) for i, q in enumerate(st.session_state.questions) if q.get("direction") == target_subject]
        
        if not subject_questions:
            st.info("Бұл пән бойынша әлі сұрақтар енгізілмеген.")
        else:
            q_options = [f"{idx+1}. {q['question']}" for idx, (real_idx, q) in enumerate(subject_questions)]
            selected_q = st.selectbox("Сұрақты таңдаңыз:", range(len(q_options)), format_func=lambda x: q_options[x])
            
            real_index, q_data = subject_questions[selected_q]
            
            st.divider()
            edit_text = st.text_input("Сұрақтың мәтіні:", value=q_data["question"], key="t_edit_text")
            edit_img = st.text_input("Сурет сілтемесі:", value=q_data.get("image", ""), key="t_edit_img")
            
            opts = q_data["options"]
            col1, col2 = st.columns(2)
            with col1:
                e_opt1 = st.text_input("А нұсқасы:", value=opts[0] if len(opts) > 0 else "", key="t_e_opt1")
                e_opt2 = st.text_input("В нұсқасы:", value=opts[1] if len(opts) > 1 else "", key="t_e_opt2")
            with col2:
                e_opt3 = st.text_input("С нұсқасы:", value=opts[2] if len(opts) > 2 else "", key="t_e_opt3")
                e_opt4 = st.text_input("D нұсқасы:", value=opts[3] if len(opts) > 3 else "", key="t_e_opt4")
                
            edit_opts_list = [e_opt1, e_opt2, e_opt3, e_opt4]
            
            if q_data.get("type") == "single":
                default_single = q_data["answer"][0] if q_data["answer"] and q_data["answer"][0] in edit_opts_list else edit_opts_list[0]
                edit_ans = [st.selectbox("Дұрыс жауабы:", edit_opts_list, index=edit_opts_list.index(default_single), key="t_e_ans_single")]
            else:
                valid_defaults = [a for a in q_data["answer"] if a in edit_opts_list]
                edit_ans = st.multiselect("Дұрыс жауаптары:", edit_opts_list, default=valid_defaults, key="t_e_ans_multi")
                
            col_save, col_del = st.columns(2)
            with col_save:
                if st.button("💾 Өзгерісті сақтау"):
                    st.session_state.questions[real_index] = {
                        "direction": target_subject,
                        "type": q_data.get("type", "single"),
                        "question": edit_text,
                        "image": edit_img,
                        "options": edit_opts_list,
                        "answer": edit_ans
                    }
                    save_questions(st.session_state.questions)
                    st.success("Сұрақ жаңартылды!")
                    st.rerun()
                    
            with col_del:
                if st.button("🗑️ Сұрақты өшіру"):
                    st.session_state.questions.pop(real_index)
                    save_questions(st.session_state.questions)
                    st.success("Сұрақ өшірілді!")
                    st.rerun()

# Директор кабинеті
def director_dashboard():
    st.title(f"👨‍💼 Директор кабинеті")
    
    tab1, tab2, tab3 = st.tabs(["📊 Оқушылар нәтижесі", "🔑 Аккаунттарды басқару", "📝 Барлық сұрақтарды басқару"])
    
    with tab1:
        st.subheader("Оқушылардың ҰБТ нәтижелері")
        if len(st.session_state.results) > 0:
            st.table(st.session_state.results)
        else:
            st.info("Әлі ешқандай оқушы тест тапсырмады.")
            
    with tab2:
        st.subheader("👥 Пайдаланушылар тізімі")
        user_list = []
        for uname, udata in st.session_state.users.items():
            role_str = "Оқушы"
            if udata["role"] == "director": role_str = "Директор"
            elif udata["role"] == "teacher": role_str = f"Мұғалім ({udata.get('subject')})"
            
            user_list.append({
                "Логин": uname,
                "Аты-жөні": udata["name"],
                "Пароль": udata["password"],
                "Ролі": role_str
            })
        st.table(user_list)
        
        st.divider()
        st.write("### ➕ Жаңа пайдаланушы тіркеу (Оқушы немесе Мұғалім)")
        new_uname = st.text_input("Логин:")
        new_name = st.text_input("Аты-жөні:")
        new_pass = st.text_input("Пароль:")
        new_role = st.selectbox("Ролі:", ["student", "teacher"], format_func=lambda x: "Оқушы" if x == "student" else "Мұғалім")
        
        teacher_subj = None
        if new_role == "teacher":
            teacher_subj = st.selectbox("Мұғалімге тағайындалатын пән:", ALL_SUBJECTS)
            
        if st.button("Тіркеу"):
            if new_uname and new_name and new_pass:
                if new_uname in st.session_state.users:
                    st.error("Бұл логин бос емес!")
                else:
                    u_data = {"password": new_pass, "name": new_name, "role": new_role}
                    if new_role == "teacher":
                        u_data["subject"] = teacher_subj
                    st.session_state.users[new_uname] = u_data
                    st.success(f"Пайдаланушы {new_name} сәтті тіркелді!")
                    st.rerun()
            else:
                st.warning("Барлық өрісті толтырыңыз!")

    with tab3:
        st.subheader("📝 Барлық сұрақтарды басқару")
        if not st.session_state.questions:
            st.info("Базада әлі сұрақтар жоқ.")
        else:
            q_options = [f"{i+1}. [{q.get('direction', 'Пәнсіз')}] {q['question']}" for i, q in enumerate(st.session_state.questions)]
            selected_q_idx = st.selectbox("Сұрақты таңдаңыз:", range(len(q_options)), format_func=lambda x: q_options[x], key="dir_select_q")
            
            q_data = st.session_state.questions[selected_q_idx]
            
            st.divider()
            edit_subj_index = ALL_SUBJECTS.index(q_data["direction"]) if q_data.get("direction") in ALL_SUBJECTS else 0
            edit_subj = st.selectbox("Пәні:", ALL_SUBJECTS, index=edit_subj_index, key="dir_edit_subj")
            edit_text = st.text_input("Сұрақтың мәтіні:", value=q_data["question"], key="dir_edit_text")
            
            if st.button("🗑️ Сұрақты өшіру", key="dir_del_btn"):
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
    elif st.session_state.role == "teacher":
        teacher_dashboard()
    elif st.session_state.role == "director":
        director_dashboard()
