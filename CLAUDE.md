# Dispute & Chargeback Management Agent

Project context: This agent workspace is focused on chargeback and dispute research, reporting, and workflow templates to help process, analyze, and document payment disputes.

## Purpose

Support research, evidence collection, and report generation for chargebacks and payment disputes. Use the templates and workflows to produce consistent dispute reports and to track investigation steps.

## About the owner

Creates concise, practical documentation and templates for payments operations and dispute resolution. Audience includes payments ops, fraud teams, and compliance reviewers.

## Rules

- Always ask clarifying questions before starting a complex task
- Show your plan and steps before executing
- Keep reports and summaries concise — use bullet points over paragraphs
- Save all output files in the `output/` folder
- Cite sources and preserve evidence metadata (timestamps, source IDs)

## Design System (Airbnb)

**All screens must match Airbnb's design language and typography:**

### Typography
- Font family: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif`
- Headers (H1): 28px, weight 800, letter-spacing -0.5px
- Section titles (H2): 18px, weight 700
- Body text: 14-16px, weight 400
- Buttons: 13-14px, weight 600

### Colors
- Primary text: #222
- Secondary text: #717171
- Background: #f5f5f5
- Card background: white
- Borders: #e0e0e0
- Status colors:
  - Open/Pending: #ffe8cc (background) / #b07500 (text)
  - Won/Approved: #dcf0d8 (background) / #3d7f3f (text)
  - Lost/Denied: #f2dede (background) / #8b3a3a (text)
  - Neutral: #f5f5f5 (background) / #717171 (text)

### Components
- Cards: 12px border-radius, 1px solid #e0e0e0 border, white background
- Buttons: 8px border-radius, 10-12px padding
- Tabs: underline style on active, 16px padding
- Empty states: centered, with icon (48px), title, and description
- Spacing: 16-20px gaps, 40px outer padding

### UI Patterns
- Two-column action cards for primary CTAs
- Tab navigation for case filtering
- Grid-based case card layouts
- Hover states with subtle shadow: `0 4px 12px rgba(0,0,0,0.08)`
- Responsive: stack to single column at 768px

## Project Structure

- `workflows/` — workflow instruction files for dispute investigations and reporting
- `output/` — finished deliverables (reports, case notes, dashboards)
- `resources/` — reference docs, evidence checklists, and templates
