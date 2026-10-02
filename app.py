import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database import (
    create_database,
    create_user,
    verify_user,
    reset_password
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Skill Gap & Career Intelligence Agent",
    page_icon="🤖",
    layout="wide"
)



# =========================================================
# PREMIUM WARM EDITORIAL UI
# =========================================================

st.markdown("""
<style>
    :root {
        --bg: #F5F2ED;
        --surface: #FFFCF8;
        --wine: #6B2737;
        --wine-dark: #4A1824;
        --text: #242323;
        --muted: #77716C;
        --border: #E3DDD5;
    }
    .stApp {
        background: radial-gradient(circle at 8% 5%, rgba(107,39,55,.055), transparent 28%),
                    radial-gradient(circle at 92% 18%, rgba(107,39,55,.035), transparent 25%),
                    var(--bg);
        color: var(--text);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: #EFEAE4;
        border-right: 1px solid var(--border);
    }
    .block-container { max-width: 1180px; padding-top: 2.5rem; padding-bottom: 4rem; }
    h1, h2, h3 { color: var(--text) !important; letter-spacing: -0.02em; }
    .hero-title { font-size: 3rem; font-weight: 750; line-height: 1.05; margin-bottom: .65rem; }
    .hero-subtitle { color: var(--muted); font-size: 1.08rem; margin-bottom: 2rem; }
    .career-hero {
        background: var(--surface);
        border: 1px solid var(--border);
        border-top: 4px solid var(--wine);
        border-radius: 20px;
        padding: 2rem 2.2rem;
        margin: 1rem 0 2rem;
        box-shadow: 0 16px 40px rgba(58,39,28,.07);
    }
    .eyebrow { color: var(--wine); font-size: .76rem; font-weight: 800; letter-spacing: .13em; text-transform: uppercase; }
    .career-heading { font-size: 1.8rem; font-weight: 750; margin: .35rem 0 .25rem; }
    .career-copy { color: var(--muted); margin-bottom: 1rem; }
    .selected-career {
        display: inline-block; padding: .45rem .8rem; border-radius: 999px;
        background: #F3E6E9; color: var(--wine-dark); font-weight: 700; font-size: .86rem;
        margin-top: .75rem;
    }
    .section-card {
        background: rgba(255,252,248,.88); border: 1px solid var(--border);
        border-radius: 16px; padding: 1.25rem 1.35rem; margin: .9rem 0;
        box-shadow: 0 8px 24px rgba(58,39,28,.045);
    }
    .step-label { color: var(--wine); font-weight: 800; font-size: .76rem; letter-spacing: .1em; text-transform: uppercase; }
    .muted { color: var(--muted); }
    div[data-baseweb="select"] > div { border-color: var(--border) !important; border-radius: 12px !important; background: var(--surface) !important; }
    .stButton > button, .stDownloadButton > button {
        border-radius: 10px; border: 1px solid var(--wine); background: var(--wine); color: white;
        font-weight: 700; padding: .65rem 1rem;
    }
    .stButton > button:hover, .stDownloadButton > button:hover { background: var(--wine-dark); border-color: var(--wine-dark); color: white; }
    .stFileUploader { background: var(--surface); border: 1px dashed #CFC5BC; border-radius: 14px; padding: .4rem; }
    .metric-card { background: var(--surface); border: 1px solid var(--border); border-radius: 14px; padding: 1rem; }
    .skill-chip { display:inline-block; background:#F1ECE6; border:1px solid var(--border); color:var(--text); padding:.38rem .65rem; border-radius:999px; margin:.2rem .18rem; font-size:.86rem; }
    hr { border: 0; border-top: 1px solid var(--border); margin: 2rem 0; }
    .section-card { position: relative; overflow: hidden; }
    .section-card::before { content: ""; position:absolute; left:0; top:0; bottom:0; width:3px; background:var(--wine); opacity:.7; }
    .insight-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin:14px 0 22px; }
    .insight-card { background:var(--surface); border:1px solid var(--border); border-radius:15px; padding:18px; box-shadow:0 7px 20px rgba(58,39,28,.04); }
    .insight-label { color:var(--muted); font-size:.74rem; font-weight:800; text-transform:uppercase; letter-spacing:.1em; }
    .insight-value { color:var(--text); font-size:1.55rem; font-weight:800; margin-top:5px; }
    .insight-note { color:var(--muted); font-size:.82rem; margin-top:4px; }
    .gap-card { background:var(--surface); border:1px solid var(--border); border-radius:15px; padding:17px 18px; margin:10px 0; box-shadow:0 6px 18px rgba(58,39,28,.035); }
    .gap-number { display:inline-flex; width:30px; height:30px; align-items:center; justify-content:center; border-radius:50%; background:#F3E6E9; color:var(--wine-dark); font-weight:800; margin-right:10px; }
    .roadmap-card { background:var(--surface); border:1px solid var(--border); border-radius:17px; padding:19px 20px; margin:12px 0; box-shadow:0 8px 24px rgba(58,39,28,.045); }
    .roadmap-top { display:flex; align-items:center; gap:12px; }
    .roadmap-index { min-width:38px; height:38px; border-radius:12px; background:#F3E6E9; color:var(--wine-dark); display:flex; align-items:center; justify-content:center; font-weight:800; }
    .roadmap-title { font-size:1.02rem; font-weight:800; color:var(--text); }
    .roadmap-flow { color:var(--muted); font-size:.88rem; margin-top:9px; line-height:1.6; }
    .practice-card { background:var(--surface); border:1px solid var(--border); border-radius:17px; padding:20px; min-height:150px; box-shadow:0 8px 24px rgba(58,39,28,.045); }
    .practice-icon { font-size:1.45rem; margin-bottom:8px; }
    .practice-title { font-weight:800; font-size:1.05rem; }
    .practice-copy { color:var(--muted); font-size:.88rem; line-height:1.55; margin:7px 0 14px; }
    .role-card { background:var(--surface); border:1px solid var(--border); border-radius:13px; padding:13px 15px; margin:7px 0; font-weight:700; }
    .career-skill-list { background:var(--surface); border:1px solid var(--border); border-radius:15px; padding:17px 19px; line-height:2; }
    .report-card { background:var(--surface); border:1px solid var(--border); border-radius:17px; padding:20px; box-shadow:0 8px 24px rgba(58,39,28,.045); }
    .upload-card { background:var(--surface); border:1px solid var(--border); border-radius:17px; padding:18px 20px; margin:10px 0 18px; }
    @media (max-width: 800px) { .insight-grid { grid-template-columns:1fr; } .hero-title { font-size:2.2rem; } }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE
# =========================================================

create_database()


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""


# =========================================================
# LOGIN / SIGNUP / FORGOT PASSWORD
# =========================================================

if not st.session_state.logged_in:

    st.title("🤖 AI Skill Gap & Career Intelligence Agent")

    st.caption(
        "Your personalized career intelligence platform"
    )

    login_tab, signup_tab, forgot_tab = st.tabs(
        [
            "🔐 Login",
            "👤 Create Account",
            "🔑 Forgot Password"
        ]
    )


    # =====================================================
    # LOGIN
    # =====================================================

    with login_tab:

        st.subheader("Welcome Back")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Please enter your email and password."
                )

            else:

                user_name = verify_user(
                    email,
                    password
                )

                if user_name:

                    st.session_state.logged_in = True
                    st.session_state.user_name = user_name

                    st.success(
                        f"Welcome back, {user_name}! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid email or password."
                    )


    # =====================================================
    # CREATE ACCOUNT
    # =====================================================

    with signup_tab:

        st.subheader("Create Your Account")

        name = st.text_input(
            "Full Name",
            key="signup_name"
        )

        new_email = st.text_input(
            "Email",
            key="signup_email"
        )

        new_password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm"
        )

        if st.button(
            "✨ Create Account",
            use_container_width=True
        ):

            if not name or not new_email or not new_password:

                st.warning(
                    "Please fill in all fields."
                )

            elif new_password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            elif len(new_password) < 6:

                st.warning(
                    "Password must contain at least 6 characters."
                )

            else:

                created = create_user(
                    name,
                    new_email,
                    new_password
                )

                if created:

                    st.success(
                        "🎉 Account created successfully!"
                    )

                    st.info(
                        "Go to the Login tab to sign in."
                    )

                else:

                    st.error(
                        "❌ An account with this email already exists."
                    )


    # =====================================================
    # FORGOT PASSWORD
    # =====================================================

    with forgot_tab:

        st.subheader("🔑 Reset Your Password")

        st.write(
            "Enter your registered email and create a new password."
        )

        reset_email = st.text_input(
            "Registered Email",
            key="reset_email"
        )

        new_reset_password = st.text_input(
            "New Password",
            type="password",
            key="new_reset_password"
        )

        confirm_reset_password = st.text_input(
            "Confirm New Password",
            type="password",
            key="confirm_reset_password"
        )

        if st.button(
            "🔄 Reset Password",
            use_container_width=True
        ):

            if (
                not reset_email
                or not new_reset_password
                or not confirm_reset_password
            ):

                st.warning(
                    "Please fill in all fields."
                )

            elif new_reset_password != confirm_reset_password:

                st.error(
                    "❌ Passwords do not match."
                )

            elif len(new_reset_password) < 6:

                st.warning(
                    "Password must contain at least 6 characters."
                )

            else:

                changed = reset_password(
                    reset_email,
                    new_reset_password
                )

                if changed:

                    st.success(
                        "✅ Password changed successfully!"
                    )

                    st.info(
                        "You can now log in with your new password."
                    )

                else:

                    st.error(
                        "❌ No account was found with that email."
                    )


    st.stop()


# =========================================================
# LOGGED-IN USER
# =========================================================

st.sidebar.success(
    f"👋 Welcome, {st.session_state.user_name}"
)


if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False
    st.session_state.user_name = ""

    st.rerun()


# =========================================================
# APPLICATION HEADER
# =========================================================

st.markdown(
    """
    <h1 style="text-align:center;">
        🤖 AI Skill Gap & Career Intelligence Agent
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="text-align:center;">
        Analyze your skills • Find your gaps • Build your career roadmap
    </p>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CAREER DATABASE
# =========================================================

career_data = {

    "AI Engineer": {

        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "AI",
            "NLP",
            "TensorFlow",
            "PyTorch",
            "NumPy",
            "Pandas",
            "SQL",
            "Git",
            "GitHub"
        ],

        "roles": [
            "AI Engineer",
            "Machine Learning Engineer",
            "NLP Engineer",
            "AI Developer"
        ]
    },

    "Data Scientist": {

        "skills": [
            "Python",
            "SQL",
            "Statistics",
            "Machine Learning",
            "Data Science",
            "Pandas",
            "NumPy",
            "Data Visualization",
            "Power BI",
            "Git"
        ],

        "roles": [
            "Data Scientist",
            "Data Science Intern",
            "Junior Data Scientist",
            "Business Intelligence Analyst"
        ]
    },

    "Data Analyst": {

        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Power BI",
            "Tableau",
            "Statistics",
            "Data Visualization",
            "Pandas",
            "Communication"
        ],

        "roles": [
            "Data Analyst",
            "Business Analyst",
            "BI Analyst",
            "Reporting Analyst"
        ]
    },

    "Machine Learning Engineer": {

        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "SQL",
            "NumPy",
            "Pandas",
            "Git",
            "GitHub"
        ],

        "roles": [
            "Machine Learning Engineer",
            "ML Engineer",
            "AI Engineer",
            "ML Intern"
        ]
    }
}


