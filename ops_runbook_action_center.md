# Ops Runbook – Action Center Review (Student Template)

## When do I get a task?
- Claims flagged High Risk (Amount >= threshold) OR validation requires human judgment.

## What do I check?
- ClaimID, Amount, DiagnosisCode, ProcedureCode, FacilityType
- Any validation warnings produced by the bot
- Supporting note (if present)

## How do I respond?
- Approve: bot continues and updates status to Approved
- Reject: bot marks claim Rejected (Business Exception outcome)
- Request Info: bot routes back to UnderReview (optional)

## SLA
- Target: respond within 2 hours (configurable)
