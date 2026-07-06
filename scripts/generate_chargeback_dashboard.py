#!/usr/bin/env python3
"""
Generate an interactive HTML dashboard of all chargebacks from evidence folder.
Scans evidence/ for case data and creates visual report with charts.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

# Configuration
EVIDENCE_DIR = "evidence"
OUTPUT_DIR = "output"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

def extract_case_data_from_markdown(case_id, report_path):
    """Extract chargeback data from markdown dispute report."""
    data = {
        "case_id": case_id,
        "amount": 0,
        "currency": "USD",
        "reason_code": "",
        "card_network": "",
        "merchant": "",
        "transaction_date": "",
        "status": "unknown",
        "friendly_fraud_indicator": False,
    }
    
    try:
        with open(report_path, 'r') as f:
            content = f.read()
            
            # Extract amount
            amount_match = re.search(r'Amount[:\s]+([A-Z]{3})\s+([\d,]+\.?\d*)', content)
            if amount_match:
                data["currency"] = amount_match.group(1)
                data["amount"] = float(amount_match.group(2).replace(',', ''))
            
            # Extract reason code and card network
            reason_match = re.search(r'Card network[/\s]+Reason code[:\s]+(\w+)\s+(\d+)\s*\((.*?)\)', content)
            if reason_match:
                data["card_network"] = reason_match.group(1)
                data["reason_code"] = reason_match.group(2)
                reason_desc = reason_match.group(3).lower()
                data["reason_description"] = reason_match.group(3)
                # Flag friendly fraud indicators
                if any(term in reason_desc for term in ["cardholder does not recognize", "fraud", "friendly fraud"]):
                    data["friendly_fraud_indicator"] = True
            
            # Extract merchant
            merchant_match = re.search(r'Merchant[:\s]+(.*?)(?:\n|$)', content)
            if merchant_match:
                data["merchant"] = merchant_match.group(1).strip()
            
            # Extract transaction date
            trans_match = re.search(r'Transaction date[:\s]+(\d{4}-\d{2}-\d{2})', content)
            if trans_match:
                data["transaction_date"] = trans_match.group(1)
            
            # Infer status from executive summary
            if "recommend representment" in content.lower():
                data["status"] = "representment_ready"
            elif "escalate" in content.lower():
                data["status"] = "escalated"
            else:
                data["status"] = "investigating"
                
    except Exception as e:
        print(f"Error reading {report_path}: {e}")
    
    return data

def extract_case_data_from_json(case_id, json_path):
    """Extract additional data from tracking JSON."""
    data = {}
    try:
        with open(json_path, 'r') as f:
            tracking = json.load(f)
            if "delivered_at" in tracking:
                data["delivered_at"] = tracking["delivered_at"]
            if "status" in tracking and "status" not in data:
                data["status"] = tracking["status"]
    except Exception as e:
        print(f"Error reading {json_path}: {e}")
    return data

def scan_evidence_folder():
    """Scan evidence/ folder and extract all case data."""
    cases = []
    evidence_path = os.path.join(BASE_DIR, EVIDENCE_DIR)
    
    if not os.path.exists(evidence_path):
        print(f"Evidence folder not found: {evidence_path}")
        return cases
    
    # Find all case folders
    for case_folder in os.listdir(evidence_path):
        case_path = os.path.join(evidence_path, case_folder)
        if not os.path.isdir(case_path):
            continue
        
        case_id = case_folder
        case_data = None
        
        # Look for markdown report first
        for file in os.listdir(case_path):
            if file.endswith('.md') or file.endswith('-dispute-sample.md'):
                report_path = os.path.join(case_path, file)
                case_data = extract_case_data_from_markdown(case_id, report_path)
                break
        
        # If no markdown, try to build from JSON
        if not case_data:
            case_data = {"case_id": case_id}
        
        # Merge tracking data if available
        json_file = os.path.join(case_path, f"tracking_{case_id}.json")
        if os.path.exists(json_file):
            json_data = extract_case_data_from_json(case_id, json_file)
            case_data.update(json_data)
        
        if case_data.get("amount", 0) > 0 or case_data.get("case_id"):
            cases.append(case_data)
    
    return sorted(cases, key=lambda x: x.get("transaction_date", ""), reverse=True)

def generate_html_dashboard(cases):
    """Generate interactive HTML dashboard."""
    # Calculate summary stats
    total_chargebacks = len(cases)
    total_amount = sum(c.get("amount", 0) for c in cases)
    avg_amount = total_amount / total_chargebacks if total_chargebacks > 0 else 0
    friendly_fraud_count = sum(1 for c in cases if c.get("friendly_fraud_indicator"))
    
    # Group by reason code
    reason_codes = {}
    for case in cases:
        code = case.get("reason_code", "Unknown")
        reason_codes[code] = reason_codes.get(code, 0) + 1
    
    # Group by merchant
    merchants = {}
    for case in cases:
        merchant = case.get("merchant", "Unknown")
        if merchant not in merchants:
            merchants[merchant] = {"count": 0, "total": 0}
        merchants[merchant]["count"] += 1
        merchants[merchant]["total"] += case.get("amount", 0)
    
    # Group by status
    statuses = {}
    for case in cases:
        status = case.get("status", "unknown")
        statuses[status] = statuses.get(status, 0) + 1
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chargeback & Dispute Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
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
            max-width: 1400px;
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
            font-size: 2.5em;
        }}
        
        .report-meta {{
            color: #666;
            font-size: 0.95em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
            transition: transform 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card.alert {{
            border-left-color: #f59e0b;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-card.alert .stat-value {{
            color: #f59e0b;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.95em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .chart-container {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .chart-container h3 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.3em;
        }}
        
        .chart-wrapper {{
            position: relative;
            height: 300px;
            margin-bottom: 20px;
        }}
        
        .cases-table {{
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .table-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
        }}
        
        .table-header h3 {{
            margin: 0;
            font-size: 1.3em;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        th {{
            background: #f3f4f6;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #e5e7eb;
            font-size: 0.9em;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #e5e7eb;
            font-size: 0.9em;
        }}
        
        tr:hover {{
            background: #f9fafb;
        }}
        
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge-friendly-fraud {{
            background: #fecaca;
            color: #991b1b;
        }}
        
        .badge-representment {{
            background: #bfdbfe;
            color: #1e40af;
        }}
        
        .badge-escalated {{
            background: #fed7aa;
            color: #92400e;
        }}
        
        .badge-investigating {{
            background: #d1d5db;
            color: #374151;
        }}
        
        .currency {{
            font-weight: 600;
            color: #667eea;
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .charts-grid {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
            
            .stat-value {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 Chargeback & Dispute Dashboard</h1>
            <div class="report-meta">
                Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
                Total Cases: <strong>{total_chargebacks}</strong>
            </div>
        </header>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{total_chargebacks}</div>
                <div class="stat-label">Total Chargebacks</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value"><span class="currency">${total_amount:,.2f}</span></div>
                <div class="stat-label">Total Amount Disputed</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value"><span class="currency">${avg_amount:,.2f}</span></div>
                <div class="stat-label">Average Dispute Amount</div>
            </div>
            
            <div class="stat-card alert">
                <div class="stat-value">{friendly_fraud_count}</div>
                <div class="stat-label">Friendly Fraud Indicators</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-container">
                <h3>Chargebacks by Status</h3>
                <div class="chart-wrapper">
                    <canvas id="statusChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Chargebacks by Reason Code</h3>
                <div class="chart-wrapper">
                    <canvas id="reasonChart"></canvas>
                </div>
            </div>
            
            <div class="chart-container">
                <h3>Amount Distribution by Merchant</h3>
                <div class="chart-wrapper">
                    <canvas id="merchantChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="cases-table">
            <div class="table-header">
                <h3>📋 Detailed Case List</h3>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Case ID</th>
                        <th>Merchant</th>
                        <th>Amount</th>
                        <th>Reason Code</th>
                        <th>Transaction Date</th>
                        <th>Status</th>
                        <th>Flags</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    for case in cases:
        status_badge = case.get("status", "unknown").replace("_", " ").title()
        status_class = f"badge-{case.get('status', 'unknown')}"
        
        flags = []
        if case.get("friendly_fraud_indicator"):
            flags.append('<span class="badge badge-friendly-fraud">Friendly Fraud</span>')
        
        flags_html = " ".join(flags) if flags else "—"
        
        html += f"""                    <tr>
                        <td><strong>{case.get('case_id', 'N/A')}</strong></td>
                        <td>{case.get('merchant', 'N/A')}</td>
                        <td><span class="currency">${case.get('amount', 0):,.2f}</span></td>
                        <td>{case.get('reason_code', 'N/A')} {case.get('reason_description', '')}</td>
                        <td>{case.get('transaction_date', 'N/A')}</td>
                        <td><span class="badge {status_class}">{status_badge}</span></td>
                        <td>{flags_html}</td>
                    </tr>
