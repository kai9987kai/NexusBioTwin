# PFAS Brine Counterfactual Frontier Program

- Mission ID: `pfas_brine_frontier_001`
- Domain: `environmental_biodesign`
- Risk tier: `high`

## Active Innovation Modules

- **Multi-Model Ensemble Genomic Engine (Evo 2 + GENERator + AlphaGenome)**
- **Epigenomic Landscape Analyzer (EpiAgent-style CRE perturbation)**
- **Cell-Free Rapid Prototyping Planner**
- **Bayesian Optimization Closed-Loop Experiment Design**
- **Sim-to-Real Transfer Bridge for BioControl**
- **Counterfactual Variant Atlas for What-If Regulatory Design**
- **Multi-Objective Pareto Frontier Planner**
- **FAIR Provenance and Twin Fidelity Bundle**

## Objective

Design a safe, uncertainty-aware PFAS brine polishing program with explicit what-if edit analysis, Pareto frontier ranking, and FAIR twin provenance.

## Integrated idea

NexusBioTwin turns a mission spec into a cross-scale plan that starts with genome design, filters through protein and enzyme triage, tests habitat and consortium behavior under stress, and ends in a closed-loop controller plan.

The stack centers Evo 2 as the genomic proposal engine while preserving strict human review and audit boundaries.

### Multi-Model Ensemble Strategy

This mission activates the multi-model ensemble engine with: **Evo 2, AlphaGenome, GENErator**. Each candidate is scored by all models independently, then a calibrated ensemble score is computed. Inter-model disagreements are flagged for human review.

### Epigenomic Landscape Analysis

Targeted CRE analysis for: **pfas_response_promoters, stress_response_cre, efflux_regulators**. The epigenomic analyzer encodes chromatin accessibility into cell sentences and predicts the regulatory impact of CRE perturbations using EpiAgent-style bidirectional attention.

### Counterfactual Variant Atlas

The planner builds an explicit what-if table for genome edits rather than only emitting ranked candidates. This makes the output more useful for human review, because each proposed intervention is paired with predicted upside, uncertainty, and exclusion windows.

### Cell-Free Rapid Prototyping

Before committing to full chassis engineering, this mission gates constructs through cell-free validation using: **e_coli_extract, bacillus_extract**. This shortens the design-build-test cycle from weeks to hours.

### Multi-Objective Frontier Planning

The planner preserves a Pareto frontier over: **pfas_reduction, community_stability, energy_efficiency, biosafety_margin**. This avoids hiding safety, resilience, or energy penalties inside a single aggregate score.

### Bayesian Optimization Strategy

- Objective: `maximize_pfas_reduction_under_energy_and_safety_constraints`
- Search dimensions: `nutrient_feed, flow_rate, oxygen_pulse, temperature`
- Acquisition function: `expected_hypervolume_improvement`
- Batch size: `3`
- Max iterations: `18`

The cognitive digital twin runs surrogate model updates after each batch, recomputing the acquisition surface to select the next set of experiment arms.

### Sim-to-Real Transfer Bridge

- Simulation environment: `habitat_twin_brine_reactor`
- Real environment: `pilot_scale_brine_reactor`
- Calibration strategy: `earth_analog_stepwise`
- Transfer validation: `bench_then_pilot`

Domain randomization ranges:

- `salinity_psu`: [38, 47]
- `temperature_c`: [22, 33]
- `toxin_load`: [0.7x, 1.4x]
- `sensor_noise`: [low, high]

### FAIR Provenance Bundle

- Bundle targets: `data, models, workflows, assays`
- Twin fidelity metrics: `prediction_error, transfer_gap, controller_stability_margin`
- Assay lineage required: `True`

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

### 2. ensemble_genome_design

- Goal: Use Evo 2, AlphaGenome, GENErator to score variants, embed genomic neighborhoods, and propose candidate regulatory programs for Pseudomonas_putida, Bacillus_subtilis.
- Engine: Multi-Model Ensemble Engine
- Influences: ArcInstitute/evo2, DNA-Helix
- Review required: True
- Outputs:
  - candidate edit bundles
  - regulatory program rankings
  - uncertainty notes
  - per-model score breakdown (Evo 2, GENERator, AlphaGenome)
  - calibrated ensemble rankings
  - inter-model disagreement flags
- Research anchors:
  - https://www.nature.com/articles/s41586-026-10176-5
  - https://doi.org/10.1038/s41586-025-10014-0
  - https://doi.org/10.1101/2024.08.16.608288
  - https://arxiv.org/abs/2502.07272
  - https://doi.org/10.1038/s41592-025-02578-2

### 3. epigenomic_landscape

- Goal: Analyze chromatin accessibility patterns and plan CRE perturbation simulations for regulatory targets: pfas_response_promoters, stress_response_cre, efflux_regulators.
- Engine: EpiAgent-style scATAC encoder
- Influences: EpiAgent, LoRNASH
- Review required: True
- Outputs:
  - cre_perturbation_matrix
  - chromatin_state_predictions
  - regulatory_circuit_map
  - in-silico knockout impact scores
- Research anchors:
  - https://doi.org/10.1038/s41592-025-02597-z
  - https://doi.org/10.1101/2024.10.31.621427

### 4. counterfactual_variant_atlas

