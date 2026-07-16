# operators/distillation.md
# Distillation operator for converting a conversation transcript into candidate repo artifacts,
# then deciding—explicitly—what we keep and what we discard.

conversation
    ↓
claims
    ↓
candidate artifacts
    ↓
critique
    ↓
commit / discard
    ↓
repository

## Distillation thesis (weakened)
PCI is a proposed format for making reasoning processes portable between humans, models, and tools.
This doc’s job is to test whether our distillation loop produces artifacts we would truly commit,
not just artifacts that look structurally “reasonable”.

## Scope
Input: one conversation transcript (here: the thread whose last two Claude inputs you pasted).
Output: up to N candidate artifacts, each with:
- what it is
- what evidence it claims (if any)
- what would falsify it
- keep/discard decision and why

This is one distillation attempt.

## Inputs
- Transcript: (conversation in this chat; no external reading required)
- Repo goal (current): strengthen PCI pitch with falsifiable experiments, reduce elaboration-only progress,
  define governance/decision procedure, and make “distillation” operational.

## Procedure (no hand-wavy “we’ll decide later”)
### Step 1: Extract “keepable load-bearing claims” (smallest possible)
From the transcript(s), extract only claims that are:
- stated explicitly or strongly implied
- testable in principle
- small enough not to explode into “new stack” implications

Candidates (from this conversation):
1) The strongest structural idea: a three-layer split (knowledge / cognitive interface / execution).
2) The “conversation as compiler / repo as executable” frame.
3) The missing piece: distillation operator must be specified as a real transformation with inputs/outputs
   and a learning loop that produces commit decisions.

### Step 2: Extract “failure modes” (what we must not do again)
From the critiques, list concrete anti-patterns:
- Anti-pattern A: escalation without resistance (“so hott”; always more framework).
- Anti-pattern B: counterarguments answered with “another schema” rather than with an artifact.
- Anti-pattern C: novelty claims made without operational distinction between style-matching vs genuine
  decision reconstruction.
- Anti-pattern D: “governance metadata” described without specifying the actual decision procedure.

### Step 3: Generate candidate artifacts (target concrete files, not descriptions)
Produce candidate artifacts that could be committed immediately.

We generate exactly three candidate documents plus one optional “experiment record”.

#### Candidate Artifact 1 (PRIMARY)
File: principles/pci-distillation-operator.md
Purpose: define PCI distillation operationally, using this transcript as an example run.

Must include:
- Operator name: distillation
- Input format: transcript + optional repo constraints
- Output format: candidate artifacts with keep/discard decisions
- Explicit “style continuation vs decision reconstruction” fork
- A worked mini-example: show 1 extracted claim → 1 artifact → 1 falsification method

Keep/discard criterion:
- If it only describes formatting, discard.
- If it describes an actual transformation and produces commit-ready artifacts, keep.

#### Candidate Artifact 2 (PRIMARY)
File: operators/distillation-run-experiment.md
Purpose: record a real held-out evaluation method (not just “we should test”).
This is the transcript-grounded experiment the critique pushes for.

Must include:
- Hypothesis:
  When a model is given the rest of the repo and a stripped-out past decision (with reason removed),
  it will reconstruct the same decision for the same held-out rationale across multiple held-out decisions.
- Null hypothesis:
  The model produces plausible tradeoffs but does not converge on the actual prior decisions
  (or converges for the wrong reasons).
- Method:
  Choose k recent past decisions you actually made (k>=3).
  For each: provide the repo context but remove the decision’s “reason” portion,
  then ask the model to recommend the decision and justify it.
- Evaluation:
  - Agreement metric: did it match your actual decision?
  - Reason alignment metric: did it cite the same rationale (not just the conclusion)?
- Output:
  A short results table template + how you would update PCI’s claim strength.

Keep/discard criterion:
- Keep only if the experiment is specific enough that you could run it next week
  without inventing new scaffolding.

#### Candidate Artifact 3 (OPTIONAL but useful)
File: governance/decision-procedure.md
Purpose: specify the actual resolution procedure when verification-loop and trust-fast-feedback conflict.

Must include:
- Current policy for solo maintainer (now): explicit tiebreaker/default
- Future policy placeholder: what changes when multiple contributors exist
- A rule stating what evidence outranks what, and when a human must decide

Keep/discard criterion:
- Keep only if it contains an explicit procedure like:
  “When A and B conflict, do X; if X is unclear, default to Y.”
  Discard if it’s “community discussion” without rules.

#### Optional Candidate Artifact 4
File: experiments/three-layer-orthogonality-check.md
Purpose: test whether the three-layer split reduces confusion rather than just looking neat.

Method sketch:
- Create two prompts:
  (i) conversation framed with knowledge/cognitive interface/execution tags
  (ii) same content without tags
- Measure whether the resulting artifacts separate concerns correctly
- Held-out evaluation: can you predict which failures fall into which layer?

Keep/discard criterion:
- Only keep if it’s tied to a concrete measurement rather than a subjective “feels clearer”.


### Step 4: For each candidate, decide keep/discard now (no “later”)

**Step 4A — Ground-truth verdict note (sealed; writer-only)**
- Output: `ground_truth_verdicts.json` with:
  - `verdict[candidate_id] ∈ {KEEP, DISCARD, HOLD}`
  - `reason_propositions[candidate_id] = [P1, P2, ...]`
- **Rule:** the writer must not later edit this file after the judge run begins.


**Step 4B — Judge pass (verdict-only)**
- Input: criteria + candidates + *sealed* ground_truth_verdicts file is **not provided to the model generating the verdicts**.
- Output: `judge_verdicts.json` with the same candidate ids.

Decisions:

- Candidate 1: KEEP
  Rationale: directly addresses the missing “distillation operator” and uses this transcript as a worked example.
  It converts critique into an actionable specification.

- Candidate 2: KEEP
  Rationale: it implements the sharpest falsification distinction in the critique:
  decision reconstruction vs style continuation, and it turns “PCI effectiveness” into a specific experiment record.

- Candidate 3: HOLD (pending your preference)
  Rationale: governance procedure is explicitly requested in the critique, but the transcript doesn’t specify
  your current default tie-breakers. This file should be written when we know your real policy.

- Candidate 4: DISCARD for this attempt
  Rationale: orthogonality checks risk becoming another “schema feels better” measurement unless you already have
  a concrete scoring rubric and held-out failure cases.


**Step 4C — Scoring pass (compare, report, apply consequences)**
- Computes:
  - decision match rate
  - reason proposition overlap metrics
- Applies consequences ladder (next section).


## Distillation output (the “candidate artifacts we would commit” list)
COMMIT NOW:
1) principles/pci-distillation-operator.md
2) operators/distillation-run-experiment.md

NOT NOW:
3) governance/decision-procedure.md (needs your current conflict policy)
4) experiments/three-layer-orthogonality-check.md (measurement risk in this attempt)

## One-line falsification hook (so this can fail correctly)
If your evaluation run shows models reconstruct neither your decisions nor your reasons, PCI’s core portability claim
shrinks to “style-transfer under cooperative framing,” and the README must say so.
