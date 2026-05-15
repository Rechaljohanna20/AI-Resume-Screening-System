import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.llm_service import analyze_resume

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="AI Based Resume Screening System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    /* Main font and background */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    .main { background-color: #f8f9fa; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a2e;
        color: white;
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* Score card */
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin-bottom: 1.5rem;
    }
    .score-number {
        font-size: 4rem;
        font-weight: 800;
        line-height: 1;
    }
    .score-label {
        font-size: 1rem;
        opacity: 0.85;
        margin-top: 0.5rem;
    }

    /* Keyword pills */
    .keyword-matched {
        display: inline-block;
        background: #d4edda;
        color: #155724;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .keyword-missing {
        display: inline-block;
        background: #f8d7da;
        color: #721c24;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    /* Suggestion cards */
    .suggestion-card {
        background-color: #ffffff;
        color: #111827;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .original-text {
        background-color: #fee2e2;
        color: #991b1b;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 0.75rem;
        font-size: 0.9rem;
    }
    .optimized-text {
        background-color: #dcfce7;
        color: #166534;
        border-radius: 8px;
        padding: 12px;
        font-size: 0.9rem;
    }

    /* Button style */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar Navigation ────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎯 AI Based Resume Screening System")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["🏠 Home", "🔍 Analyze", "ℹ️ About"],
        label_visibility="hidden"
    )
    st.markdown("---")
    st.markdown("**How it works:**")
    st.markdown("1. Upload your resume (PDF)")
    st.markdown("2. Paste the job description")
    st.markdown("3. Get your ATS match score")
    st.markdown("4. Apply AI-suggested rewrites")

