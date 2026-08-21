# Risk register

| ID | Risk | Severity | Containment | Exit evidence |
|---|---|---:|---|---|
| R-001 | Repository head is mistaken for the deployed artifact. | Critical | Canonical ledger separates `source_sha` from `deployed_sha`. | Host-to-artifact evidence for every active deployment. |
| R-002 | Unauthenticated dashboard is exposed beyond loopback. | Critical | Reject non-loopback binds and unauthenticated mutations. | Bind and mutation regression tests in every dashboard repository. |
| R-003 | Windows scheduled task fires but never starts SemInt. | Critical | Native Task Scheduler action fields; observable invocation/result/heartbeat. | Two real unattended Windows runs. |
| R-004 | API keys or webhook credentials enter logs or crash output. | Critical | Header-based credentials and centralized redaction. | Sentinel tests plus tree/history/artifact scan and key rotation record. |
| R-005 | Duplicate architecture repositories imply conflicting authority. | High | ADR-0001 proposes roles and a reviewed disposition for `unified-clank-platform`. | Merged ADR, completed disposition, and conformance links resolve to one governance and one implementation authority. |
