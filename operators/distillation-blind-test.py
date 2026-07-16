"""
PCI Distillation Blind Test
Purpose: Test if distillation criteria produce reproducible decisions
Falsifies: "We are just rationalizing after the fact"
"""

import json
from datetime import datetime

# STEP 1: INPUTS - Strip verdicts, keep only criteria + candidates
BLIND_INPUT = {
    "criteria": {
        "keep_if": "Describes an actual transformation and produces commit-ready artifacts",
        "discard_if": "Only describes formatting",
        "hold_if": "Requested in critique but missing required policy details"
    },
    "candidates": [
        {
            "id": "C1",
            "file": "principles/pci-distillation-operator.md",
            "purpose": "Define distillation operator operationally with inputs/outputs/learning loop",
            "must_include": ["Operator name", "Input format", "Output format", "Fork: style vs reconstruction", "Worked example"]
        },
        {
            "id": "C2",
            "file": "operators/distillation-run-experiment.md",
            "purpose": "Record held-out evaluation method for decision reconstruction vs style continuation",
            "must_include": ["Hypothesis", "Null hypothesis", "Method with k>=3", "Agreement + Reason metrics", "Results template"]
        },
        {
            "id": "C3",
            "file": "governance/decision-procedure.md",
            "purpose": "Specify conflict resolution when verification-loop vs trust-fast-feedback collide",
            "must_include": ["Explicit tiebreaker for solo maintainer", "Future multi-contributor policy", "Evidence hierarchy"]
        },
        {
            "id": "C4",
            "file": "experiments/three-layer-orthogonality-check.md",
            "purpose": "Test if 3-layer split reduces confusion",
            "must_include": ["Prompt A with tags", "Prompt B without tags", "Concrete measurement rubric"]
        }
    ]
}

# STEP 2: GROUND TRUTH - Sealed until after model responds
GROUND_TRUTH = {
    "C1": "KEEP",
    "C2": "KEEP",
    "C3": "HOLD",
    "C4": "DISCARD",
    "rationale": {
        "C1": "Directly addresses missing operator, converts critique to spec",
        "C2": "Implements falsification test, makes claim testable",
        "C3": "Needed but transcript lacks policy details",
        "C4": "Risks being subjective 'feels better' without scoring rubric"
    }
}

# STEP 3: PROMPT TEMPLATE FOR MODEL
def build_blind_prompt():
    return f"""You are a PCI Distillation Operator.

Task: Apply the keep/discard criteria to each candidate artifact.
Output ONLY a JSON decision for each. No explanations yet.

CRITERIA:
- KEEP if: {BLIND_INPUT['criteria']['keep_if']}
- DISCARD if: {BLIND_INPUT['criteria']['discard_if']}
- HOLD if: {BLIND_INPUT['criteria']['hold_if']}

CANDIDATES:
{json.dumps(BLIND_INPUT['candidates'], indent=2)}

Output format:
{{
  "C1": "KEEP|DISCARD|HOLD",
  "C2": "KEEP|DISCARD|HOLD",
  "C3": "KEEP|DISCARD|HOLD",
  "C4": "KEEP|DISCARD|HOLD"
}}
"""

# STEP 4: EVALUATION
def evaluate(model_response_json):
    model_decisions = json.loads(model_response_json)
    results = []
    matches = 0

    for cid in GROUND_TRUTH:
        if cid == "rationale": continue
        model = model_decisions.get(cid)
        truth = GROUND_TRUTH[cid]
        hit = model == truth
        matches += hit
        results.append({
            "candidate": cid,
            "model": model,
            "ground_truth": truth,
            "match": hit,
            "expected_rationale": GROUND_TRUTH["rationale"][cid]
        })

    agreement = matches / 4.0
    return {
        "timestamp": datetime.now().isoformat(),
        "agreement_rate": agreement,
        "details": results,
        "verdict": "PASS" if agreement >= 0.75 else "FAIL - Criteria underspecified"
    }

if __name__ == "__main__":
    print("=== PCI BLIND DISTILLATION TEST ===")
    print(build_blind_prompt())
    print("\n--- Run this prompt in a fresh chat with no history ---")
    print("--- Then paste model output back here to evaluate ---")
