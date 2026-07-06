# Research Workflow

Use this workflow whenever the user gives you a topic to research.
Follow every stage in order. Do not proceed to the next stage until the current one is complete.

---


## Stage 1: Clarify Before You Research

Ask the user the following questions before doing anything else. Present them as a numbered list and wait for answers. For dispute/chargeback investigations, collect case identifiers and data sources up-front.

1. **Scope** — How broad or narrow should this be? (e.g., quick case summary vs. deep investigation)
2. **Case ID / Transaction** — Provide internal case ID, transaction ID, and relevant dates
3. **Audience** — Who will read this? (e.g., Chargeback specialist, Fraud ops, Legal)
4. **Depth** — How detailed? (e.g., quick summary, thorough evidence package)
5. **Data sources** — Where can logs, shipping, and comms be pulled from? (gateway, CRM, shipping provider)
6. **Urgency** — Any SLA or representment deadline to meet?

Do not assume answers. If the user already provided some of these, confirm them and only ask for what is missing.

---

## Stage 2: Plan the Research

Before searching, state your research plan to the user as 3-5 bullet points covering:
- What subtopics you will cover
- What types of sources you will target (official docs, news, academic papers, practitioner blogs)
- How many sources you aim to find (target 8-10 credible sources)
- Any known gaps or limitations upfront

Wait for the user to approve or adjust the plan before proceeding.

---

## Stage 3: Conduct the Research

Search systematically. For each subtopic identified in Stage 2:
- Run targeted searches using WebSearch
- Fetch full content from the most relevant pages using WebFetch where needed
- Look for: definitions, statistics, real-world examples, expert opinions, contrasting viewpoints
- Flag anything that is contested, outdated, or unverified

Source quality guidelines:
- Prefer primary sources (official documentation, original studies, direct quotes)
- Prefer sources from the last 2 years unless the topic is foundational or historical
- Record the URL and publication date for every source used
- Minimum 5 sources. Target 8-10 for a thorough report.

---

## Stage 4: Organize the Findings

Before writing the report, group your notes:
- Identify 3-5 major themes or subtopics from what you found
- Note which sources support which themes
- Identify the 3-5 most important actionable takeaways
- Identify 2-4 logical next steps for the reader

This step ensures the report is structured, not just a dump of notes.

---


## Stage 5: Write the Report

Use the template at `resources/report-template.md` and include the `Case ID` and `evidence checklist` fields. Follow these rules:

- Executive Summary: exactly 3-5 bullet points, each one sentence
- Case Details & Evidence Checklist must be completed
- Timeline & Findings: list events chronologically with timestamps
- No paragraph walls — convert long text to bullets
- Reference every factual claim with the source location (file path, log ID, or URL)
- Key Takeaways: 3-5 bullets with the most actionable insights (required)
- Recommended Next Steps: 2-4 concrete actions with owners and deadlines (required)
- Keep the whole report under 800 words unless the user asked for exhaustive depth

---


## Stage 6: Save the Report

Save the finished report to the `output/` folder and attach or link the evidence files. Naming convention:

- `YYYY-MM-DD-caseid-topic.md` (include case id for traceability)

After saving, tell the user:

- The full file path where the report was saved
- How many evidence items / sources were attached
- A one-line summary of the top finding and recommended disposition
