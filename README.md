# Dispute & Chargeback Management Agent

Purpose: Templates and workflows to support chargeback and dispute investigations, evidence collection, and report generation.

Quick start:

- Use `workflows/research.md` to collect scope, case IDs, data sources, and deadlines.
- Use `resources/report-template.md` to generate a case report and save it to `output/`.
- Keep original logs and evidence files alongside the report; reference file paths inside the report.

Folder layout:

- `workflows/` — investigation and research workflows
- `resources/` — templates and checklists
- `output/` — saved reports and deliverables

If you'd like, I can:

- Pre-populate a sample dispute report in `output/` from an example case
- Add a short script to compile evidence into a ZIP for representment

How to create an evidence bundle

1. Put evidence files for a case into a folder, e.g. `evidence/CASE123/`
2. Run the bundling script:

```bash
python scripts/bundle_evidence.py CASE123 evidence/CASE123/ output/
```

The script will produce `output/CASE123_evidence.zip` which you can attach to your representment package.
