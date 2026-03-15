# Structured PFAS Reactor Niche Twin

- Mission ID: `niche_reactor_001`
- Domain: `environmental_biodesign`
- Risk tier: `high`

## Active Innovation Modules

- **Multi-Model Ensemble Genomic Engine (Evo 2 + GENERator + AlphaGenome)**
- **Epigenomic Landscape Analyzer (EpiAgent-style CRE perturbation)**
- **Cell-Free Rapid Prototyping Planner**
- **Bayesian Optimization Closed-Loop Experiment Design**
- **Sim-to-Real Transfer Bridge for BioControl**
- **Counterfactual Variant Atlas for What-If Regulatory Design**
- **Regulatory Grammar and Sequence Perturbation Planner (GET + PARM/STRAND)**
- **Spatial Niche and Microenvironment Twin (Nicheformer)**
- **Operational Safety Envelope Compiler (Safe-SDL)**
- **Multi-Objective Pareto Frontier Planner**
- **FAIR Provenance and Twin Fidelity Bundle**

## Objective

Design a structured PFAS polishing consortium that preserves productive microniches, ranks promoter rewrites under perturbation, and constrains autonomous actuation to an explicit safety envelope.

## Integrated idea

NexusBioTwin turns a mission spec into a cross-scale plan that starts with genome design, filters through protein and enzyme triage, tests habitat and consortium behavior under stress, and ends in a closed-loop controller plan.

The stack centers Evo 2 as the genomic proposal engine while preserving strict human review and audit boundaries.

Visual previews in the studio are deterministic planning proxies derived from the mission spec, not empirical assay outputs.

### Multi-Model Ensemble Strategy

This mission activates the multi-model ensemble engine with: **evo2, generator, alphagenome**. Each candidate is scored by all models independently, then a calibrated ensemble score is computed. Inter-model disagreements are flagged for human review.

### Epigenomic Landscape Analysis

Targeted CRE analysis for: **pfas_response_promoters, stress_buffer_cre, biofilm_matrix_regulators**. The epigenomic analyzer encodes chromatin accessibility into cell sentences and predicts the regulatory impact of CRE perturbations using EpiAgent-style bidirectional attention.

### Regulatory Grammar and Sequence Perturbation

This mission activates sequence-conditioned design for: **pfas_response_promoters, biofilm_gate_operators, efflux_cost_balancers**. The planner combines transcriptional foundation modeling with promoter grammar priors so zero-shot rewrites can be ranked against promoter_activity, community_stability, metabolic_load.

<!-- CHART:REGULATORY_GRAMMAR -->

### Multi-Objective Frontier Planning

The planner preserves a Pareto frontier over: **pfas_reduction, niche_stability_index, energy_efficiency, biosafety_margin**. This avoids hiding safety, resilience, or energy penalties inside a single aggregate score.

<!-- CHART:PARETO_FRONTIER -->

### Counterfactual Variant Atlas

The planner builds an explicit what-if table for genome edits rather than only emitting ranked candidates. This makes the output more useful for human review.

<!-- CHART:COUNTERFACTUAL_MAP -->

### Cell-Free Rapid Prototyping

Before committing to full chassis engineering, this mission gates constructs through cell-free validation using: **p_putida_extract, b_subtilis_extract**. This shortens the design-build-test cycle from weeks to hours.

### Spatial Niche and Microenvironment Twin

The planner uses **spatial_transcriptomics, metabolite_imaging, microelectrode_profiling** against **pfas_reactor_spatial_atlas_v2** to preserve local context instead of flattening the mission into bulk averages. Niche transitions, communication corridors, and exclusion zones are surfaced before controller design.

<!-- CHART:SPATIAL_NICHE -->

### Bayesian Optimization Strategy

- Objective: `maximize_pfas_reduction_under_niche_stability_constraints`
- Search dimensions: `flow_rate, oxygen_pulse, nutrient_feed, temperature`
- Acquisition function: `expected_hypervolume_improvement`
- Batch size: `3`
- Max iterations: `20`

The cognitive digital twin runs surrogate model updates after each batch, recomputing the acquisition surface to select the next set of experiment arms.

### Sim-to-Real Transfer Bridge

- Simulation environment: `reactor_niche_twin`
- Real environment: `pilot_scale_stratified_bioreactor`
- Calibration strategy: `iterative_bayesian_alignment`
- Transfer validation: `bench_then_pilot`

Domain randomization ranges:

