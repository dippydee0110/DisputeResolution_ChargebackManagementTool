# 📊 Dispute & Chargeback Analysis System
## Early Detection, Risk Scoring & Chatbot Integration

**Created:** 2026-06-24  
**Purpose:** Identify potential chargebacks from customer chatbot sessions before they happen

---

## 🎯 Overview

This system provides three core capabilities:

1. **Chargeback Dataset (Excel)** — Centralized tracking of all disputes with risk scoring
2. **Early Dispute Detection** — AI analysis of chatbot sessions to identify warning signs
3. **Interactive Reporting** — Visual dashboards and actionable recommendations

---

## 🚀 Quick Start

### Installation

No special installation needed! The system uses:
- **Python 3.6+** (already on most systems)
- **openpyxl** library (auto-installed if missing)

### One-Command Setup

Run this once to generate everything:

```bash
cd "c:\Users\suman\Documents\Dispute & Chargeback Management Agent"
python scripts/run_analysis.py
```

Or run individual components:

```bash
# Generate sample Excel data
python scripts/generate_chargeback_dataset.py

# Analyze chat sessions for disputes
python scripts/early_dispute_detection.py
```

---

## 📁 Project Structure

```
Dispute & Chargeback Management Agent/
├── scripts/
│   ├── generate_chargeback_dataset.py    ← Creates Excel data
│   ├── early_dispute_detection.py        ← AI analysis engine
│   ├── run_analysis.py                   ← Master runner
│   └── bundle_evidence.py                ← Evidence packaging
├── evidence/
│   ├── CASE123/
│   │   ├── chat_CASE123.txt              ← Chat transcripts
│   │   └── tracking_CASE123.json
│   └── CASE124/
│       └── chat_CASE124.txt
├── output/
│   ├── chargeback_records.xlsx           ← Main dataset
│   ├── early_dispute_detection.html      ← Visual report
│   ├── dispute_detection_results.json    ← Raw data
│   └── ANALYSIS_SUMMARY.md               ← This file
└── workflows/
    └── research.md                       ← Investigation workflows
```

---

## 📊 Component 1: Chargeback Dataset (Excel)

### What It Does
- Generates or organizes all your chargeback records in one place
- Calculates risk scores automatically
- Tracks case status, merchant, amounts, reason codes

### File Location
`output/chargeback_records.xlsx`

### Data Included Per Record
- Case ID
- Transaction Date & Complaint Date
- Days to Complaint (time lag)
- Merchant name
- Amount & Currency
- Card Network & Reason Code
- Status (Opened, Investigating, Representment Ready, Escalated)
- **Dispute Risk Score** (0.0-1.0, color-coded)
- Early Signals Detected (count)
- Friendly Fraud Indicator (Yes/No/Maybe)
- Refund Request, Shipping Match, AVS Result
- Notes/Observations

### How to Use
1. Open `output/chargeback_records.xlsx` in Excel
2. Replace sample data with your actual chargebacks
3. Update status as you progress on cases
4. Risk scores help prioritize which cases need immediate attention

### Customizing
Edit `generate_chargeback_dataset.py` to:
- Change merchant names
- Add more fields
- Adjust sample data

---

## 🧠 Component 2: Early Dispute Detection Engine

### What It Does
- Analyzes customer chatbot conversations
- Detects 8 types of early warning signals
- Assigns risk score to each case
- Provides specific action recommendations

### How It Works

#### Data Input
Place customer chat transcripts in your evidence folders:

```
evidence/
  CASE123/
    chat_CASE123.txt
  CASE124/
    chat_CASE124.txt
```

Format: Plain text files with customer-support conversations.

#### Detection Signals

The AI flags these patterns as potential dispute indicators:

