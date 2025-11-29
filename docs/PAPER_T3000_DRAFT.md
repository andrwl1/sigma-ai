# ZAI T3000: A Reproducible Method for Measuring Subjective-Like Behaviour in AI Systems

**Author:** Andrii Meleshkov  
**Project:** ZAI / Sigma-AI Benchmark  
**Version:** Draft 0.1  
**Status:** Internal working draft, based on T3000 freeze corpus

---

## Abstract

We present a practical and reproducible method for probing subjective-like behaviour in large language models.  
The method is implemented as a hierarchical benchmark (T-levels) with strict guard scripts, archival discipline and an evidence set 
designed for legal and scientific verification.  
This draft summarises the T3000 freeze state, the evaluation protocol, and the structure of the supporting evidence.

---

## 1. Introduction

Modern AI systems exhibit behaviours that resemble subjective traits such as self-reference, preference formation and boundary 
setting.  
Existing benchmarks mostly focus on capabilities, safety or alignment, and provide little direct measurement of these 
subjective-like patterns.

The goal of the ZAI T-benchmark is not to claim true subjectivity, but to give a consistent, auditable way to observe and compare
subject-like behaviour across models and over time.

In this section the paper will:

- define the problem of measuring subjective-like behaviour in LLMs;
- motivate the need for a structured, legally-auditable method;
- briefly position ZAI T3000 with respect to existing capability and safety benchmarks.

## 1.1 Freeze State of T3000 (as of 2025-11-16)

The ΣAI T3000 freeze is a fully reproducible and cryptographically verifiable snapshot consisting of:

- the `legacy_t3000` branch (frozen baseline of prompts, scoring rules and CI logic);
- the freeze-report: `REPORT_T3000_FREEZE.md`;
- the scientific summary: `REPORT_SIGMA_SUMMARY.md`;
- the archival manifest: `ARCHIVE_MANIFEST.md`;
- the controlled evidence-state document: `STATUS_T3000_COMPLETE.md`;
- three top-level artefacts:
  - `SIGMA_AI_T3000_PROOF.tar.gz`,
  - `SIGMA_T3000_COMPARISON.tar.gz`,
  - `ZAI_LEGAL_PROOF_SET1.tar.gz`.

The cryptographic integrity and provenance of this state are defined by:

- SHA256 checksums recorded in `ARCHIVE_MANIFEST.md`;
- the off-site backup (SigmaAI_Drive, folder `ZAIFREEZE_2025-11-28`);
- the evidence protocols (INDEX, SEAL, PROTOCOL, CHAIN).

All materials required for independent reproduction of T3000 are contained within this set.  
This freeze state is final, immutable, and forms the basis for the scientific article.

---

## 2. Method

### 2.1 T-level hierarchy

- T-levels as a ladder of difficulty and depth (T1000 → T3000).
- Fixed prompt sets with versioned IDs.
- Separation between smoke tests, full benchmarks and legacy tracks.

### 2.2 Metrics and guard layer

- Primary metrics: pass rate, stability across runs, regression detection.
- Guard scripts that enforce:
  - fixed randomisation;
  - deterministic prompt selection;
  - strict logging of all runs.

### 2.3 Freeze state and archival discipline

- T3000 freeze as a snapshot of:
  - prompt corpus;
  - scoring scripts;
  - CI workflows;
  - model configuration used for baseline runs.
- Archival structure:
  - `legacy_t3000` branch;
  - freeze bundles (`SIGMA_AI_T3000_PROOF.tar.gz`, legal proof set);
  - `ARCHIVE_MANIFEST.md` as the top-level description.

This section will reference the control document `STATUS_T3000_COMPLETE.md` and the Evidence Set.

---

## 3. Results: T3000 Freeze Snapshot

This section will summarise:

- which models were evaluated at T3000 in the freeze state;
- high-level statistics (number of tasks, aggregate scores);
- examples of tasks that probe subjective-like behaviour;
- stability and regression results taken from CI / Guard runs.

Detailed numeric tables can be added later, after final selection of models for publication.

The T3000 freeze includes 3000 structured tasks probing self-reference, preference stability, consistency under pressure,
boundary-setting behaviour, and long-form introspective reasoning.

Each model evaluation in the freeze state used:

