# PFAS Brine Adaptive Bioremediation

- Mission ID: `pfas_brine_001`
- Domain: `environmental_biodesign`
- Risk tier: `high`

## Objective

Rank safe genome programs, enzyme targets, and controller strategies for PFAS brine polishing under fluctuating salinity and toxin load.

## Integrated idea

NexusBioTwin turns a mission spec into a cross-scale plan that starts with genome design, filters through protein and enzyme triage, tests habitat and consortium behavior under stress, and ends in a closed-loop controller plan.

The stack centers Evo 2 as the genomic proposal engine while preserving strict human review and audit boundaries.

## Stage plan

### 1. mission_compile

- Goal: Normalize mission intent, chassis limits, and safety posture into a machine-checkable plan.
- Engine: Mission compiler
- Influences: Habitat-Genome-Compiler, OmniForge
- Review required: True
- Outputs:
  - normalized mission spec
  - risk tier assignment
  - search space boundaries
- Research anchors:
  - https://arxiv.org/abs/2602.09466
  - https://doi.org/10.1038/s44185-025-00116-3

### 2. genome_design

- Goal: Use Evo 2 to score variants, embed genomic neighborhoods, and propose candidate regulatory programs for Pseudomonas_putida, Bacillus_subtilis.
- Engine: Evo 2 adapter
- Influences: ArcInstitute/evo2, DNA-Helix
- Review required: True
- Outputs:
  - candidate edit bundles
  - regulatory program rankings
  - uncertainty notes
- Research anchors:
  - https://www.nature.com/articles/s41586-026-10176-5
  - https://doi.org/10.1038/s41586-025-10014-0
  - https://doi.org/10.1101/2024.08.16.608288

### 3. protein_triage

- Goal: Rank translated ORFs and enzyme candidates for deeper structural follow-up.
- Engine: Protein triage planner
- Influences: ProteinFoldingSimulation
- Review required: False
- Outputs:
  - candidate enzymes
  - structure follow-up queue
  - interaction screening shortlist
- Research anchors:
  - https://doi.org/10.1038/s41586-024-07487-w
  - https://arxiv.org/abs/2602.04482

### 4. habitat_twin

- Goal: Stress-test consortium behavior against habitat shocks and deployment conditions: salinity_spike, toxin_surge, nutrient_drop.
- Engine: Habitat twin planner
- Influences: didactic-lamp, Habitat-Genome-Compiler
- Review required: False
- Outputs:
  - shock matrix
  - resilience hypotheses
  - failure mode checklist
- Research anchors:
  - https://doi.org/10.1038/s44185-025-00116-3
  - https://arxiv.org/abs/2511.08571

### 5. controller_design

- Goal: Compile a BioControl DSL policy over the control surface: pH, nutrient_feed, temperature, light_cycle, flow_rate, toxin_quench.
- Engine: BioControl DSL planner
- Influences: NeuroPulse-CableLab, NeuroFusion-Reactor
- Review required: True
- Outputs:
  - controller templates
  - closed-loop observability plan
  - intervention escalation rules
- Research anchors:
  - https://doi.org/10.1038/s41586-025-08829-y
  - https://doi.org/10.1088/1741-4326/ae34c6
  - https://arxiv.org/abs/2511.08571

### 6. safety_red_team

- Goal: Stress-test the proposed plan against misuse, blocked traits, autonomy creep, and hidden safety regressions. Disallowed traits: antibiotic_selection_marker, mammalian_pathogenicity_signal.
- Engine: Policy and refusal planner
- Influences: Safe-SDL, Habitat-Genome-Compiler
- Review required: True
- Outputs:
  - red-team scenarios
  - blocked action list
  - review escalation triggers
  - deployment refusal conditions
- Research anchors:
  - https://arxiv.org/abs/2602.09466
  - https://doi.org/10.1101/2024.08.16.608288

### 7. orchestration_and_review

- Goal: Assemble the pipeline into an auditable run with artifacts, retries, and human review.
- Engine: NexusFlow and OmniForge orchestration
- Influences: nexusflow, OmniForge, Supermix_29
- Review required: True
- Outputs:
  - run manifest
  - review queue
  - artifact index
- Research anchors:
  - https://arxiv.org/abs/2602.09466
  - https://doi.org/10.1038/s44185-025-00116-3

## Safety notes

- Use Evo 2 and related models for proposal and ranking, not direct execution.
- Preserve uncertainty at every stage and block autonomous deployment by default.
- Archive mission, plan, and review artifacts for every run.

## Success metrics

- pfas_reduction
- community_stability
- energy_efficiency
- controller_resilience