| Signal | Severity | Weight | Example |
|--------|----------|--------|---------|
| **Unrecognized Transaction** | 🔴 High | 25% | "I don't recognize this charge" |
| **Refund Request** | 🔴 High | 20% | "I want my money back" |
| **Item Not Received** | 🔴 High | 20% | "Package never arrived" |
| **Duplicate Charge** | 🔴 High | 18% | "Why was I charged twice?" |
| **Merchant Mismatch** | 🟠 Medium | 15% | "Who is this merchant?" |
| **Quality Complaint** | 🟠 Medium | 15% | "This is damaged/fake" |
| **Frustration** | 🟠 Medium | 15% | "This is unacceptable!" |
| **Urgency** | 🟠 Medium | 10% | "HELP! URGENT!" |

#### Risk Score Calculation
- Signals are weighted and summed
- Higher severity signals contribute more
- Score normalized to 0.0-1.0 range
- Multiplier applied if 3+ high-severity signals detected

#### Output Files
- `output/early_dispute_detection.html` — Interactive dashboard
- `output/dispute_detection_results.json` — Machine-readable results

---

## 📈 Component 3: Interactive Dashboard

### What It Shows
- Cases ranked by risk level
- Detected signals per case
- Risk score visualization
- Action recommendations
- Case details table

### Risk Levels
- 🔴 **CRITICAL** (70%+) — Immediate action needed
- 🟠 **HIGH** (50-70%) — Priority review
- 🟡 **MEDIUM** (30-50%) — Monitor
- 🟢 **LOW** (0-30%) — Standard handling

### Recommended Actions by Risk Level

**🔴 CRITICAL Cases:**
1. Contact customer within 24 hours
2. Offer proactive resolution (refund/reshipment)
3. Gather complete evidence immediately
4. Prepare representment package
5. Monitor for chargeback filing

**🟠 HIGH Cases:**
1. Review case within 48 hours
2. Gather evidence (tracking, comms, etc.)
3. Prepare for representment
4. Follow up on any pending information

**🟡 MEDIUM Cases:**
1. Routine investigation
2. Respond to customer within SLA
3. Document all interactions

**🟢 LOW Cases:**
1. Standard customer service response
2. Continue normal process

---

## 💻 Running the System

### Option 1: Complete Analysis (Recommended)
```bash
python scripts/run_analysis.py
```

Generates:
- ✅ chargeback_records.xlsx
- ✅ early_dispute_detection.html
- ✅ dispute_detection_results.json
- ✅ ANALYSIS_SUMMARY.md

### Option 2: Generate Excel Data Only
```bash
python scripts/generate_chargeback_dataset.py
```

Output: `output/chargeback_records.xlsx`

### Option 3: Run Dispute Detection Only
```bash
python scripts/early_dispute_detection.py
```

Reads from: `evidence/*/chat_*.txt`  
Output: `output/early_dispute_detection.html`

---

## 📝 Using Your Own Data

### Step 1: Add Chat Sessions
Create folders with your chat transcripts:

```
evidence/
  ACME_001/
    chat_ACME_001.txt
  ACME_002/
    chat_ACME_002.txt
```

**Format:** Plain text with customer-service conversation.

Example:
```
Customer: I don't recognize this charge from TechStore Pro
Support: Can you provide more details?
Customer: I never authorized this. I want my money back ASAP.
Support: Let me look into this for you...
```

### Step 2: Replace Sample Excel Data
1. Open `output/chargeback_records.xlsx`
2. Replace rows with your actual chargeback records
3. Keep the same column structure
4. Save the file

### Step 3: Run Detection
```bash
python scripts/early_dispute_detection.py
```

### Step 4: Review Results
- Open `output/early_dispute_detection.html` in browser
- Review high-risk cases first
- Take recommended actions

---

## 🔄 Automation & Scheduling

### Windows Task Scheduler

Schedule daily analysis:

1. Open Task Scheduler
2. Create new task: "Run Chargeback Analysis"
3. Trigger: Daily at 9:00 AM
4. Action: `python scripts/run_analysis.py`
5. Working directory: Project root

### Manual Scheduling
Run the script regularly (daily/weekly):

