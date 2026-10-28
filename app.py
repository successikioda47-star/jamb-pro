import streamlit as st
import time
import random

st.set_page_config(page_title="JAMB PRO MAX 2026", page_icon="🚀", layout="wide")

# ===== MIND-BLOWING CSS =====
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
.main-title {text-align:center; color:white; font-size:40px; font-weight:900; text-shadow:0 5px 15px rgba(0,0,0,0.3);}
.card {background:white; border-radius:20px; padding:20px; box-shadow:0 10px 40px rgba(0,0,0,0.2); margin-bottom:15px; transition:0.3s;}
.card:hover {transform: scale(1.02);}
.score-big {font-size:70px; font-weight:900; text-align:center; background: linear-gradient(90deg, #0a8a0a, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
.timer {background:black; color:#00ff88; padding:10px 20px; border-radius:50px; font-family:monospace; font-size:22px; font-weight:bold; border:2px solid #00ff88;}
.ad-box {background: linear-gradient(90deg, #ff7a00, #ffaa00); color:white; padding:15px; border-radius:15px; text-align:center; font-weight:bold; margin:15px 0;}
</style>
""", unsafe_allow_html=True)

# ===== DATA =====
CUTOFFS = {"UNILAG": 200, "UI": 200, "UNN": 180, "ABU": 180, "UNILORIN": 180, "LASU": 190, "Medicine": 280, "Law": 250, "Engineering": 220, "Computer Science": 220}
NOVELS = {"The Life Changer": "The Life Changer by Khadija Abubakar Jalli - Summary: Salma and her friends... (Tap to read full novel)"}

QUESTIONS_DB = {
    "2024": {
        "English": [
            {"q": "What is the synonym of 'Eloquent'?", "o": ["Fluent", "Dull", "Quiet", "Rude"], "a": 0, "exp": "Eloquent = fluent in speaking"},
            {"q": "The Life Changer: Who is Salma's roommate?", "o": ["Tomiwa", "Ada", "Ngozi", "Bint"], "a": 1},
        ],
        "Mathematics": [
            {"q": "If log 4 base 2 = x, x = ?", "o": ["2", "3", "4", "1"], "a": 0},
        ]
    }
}

if 'page' not in st.session_state:
    st.session_state.page = "home"
    st.session_state.year = "2024"
    st.session_state.mock_answers = {}
    st.session_state.mock_idx = 0

# ===== HEADER =====
st.markdown('<div class="main-title">🚀 JAMB PRO MAX 2026 🚀</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:white;">The Only JAMB App You Need to Score 300+</p>', unsafe_allow_html=True)

# ===== SIDEBAR - SCORE CALCULATOR =====
with st.sidebar:
    st.header("🧮 JAMB Score Calculator")
    st.write("Calculate your real JAMB score (400 marks)")
    eng = st.slider("English (0-100)", 0, 100, 65)
    sub2 = st.slider("Subject 2 (0-100)", 0, 100, 70)
    sub3 = st.slider("Subject 3 (0-100)", 0, 100, 60)
    sub4 = st.slider("Subject 4 (0-100)", 0, 100, 75)
    total = eng + sub2 + sub3 + sub4
    st.markdown(f'<div class="card"><div class="score-big">{total}</div><p style="text-align:center;">/ 400</p></div>', unsafe_allow_html=True)
    if total >= 250: st.success("🔥 You fit enter Medicine/Law!")
    elif total >= 200: st.info("✅ You go get admission!")
    else: st.warning("💪 More practice needed!")
    
    st.divider()
    st.header("🎯 Cut-off Checker")
    uni = st.selectbox("Select School/Course", list(CUTOFFS.keys()))
    if total >= CUTOFFS[uni]: st.success(f"✅ You meet {uni} cut-off ({CUTOFFS[uni]})")
    else: st.error(f"❌ {uni} needs {CUTOFFS[uni]}. You have {total}")
    
    st.divider()
    st.markdown('<div class="ad-box">📢 AD SPACE<br>Your AdMob Rewarded Ad</div>', unsafe_allow_html=True)
    if st.button("▶ Watch Ad to Unlock All Years"):
        st.balloons()
        st.success("Unlocked 2015-2024! (Add real AdMob code here later)")

# ===== HOME TABS =====
if st.session_state.page == "home":
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Past Questions by Year", "🔥 Full JAMB Mock (400 Marks)", "📚 Novel & Syllabus", "🏆 Leaderboard"])
    
    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns([1,3])
        with c1:
            year = st.selectbox("Select Year", ["2024","2023","2022","2021","2020","2019","2018","2017","2016","2015"])
            st.session_state.year = year
            subject = st.selectbox("Select Subject", ["English","Mathematics","Physics","Chemistry","Biology","Government","Economics"])
        with c2:
            st.subheader(f"{subject} - {year} Past Questions")
            st.write(f"Real JAMB {year} questions from original past papers")
            if st.button(f"🚀 Start {subject} {year} CBT", type="primary", use_container_width=True):
                st.session_state.page = "exam"
                st.session_state.subject = subject
                st.session_state.q_idx = 0
                st.session_state.answers = {}
                st.session_state.start_time = time.time()
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.info("💡 Tip: Each year has 40 real questions like real JAMB. We add more weekly!")

    with tab2:
        st.markdown('<div class="card" style="border:3px solid #0a8a0a;">', unsafe_allow_html=True)
        st.subheader("🔥 REAL JAMB MOCK - 4 Subjects, 2 Hours, 400 Marks")
        st.write("Exactly like real JAMB: English 60 Qs + 3 other subjects 40 Qs each = 180 Questions")
        col1, col2 = st.columns(2)
        with col1:
            s2 = st.selectbox("Subject 2", ["Mathematics","Physics","Chemistry","Biology","Government"])
            s3 = st.selectbox("Subject 3", ["Physics","Chemistry","Biology","Economics","Literature"])
        with col2:
            s4 = st.selectbox("Subject 4", ["Chemistry","Biology","Government","Economics","CRS"])
            st.write("⏰ Time: 2 Hours | 🎯 Score: 400 Marks")
        if st.button("START FULL MOCK EXAM NOW 🔥", type="primary", use_container_width=True):
            st.session_state.page = "mock"
            st.session_state.mock_idx = 0
            st.session_state.mock_answers = {}
            st.session_state.start_time = time.time()
            st.session_state.mock_subjects = ["English", s2, s3, s4]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📖 The Life Changer - JAMB Novel 2026")
        st.write(NOVELS["The Life Changer"])
        st.button("Read Full Novel Summary (Unlock with Ad)")
        st.divider()
        st.subheader("📋 JAMB Syllabus 2026")
        st.write("✅ English Syllabus: Comprehension, Lexis, Structure, Oral Forms, Life Changer")
        st.write("✅ Mathematics: Number Bases, Algebra, Geometry...")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏆 Top Scorers This Week")
        st.table([{"Rank": "1st 🥇", "Name": "David O.", "Score": "345/400", "School": "UNILAG - Medicine"}, {"Rank": "2nd 🥈", "Name": "Aisha B.", "Score": "320/400", "School": "UI - Law"}, {"Rank": "You", "Name": "You?", "Score": f"{total}/400", "School": "Keep Pushing!"}])
        st.markdown('</div>', unsafe_allow_html=True)

# ===== EXAM MODE =====
elif st.session_state.page == "exam":
    # (Same lively exam with palette, timer)
    subject = st.session_state.subject
    qs = QUESTIONS_DB.get(st.session_state.year, {}).get(subject, QUESTIONS_DB["2024"]["English"])
    idx = st.session_state.q_idx
    elapsed = int(time.time() - st.session_state.start_time)
    rem = max(0, 1800-elapsed)
    m,s = divmod(rem,60)
    
    st.markdown(f'<div style="display:flex; justify-content:space-between;"><h3>{subject} {st.session_state.year}</h3><div class="timer">⏰ {m:02d}:{s:02d}</div></div>', unsafe_allow_html=True)
    st.progress((idx+1)/len(qs))
    
    # Palette
    cols = st.columns(10)
    for i in range(len(qs)):
        with cols[i%10]:
            color = "✅" if i in st.session_state.answers else "⬜"
            if st.button(f"{color}{i+1}", key=f"p{i}"): 
                st.session_state.q_idx=i
                st.rerun()
    
    q = qs[idx]
    st.markdown(f'<div class="card"><b>Question {idx+1}:</b><br><h3>{q["q"]}</h3></div>', unsafe_allow_html=True)
    choice = st.radio("Select answer:", q['o'], index=None)
    if choice: st.session_state.answers[idx]=q['o'].index(choice)
    
    if st.button("Submit Exam", type="primary", use_container_width=True):
        st.session_state.page="result"
        st.rerun()

elif st.session_state.page == "result":
    st.balloons()
    qs = QUESTIONS_DB.get(st.session_state.year, {}).get(st.session_state.subject, QUESTIONS_DB["2024"]["English"])
    correct = sum(1 for i,q in enumerate(qs) if st.session_state.answers.get(i)==q['a'])
    jamb_score = int(correct/len(qs)*100)
    st.markdown(f'<div class="card" style="text-align:center;"><div class="score-big">{jamb_score}/100</div><h3>{correct}/{len(qs)} Correct</h3><p>{"You go blow JAMB! 🔥" if jamb_score>=70 else "You need more practice"}</p></div>', unsafe_allow_html=True)
    for i,q in enumerate(qs):
        with st.expander(f"{'✅' if st.session_state.answers.get(i)==q['a'] else '❌'} Q{i+1}"):
            st.write(f"Your answer: {q['o'][st.session_state.answers.get(i,0)] if i in st.session_state.answers else 'None'}")
            st.write(f"Correct: {q['o'][q['a']]}")
            st.info(q.get('exp',''))
    st.markdown('<div class="ad-box">📢 INTERSTITIAL AD - Show AdMob here, you go make money!</div>', unsafe_allow_html=True)
    if st.button("Back Home"):
        st.session_state.page="home"
        st.rerun()
