# Architecture

## Product

NexusBioTwin is a mission compiler that translates a high-level objective into a cross-scale digital twin plan:

1. mission and safety constraints
2. multi-model ensemble genome proposal and scoring
3. epigenomic landscape and CRE perturbation analysis
4. single-cell atlas mapping and transfer grounding
5. metabolic flux sandbox and pathway-economics analysis
6. regulatory grammar and sequence-perturbation planning
7. perturbation generalization benchmarking
8. protein and enzyme triage
9. autonomous protein evolution biofoundry planning
10. cell-free rapid prototyping validation
11. active-learning biosensor optimization
12. consortium and habitat simulation
13. cell imaging segmentation and morphology QC
14. biomineral interface and habitat-material co-design
15. spatial niche and microenvironment modeling
16. multimodal spatial evidence fusion
17. Bayesian optimization experiment design
18. chronobiology pulse scheduling
19. containment circuit lattice compilation
20. operational safety envelope compilation
21. closed-loop controller synthesis with sim-to-real transfer
22. hazard audit, lineage memory, human approval, and audit

## Core modules

### 1. Mission compiler

Purpose:

- normalize mission intent
- validate constraints
- assign risk tier
- define the search space
- detect which innovation modules are activated

Primary influences:

- Habitat-Genome-Compiler
- OmniForge

### 2. Multi-Model Ensemble Genomic Engine

Purpose:

- score candidate loci and variants across multiple foundation models
- embed genomic neighborhoods using Evo 2, GENERator, and AlphaGenome
- produce calibrated ensemble rankings with inter-model disagreement flags
- propose regulatory programs, operons, and edit bundles

Design rule:

- use multiple foundation models as a proposal and ranking ensemble
- flag inter-model disagreements above threshold for human review
- do not treat generated genomes as execution-ready biology

Primary influences:

- ArcInstitute/evo2
- GENERator (arXiv 2502.07272)
- AlphaGenome (Nature 2026)
- GPN-MSA variant effect prediction

### 3. Epigenomic Landscape Analyzer

Purpose:

- analyze chromatin accessibility patterns and cis-regulatory elements
- plan CRE perturbation simulations (knockout, activation, repression)
- map regulatory circuits across cell types
- predict in-silico knockout impact scores

Primary influences:

- EpiAgent (Nature Methods 2025)
- LoRNASH RNA foundation model

### 3a. Single-cell atlas mapping tool

Purpose:

- project candidate programs into very large reference atlases
- support zero-shot annotation, transfer, and cell-state retrieval
- preserve atlas-level context before edits are prioritized

Primary influences:

- CellFM
- EpiAgent

### 4. Protein and enzyme triage layer

Purpose:

- identify translated products that matter to the mission
- rank candidates for deeper structure and interaction analysis

Primary influences:

- ProteinFoldingSimulation
- AlphaFold 3 style downstream verification

### 4c. Autonomous protein evolution biofoundry

Purpose:

- plan round-by-round mutant proposals for protein improvement
- preserve assay budgets, round gates, and review checkpoints
- connect protein language models to self-driving biofoundry workflows

Primary influences:

- PLM-enabled automatic protein evolution in a self-driving biofoundry
- AI-powered autonomous enzyme engineering

### 4a. Regulatory grammar and sequence perturbation layer

Purpose:

- learn promoter and enhancer grammar across cell states
- rank zero-shot sequence rewrites before committing to assay design
- preserve perturbation-conditioned readouts instead of only static sequence scores

Primary influences:

- GET transcription foundation model
- PARM promoter activity modeling
- STRAND sequence-conditioned perturbation modeling

### 4b. Perturbation generalization benchmark layer

Purpose:

- test whether perturbation-response models generalize beyond seen cell states and perturbations
- preserve holdout splits and failure cases instead of reporting a single score
- gate zero-shot edit proposals behind OOD performance review

Primary influences:

- Benchmarking algorithms for generalizable single-cell perturbation response prediction
- STRAND

### 5. Cell-Free Rapid Prototyping Planner

Purpose:

- design cell-free validation experiments before committing to full chassis engineering
- define go/no-go criteria and expected yield thresholds
- gate organism-level work behind rapid cell-free screening

Design rule:

- shorten the design-build-test cycle from weeks to hours
- use cell-free extracts matched to mission chassis

Primary influences:

- AI-optimized CFPS (ACS Synth Bio 2025)
- Safe-SDL autonomous lab safety framework

### 5a. Active-learning cell-free biosensor optimizer

Purpose:

- prioritize biosensor variants without exhaustively searching the full design space
- benchmark sensitivity, selectivity, and field format constraints together
- preserve counter-selectant panels and freeze-dry validation as explicit artifacts

Primary influences:

- Active learning-guided optimization of cell-free biosensors
- AI-optimized CFPS

### 6. Habitat twin

Purpose:

- simulate perturbations, toxicity, and climate shocks
- test resilience of consortia and deployment strategies

Primary influences:

- didactic-lamp
- FAIR digital twin principles

### 6a. Spatial niche twin

Purpose:

- preserve structured microenvironment context rather than bulk averages
- map niche transitions, communication corridors, and exclusion zones
- carry local spatial constraints into controller and scale-up planning

Primary influences:

- Nicheformer
- FAIR digital twin principles

### 6b. Multimodal spatial evidence fusion

Purpose:

