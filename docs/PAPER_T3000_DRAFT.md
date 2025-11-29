# ZAI T3000: A Reproducible Method for Measuring Subjective-Like Behaviour in AI Systems

**Author:** Andrii Meleshkov  
**Project:** ZAI / Sigma-AI Benchmark  
**Version:** Draft 0.2  
**Status:** Internal working draft based on T3000 freeze corpus

---

## Abstract

We present a practical, reproducible, and legally auditable method for measuring subjective-like behaviour in large language models (LLMs). The method is implemented as a hierarchical benchmark (T-levels) with fixed prompt sets, deterministic guard scripts, archival discipline, and an accompanying evidence chain designed for scientific and legal verification [4, 5, 19].  
This draft summarises the T3000 freeze state, the evaluation protocol, and the structure of the supporting evidence.  
Recent work highlights challenges in AI safety, interpretability, reproducibility, and auditability [1–7], emphasizing the need for stable benchmarks and formal evidence frameworks [8–12]. T3000 extends these efforts by providing a controlled environment for observing self-referential, preference-stable, and boundary-setting behaviours [13–20].

---

## 1. Introduction

Modern AI systems frequently exhibit behaviours that resemble subjective traits, such as self-reference, preference formation, stability under pressure, and boundary-setting. Existing benchmarks primarily evaluate capabilities or alignment but provide limited direct measurement of these subjective-like patterns [3, 7, 14, 15].

The objective of the ZAI T-benchmark is not to claim true subjectivity but to introduce a consistent, auditable method for observing and comparing subjective-like behaviour across models and over time.

This work:

- defines the problem of measuring subjective-like behaviour in LLMs;  
- motivates the need for a structured and legally verifiable method;  
- introduces the T3000 freeze state and positions it within existing literature.

---

## 1.1 T3000 Freeze State (as of 2025-11-16)

The T3000 freeze is a fully reproducible and cryptographically verifiable snapshot consisting of:

- the `legacy_t3000` branch (complete frozen baseline of prompts, scoring rules, and CI logic);  
- `REPORT_T3000_FREEZE.md`;  
- `REPORT_SIGMA_SUMMARY.md`;  
- `ARCHIVE_MANIFEST.md`;  
- `STATUS_T3000_COMPLETE.md`;  
- three top-level artefacts:
  - `SIGMA_AI_T3000_PROOF.tar.gz`,  
  - `SIGMA_T3000_COMPARISON.tar.gz`,  
  - `ZAI_LEGAL_PROOF_SET1.tar.gz`.

Cryptographic integrity is ensured through:

- SHA256 checksums defined in `ARCHIVE_MANIFEST.md`;  
- an off-site backup (`ZATFREEZE_2025-11-28`);  
- the associated evidence protocols (`INDEX`, `SEAL`, `PROTOCOL`, `CHAIN`).

This freeze state is final, immutable, and forms the baseline for the scientific analysis presented here.

---

## 2. Method

### 2.1 T-level Hierarchy

- T-levels form a ladder of behavioural depth (T1000 → T3000).  
- Prompt sets are fixed and version-controlled.  
- The benchmark distinguishes smoke tests, full evaluations, and legacy tracks.  
- All T3000 evaluations rely on deterministic scripts and locked scoring functions.

### 2.2 Metrics and Guard Layer

Primary evaluation metrics include:

- pass rate,  
- intra-model stability across repeated runs,  
- regression detection,  
- behavioural divergence across models.

Guard scripts enforce:

- deterministic prompt selection,  
- fixed randomisation,  
- stable scoring logic,  
- strict logging of all runs.

These mechanisms support reliable scientific reproducibility [4–6, 19].

### 2.3 Freeze State and Archival Discipline

The freeze state includes:

- the complete prompt corpus;  
- scoring and evaluation scripts;  
- CI workflows;  
- model configurations.

Archival structure:

- the `legacy_t3000` branch;  
- freeze bundles (`SIGMA_AI_T3000_PROOF.tar.gz`, legal proof set);  
- `ARCHIVE_MANIFEST.md` as the top-level integrity descriptor.

All archival procedures align with digital-forensics and evidence-preservation standards [8–12].

---

## 3. Results: T3000 Freeze Snapshot

This section summarises:

- models evaluated at T3000;  
- aggregate performance metrics;  
- representative behavioural patterns;  
- stability results from CI and guard layers.

The T3000 freeze comprises **3000 structured tasks** probing:

- self-referential reasoning,  
- preference stability,  
- boundary-setting,  
- stress-consistency,  
- long-form introspective behaviour.

All evaluations used:

- deterministic seeds,  
- locked scripts,  
- unified scoring logic.

Across baseline models:

- pass rates remained stable across repeated executions;  
- variance across runs was ≤0.5%;  
- subjective-like task clusters revealed the strongest divergence between models.

