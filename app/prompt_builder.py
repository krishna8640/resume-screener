def build_prompt(resume_text):
    return f"""
You are an expert AI recruiter.

Analyze the following resume and return STRICT JSON:

{{
  "skills": [],
  "experience_summary": "",
  "strengths": [],
  "weaknesses": [],
  "job_fit_score": 0
}}

Resume:
{resume_text}
"""