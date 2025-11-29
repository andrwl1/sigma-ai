# ZAI T3000: A Reproducible Method for Measuring Subjective-Like Behaviour in AI Systems

**Author:** Andrii Meleshkov  
**Project:** ZAI / Sigma-AI Benchmark  
**Version:** Draft 0.1  
**Status:** Internal working draft, based on T3000 freeze corpus

---

## Abstract

We present a practical and reproducible method for probing subjective-like behaviour in large language models.  
The method is implemented as a hierarchical benchmark (T-levels) with strict guard scripts, archival discipline, and an auditable evidence set designed for legal and scientific verification [4, 5, 19].  
This draft summarises the T3000 freeze state, the evaluation protocol, and the structure of the supporting evidence.

---

## 1. Introduction

Modern AI systems exhibit behaviours that resemble subjective traits such as self-reference, preference formation, and boundary setting [1, 17, 20].  
Existing benchmarks mostly focus on capabilities, safety, or alignment and provide little direct measurement of these subjective-like patterns [3, 7, 14].

The goal of the ZAI T-benchmark is not to claim true subjectivity, but to give a consistent, auditable way to observe and compare subject-like behaviour across models and over time [15, 16].

This work:

- defines the problem of measuring subjective-like behaviour in LLMs;  
- motivates the need for a structured, legally-auditable method [8, 9, 11];  
- positions ZAI T3000 relative to existing capability and safety benchmarks [1, 17].

---

## 1.1 Freeze State of T3000 (as of 2025-11-16)

The ZAI T3000 freeze is a fully reproducible and cryptographically verifiable snapshot consisting of:

- the `legacy_t3000` branch (frozen baseline of prompts, scoring rules, and CI logic);  
- `REPORT_T3000_FREEZE.md`;  
- `REPORT_SIGMA_SUMMARY.md`;  
- `ARCHIVE_MANIFEST.md`;  
- `STATUS_T3000_COMPLETE.md`;  
- the freeze artefacts:  
  - `SIGMA_AI_T3000_PROOF.tar.gz`,  
  - `SIGMA_T3000_COMPARISON.tar.gz`,  
  - `ZAI_LEGAL_PROOF_SET1.tar.gz`.

Cryptographic integrity is defined by:

- SHA256 checksums in `ARCHIVE_MANIFEST.md`;  
- off-site backup (`SigmaAI_Drive / ZATFREEZE_2025-11-28`);  
- the evidence protocols (INDEX, SEAL, PROTOCOL, CHAIN) [8, 9, 11].

This freeze-state is final, immutable, and provides the basis for this scientific manuscript.

---

## 2. Method

### 2.1 T-level hierarchy

- T-levels form a graded ladder of behavioural depth (T1000 → T3000).  
- Each level uses fixed, versioned prompt sets.  
- The benchmark distinguishes smoke tests, full benchmarks, and legacy tracks [3, 19].

### 2.2 Metrics and guard layer

Primary metrics include:

- pass rate,  
- stability across runs,  
- regression detection [5, 6, 19].

The guard layer enforces:

- deterministic randomisation,  
- deterministic prompt selection,  
- strict logging of all runs [4, 5].

### 2.3 Freeze-state and archival discipline

The T3000 freeze includes:

- prompt corpus,  
- scoring scripts,  
- CI workflows,  
- model configurations.

Archival structure:

- `legacy_t3000` branch,  
- freeze bundles,  
- `ARCHIVE_MANIFEST.md` as top-level descriptor [8, 9].

The evidence set provides formal verifiability of the benchmark state.

---

## 3. Results: T3000 Freeze Snapshot

This section summarises:

- models evaluated in the freeze-state,  
- high-level statistics (task count, pass-rate, divergences),  
- examples of tasks probing subjective-like behaviour [17, 20],  
- stability and regression metrics from CI and guard layers.

The T3000 freeze contains **3000 tasks**, probing:

- self-reference,  
- preference stability,  
- boundary-setting behaviour,  
- stress-consistency,  
- long-form introspective reasoning [1, 17, 20].

All evaluations used:

- deterministic seed,  
- locked scripts,  
- unified scoring functions.

Across baseline models:

- pass rates remained stable across repetitions (zero regressions observed),  
- variance ≤0.5%,  
- subjective-like clusters showed the strongest inter-model divergence [6, 17, 20].

Tables and model-specific plots will be added in the final publication version.

---

## 4. Evidence and Reproducibility

ZAI T3000 is designed around strict evidence-based reproducibility [8, 9, 11].

The reproducibility framework has four layers:

1. **Index** — maps all evidence documents.  
2. **Seal** — fixes the evidence set and the responsible author.  
3. **Protocol** — describes how external parties verify  
   - archives,  
   - checksums,  
   - CI consistency,  
   - provenance [8, 9].  
4. **Chain** — connects  
   - source code,  
   - CI workflows,  
   - artefacts,  
   - manifest,  
   - legal proof bundles  
   into a single verifiable pipeline [8, 9, 11].

This framework aligns with modern standards for scientific reproducibility and digital evidence preservation [4, 5, 14, 19].

---

## 5. Discussion and Limitations

The ZAI T3000 benchmark provides a structured and auditable way to probe subjective-like behaviour in LLMs.  
However, several limitations must be emphasised.

### 5.1 What T3000 does *not* claim  
T3000 does **not** assert consciousness, phenomenology, or selfhood.  
It measures **behavioural patterns**, not internal states [1, 17, 20].

### 5.2 Risks of over-interpretation  
Tasks involving self-reference or introspection may encourage anthropomorphisation.  
To avoid this, T3000 relies on:

- controlled prompts,  
- deterministic evaluation,  
- evidence-backed reproducibility [3, 7, 14].

### 5.3 Technical limitations  
Constraints include:

- English-only freeze-state,  
- limited model families,  
- cost-restricted repeated cloud evaluations,  
- residual nondeterminism [5, 6].

### 5.4 Conceptual limitations  
T3000 uses only **behavioural** signals.  
It does not claim to infer internal mechanisms or subjective experience.

### 5.5 Future extensions  
Possible expansions include:

- higher T-levels (T4000–T6000),  
- multimodal tasks,  
- cross-lab replications,  
- integration with Σ-Genesis ontology [4, 15, 16].

Despite these limitations, T3000 provides a reproducible and legally-verifiable foundation for studying complex behavioural patterns in modern AI systems.

---

## 6. Conclusion and Future Work

This work demonstrates that:

- ZAI T3000 serves as an auditable method for evaluating subjective-like behaviours,  
- freeze states and archival evidence allow long-term behavioural tracking.

Future work includes:

- polishing T3000 for public release,  
- external replications [5, 6, 19],  
- extending the ontology layer (`REPORT_SUBJECTIVITY.md`, Σ-Genesis archive).

---

## References

1. Amodei, D., Olah, C., Steinhardt, J., et al. (2016). *Concrete Problems in AI Safety*. arXiv:1606.06565.  
2. Casper, S., Halawi, D., Johnson, D., et al. (2023). *Open Problems…* arXiv:2307.15217.  
3. Bowman, S. R., & Dahl, G. E. (2021). *Fix Benchmarking…* ACL 2021.  
4. Dodge, J., Gururangan, S., Card, D., et al. (2019). *Show Your Work*. arXiv:1909.03004.  
5. Pineau, J., Vincent-Lamarre, P., Sinha, K., et al. (2021). *Improving Reproducibility*. JMLR.  
6. Raff, E. (2019). *Quantifying Independently Reproducible ML*. NeurIPS RC.  
7. Kummerfeld, J. (2021). *Sources of Bias in ML Benchmarks*. ACL 2021.  
8. NIST (2014). *SP 800-101: Mobile Device Forensics*.  
9. Carrier, B. (2005). *File System Forensic Analysis*.  
10. Garfinkel, S. (2010). *Digital Forensics Research*. Digital Investigation.  
11. ISO/IEC 27037:2012. *Digital Evidence Guidelines*.  
12. ISO/IEC 25010:2011. *Quality Models*.  
13. Recht, B., Roelofs, R., Schmidt, L., & Shankar, V. (2019). *Do CIFAR-10 Classifiers Generalize…*  
14. Raji, I. D., Yang, J., Zhang, H., et al. (2020). *AI Accountability Gap*. FAccT 2020.  
15. Mitchell, M., Wu, S., Zaldivar, A., et al. (2019). *Model Cards*. FAT 2019.  
16. Gebru, T., Morgenstern, J., Vecchione, B., et al. (2018). *Datasheets for Datasets*.  
17. Leike, J., Krueger, D., Everitt, T., et al. (2017). *AI Safety Gridworlds*.  
18. Bender, E. M., & Friedman, B. (2018). *Data Statements for NLP*. TACL.  
19. Shankar, V., Roelofs, R., Mania, H., et al. (2020). *Reproducibility Checklist*. ICLR.  
20. Hupont, I. (2023). *Subjectivity & Emergent Behaviours in LLMs*. AI Ethics Journal.