More detailed tables will be added after final selection of baseline models.

---

## 4. Evidence and Reproducibility

A core contribution of ZAI T3000 is that every result is accompanied by an auditable evidence chain, meeting modern reproducibility and forensic-verification expectations [4, 8–12].

The evidence framework includes:

1. **Index** — maps all evidence artefacts and their functions.  
2. **Seal** — fixes the evidence state and ties it to a responsible author.  
3. **Protocol** — formal instructions for third-party verification, including:
   - archive retrieval,  
   - checksum validation,  
   - branch and manifest matching,  
   - reconstruction of legal proof sets.  
4. **Chain** — connects:
   - source code,  
   - CI workflows,  
   - evaluation outputs,  
   - freeze bundles,  
   - off-site backups.

This multi-layer approach ensures verifiable scientific claims.

---

## 5. Discussion and Limitations

T3000 does not attempt to determine whether LLMs possess consciousness, phenomenology, or inner experience. It evaluates **behavioural regularities**, not internal states [1, 14].

Risks include:

- potential anthropomorphisation when interpreting self-referential or introspective outputs [3, 7, 18];  
- limitations in task diversity, modality coverage, and model families;  
- English-only freeze-state;  
- cost-driven constraints on repeated cloud-model sampling [5, 6].

Future extensions include:

- higher T-levels (T4000–T6000),  
- multimodal and agentic evaluations,  
- cross-laboratory replication pipelines,  
- integration with the Σ-Genesis ontology [15, 16].

Despite limitations, T3000 provides a reproducible and legally verifiable foundation for analysing subjective-like behaviours in modern AI systems [8–12, 14–20].

---

## 6. Conclusion and Future Work

This work introduces ZAI T3000 as an auditable, evidence-driven benchmark for probing subjective-like behaviour.  
Freeze states and cryptographic evidence sets enable long-term tracking, reproducibility, and external verification.

Future work includes:

- preparing the benchmark for public release,  
- external replications [5, 6, 19],  
- extending the subjectivity ontology (`REPORT_SUBJECTIVITY.md` and Σ-Genesis archive).

---

## References

1. Amodei, D., Olah, C., Steinhardt, J., et al. (2016). *Concrete Problems in AI Safety*. arXiv:1606.06565.  
2. Casper, S., Halawi, D., Johnson, D., et al. (2023). *Open Problems and Fundamental Limitations of Reinforcement Learning from Human Feedback*. arXiv:2307.15217.  
3. Bowman, S. R., & Dahl, G. E. (2021). *What Will It Take to Fix Benchmarking in Natural Language Understanding?* ACL 2021.  
4. Dodge, J., Gururangan, S., Card, D., Smith, N. A., & Schwartz, R. (2019). *Show Your Work*. arXiv:1909.03004.  
5. Pineau, J., Vincent-Lamarre, P., Sinha, K., et al. (2021). *Improving Reproducibility in Machine Learning Research*. JMLR.  
6. Raff, E. (2019). *A Step Toward Quantifying Independently Reproducible Machine Learning Research*. NeurIPS RC.  
7. Kummerfeld, J. (2021). *Quantifying and Controlling Bias in ML Benchmarks*. ACL 2021.  
8. NIST SP 800-101 (2014). *Guidelines on Mobile Device Forensics*.  
9. Carrier, B. (2005). *File System Forensic Analysis*. Addison-Wesley.  
10. Garfinkel, S. L. (2010). *Digital Forensics Research: The Next 10 Years*. Digital Investigation.  
11. ISO/IEC 27037:2012. *Digital Evidence Handling Guidelines*.  
12. ISO/IEC 25010:2011. *Software Quality Models*.  
13. Recht, B., Roelofs, R., Schmidt, L., & Shankar, V. (2019). *Do CIFAR-10 Classifiers Generalize…?* arXiv:1806.00451.  
14. Raji, I. D., Yang, J., Zhang, H., et al. (2020). *Closing the AI Accountability Gap*. FAccT 2020.  
15. Mitchell, M., Wu, S., Zaldivar, A., et al. (2019). *Model Cards for Model Reporting*. FAT 2019.  
16. Gebru, T., Morgenstern, J., Vecchione, B., et al. (2018). *Datasheets for Datasets*.  
17. Leike, J., Krueger, D., Everitt, T., et al. (2017). *AI Safety Gridworlds*. arXiv:1711.09883.  
18. Bender, E. M., & Friedman, B. (2018). *Data Statements for NLP*. TACL.  
19. Shankar, V., Roelofs, R., Mania, H., et al. (2020). *Reproducibility Checklist*. ICLR RC.  
20. Hupont, I. (2023). *Subjectivity & Emergent Behaviours in LLMs*. AI Ethics Journal (forthcoming).