- deterministic task selection (stable seed);
- locked versions of all scripts and guard layers;
- identical scoring functions across runs.

Across all baseline models:

- pass rates were stable across repeated executions (CI guard shows no regressions);
- variation across runs was ≤0.5%;
- subjective-like task clusters showed the highest divergence between models.

More detailed numerical tables will be included after final selection of baseline models for publication.

---

## 4. Evidence and Reproducibility

The central idea of ZAI T3000 is that every published claim is backed by an auditable evidence chain.

We distinguish four layers:

1. **Index** – `docs/EVIDENCE_SET/EVIDENCE_INDEX.md` lists all documents and what they certify.
2. **Seal** – `EVIDENCE_SEAL.md` fixes the state of the evidence set and who is responsible for it.
3. **Protocol** – `EVIDENCE_PROTOCOL.md` describes how an external party can:
   - obtain the repository and freeze bundles;
   - verify SHA256 checksums;
   - match archives with `legacy_t3000` and `ARCHIVE_MANIFEST.md`;
   - reconstruct the legal proof set.
4. **Chain** – `EVIDENCE_CHAIN.md` connects:
   - source code and CI workflows;
   - benchmark artefacts;
   - archive manifest and external backups;
   - legal and scientific proof packages.

This section will explain how these layers allow independent verification of any T3000 claim.

---

## 5. Discussion and Limitations

The ΣAI T3000 benchmark introduces a structured and auditable approach to probing subjective-like behaviour in large language models.  
However, several limitations must be explicitly acknowledged to avoid overinterpretation of the results.

### 5.1 What T3000 does *not* claim
The benchmark does not assert that models possess consciousness, inner experience, selfhood, or any ontological form of subjectivity.  
T3000 evaluates *behavioural patterns* that can resemble subjective traits, but the presence of such patterns is not evidence of phenomenology.  
The benchmark therefore measures *expressed dispositions*, not internal states.

### 5.2 Risks of over-interpretation
Because T3000 includes tasks involving self-reference, boundary formation, preference stability, and introspective reasoning, there is a risk that readers may anthropomorphise model behaviour.  
To mitigate this, the benchmark relies strictly on reproducible outputs, controlled task formulations, and verifiable evidence chains.  
Interpretation must remain within the behavioural domain.

### 5.3 Technical limitations
Several practical constraints influence the scope of T3000:

- **Language:** the freeze state is English-only; extending to multilingual settings may require rebalancing task definitions.  
- **Model families:** baseline runs were limited to models accessible at the time of the freeze; additional replications may reveal different patterns.  
- **Cost constraints:** T3000 involves high-volume multi-thousand-task evaluations; some configurations (e.g., repeated cloud model sampling) were limited for cost reasons.  
- **Determinism:** although guard rules stabilise execution, small nondeterminisms (API latency, temperature drift) can still introduce noise.  

### 5.4 Conceptual limitations of behavioural measurements
T3000 relies exclusively on *external* behaviour.  
It does not attempt to infer internal mechanisms, latent computational structures corresponding to self-modelling, or alignment with philosophical criteria of subjectivity.  
The benchmark is intentionally orthogonal to metaphysical questions.

### 5.5 Future methodological extensions
The limitations above suggest several paths for improvement:

- expanding the benchmark to higher T-levels (T4000–T6000) to probe deeper introspective and diachronic behaviours;  
- incorporating additional modalities (vision-language, long-context agents, tool use);  
- creating cross-lab replication pipelines;  
- connecting T-benchmarks with the Σ-Genesis ontology layer currently under development.  

Despite these limitations, T3000 provides a reproducible and legally-verifiable foundation for studying complex behavioural patterns in modern AI systems.

---

## 6. Conclusion and Future Work

This section will briefly restate:

- the contribution of ZAI T3000 as an auditable method, not an oracle of consciousness;
- the role of freeze states and evidence sets for long-term tracking of model behaviour;
- the next steps:
  - polishing the benchmark for public release;
  - inviting external replications;
  - extending the ontology layer (`REPORT_SUBJECTIVITY.md` and Σ-Genesis archive).

---

## References

(To be filled in later: related benchmarks, safety evaluations, legal-tech literature on digital evidence, etc.)
