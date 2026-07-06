from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from pathlib import Path


def build_pdf(output_path: Path) -> None:
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=LETTER,
        leftMargin=0.8 * inch,
        rightMargin=0.8 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
        title="Dispute & Chargeback Management Agent - Narrative",
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    h_style = styles["Heading2"]
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        leading=15,
        spaceAfter=8,
    )

    story = []
    story.append(Paragraph("Dispute & Chargeback Management Agent", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("High-Level Narrative", h_style))
    story.append(Spacer(1, 6))

    sections = [
        (
            "What this application does",
            "This application is a dispute-operations simulation and decision-support environment for chargeback management. "
            "It helps teams detect early risk, coordinate evidence, run policy-aware workflows, and close disputes with "
            "clear accountability across customer, merchant, and admin roles.",
        ),
        (
            "Core capabilities",
            "1) End-to-end lifecycle visibility from intake through closure. "
            "2) Early signal detection and urgency scoring. "
            "3) Policy-aware guidance including on-trip urgency and enforcement context. "
            "4) Evidence-centric case handling with sample documentation. "
            "5) Money movement and closure acceptance logic.",
        ),
        (
            "Why it matters",
            "Dispute operations often fail due to fragmented data and inconsistent response quality. "
            "This workspace centralizes communication, evidence, policy guidance, and financial context so teams can reduce "
            "avoidable escalation and improve closure speed.",
        ),
        (
            "Three-party operating model",
            "The system aligns customer, merchant, and platform-admin decisions in one workflow so each case has a shared "
            "timeline, traceable actions, and policy-consistent next steps.",
        ),
        (
            "Current communication flow",
            "Case Level Communication supports Send Money, Receive Money, and Send Message actions. "
            "Submitting an action moves the case to Request Closure. "
            "When the counterparty accepts closure, the case automatically transitions to Closed.",
        ),
        (
            "Merchant benefits",
            "Merchants get faster closure paths, clearer payout and exposure visibility, stronger evidence discipline, "
            "and earlier policy-aligned guidance to reduce avoidable escalation.",
        ),
        (
            "Customer benefits",
            "Customers get clearer lifecycle visibility, more predictable next steps, and faster communication-to-resolution "
            "outcomes with explicit closure acceptance flow.",
        ),
        (
            "Calculable financial metrics",
            "Disputed amount at risk, win/loss value, net recovery, average settlement amount, fee burden, and estimated "
            "escalation cost avoided.",
        ),
        (
            "Calculable non-financial metrics",
            "Time to first response, time to close, closure acceptance rate, escalation rate, evidence completeness rate, "
            "policy compliance rate, and repeat-dispute incidence.",
        ),
        (
            "Practical value",
            "This project helps payments, risk, and product teams pressure-test workflows before production rollout, "
            "standardize dispute playbooks, and improve evidence quality for negotiation or representment.",
        ),
    ]

    for heading, text in sections:
        story.append(Paragraph(heading, h_style))
        story.append(Paragraph(text, body))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Generated: 2026-07-06", body))

    doc.build(story)


if __name__ == "__main__":
    out = Path("output") / "2026-07-06-application-narrative.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(out)
    print(f"Created {out}")
