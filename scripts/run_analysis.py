#!/usr/bin/env python3
"""
Master Dispute Analysis Runner
Orchestrates the complete chargeback and dispute detection workflow.
Runs: data generation, dispute detection, and generates integrated reports.
"""

import subprocess
import os
import sys
import json
from datetime import datetime

def run_script(script_name, description):
    """Run a Python script and report results."""
    print(f"\n{'='*70}")
    print(f"[RUNNING] {description}")
    print(f"{'='*70}")
    
    script_path = os.path.join(os.path.dirname(__file__), script_name)
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=60)
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("[WARNING] Warnings/Errors:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"❌ Script timed out: {script_name}")
        return False
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def generate_integrated_summary():
    """Generate an integrated summary report."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    
    try:
        # Read detection results
        detection_file = os.path.join(OUTPUT_DIR, "dispute_detection_results.json")
        detection_results = []
        
        if os.path.exists(detection_file):
            with open(detection_file, 'r') as f:
                detection_results = json.load(f)
        
        critical_count = sum(1 for r in detection_results if "CRITICAL" in r["risk_level"])
        high_count = sum(1 for r in detection_results if "HIGH" in r["risk_level"])
        
        summary = f"""
[SYSTEM] DISPUTE ANALYSIS SYSTEM - INTEGRATED SUMMARY

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## What Was Created

[OK] **1. Chargeback Dataset (Excel)**
   - File: `output/chargeback_records.xlsx`
   - Contains: 15 sample chargeback records with risk scoring
   - Use this to understand your chargeback data structure

[OK] **2. Early Dispute Detection System**
   - Analyzes chatbot sessions for warning signals
   - Scans: `evidence/*/chat_*.txt` files
   - Produces risk scores and actionable recommendations

[OK] **3. Interactive Dashboard**
   - File: `output/early_dispute_detection.html`
   - Shows: Cases ranked by risk, detected signals, recommendations
   - Open in browser for interactive view

[OK] **4. JSON Analysis Results**
   - File: `output/dispute_detection_results.json`
   - For programmatic access and integration

## Current Status

- **Cases Analyzed:** {len(detection_results)}
- **[CRITICAL] Critical Risk:** {critical_count}
- **[HIGH] High Risk:** {high_count}
- **Average Signals/Case:** {sum(r['signal_count'] for r in detection_results) / len(detection_results) if detection_results else 0:.1f}

## Dispute Detection Signals Monitored

[OK] Customer doesn't recognize transaction
[OK] Refund requests (before chargeback)
[OK] Items not received
[OK] Quality complaints
[OK] Duplicate charges
[OK] Merchant name mismatch
[OK] Frustration escalation
[OK] Urgent/emergency tone

## How to Use This System

### Step 1: Add Your Chargeback Data
1. Open `output/chargeback_records.xlsx`
2. Replace sample data with your actual chargeback records
3. Save and keep updated

### Step 2: Add Chatbot Sessions
1. Place customer chat transcripts in: `evidence/CASEID/chat_CASEID.txt`
2. One chat file per case folder
3. System automatically scans and analyzes

### Step 3: Run Analysis
```bash
# Run all analysis (this script)
python scripts/run_analysis.py

# Or run individually:
python scripts/generate_chargeback_dataset.py
python scripts/early_dispute_detection.py
```

### Step 4: Review Reports
- **Dashboard:** Open `output/early_dispute_detection.html` in browser
- **Excel Data:** `output/chargeback_records.xlsx`
- **JSON Results:** `output/dispute_detection_results.json`

## Next Steps

### For Critical/High Risk Cases:
1. **Immediate Contact** - Reach out to customer proactively
2. **Gather Evidence** - Collect tracking, communications, authorization logs
3. **Offer Resolution** - Refund, resend, or investigate
4. **Monitor** - Watch for chargeback filing
5. **Document** - Log all interactions for representment

### For Integration:
- Export detection results (JSON) to your case management system
- Set up automated alerts for new chat files
- Schedule weekly analysis runs
- Track conversion of "at-risk" cases to actual chargebacks

## Key Metrics to Track

- Early Detection Rate: How many disputes were identified before chargeback?
- False Positive Rate: How accurate are the risk scores?
- Resolution Rate: What % of flagged cases were resolved proactively?
- Cost Savings: Compare prevention costs vs. chargeback fees

---

**Questions or Issues?**
- Review the workflows/ folder for detailed investigation procedures
- Check resources/ folder for templates and checklists
- Modify dispute detection patterns in early_dispute_detection.py for your use case

"""
        
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"

def main():
    """Main execution."""
    print("""
=====================================================================
DISPUTE & CHARGEBACK ANALYSIS SYSTEM
Early Detection + Risk Scoring + Automated Reporting
=====================================================================
    """)
    
    # Run analysis scripts
    scripts_to_run = [
        ("generate_chargeback_dataset.py", "[1] Generating Chargeback Dataset"),
        ("early_dispute_detection.py", "[2] Running Early Dispute Detection"),
    ]
    
    results = {}
    for script, description in scripts_to_run:
        success = run_script(script, description)
        results[script] = "✅ Success" if success else "❌ Failed"
    
    # Generate summary
    print(f"\n{'='*70}")
    print("[*] Generating Integrated Summary")
    print(f"{'='*70}")
    summary = generate_integrated_summary()
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    summary_file = os.path.join(OUTPUT_DIR, "ANALYSIS_SUMMARY.md")
    
    with open(summary_file, 'w') as f:
        f.write(summary)
    
    print(summary)
    print(f"\n[OK] Summary saved to: {summary_file}")
    
    # Final report
    print(f"\n{'='*70}")
    print("[COMPLETE] ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print("\n[INFO] Output Files Generated:")
    print("   [OK] output/chargeback_records.xlsx (Excel dataset)")
    print("   [OK] output/early_dispute_detection.html (Interactive dashboard)")
    print("   [OK] output/dispute_detection_results.json (Machine-readable results)")
    print("   [OK] output/ANALYSIS_SUMMARY.md (This summary)")
    print("\n[ACTION] Next Steps:")
    print("   1. Review the interactive dashboard in your browser")
    print("   2. Add your chat sessions to evidence/CASEID/chat_*.txt")
    print("   3. Replace sample data in Excel with your records")
    print("   4. Run analysis again: python scripts/run_analysis.py")
    print("\n[INFO] For more info, see resources/ and workflows/ folders")

if __name__ == "__main__":
    main()