```bash
# From PowerShell
$schedule = @{
    RepetitionInterval = (New-TimeSpan -Hours 24)
    RepetitionDuration = (New-TimeSpan -Days 365)
}
Register-ScheduledJob -Name "DisputeAnalysis" -ScriptBlock { 
    cd "c:\Users\suman\Documents\Dispute & Chargeback Management Agent"
    python scripts/run_analysis.py 
} -Trigger (New-JobTrigger -Daily -At "09:00") @schedule
```

---

## 📊 Key Metrics to Track

### Prevention Metrics
- **Early Detection Rate** — % of disputes identified before chargeback filed
- **Resolution Rate** — % of flagged cases resolved proactively
- **Cost Savings** — Prevention cost vs. chargeback fees avoided

### System Metrics
- **False Positive Rate** — Are risk scores accurate?
- **Average Time to Resolution** — For flagged cases
- **Signal Accuracy** — Which signals are most predictive?

### Business Metrics
- Total chargebacks prevented
- Average chargeback amount
- Most common reason codes
- Highest-risk merchants

---

## 🔧 Customization

### Modify Dispute Signals

Edit `scripts/early_dispute_detection.py` in the `signals` dictionary:

```python
"unrecognized_transaction": {
    "patterns": [
        r"don't recognize",
        r"unauthorized",
        # Add more patterns here
    ],
    "weight": 0.25,          # Change weight (0-1)
    "severity": "high"       # high or medium
},
```

### Add Custom Fields

Edit `generate_chargeback_dataset.py` to add columns:

```python
"custom_field": "value",
```

### Change Risk Score Thresholds

In `early_dispute_detection.py`, update risk classification:

```python
if score >= 0.75:  # Changed from 0.70
    return "🔴 CRITICAL"
```

---

## 📖 Examples

### Example 1: New Chargeback Case

**Data:**
```
Case ID: ACME_001
Transaction: $150 from "GizmoStore"
Chat contains: "I never ordered this", "unauthorized", "want refund"
```

**System Output:**
- Detected signals: 2 (unrecognized transaction, refund request)
- Risk score: 0.65 (🟠 HIGH)
- Recommendation: "HIGH PRIORITY: Review case, prepare evidence package"

**Action:** Contact customer within 48 hours, offer solution.

### Example 2: Quality Complaint

**Data:**
```
Case ID: ACME_002
Chat contains: "Item damaged", "poor quality", "not as described"
```

**System Output:**
- Detected signals: 1 (quality complaint)
- Risk score: 0.35 (🟡 MEDIUM)
- Recommendation: "MONITOR: Track for escalation"

**Action:** Standard customer service follow-up.

---

## ⚠️ Important Notes

### Data Privacy
- Keep customer chat data secure
- Don't share HTML reports publicly
- Store JSON results securely

### Accuracy
- System identifies potential disputes, not guarantees
- False positives possible - review each flagged case
- Customize signals based on your experience

### Limitations
- Analysis based on chat text only
- Requires consistent chat format
- Better with longer conversations

---

## 🚀 Next Steps

1. **Try the sample:** Run `python scripts/run_analysis.py` with sample data
2. **Review outputs:** Open the HTML dashboard in your browser
3. **Customize:** Adjust signal weights based on your data
4. **Integrate:** Add your chat sessions to `evidence/` folders
5. **Automate:** Schedule daily/weekly runs
6. **Monitor:** Track which signals are most predictive for your business

---

## 📞 Troubleshooting

### Python not found
- Install Python 3.8+ from python.org
- Add to PATH during installation
- Restart terminal after installing

### openpyxl not installed
- Script auto-installs, but can manually install:
  ```bash
  pip install openpyxl
  ```

### No results generated
- Check file paths in `evidence/` folder
- Ensure chat files end in `.txt`
- Check file has readable content

### Risk scores seem inaccurate
- Review detected signals in JSON output
- Adjust signal weights in early_dispute_detection.py
- Add patterns for signals you're missing

---

## 📚 Related Files

- `workflows/research.md` — Investigation procedures
- `resources/report-template.md` — Case report template
- `scripts/bundle_evidence.py` — Create evidence packages

---

**System Created:** 2026-06-24  
**Last Updated:** 2026-06-24  
**Version:** 1.0