- Goal: Construct a counterfactual regulatory atlas that answers mission-specific what-if edit questions: What if stress-response promoters are strengthened while efflux burden is capped?; What if toxin-quench activation is delayed until salinity spike recovery?; What edits increase PFAS reduction without degrading community stability?.
- Engine: Counterfactual atlas planner
- Influences: ArcInstitute/evo2, AlphaGenome
- Review required: True
- Outputs:
  - variant impact atlas
  - regulatory what-if table
  - safe edit exclusion list
  - uncertainty-ranked intervention windows
- Research anchors:
  - https://www.nature.com/articles/s41586-026-10176-5
  - https://doi.org/10.1038/s41586-025-10014-0
  - https://doi.org/10.1101/2024.08.16.608288

### 5. protein_triage

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

### 6. cell_free_prototyping

- Goal: Design cell-free validation experiments using e_coli_extract, bacillus_extract to test candidate constructs before committing to full chassis engineering.
- Engine: Cell-free experiment planner
- Influences: Safe-SDL, AI-CFPS
- Review required: True
- Outputs:
  - cfps_experiment_designs
  - rapid_screening_matrix
  - go_no_go_criteria
  - expected_yield_estimates
- Research anchors:
  - https://doi.org/10.1021/acssynbio.4c00671
  - https://doi.org/10.1016/j.synbio.2025.01.003
  - https://arxiv.org/abs/2602.09466

### 7. habitat_twin

- Goal: Stress-test consortium behavior against habitat shocks and deployment conditions: salinity_spike, toxin_surge, nutrient_drop, temperature_excursion.
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

### 8. multiobjective_frontier

- Goal: Compute a Pareto frontier across mission tradeoffs to avoid collapsing the search into a single score. Frontier objectives: pfas_reduction, community_stability, energy_efficiency, biosafety_margin.
- Engine: Pareto frontier planner
- Influences: Bayesian-Optimization, Habitat twin, Consortium control
- Review required: True
- Outputs:
  - pareto frontier candidates
  - tradeoff matrix
  - dominated candidate rejects
  - budget-aware follow-up recommendations
- Research anchors:
  - https://doi.org/10.1002/bit.28929
  - https://doi.org/10.1016/j.bej.2025.109618
  - https://arxiv.org/abs/2511.08571

### 9. bayesian_experiment_design

- Goal: Plan adaptive Bayesian optimization loops to maximize maximize_pfas_reduction_under_energy_and_safety_constraints over search dimensions [nutrient_feed, flow_rate, oxygen_pulse, temperature] using expected_hypervolume_improvement acquisition with batch size 3 for up to 18 iterations.
- Engine: BO acquisition planner with cognitive digital twin
- Influences: Bayesian-Optimization, Cognitive-Digital-Twin
- Review required: True
- Outputs:
  - experiment_arms
  - acquisition_function_policy
  - stopping_criteria
  - expected_improvement_surface
  - surrogate_model_spec
- Research anchors:
  - https://doi.org/10.1002/bit.28929
  - https://doi.org/10.1016/j.bej.2025.109618
  - https://doi.org/10.1016/j.bej.2024.109547

### 10. controller_design

- Goal: Compile a BioControl DSL policy over the control surface: pH, nutrient_feed, temperature, light_cycle, flow_rate, toxin_quench, oxygen_pulse. Include sim-to-real transfer bridge from habitat_twin_brine_reactor to pilot_scale_brine_reactor.
- Engine: BioControl DSL planner + Sim-to-Real Transfer Bridge
- Influences: NeuroPulse-CableLab, NeuroFusion-Reactor, Dual-DT-RL
- Review required: True
- Outputs:
  - controller templates
  - closed-loop observability plan
  - intervention escalation rules
  - domain_randomization_spec (habitat_twin_brine_reactor → pilot_scale_brine_reactor)
  - transfer_gap_estimate
  - calibration_protocol (earth_analog_stepwise)
  - reality_gap_test_matrix
- Research anchors:
  - https://doi.org/10.1038/s41586-025-08829-y
  - https://doi.org/10.1088/1741-4326/ae34c6
  - https://arxiv.org/abs/2511.08571
  - https://doi.org/10.3390/s25030601
  - https://doi.org/10.48550/arXiv.2502.14371

### 11. safety_red_team

- Goal: Stress-test the proposed plan against misuse, blocked traits, autonomy creep, and hidden safety regressions. Disallowed traits: antibiotic_selection_marker, mammalian_pathogenicity_signal, unbounded_horizontal_transfer.
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

### 12. fair_provenance_bundle

- Goal: Package the twin as a FAIR artifact bundle with explicit provenance, model lineage, and assay traceability targets for data, models, workflows, assays.
- Engine: FAIR twin bundle planner
- Influences: FAIR digital twins, OmniForge, nexusflow
- Review required: False
- Outputs:
  - artifact lineage graph
  - model and assay provenance bundle
  - twin fidelity checklist
  - reproducibility handoff pack
- Research anchors:
  - https://doi.org/10.1038/s44185-025-00116-3
  - https://arxiv.org/abs/2602.09466

### 13. orchestration_and_review

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
- Flag all inter-model disagreements above threshold for human review.
- Gate full organism engineering behind successful cell-free validation.
- Validate sim-to-real transfer in Earth-analog chambers before any deployment.
- Enforce stopping criteria and budget limits on Bayesian optimization loops.
- Preserve explicit no-go edit zones in the counterfactual atlas.
- Keep safety and resilience as first-class Pareto objectives, not soft penalties.

## Success metrics

- pfas_reduction
- community_stability
- energy_efficiency
- controller_resilience
- biosafety_margin
