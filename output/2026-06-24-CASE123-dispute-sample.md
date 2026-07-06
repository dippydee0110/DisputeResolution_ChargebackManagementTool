# DISPUTE REPORT: CASE123

**Date:** 2026-06-24
**Case ID:** CASE123
**Requested by:** Self
**Audience:** Payments ops, Fraud team
**Scope:** Quick investigation of disputed transaction and recommended disposition

---

## Executive Summary

- Evidence supports merchant delivery and valid authorization; recommend representment.
- Missing: signed delivery confirmation image — request from shipping provider.
- Action: bundle gateway logs, order invoice, and customer communications for representment.

---

## Case Details

- **Transaction date:** 2026-06-01
- **Amount:** USD 134.50
- **Merchant:** ExampleMerchant Inc.
- **Processor / Acquirer:** ExampleAcquirer
- **Card network / Reason code:** Visa 4837 (Fraud — Cardholder does not recognize)
- **Customer claim summary:** Cardholder reports unauthorized transaction; no recognition of merchant.

---

## Evidence Checklist

- Transaction record (gateway logs) — present
- Authorization & AVS/CVV result — present (AVS mismatch shown)
- Shipping/tracking info — present (tracking shows delivered)
- Delivery confirmation / signature — missing (request pending)
- Communications (customer emails/chat) — present
- Refund records — none
- Supporting attachments (screenshots, invoices) — present (invoice.pdf)

---

## Timeline & Findings

### Timeline
- 2026-06-01 14:12 — Transaction processed
- 2026-06-03 09:20 — Customer complaint received
- 2026-06-10 10:45 — Merchant provided invoice and tracking

### Findings
- Gateway logs show valid authorization with AVS mismatch (billing vs shipping address).
- Shipping provider marks package delivered to address on file on 2026-06-05.
- Customer communications include request to dispute charge two days after transaction.

---

## Disputed Points & Uncertainties

- No signed delivery confirmation image yet — merchant claims standard delivery.
- AVS mismatch increases risk of friendly fraud or stolen card use.

---

## Sources / References

1. Gateway logs — /evidence/gateway_CASE123.log
2. Merchant invoice — /evidence/invoice_CASE123.pdf
3. Shipping provider tracking — /evidence/tracking_CASE123.json
4. Customer chat export — /evidence/chat_CASE123.txt

---

## Conclusion & Recommendation

- Represent with evidence package: gateway logs, invoice, tracking. Attempt to fetch signed POD from carrier within 5 business days.
- If POD cannot be provided and AVS mismatch remains unexplained, escalate to chargeback specialist for manual review.

---

## Key Takeaways

- Prepare evidence bundle promptly; networks favor delivery + logs for representment.
- Track outstanding evidence items with clear owners and deadlines.

---

## Recommended Next Steps

- Request proof-of-delivery image from carrier (owner: Ops, due: 2026-06-29).
- Create evidence ZIP using `scripts/bundle_evidence.py CASE123 /path/to/evidence/ /path/to/output/` and attach to representment.

---

*Saved to `output/`.*