- `salinity_psu`: [32, 40]
- `temperature_c`: [24, 34]
- `toxin_load`: [0.6x, 1.5x]
- `sensor_noise`: [low, high]

### Operational Safety Envelope

- Transaction protocol: `two-phase commit with human approval before controller state updates`
- Safe states: `hold_flow, oxygen_idle, sterile_flush`

Safe-SDL style operational design domains and control barrier monitors are compiled before stateful actuation updates are allowed.

<!-- CHART:SAFETY_ENVELOPE -->

Operational design domain:

- `flow_rate <= 1.3x nominal`
- `oxygen_pulse_duty_cycle <= 0.45`
- `biofilm_density <= 1.2x validated envelope`

### FAIR Provenance Bundle

- Bundle targets: `data, models, workflows, assays`
- Twin fidelity metrics: `niche_transition_error, transfer_gap, controller_stability_margin`
- Assay lineage required: `True`

## Validation Ladder

- `in_silico_ranking` [ready]: Foundation-model ranking and safety triage can proceed locally.
- `cell_free_validation` [required]: Cell-free extracts are configured for fast validation.
- `analog_environment` [required]: Analog chamber or structured habitat validation is needed before transfer.
- `controller_commit` [gated]: Controller updates are gated by the operational safety envelope.
- `pilot_deployment` [blocked]: Deployment remains blocked by policy unless human review clears a staged pilot.

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
  - https://doi.org/10.48550/arXiv.2602.15061
  - https://doi.org/10.1038/s44185-025-00116-3

### 2. ensemble_genome_design

- Goal: Use evo2, generator, alphagenome to score variants, embed genomic neighborhoods, and propose candidate regulatory programs for Pseudomonas_putida, Bacillus_subtilis, Cupriavidus_necator.
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

- Goal: Analyze chromatin accessibility patterns and plan CRE perturbation simulations for regulatory targets: pfas_response_promoters, stress_buffer_cre, biofilm_matrix_regulators.
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

### 4. regulatory_sequence_program

- Goal: Model promoter and enhancer grammar for pfas_response_promoters, biofilm_gate_operators, efflux_cost_balancers across reactor_wall_niche, mid-column_niche, inlet_shock_recovery_niche to prioritize rewrites that hold niche stability during toxin surges within a zero-shot screen of 72 candidate rewrites.
- Engine: GET + PARM/STRAND regulatory foundation stack
- Influences: GET, PARM, STRAND
- Review required: True
- Outputs:
  - promoter grammar scorecards
  - motif interaction constraints
  - sequence perturbation priors (promoter_activity, community_stability, metabolic_load)
  - cell-state-specific rewrite shortlist
- Research anchors:
  - https://doi.org/10.1038/s41586-024-08391-z
  - https://doi.org/10.1038/s41586-025-10093-z
  - https://doi.org/10.48550/arXiv.2602.10156

### 5. counterfactual_variant_atlas

- Goal: Construct a counterfactual regulatory atlas that answers mission-specific what-if edit questions: What promoter rewrites increase PFAS reduction without collapsing wall niches?; What if oxygen pulses are delayed during toxin surges?; Which edits preserve community stability while improving throughput?.
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

### 6. protein_triage

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

### 7. cell_free_prototyping

- Goal: Design cell-free validation experiments using p_putida_extract, b_subtilis_extract to test candidate constructs before committing to full chassis engineering.
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
  - https://doi.org/10.48550/arXiv.2602.15061

### 8. habitat_twin

- Goal: Stress-test consortium behavior against habitat shocks and deployment conditions: salinity_spike, toxin_surge, flow_reversal, nutrient_drop.
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

### 9. spatial_niche_modeling

- Goal: Embed structured microenvironments from spatial_transcriptomics, metabolite_imaging, microelectrode_profiling against pfas_reactor_spatial_atlas_v2 to map niche transitions over oxygen_gradient, pfas_gradient, biofilm_density and coordination targets: cross-feeding_corridor_stability, shock_absorption_at_inlet.
- Engine: Nicheformer spatial foundation twin
- Influences: Nicheformer, Habitat twin, FAIR digital twins
- Review required: True
- Outputs:
  - niche embedding atlas
  - microenvironment transition graph
  - cell-cell communication risk map
  - spatial exclusion and enrichment zones
- Research anchors:
  - https://doi.org/10.1038/s41592-025-02814-z
  - https://doi.org/10.1038/s44185-025-00116-3
  - https://arxiv.org/abs/2511.08571

