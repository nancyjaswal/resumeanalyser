# app.py
import streamlit as st
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import time
# ---------------- PAGE CONFIG ----------------


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI ATS Resume Analyzer Pro",
    page_icon="🚀",
    layout="wide"
)

# PRELOADER
preloader = st.empty()

preloader.markdown("""
<div style="
display:flex;
justify-content:center;
align-items:center;
height:80vh;
flex-direction:column;
">

<h1 style="
font-size:60px;
font-weight:900;
background:linear-gradient(90deg,#38bdf8,#818cf8,#ec4899);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:20px;
">
🚀 ResumeAnalyzer
</h1>

<div class="loader"></div>

<p style="
color:white;
font-size:20px;
margin-top:20px;
">
Analyzing Careers with AI...
</p>

</div>

<style>

.preloader-container{
display:flex;
justify-content:center;
align-items:center;
flex-direction:column;
height:90vh;
}

.logo{
font-size:70px;
font-weight:900;
background: linear-gradient(
90deg,
#00d4ff,
#6366f1,
#ff4ecd
);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
animation: glow 2s infinite alternate;
}

.tagline{
color:#cbd5e1;
font-size:20px;
margin-top:10px;
margin-bottom:30px;
}

.progress-box{
width:350px;
height:12px;
background:#1e293b;
border-radius:50px;
overflow:hidden;
}

.progress-fill{
height:100%;
width:100%;
background:linear-gradient(
90deg,
#00d4ff,
#6366f1,
#ff4ecd
);
animation: loading 3s linear forwards;
}

@keyframes loading{
from{width:0%;}
to{width:100%;}
}

@keyframes glow{
from{
filter:drop-shadow(0px 0px 10px #00d4ff);
}
to{
filter:drop-shadow(0px 0px 30px #ff4ecd);
}
}

</style>
""", unsafe_allow_html=True)

time.sleep(3)

preloader.empty()


st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right,#0f172a,#1e293b);
    color:white;
}

.big-title{
    font-size:50px;
    font-weight:bold;
    text-align:center;
    color:#38bdf8;
}

.sub-title{
    text-align:center;
    color:#cbd5e1;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="big-title">🚀 AI ATS Resume Analyzer Pro</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">ATS Score + Career Prediction + Skill Gap Analysis</p>',
    unsafe_allow_html=True
)

# ---------------- CAREER DATA ----------------

career_roles = {
    "Web Developer": [
        "html", "css", "javascript", "react",
        "node", "express", "sql", "git"
    ],

    "Python Developer": [
        "python", "django", "flask",
        "api", "sql", "git"
    ],

    "Data Analyst": [
        "python", "sql", "excel",
        "power bi", "tableau",
        "statistics", "data analysis"
    ],

    "Data Scientist": [
        "python", "machine learning",
        "deep learning", "pandas",
        "numpy", "tensorflow", "sql"
    ],

    "UI/UX Designer": [
        "figma", "adobe xd",
        "wireframe", "prototype",
        "ui design"
    ]
}

salary_ranges = {
    "Web Developer": "₹3–10 LPA",
    "Python Developer": "₹4–12 LPA",
    "Data Analyst": "₹4–11 LPA",
    "Data Scientist": "₹6–20 LPA",
    "UI/UX Designer": "₹3–12 LPA"
}

all_skills = sorted(
    set(skill for skills in career_roles.values() for skill in skills)
)

# ---------------- ML TRAINING DATA ----------------

training_data = [
    ("html css javascript react node express sql git frontend web development", "Web Developer"),

    ("python django flask api backend sql git software development", "Python Developer"),

    ("python sql excel power bi tableau statistics data analysis reporting", "Data Analyst"),

    ("python machine learning deep learning pandas numpy tensorflow sql ai", "Data Scientist"),

    ("figma adobe xd wireframe prototype ui design ux design", "UI/UX Designer"),

    ("react javascript frontend website", "Web Developer"),
    ("flask django backend api", "Python Developer"),
    ("machine learning ai data science", "Data Scientist"),
    ("tableau power bi analytics", "Data Analyst"),
    ("figma user interface prototype", "UI/UX Designer")
]

