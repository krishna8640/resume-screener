def build_prompt(resume_text, job_description=""):
    if job_description.strip():
        jd_section = f"""
Job Description:
{job_description}

Compare the resume against this job description. Use it to inform the job_fit_score, weaknesses, and rewrite_tips.
Tailor rewrite_tips to highlight gaps between the resume and the role.
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
  "job_fit_score": 72,
  "rewrite_tips": [
    {{
      "type": "bullet",
      "original": "Responsible for managing deployments",
      "rewritten": "Led (Action) deployment pipeline redesign (What) using GitHub Actions and Docker (How), cutting release time by 40% (Impact)",
      "note": "Add the quantified outcome if you have it — e.g. how many deployments per week, or time saved."
    }},
    {{
      "type": "missing_section",
      "section": "Professional Summary",
      "suggestion": "Add a 2-3 sentence summary at the top covering your role, core stack, and one standout achievement."
    }},
    {{
      "type": "general",
      "suggestion": "Move Python and SQL higher in your skills list — they appear most relevant to the roles you have held."
    }}
  ]
}}

Rules:
- job_fit_score must be an integer from 0 to 100
- skills, strengths, weaknesses must be arrays of short strings (not sentences)
- experience_summary must be a single string
- rewrite_tips must be an array of tip objects. Each tip must have a "type" field:
    * "bullet"          — for weak or vague bullet points found in the resume
    * "missing_section" — for sections that are absent but would strengthen the resume
    * "general"         — for broader formatting, ordering, or language advice
- For every "bullet" tip you MUST include:
    * "original"  — quote the weak bullet exactly as it appears in the resume
    * "rewritten" — rewrite it using the Action + What + How + Impact framework:
        Action  = strong verb (Led, Built, Reduced, Designed, Launched...)
        What    = the thing you built or did
        How     = the method, tool, or approach used
        Impact  = measurable outcome (%, $, time, users, etc.)
    * "note"      — if the resume lacks enough detail to complete all four parts,
                    tell the candidate exactly what information to fill in
- Do not fabricate experience, companies, or metrics not implied by the resume
- Provide 3 to 6 rewrite_tips total, prioritising the most impactful improvements
- Return ONLY the JSON object, nothing else

{jd_section}

Resume:
{resume_text}
"""