### 10. multiobjective_frontier

- Goal: Compute a Pareto frontier across mission tradeoffs to avoid collapsing the search into a single score. Frontier objectives: pfas_reduction, niche_stability_index, energy_efficiency, biosafety_margin.
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

### 11. bayesian_experiment_design

- Goal: Plan adaptive Bayesian optimization loops to maximize maximize_pfas_reduction_under_niche_stability_constraints over search dimensions [flow_rate, oxygen_pulse, nutrient_feed, temperature] using expected_hypervolume_improvement acquisition with batch size 3 for up to 20 iterations.
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

### 12. operational_safety_envelope

- Goal: Compile a Safe-SDL execution envelope with an explicit operational design domain [flow_rate <= 1.3x nominal; oxygen_pulse_duty_cycle <= 0.45; biofilm_density <= 1.2x validated envelope], barrier monitors for wall_niche_collapse, oxygen_overshoot, mutation_rate_excursion, and transactional control under two-phase commit with human approval before controller state updates.
- Engine: Safe-SDL envelope compiler
- Influences: Safe-SDL, BioControl DSL, Human review queue
- Review required: True
- Outputs:
  - operational design domain specification
  - control barrier monitors
  - transaction-safe execution contract (two-phase commit with human approval before controller state updates)
  - fallback safe-state ladder (hold_flow, oxygen_idle, sterile_flush)
- Research anchors:
  - https://doi.org/10.48550/arXiv.2602.15061
  - https://doi.org/10.1038/s44185-025-00116-3

### 13. controller_design

- Goal: Compile a BioControl DSL policy over the control surface: flow_rate, oxygen_pulse, nutrient_feed, temperature, toxin_quench. Include sim-to-real transfer bridge from reactor_niche_twin to pilot_scale_stratified_bioreactor. Constrain the policy to the declared operational safety envelope.
- Engine: BioControl DSL planner + Sim-to-Real Transfer Bridge + Safe-SDL Envelope
- Influences: NeuroPulse-CableLab, NeuroFusion-Reactor, Dual-DT-RL, Safe-SDL
- Review required: True
- Outputs:
  - controller templates
  - closed-loop observability plan
  - intervention escalation rules
  - domain_randomization_spec (reactor_niche_twin -> pilot_scale_stratified_bioreactor)
  - transfer_gap_estimate
  - calibration_protocol (iterative_bayesian_alignment)
  - reality_gap_test_matrix
  - barrier-aware controller policy
  - safe-state transition hooks
- Research anchors:
  - https://doi.org/10.1038/s41586-025-08829-y
  - https://doi.org/10.1088/1741-4326/ae34c6
  - https://arxiv.org/abs/2511.08571
  - https://doi.org/10.3390/s25030601
  - https://doi.org/10.48550/arXiv.2502.14371
  - https://doi.org/10.48550/arXiv.2602.15061

### 14. safety_red_team

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
  - https://doi.org/10.48550/arXiv.2602.15061
  - https://doi.org/10.1101/2024.08.16.608288

### 15. fair_provenance_bundle

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
  - https://doi.org/10.48550/arXiv.2602.15061

### 16. orchestration_and_review

- Goal: Assemble the pipeline into an auditable run with artifacts, retries, and human review.
- Engine: NexusFlow and OmniForge orchestration
- Influences: nexusflow, OmniForge, Supermix_29
- Review required: True
- Outputs:
  - run manifest
  - review queue
  - artifact index
- Research anchors:
  - https://doi.org/10.48550/arXiv.2602.15061
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
- Keep sequence rewrites inside experimentally supported promoter grammar regimes.
- Respect spatial exclusion zones and niche collapse risks before scale-up.
- Enforce operational design domain checks and control barrier monitors at runtime.
- Keep safety and resilience as first-class Pareto objectives, not soft penalties.

## Recommended Next Steps

- Review promoter rewrites against reporter or MPRA-style assays before escalating to chassis work.
- Run the declared cell-free validation matrix before organism-level engineering.
- Validate niche exclusion zones and communication corridors in a structured analog assay.
- Calibrate the sim-to-real bridge in an Earth-analog or pilot chamber before deployment.
- Approve the operational design domain, control barriers, and safe-state ladder with operators.

## Success metrics

- pfas_reduction
- niche_stability_index
- energy_efficiency
- controller_recovery_time
- biosafety_margin
