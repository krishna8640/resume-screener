def build_prompt(resume_text, job_description=""):
    if job_description.strip():
        jd_section = f"""
Job Description:
{job_description}

Compare the resume against this job description. Use it to inform the job_fit_score and weaknesses.
"""
    else:
        jd_section = "No job description provided. Score based on general resume quality."

    return f"""
You are an expert AI recruiter and resume coach.

Analyze the resume below and return ONLY valid JSON with no extra text, no markdown, no explanation.

Return exactly this structure:
{{
  "skills": ["skill1", "skill2", "skill3"],
  "experience_summary": "2-3 sentence summary of the candidate's background and experience level.",
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["gap1", "gap2", "gap3"],
  "job_fit_score": 72
}}

Rules:
- job_fit_score must be an integer from 0 to 100
- skills, strengths, weaknesses must be arrays of short strings (not sentences)
- experience_summary must be a single string
- Return ONLY the JSON object, nothing else

{jd_section}

Resume:
{resume_text}
"""