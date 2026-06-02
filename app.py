
import streamlit as st
import PyPDF2
import pandas as pd

st.set_page_config(page_title="AI ATS Resume Analyzer Pro", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.stApp {background: linear-gradient(to right,#0f172a,#1e293b); color:white;}
.big-title{font-size:50px;font-weight:bold;text-align:center;color:#38bdf8;}
.sub-title{text-align:center;color:#cbd5e1;}
.card{background:#1e293b;padding:20px;border-radius:12px;margin:10px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🚀 AI ATS Resume Analyzer Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">ATS Score + Career Prediction + Skill Gap Analysis</p>', unsafe_allow_html=True)

career_roles = {
    "Web Developer":["html","css","javascript","react","node","express","sql","git"],
    "Python Developer":["python","django","flask","api","sql","git"],
    "Data Analyst":["python","sql","excel","power bi","tableau","statistics","data analysis"],
    "Data Scientist":["python","machine learning","deep learning","pandas","numpy","tensorflow","sql"],
    "UI/UX Designer":["figma","adobe xd","wireframe","prototype","ui design"]
}

all_skills = sorted(set(skill for v in career_roles.values() for skill in v))

salary_ranges = {
    "Web Developer":"₹3–10 LPA",
    "Python Developer":"₹4–12 LPA",
    "Data Analyst":"₹4–11 LPA",
    "Data Scientist":"₹6–20 LPA",
    "UI/UX Designer":"₹3–12 LPA"
}

def extract_text(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content.lower()
    return text

def ats_score(text):
    matched = [s for s in all_skills if s in text]
    score = int((len(matched)/len(all_skills))*100)
    return score, matched

def predict_career(text):
    best_role = ""
    best_score = 0
    matched_best = []
    missing_best = []

    for role, skills in career_roles.items():
        matched = [s for s in skills if s in text]
        score = int((len(matched)/len(skills))*100)

        if score > best_score:
            best_score = score
            best_role = role
            matched_best = matched
            missing_best = [s for s in skills if s not in matched]

    return best_role, best_score, matched_best, missing_best

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)

    score, matched = ats_score(text)
    role, role_score, role_matched, role_missing = predict_career(text)

    st.subheader("🎯 ATS Score")
    st.progress(score/100)
    st.metric("ATS Score", f"{score}%")

    c1, c2 = st.columns(2)

    with c1:
        st.success(f"Recommended Profession: {role}")
        st.info(f"Profession Match Score: {role_score}%")
        st.write("Expected Salary:", salary_ranges.get(role, "N/A"))

    with c2:
        st.write("### Skills Found")
        for s in role_matched:
            st.write("✅", s)

    st.write("### Missing Skills For Selected Career")
    if role_missing:
        for s in role_missing:
            st.write("❌", s)
    else:
        st.success("All required skills found for this profession!")

    st.write("### Career Roadmap")
    for i, skill in enumerate(role_missing, start=1):
        st.write(f"{i}. Learn {skill}")

    suggestions = []
    if "github" not in text:
        suggestions.append("Add GitHub profile")
    if "linkedin" not in text:
        suggestions.append("Add LinkedIn profile")
    if "project" not in text:
        suggestions.append("Add projects section")
    if "internship" not in text:
        suggestions.append("Add internship experience")

    st.write("### Resume Suggestions")
    if suggestions:
        for s in suggestions:
            st.write("✔", s)
    else:
        st.success("Resume looks strong!")

    chart_df = pd.DataFrame({
        "Category":["Matched Skills","Missing Skills"],
        "Count":[len(role_matched), len(role_missing)]
    })
    st.bar_chart(chart_df.set_index("Category"))

    with st.expander("Extracted Resume Text"):
        st.text_area("", text, height=300)

st.sidebar.title("About")
st.sidebar.info(
    "Offline ATS Resume Analyzer\n\n"
    "✔ ATS Score\n"
    "✔ Career Prediction\n"
    "✔ Missing Skills\n"
    "✔ Resume Suggestions\n"
    "✔ Salary Estimate\n"
    "✔ Learning Roadmap"
)