# =========================================================
# SKILL DATABASE
# =========================================================

all_skills = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Excel",
    "Machine Learning",
    "Deep Learning",
    "AI",
    "Data Science",
    "Statistics",
    "Pandas",
    "NumPy",
    "Power BI",
    "Tableau",
    "Data Visualization",
    "TensorFlow",
    "PyTorch",
    "NLP",
    "Git",
    "GitHub",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "MongoDB",
    "Communication",
    "Leadership"
]


# =========================================================
# FUNCTIONS
# =========================================================

def extract_text_from_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + " "

    return text


def extract_skills(text):

    text_lower = text.lower()

    detected = []

    for skill in all_skills:

        if skill.lower() in text_lower:
            detected.append(skill)

    return detected


def calculate_match(user_skills, career_skills):

    if not user_skills:
        return 0

    user_text = " ".join(user_skills)
    career_text = " ".join(career_skills)

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [
            user_text,
            career_text
        ]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(
        similarity * 100,
        2
    )


def generate_roadmap(missing_skills):

    roadmap = []

    for skill in missing_skills:

        roadmap.append(
            f"Learn {skill} → Practice → Build a mini project → Add it to your resume"
        )

    return roadmap


# =========================================================
# CAREER DATABASE
# =========================================================

career_data = {

    "AI Engineer": {

        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "AI",
            "NLP",
            "TensorFlow",
            "PyTorch",
            "NumPy",
            "Pandas",
            "SQL",
            "Git",
            "GitHub"
        ],

        "roles": [
            "AI Engineer",
            "Machine Learning Engineer",
            "NLP Engineer",
            "AI Developer"
        ]
    },

    "Data Scientist": {

        "skills": [
            "Python",
            "SQL",
            "Statistics",
            "Machine Learning",
            "Data Science",
            "Pandas",
            "NumPy",
            "Data Visualization",
            "Power BI",
            "Git"
        ],

        "roles": [
            "Data Scientist",
            "Data Science Intern",
            "Junior Data Scientist",
            "Business Intelligence Analyst"
        ]
    },

    "Data Analyst": {

        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Power BI",
            "Tableau",
            "Statistics",
            "Data Visualization",
            "Pandas",
            "Communication"
        ],

        "roles": [
            "Data Analyst",
            "Business Analyst",
            "BI Analyst",
            "Reporting Analyst"
        ]
    },

    "Machine Learning Engineer": {

        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "SQL",
            "NumPy",
            "Pandas",
            "Git",
            "GitHub"
        ],

        "roles": [
            "Machine Learning Engineer",
            "ML Engineer",
            "AI Engineer",
            "ML Intern"
        ]
    }
}


