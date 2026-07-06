# P0 Implementation Backlog (1-2 Weeks)

## Goal
Ship an MVP that demonstrates Airbnb-scale chargeback and dispute product thinking: loss reduction, trust preservation, and policy-safe workflows.

## Outcomes (P0)
- End-to-end dispute lifecycle visible from ingestion through closure.
- Policy-timed guardrails for Resolution Center and Host Damage Protection terms.
- Decisioning support by reason code/payment method with explainable recommendations.
- Table-first operational UX for Customer, Merchant, and Admin dashboards.

## Workstreams

### 1. Case Lifecycle Engine
- Add canonical lifecycle states:
  - Chargeback Ingested
  - Representment Recommended
  - Representment Submitted
  - Pre-Arbitration Eligible
  - Pre-Arbitration Submitted
  - Final Decision (Won/Lost)
  - Recovery Pending (Airbnb -> Guest paid, Merchant clawback pending)
  - Closed
- Add transition validation map by payment method and reason code.
- Add terminal-state lock rules and re-open exceptions.

### 2. Policy Rules Layer
- Resolution Center timers:
  - 60-day request window from checkout.
  - 72-hour discovery flag for refund/rebooking handling.
- Host Damage Protection timers:
  - 14-day host-to-guest pursuit requirement.
  - 30-day host request submission window.
- Add policy violation flags in case rows and expanded details.
- Add explainers for ineligible requests and required remediation.

### 3. Reason Code Decisioning (v1)
- Add reason-code playbook object with:
  - Recommended action (deflect/settle/represent).
  - Required evidence checklist.
  - Optional evidence boosting win probability.
  - Expected win-rate bands by payment method.
- Add per-case recommendation card/table with confidence and expected value.

### 4. Money Movement Ledger
- Add normalized ledger events:
  - Debit/Credit with party, amount, currency, stage, source.
- Show final closure path when Airbnb loses:
  - Airbnb credits guest first.
  - Merchant clawback/offset posted later.
  - Case closes after reconciliation.
- Add running balances for Guest, Merchant, Airbnb in expanded case table.

### 5. Evidence UX (Actionable)
- At each stage line item, allow attaching one or more docs.
- Add “missing evidence” indicator and upload CTA by stage.
- Add sample evidence preview in modal/table row details.
- Add legitimacy flags (missing metadata, low-quality, unverifiable source).

### 6. Top-Risk KPI Strip (3-Party)
- Add top cards for Airbnb, Merchant, Guest with:
  - Win probability (%)
  - Exposure at risk ($)
  - Suggested documents to improve odds
- Add breakdown by reason code and payment method.

## Technical Tasks
- Introduce shared utility modules in JS (single source):
  - policyRules
  - reasonCodeRules
  - ledgerEngine
  - evidenceRequirements
- Add localStorage schema versioning + migration function.
- Add deterministic demo seed scenarios:3
  - Card representment win
  - Card representment loss + guest payout + merchant clawback
  - Klarna auto-closure
  - UPI merchant-record-request pending

## Validation / Acceptance Criteria
- A case can traverse all lifecycle stages without manual JSON edits.
- Policy deadline breaches are visibly flagged in all 3 dashboards.
- Each expanded case shows table-based timeline + activity + ledger.
- Evidence attachments can be added from each stage row.
- Final-loss path shows Airbnb-to-guest payout and merchant clawback before close.

## Demo Script (8-10 min)
1. Ingest chargeback case.
2. Show decisioning recommendation by reason code.
3. Add missing evidence and improve win probability.
4. Simulate loss path: guest credit, merchant pullback, close.
5. Show KPI impact and policy compliance trace.
    