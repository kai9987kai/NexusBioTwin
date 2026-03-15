# Research Basis

These papers anchor the NexusBioTwin concept.

## Genome and regulatory modeling

- AlphaGenome, published January 28, 2026:
  https://doi.org/10.1038/s41586-025-10014-0
- Genome modelling and design across all domains of life with Evo 2, published March 4, 2026:
  https://www.nature.com/articles/s41586-026-10176-5
- Sequence modeling and design from molecular to genome scale with Evo, published November 15, 2024:
  https://doi.org/10.1126/science.ado9336
- Benchmarking DNA Foundation Models for Genomic and Genetic Tasks:
  https://doi.org/10.1101/2024.08.16.608288
- GENERator: A Long-Context Generative Genomic Foundation Model, revised January 2026:
  https://arxiv.org/abs/2502.07272
- GPN-MSA: Genome-wide Variant Effect Prediction via Multispecies Alignment, published December 2025:
  https://doi.org/10.1038/s41592-025-02578-2

## Epigenomics and chromatin accessibility

- EpiAgent: Foundation Model for Single-Cell Epigenomic Data, published September 2025:
  https://doi.org/10.1038/s41592-025-02597-z
- LoRNASH: Long-Range RNA Foundation Model for Transcriptome Architecture, posted October 2024:
  https://doi.org/10.1101/2024.10.31.621427
- CellFM: a foundation model pre-trained on 100 million human cells for transcriptional system-level prediction, published June 26, 2025:
  https://www.nature.com/articles/s41467-025-59926-5

## Cell imaging and segmentation

- CellSAM, a foundation model for promptable cell segmentation, published January 24, 2026:
  https://doi.org/10.1038/s41592-025-02879-w

## Regulatory grammar and sequence perturbation

- Towards a foundation model of transcription in 213 human cell types, published January 8, 2025:
  https://doi.org/10.1038/s41586-024-08391-z
- Regulatory grammar in human promoters uncovered by MPRA-based deep learning, published February 11, 2026:
  https://doi.org/10.1038/s41586-025-10093-z
- STRAND: Prediction of sequence perturbation response in single cells from sequence alone, posted February 14, 2026:
  https://doi.org/10.48550/arXiv.2602.10156
- Benchmarking algorithms for generalizable single-cell perturbation response prediction, published December 11, 2025:
  https://doi.org/10.1038/s41592-025-02980-0

## Spatial microenvironments and niche modeling

- Nicheformer maps context-dependent cell-cell communication from single-cell and spatial transcriptomics at scale, published January 2, 2026:
  https://doi.org/10.1038/s41592-025-02814-z
- OmiCLIP: multimodal contrastive learning with visual-omics alignment for spatial biology, published May 29, 2025:
  https://doi.org/10.1038/s41592-025-02707-1
- VISTA: Visual Foundation Model Improves Spatial Transcriptomics Imputation and Annotation, published January 8, 2026:
  https://doi.org/10.1038/s42003-025-09479-6

## Protein structure and generation

- Accurate structure prediction of biomolecular interactions with AlphaFold 3, published May 8, 2024:
  https://doi.org/10.1038/s41586-024-07487-w
- SaDiT: Diffusion Transformer for Scalable Protein Backbone Generation, posted February 6, 2026:
  https://arxiv.org/abs/2602.04482

## Control and adaptive systems

- Foundation model of neural activity predicts response to new stimulus types, published April 9, 2025:
  https://doi.org/10.1038/s41586-025-08829-y
- Reconstruction-free magnetic control of DIII-D plasmas with deep reinforcement learning, published January 21, 2026:
  https://doi.org/10.1088/1741-4326/ae34c6
- A bioreactor-based architecture for in vivo model-based and sim-to-real learning control of microbial consortium composition, posted November 11, 2025:
  https://arxiv.org/abs/2511.08571

## Bayesian optimization for bioprocess engineering

- Bayesian Optimization in Bioprocess Engineering — Where Do We Stand Today, published March 2025:
  https://doi.org/10.1002/bit.28929
- Automated Regression of Bioreactor Models Using a Bayesian Approach for Parallel Cultivations (Cognitive Digital Twin), published March 2025:
  https://doi.org/10.1016/j.bej.2025.109618
- Integration of Bayesian Optimization and Solution Thermodynamics for Media Design, published 2025:
  https://doi.org/10.1016/j.bej.2024.109547

## Sim-to-real transfer and autonomous labs

- Dual Digital Twin Framework for Reinforcement Learning in Industrial Robotics, posted 2025:
  https://doi.org/10.3390/s25030601
- Zero-Shot Sim-to-Real Transfer for Robot Manipulation, published 2025:
  https://doi.org/10.48550/arXiv.2502.14371

## Cell-free synthetic biology