# =========================================================
# SKILL DATABASE
# =========================================================

all_skills = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Excel",
    "Machine Learning",
    "Deep Learning",
    "AI",
    "Data Science",
    "Statistics",
    "Pandas",
    "NumPy",
    "Power BI",
    "Tableau",
    "Data Visualization",
    "TensorFlow",
    "PyTorch",
    "NLP",
    "Git",
    "GitHub",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "MongoDB",
    "Communication",
    "Leadership"
]


# =========================================================
# FUNCTIONS
# =========================================================

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text


def extract_skills(text):
    text_lower = text.lower()
    detected = []
    for skill in all_skills:
        if skill.lower() in text_lower:
            detected.append(skill)
    return detected


def calculate_match(user_skills, career_skills):
    if not user_skills:
        return 0
    user_text = " ".join(user_skills)
    career_text = " ".join(career_skills)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([user_text, career_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(similarity * 100, 2)


def generate_roadmap(missing_skills):
    return [f"Learn {skill} → Practice → Build a mini project → Add it to your resume" for skill in missing_skills]


def resume_context_questions(target_career, detected_skills, resume_text, mode):
    skills = detected_skills[:]
    lower = resume_text.lower()
    questions = []

    if skills:
        primary = skills[:3]
        if mode == "assessment":
            questions.extend([
                f"Your resume lists {', '.join(primary)}. Explain how you would use these skills in a {target_career} workflow.",
                f"Choose one project or experience from your resume involving {primary[0]}. What was your approach, and what result did you achieve?",
                f"If you had to improve a project on your resume using {primary[-1]}, what would you change and why?"
            ])
        else:
            questions.extend([
                f"Walk me through the project or experience on your resume where you used {primary[0]}. What problem were you solving?",
                f"Your resume mentions {', '.join(primary)}. Why did you choose those technologies or methods for your work?",
                f"Tell me about a technical challenge you faced in your resume projects and how you solved it."
            ])

    project_terms = [
        "project", "internship", "experience", "developed", "built", "created", "implemented", "model", "dashboard", "application"
    ]
    if any(term in lower for term in project_terms):
        if mode == "assessment":
            questions.append(f"Based on the projects described in your resume, what would you measure to decide whether the solution was successful?")
        else:
            questions.append(f"Pick one project from your resume and explain one design or technical decision you would defend in a {target_career} interview.")

    questions.append(f"For the {target_career} role you selected, which skill from your resume is your strongest and how have you demonstrated it?")
    return questions[:5]


# =========================================================
# PREMIUM CAREER-FIRST DASHBOARD
# =========================================================

st.markdown('<div class="hero-title">AI Skill Gap & Career Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Choose your destination first. Your resume analysis, skill gap, roadmap, assessment and interview will follow that career.</div>', unsafe_allow_html=True)

st.markdown('''
<div class="career-hero">
    <div class="eyebrow">01 · Your Career Destination</div>
    <div class="career-heading">Choose Your Target Career</div>
    <div class="career-copy">This is the main decision that personalizes every part of your career intelligence dashboard.</div>
</div>
''', unsafe_allow_html=True)

target_career = st.selectbox(
    "Select the career you want to prepare for",
    list(career_data.keys()),
    key="target_career_main"
)

st.markdown(f'<div class="selected-career">TARGET CAREER · {target_career}</div>', unsafe_allow_html=True)
st.caption("Your skill gap, learning roadmap, assessment and mock interview are personalized to this selection.")

st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================
# RESUME UPLOAD
# =========================================================

st.markdown('<div class="step-label">02 · Resume Analysis</div>', unsafe_allow_html=True)
st.subheader("Build your profile")
st.markdown('''
<div class="upload-card">
    <b>Upload your resume to begin the analysis</b><br>
    <span class="muted">We compare the skills found in your PDF with the requirements of your selected career.</span>
</div>
''', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Resume PDF", type=["pdf"], label_visibility="collapsed")

if uploaded_file is None:
    st.info("Upload your resume to unlock your personalized career analysis.")
    st.stop()

text = extract_text_from_pdf(uploaded_file)

if not text.strip():
    st.error("Unable to extract text from this PDF.")
    st.stop()

# =========================================================
# PROFILE SNAPSHOT
# =========================================================

detected_skills = extract_skills(text)

st.markdown('<div class="step-label">03 · Profile Snapshot</div>', unsafe_allow_html=True)
st.subheader("What we found in your resume")

st.markdown(
    f'''<div class="insight-grid">
        <div class="insight-card"><div class="insight-label">Detected Skills</div><div class="insight-value">{len(detected_skills)}</div><div class="insight-note">Skills identified from your resume</div></div>
        <div class="insight-card"><div class="insight-label">Target Career</div><div class="insight-value" style="font-size:1.15rem">{target_career}</div><div class="insight-note">Your selected destination</div></div>
        <div class="insight-card"><div class="insight-label">Required Skills</div><div class="insight-value">{len(career_data[target_career]["skills"])}</div><div class="insight-note">Skills used for the comparison</div></div>
    </div>''', unsafe_allow_html=True
)

if detected_skills:
    st.markdown("".join(f'<span class="skill-chip">✓ {skill}</span>' for skill in detected_skills), unsafe_allow_html=True)
else:
    st.warning("No predefined skills were detected in the uploaded resume.")

# =========================================================
# SKILL SELF-RATING
# =========================================================

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="step-label">Your Self-Assessment</div>', unsafe_allow_html=True)
st.subheader("Rate your detected skills")
st.caption("Your ratings add personal context to the resume-derived profile.")
skill_levels = {}

if detected_skills:
    cols = st.columns(2)
    for index, skill in enumerate(detected_skills):
        with cols[index % 2]:
            skill_levels[skill] = st.select_slider(
                f"{skill}", options=["Beginner", "Intermediate", "Advanced"], value="Beginner", key=f"skill_level_{skill}"
            )
else:
    st.caption("Skill ratings will appear once skills are detected.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# CAREER MATCH
# =========================================================

required_skills = career_data[target_career]["skills"]
match_percentage = calculate_match(detected_skills, required_skills)

st.markdown('<div class="step-label">04 · Career Fit</div>', unsafe_allow_html=True)
st.subheader(f"Your match for {target_career}")

m1, m2 = st.columns([1, 2])
with m1:
    st.markdown(f'''<div class="metric-card"><div class="insight-label">Career Skill Match</div><div class="insight-value">{match_percentage}%</div><div class="insight-note">Resume-to-career skill similarity</div></div>''', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.caption("Current profile alignment")
    st.progress(min(match_percentage / 100, 1.0))
    st.caption(f"Compared against {len(required_skills)} skills associated with {target_career}.")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SKILL GAP
# =========================================================

missing_skills = [skill for skill in required_skills if skill not in detected_skills]

st.markdown('<div class="step-label">05 · Skill Gap</div>', unsafe_allow_html=True)
st.subheader("What to strengthen next")

if missing_skills:
    st.caption(f"{len(missing_skills)} career skills were not detected in your resume.")
    for index, skill in enumerate(missing_skills, 1):
        st.markdown(f'''<div class="gap-card"><span class="gap-number">{index}</span><b>{skill}</b><div class="muted" style="margin:5px 0 0 42px;font-size:.86rem">Recommended focus area for your {target_career} path.</div></div>''', unsafe_allow_html=True)
else:
    st.success("All listed career skills were detected in your resume.")

# =========================================================
# LEARNING ROADMAP
# =========================================================

roadmap = generate_roadmap(missing_skills)
st.markdown('<div class="step-label">06 · Learning Roadmap</div>', unsafe_allow_html=True)
st.subheader(f"Your {target_career} learning path")
st.caption("Turn each identified gap into evidence you can demonstrate in a real project or interview.")

if roadmap:
    for index, item in enumerate(roadmap, 1):
        skill = missing_skills[index - 1]
        st.markdown(f'''<div class="roadmap-card">
            <div class="roadmap-top"><div class="roadmap-index">{index:02d}</div><div class="roadmap-title">{skill}</div></div>
            <div class="roadmap-flow"><b>Learn</b> → Understand the fundamentals &nbsp; <b>Practice</b> → Work through focused exercises &nbsp; <b>Build</b> → Create a mini project &nbsp; <b>Showcase</b> → Add the result to your resume</div>
        </div>''', unsafe_allow_html=True)
else:
    st.success("You have covered the listed skills for this target career.")

# =========================================================
# OPTIONAL ASSESSMENT / MOCK INTERVIEW
# =========================================================

st.markdown('<div class="step-label">07 · Optional Practice</div>', unsafe_allow_html=True)
st.subheader("Practice when you're ready")
st.caption("Nothing starts automatically. Choose an activity and the questions will use your resume, detected skills and selected career.")

p1, p2 = st.columns(2)
with p1:
    st.markdown('''<div class="practice-card"><div class="practice-icon">📝</div><div class="practice-title">Resume-Based Assessment</div><div class="practice-copy">Test your understanding using questions connected to the skills and experience shown in your resume.</div></div>''', unsafe_allow_html=True)
with p2:
    st.markdown('''<div class="practice-card"><div class="practice-icon">🎤</div><div class="practice-title">Resume-Based Mock Interview</div><div class="practice-copy">Practice explaining your projects, technical choices and strengths for your selected career.</div></div>''', unsafe_allow_html=True)

assessment_tab, interview_tab = st.tabs(["📝 Start Assessment", "🎤 Start Mock Interview"])

with assessment_tab:
    if st.button("Start Assessment", key="start_assessment", use_container_width=True):
        st.session_state.assessment_started = True

    if st.session_state.get("assessment_started", False):
        assessment_questions = resume_context_questions(target_career, detected_skills, text, "assessment")
        st.markdown("#### Resume-driven assessment")
        st.caption(f"{len(assessment_questions)} questions · Target: {target_career}")
        assessment_answers = []
        for index, question in enumerate(assessment_questions):
            st.markdown(f'''<div class="section-card"><b>Question {index + 1}</b><br><span class="muted">{question}</span></div>''', unsafe_allow_html=True)
            assessment_answers.append(st.text_area("Your answer", key=f"assessment_{index}", label_visibility="collapsed"))
        if st.button("Submit Assessment", key="submit_assessment", use_container_width=True):
            answered = sum(bool(a.strip()) for a in assessment_answers)
            if answered == len(assessment_answers):
                st.success("Assessment completed.")
            else:
                st.warning(f"You answered {answered} of {len(assessment_answers)} questions.")

with interview_tab:
    if st.button("Start Mock Interview", key="start_interview", use_container_width=True):
        st.session_state.interview_started = True

    if st.session_state.get("interview_started", False):
        interview_questions = resume_context_questions(target_career, detected_skills, text, "interview")
        st.markdown("#### Resume-driven mock interview")
        st.caption(f"{len(interview_questions)} questions · Target: {target_career}")
        interview_answers = {}
        for index, question in enumerate(interview_questions):
            st.markdown(f'''<div class="section-card"><b>Question {index + 1}</b><br><span class="muted">{question}</span></div>''', unsafe_allow_html=True)
            interview_answers[index] = st.text_area("Your response", key=f"interview_{index}", label_visibility="collapsed")
        if st.button("Analyze Interview", key="analyze_interview", use_container_width=True):
            answered = sum(bool(answer.strip()) for answer in interview_answers.values())
            total = len(interview_answers)
            if answered == total:
                st.success("Mock interview completed.")
            else:
                st.warning(f"You answered {answered} out of {total} questions.")

# =========================================================
# CAREER INTELLIGENCE
# =========================================================

st.markdown('<div class="step-label">08 · Career Intelligence</div>', unsafe_allow_html=True)
st.subheader(f"Your {target_career} landscape")
st.caption("Core skills and role options connected to your selected destination.")

st.markdown('<div class="career-skill-list">' + "".join(f'<span class="skill-chip">{skill}</span>' for skill in required_skills) + '</div>', unsafe_allow_html=True)

st.markdown("#### Suggested job roles")
role_cols = st.columns(2)
for index, role in enumerate(career_data[target_career]["roles"]):
    with role_cols[index % 2]:
        st.markdown(f'<div class="role-card">💼 {role}</div>', unsafe_allow_html=True)

# =========================================================
# CAREER REPORT
# =========================================================

st.markdown('<div class="step-label">09 · Export</div>', unsafe_allow_html=True)
st.subheader("Your career report")
st.markdown('''<div class="report-card"><b>Ready to export</b><br><span class="muted">Your report includes the selected career, detected skills, self-ratings, career match, skill gaps, roadmap and suggested roles.</span></div>''', unsafe_allow_html=True)

report = f"AI SKILL GAP & CAREER INTELLIGENCE AGENT\n=========================================\n\nUSER\n{st.session_state.user_name}\n\nTARGET CAREER\n{target_career}\n\nDETECTED SKILLS\n---------------\n{', '.join(detected_skills)}\n\nSELF-RATED SKILLS\n-----------------\n"

for skill, level in skill_levels.items():
    report += f"{skill}: {level}\n"

report += f"\nCAREER MATCH\n------------\n{match_percentage}%\n\nMISSING SKILLS\n--------------\n{', '.join(missing_skills)}\n\nLEARNING ROADMAP\n----------------\n"

for index, item in enumerate(roadmap, 1):
    report += f"{index}. {item}\n"

report += "\nSUGGESTED JOB ROLES\n-------------------\n"
for role in career_data[target_career]["roles"]:
    report += f"- {role}\n"

st.download_button(
    label="Download Career Report",
    data=report,
    file_name="career_intelligence_report.txt",
    mime="text/plain",
    use_container_width=True

st.markdown("""
<style>
@media (max-width: 600px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1.5rem !important;
    }

    h1 {
        font-size: 2rem !important;
        line-height: 1.15 !important;
        word-break: normal !important;
    }

    h2 {
        font-size: 1.5rem !important;
    }

    h3 {
        font-size: 1.2rem !important;
    }

    button[role="tab"] {
        font-size: 0.82rem !important;
        color: #242323 !important;
        white-space: normal !important;
        line-height: 1.2 !important;
    }

    [data-baseweb="tab-list"] {
        gap: 0.15rem !important;
    }

    [data-baseweb="input"] input {
        font-size: 16px !important;
    }

    label {
        color: #242323 !important;
    }

    .stButton > button {
        width: 100% !important;
    }
}
</style>
""")