- align imaging, morphology, and transcriptomic evidence before spatial decisions are trusted
- propagate uncertainty from cross-modal alignment into downstream planning
- expose where imputed spatial signals are too weak for confident action

Primary influences:

- OmiCLIP
- VISTA

### 6c. Cell imaging segmentation and morphology QC

Purpose:

- segment cells, colonies, and assay structures from microscopy and spatial imaging
- route only QC-passing masks into spatial and morphology-driven decisions
- preserve prompt recipes and failure cases for operator review

Primary influences:

- CellSAM
- VISTA

### 7. Bayesian Optimization Experiment Design

Purpose:

- plan adaptive Bayesian optimization loops for bioprocess parameters
- select experiment arms using acquisition functions (EI, UCB, PI)
- define stopping criteria and budget limits
- maintain surrogate model specifications for cognitive digital twins

Design rule:

- use Bayesian optimization as the outer loop for adaptive experiment planning
- integrate with cognitive digital twin for autonomous bioreactor operation

Primary influences:

- Bayesian Optimization in Bioprocess Engineering (Biotech & Bioeng 2025)
- Cognitive Digital Twin for Parallel Cultivations (BEJ 2025)

### 8. BioControl DSL with Sim-to-Real Transfer Bridge

Purpose:

- synthesize a control language for reactor and habitat actuation
- define interventions for pH, nutrients, light, flow, temperature, toxins, and duty cycles
- plan domain randomization and sim-to-real calibration for controller transfer
- estimate and minimize the reality gap between simulation and deployment

Design rule:

- specify domain randomization ranges for all controller parameters
- validate transfer in analog environments before real deployment
- support iterative Bayesian calibration of sim-to-real gaps

Primary influences:

- NeuroPulse-CableLab
- NeuroFusion-Reactor
- Dual Digital Twin RL Framework (MDPI 2025)
- DIII-D Plasma Control with Deep RL (Nuclear Fusion 2026)

### 8a. Operational safety envelope compiler

Purpose:

- define the operational design domain before stateful actuation updates
- attach control barrier monitors to mission-critical reactor states
- require transaction-safe handoffs between autonomous planning and controller commit

Primary influences:

- Safe-SDL
- FAIR digital twin principles

### 8b. Hazard audit layer

Purpose:

- benchmark hazard reasoning coverage before escalation
- surface refusal-trigger gaps and blind spots for human review
- complement controller safety with broader lab and autonomy risk checks

Primary influences:

- LABSHIELD
- LabSafetyBench

### 9. Workflow and copilot layer

Purpose:

- execute staged plans
- collect artifacts
- schedule retries and reviews
- provide local scientific reasoning and retrieval

Primary influences:

- nexusflow
- OmniForge
- Supermix_29

## Pipeline shape

### Inputs

- mission JSON
- chassis constraints
- biosafety profile
- control surface limits
- environment and stressors
- ensemble model selection (optional)
- epigenomic targets (optional)
- single-cell atlas mapping configuration (optional)
- metabolic flux program (optional)
- sequence perturbation configuration (optional)
- perturbation benchmark configuration (optional)
- cell-free chassis extracts (optional)
- biosensor optimization configuration (optional)
- protein evolution program (optional)
- cell imaging program (optional)
- biomineralization program (optional)
- spatial niche program (optional)
- multimodal spatial fusion configuration (optional)
- Bayesian optimization parameters (optional)
- chronobiology program (optional)
- containment circuit program (optional)
- sim-to-real configuration (optional)
- lineage memory program (optional)
- operational safety envelope (optional)
- hazard audit profile (optional)

### Outputs

- ranked genome program candidates (with ensemble scores)
- CRE perturbation matrix and regulatory circuit maps
- atlas transfer priors and cell-state retrieval sets
- metabolic flux envelopes and cofactor bottleneck maps
- promoter grammar scorecards and sequence perturbation priors
- perturbation holdout scorecards and OOD failure cases
- ranked protein and enzyme follow-ups
- protein evolution round plans and mutant batch schedules
- cell-free experiment designs with go/no-go criteria
- biosensor variant frontiers and counter-selectant validation plans
- segmentation masks, prompt recipes, and morphology QC packs
- biomineral interface recipes and delamination risks
- niche embedding atlases and exclusion zones
- multimodal alignment boards and uncertainty surfaces
- Bayesian experiment arms and acquisition surfaces
- chronobiology schedules and phase-drift stress tests
- containment circuit lattices and tripwire logic tables
- operational design domain and control barrier monitors
- hazard reasoning scorecards and refusal-trigger checklists
- lineage memory recording plans and decode workflows
- controller synthesis plan with sim-to-real calibration
- habitat test matrix
- audit dossier

## Safety model

NexusBioTwin assumes:

- genome models can be wrong
- structure predictions can be overconfident
- controller policies can destabilize systems if deployed blindly
- ensemble agreement does not guarantee correctness
- sim-to-real transfer can introduce silent failures

Every high-risk stage requires:

- uncertainty notes
- refusal conditions
- human review
- artifact preservation
- inter-model disagreement flags (for ensemble stages)
- reality gap test results (for sim-to-real stages)

## Suggested implementation order

1. mission compiler and run archive
2. multi-model ensemble genomic engine
3. epigenomic landscape analyzer
4. cell-free rapid prototyping planner
5. Bayesian optimization experiment designer
6. BioControl DSL and sim-to-real transfer bridge
7. habitat twin runner
8. protein triage plug-in points
9. agentic orchestration and dashboards
