import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print(api_key)
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",  
    temperature=0.3,
    google_api_key=api_key
)
ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["resume", "job_description"],
    template="""
You are an expert ATS (Applicant Tracking System) optimization specialist.

Analyze the following resume against the job description and respond ONLY with a valid JSON object.
Do not include any explanation, markdown, or text outside the JSON.

Resume:
{resume}

Job Description:
{job_description}

Return this exact JSON structure:
{{
  "score": <integer 0-100 representing keyword and semantic match>,
  "matched_keywords": [<list of keywords/skills found in both resume and JD>],
  "missing_keywords": [<list of important keywords from JD missing in resume>],
  "bullet_suggestions": [
    {{
      "original": "<exact bullet point from resume>",
      "optimized": "<rewritten bullet point with missing keywords, preserving truthfulness>",
      "keywords_added": [<keywords added in this rewrite>]
    }}
  ],
  "summary": "<2-3 sentence overall assessment>"
}}

Rules:
- score must be a number between 0 and 100
- matched_keywords: max 15 items
- missing_keywords: max 10 most critical items
- bullet_suggestions: rewrite the 3 most impactful bullet points from the resume
- Do NOT invent experience. Only rephrase existing experience to highlight relevant skills.
"""
)

def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Sends resume and JD to GPT-4o-mini.
    Returns a parsed dictionary with score, keywords, and suggestions.
    """
    chain = ANALYSIS_PROMPT | llm
    response = chain.invoke({
        "resume": resume_text[:8000],           # stay within token limits
        "job_description": job_description[:3000]
    })
    if isinstance(response.content, list):
        raw = "".join(
            item.get("text",str(item)) if isinstance(item, dict) else str(item)
            for item in response.content
        )
    else:
        raw = str(response.content)
    raw = raw.strip()

    # Strip markdown fences if model adds them
    if raw.startswith("```"):
        raw = raw.replace("```json","").replace("'''","").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print("Failed JSON:")
        print(raw)
        raise e