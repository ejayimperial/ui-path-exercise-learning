# Day 2 Assignment – Healthcare Claims Queue Processing (UiPath)

## Goal
Build a Dispatcher + Performer automation using UiPath Studio and UiPath Orchestrator queues.

## Inputs
- claims_batch_60.csv (main batch)
- claims_edge_cases_5.csv (edge cases)
- eligibility_mock_responses.csv (optional for API simulation or lookup)
- business_rules_decision_table.csv
- uat_test_cases_template.csv

## Instructions 
1) Claims Triage Bot with Action Center Approval

Skills: REFramework, Queues, Action Center, exception handling, logging

Scenario

Claims above a threshold require human approval.

Requirements

Dispatcher loads claims from CSV → Orchestrator Queue.

Performer validates + classifies:

Low risk → auto-approve

High risk → create Action Center task

Missing required data → Business Exception

Resume workflow after Action Center decision and update queue status.

Deliverables

Action Center tasks created + completed

Screenshots: queue items, action tasks, logs

A short SOP: “How an Ops user reviews claims”

2) Eligibility Verification via REST API (Mock)

Skills: REST API integration, error handling, retry discipline, queue processing

Scenario

Bot checks member eligibility against an API.

Requirements

Use a mock REST endpoint (e.g., Postman mock server or public JSON test API).

On API 500/timeout → System Exception → retry

On “ineligible” response → Business Exception

On success → mark claim eligible + store response in output file

Deliverables

API request/response logs (PHI-safe)

Retry validation proof

Output CSV with eligibility flag

3) Pharmacy Inventory Reconciliation Bot

Skills: Orchestrator queues, data transformation, exception handling

Scenario

Inventory counts differ between two sources.

Requirements

Dispatcher loads ["WMS.csv"](WMS.csv)  and  ["POS.csv"](POS.csv)

Performer matches SKU and computes delta:

delta within tolerance → success

delta too large → Business Exception (requires review)

Produce a reconciliation report

Deliverables

Delta report

Exceptions summary

Queue metrics (backlog, processing time)

4) Python Risk Score Integration (Simple Model)

Reffer to [risk_scoring.py](risk_scoring.py) 

Skills: Python integration + UiPath, queue performer, robustness

Scenario

Claims need a “risk score” calculated via Python.

Requirements

Python script accepts JSON/args and returns score

Performer calls Python for each claim

If Python crashes or returns invalid data → System Exception → retry

Add “risk_band”: Low/Med/High

Deliverables

Python script + UiPath workflow

Logs showing score + execution time

Proof of failure handling

Expected Output Example

For CLM-EDGE-005 (250k amount), output will look like:

### Output:
```JSON 
{
  "risk_score": 60-100,
  "risk_band": "HIGH",
  "reasons": ["VeryHighAmount>=250000", ...]
}

```

5) LLM Claim Summary Generator (Structured Output)

Skills: LLM prompt orchestration, JSON schema validation, logging

Scenario

Generate a structured summary for each claim for Ops.

Requirements

For each claim, call LLM (or mock LLM via static JSON if no API access)

Prompt must request JSON only:

summary

issues_found

next_action

Validate JSON; if malformed → retry once; if still malformed → Business Exception

Deliverables

Prompt template + versioning

JSON outputs saved per ClaimID

Token/latency logs (even if simulated)

6) SLA Breach Watcher + Alerting

Skills: Orchestrator monitoring, queue analytics, operational mindset

Scenario

Queue items waiting too long must be escalated.

Requirements

A monitoring workflow runs every 30 minutes:

checks queue items “New” older than X minutes

sends email/Teams message (or writes alert file)

Creates an “Ops Alert” queue item for follow-up

Deliverables

Alert evidence (log + output)

SLA breach list report

Basic runbook: “What Ops does when alerted”

7) UAT Pack Builder (Functional Skills Emphasis)

Skills: business rule translation, test case creation, UAT support

Scenario

Students must create UAT-ready artifacts, not just automation.

Requirements

Decision table for claims rules

20 test cases:

positive/negative

boundary values

exception scenarios

UAT execution log template

Defect template (severity, reproduction steps)

Deliverables

UAT pack (doc or spreadsheet)

Traceability matrix (rule → test case → expected outcome)

8) End-to-End Mini Capstone (All-In)

Skills: everything combined

Scenario

Claims intake → eligibility check → risk score → LLM summary → Action Center approval → status update.

Must Include

Dispatcher/Performer

REST API call

Python call

LLM call (real or mocked)

Action Center branch

Logging + monitoring summary

Deliverables

5–7 min demo

Metrics report: success %, retries %, avg processing time



## Required Components
1) Orchestrator
   - Create Queue: HEALTHCARE_CLAIMS
   - Set max retries: 2
   - Enable priorities (High/Normal recommended)

2) Dispatcher (Studio)
   - Read claims_batch_60.csv AND claims_edge_cases_5.csv
   - Add each row as a queue item
   - Use ClaimID as Reference
   - Priority = High if Amount >= 50000

3) Performer (REFramework)
   - Get Transaction Item from HEALTHCARE_CLAIMS
   - Validate against decision table
   - If Amount >= 100000: send to Action Center (optional if available)
   - Set transaction status correctly:
     - Business Exception => Failed (no retry)
     - System Exception => Failed (retry)
     - Success => Successful

## Deliverables
- Orchestrator screenshots (queue, jobs, transactions)
- Run results (success %, rejected %, retry %)
- Completed uat_test_cases_template.csv
- Short 3–5 min demo

## Notes
Treat the data as PHI-adjacent: keep logs sanitized.
