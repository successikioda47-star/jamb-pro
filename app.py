import streamlit as st
import streamlit.components.v1 as components
import time

st.set_page_config(page_title="JAMB CBT 2026", page_icon="📚", layout="centered")

# ===== ADMOB - REPLACE WITH YOUR REAL ID LATER =====
ADMOB_BANNER = """
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3940256099942544" crossorigin="anonymous"></script>
<div style="text-align:center; border:2px dashed green; padding:10px; border-radius:10px;">
BANNER AD - Your AdMob Will Show Here
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3940256099942544" data-ad-slot="6300978111" data-ad-format="auto"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
</div>
"""

# ===== QUESTIONS =====
QUESTIONS = {
    "English": [
        {"q": "What is JAMB full meaning?", "o": ["Joint Admission Board", "Joint Admissions and Matriculation Board", "Joint Matric Board"], "a": 1},
        {"q": "Choose the correct spelling", "o": ["Accomodate", "Accommodate", "Acommodate"], "a": 1},
    ],
    "Mathematics": [
        {"q": "2x + 4 = 10, find x", "o": ["2", "3", "5"], "a": 1},
        {"q": "Solve 5x = 25", "o": ["5", "25", "10"], "a": 0},
    ],
    "Physics": [
        {"q": "Unit of force?", "o": ["Watt", "Newton", "Joule"], "a": 1},
    ],
    "Chemistry": [
        {"q": "H2O is?", "o": ["Salt", "Water", "Acid"], "a": 1},
    ],
    "Biology": [
        {"q": "Powerhouse of cell?", "o": ["Mitochondria", "Nucleus"], "a": 0},
    ]
}

if 'started' not in st.session_state:
    st.session_state.started = False
    st.session_state.subject = None
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answers = {}

def start_exam(subject):
    st.session_state.started = True
    st.session_state.subject = subject
    st.session_state.q_index = 0
    st.session_state.score = 0
    st.session_state.answers = {}

def submit():
    st.session_state.started = False
    st.balloons()
    st.success(f"Exam Submitted! Score: {st.session_state.score}/{len(QUESTIONS[st.session_state.subject])}")
    # INTERSTITIAL AD HERE
    components.html(ADMOB_BANNER, height=150)
    st.session_state.subject = None

# ===== UI =====
st.title("JAMB CBT 2026 PRO")

# Show Banner Ad Top
components.html(ADMOB_BANNER, height=150)

if not st.session_state.started:
    st.subheader("Select Subject")
    cols = st.columns(2)
    i=0
    for sub in QUESTIONS.keys():
        with cols[i%2]:
            if st.button(f"📘 {sub}", use_container_width=True):
                start_exam(sub)
        i+=1
    
    st.markdown("---")
    if st.button("▶ WATCH AD TO UNLOCK 10 YEARS PAST QUESTIONS", type="primary", use_container_width=True):
        st.info("Rewarded Ad - Unlock successful! Replace with your real AdMob Rewarded code later.")
        components.html(ADMOB_BANNER, height=150)

else:
    subject = st.session_state.subject
    qs = QUESTIONS[subject]
    idx = st.session_state.q_index
    q = qs[idx]

    st.subheader(f"{subject} - Question {idx+1}/{len(qs)}")
    st.progress((idx+1)/len(qs))
    st.write(f"**{q['q']}**")

    choice = st.radio("Choose:", q['o'], key=f"q{idx}")
    
    col1, col2 = st.columns(2)
    with col1:
        if idx > 0:
            if st.button("⬅ Back"):
                st.session_state.q_index -= 1
                st.rerun()
    with col2:
        if st.button("Next / Submit ➡", type="primary"):
            # save score
            if q['o'].index(choice) == q['a']:
                if idx not in st.session_state.answers:
                    st.session_state.score += 1
                    st.session_state.answers[idx] = True
            
            if idx < len(qs)-1:
                st.session_state.q_index += 1
                st.rerun()
            else:
                submit()
                st.rerun()

# Bottom Banner
components.html(ADMOB_BANNER, height=150)
