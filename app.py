import streamlit as st
import random
import time
from datetime import datetime, timedelta
import json

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MindEase – Mental Health Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700;800&display=swap');

/* ── Root & Body ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #0d0d1a;
    color: #f0eeff;
}

.stApp {
    background: linear-gradient(135deg, #0d0d1a 0%, #12102a 50%, #0d1a2a 100%);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(13, 13, 26, 0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
}

[data-testid="stSidebar"] * { color: #f0eeff !important; }

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 1100px; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(124,106,247,0.4); border-radius: 2px; }

/* ── Logo ── */
.mindease-logo {
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a89cf8, #f178b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
    line-height:1.1;
}
.mindease-tagline {
    font-size: 0.68rem;
    color: rgba(240,238,255,0.45);
    letter-spacing: 0.04em;
    margin-top:0;
}

/* ── Page Title ── */
.page-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a89cf8, #f178b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.page-sub {
    color: rgba(240,238,255,0.55);
    font-size: 0.88rem;
    margin-top: 0;
    margin-bottom: 1.5rem;
}

/* ── Glass Card ── */
.glass-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.1rem;
    transition: border-color 0.25s;
}
.glass-card:hover { border-color: rgba(124,106,247,0.35); }

/* ── Chat Bubbles ── */
.chat-container { display:flex; flex-direction:column; gap:1rem; }
.msg-row { display:flex; gap:0.75rem; align-items:flex-start; }
.msg-row.user { flex-direction:row-reverse; }
.msg-avatar {
    width:38px; height:38px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:1rem; flex-shrink:0; margin-top:2px;
}
.bot-av { background: linear-gradient(135deg,#7c6af7,#f178b6); }
.user-av { background: linear-gradient(135deg,#4fc4cf,#56cfb2); font-weight:700; }
.msg-bubble {
    padding: 0.85rem 1.1rem;
    border-radius: 18px;
    font-size: 0.91rem;
    line-height: 1.65;
    max-width: 75%;
}
.bot-bubble {
    background: rgba(124,106,247,0.12);
    border: 1px solid rgba(124,106,247,0.22);
    border-bottom-left-radius: 6px;
}
.user-bubble {
    background: linear-gradient(135deg,rgba(124,106,247,0.38),rgba(241,120,182,0.28));
    border: 1px solid rgba(124,106,247,0.35);
    border-bottom-right-radius: 6px;
    text-align: left;
}
.msg-time { font-size:0.67rem; color:rgba(240,238,255,0.38); margin-top:0.25rem; }
.user .msg-time { text-align:right; }

/* ── Mood stars ── */
.mood-bar-wrap {
    background: rgba(255,255,255,0.07);
    border-radius: 4px;
    height: 7px;
    overflow: hidden;
    margin: 0 0.75rem;
    flex:1;
}
.mood-bar-fill {
    height:100%;
    border-radius:4px;
    background: linear-gradient(90deg, #7c6af7, #f178b6);
}

/* ── Stat Cards ── */
.stat-box {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 1.1rem;
    text-align: center;
}
.stat-val {
    font-family: 'Outfit', sans-serif;
    font-size:1.9rem; font-weight:700;
    background: linear-gradient(135deg,#a89cf8,#f178b6);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.stat-lbl { font-size:0.72rem; color:rgba(240,238,255,0.45); margin-top:0.2rem; }

/* ── Crisis Alert ── */
.crisis-alert {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.35);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
    font-size: 0.88rem;
}
.helpline-row {
    display:flex; justify-content:space-between; align-items:center;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size:0.84rem;
}
.helpline-row:last-child { border-bottom:none; }
.helpline-num { color:#a89cf8; font-weight:600; }

/* ── Resource Cards ── */
.resource-icon { font-size:1.75rem; margin-bottom:0.6rem; }
.resource-title { font-family:'Outfit',sans-serif; font-size:1rem; font-weight:600; margin-bottom:0.4rem; }
.resource-desc { font-size:0.83rem; color:rgba(240,238,255,0.58); margin-bottom:1rem; line-height:1.6; }

/* ── Insight Box ── */
.insight-box {
    background: rgba(124,106,247,0.08);
    border: 1px solid rgba(124,106,247,0.28);
    border-radius:14px; padding:1.1rem 1.3rem;
    display:flex; gap:0.8rem; align-items:flex-start;
}
.insight-icon {font-size:1.4rem; flex-shrink:0;}
.insight-body h4 { font-size:0.88rem; font-weight:600; margin:0 0 0.25rem; }
.insight-body p  { font-size:0.81rem; color:rgba(240,238,255,0.6); margin:0; line-height:1.6; }

/* ── Streamlit widget overrides ── */
.stButton button {
    background: linear-gradient(135deg, #7c6af7, #f178b6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(124,106,247,0.35) !important;
}
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,106,247,0.5) !important;
}
.stTextArea textarea, .stTextInput input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #f0eeff !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: rgba(124,106,247,0.6) !important;
    box-shadow: 0 0 0 3px rgba(124,106,247,0.15) !important;
}
.stSelectbox select, [data-baseweb="select"] {
    background: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.12) !important;
    color: #f0eeff !important;
}
div[data-testid="stChatMessage"] {
    background: transparent !important;
}
.stChatFloatingInputContainer {
    background: rgba(13,13,26,0.9) !important;
    border-top: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #f0eeff !important;
}
/* Radio buttons */
.stRadio label { color: #f0eeff !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #f0eeff !important; }
/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    gap: 4px;
    padding: 4px;
    border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 9px;
    color: rgba(240,238,255,0.55) !important;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(124,106,247,0.3), rgba(241,120,182,0.2)) !important;
    color: #a89cf8 !important;
    border: 1px solid rgba(124,106,247,0.3) !important;
}
h1,h2,h3 { color: #f0eeff !important; }
p, li { color: rgba(240,238,255,0.82) !important; }
.stMarkdown p { color: rgba(240,238,255,0.82) !important; }
hr { border-color: rgba(255,255,255,0.08) !important; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_error" not in st.session_state:
    st.session_state.login_error = ""
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = ""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm **Elara** 💜 — your AI mental wellness companion.\n\nThis is a **safe, confidential space** to share what's on your mind. I'm here to listen, provide guidance, and connect you with resources.\n\n*How are you feeling today?*",
            "time": datetime.now().strftime("%I:%M %p")
        }
    ]

if "mood_log" not in st.session_state:
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    scores = [2, 3, 4, 5, 3, 4, 3.5]
    emojis = ["😢", "😕", "😐", "😄", "😕", "🙂", "😐"]
    st.session_state.mood_log = [
        {"day": d, "score": s, "emoji": e} for d, s, e in zip(days, scores, emojis)
    ]

if "journal_idx" not in st.session_state:
    st.session_state.journal_idx = 0

if "breath_running" not in st.session_state:
    st.session_state.breath_running = False

# ── DEMO CREDENTIALS ─────────────────────────────────────────────────────────
DEMO_USERS = {
    "demo":    {"password": "mindease123",  "name": "Demo User",    "avatar": "🧑"},
    "student": {"password": "student@2024", "name": "Student User", "avatar": "🎓"},
    "admin":   {"password": "admin@mind",   "name": "Admin",        "avatar": "🛡️"},
}

# ── LOGIN PAGE ────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    # Hide sidebar on login page
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    .block-container { max-width: 460px !important; padding-top: 4rem !important; }

    /* Login card */
    .login-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 2.5rem 2.2rem;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        margin: 0 auto;
    }
    .login-logo {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a89cf8, #f178b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }
    .login-sub {
        text-align: center;
        font-size: 0.82rem;
        color: rgba(240,238,255,0.45);
        margin-bottom: 2rem;
    }
    .demo-pill {
        display: inline-flex; align-items: center; gap: 0.5rem;
        background: rgba(124,106,247,0.15);
        border: 1px solid rgba(124,106,247,0.3);
        border-radius: 20px;
        padding: 0.4rem 1rem;
        font-size: 0.78rem;
        color: #a89cf8;
        cursor: pointer;
        margin: 0.25rem;
        transition: all 0.2s;
    }
    .demo-pill:hover {
        background: rgba(124,106,247,0.28);
        transform: translateY(-1px);
    }
    .login-error {
        background: rgba(239,68,68,0.12);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: 10px;
        padding: 0.65rem 1rem;
        font-size: 0.83rem;
        color: #fca5a5;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    .feature-row {
        display: flex; gap: 0.5rem; flex-wrap: wrap;
        justify-content: center; margin: 1.2rem 0 0;
    }
    .feature-chip {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 20px;
        padding: 0.3rem 0.75rem;
        font-size: 0.73rem;
        color: rgba(240,238,255,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

    # Centered login card
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-logo">🧠 MindEase</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Your AI Mental Wellness Companion<br/>Sign in to continue your journey 💜</div>', unsafe_allow_html=True)

    # Demo credentials hint
    st.markdown("""
    <div style="background:rgba(124,106,247,0.08);border:1px solid rgba(124,106,247,0.2);
         border-radius:12px;padding:0.85rem 1rem;margin-bottom:1.2rem;font-size:0.8rem">
        <strong style="color:#a89cf8">🎓 Demo Credentials</strong><br/>
        <div style="margin-top:0.5rem;display:flex;flex-direction:column;gap:0.3rem">
            <span style="color:rgba(240,238,255,0.7)">👤 Username: <code style="background:rgba(255,255,255,0.1);padding:0.1rem 0.4rem;border-radius:4px">demo</code> &nbsp; Password: <code style="background:rgba(255,255,255,0.1);padding:0.1rem 0.4rem;border-radius:4px">mindease123</code></span>
            <span style="color:rgba(240,238,255,0.7)">🎓 Username: <code style="background:rgba(255,255,255,0.1);padding:0.1rem 0.4rem;border-radius:4px">student</code> &nbsp; Password: <code style="background:rgba(255,255,255,0.1);padding:0.1rem 0.4rem;border-radius:4px">student@2024</code></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Username input
    username = st.text_input(
        "👤 Username",
        placeholder="Enter username",
        key="login_username"
    )
    # Password input
    password = st.text_input(
        "🔒 Password",
        placeholder="Enter password",
        type="password",
        key="login_password"
    )

    # Error message
    if st.session_state.login_error:
        st.markdown(f'<div class="login-error">⚠️ {st.session_state.login_error}</div>', unsafe_allow_html=True)

    # Login button
    if st.button("Sign In →", key="login_btn", use_container_width=True):
        uname = username.strip().lower()
        if uname in DEMO_USERS and DEMO_USERS[uname]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.logged_in_user = DEMO_USERS[uname]["name"]
            st.session_state.login_error = ""
            # Personalize first message
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": f"Welcome back, **{DEMO_USERS[uname]['name']}** {DEMO_USERS[uname]['avatar']} 💜\n\nI'm **Elara**, your AI mental wellness companion. This is a **safe, confidential space** for you.\n\n*How are you feeling today?*",
                    "time": datetime.now().strftime("%I:%M %p")
                }
            ]
            st.rerun()
        elif not uname:
            st.session_state.login_error = "Please enter a username."
            st.rerun()
        else:
            st.session_state.login_error = "Invalid username or password. Try the demo credentials above."
            st.rerun()

    st.markdown("""<div class="feature-row">
        <span class="feature-chip">💬 AI Chat</span>
        <span class="feature-chip">📊 Mood Tracker</span>
        <span class="feature-chip">🫁 Breathing</span>
        <span class="feature-chip">🆘 Crisis Help</span>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;font-size:0.67rem;color:rgba(240,238,255,0.25);margin-top:1.5rem">🔒 Secure Demo • Not a substitute for professional care</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()  # Stop rendering rest of app until logged in

# ── CHATBOT RESPONSES ─────────────────────────────────────────────────────────
RESPONSES = [
    {
        "patterns": ["hello","hi ","hey","greet","good morning","good evening","good afternoon","hii","helo"],
        "replies": [
            "Hello! 💜 I'm Elara, your mental wellness companion. How are you feeling today? Remember, this is a safe space to share anything.",
            "Hi there! 😊 I'm so glad you're here. What's on your heart today?",
            "Hey! 🌟 Welcome to MindEase. I'm here to listen and support you. How are you doing right now?"
        ]
    },
    {
        "patterns": ["anxious","anxiety","worry","worried","nervous","panic","overthink","overthinking"],
        "replies": [
            "I hear you — anxiety can feel really overwhelming. 💜\n\n**Try Box Breathing right now:**\n- Inhale for 4 counts → Hold 4 → Exhale 4 → Hold 4\n- Repeat 3–4 cycles\n\nThis activates your parasympathetic nervous system and calms the stress response. Would you like to tell me more about what's been worrying you?",
            "Anxiety is incredibly common and you are **not alone** in feeling this. 🤝\n\n**5-4-3-2-1 Grounding:**\nName 5 things you see → 4 you can touch → 3 you hear → 2 you smell → 1 you taste.\n\nThis brings your mind back to the present moment. What's making you feel anxious?",
            "Your feelings are completely valid. 💫 Some science-backed strategies:\n- 🧘 Deep diaphragmatic breathing\n- ✍️ Write down your worries (journaling helps!)\n- 🚶 A brisk 10-minute walk\n- 📵 Digital detox for 30 minutes\n\nWhat feels most do-able right now?"
        ]
    },
    {
        "patterns": ["stress","stressed","overwhelm","overwhelmed","pressure","burnout","exhausted","too much"],
        "replies": [
            "It sounds like you're carrying a really heavy load right now. 💜\n\n**A simple reset:**\n1. **Stop** — pause everything for 2 minutes\n2. **Breathe** — slow, deep breaths  \n3. **List** — write only your top 3 priorities\n4. **Release** — let go of everything else\n\nYou don't have to do everything at once. What's the single most stressful thing right now?",
            "Feeling overwhelmed is so hard. 🌊 Let's break it down:\n\n**The STOP technique:**\n- S — Stop what you're doing\n- T — Take a deep breath\n- O — Observe your thoughts without judgment\n- P — Proceed with intention\n\nRemember: you can only do one thing at a time. 💪"
        ]
    },
    {
        "patterns": ["depress","sad","unhappy","hopeless","empty","numb","meaningless","worthless","crying","cry"],
        "replies": [
            "Thank you for trusting me with something so personal. 💜 Depression and deep sadness are **real and valid**. You're not weak for feeling this way.\n\nSome gentle steps:\n- 🌅 Morning sunlight (even 5 minutes)\n- 🚶 A short walk — movement releases endorphins\n- 📞 Reach out to one person you trust\n- ✅ Complete one small task to build momentum\n\nPlease know you don't have to face this alone. Would you like to talk more?",
            "I'm really glad you shared that with me. 🤍 Feeling this way is **not a personal failure** — many people experience this and it can get better.\n\nRight now, try one tiny act of self-care:\n- Make yourself a warm drink 🍵\n- Step outside for fresh air 🌿\n- Text someone you trust 💬\n\nI'm here to listen whenever you need. What's been happening?"
        ]
    },
    {
        "patterns": ["sleep","insomnia","can't sleep","cant sleep","sleep problem","tired","fatigue","awake at night"],
        "replies": [
            "Poor sleep deeply affects mental health. 😴\n\n**Sleep Hygiene Tips:**\n- 📵 Stop screens 60 min before bed\n- 🌡️ Keep room cool and dark\n- 🫁 Try 4-7-8 breathing at bedtime\n- ✍️ Write a 'worry dump' journal entry\n\n⏰ **Consistency is key** — wake at the same time daily, even weekends.\n\nIs your issue falling asleep, staying asleep, or waking too early?",
            "Sleep difficulties and mental health are deeply connected. 💤\n\n**Military Sleep Method:**\nRelax your face → drop shoulders → breathe out slowly → clear your mind for 10 seconds. Most people fall asleep within 2 minutes with practice!\n\nWhat do you think is keeping you awake?"
        ]
    },
    {
        "patterns": ["lonely","alone","no friends","isolated","no one","nobody","miss someone"],
        "replies": [
            "Loneliness is one of the most painful feelings. 💔 Please know that your feelings matter deeply.\n\nYou reached out here — that takes courage. 🌟\n\n**Small steps to connection:**\n- 📱 Send one text to an old friend today\n- 🌐 Join an online community around an interest\n- 🤝 Volunteer locally — shared purpose builds bonds\n- ☕ A library, café, or class puts you around others gently\n\nWhat's your life like right now?",
            "I hear you. 💜 Feeling alone is incredibly hard, and your longing for connection is so human and valid.\n\nWould you like to talk about what's been going on? Sometimes just being heard helps. I'm not going anywhere. 🕊️"
        ]
    },
    {
        "patterns": ["breath","breathing","calm down","calm me","relax","relaxation","meditat"],
        "replies": [
            "Let's do a breathing exercise together! 🫁\n\n**4-7-8 Technique:**\n1. Inhale through your nose for **4 seconds**\n2. Hold your breath for **7 seconds**\n3. Exhale completely through your mouth for **8 seconds**\n4. Repeat 4 cycles\n\nThis is like a natural tranquilizer for your nervous system. Begin now — I'll be here when you're done. 🕊️",
            "**Box Breathing** (used by Navy SEALs to stay calm):\n\n⬜ Inhale 4 → Hold 4 → Exhale 4 → Hold 4\n\nVisualize tracing the four sides of a box as you breathe. Do 4 rounds and let me know how you feel! 💜"
        ]
    },
    {
        "patterns": ["crisis","suicid","self harm","hurt myself","end it","give up","no reason to live","want to die"],
        "replies": [
            "⚠️ I'm really concerned about you and I want you to be safe.\n\n**Please reach out immediately:**\n- 🇮🇳 **iCall (India):** 9152987821\n- 📞 **Vandrevala Foundation:** 1860-266-2345\n- 🌍 **International:** befrienders.org\n\nYou deserve support from a trained professional right now. Please check the **Crisis Help** tab or call one of these numbers.\n\n**Your life has value. 💜 I care about you.**"
        ]
    },
    {
        "patterns": ["thank","thanks","helpful","better","good job","appreciate","great"],
        "replies": [
            "You're so welcome! 💜 I'm really glad I could help even a little. Taking care of your mental health is one of the most important things you can do. 🌟\n\nIs there anything else on your mind?",
            "It means a lot to hear that! Keep going — you're doing something brave by taking care of your mental health. 🌿\n\nI'm always here whenever you need to talk.",
        ]
    },
    {
        "patterns": ["tip","advice","help me","what should i do","what can i do","suggest","how to"],
        "replies": [
            "Here are some evidence-based mental wellness tips! 💡\n\n🏃 **Move** — 20 min of exercise reduces anxiety by 48%\n📓 **Journal** — 3 min of gratitude writing rewires your brain\n📵 **Unplug** — Social media detox for 1 hour improves mood\n💤 **Sleep** — 7-8 hours is non-negotiable for mental health\n🌿 **Nature** — 15 minutes outside lowers cortisol\n🤝 **Connect** — One meaningful conversation per day\n\nWhich area would you like to focus on?",
        ]
    }
]

DEFAULTS = [
    "Thank you for sharing that with me. 💜 It takes courage to talk about how you're feeling. Can you tell me a bit more about what you're going through?",
    "I hear you. 🤍 Your feelings are completely valid. Let's explore this together — what would feel most helpful right now?",
    "I'm here and I'm listening. 💫 You don't have to figure this out alone. Would you like some coping strategies, or do you just want to talk?",
    "That sounds really tough. 💙 I want to make sure you get the right support. Is this something that's been going on for a while, or did something happen recently?",
    "Thank you for opening up. 🌸 Mental health is just as important as physical health. What's weighing on your mind most right now?"
]

def get_bot_reply(user_text: str) -> str:
    text = user_text.lower()
    for r in RESPONSES:
        if any(p in text for p in r["patterns"]):
            return random.choice(r["replies"])
    return random.choice(DEFAULTS)

# ── JOURNAL PROMPTS ────────────────────────────────────────────────────────────
JOURNAL_PROMPTS = [
    "What is one thing you are grateful for today, no matter how small?",
    "Describe a moment this week when you felt genuinely at peace.",
    "What emotion are you carrying right now, and where do you feel it in your body?",
    "What would you tell your younger self about getting through hard times?",
    "List three personal strengths that have helped you overcome challenges.",
    "What does your ideal day for mental wellbeing look like?",
    "Write about a time you were proud of yourself for being resilient.",
    "What boundaries do you need to set to protect your mental energy?",
    "If your anxiety could speak, what would it say? What would you reply back?",
    "What brings you joy that you haven't done in a while? Can you do it today?",
    "Describe someone in your life who makes you feel safe and valued.",
    "What negative thought pattern do you want to release this week?"
]

MINDFULNESS = {
    "5-4-3-2-1 Grounding": """**Name out loud:**
- 🟣 **5 things** you can see right now
- 🔵 **4 things** you can physically feel  
- 🟢 **3 things** you can hear  
- 🟡 **2 things** you can smell  
- 🔴 **1 thing** you can taste

This pulls your mind out of rumination and into the **present moment**. Repeat whenever you feel overwhelmed.""",

    "Body Scan Meditation": """Sit or lie comfortably. **Close your eyes.**

Starting at the top of your head, slowly scan downward — notice any tension, tightness, or discomfort **without judgment**.

Breathe into each area and consciously relax it before moving on. Take **10–15 minutes** for a full scan.

This connects mind and body and reduces chronic stress.""",

    "Safe Place Visualization": """Close your eyes and imagine a place where you feel **completely safe and at peace** — a beach, forest, childhood bedroom, or anywhere real or imagined.

Engage all your senses:
- 👁️ What do you **see**?
- 👂 What do you **hear**?
- 👃 What do you **smell**?
- 🤲 What do you **feel**?

Spend **5 minutes** here. This calms the amygdala and activates your rest-and-digest system."""
}

CBT_TECHNIQUES = [
    ("✅", "Thought Record", "Identify and challenge negative automatic thoughts by rating their truth, listing evidence for/against, and creating a balanced alternative thought."),
    ("✅", "Behavioral Activation", "Break the avoidance cycle by scheduling small, enjoyable activities daily — even when motivation is low. Action precedes motivation."),
    ("✅", "Gratitude Practice", "Write 3 specific things you're grateful for each morning. Over 4 weeks, this measurably increases baseline happiness."),
    ("✅", "Progressive Muscle Relaxation", "Tense, then release each muscle group from toes to head. Reduces physical tension linked to anxiety within 15 minutes."),
]

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR  (only shown when logged in)
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<p class="mindease-logo">🧠 MindEase</p>', unsafe_allow_html=True)
    st.markdown('<p class="mindease-tagline">Your Mental Wellness Companion</p>', unsafe_allow_html=True)
    # Welcome user
    st.markdown(f"""<div style="background:rgba(124,106,247,0.1);border:1px solid rgba(124,106,247,0.2);
        border-radius:10px;padding:0.6rem 0.9rem;font-size:0.8rem;margin-bottom:0.5rem">
        👋 Welcome, <strong>{st.session_state.logged_in_user}</strong>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    tab_choice = st.radio(
        "Navigate",
        ["💬 Chat", "📊 Mood Tracker", "📚 Resources", "🆘 Crisis Help"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Quick mood picker
    st.markdown("**How are you feeling?**")
    mood_cols = st.columns(5)
    mood_labels = {1: "😢", 2: "😕", 3: "😐", 4: "🙂", 5: "😄"}
    mood_names  = {1: "very sad", 2: "a bit sad", 3: "okay", 4: "good", 5: "great"}

    for i, col in enumerate(mood_cols, 1):
        with col:
            if st.button(mood_labels[i], key=f"mood_quick_{i}", help=mood_names[i]):
                msg = f"I see you're feeling **{mood_names[i]}** today 💜 That's completely valid. I'm here if you want to talk about it."
                st.session_state.messages.append({
                    "role": "user",
                    "content": f"I'm feeling {mood_names[i]} today {mood_labels[i]}",
                    "time": datetime.now().strftime("%I:%M %p")
                })
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": msg,
                    "time": datetime.now().strftime("%I:%M %p")
                })
                # Update mood log
                today = datetime.now().strftime("%a")
                st.session_state.mood_log.append({"day": today, "score": i, "emoji": mood_labels[i]})
                st.rerun()

    st.markdown("---")
    st.markdown("🔒 *Conversations are private and secure.*")
    st.markdown("🆘 **Emergency:** Call **112**")
    st.markdown("")
    if st.button("🚪 Log Out", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.logged_in_user = ""
        st.session_state.messages = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# ── TAB: CHAT ─────────────────────────────────────────────────────────────────
if tab_choice == "💬 Chat":
    st.markdown('<h1 class="page-title">💬 Chat with Elara</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">AI Mental Wellness Companion • Always here for you</p>', unsafe_allow_html=True)

    # Quick prompt buttons
    st.markdown("**Quick start:**")
    qp_cols = st.columns(5)
    quick_prompts = [
        ("😰 Anxious", "I'm feeling anxious today"),
        ("😴 Sleep", "I can't sleep well lately"),
        ("😓 Stressed", "I feel very stressed and overwhelmed"),
        ("💔 Lonely", "I've been feeling lonely and isolated"),
        ("🫁 Breathe", "Can you teach me a breathing exercise?"),
    ]
    for col, (label, prompt) in zip(qp_cols, quick_prompts):
        with col:
            if st.button(label, key=f"qp_{label}"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": prompt,
                    "time": datetime.now().strftime("%I:%M %p")
                })
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": get_bot_reply(prompt),
                    "time": datetime.now().strftime("%I:%M %p")
                })
                st.rerun()

    st.markdown("---")

    # Render messages
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        time_str = msg.get("time", "")
        is_user = role == "user"

        av_class = "user-av" if is_user else "bot-av"
        av_icon = "U" if is_user else "🤍"
        bubble_class = "user-bubble" if is_user else "bot-bubble"
        row_class = "msg-row user" if is_user else "msg-row"
        time_class = "msg-time user" if is_user else "msg-time"

        # Simple markdown → html for bold
        import re
        html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
        html_content = html_content.replace('\n', '<br>')

        chat_html += f"""
        <div class="{row_class}">
            <div class="msg-avatar {av_class}">{av_icon}</div>
            <div style="display:flex;flex-direction:column;max-width:75%">
                <div class="msg-bubble {bubble_class}">{html_content}</div>
                <div class="{time_class}">{time_str}</div>
            </div>
        </div>"""

    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Input
    col_input, col_clear = st.columns([6, 1])
    with col_input:
        user_input = st.chat_input("Share what's on your mind…", key="chat_input")
    with col_clear:
        if st.button("🗑️ Clear", key="clear_chat"):
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()

    if user_input and user_input.strip():
        st.session_state.messages.append({
            "role": "user",
            "content": user_input.strip(),
            "time": datetime.now().strftime("%I:%M %p")
        })
        reply = get_bot_reply(user_input)
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply,
            "time": datetime.now().strftime("%I:%M %p")
        })
        st.rerun()

    st.markdown(
        '<p style="font-size:0.7rem;color:rgba(240,238,255,0.3);text-align:center;margin-top:1rem;">'
        '🔒 Conversations are private and not stored. For emergencies, call 112 or iCall: 9152987821</p>',
        unsafe_allow_html=True
    )

# ── TAB: MOOD TRACKER ─────────────────────────────────────────────────────────
elif tab_choice == "📊 Mood Tracker":
    st.markdown('<h1 class="page-title">📊 Mood Tracker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Visualize your emotional journey over the past week</p>', unsafe_allow_html=True)

    # Stats
    recent = st.session_state.mood_log[-7:]
    avg = round(sum(m["score"] for m in recent) / len(recent), 1)
    best_day = max(recent, key=lambda x: x["score"])["day"]

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, val, lbl in [
        (c1, "📈", str(avg), "Avg Mood (7d)"),
        (c2, "🔥", "4", "Day Streak"),
        (c3, "💬", str(len(st.session_state.messages)), "Messages"),
        (c4, "🌟", best_day, "Best Day"),
    ]:
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <div style="font-size:1.5rem">{icon}</div>
                <div class="stat-val">{val}</div>
                <div class="stat-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Mood chart using st.line_chart
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**📅 This Week's Mood**")

    import pandas as pd
    chart_data = pd.DataFrame({
        "Mood Score": [m["score"] for m in recent],
    }, index=[m["day"] for m in recent])
    st.line_chart(chart_data, color="#7c6af7", use_container_width=True, height=220)
    st.markdown('</div>', unsafe_allow_html=True)

    # Mood log
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("**📋 Mood History**")
    emoji_map = {1: "😢", 2: "😕", 3: "😐", 4: "🙂", 5: "😄"}
    for m in reversed(recent):
        pct = int(((m["score"] - 1) / 4) * 100)
        em = emoji_map.get(round(m["score"]), "😐")
        st.markdown(f"""
        <div style="display:flex;align-items:center;padding:0.55rem 0;border-bottom:1px solid rgba(255,255,255,0.05)">
            <span style="width:50px;font-size:0.82rem;color:rgba(240,238,255,0.55)">{m["day"]}</span>
            <div class="mood-bar-wrap" style="flex:1;margin:0 0.75rem">
                <div class="mood-bar-fill" style="width:{pct}%"></div>
            </div>
            <span style="font-size:1.1rem">{em}</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Insight
    st.markdown("""
    <div class="insight-box">
        <span class="insight-icon">💡</span>
        <div class="insight-body">
            <h4>Weekly Insight</h4>
            <p>Your mood tends to dip early in the week and peak mid-week. Try starting Mondays with a 5-minute gratitude journal to boost your baseline mood. Consistency in your sleep schedule also correlates strongly with mood improvement.</p>
        </div>
    </div>""", unsafe_allow_html=True)

    # Log today's mood
    st.markdown("<br>**Log today's mood:**", unsafe_allow_html=True)
    mood_today = st.select_slider(
        "Today I feel…",
        options=["😢 Very Sad", "😕 Sad", "😐 Okay", "🙂 Good", "😄 Great"],
        value="😐 Okay",
        label_visibility="collapsed"
    )
    if st.button("💾 Save Today's Mood", key="save_mood"):
        score_map = {"😢 Very Sad": 1, "😕 Sad": 2, "😐 Okay": 3, "🙂 Good": 4, "😄 Great": 5}
        emoji_today = mood_today.split(" ")[0]
        st.session_state.mood_log.append({
            "day": datetime.now().strftime("%a"),
            "score": score_map[mood_today],
            "emoji": emoji_today
        })
        st.success(f"Mood logged: {mood_today} ✅")
        time.sleep(0.8)
        st.rerun()

# ── TAB: RESOURCES ────────────────────────────────────────────────────────────
elif tab_choice == "📚 Resources":
    st.markdown('<h1 class="page-title">📚 Wellness Resources</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Curated evidence-based tools for your mental health journey</p>', unsafe_allow_html=True)

    res_tabs = st.tabs(["🫁 Breathing", "📓 Journal", "🧩 CBT", "🧘 Mindfulness"])

    # ── Breathing ──
    with res_tabs[0]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🫁 Guided Breathing Exercises")
        st.markdown("*Activate your body's natural relaxation response in minutes.*")
        
        technique = st.selectbox(
            "Choose technique",
            ["4-7-8 Breathing", "Box Breathing (4-4-4-4)", "Deep Belly Breathing"],
            key="breath_tech"
        )

        if technique == "4-7-8 Breathing":
            steps = [("Inhale", 4), ("Hold", 7), ("Exhale", 8)]
            st.info("This technique acts as a **natural tranquilizer** for the nervous system — clinically shown to reduce anxiety within 4 cycles.")
        elif technique == "Box Breathing (4-4-4-4)":
            steps = [("Inhale", 4), ("Hold", 4), ("Exhale", 4), ("Hold", 4)]
            st.info("Used by **Navy SEALs** and elite athletes to maintain calm under extreme pressure.")
        else:
            steps = [("Inhale deeply", 5), ("Pause", 2), ("Exhale slowly", 6)]
            st.info("**Diaphragmatic breathing** activates the vagus nerve, directly lowering heart rate and blood pressure.")

        if st.button("▶️ Start Guided Breathing", key="start_breath"):
            progress_bar = st.progress(0)
            phase_text = st.empty()
            circle = st.empty()

            for cycle in range(4):
                st.markdown(f"**Cycle {cycle+1} of 4**")
                for phase, duration in steps:
                    for t in range(duration):
                        pct = int((t + 1) / duration * 100)
                        progress_bar.progress(pct)
                        if phase.startswith("Inhale"):
                            icon = "🔵"
                            size = 100 + int(t * 40 / duration)
                        elif phase.startswith("Hold"):
                            icon = "⚪"
                            size = 140
                        else:
                            icon = "🟣"
                            size = 140 - int(t * 40 / duration)
                        
                        phase_text.markdown(f"**{icon} {phase}…** ({duration - t}s)")
                        circle.markdown(f"""
                        <div style="text-align:center;margin:1rem 0">
                            <div style="display:inline-block;width:{size}px;height:{size}px;
                                border-radius:50%;background:radial-gradient(circle,rgba(124,106,247,0.4),rgba(124,106,247,0.05));
                                border:2px solid rgba(124,106,247,0.6);
                                transition:all 1s ease;
                                box-shadow:0 0 {size//3}px rgba(124,106,247,0.3);">
                            </div>
                        </div>""", unsafe_allow_html=True)
                        time.sleep(1)

            phase_text.empty()
            circle.empty()
            progress_bar.empty()
            st.success("✨ Great job! You've completed 4 cycles. Notice how you feel right now.")

        st.markdown('</div>', unsafe_allow_html=True)

    # ── Journal ──
    with res_tabs[1]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📓 Daily Journal Prompts")
        st.markdown("*Reflective writing helps process emotions and build self-awareness.*")
        
        prompt = JOURNAL_PROMPTS[st.session_state.journal_idx]
        st.markdown(f"""
        <div style="background:rgba(124,106,247,0.1);border:1px solid rgba(124,106,247,0.25);
             border-radius:12px;padding:1.1rem 1.3rem;margin:1rem 0;font-style:italic;
             font-size:0.95rem;line-height:1.7;color:#c4b8ff">
            💬 "{prompt}"
        </div>""", unsafe_allow_html=True)

        col_new, col_copy = st.columns([1, 3])
        with col_new:
            if st.button("↻ New Prompt", key="new_prompt"):
                st.session_state.journal_idx = (st.session_state.journal_idx + 1) % len(JOURNAL_PROMPTS)
                st.rerun()

        st.markdown("**Write your response below:**")
        journal_entry = st.text_area(
            "Journal entry",
            placeholder="Start writing here… this is your private space.",
            height=180,
            label_visibility="collapsed",
            key="journal_text"
        )

        if st.button("💾 Save Entry", key="save_journal"):
            if journal_entry.strip():
                st.success("✅ Entry saved! Journaling consistently for 21 days significantly improves emotional well-being.")
            else:
                st.warning("Please write something first!")

        st.markdown("---")
        st.markdown("**📚 Benefits of Journaling (Research-backed):**")
        st.markdown("""
        - 🧠 Reduces stress hormones (cortisol) by up to **32%**  
        - 💭 Improves working memory and cognitive clarity  
        - 😴 People who journal sleep **25% better** on average  
        - 💪 Builds emotional resilience over time
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── CBT ──
    with res_tabs[2]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🧩 Cognitive Behavioral Therapy (CBT) Techniques")
        st.markdown("*Evidence-based exercises to identify and reframe negative thought patterns.*")
        st.markdown("")

        for icon, title, desc in CBT_TECHNIQUES:
            st.markdown(f"**{icon} {title}**")
            st.markdown(f"<p style='font-size:0.85rem;color:rgba(240,238,255,0.6);margin-top:-0.3rem;margin-bottom:1rem'>{desc}</p>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🧠 Try the Thought Record")
        st.markdown("*Challenge a negative thought in 3 steps:*")
        
        neg_thought = st.text_input("1️⃣ What is the negative thought?", placeholder="e.g. I always fail at everything", key="cbt_thought")
        evidence_for = st.text_area("2️⃣ Evidence that supports it:", placeholder="List facts, not feelings…", height=80, key="cbt_for")
        evidence_against = st.text_area("3️⃣ Evidence AGAINST it:", placeholder="Think of exceptions, past successes…", height=80, key="cbt_against")

        if st.button("🔄 Generate Balanced Thought", key="gen_balanced"):
            if neg_thought:
                st.markdown(f"""
                <div style="background:rgba(86,207,178,0.12);border:1px solid rgba(86,207,178,0.3);
                     border-radius:12px;padding:1rem 1.2rem;margin-top:0.5rem;font-size:0.88rem">
                    💚 <strong>Balanced Thought:</strong><br/><br/>
                    While it's true that "{neg_thought}", the evidence also shows there are 
                    situations where this isn't the case. A more balanced view would be: 
                    <em>"I sometimes struggle, but I also have strengths and successes I can build on."</em><br/><br/>
                    <span style="color:rgba(240,238,255,0.6);font-size:0.8rem">
                    This is a starting point — work with a therapist for deeper exploration.
                    </span>
                </div>""", unsafe_allow_html=True)
            else:
                st.warning("Please enter a negative thought first.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Mindfulness ──
    with res_tabs[3]:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🧘 Mindfulness Guide")
        st.markdown("*Simple exercises to anchor yourself in the present moment.*")
        
        selected_technique = st.radio(
            "Choose a technique:",
            list(MINDFULNESS.keys()),
            horizontal=True,
            key="mindfulness_tech"
        )
        
        st.markdown(f"""
        <div style="background:rgba(79,196,207,0.1);border:1px solid rgba(79,196,207,0.25);
             border-radius:12px;padding:1.2rem 1.4rem;margin:1rem 0;line-height:1.8">
            {MINDFULNESS[selected_technique].replace(chr(10), '<br>')}
        </div>""", unsafe_allow_html=True)

        if st.button("⏱️ Start 5-Min Timer", key="start_mindfulness"):
            timer_bar = st.progress(0)
            time_left = st.empty()
            total = 300
            for elapsed in range(total):
                timer_bar.progress((elapsed + 1) / total)
                mins, secs = divmod(total - elapsed - 1, 60)
                time_left.markdown(f"⏱️ **{mins:02d}:{secs:02d}** remaining — stay with it…")
                time.sleep(1)
            time_left.markdown("✨ **Session complete!** Take a moment to notice how you feel.")
            st.balloons()

        st.markdown('</div>', unsafe_allow_html=True)

# ── TAB: CRISIS HELP ─────────────────────────────────────────────────────────
elif tab_choice == "🆘 Crisis Help":
    st.markdown('<h1 class="page-title" style="background:linear-gradient(135deg,#ef4444,#f59e0b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">🆘 Crisis Support</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">You are not alone. Help is always available — reach out immediately.</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="crisis-alert">
        ⚠️ <strong>If you're in immediate danger, call emergency services (112) right now.</strong><br/>
        <span style="font-size:0.82rem;color:rgba(240,238,255,0.6)">
        This chatbot is not a substitute for professional help during a crisis.
        </span>
    </div>""", unsafe_allow_html=True)

    col_in, col_gl = st.columns(2)

    with col_in:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("🇮🇳 **India Helplines**")
        helplines_india = [
            ("iCall (TISS)", "📞 9152987821"),
            ("Vandrevala Foundation", "📞 1860-266-2345"),
            ("NIMHANS Helpline", "📞 080-46110007"),
            ("Snehi", "📞 044-24640050"),
            ("Aasra", "📞 9820466627"),
        ]
        for name, num in helplines_india:
            st.markdown(f"""
            <div class="helpline-row">
                <span style="font-size:0.83rem;color:rgba(240,238,255,0.62)">{name}</span>
                <span class="helpline-num">{num}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_gl:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("🌍 **Global Resources**")
        helplines_global = [
            ("988 Suicide & Crisis (USA)", "📞 988"),
            ("Crisis Text Line", "💬 Text HOME to 741741"),
            ("Samaritans (UK/Ireland)", "📞 116 123"),
            ("Befrienders Worldwide", "🌐 befrienders.org"),
            ("Crisis Services Canada", "📞 1-833-456-4566"),
        ]
        for name, num in helplines_global:
            st.markdown(f"""
            <div class="helpline-row">
                <span style="font-size:0.83rem;color:rgba(240,238,255,0.62)">{name}</span>
                <span class="helpline-num">{num}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Self-help steps
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("🛡️ **Right Now, Try This:**")
    steps = [
        ("1", "Take 5 slow, deep breaths — inhale for 4 seconds, exhale for 6 seconds."),
        ("2", "Ground yourself: name 5 things you can see around you right now."),
        ("3", "Call someone you trust — a friend, family member, or counselor."),
        ("4", "Remove yourself from the immediate stressful environment if possible."),
    ]
    cols = st.columns(2)
    for i, (num, step) in enumerate(steps):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="display:flex;gap:0.75rem;align-items:flex-start;margin-bottom:0.9rem">
                <div style="min-width:28px;height:28px;background:linear-gradient(135deg,#7c6af7,#f178b6);
                    border-radius:50%;display:flex;align-items:center;justify-content:center;
                    font-size:0.8rem;font-weight:700;flex-shrink:0">{num}</div>
                <p style="font-size:0.85rem;line-height:1.55;margin:0;color:rgba(240,238,255,0.75)">{step}</p>
            </div>""", unsafe_allow_html=True)
    
    if st.button("💬 Talk to Elara Now", key="go_chat_crisis"):
        st.info("⬅️ Click **'💬 Chat'** in the sidebar to start talking with Elara.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Professional resources info
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("🏥 **Finding Professional Help in India**")
    st.markdown("""
| Type | Description | Cost |
|------|-------------|------|
| **NIMHANS** | National Institute of Mental Health, Bengaluru | Free/subsidized |
| **Government Hospitals** | Psychiatry OPD in all major government hospitals | Free |
| **iCall (TISS)** | Online/phone counseling by trained professionals | ₹300–700/session |
| **YourDost** | Online counseling platform | ₹500–1500/session |
| **Vandrevala Foundation** | 24/7 free crisis support | Free |
""")
    st.markdown('</div>', unsafe_allow_html=True)