# ─── HOME PAGE ─────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown("# 🎯 Resume Screening AI")
    st.markdown("### Beat the ATS. Land the Interview.")
    st.markdown("""
    Most resumes never reach a human — they're filtered out by
    **Applicant Tracking Systems (ATS)** before anyone reads them.

    PivotPerfect AI analyzes your resume against any job description,
    identifies keyword gaps, and rewrites your bullet points to maximize
    your match score — without changing your actual experience.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📊 Match Score")
        st.markdown("Instant 0–100 score showing how well your resume matches the job.")
    with col2:
        st.markdown("### 🔑 Keyword Gap")
        st.markdown("See exactly which skills the employer wants that you're not highlighting.")
    with col3:
        st.markdown("### ✍️ AI Rewrites")
        st.markdown("Get ready-to-use optimized bullet points that preserve your truthful experience.")

    st.markdown("---")
    if st.button("🚀 Start Optimizing →"):
        st.info("Click **🔍 Analyze** in the sidebar to begin.")

# ─── ANALYZE PAGE ──────────────────────────────────────────
elif page == "🔍 Analyze":
    st.markdown("## 🔍 Upload & Analyze")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📄 Your Resume")
        uploaded_resume = st.file_uploader(
            "Upload resume as PDF",
            type=["pdf"],
            help="Upload a PDF version of your resume."
        )
        if uploaded_resume:
            st.success(f"✅ Uploaded: {uploaded_resume.name}")

    with col_right:
        st.markdown("### 💼 Target Job Description")
        job_description = st.text_area(
            "Paste the full job description here",
            height=220,
            placeholder="Copy and paste the complete job posting here..."
        )

    st.markdown("---")

    analyze_btn = st.button("🎯 Analyze My Resume", use_container_width=True)

    if analyze_btn:
        if not uploaded_resume:
            st.error("⚠️ Please upload your resume PDF first.")
        elif not job_description.strip():
            st.error("⚠️ Please paste a job description.")
        else:
            with st.spinner("🤖 Analyzing your resume... this takes 15–30 seconds"):
                try:
                    # Extract text from PDF
                    resume_text = extract_text_from_pdf(uploaded_resume)

                    if not resume_text:
                        st.error("Could not extract text from the PDF. Try a text-based PDF (not scanned).")
                        st.stop()

                    # Store in session state
                    st.session_state["resume_text"] = resume_text
                    st.session_state["job_text"] = job_description

                    # Call AI
                    results = analyze_resume(resume_text, job_description)
                    st.session_state["analysis_results"] = results

                    st.success("✅ Analysis complete! Scroll down to see your results.")

                except Exception as e:
                    st.error(f"❌ Something went wrong: {str(e)}")
                    st.stop()

    # ─── Display Results ──────────────────────────────────
    if "analysis_results" in st.session_state:
        results = st.session_state["analysis_results"]
        score = results.get("score", 0)

        st.markdown("---")
        st.markdown("## 📊 Your Results")

        # Score display
        score_color = "#28a745" if score >= 70 else "#ffc107" if score >= 45 else "#dc3545"
        score_emoji = "🟢" if score >= 70 else "🟡" if score >= 45 else "🔴"
        st.markdown(f"""
        <div class="score-card">
            <div class="score-number">{score}</div>
            <div class="score-label">ATS Match Score {score_emoji}</div>
        </div>
        """, unsafe_allow_html=True)

        st.progress(score / 100)

        if score >= 70:
            st.success("🟢 Strong match! You're a competitive candidate for this role.")
        elif score >= 45:
            st.warning("🟡 Moderate match. Applying the suggestions below can significantly improve your chances.")
        else:
            st.error("🔴 Low match. Your resume needs substantial keyword alignment for this role.")

        # Summary
        if results.get("summary"):
            st.markdown("### 💡 AI Summary")
            st.info(results["summary"])

        # Keyword analysis
        st.markdown("### 🔑 Keyword Analysis")
        kw_col1, kw_col2 = st.columns(2)

        with kw_col1:
            st.markdown("**✅ Keywords You Already Have**")
            matched = results.get("matched_keywords", [])
            if matched:
                pills = " ".join([f'<span class="keyword-matched">{k}</span>' for k in matched])
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.markdown("_None detected_")

        with kw_col2:
            st.markdown("**❌ Missing Keywords to Add**")
            missing = results.get("missing_keywords", [])
            if missing:
                pills = " ".join([f'<span class="keyword-missing">{k}</span>' for k in missing])
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.markdown("_No critical gaps found — great job!_")

        # Bullet suggestions
        st.markdown("---")
        st.markdown("## ✍️ AI Action Plan — Optimized Bullet Points")
        st.markdown(
            "These are AI-suggested rewrites of your existing bullet points. "
            "Copy and paste them into your resume."
        )

        suggestions = results.get("bullet_suggestions", [])
        if not suggestions:
            st.info("No specific bullet point suggestions were generated for this analysis.")
        else:
            for i, s in enumerate(suggestions, 1):
                st.markdown(f"### Suggestion {i}")
                st.markdown(f"""
                <div class="suggestion-card">
                    <p><strong>🔴 Original</strong></p>
                    <div class="original-text">{s.get("original", "N/A")}</div>
                    <p><strong>🟢 Optimized</strong></p>
                    <div class="optimized-text">{s.get("optimized", "N/A")}</div>
                    <p style="margin-top:0.75rem; font-size:0.8rem; color: #000000;">
                        Keywords added: {", ".join(s.get("keywords_added", []))}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Raw resume preview (collapsed)
        with st.expander("📄 View extracted resume text"):
            st.text(st.session_state.get("resume_text", ""))

# ─── ABOUT PAGE ────────────────────────────────────────────
elif page == "ℹ️ About":
    st.markdown("## ℹ️ About Resume Screening AI")
    st.markdown("""
    **Resume Screening AI** is an ATS resume optimization tool built with:

    | Component | Technology |
    |-----------|-----------|
    | Frontend + Backend | Streamlit |
    | PDF Parsing | pdfplumber |
    | AI Model | GPT-4o-mini via OpenAI |
    | AI Orchestration | LangChain |
    | Deployment | Streamlit Cloud |

    ### Scoring Logic
    The 0–100 score is generated by GPT-4o-mini via semantic comparison of your
    resume content against extracted job requirements, factoring in both
    keyword overlap and contextual relevance.

    ### Privacy
    Your resume text is sent to OpenAI for analysis. No data is stored
    persistently — all session data clears on page refresh.

    ### Honesty-Preserved Rewrites
    The AI is explicitly instructed **not to invent experience**. It only
    rephrases your existing bullet points to surface relevant keywords
    you may already have but haven't expressed clearly.
    """)
