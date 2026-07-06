# P1 Architecture Roadmap (2-6 Weeks)

## Objective
Evolve from demo UI into scalable disputes platform architecture supporting new payment methods, geographies, and verticals.

## Target Architecture

### 1. Domain Services
- Dispute Lifecycle Service
  - Owns state machine and transition authorization.
- Decisioning Service
  - Rule-based + ML score blending.
  - Outputs recommendation, confidence, and expected value.
- Policy Compliance Service
  - Encodes deadlines and eligibility constraints.
  - Provides deterministic pass/fail reasons.
- Ledger Service
  - Immutable financial events + balance projections.
- Evidence Service
  - Evidence package completeness scoring.
  - Metadata validation and anti-fraud checks.

### 2. Data Model (Core Entities)
- dispute_case
- dispute_stage_event
- monetary_ledger_event
- evidence_item
- evidence_requirement
- policy_evaluation
- decision_recommendation
- reason_code_rule
- payment_method_rule
- risk_snapshot

### 3. Decisioning Stack
- Rules-first orchestration:
  - Hard policy constraints -> eligibility gating.
  - Reason-code/payment-method playbook.
  - ML risk/win scores as ranking/prioritization features.
- Add explainability payload:
  - top_signals
  - missing_signals
  - confidence drivers

### 4. Eventing and Integrations
- Processor webhook ingestion boundary.
- Event bus for stage, evidence, and ledger updates.
- Retry-safe idempotency keys for chargeback events.
- Audit trail for policy-sensitive actions.

### 5. UX Architecture
- One shared case-expansion renderer with table sections:
  - Case Summary Table
  - Timeline Activity Table
  - Payment/Ledger Table
  - Evidence Package Table
- Role overlays only (Customer/Merchant/Admin permissions), not separate logic forks.

## Security and Integrity
- Fraud-resistance checks for doctored evidence and inconsistent metadata.
- Role-based permissioning for sensitive actions.
- Immutable financial event append-only model.
- SLA monitoring for response windows.

## Observability
- Lifecycle funnel metrics:
  - Ingested -> Deflected -> Represented -> Pre-Arb -> Closed
- Win/loss by reason code, processor, payment method, region.
- Alerting:
  - deadline at-risk
  - failed clawback
  - high-loss clusters

## Rollout Plan

### Phase 1
- Introduce shared domain modules behind existing UI.
- Add schema version and migration support.

### Phase 2
- Move lifecycle + policy logic to service abstraction.
- Introduce immutable ledger events and reconciliation checks.

### Phase 3
- Plug in score providers (ML + external risk vendors).
- Add experiment framework for deflection and outreach variants.

## Success Criteria
- 0 ambiguous stage transitions.
- 100% explainable recommendations for operator actions.
- Reduced manual intervention in evidence collection.
- Lower net loss rate with stable trust and satisfaction indicators.
