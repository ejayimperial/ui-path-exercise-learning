# Logging Specification (Student Template)
Use PHI-safe logging. Do NOT log patient names, addresses, or full identifiers.

Required fields to log for every transaction:
- correlation_id (generated per job run)
- claim_id (Queue Reference)
- queue_item_id
- stage/state (Init, GetTransactionData, ProcessTransaction, SetTransactionStatus)
- outcome (Approved / Rejected / ActionCenter / Retry)
- exception_type (None / Business / System)
- exception_message (sanitized)
- duration_ms
- retry_number (from Orchestrator queue item)

Suggested log events:
- TX_START, TX_VALIDATION, TX_INTEGRATION_CALL, TX_DECISION, TX_END