"""
    
    html += """                </tbody>
            </table>
        </div>
        
        <footer>
            <p>📊 This dashboard was auto-generated from your evidence/ folder. Add more cases to keep it updated.</p>
        </footer>
    </div>
    
    <script>
        const chartConfig = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: { padding: 15, font: { size: 11 } }
                }
            }
        };
"""
    
    # Status chart data
    status_labels = list(statuses.keys())
    status_values = list(statuses.values())
    
    html += f"""        
        const statusCtx = document.getElementById('statusChart').getContext('2d');
        new Chart(statusCtx, {{
            type: 'doughnut',
            data: {{
                labels: {json.dumps(status_labels)},
                datasets: [{{
                    data: {json.dumps(status_values)},
                    backgroundColor: ['#3b82f6', '#f59e0b', '#ef4444'],
                    borderColor: '#fff',
                    borderWidth: 2
                }}]
            }},
            options: chartConfig
        }});
"""
    
    # Reason code chart data
    reason_labels = list(reason_codes.keys())
    reason_values = list(reason_codes.values())
    
    html += f"""        
        const reasonCtx = document.getElementById('reasonChart').getContext('2d');
        new Chart(reasonCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(reason_labels)},
                datasets: [{{
                    label: 'Count',
                    data: {json.dumps(reason_values)},
                    backgroundColor: '#8b5cf6',
                    borderRadius: 5
                }}]
            }},
            options: {{
                ...chartConfig,
                indexAxis: 'y',
                scales: {{
                    x: {{ beginAtZero: true }}
                }}
            }}
        }});
