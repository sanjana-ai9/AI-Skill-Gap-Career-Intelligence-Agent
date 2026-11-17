import streamlit as st
import re

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
# PREMIUM UI DESIGN
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
    background: #F5F2ED;
    color: #242323;
}

[data-testid="stSidebar"] {
    background: #EFEAE4;
}

.block-container {
    max-width: 1180px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    color: #242323 !important;
}

.stButton > button,
.stDownloadButton > button,
[data-testid="stFormSubmitButton"] button {
    background: #6B2737;
    color: white;
    border: 1px solid #6B2737;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.65rem 1rem;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background: #4A1824;
    color: white;
}

.section-card,
.metric-card,
.gap-card,
.roadmap-card,
.practice-card,
.report-card {
    background: #FFFCF8;
    border: 1px solid #E3DDD5;
    border-radius: 16px;
    padding: 20px;
    margin: 12px 0;
}

.skill-chip {
    display: inline-block;
    background: #F1ECE6;
    border: 1px solid #E3DDD5;
    padding: 7px 12px;
    border-radius: 20px;
    margin: 4px;
}

.insight-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin: 15px 0;
}

.insight-card {
    background: #FFFCF8;
    border: 1px solid #E3DDD5;
    border-radius: 16px;
    padding: 20px;
}

.insight-label {
    color: #77716C;
    font-size: 12px;
    font-weight: bold;
}

.insight-value {
    font-size: 25px;
    font-weight: bold;
    margin-top: 8px;
}

.roadmap-card {
    line-height: 1.8;
}

.muted {
    color: #77716C;
}

@media(max-width: 600px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .insight-grid {
        grid-template-columns: 1fr;
    }
}

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

if "assessment_started" not in st.session_state:
    st.session_state.assessment_started = False

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False


# =========================================================
# LOGIN / SIGNUP / FORGOT PASSWORD
# =========================================================

if not st.session_state.logged_in:

    st.title("🤖 AI Skill Gap & Career Intelligence Agent")
    st.caption("Your personalized career intelligence platform")

    login_tab, signup_tab, forgot_tab = st.tabs([
        "🔐 Login",
        "👤 Create Account",
        "🔑 Forgot Password"
    ])

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    with login_tab:

        st.subheader("Welcome Back")

        with st.form("login_form"):

            login_email = st.text_input(
                "Email",
                key="login_email"
            )

            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            login_submitted = st.form_submit_button(
                "🔐 Login",
                use_container_width=True
            )

        if login_submitted:

            clean_email = login_email.strip().lower()

            if not clean_email or not login_password:

                st.warning("Please enter your email and password.")

            else:

                user_name = verify_user(
                    clean_email,
                    login_password
                )

                if user_name:

                    st.session_state.logged_in = True
                    st.session_state.user_name = user_name

                    st.success("Welcome back!")

                    st.rerun()

                else:

                    st.error("Invalid email or password.")

    # -----------------------------------------------------
    # CREATE ACCOUNT
    # -----------------------------------------------------

    with signup_tab:

        st.subheader("Create Your Account")

        with st.form("signup_form", clear_on_submit=False):

            signup_name = st.text_input(
                "Full Name",
                key="signup_name"
            )

            signup_email = st.text_input(
                "Email",
                key="signup_email"
            )

            signup_password = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            signup_confirm = st.text_input(
                "Confirm Password",
                type="password",
                key="signup_confirm"
            )

            signup_submitted = st.form_submit_button(
                "✨ Create Account",
                use_container_width=True
            )

        if signup_submitted:

            clean_name = signup_name.strip()
            clean_email = signup_email.strip().lower()

            if (
                not clean_name
                or not clean_email
                or not signup_password
                or not signup_confirm
            ):

                st.warning("Please fill in all four fields.")

            elif not re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+",
                clean_email
            ):

                st.warning("Please enter a valid email address.")

            elif signup_password != signup_confirm:

                st.error("Passwords do not match.")

            elif len(signup_password) < 6:

                st.warning(
                    "Password must contain at least 6 characters."
                )

            else:

                created = create_user(
                    clean_name,
                    clean_email,
                    signup_password
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
                        "An account with this email already exists."
                    )

    # -----------------------------------------------------
    # FORGOT PASSWORD
    # -----------------------------------------------------

    with forgot_tab:

        st.subheader("🔑 Reset Your Password")

        st.write(
            "Enter your registered email and create a new password."
        )

        with st.form("forgot_password_form"):

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

            reset_submitted = st.form_submit_button(
                "🔄 Reset Password",
                use_container_width=True
            )

        if reset_submitted:

            clean_reset_email = reset_email.strip().lower()

            if (
                not clean_reset_email
                or not new_reset_password
                or not confirm_reset_password
            ):

                st.warning("Please fill in all fields.")

            elif new_reset_password != confirm_reset_password:

                st.error("Passwords do not match.")

            elif len(new_reset_password) < 6:

                st.warning(
                    "Password must contain at least 6 characters."
                )

            else:

                changed = reset_password(
                    clean_reset_email,
                    new_reset_password
                )

                if changed:

                    st.success(
                        "Password changed successfully!"
                    )

                    st.info(
                        "You can now log in with your new password."
                    )

                else:

                    st.error(
                        "No account was found with that email."
                    )

    st.stop()


