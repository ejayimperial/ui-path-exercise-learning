# Day 2 Assignment – Healthcare Claims Queue Processing (UiPath)

## Goal
Build a Dispatcher + Performer automation using UiPath Studio and UiPath Orchestrator queues.

## Inputs
- claims_batch_60.csv (main batch)
- claims_edge_cases_5.csv (edge cases)
- eligibility_mock_responses.csv (optional for API simulation or lookup)
- business_rules_decision_table.csv
- uat_test_cases_template.csv

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
