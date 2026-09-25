import streamlit as st

st.title("📚 ҰБТ-ға дайындық тесті")

# Төмендегі тізімге қалағанша сұрақ қоса бересіз:
questions = [
    {
        "question": "Қазақ хандығы қай жылы құрылды?",
        "options": ["1465 ж.", "1723 ж.", "1991 ж.", "1206 ж."],
        "answer": "1465 ж."
    },
    {
        "question": "Қазақстанның астанасы қай қала?",
        "options": ["Алматы", "Шымкент", "Астана", "Ақтөбе"],
        "answer": "Астана"
    }
]

score = 0

for i, q in enumerate(questions):
    st.subheader(f"{i+1}-сұрақ: {q['question']}")
    user_choice = st.radio(f"Жауапты таңдаңыз:", q['options'], key=i)
    if user_choice == q['answer']:
        score += 1

if st.button("Нәтижені тексеру"):
    st.success(f"Сіздің нәтижеңіз: {score} / {len(questions)}")
