#!/usr/bin/env python3
"""
Dispute Detection Engine
Analyzes chatbot sessions to identify early dispute signals and predict chargebacks.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

class DisputeDetectionEngine:
    """Analyzes chat sessions for early dispute indicators."""
    
    def __init__(self):
        """Initialize detection patterns and weights."""
        # Keywords and patterns for dispute signals
        self.signals = {
            "unrecognized_transaction": {
                "patterns": [
                    r"don't recognize", r"didn't order", r"unauthorized",
                    r"not me", r"never authorized", r"no recognition",
                    r"didn't purchase", r"not familiar"
                ],
                "weight": 0.25,
                "severity": "high"
            },
            "refund_request": {
                "patterns": [
                    r"refund", r"money back", r"return", r"reimburs",
                    r"credit", r"reverse charge", r"get my money"
                ],
                "weight": 0.20,
                "severity": "high"
            },
            "item_not_received": {
                "patterns": [
                    r"didn't receive", r"no delivery", r"not delivered",
                    r"where is my", r"haven't got", r"missing package",
                    r"item never arrived", r"tracking shows", r"lost"
                ],
                "weight": 0.20,
                "severity": "high"
            },
            "quality_complaint": {
                "patterns": [
                    r"wrong item", r"damaged", r"broken", r"defective",
                    r"poor quality", r"not as described", r"fake",
                    r"counterfeit", r"wrong size", r"not working"
                ],
                "weight": 0.15,
                "severity": "medium"
            },
            "duplicate_charge": {
                "patterns": [
                    r"charged twice", r"double charge", r"duplicate",
                    r"multiple charges", r"extra charge", r"charged again"
                ],
                "weight": 0.18,
                "severity": "high"
            },
            "merchant_mismatch": {
                "patterns": [
                    r"charge from", r"who is", r"don't recognize the name",
                    r"weird charge", r"strange merchant", r"unfamiliar merchant"
                ],
                "weight": 0.15,
                "severity": "medium"
            },
            "frustration_escalation": {
                "patterns": [
                    r"upset", r"angry", r"frustrated", r"ridiculous",
                    r"unacceptable", r"terrible", r"worst", r"never again",
                    r"chargeback", r"dispute", r"report this"
                ],
                "weight": 0.15,
                "severity": "high"
            },
            "urgent_tone": {
                "patterns": [
                    r"asap", r"urgent", r"immediately", r"hurry",
                    r"now", r"emergency", r"quick", r"fast",
                    r"!!!", r"\?\?\?", r"HELP"
                ],
                "weight": 0.10,
                "severity": "medium"
            }
        }
    
    def analyze_session(self, session_text, case_id="UNKNOWN"):
        """Analyze a chat session for dispute indicators."""
        session_lower = session_text.lower()
        
        detected_signals = []
        risk_score = 0.0
        signal_count = 0
        
        for signal_name, signal_config in self.signals.items():
            for pattern in signal_config["patterns"]:
                if re.search(pattern, session_lower):
                    detected_signals.append({
                        "signal": signal_name,
                        "weight": signal_config["weight"],
                        "severity": signal_config["severity"],
                        "pattern_matched": pattern
                    })
                    risk_score += signal_config["weight"]
                    signal_count += 1
                    break  # Count each signal type only once per session
        
        # Normalize risk score (cap at 0.95)
        risk_score = min(risk_score / (len(self.signals) * 0.25), 0.95)
        
        # Calculate multiplier based on frustration level
        frustration_count = sum(1 for s in detected_signals if s["severity"] == "high")
        if frustration_count >= 3:
            risk_score = min(risk_score * 1.2, 0.95)
        
        return {
            "case_id": case_id,
            "risk_score": round(risk_score, 3),
            "signal_count": signal_count,
            "signals_detected": detected_signals,
            "risk_level": self._classify_risk(risk_score),
            "recommendation": self._get_recommendation(risk_score, frustration_count)
        }
    
    def _classify_risk(self, score):
        """Classify risk level based on score."""
        if score >= 0.7:
            return "[CRITICAL] CRITICAL"
        elif score >= 0.5:
            return "[HIGH] HIGH"
        elif score >= 0.3:
            return "[MEDIUM] MEDIUM"
        else:
            return "[LOW] LOW"
    
    def _get_recommendation(self, score, frustration_count):
        """Get action recommendation based on risk analysis."""
        if score >= 0.7:
            return "IMMEDIATE ACTION: Proactive customer contact, offer resolution, flag for monitoring"
        elif score >= 0.5:
            return "HIGH PRIORITY: Review case, prepare evidence package, monitor for chargeback"
        elif score >= 0.3:
            return "MONITOR: Track for escalation, ensure timely responses"
        else:
            return "STANDARD: Routine handling, document interactions"

def scan_evidence_sessions():
    """Scan evidence/ folder for chat session files."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    evidence_dir = os.path.join(BASE_DIR, "evidence")
    
    sessions = {}
    
    if not os.path.exists(evidence_dir):
        return sessions
    
    for case_folder in os.listdir(evidence_dir):
        case_path = os.path.join(evidence_dir, case_folder)
        if not os.path.isdir(case_path):
            continue
        
        # Look for chat files
        for file in os.listdir(case_path):
            if 'chat' in file.lower() and file.endswith('.txt'):
                file_path = os.path.join(case_path, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        sessions[case_folder] = {
                            "path": file_path,
                            "content": content,
                            "filename": file
                        }
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return sessions

def generate_analysis_report(analysis_results):
    """Generate HTML report of dispute detection analysis."""
    sorted_results = sorted(analysis_results, key=lambda x: x["risk_score"], reverse=True)
    
    critical_count = sum(1 for r in analysis_results if "CRITICAL" in r["risk_level"])
    high_count = sum(1 for r in analysis_results if "HIGH" in r["risk_level"])
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Early Dispute Detection Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        
        h1 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.2em;
        }}
        
        .alert-banner {{
            background: #fef3c7;
            border-left: 5px solid #f59e0b;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            font-size: 0.95em;
            line-height: 1.6;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        
        .stat-box {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .stat-box.critical .stat-value {{
            color: #dc2626;
        }}
        
        .stat-box.high .stat-value {{
            color: #f59e0b;
        }}
        
        .case-card {{
            background: white;
            margin-bottom: 20px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 5px solid #ddd;
            transition: all 0.2s;
        }}
        
        .case-card:hover {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }}
        
        .case-card.critical {{
            border-left-color: #dc2626;
            background: #fef2f2;
        }}
        
        .case-card.high {{
            border-left-color: #f59e0b;
            background: #fffbf0;
        }}
        
        .case-header {{
            padding: 20px;
            border-bottom: 1px solid #e5e7eb;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .case-id {{
            font-weight: bold;
            font-size: 1.1em;
            color: #333;
        }}
        
        .risk-score {{
            font-size: 1.8em;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 8px;
            background: #f3f4f6;
        }}
        
        .risk-score.critical {{
            background: #fee2e2;
            color: #dc2626;
        }}
        
        .risk-score.high {{
            background: #fef3c7;
            color: #f59e0b;
        }}
        
        .risk-score.medium {{
            background: #dbeafe;
            color: #2563eb;
        }}
        
        .risk-level {{
            font-weight: bold;
            font-size: 1em;
        }}
        
        .case-body {{
            padding: 20px;
        }}
        
        .signals-list {{
            margin-bottom: 15px;
        }}
        
        .signals-list h4 {{
            color: #667eea;
            margin-bottom: 10px;
            font-size: 0.95em;
        }}
        
        .signal-item {{
            background: #f9fafb;
            padding: 8px 12px;
            margin-bottom: 8px;
            border-radius: 5px;
            font-size: 0.9em;
            border-left: 3px solid #ddd;
        }}
        
        .signal-item.high {{
            border-left-color: #dc2626;
            background: #fef2f2;
        }}
        
        .signal-item.medium {{
            border-left-color: #f59e0b;
            background: #fffbf0;
        }}
        
        .signal-name {{
            font-weight: 600;
            color: #333;
            margin-bottom: 3px;
        }}
        
        .signal-pattern {{
            color: #666;
            font-size: 0.85em;
            font-style: italic;
        }}
        
        .recommendation {{
            background: #eff6ff;
            border-left: 4px solid #2563eb;
            padding: 12px;
            border-radius: 5px;
            margin-top: 10px;
            font-size: 0.9em;
            color: #1e40af;
            font-weight: 500;
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            font-size: 0.9em;
        }}
        
        .priority-badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
            margin-left: 10px;
        }}
        
        .priority-badge.critical {{
            background: #dc2626;
            color: white;
        }}
        
        .priority-badge.high {{
            background: #f59e0b;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .case-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>[ALERT] Early Dispute Detection Report</h1>
            <p style="color: #666; margin-top: 5px;">Chatbot Session Analysis for Chargeback Risk</p>
            <p style="color: #999; font-size: 0.9em; margin-top: 10px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </header>
        
        <div class="alert-banner">
            <strong>[STATS] Summary:</strong> Analyzed {len(analysis_results)} chatbot session(s).
            Found <strong>{critical_count} CRITICAL</strong> and <strong>{high_count} HIGH RISK</strong> cases.
            Immediate attention recommended for flagged cases.
        </div>
        
        <div class="stats-grid">
            <div class="stat-box critical">
                <div class="stat-value">{critical_count}</div>
                <div class="stat-label">CRITICAL Risk</div>
            </div>
            <div class="stat-box high">
                <div class="stat-value">{high_count}</div>
                <div class="stat-label">HIGH Risk</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{len(analysis_results)}</div>
                <div class="stat-label">[INFO] Total Analyzed</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{sum(r['signal_count'] for r in analysis_results) // len(analysis_results) if analysis_results else 0}</div>
                <div class="stat-label">[WARNING] Avg Signals/Case</div>
            </div>
        </div>
        
        <h2 style="color: #333; margin: 30px 0 20px 0; font-size: 1.5em;">Detailed Case Analysis</h2>
        
"""
    
    for result in sorted_results:
        risk_level_text = result["risk_level"].split()[1].lower()
        risk_class = risk_level_text.replace("critical", "critical").replace("high", "high").replace("medium", "medium").replace("low", "low")
        
        signals_html = ""
        for signal in result["signals_detected"]:
            signal_class = "high" if signal["severity"] == "high" else "medium"
            signals_html += f"""
            <div class="signal-item {signal_class}">
                <div class="signal-name">{signal['signal'].replace('_', ' ').title()}</div>
                <div class="signal-pattern">Pattern: "{signal['pattern_matched']}"</div>
            </div>
            """
        
        priority_class = "critical" if "CRITICAL" in result["risk_level"] else "high" if "HIGH" in result["risk_level"] else ""
        priority_badge = f'<span class="priority-badge {priority_class}">PRIORITY</span>' if priority_class else ""
        
        html += f"""
        <div class="case-card {priority_class}">
            <div class="case-header">
                <div>
                    <div class="case-id">{result['case_id']}{priority_badge}</div>
                    <div style="font-size: 0.9em; color: #666; margin-top: 5px;">{result['signal_count']} signals detected</div>
                </div>
                <div class="risk-score {priority_class}">{result['risk_score']:.1%}</div>
            </div>
            <div class="case-body">
                <div style="margin-bottom: 15px;">
                    <strong>Risk Level:</strong> {result['risk_level']}
                </div>
                <div class="signals-list">
                    <h4>[WARNING] Detected Signals ({result['signal_count']}):</h4>
                    {signals_html}
                </div>
                <div class="recommendation">
                    <strong>[OK] Recommended Action:</strong><br>
                    {result['recommendation']}
                </div>
            </div>
        </div>
        """
    
    html += """
        <footer>
            <p>[INFO] Use this report to prioritize case reviews and take proactive measures to prevent chargebacks.</p>
        </footer>
    </div>
</body>
</html>
"""
    
    return html

def main():
    """Main execution."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    
    print("[*] Scanning evidence folder for chatbot sessions...")
    sessions = scan_evidence_sessions()
    
    if not sessions:
        print("[WARNING] No chatbot session files found in evidence/ folder.")
        print("Place chat session files named 'chat_*.txt' in evidence/CASEID/ folders.")
        return
    
    print(f"[OK] Found {len(sessions)} chatbot session(s)")
    
    # Analyze sessions
    print("[*] Analyzing sessions for early dispute signals...")
    engine = DisputeDetectionEngine()
    analysis_results = []
    
    for case_id, session_data in sessions.items():
        result = engine.analyze_session(session_data["content"], case_id)
        analysis_results.append(result)
        
        # Print summary
        risk_label = "[CRITICAL]" if "CRITICAL" in result["risk_level"] else "[HIGH]" if "HIGH" in result["risk_level"] else "[MEDIUM]" if "MEDIUM" in result["risk_level"] else "[LOW]"
        print(f"  {risk_label} {case_id}: Risk {result['risk_score']:.1%} ({result['signal_count']} signals)")
    
    # Generate report
    print("[*] Generating detection report...")
    html = generate_analysis_report(analysis_results)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    report_file = os.path.join(OUTPUT_DIR, "early_dispute_detection.html")
    
    with open(report_file, 'w') as f:
        f.write(html)
    
    print(f"[OK] Report saved: {report_file}")
    
    # Also save JSON results
    json_file = os.path.join(OUTPUT_DIR, "dispute_detection_results.json")
    with open(json_file, 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    print(f"[OK] JSON results saved: {json_file}")

if __name__ == "__main__":
    main()
