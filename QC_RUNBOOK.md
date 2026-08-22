# QC RUNBOOK — operator surfaces per Clank (M4.5)

How to actually file human QC so the Motherclank M4 corpus keeps growing.
All surfaces are loopback/local; Motherclank ingests read-only afterwards.

## watch-clank  (OPERATIONAL — primary corpus source)
- Surface: dashboard `POST qc_submit_review` (app/main.py) — event review page.
- Dispositions: USEFUL / NOT_USEFUL / DUPLICATE / FALSE_POSITIVE (+ OUT_OF_STOCK on events).
- Corrections: re-submit with a different disposition — upstream records
  `is_corrected` + `updated_at`; M4 emits a superseding corpus record.
- Cadence guidance: review new events after each soak day; every review is ingested.

## smartphone-clank  (NEWLY ACTIVATED)
- Surface: `python main.py qc-action --action confirm|reject|quarantine|promote|note \
    --target-type device|evidence --target-id <id> --reason "why"`
- Writes one analyst_actions row verbatim (actor_label=operator-cli).
- Vocabulary is native/freeform today; Motherclank marks unmapped values UNMAPPED
  until a reviewed mapping lands.

## korean-tech-wire  (OPERATIONAL, loopback field-test dashboard)
- Surface: article detail page → Editorial Feedback buttons → `POST /feedback`.
- Outcomes freeform (e.g. USEFUL / NOT_USEFUL / OFF-TOPIC); preserved verbatim;
  writes now take the collector RunLock (M4.5 fix).

## oem-radar  (ACTIVATION FLAG — designed v4 subsystem)
- Surface: dashboard alert pages → review POST `/api/alerts/{id}/review`.
- Launch with: `oem-radar dashboard --allow-review-writes` (default remains off;
  loopback enforced; only the review POST path is authorized).
- Dispositions land in `alert_reviews` (+history); `alert_review_history` and
  `rule_suggestions` then become usable for deterministic feedback analysis
  (`oem-radar feedback` family already reads them).

## chinese-tech-wire / tablet-clank / semiconductor-intelligence / free-game-tracker
No human-QC surface yet — out of M4.5 scope; do not fabricate labels.

## Motherclank side
```
motherclank ingest-qc --real-state DIR --var-dir var --out var
```
Coverage per Clank now reports eligible_items, review_rate, disposition
distribution, correction_rate, unmapped_rate + examples. Raw dispositions are
always preserved verbatim; fleet values appear only via explicit mapping.