"""
    
    # Merchant chart data
    merchant_labels = list(merchants.keys())
    merchant_values = [merchants[m]["total"] for m in merchant_labels]
    
    html += f"""        
        const merchantCtx = document.getElementById('merchantChart').getContext('2d');
        new Chart(merchantCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(merchant_labels)},
                datasets: [{{
                    label: 'Amount ($)',
                    data: {json.dumps(merchant_values)},
                    backgroundColor: '#ec4899',
                    borderRadius: 5
                }}]
            }},
            options: {{
                ...chartConfig,
                scales: {{
                    y: {{ beginAtZero: true }}
                }}
            }}
        }});
    </script>
</body>
</html>"""
    
    return html

def main():
    """Main execution."""
    print("🔍 Scanning evidence folder for chargebacks...")
    cases = scan_evidence_folder()
    
    if not cases:
        print("⚠️  No chargebacks found in evidence/ folder.")
        print("Please ensure case folders contain tracking JSON or dispute reports.")
        return
    
    print(f"✅ Found {len(cases)} chargeback(s).")
    
    # Generate dashboard
    print("📊 Generating HTML dashboard...")
    html = generate_html_dashboard(cases)
    
    # Save dashboard
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(BASE_DIR, OUTPUT_DIR, "chargeback_dashboard.html")
    
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"✅ Dashboard saved to: {output_file}")
    print(f"📈 Open in browser to view interactive charts and tables.")

if __name__ == "__main__":
    main()