# =========================================================
# LOGOUT
# =========================================================

st.sidebar.success(
    f"Welcome, {st.session_state.user_name}"
)

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.assessment_started = False
    st.session_state.interview_started = False

    st.rerun()


# =========================================================
# APPLICATION HEADER
# =========================================================

st.title("🤖 AI Skill Gap & Career Intelligence Agent")

st.markdown(
    "Analyze your skills • Find your gaps • Build your career roadmap"
)


# =========================================================
# CAREER DATABASE
# =========================================================

career_data = {

    "AI Engineer": {

        "skills": [
            "Python", "Machine Learning", "Deep Learning",
            "AI", "NLP", "TensorFlow", "PyTorch",
            "NumPy", "Pandas", "SQL", "Git", "GitHub"
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
            "Python", "SQL", "Statistics",
            "Machine Learning", "Data Science",
            "Pandas", "NumPy", "Data Visualization",
            "Power BI", "Git"
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
            "Python", "SQL", "Excel",
            "Power BI", "Tableau", "Statistics",
            "Data Visualization", "Pandas",
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
            "Python", "Machine Learning",
            "Deep Learning", "TensorFlow",
            "PyTorch", "SQL", "NumPy",
            "Pandas", "Git", "GitHub"
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

    "Python", "Java", "C++", "SQL", "Excel",
    "Machine Learning", "Deep Learning", "AI",
    "Data Science", "Statistics", "Pandas",
    "NumPy", "Power BI", "Tableau",
    "Data Visualization", "TensorFlow",
    "PyTorch", "NLP", "Git", "GitHub",
    "HTML", "CSS", "JavaScript", "React",
    "MongoDB", "Communication", "Leadership"

]


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def extract_text_from_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    extracted_text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            extracted_text.append(page_text)

    return " ".join(extracted_text)


def extract_skills(resume_text):

    text_lower = resume_text.lower()

    detected = []

    for skill in all_skills:

        if skill.lower() in text_lower:

            detected.append(skill)

    return detected


def calculate_match(user_skills, career_skills):

    if not user_skills or not career_skills:

        return 0.0

    user_text = " ".join(user_skills)

    career_text = " ".join(career_skills)

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([
        user_text,
        career_text
    ])

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(float(similarity) * 100, 2)


def generate_roadmap(missing_skills):

    roadmap = []

    for skill in missing_skills:

        roadmap.append(
            f"Learn {skill} → Practice → Build a mini project → Add it to your resume"
        )

    return roadmap


def resume_context_questions(
    target_career,
    detected_skills,
    resume_text,
    mode
):

    skills = detected_skills[:]

    resume_lower = resume_text.lower()

    questions = []

    if skills:

        primary = skills[:3]

        if mode == "assessment":

            questions.extend([

                f"Your resume lists {', '.join(primary)}. Explain how you would use these skills in a {target_career} workflow.",

                f"Choose one project involving {primary[0]}. What was your approach?",

                f"How would you improve a project using {primary[-1]}?"

            ])

        else:

            questions.extend([

                f"Explain a project where you used {primary[0]}.",

                f"Why did you choose {', '.join(primary)} for your work?",

                "Describe a technical challenge you faced and how you solved it."

            ])

    if any(
        term in resume_lower
        for term in [
            "project", "internship", "experience",
            "developed", "built", "created",
            "implemented", "model", "dashboard"
        ]
    ):

        questions.append(
            "Explain one project from your resume and how you measured its success."
        )

    questions.append(
        f"Why are you interested in the {target_career} role?"
    )

    return questions[:5]


# =========================================================
# CAREER SELECTION
# =========================================================

st.markdown("## 01. Choose Your Target Career")

target_career = st.selectbox(
    "Select the career you want to prepare for",
    list(career_data.keys()),
    key="target_career_main"
)

st.success(f"Your selected career: {target_career}")


# =========================================================
# RESUME UPLOAD
# =========================================================

st.markdown("---")

st.markdown("## 02. Resume Analysis")

st.write(
    "Upload your resume to identify your existing skills "
    "and compare them with your target career."
)

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

if uploaded_file is None:

    st.info("Upload your resume to continue.")

    st.stop()


try:

    resume_text = extract_text_from_pdf(uploaded_file)

except Exception:

    st.error(
        "Unable to read this PDF. Please upload another PDF."
    )

    st.stop()


if not resume_text.strip():

    st.error(
        "No readable text found. Please upload a text-based PDF."
    )

    st.stop()


# =========================================================
# DETECT SKILLS
# =========================================================

detected_skills = extract_skills(resume_text)

required_skills = career_data[target_career]["skills"]


st.markdown("---")

st.markdown("## 03. Your Profile Snapshot")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Detected Skills",
        len(detected_skills)
    )

with col2:

    st.metric(
        "Target Career",
        target_career
    )

with col3:

    st.metric(
        "Required Skills",
        len(required_skills)
    )


if detected_skills:

    st.markdown("### Skills Found")

    for skill in detected_skills:

        st.markdown(
            f'<span class="skill-chip">✓ {skill}</span>',
            unsafe_allow_html=True
        )

else:

    st.warning(
        "No predefined skills were detected in your resume."
    )


# =========================================================
# SELF ASSESSMENT
# =========================================================

st.markdown("---")

st.markdown("## 04. Rate Your Skills")

skill_levels = {}

if detected_skills:

    columns = st.columns(2)

    for index, skill in enumerate(detected_skills):

        with columns[index % 2]:

            skill_levels[skill] = st.select_slider(
                skill,
                options=[
                    "Beginner",
                    "Intermediate",
                    "Advanced"
                ],
                value="Beginner",
                key=f"skill_level_{skill}"
            )

else:

    st.info("Skill ratings will appear when skills are detected.")


# =========================================================
# CAREER MATCH
# =========================================================

st.markdown("---")

st.markdown("## 05. Career Match Analysis")

match_percentage = calculate_match(
    detected_skills,
    required_skills
)

st.metric(
    "Career Match Percentage",
    f"{match_percentage}%"
)

st.progress(
    min(match_percentage / 100, 1.0)
)

st.caption(
    "This percentage represents TF-IDF text similarity "
    "between detected and required skills."
)


# =========================================================
# SKILL GAP ANALYSIS
# =========================================================

st.markdown("---")

st.markdown("## 06. Missing Skills")

missing_skills = [

    skill for skill in required_skills
    if skill not in detected_skills

]

if missing_skills:

    for index, skill in enumerate(missing_skills, 1):

        st.markdown(
            f"**{index}. {skill}**"
        )

else:

    st.success(
        "All listed career skills were detected in your resume."
    )


# =========================================================
# PERSONALIZED ROADMAP
# =========================================================

st.markdown("---")

st.markdown("## 07. Your Learning Roadmap")

roadmap = generate_roadmap(missing_skills)

if roadmap:

    for index, skill in enumerate(missing_skills, 1):

        st.markdown(f"""
        <div class="roadmap-card">

        <h4>{index:02d}. {skill}</h4>

        <b>Step 1:</b> Learn the fundamentals.

        <br>

        <b>Step 2:</b> Practice with exercises.

        <br>

        <b>Step 3:</b> Build a mini project.

        <br>

        <b>Step 4:</b> Add the project to your resume.

        </div>
        """, unsafe_allow_html=True)

else:

    st.success(
        "You have covered all the listed skills!"
    )


# =========================================================
# OPTIONAL ASSESSMENT AND MOCK INTERVIEW
# =========================================================

st.markdown("---")

st.markdown("## 08. Practice Zone")

assessment_tab, interview_tab = st.tabs([
    "📝 Resume-Based Assessment",
    "🎤 Mock Interview"
])


# ---------------------------------------------------------
# ASSESSMENT
# ---------------------------------------------------------

with assessment_tab:

    st.write(
        "Practice questions based on your resume and target career."
    )

    if st.button("Start Assessment"):

        st.session_state.assessment_started = True

    if st.session_state.assessment_started:

        questions = resume_context_questions(
            target_career,
            detected_skills,
            resume_text,
            "assessment"
        )

        answers = []

        for index, question in enumerate(questions):

            st.markdown(f"**Question {index + 1}: {question}**")

            answer = st.text_area(
                "Your Answer",
                key=f"assessment_answer_{index}"
            )

            answers.append(answer)

        if st.button("Submit Assessment"):

            answered = sum(
                bool(answer.strip())
                for answer in answers
            )

            if answered == len(answers):

                st.success("Assessment completed!")

            else:

                st.warning(
                    f"You answered {answered} of {len(answers)} questions."
                )


# ---------------------------------------------------------
# MOCK INTERVIEW
# ---------------------------------------------------------

with interview_tab:

    st.write(
        "Practice explaining your projects, skills and experience."
    )

    if st.button("Start Mock Interview"):

        st.session_state.interview_started = True

    if st.session_state.interview_started:

        questions = resume_context_questions(
            target_career,
            detected_skills,
            resume_text,
            "interview"
        )

        answers = []

        for index, question in enumerate(questions):

            st.markdown(f"**Question {index + 1}: {question}**")

            answer = st.text_area(
                "Your Response",
                key=f"interview_answer_{index}"
            )

            answers.append(answer)

        if st.button("Analyze Interview"):

            answered = sum(
                bool(answer.strip())
                for answer in answers
            )

            if answered == len(answers):

                st.success("Mock interview completed!")

            else:

                st.warning(
                    f"You answered {answered} of {len(answers)} questions."
                )


# =========================================================
# CAREER INTELLIGENCE
# =========================================================

st.markdown("---")

st.markdown("## 09. Career Intelligence")

st.subheader("Required Career Skills")

for skill in required_skills:

    st.markdown(
        f'<span class="skill-chip">{skill}</span>',
        unsafe_allow_html=True
    )


st.subheader("Suggested Job Roles")

for role in career_data[target_career]["roles"]:

    st.write(f"💼 {role}")


# =========================================================
# DOWNLOAD CAREER REPORT
# =========================================================

st.markdown("---")

st.markdown("## 10. Download Your Career Report")

report = f"""
AI SKILL GAP & CAREER INTELLIGENCE AGENT

User: {st.session_state.user_name}

Target Career:
{target_career}


DETECTED SKILLS
---------------

{', '.join(detected_skills)}


SELF ASSESSMENT
---------------

"""

for skill, level in skill_levels.items():

    report += f"{skill}: {level}\n"


report += f"""

CAREER MATCH
------------

{match_percentage}%


MISSING SKILLS
--------------

{', '.join(missing_skills)}


LEARNING ROADMAP
----------------

"""

for index, item in enumerate(roadmap, 1):

    report += f"{index}. {item}\n"


report += """

SUGGESTED JOB ROLES
-------------------
"""

for role in career_data[target_career]["roles"]:

    report += f"- {role}\n"


st.download_button(
    label="📥 Download Career Report",
    data=report,
    file_name="career_intelligence_report.txt",
    mime="text/plain",
    use_container_width=True
)


st.markdown("---")

st.success(
    "Your Career Intelligence Dashboard is ready!"
)

st.caption(
    "AI Skill Gap & Career Intelligence Agent | Career Development Platform"
)
