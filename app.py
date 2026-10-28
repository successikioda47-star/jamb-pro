import streamlit as st
from datetime import date, datetime
import random, time

st.set_page_config(page_title="JAMB CBT Real App", page_icon="💻", layout="centered")

# ===== REAL JAMB APP CSS - LOOKS LIKE REAL CBT =====
st.markdown("""
<style>
.stApp {background:#e9e9e9;}
.cbt-header {background:#008000; color:white; padding:10px 15px; display:flex; justify-content:space-between; align-items:center; border-radius:0px;}
.cbt-subject-bar {background:white; display:flex; gap:5px; padding:10px; overflow-x:auto; border-bottom:2px solid #008000;}
.sub-btn {padding:8px 15px; border-radius:20px; border:1px solid #008000; background:white; color:#008000; font-weight:bold; cursor:pointer; white-space:nowrap;}
.sub-btn.active {background:#008000; color:white;}
.palette {background:white; padding:10px; border-radius:10px; margin:10px 0;}
.q-num {width:35px; height:35px; border-radius:5px; border:1px solid #ccc; display:inline-flex; justify-content:center; align-items:center; margin:3px; font-weight:bold; cursor:pointer;}
.q-num.answered {background:#008000; color:white; border-color:#008000;}
.q-num.current {background:#ffcc00; border-color:#ffcc00;}
.q-num.flagged {background:#ff4444; color:white;}
.question-card {background:white; padding:20px; border-radius:10px; min-height:250px; box-shadow:0 2px 10px rgba(0,0,0,0.1);}
.timer-box {background:black; color:#00ff00; padding:5px 12px; border-radius:5px; font-family:monospace; font-size:20px;}
.instruction {background:white; padding:20px; border-radius:10px; line-height:1.6;}
.result-slip {background:white; border:2px solid #008000; padding:20px; border-radius:10px; font-family:monospace;}
</style>
""", unsafe_allow_html=True)

today = date.today()
random.seed(today.timetuple().tm_yday)

# ===== 40 QUESTIONS PER SUBJECT - REAL FORMAT =====
def load_db():
    base = {
        "English": [
            {"q": "In 'The Life Changer', who is Salma's closest friend?", "o": ["Tomiwa", "Ada", "Ngozi", "Bint"], "a": 1},
            {"q": "Choose the word that is nearest in meaning to 'Eloquent'", "o": ["Fluent in speech", "Dull", "Quiet", "Rude"], "a": 0},
            {"q": "Antonym of 'Abundant' is ____", "o": ["Scarce", "Plenty", "Much", "Full"], "a": 0},
            {"q": "The boy ___ to school yesterday", "o": ["go", "went", "gone", "going"], "a": 1},
            {"q": "Select the correctly spelt word", "o": ["Accomodate", "Accommodate", "Acommodate", "Accommmodate"], "a": 1},
        ] * 8,
        "Mathematics": [
            {"q": "If 2x + 3 = 11, find x", "o": ["4", "3", "5", "2"], "a": 0},
            {"q": "Factorize x² - 9", "o": ["(x-3)(x+3)", "(x-9)(x+1)", "(x-3)²", "(x+3)²"], "a": 0},
            {"q": "Find simple interest on N2000 at 5% for 2 years", "o": ["N200", "N300", "N100", "N400"], "a": 0},
            {"q": "Solve: log₂ 8 = ?", "o": ["3", "2", "4", "1"], "a": 0},
            {"q": "If sin θ = 0.5, θ = ?", "o": ["30°", "60°", "45°", "90°"], "a": 0},
        ] * 8,
        "Physics": [
            {"q": "Unit of Power is?", "o": ["Watt", "Joule", "Newton", "Volt"], "a": 0},
            {"q": "Acceleration due to gravity g = ?", "o": ["9.8 m/s²", "10 m/s²", "8.9 m/s²", "9 m/s²"], "a": 0},
        ] * 20,
        "Chemistry": [
            {"q": "Atomic number of Carbon is?", "o": ["6", "8", "12", "4"], "a": 0},
            {"q": "pH of neutral solution is?", "o": ["7", "0", "14", "1"], "a": 0},
        ] * 20,
    }
    for k in base:
        random.shuffle(base[k])
        base[k] = base[k][:40]
    return base

DB = load_db()

