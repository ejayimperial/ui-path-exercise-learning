# Day 3 Lab Instruction Worksheet (Student) – Exception Handling & Reliability
**Topic:** Business vs System Exceptions • Retry Discipline • Production Behavior  
**Estimated time:** 60–90 minutes  
**Prerequisites:** Day 3 Dispatcher + Performer (REFramework) + Orchestrator Queue already working

---

## 0) What You Will Build Today
You will enhance your existing queue-based claims automation so it behaves correctly under failure.

### Outcomes you must demonstrate
- Business exceptions: **fail once, no retry**
- System exceptions: **retry up to MaxRetries (e.g., 2)**
- High-risk items: **route to Manual Review (or Action Center if available)**
- Logs: **PHI-safe, structured, includes correlation IDs**

---

## 1) Setup Checklist (10 minutes)

### A. Orchestrator
1. Confirm Queue exists:
   - Queue name: `HEALTHCARE_CLAIMS`
2. Confirm retry count:
   - Max retries: `2`
3. Confirm you can see:
   - Transactions view
   - Failed / Successful counts
   - Retry number per transaction item

### B. Studio
1. Open your Performer project (REFramework).
2. Confirm Config file exists (Config.xlsx recommended).
3. Confirm logging is working (Log Message activity or framework logging).
4. Confirm your Dispatcher can add items to the queue.

---

## 2) Add Validation Rules (Business Exceptions) (20 minutes)

**Implement these validation rules inside `Process.xaml` BEFORE external integrations.**

### Rule R1: Missing MemberID
- Condition: `MemberID` is empty or whitespace
- Action: Throw **BusinessRuleException** with message `MissingMemberID`

### Rule R2: Missing ProcedureCode
- Condition: `ProcedureCode` is empty or whitespace
- Action: Throw **BusinessRuleException** message `MissingProcedureCode`

### Rule R3: Amount <= 0
- Condition: `Amount <= 0`
- Action: Throw **BusinessRuleException** message `InvalidAmount`

### Rule R4: Future ServiceDate
- Condition: `ServiceDate > Today`
- Action: Throw **BusinessRuleException** message `FutureServiceDate`

✅ Evidence required
- Screenshot of Orchestrator transaction for each edge case showing:
  - Failed (business)
  - Retry count does not increase

---

## 3) Add Failure Injection (System Exceptions) (20 minutes)

You will simulate transient failures to verify retry behavior.

### Method A (Recommended): Random failure injection in Process.xaml
- Add a config value: `InjectSystemFailureRate` (e.g., 0.10)
- Each transaction:
  - Generate random number 0..1
  - If random < rate → throw **System.Exception** (`SimulatedTransientFailure`)

### Method B: Trigger failures for specific ClaimIDs
- If ClaimID matches a known list:
  - `CLM-FAIL-API-001` → throw System.Exception
  - `CLM-FAIL-PY-001` → throw System.Exception

✅ Evidence required
- Orchestrator shows:
  - Transaction failed on attempt 0
  - Retried on attempt 1 (and attempt 2 if configured)
  - Finally succeeds after you disable injection or logic allows success

---

## 4) Log Enhancements (10 minutes)

For each transaction, log at minimum:
- correlation_id (generated per job run)
- ClaimID (Queue Reference)
- stage/state
- outcome (Approved/Rejected/ManualReview/Retry)
- exception_type (Business/System)
- duration_ms
- retry_number

✅ Evidence required
- Screenshot of Orchestrator logs for:
  - A successful transaction
  - A business exception
  - A system exception retry

---

## 5) Update SetTransactionStatus Behavior (10 minutes)

Ensure:
- Business exceptions set status to **Failed** and do not retry
- System exceptions set status to **Failed** and allow retry (queue will retry)

✅ Evidence required
- Screenshot: Transaction details showing exception type and retry behavior

---

## 6) Run the Required Test Cases (15 minutes)

Use the provided edge case file:
- `claims_edge_cases_5.csv`

### Required tests
1. CLM-EDGE-001 → Business exception (MissingMemberID) → no retry
2. CLM-EDGE-002 → Business exception (MissingProcedureCode) → no retry
3. CLM-EDGE-003 → Business exception (InvalidAmount) → no retry
4. CLM-EDGE-004 → Business exception (FutureServiceDate) → no retry
5. CLM-EDGE-005 → Manual Review (or Action Center) → no retry

### Failure injection test
6. Any normal claim → simulate system failure once → retry succeeds

---

## 7) Submission Checklist (Student Deliverables)
Submit:
1. Screenshot of Orchestrator Queue transactions showing:
   - successes, business failures, retries
2. Completed `uat_execution_log_TEMPLATE.csv`
3. Updated `Process.xaml` (or project zip)
4. Short note (5–10 lines): “What I learned about Business vs System exceptions”

---

## Common Mistakes (Read This)
- ❌ Treating business exception as system exception → causes retry storms
- ❌ Logging sensitive details in plain text
- ❌ Throwing exceptions outside Process.xaml without proper handling
- ❌ Not using queue retry counts (manual retry loops)

---

## Instructor Verification
The instructor will validate:
- Correct classification
- Correct retry behavior
- Evidence screenshots
- Logging completeness
