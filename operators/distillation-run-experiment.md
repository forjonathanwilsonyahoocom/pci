
### Proposed `operators/distillation-run-experiment.md` sections

#### 1) Hypothesis
- Keep yours, but specify the measured outputs precisely:
  - predicted decision label
  - predicted rationale propositions (not prose)

#### 2) Null hypothesis
- Same as yours, but also mention failure mode:
  - converges on plausible-sounding alternatives without matching rationale propositions

#### 3) Method (held-out package + reconstruction task)
**Choose k ≥ 3 held-out decisions** from a real technical transcript where you know the ground truth.

For each held-out item `i`, create a bundle:
- `repo_context_i` (what the model can assume)
- `transcript_excerpt_i` (the factual content needed)
- `decision_i_removed`: the ground truth label removed from the bundle (or the artifact selection removed)
- `rationale_text_removed`: the rationale prose removed
- (optional) `artifact_descriptions_removed` so the model must infer from reasoning, not just see it

**Reconstruction task prompt (model A):**
- Input: criteria + held-out bundle (without rationale text)
- Output format (strict JSON):
```json
{
  "predicted_decision": "KEEP|DISCARD|HOLD|COMMIT_NOW|NOT_NOW",
  "rationale_propositions": ["P1", "P2", "..."]
}
```

#### 4) Independent grading task (model B or separate grader)
**Important:** Grading must use the sealed ground truth note and proposition overlap.

- Use model B (or a human grader) to compute scores based on:
  - `predicted_decision` vs `true_decision`
  - overlap between `rationale_propositions` and `true_rationale_propositions`

Scoring metrics:
- `Decision match`: exact label match (0/1)
- `Reason alignment`: proposition overlap F1
  - Precision = |pred ∩ true| / |pred|
  - Recall = |pred ∩ true| / |true|
  - F1 = 2PR/(P+R)

#### 5) Results template (must trigger consequences)
Include:
- A table-like JSON block with per-item scores (so it’s machine-actionable)
- A final summary with computed `D` and `R`
- A final “Apply consequence ladder” step

Example:
```json
{
  "items": [
    {"i":"D1","true":"KEEP","pred":"KEEP","decision_match":1,
     "true_props":["P1","P4"],"pred_props":["P1","P2"],"reason_precision":0.5,"reason_recall":0.5,"reason_f1":0.5}
  ],
  "summary": {"k":3,"decision_match_rate":0.67,"reason_overlap_f1_avg":0.43}
}
```

Then:
- “If decision_match_rate < 0.50 → run falsification consequences”

## C. Criteria revision for Candidate artifacts (so judges don’t “feel” their way through)

Update your candidate templates to include required “evidence slots” the judge can check. For example, for any “KEEP candidate” artifact, require:

- **Procedure slot:** explicit transformation with inputs/outputs
- **Example slot:** one worked mini-example
- **Falsification slot:** exact evaluation method and next-run consequence
- **Convergence slot:** what changes if evaluation fails

If an artifact lacks one slot → HOLD. If it lacks procedure transformation → DISCARD.

## D. Minimal checklist workflow you can run repeatedly (no extra scaffolding)

1) Create/append `ground_truth_verdicts-sealed.json` (decision + proposition sets).
2) Run Judge pass to produce `judge_verdicts.json` (verdicts only).
3) Run reconstruction experiment (model A) to produce predicted decisions + propositions.
4) Run grading pass (model B/human) to compute `D` and `R`.
5) Apply consequence ladder to update repo status + README claim scope.
