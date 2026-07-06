from pathlib import Path
import struct
from fpdf import FPDF

out = Path(r"c:\Users\suman\Documents\Dispute & Chargeback Management Agent\output\TOOL_OVERVIEW.pdf")
out.parent.mkdir(parents=True, exist_ok=True)

screenshot_dir = Path(r"c:\Users\suman\Documents\Dispute & Chargeback Management Agent\output\screenshots")
output_dir = Path(r"c:\Users\suman\Documents\Dispute & Chargeback Management Agent\output")

pdf = FPDF(orientation="L", format="A4")
pdf.set_auto_page_break(auto=True, margin=15)

THEME_PRIMARY = (34, 49, 63)
THEME_ACCENT = (31, 111, 235)
THEME_SOFT_BG = (245, 247, 250)
THEME_TEXT = (34, 34, 34)
MARGIN_X = 10
CONTENT_W = pdf.w - (MARGIN_X * 2)
PAGE_BOTTOM_Y = pdf.h - 15


def ensure_space(required_height: float, subtitle: str = "Dashboard Highlights") -> None:
    if pdf.get_y() + required_height > PAGE_BOTTOM_Y:
        add_header("Early Dispute Detection & Chargeback Management Tool", subtitle)


def estimate_wrapped_lines(text: str, width: float) -> int:
    words = text.split()
    if not words:
        return 1

    lines = 1
    current = words[0]
    for word in words[1:]:
        trial = f"{current} {word}"
        if pdf.get_string_width(trial) <= width:
            current = trial
        else:
            lines += 1
            current = word
    return lines


def estimate_section_height(bullets: list[str]) -> float:
    # Section band + spacing + bullet content + small padding.
    total = 11
    for bullet in bullets:
        lines = estimate_wrapped_lines(f"- {bullet}", CONTENT_W - 4)
        total += lines * 6
    return total + 2


def add_section_title(title: str) -> None:
    ensure_space(11, "Dashboard Highlights")
    pdf.set_fill_color(*THEME_SOFT_BG)
    pdf.set_draw_color(220, 226, 232)
    pdf.rect(MARGIN_X, pdf.get_y(), CONTENT_W, 10, style="DF")
    pdf.set_xy(MARGIN_X + 2, pdf.get_y() + 2)
    pdf.set_text_color(*THEME_ACCENT)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 6, title)
    pdf.ln(9)


