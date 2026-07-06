# 🎯 Quick Reference: Early Dispute Detection System

## Commands

```bash
# Generate sample Excel dataset
python scripts/generate_chargeback_dataset.py

# Analyze chat sessions for disputes
python scripts/early_dispute_detection.py

# Run everything at once
python scripts/run_analysis.py
```

---

## File Structure

```
input: evidence/CASEID/chat_CASEID.txt
       ↓
[Early Dispute Detection Engine]
       ↓
output: output/early_dispute_detection.html
        output/dispute_detection_results.json
```

---

## Risk Score Interpretation

| Score | Level | Action | Timeframe |
|-------|-------|--------|-----------|
| 0.7-1.0 | 🔴 CRITICAL | Contact customer immediately | 24 hours |
| 0.5-0.7 | 🟠 HIGH | Priority review | 48 hours |
| 0.3-0.5 | 🟡 MEDIUM | Monitor | 1 week |
| 0.0-0.3 | 🟢 LOW | Standard process | Normal SLA |

---

## Detection Signals & Weights

```python
{
    "unrecognized_transaction": 0.25,    # Highest priority
    "refund_request": 0.20,
    "item_not_received": 0.20,
    "duplicate_charge": 0.18,
    "merchant_mismatch": 0.15,
    "quality_complaint": 0.15,
    "frustration_escalation": 0.15,
    "urgent_tone": 0.10
}
```

---

## Chat File Format

**Location:** `evidence/CASEID/chat_CASEID.txt`

**Content:** Plain text conversation

```
Customer: I don't recognize this charge from TechStore
Support: I can help you with that. Can you provide the transaction date?
Customer: It's from June 1st, $134.50. I never authorized this.
Support: Let me investigate...
```

---

## Sample Excel Data Columns

- Case ID
- Transaction Date
- Complaint Date
- Days to Complaint
- Merchant
- Amount
- Currency
- Reason Code
- Reason Description
- Card Network
- Status
- **Dispute Risk Score** ← AI-generated
- Early Signals Detected
- Friendly Fraud Indicator
- Has Refund Request
- Shipping Address Match
- AVS Result
- Notes

---

## Output Files Explained

| File | Purpose | Format | Use Case |
|------|---------|--------|----------|
| `chargeback_records.xlsx` | Master dataset | Excel | Track all chargebacks |
| `early_dispute_detection.html` | Risk report | Interactive HTML | Review risk analysis |
| `dispute_detection_results.json` | Raw analysis | JSON | Integration, automation |
| `ANALYSIS_SUMMARY.md` | Execution summary | Markdown | Quick overview |

---

## Adding Your Chat Data

1. Create folder: `evidence/CASE123/`
2. Add file: `chat_CASE123.txt`
3. Add chat content: Customer-support conversation
4. Run: `python scripts/early_dispute_detection.py`
5. Review: `output/early_dispute_detection.html`

---

## Customizing Detection

Edit `scripts/early_dispute_detection.py`:

### Change Signal Weight
```python
"refund_request": {
    "weight": 0.20,  # Increase from 0.20 to 0.25
    "severity": "high"
}
```

### Add Pattern
```python
"refund_request": {
    "patterns": [
        r"refund",
        r"money back",
        r"return",
        r"my complaint",  # NEW
    ]
}
```

### Adjust Risk Thresholds
```python
if score >= 0.65:  # Changed from 0.70
    return "🔴 CRITICAL"
elif score >= 0.45:  # Changed from 0.50
    return "🟠 HIGH"
```

---

## Integration Examples

### Access JSON Results
```python
import json

with open('output/dispute_detection_results.json', 'r') as f:
    results = json.load(f)
    for case in results:
        print(f"{case['case_id']}: {case['risk_score']:.0%}")
```

### Export to Database
```python
import json
import sqlite3

conn = sqlite3.connect('disputes.db')
with open('output/dispute_detection_results.json') as f:
    for case in json.load(f):
        conn.execute(
            'INSERT INTO disputes VALUES (?, ?, ?)',
            (case['case_id'], case['risk_score'], case['risk_level'])
        )
```

### Send Alert
```python
results = json.load(open('output/dispute_detection_results.json'))
critical = [r for r in results if 'CRITICAL' in r['risk_level']]
if critical:
    # Send email or Slack alert
    send_alert(f"⚠️  {len(critical)} critical cases detected!")
```

---

## Performance

| Metric | Value |
|--------|-------|
| Analysis speed | ~10 cases/second |
| Memory usage | <50MB |
| Output size | 100KB HTML + 50KB JSON |
| Supported chat length | Unlimited |

---

## Scheduling (Windows)

### Task Scheduler
```
Name: DisputeAnalysis
Trigger: Daily at 09:00
Action: python scripts/run_analysis.py
Repeat: Every 1 day indefinitely
```

### PowerShell
```powershell
$trigger = New-JobTrigger -Daily -At "09:00"
Register-ScheduledJob -Name "DisputeAnalysis" `
  -ScriptBlock { cd "path\to\project"; python scripts/run_analysis.py } `
  -Trigger $trigger
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Python not found` | Install from python.org, add to PATH |
| `openpyxl not installed` | Run: `pip install openpyxl` |
| `No results` | Check `evidence/CASEID/chat_*.txt` format |
| `Empty Excel file` | Run: `python scripts/generate_chargeback_dataset.py` |
| `Risk scores too low` | Adjust signal weights in early_dispute_detection.py |

---

## Success Criteria

✅ System is working well when:
- Early detection catches 60%+ of disputes before chargeback
- False positive rate <20%
- Teams act on recommendations within 24h
- Prevention costs <50% of average chargeback fee

---

## Support Files

- 📖 `SYSTEM_GUIDE.md` — Detailed documentation
- 🎯 `SYSTEM_SETUP_GUIDE.html` — Interactive setup guide  
- 📋 `workflows/research.md` — Investigation procedures
- 📝 `resources/report-template.md` — Report template

---

**Created:** 2026-06-24 | **Version:** 1.0 | **Status:** Ready to Use
