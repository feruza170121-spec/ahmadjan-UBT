import streamlit as st
import json
import os
import uuid

# Параметры страницы
st.set_page_config(page_title="Ахмад Академиясы - ҰБТ Порталы", page_icon="🎓", layout="centered")

# 1. ВСЕ ПРЕДМЕТЫ ЕНТ
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

# 2. РАБОТА С ФАЙЛОМ ВОПРОСОВ (JSON)
QUESTIONS_FILE = "questions.json"

DEFAULT_QUESTIONS = [
    {
        "direction": "Математикалық сауаттылық",
        "type": "single",
        "question": "Сандар тізбегіндегі келесі санды тап: 2, 4, 8, 16, ?",
        "image": "",
        "options": ["20", "24", "32", "64"],
        "answer": ["32"],
        "author": "Математика мұғалімі"
    },
    {
        "direction": "Математика",
        "type": "single",
        "question": "Синус 30 градуста нешеге тең?",
        "image": "",
        "options": ["0", "0.5", "1", "sqrt(3)/2"],
        "answer": ["0.5"],
        "author": "Математика мұғалімі"
    },
    {
        "direction": "Физика",
        "type": "multiple",
        "question": "Төмендегілердің қайсысы скаляр шамалар болып табылады? (Бірнеше жауап таңдаңыз)",
        "image": "",
        "options": ["Масса", "Үдеу", "Уақыт", "Күш"],
        "answer": ["Масса", "Уақыт"],
        "author": "Мектеп Директоры"
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

# 3. ДИЗАЙН (ЖАСЫЛ ТЕХНОЛОГИЯЛЫҚ СТИЛЬ)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #05140B !important;
        color: #4ADE80 !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #22C55E !important;
    }
    input, textarea, div[data-baseweb="select"] > div {
        background-color: #0A2615 !important;
        color: #4ADE80 !important;
        border: 1px solid #22C55E !important;
        border-radius: 8px !important;
    }
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
    div[class*="stRadio"] label, div[class*="stCheckbox"] label {
        color: #86EFAC !important;
    }
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

# СЕССИЯ ЖӘНЕ ПАЙДАЛАНУШЫЛАРДЫ БАСҚАРУ
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.session_id = ""

if 'users' not in st.session_state:
    st.session_state.users = {
        "student": {"password": "123", "name": "Айбек", "role": "student", "active_session_id": "", "is_blocked": False},
        "teacher": {"password": "123", "name": "Математика мұғалімі", "role": "teacher", "subject": "Математикалық сауаттылық", "active_session_id": "", "is_blocked": False},
        "admin": {"password": "admin123", "name": "Мектеп Директоры", "role": "director", "active_session_id": "", "is_blocked": False}
    }

if 'results' not in st.session_state:
    st.session_state.results = [
        {"Оқушы": "Айбек", "Пән": "Математикалық сауаттылық", "Балл": 5, "Макс": 5}
    ]

# СЕРТИФИКАТ КӨРСЕТУ
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
            margin-bottom: 25px;
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

# КІРУ СРАНИЦАСЫ (LOGIN)
def login_page():
    st.title("🎓 Ахмад Академиясы - ҰБТ Порталы")
    
    username = st.text_input("Логин (Пайдаланушы аты)")
    password = st.text_input("Пароль", type="password")
    
    if st.button("Кіру", type="primary", use_container_width=True):
        if username in st.session_state.users:
            user = st.session_state.users[username]
            if user.get("is_blocked", False):
                st.error("🚫 Бұл аккаунт ереже бұзғаны (вкладка ауыстыру) үшін бұғатталған! Директорға хабарласыңыз.")
            elif user["password"] == password:
                new_session_id = str(uuid.uuid4())
                st.session_state.users[username]["active_session_id"] = new_session_id
                
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.display_name = user["name"]
                st.session_state.role = user["role"]
                st.session_state.session_id = new_session_id
                st.session_state.teacher_subject = user.get("subject", "Математикалық сауаттылық")
                st.session_state.tab_warnings = 0
                st.rerun()
            else:
                st.error("Пароль қате!")
        else:
            st.error("Мұндай логин табылмады!")

    st.info("""
    **Қолжетімді аккаунттар:**
    * 👨‍🎓 **Оқушы:** Логин: `student` | Пароль: `123`
    * 👩‍🏫 **Мұғалім:** Логин: `teacher` | Пароль: `123`
    * 👨‍💼 **Директор:** Логин: `admin` | Пароль: `admin123`
    """)

# ОҚУШЫ КАБИНЕТІ
def student_dashboard():
    st.title(f"👨‍🎓 Оқушы кабинеті: {st.session_state.display_name}")
    
    if "test_started" not in st.session_state:
        st.session_state.test_started = False
    if "test_finished" not in st.session_state:
        st.session_state.test_finished = False
    if "selected_subject" not in st.session_state:
        st.session_state.selected_subject = ALL_SUBJECTS[0]
    if "tab_warnings" not in st.session_state:
        st.session_state.tab_warnings = 0

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
                st.session_state.tab_warnings = 0
                st.rerun()

    elif st.session_state.test_started and not st.session_state.test_finished:
        
        # Ескерту батырмасы (Қолмен немесе авто жұмыс істейді)
        col_warn1, col_warn2 = st.columns([3, 1])
        with col_warn2:
            if st.button("🔔 Ескертуді тіркеу", key="manual_warn_btn"):
                st.session_state.tab_warnings += 1
                st.rerun()

        # Жетілдірілген JavaScript: Вкладка ауысқанда автоматты түрде Ескерту батырмасын басады
        st.components.v1.html("""
            <script>
            document.addEventListener("visibilitychange", function() {
                if (document.hidden) {
                    const buttons = window.parent.document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.innerText.includes("Ескертуді тіркеу")) {
                            btn.click();
                            break;
                        }
                    }
                }
            });
            </script>
        """, height=0)

        # Ескертулер мен бұғаттау жүйесі
        warnings = st.session_state.tab_warnings

        if warnings == 1 or warnings == 2:
            st.warning(f"⚠️ **Ескерту ({warnings}/4):** Тест кезінде басқа вкладкаға өтуге болмайды!")
        elif warnings == 3:
            st.warning(f"⚠️ **Ескерту (3/4):** Қайтадан басқа вкладкаға өтпеңіз! Соңғы мүмкіндік!")
        elif warnings == 4:
            st.error("🚨 **НАЗАР АУДАРЫҢЫЗ!** Бұл 4-ші ескерту. Тағы 1 рет ауыстырсаңыз, аккаунт БҰҒАТТАЛАДЫ!")
        elif warnings >= 5:
            curr_user = st.session_state.username
            st.session_state.users[curr_user]["is_blocked"] = True
            st.session_state.logged_in = False
            st.session_state.test_started = False
            st.error("🚫 Ереже бұзылды! Вкладканы 5 рет ауыстырғаныңыз үшін аккаунтыңыз бұғатталды!")
            st.rerun()

        subject = st.session_state.get("selected_subject", ALL_SUBJECTS[0])
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
        subject = st.session_state.get("selected_subject", ALL_SUBJECTS[0])
        filtered_questions = [q for q in st.session_state.questions if q.get("direction") == subject]
        
        score = st.session_state.get("score", 0)
        total = st.session_state.get("total", 0)
        user_answers = st.session_state.get("user_answers", {})

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

# МҰҒАЛІМ КАБИНЕТІ
def teacher_dashboard():
    st.title(f"👩‍🏫 Мұғалім кабинеті: {st.session_state.display_name}")
    
    target_subject = st.session_state.get("teacher_subject", ALL_SUBJECTS[0])
    st.success(f"📌 Сіздің тағайындалған пәніңіз: **{target_subject}**")
    
    st.subheader(f"➕ «{target_subject}» пәніне жаңа сұрақ қосу")
    
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

    if st.button("Сұрақты сақтау", type="primary", use_container_width=True):
        if q_text and len(options_list) == 4 and correct_ans:
            st.session_state.questions.append({
                "direction": target_subject,
                "type": "single" if q_type == "Бір дұрыс жауапты" else "multiple",
                "question": q_text,
                "image": img_url,
                "options": options_list,
                "answer": correct_ans,
                "author": st.session_state.display_name
            })
            save_questions(st.session_state.questions)
            st.success(f"Сұрақ '{target_subject}' пәніне сәтті сақталды!")
            st.rerun()
        else:
            st.error("Барлық өрістерді толық толтырыңыз!")

# ДИРЕКТОР КАБИНЕТІ
def director_dashboard():
    st.title(f"👨‍💼 Директор кабинеті")
    
    tab1, tab2, tab3 = st.tabs(["📊 Оқушылар нәтижесі", "🔑 Аккаунттар & Блоктауды басқару", "🔍 Сұрақтарды басқару & Өшіру"])
    
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
            
            status_str = "🚫 Бұғатталған" if udata.get("is_blocked", False) else "✅ Белсенді"
            
            user_list.append({
                "Логин": uname,
                "Аты-жөні": udata["name"],
                "Пароль": udata["password"],
                "Ролі": role_str,
                "Статусы": status_str
            })
        st.table(user_list)
        
        st.divider()
        st.subheader("⚙️ Аккаунтты өңдеу, бұғаттан шығару немесе өшіру")
        
        all_logins = list(st.session_state.users.keys())
        selected_user_to_edit = st.selectbox("Пайдаланушыны таңдаңыз:", all_logins)
        
        if selected_user_to_edit:
            u_info = st.session_state.users[selected_user_to_edit]
            edit_name = st.text_input("Аты-жөні:", value=u_info["name"], key="edit_u_name")
            edit_pass = st.text_input("Пароль:", value=u_info["password"], key="edit_u_pass")
            is_blocked_status = st.checkbox("🚫 Аккаунт бұғатталған (Бұғаттан шығару үшін осы белгіні алып тастаңыз)", value=u_info.get("is_blocked", False))
            
            col_u_save, col_u_del = st.columns(2)
            
            with col_u_save:
                if st.button("💾 Мәліметтерді сақтау", type="primary"):
                    st.session_state.users[selected_user_to_edit]["name"] = edit_name
                    st.session_state.users[selected_user_to_edit]["password"] = edit_pass
                    st.session_state.users[selected_user_to_edit]["is_blocked"] = is_blocked_status
                    st.success(f"'{selected_user_to_edit}' аккаунты жаңартылды!")
                    st.rerun()

            with col_u_del:
                if selected_user_to_edit == st.session_state.username:
                    st.warning("⚠️ Өз аккаунтыңызды өшіре алмайсыз!")
                else:
                    if st.button("🗑️ Пайдаланушыны өшіру"):
                        del st.session_state.users[selected_user_to_edit]
                        st.success(f"Пайдаланушы '{selected_user_to_edit}' жүйеден өшірілді!")
                        st.rerun()

        st.divider()
        st.write("### ➕ Жаңа пайдаланушы тіркеу")
        new_uname = st.text_input("Логин:", key="new_u_login")
        new_name = st.text_input("Аты-жөні:", key="new_u_name")
        new_pass = st.text_input("Пароль:", key="new_u_pass")
        new_role = st.selectbox("Ролі:", ["student", "teacher"], format_func=lambda x: "Оқушы" if x == "student" else "Мұғалім")
        
        teacher_subj = None
        if new_role == "teacher":
            teacher_subj = st.selectbox("Мұғалімге берілетін пән:", ALL_SUBJECTS)
            
        if st.button("Тіркеу"):
            if new_uname and new_name and new_pass:
                if new_uname in st.session_state.users:
                    st.error("Бұл логин бос емес!")
                else:
                    u_data = {"password": new_pass, "name": new_name, "role": new_role, "active_session_id": "", "is_blocked": False}
                    if new_role == "teacher":
                        u_data["subject"] = teacher_subj
                    st.session_state.users[new_uname] = u_data
                    st.success(f"Пайдаланушы {new_name} сәтті тіркелді!")
                    st.rerun()
            else:
                st.warning("Барлық өрісті толтырыңыз!")

    with tab3:
        st.subheader("🔍 Сұрақтарды іздеу, өзгерту және өшіру")
        
        col_s1, col_s2 = st.columns([2, 1])
        with col_s1:
            search_query = st.text_input("🔍 Іздеу (мәтін немесе автор аты):", placeholder="Іздеу сөзі...").strip().lower()
        with col_s2:
            filter_subj = st.selectbox("Пән бойынша сүзгі:", ["Барлығы"] + ALL_SUBJECTS)
        
        matching_questions = []
        for idx, q in enumerate(st.session_state.questions):
            q_text = q.get("question", "").lower()
            q_author = q.get("author", "Белгісіз").lower()
            q_subj = q.get("direction", "")
            
            matches_search = (search_query in q_text) or (search_query in q_author)
            matches_subj = (filter_subj == "Барлығы") or (filter_subj == q_subj)
            
            if matches_search and matches_subj:
                matching_questions.append((idx, q))
                
        st.write(f"Табылған сұрақтар саны: **{len(matching_questions)}**")
        
        if not matching_questions:
            st.warning("Іздеуге сәйкес сұрақтар табылмады.")
        else:
            q_options = [f"{idx+1}. [{q.get('direction', 'Пәнсіз')}] {q['question']}" for idx, (real_idx, q) in enumerate(matching_questions)]
            selected_match_idx = st.selectbox("Басқару үшін сұрақты таңдаңыз:", range(len(q_options)), format_func=lambda x: q_options[x], key="dir_search_select")
            
            real_index, q_data = matching_questions[selected_match_idx]
            
            st.divider()
            st.info(f"✍️ **Бұл сұрақтың авторы:** {q_data.get('author', 'Белгісіз')}")
            
            edit_subj_index = ALL_SUBJECTS.index(q_data["direction"]) if q_data.get("direction") in ALL_SUBJECTS else 0
            edit_subj = st.selectbox("Пәні:", ALL_SUBJECTS, index=edit_subj_index, key="dir_edit_subj")
            edit_text = st.text_input("Сұрақ мәтіні:", value=q_data["question"], key="dir_edit_text")
            
            opts = q_data["options"]
            col1, col2 = st.columns(2)
            with col1:
                e_opt1 = st.text_input("А нұсқасы:", value=opts[0] if len(opts) > 0 else "", key="dir_e_opt1")
                e_opt2 = st.text_input("В нұсқасы:", value=opts[1] if len(opts) > 1 else "", key="dir_e_opt2")
            with col2:
                e_opt3 = st.text_input("С нұсқасы:", value=opts[2] if len(opts) > 2 else "", key="dir_e_opt3")
                e_opt4 = st.text_input("D нұсқасы:", value=opts[3] if len(opts) > 3 else "", key="dir_e_opt4")
                
            edit_opts_list = [e_opt1, e_opt2, e_opt3, e_opt4]
            
            col_save_dir, col_del_dir = st.columns(2)
            with col_save_dir:
                if st.button("💾 Өзгерісті сақтау", key="dir_save_btn"):
                    st.session_state.questions[real_index]["direction"] = edit_subj
                    st.session_state.questions[real_index]["question"] = edit_text
                    st.session_state.questions[real_index]["options"] = edit_opts_list
                    save_questions(st.session_state.questions)
                    st.success("Сұрақ сәтті жаңартылды!")
                    st.rerun()

            with col_del_dir:
                if st.button("🗑️ Сұрақты өшіру", key="dir_del_btn"):
                    st.session_state.questions.pop(real_index)
                    save_questions(st.session_state.questions)
                    st.success("Сұрақ базадан өшірілді!")
                    st.rerun()

# СЕССИЯНЫ ТЕКСЕРУ (Бір уақытта бір құрылғыдан ғана кіру)
if st.session_state.logged_in:
    current_username = st.session_state.username
    current_session_id = st.session_state.session_id
    
    active_session_in_db = st.session_state.users.get(current_username, {}).get("active_session_id", "")
    
    if current_session_id != active_session_in_db:
        st.session_state.logged_in = False
        st.warning("⚠️ Сіздің аккаунтыңызға басқа құрылғыдан кірді! Жүйеден шығарылдыңыз.")
        st.rerun()

# БАСҚАРУ ЖӘНЕ ІСКЕ ҚОСУ ЛОГИКАСЫ
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