- AI-Optimized Cell-Free Protein Synthesis for Small Molecule Production, published 2025:
  https://doi.org/10.1021/acssynbio.4c00671
- Cell-Free Biomanufacturing: AI-Augmented Design and Enzymatic Precision, published 2025:
  https://doi.org/10.1016/j.synbio.2025.01.003
- Active learning-guided optimization of cell-free biosensors for lead testing in drinking water, published October 2, 2025:
  https://doi.org/10.1038/s41467-025-66964-6

## Autonomous protein engineering and biofoundries

- PLM-enabled automatic protein evolution in a self-driving biofoundry, published June 4, 2025:
  https://doi.org/10.1038/s41467-025-56751-8
- A generalized platform for AI-powered autonomous enzyme engineering, published June 12, 2025:
  https://doi.org/10.1038/s41467-025-61209-y

## Safety and digital twins

- Safe-SDL: Operational Design Domains, Control Barrier Functions, and CRUTD for AI-Driven Self-Driving Laboratories, posted February 20, 2026:
  https://doi.org/10.48550/arXiv.2602.15061
- LABSHIELD: Benchmarking agentic AI safety in scientific laboratories, posted March 12, 2026:
  https://arxiv.org/abs/2603.11987
- Benchmarking large language models on safety risks in scientific laboratories, published January 14, 2026:
  https://www.nature.com/articles/s42256-025-01152-1
- FAIR digital twins for biodiversity: enabling data, model, and workflow integration, published February 2, 2026:
  https://doi.org/10.1038/s44185-025-00116-3

## Design implications

- Use Evo 2 as the center of the genome design layer, with GENERator and AlphaGenome as ensemble partners.
- Treat genome and protein models as proposal and ranking systems, not as truth.
- Add a counterfactual variant atlas so reviewable what-if edit analysis is preserved alongside rankings.
- Add epigenomic context via EpiAgent-style CRE perturbation analysis.
- Add CellFM-style atlas transfer so candidate edits can be grounded against large reference cell-state banks.
- Add regulatory grammar and perturbation-conditioned sequence planning so promoter rewrites are ranked with cell-state context.
- Add explicit perturbation generalization benchmarks so zero-shot edit predictions are stress-tested on unseen contexts.
- Add CellSAM-style segmentation and morphology QC before microscopy-derived evidence feeds the spatial twin.
- Preserve spatial niche context so structured habitats and consortia are not reduced to bulk averages.
- Fuse imaging and transcriptomic evidence with explicit uncertainty budgets before trusting imputed spatial signals.
- Add active-learning cell-free biosensor loops to prioritize selectivity and field-deployable screening without brute-force search.
- Add autonomous protein evolution planning so biofoundry rounds, mutant budgets, and assay gates are preserved as first-class artifacts.
- Preserve a Pareto frontier over safety, resilience, energy, and mission performance instead of one blended score.
- Use Bayesian optimization with cognitive digital twins for adaptive experiment design.
- Plan explicit sim-to-real calibration for every controller policy before deployment.
- Compile an operational safety envelope with ODD bounds, barrier monitors, and transaction-safe commit rules.
- Add hazard-audit layers that benchmark refusal gaps and reasoning blind spots before escalation.
- Gate organism-level engineering behind cell-free rapid prototyping.
- Keep explicit safety gates around autonomous planning.
- Build digital twin artifacts that preserve data, model, and workflow provenance.

## Phase 6 Upgrades (2026 Breakthroughs)

- **Quantum Simulation / Drug Discovery**: Accelerate molecular folding via hybrid Quantum-Classical simulations like Berkeley Lab's AQuaRef and IBM Heron cluster models.
- **Agentic Edge-AI Swarms**: Unify deployment of tiny SLMs to Edge nodes (robots/bioreactors) for autonomous, zero-latency microbial swarm orchestration in extreme environments.
- **Zero-Knowledge Proof (ZKP) BioSecure Twins**: Safeguard biological data sovereignty by securing IIoT digital twins behind cryptographic ZK-Proofs. Protects proprietary bioreactor parameters and patient biomaterial from leakage.

## Phase 7 Horizon (2026-2027 Synthetics)

- **Hachimoji DNA / Xenobiology**: Expanding the canonical 4-letter DNA alphabet to 8 letters (A, T, C, G, Z, P, S, B). This creates true molecular orthogonality, establishing a "genetic firewall" that mathematically prevents horizontal gene transfer with natural biospheres.
- **DNA Data Storage & Bio-Hybrid Computing**: Engineering synthetic DNA interacting with semiconducting perovskite materials to create low-power neuromorphic memory resistors, turning living cell consortia into extreme-density data storage drives.
- **Spatial-FM Whole-Cell Simulation**: Utilizing foundation models trained on spatial transcriptomics (like scSpatialSIM) to simulate true 3D whole-cell physics, moving beyond isolated protein pathways to full spatial cellular context modeling.