if 'stage' not in st.session_state:
    st.session_state.stage = "instructions"
    st.session_state.subjects = ["English","Mathematics","Physics","Chemistry"]
    st.session_state.current_sub = "English"
    st.session_state.q_index = 0
    st.session_state.answers = {sub: {} for sub in ["English","Mathematics","Physics","Chemistry"]}
    st.session_state.flagged = set()
    st.session_state.start = None

# ===== 1. INSTRUCTIONS SCREEN - LIKE REAL JAMB =====
if st.session_state.stage == "instructions":
    st.markdown('<div class="cbt-header"><b>JAMB - UTME 2026</b><span>Candidate: JAMB PRO</span></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="instruction">
    <h3 style="text-align:center;">INSTRUCTIONS</h3>
    <p>1. This is a MOCK examination with 4 subjects, 40 questions each.</p>
    <p>2. Time allowed is <b>1 Hour 30 Minutes</b> (like real JAMB).</p>
    <p>3. Click on subject tabs to switch subjects.</p>
    <p>4. Click question numbers to navigate. Green = Answered, Yellow = Current, Red = Flagged.</p>
    <p>5. Use Calculator if needed.</p>
    <p>6. You must answer all questions before submission. The system will auto-submit when time is up.</p>
    <p style="text-align:center; color:green;"><b>CHANGES DAILY: Questions shuffle everyday automatically based on date.</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📅 SELECT YEAR", use_container_width=True):
            st.session_state.year = st.selectbox("Year", ["2024","2023","2022","2021"], key="yr")
    with col2:
        if st.button("🚀 START EXAM", type="primary", use_container_width=True):
            st.session_state.stage = "exam"
            st.session_state.start = time.time()
            st.rerun()

# ===== 2. EXAM SCREEN - REAL CBT LOOK =====
elif st.session_state.stage == "exam":
    elapsed = int(time.time() - st.session_state.start) if st.session_state.start else 0
    remaining = max(0, 5400 - elapsed) # 90 mins
    mm, ss = divmod(remaining, 60)
    hh, mm = divmod(mm, 60)
    
    if remaining == 0:
        st.session_state.stage = "result"
        st.rerun()

    # Header like real JAMB
    st.markdown(f"""
    <div class="cbt-header">
    <div><b>Time Left: <span class="timer-box">{hh:02d}:{mm:02d}:{ss:02d}</span></b></div>
    <div>Candidate: JAMB PRO | Centre: LAGOS</div>
    </div>
    """, unsafe_allow_html=True)

    # Subject Bar
    st.markdown('<div class="cbt-subject-bar">', unsafe_allow_html=True)
    cols = st.columns(len(st.session_state.subjects))
    for i, sub in enumerate(st.session_state.subjects):
        with cols[i]:
            active = "active" if sub == st.session_state.current_sub else ""
            if st.button(sub, key=f"sub_{sub}", use_container_width=True):
                st.session_state.current_sub = sub
                st.session_state.q_index = 0
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Main CBT Layout
    left, right = st.columns([3,1])
    
    with left:
        qs = DB[st.session_state.current_sub]
        idx = st.session_state.q_index
        q = qs[idx]
        
        st.markdown(f"""
        <div class="question-card">
        <div style="display:flex; justify-content:space-between;">
        <b>Question {idx+1} of 40 - {st.session_state.current_sub}</b>
        <span><input type="checkbox"> Flag Question</span>
        </div>
        <hr>
        <h4>{q['q']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Options like real JAMB (A, B, C, D)
        labels = ["A", "B", "C", "D"]
        for j, opt in enumerate(q['o']):
            is_selected = st.session_state.answers[st.session_state.current_sub].get(idx) == j
            if st.button(f"{labels[j]}. {opt}", key=f"opt_{idx}_{j}", use_container_width=True, type="primary" if is_selected else "secondary"):
                st.session_state.answers[st.session_state.current_sub][idx] = j
                # auto next
                if idx < 39:
                    st.session_state.q_index += 1
                st.rerun()
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⬅ Previous", disabled=(idx==0), use_container_width=True):
                st.session_state.q_index -=1
                st.rerun()
        with c2:
            if st.button("Flag 🚩", use_container_width=True):
                st.session_state.flagged.add(f"{st.session_state.current_sub}_{idx}")
                st.rerun()
        with c3:
            if st.button("Next ➡", disabled=(idx==39), use_container_width=True):
                st.session_state.q_index +=1
                st.rerun()

    with right:
        st.markdown('<div class="palette">', unsafe_allow_html=True)
        st.write(f"**{st.session_state.current_sub} Palette**")
        # 40 numbers grid
        grid_cols = st.columns(5)
        qs = DB[st.session_state.current_sub]
        for i in range(40):
            with grid_cols[i%5]:
                ans = i in st.session_state.answers[st.session_state.current_sub]
                curr = i == st.session_state.q_index
                flag = f"{st.session_state.current_sub}_{i}" in st.session_state.flagged
                label = f"{'✅' if ans else ''}{i+1}"
                if st.button(label, key=f"pal_{st.session_state.current_sub}_{i}", use_container_width=True):
                    st.session_state.q_index = i
                    st.rerun()
        
        st.divider()
        st.write("Legend: ✅ Answered | ⬜ Not Answered | 🚩 Flagged")
        if st.button("CALCULATOR 🧮", use_container_width=True):
            st.info("2+2=4 - Real JAMB calculator pops here")
        if st.button("SUBMIT EXAM", type="primary", use_container_width=True):
            st.session_state.show_confirm = True
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("show_confirm"):
        st.warning("Are you sure you want to submit? You cannot return.")
        if st.button("YES, SUBMIT NOW"):
            st.session_state.stage = "result"
            st.rerun()

# ===== 3. RESULT SLIP - LIKE REAL JAMB SLIP =====
elif st.session_state.stage == "result":
    st.balloons()
    st.markdown('<div class="cbt-header"><b>JAMB RESULT SLIP 2026</b></div>', unsafe_allow_html=True)
    
    total_score = 0
    breakdown = ""
    for sub in st.session_state.subjects:
        qs = DB[sub]
        correct = sum(1 for i in range(40) if st.session_state.answers[sub].get(i) == qs[i]['a'])
        score = int((correct/40)*100)  # JAMB scores each subject over 100
        total_score += score
        breakdown += f"<tr><td>{sub}</td><td>{correct}/40</td><td>{score}/100</td></tr>"
    
    st.markdown(f"""
    <div class="result-slip">
    <h3 style="text-align:center;">JOINT ADMISSIONS AND MATRICULATION BOARD</h3>
    <p style="text-align:center;">2026 UTME RESULT - PRO MAX MOCK</p>
    <p>Candidate Name: JAMB PRO MAX<br>Reg No: 2026XXXXXXX<br>Date: {today}</p>
    <table style="width:100%; border-collapse:collapse; border:1px solid black;">
    <tr style="background:#008000; color:white;"><th>Subject</th><th>Correct</th><th>Score</th></tr>
    {breakdown}
    <tr style="font-weight:bold; background:#eee;"><td>TOTAL</td><td></td><td>{total_score}/400</td></tr>
    </table>
    <p style="text-align:center; margin-top:15px; font-size:24px; font-weight:bold; color:#008000;">TOTAL: {total_score}/400</p>
    <p style="text-align:center;">{"🔥 EXCELLENT - You will get Medicine/Law!" if total_score>=280 else "✅ GOOD - You will get admission!" if total_score>=200 else "💪 KEEP PRACTICING - Daily practice changes your score!"}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📊 Analysis (Changes daily)")
    for sub in st.session_state.subjects:
        qs = DB[sub]
        correct = sum(1 for i in range(40) if st.session_state.answers[sub].get(i) == qs[i]['a'])
        st.progress(correct/40, text=f"{sub}: {correct}/40")
    
    st.info("📢 AD SPACE: Your AdMob Interstitial ad will show here after result - this is where you make money!")
    
    if st.button("🔄 RETAKE EXAM (New Questions Tomorrow)", type="primary", use_container_width=True):
        st.session_state.stage = "instructions"
        st.session_state.answers = {sub: {} for sub in st.session_state.subjects}
        st.session_state.start = None
        st.rerun()
    
    if st.button("🏠 Back to Home"):
        st.session_state.stage = "instructions"
        st.rerun()

st.markdown(f"<p style='text-align:center; color:#666; font-size:12px;'>App auto-updates daily | Seed: {today} | Real JAMB Clone | Made for you</p>", unsafe_allow_html=True)
