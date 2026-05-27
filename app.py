import streamlit as st
import PyPDF2
import re
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI ATS Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
}

h1, h2, h3, h4 {
    color: white;
}

.big-title {
    font-size: 55px;
    font-weight: bold;
    text-align: center;
    color: #38bdf8;
}

.sub-title {
    text-align: center;
    font-size: 20px;
    color: #cbd5e1;
    margin-bottom: 30px;
}

.card {
    background-color: #1e293b;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

.skill-box {
    background-color: #0ea5e9;
    padding: 8px 15px;
    border-radius: 10px;
    display: inline-block;
    margin: 5px;
    color: white;
    font-weight: bold;
}

.missing-skill {
    background-color: #ef4444;
    padding: 8px 15px;
    border-radius: 10px;
    display: inline-block;
    margin: 5px;
    color: white;
    font-weight: bold;
}

.footer {
    text-align: center;
    margin-top: 50px;
    color: gray;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<p class="big-title">🚀 AI ATS Resume Analyzer</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Smart Resume Screening System using Artificial Intelligence</p>',
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 About Project")

st.sidebar.info("""
This project analyzes resumes and checks ATS compatibility.

### Features:
✅ Resume Upload  
✅ ATS Score Checker  
✅ Skill Matching  
✅ Missing Skills Detection  
✅ Resume Suggestions  
✅ Professional Dashboard  
""")

# ---------------- REQUIRED SKILLS ----------------
required_skills = [
    "python",
    "html",
    "css",
    "javascript",
    "sql",
    "machine learning",
    "data analysis",
    "communication",
    "leadership",
    "streamlit",
    "react",
    "django"
]

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📄 Upload Your Resume",
    type=["pdf"]
)

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text(pdf_file):

    text = ""

    pdf_reader = PyPDF2.PdfReader(pdf_file)

    for page in pdf_reader.pages:
        content = page.extract_text()

        if content:
            text += content

    return text.lower()

# ---------------- ATS SCORE ----------------
def calculate_score(resume_text):

    matched_skills = []

    for skill in required_skills:

        if skill.lower() in resume_text:
            matched_skills.append(skill)

    score = int((len(matched_skills) / len(required_skills)) * 100)

    return score, matched_skills

# ---------------- MAIN ----------------
if uploaded_file is not None:

    resume_text = extract_text(uploaded_file)

    score, matched_skills = calculate_score(resume_text)

    missing_skills = [
        skill for skill in required_skills
        if skill not in matched_skills
    ]

    # ---------- SCORE SECTION ----------
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🎯 ATS Resume Score")

    st.progress(score / 100)

    st.markdown(
        f"<h1 style='text-align:center; color:#38bdf8;'>{score}%</h1>",
        unsafe_allow_html=True
    )

    if score >= 80:
        st.success("Excellent Resume 🚀")
    elif score >= 60:
        st.warning("Good Resume 👍")
    else:
        st.error("Resume Needs Improvement ❌")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- SKILLS SECTION ----------
    col1, col2 = st.columns(2)

    with col1:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("✅ Matched Skills")

        for skill in matched_skills:
            st.markdown(
                f'<span class="skill-box">{skill}</span>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("❌ Missing Skills")

        for skill in missing_skills:
            st.markdown(
                f'<span class="missing-skill">{skill}</span>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- RESUME TEXT ----------
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📃 Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=300
    )

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- SUGGESTIONS ----------
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("💡 Resume Improvement Suggestions")

    suggestions = []

    if "projects" not in resume_text:
        suggestions.append("Add Projects Section")

    if "internship" not in resume_text:
        suggestions.append("Add Internship Experience")

    if "github" not in resume_text:
        suggestions.append("Add GitHub Profile")

    if "linkedin" not in resume_text:
        suggestions.append("Add LinkedIn Profile")

    if len(missing_skills) > 0:
        suggestions.append("Add More Technical Skills")

    if len(suggestions) > 0:

        for item in suggestions:
            st.write("✔", item)

    else:
        st.success("Your resume looks strong!")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- CHART ----------
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Resume Analysis")

    data = {
        "Category": ["Matched Skills", "Missing Skills"],
        "Count": [len(matched_skills), len(missing_skills)]
    }

    df = pd.DataFrame(data)

    st.bar_chart(df.set_index("Category"))

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
Developed with ❤️ using Python & Streamlit
</div>
""", unsafe_allow_html=True)