X_train = [x[0] for x in training_data]
y_train = [x[1] for x in training_data]

vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X_train)

model = MultinomialNB()
model.fit(X_vectorized, y_train)

# ---------------- FUNCTIONS ----------------

def extract_text(pdf_file):
    text = ""

    try:
        reader = PyPDF2.PdfReader(pdf_file)

        for page in reader.pages:
            content = page.extract_text()

            if content:
                text += content.lower()

    except Exception:
        pass

    return text


def ats_score(text):
    matched_skills = [
        skill for skill in all_skills
        if skill in text
    ]

    score = int(
        (len(matched_skills) / len(all_skills)) * 100
    )

    return score, matched_skills


def predict_career_ml(text):

    text_vector = vectorizer.transform([text])

    predicted_role = model.predict(text_vector)[0]

    probabilities = model.predict_proba(text_vector)[0]

    confidence = round(max(probabilities) * 100, 2)

    matched = [
        skill for skill in career_roles[predicted_role]
        if skill in text
    ]

    missing = [
        skill for skill in career_roles[predicted_role]
        if skill not in text
    ]

    return (
        predicted_role,
        confidence,
        matched,
        missing
    )

# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

if uploaded_file:

    text = extract_text(uploaded_file)

    score, matched_skills = ats_score(text)

    role, confidence, role_matched, role_missing = predict_career_ml(text)

    st.subheader("🎯 ATS Score")

    st.progress(score / 100)

    st.metric(
        "ATS Score",
        f"{score}%"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"ML Predicted Career: {role}"
        )

        st.info(
            f"Prediction Confidence: {confidence}%"
        )

        st.write(
            f"Expected Salary: {salary_ranges.get(role,'N/A')}"
        )

    with col2:

        st.write("### Skills Found")

        if role_matched:
            for skill in role_matched:
                st.write("✅", skill)
        else:
            st.write("No matching skills found.")

    st.write("## Missing Skills")

    if role_missing:

        for skill in role_missing:
            st.write("❌", skill)

    else:
        st.success(
            "All required skills found!"
        )

    st.write("## Career Roadmap")

    if role_missing:

        for i, skill in enumerate(role_missing, start=1):
            st.write(
                f"{i}. Learn {skill}"
            )

    else:
        st.success(
            "You already match this role strongly."
        )

    suggestions = []

    if "github" not in text:
        suggestions.append("Add GitHub Profile")

    if "linkedin" not in text:
        suggestions.append("Add LinkedIn Profile")

    if "project" not in text:
        suggestions.append("Add Projects Section")

    if "internship" not in text:
        suggestions.append("Add Internship Experience")

    st.write("## Resume Suggestions")

    if suggestions:

        for item in suggestions:
            st.write("✔", item)

    else:
        st.success(
            "Resume looks strong!"
        )

    st.write("## Skills Analysis")

    chart_df = pd.DataFrame({
        "Category": [
            "Matched Skills",
            "Missing Skills"
        ],
        "Count": [
            len(role_matched),
            len(role_missing)
        ]
    })

    st.bar_chart(
        chart_df.set_index("Category")
    )

    st.write("## Pie Chart Overview")

    fig, ax = plt.subplots()

    ax.pie(
        [
            len(role_matched),
            len(role_missing)
        ],
        labels=[
            "Matched",
            "Missing"
        ],
        autopct="%1.1f%%"
    )

    st.pyplot(fig)

    with st.expander(
        "Extracted Resume Text"
    ):
        st.text_area(
            "",
            text,
            height=300
        )

# ---------------- SIDEBAR ----------------

st.sidebar.title("About")

st.sidebar.info(
    "AI ATS Resume Analyzer Pro\n\n"
    "✔ ATS Score\n"
    "✔ Machine Learning Career Prediction\n"
    "✔ Confidence Score\n"
    "✔ Missing Skills Analysis\n"
    "✔ Learning Roadmap\n"
    "✔ Salary Estimation\n"
    "✔ Resume Suggestions"
)