def add_header(title: str, subtitle: str) -> None:
    pdf.add_page()
    pdf.set_fill_color(*THEME_PRIMARY)
    pdf.rect(0, 0, pdf.w, 28, style="F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_xy(MARGIN_X, 8)
    pdf.cell(0, 8, title)
    pdf.set_font("Helvetica", size=10)
    pdf.set_xy(MARGIN_X, 18)
    pdf.cell(0, 6, subtitle)
    pdf.set_text_color(*THEME_TEXT)
    pdf.ln(24)


def add_section(title: str, bullets: list[str]) -> None:
    ensure_space(estimate_section_height(bullets), "Dashboard Highlights")
    add_section_title(title)

    pdf.set_text_color(*THEME_TEXT)
    pdf.set_font("Helvetica", size=11)
    for bullet in bullets:
        line_count = estimate_wrapped_lines(f"- {bullet}", CONTENT_W - 4)
        required_h = (line_count * 6) + 1
        if pdf.get_y() + required_h > PAGE_BOTTOM_Y:
            add_header("Early Dispute Detection & Chargeback Management Tool", f"{title} (cont.)")
            add_section_title(f"{title} (cont.)")
            pdf.set_text_color(*THEME_TEXT)
            pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(CONTENT_W - 4, 6, f"- {bullet}")
    pdf.ln(1)


def add_image_section(title: str, image_path: Path, caption: str) -> None:
    if not image_path.exists():
        return

    def get_png_dimensions(path: Path):
        with path.open("rb") as f:
            header = f.read(24)
        if len(header) < 24 or header[0:8] != b"\x89PNG\r\n\x1a\n":
            return None
        width, height = struct.unpack(">II", header[16:24])
        if width <= 0 or height <= 0:
            return None
        return width, height

    dims = get_png_dimensions(image_path)
    max_w = CONTENT_W - 4
    max_h = 130

    if not dims:
        draw_w, draw_h = max_w, 78
    else:
        img_w, img_h = dims
        img_ratio = img_w / img_h
        box_ratio = max_w / max_h
        if img_ratio >= box_ratio:
            draw_w = max_w
            draw_h = max_w / img_ratio
        else:
            draw_h = max_h
            draw_w = max_h * img_ratio

    ensure_space(estimate_section_height([caption]) + 20, "Dashboard Screenshots")
    add_section(title, [caption])
    y = pdf.get_y()

    # Recompute available space after caption to guarantee full visibility.
    available_h = PAGE_BOTTOM_Y - y - 4
    if available_h <= 20:
        add_header("Early Dispute Detection & Chargeback Management Tool", "Dashboard Screenshots")
        add_section(title, [caption])
        y = pdf.get_y()
        available_h = PAGE_BOTTOM_Y - y - 4

    max_h = min(max_h, available_h)
    if dims:
        img_w, img_h = dims
        img_ratio = img_w / img_h
        box_ratio = max_w / max_h
        if img_ratio >= box_ratio:
            draw_w = max_w
            draw_h = max_w / img_ratio
        else:
            draw_h = max_h
            draw_w = max_h * img_ratio
    else:
        draw_w = max_w
        draw_h = max_h

    x = (MARGIN_X + 2) + (max_w - draw_w) / 2
    pdf.image(str(image_path), x=x, y=y, w=draw_w, h=draw_h)
    pdf.set_y(y + draw_h)
    pdf.ln(4)


add_header(
    "Early Dispute Detection & Chargeback Management Tool",
    "Generated: 2026-07-01",
)

sections = [
    (
        "What This Tool Does",
        [
            "Detects dispute signals before formal chargeback filing.",
            "Scores case risk to prioritize operational action.",
            "Supports customer and merchant AI-assisted live chat negotiation.",
            "Separates disputes from official chargebacks.",
            "Enables evidence prompts and automatic closure when both parties agree.",
        ],
    ),
    (
        "Core System Components",
        [
            "Data generation layer: structured chargeback records with reason-code fields.",
            "Detection layer: chat and evidence signal extraction with weighted risk scoring.",
            "Resolution layer: role-specific customer and merchant workflows.",
            "Governance layer: intervention controls, policy checks, and escalation actions.",
            "Reporting layer: operational dashboards and integration-ready output files.",
        ],
    ),
    (
        "Function Overview (Scripts)",
        [
            "generate_chargeback_dataset.py: creates normalized sample case data for reporting and QA.",
            "early_dispute_detection.py: detects early dispute indicators and computes risk classifications.",
            "run_analysis.py: orchestrates full execution and regenerates all downstream deliverables.",
            "create_tool_overview_pdf.py: produces this stakeholder-ready summary PDF.",
            "create_tool_presentation.py: builds the presentation with visuals and speaker notes.",
        ],
    ),
    (
        "Dispute vs Chargeback Lifecycle",
        [
            "Dispute stage: customer or merchant can initiate, negotiate with notes/evidence/amount, and track accept/reject outcomes.",
            "Chargeback stage: official network-level filing with reason-code validation, evidence arbitration, and final won/lost outcomes.",
            "Lifecycle separation improves ownership clarity and reduces operational delays.",
        ],
    ),
    (
        "Risk and Detection Logic",
        [
            "Risk tiers: Critical, High, Medium, Low.",
            "Signal weighting from conversation patterns and evidence context.",
            "Reason-code-aware triage supports faster and more consistent routing.",
            "High-risk alerts enable proactive outreach and faster intervention.",
        ],
    ),
    (
        "Dashboards and User Views",
        [
            "Customer Resolution Center: active chat, evidence prompts, and settlement response.",
            "Merchant Resolution Center: live evidence exchange and representment readiness.",
            "Merchant Admin Dashboard: intervention queue, risk segmentation, and policy oversight.",
            "Disputes and chargebacks are separated to preserve lifecycle clarity.",
            "Visual analytics track risk distribution, case aging, and exposure by status.",
        ],
    ),
    (
        "Workflow Interpretation",
        [
            "Input context is captured from customer-support conversations and evidence artifacts.",
            "Signals are matched once per category to reduce duplicate inflation.",
            "Weighted scoring determines priority bands for operational action.",
            "Risk levels map directly to response urgency and ownership.",
            "AI prompt chips guide evidence collection and confirmation in live chat.",
            "Cases auto-close when both parties explicitly agree in the chat flow.",
            "Outputs support both daily operations and system integration.",
        ],
    ),
    (
        "Outputs and Deliverables",
        [
            "Excel dataset for case operations and audits.",
            "Interactive HTML dashboards for daily workflows.",
            "JSON output for downstream system integration.",
            "Markdown summary for run-level insights.",
            "Export-ready reporting for stakeholders.",
        ],
    ),
    (
        "Intervention Workflow",
        [
            "Request evidence.",
            "Escalate to network review.",
            "Mark chargeback won.",
            "Mark chargeback lost.",
            "Track status and rationale for compliance.",
        ],
    ),
    (
        "Business Value",
        [
            "Lower chargeback losses via earlier detection.",
            "Faster response through risk-based prioritization.",
            "Clear accountability across customer, merchant, and operations teams.",
            "Improved audit readiness and policy consistency.",
            "Scalable process for growing dispute volume.",
        ],
    ),
    (
        "Next Steps",
        [
            "Add production reason-code policy mappings.",
            "Integrate with case management and ticketing systems.",
            "Automate daily run scheduling.",
            "Track precision, false positives, and recovery rate.",
            "Refine intervention thresholds by merchant segment.",
        ],
    ),
]

for heading, bullets in sections:
    add_section(heading, bullets)

add_header(
    "Early Dispute Detection & Chargeback Management Tool",
    "Workflow and Application Context",
)

add_image_section(
    "Application Context: Entry and Navigation",
    screenshot_dir / "index.png",
    "Portal navigation showing role-based entry points and workflow access across dashboards.",
)

add_image_section(
    "Workflow Diagram: Agentic Detection Flow",
    output_dir / "agentic_workflow_diagram.png",
    "End-to-end detection flow from chat input through signal extraction, scoring, risk classification, and outputs.",
)

add_image_section(
    "Workflow Diagram: Agent Loop (LLM + Tools)",
    output_dir / "agent_loop_llm_tools_workflow.png",
    "LLM planner, tool router, policy-confidence gate, human-review fallback, and closed-loop case state updates.",
)

add_image_section(
    "Merchant Admin Dashboard",
    screenshot_dir / "merchant_dashboard.png",
    "Merchant risk drilldown, case workflow controls, evidence readiness actions, and issuer outcome tracking.",
)
add_image_section(
    "Early Dispute Detection Dashboard",
    screenshot_dir / "early_dispute_detection.png",
    "Risk-ranked early warning view based on chat and evidence signals.",
)
add_image_section(
    "Customer Resolution Center",
    screenshot_dir / "resolution_center_customer.png",
    "Customer-side live chat negotiation, evidence prompts, and agreement-based closure controls.",
)
add_image_section(
    "Merchant Resolution Center",
    screenshot_dir / "resolution_center_merchant.png",
    "Merchant-side live chat response controls, evidence exchange, and mutual-agreement closure progression.",
)
add_image_section(
    "System Portal",
    screenshot_dir / "index.png",
    "Central entry point to all generated dashboards and views.",
)

pdf.output(str(out))
print(out)
