# Оқушы кабинеті
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
        
        # ----------------------------------------------------
        # Вкладка ауыстыруды бақылайтын жаңартылған механизм
        # ----------------------------------------------------
        col_warn1, col_warn2 = st.columns([3, 1])
        with col_warn2:
            # Қолдан немесе авто-кликтен ескертуді тіркеу батырмасы
            if st.button("🔔 Ескертуді тіркеу", key="manual_warn_btn"):
                st.session_state.tab_warnings += 1
                st.rerun()

        # Браузерде вкладка ауысқанын анықтайтын сенімді JS скрипт
        st.components.v1.html("""
            <script>
            document.addEventListener("visibilitychange", function() {
                if (document.hidden) {
                    // Streamlit батырмасын табу және басу
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

        # Ескертулерді көрсету логикасы
        warnings = st.session_state.tab_warnings

        if warnings == 1 or warnings == 2:
            st.warning(f"⚠️ **Ескерту ({warnings}/4):** Тест кезінде басқа вкладкаға өтуге болмайды!")
        elif warnings == 3:
            st.warning(f"⚠️ **Ескерту (3/4):** Қайтадан басқа вкладкаға өтпеңіз! Соңғы мүмкіндік!")
        elif warnings == 4:
            st.error("🚨 **НАЗАР АУДАРЫҢЫЗ!** Бұл 4-ші ескерту. Тағы 1 рет ауыстырсаңыз, аккаунт БҰҒАТТАЛАДЫ!")
        elif warnings >= 5:
            # 5-ші рет ауыстырғанда бұғаттау
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
