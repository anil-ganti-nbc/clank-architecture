# M5 ENTRY CRITERIA — when a QC learning experiment becomes worthwhile (ADR-0002 gate)

Status: ADOPTED as the objective pre-conditions for designing any M5
learning/feedback phase. Measured against Motherclank M4 corpus batches only —
never against machine scores or bulk-labeled history.

## Hard criteria (ALL must hold, measured over a rolling 4-week soak)

| # | Criterion | Threshold | Rationale |
|---|---|---|---|
| 1 | Corpus size per ACTIVE clank lane | ≥ 50 human records each for ≥ 2 Clanks | below this, any learned signal is noise-fitting |
| 2 | Disposition diversity per qualifying Clank | ≥ 3 distinct fleet dispositions with ≥ 5 records each | single-class corpora teach nothing |
| 3 | Correction rate observed | ≥ 5% of records carry is_corrected_upstream or a supersedes chain in ≥ 1 Clank | proves operators actually revise decisions — the core signal a learner would amplify; also validates lineage plumbing |
| 4 | Review rate on at least one lane | ≥ 20% of eligible items reviewed over the window | eligible-but-unreviewed masses cannot anchor recall estimates |
| 5 | Unmapped vocabulary share | ≤ 10% of new records per Clank | high UNMAPPED means the normalization layer needs a reviewed mapping first, not a model |
| 6 | Soak duration | ≥ 28 days since first M4 batch | guards against launch-week enthusiasm bias |
| 7 | Provenance integrity | 100% of records carry adapter contract version + ingestion snapshot hash; zero broken supersedes chains | mechanical check via conformance suite |

## Anti-criteria (any ONE vetoes starting M5)

- Any bulk-labeling or score-derived "labels" entered to satisfy thresholds.
- Correction rate = 0% across the whole corpus after ≥ 50 records (operators
  never revise → the feedback channel is decorative).
- Any unresolved write-back path from Motherclank toward a Clank.

## Measurement

`motherclank ingest-qc` coverage output IS the measurement instrument:
eligible_items / review_rate / disposition_distribution / correction_rate /
unmapped_rate per Clank. The conformance suite asserts provenance integrity (#7).

## Decision protocol

When all hard criteria hold and no anti-criterion applies, file an ADR proposing
the specific M5 experiment design (dataset manifest, label policy, evaluation
plan, rollback). The ADR — not this document — authorizes work.
