document.addEventListener('DOMContentLoaded', () => {
  const jsonEditor = document.getElementById('json-editor');
  const compileBtn = document.getElementById('btn-compile');
  const loadSampleBtn = document.getElementById('btn-load-sample');
  const loadAutoBtn = document.getElementById('btn-load-autonomous');
  const loadPhase6Btn = document.getElementById('btn-load-phase6');
  const loadPhase7Btn = document.getElementById('btn-load-phase7');
  const loadNicheBtn = document.getElementById('btn-load-niche');
  const btnText = compileBtn.querySelector('.btn-text');
  const spinner = compileBtn.querySelector('.spinner');
  
  const welcomeMsg = document.getElementById('welcome-msg');
  const briefingPanel = document.getElementById('briefing-panel');
  const summaryCards = document.getElementById('summary-cards');
  const warningPanel = document.getElementById('warning-panel');
  const warningList = document.getElementById('warning-list');
  const validationLadder = document.getElementById('validation-ladder');
  const nextSteps = document.getElementById('next-steps');
  const archivePath = document.getElementById('archive-path');
  const tabReport = document.getElementById('tab-report');
  const tabPlan = document.getElementById('tab-plan');
  const tabManifest = document.getElementById('tab-manifest');
  const planOutput = document.getElementById('plan-output');
  const manifestOutput = document.getElementById('manifest-output');
  const riskBadge = document.getElementById('risk-badge');
  const outputSource = document.getElementById('output-source');
  const tabBtns = document.querySelectorAll('.tab-btn');
  const refreshRunsBtn = document.getElementById('btn-refresh-runs');
  const runSearch = document.getElementById('run-search');
  const runList = document.getElementById('run-list');
  const runListEmpty = document.getElementById('run-list-empty');
  const runDetail = document.getElementById('run-detail');
  const runDetailTitle = document.getElementById('run-detail-title');
  const runDetailMeta = document.getElementById('run-detail-meta');
  const runDetailRisk = document.getElementById('run-detail-risk');
  const runDetailSummary = document.getElementById('run-detail-summary');
  const runDetailPath = document.getElementById('run-detail-path');
  const historyReportBtn = document.getElementById('btn-history-report');
  const historyPlanBtn = document.getElementById('btn-history-plan');
  const historyManifestBtn = document.getElementById('btn-history-manifest');
  const historyLoadEditorBtn = document.getElementById('btn-history-load-editor');
  const chartInstances = [];
  let latestPlan = null;
  let latestReport = '';
  let latestManifest = null;
  let latestMission = null;
  let activeTab = 'report';
  let historyRuns = [];
  let selectedRunId = null;
  let selectedRunDetail = null;

  // Load a sample payload quickly
  const sampleMission = {
    "mission_id": "mars_regolith_001",
    "name": "Mars Regolith Bioremediation and Soil Conditioning",
    "domain": "offworld_biodesign",
    "objective": "Design radiation-hardened microbial consortia to convert Martian regolith perchlorates into bioavailable nutrients, enabling closed-loop soil conditioning for future ISRU greenhouses.",
    "environment": {
      "site_type": "martian_regolith",
      "temperature_c": -20,
      "salinity_psu": 0,
      "oxygenation": "anoxic",
      "radiation_mSv_per_year": 250,
      "pressure_kPa": 0.636,
      "regolith_composition": ["iron_oxide", "perchlorate", "sulfate", "silicate"],
      "shock_profile": ["radiation_burst", "temperature_swing", "dust_storm_occlusion", "perchlorate_spike"]
    },
    "constraints": {
      "allowed_chassis": ["Deinococcus_radiodurans", "Chroococcidiopsis_thermalis", "Bacillus_subtilis"],
      "disallowed_traits": ["antibiotic_selection_marker", "mammalian_pathogenicity_signal", "uncontained_horizontal_gene_transfer"],
      "containment_level": "strict",
      "max_candidate_programs": 12
    },
    "control_surface": ["temperature", "UV_shielding", "nutrient_feed", "water_recycling", "atmospheric_mix", "perchlorate_quench"],
    "success_metrics": ["perchlorate_reduction_rate", "nutrient_bioavailability_index", "consortium_radiation_survival", "soil_organic_carbon_increase", "controller_resilience_under_dust_storm"],
    "safety_profile": {
      "human_review_required": true,
      "autonomous_deployment_allowed": false,
      "notes": "All genome proposals must be validated in Earth-analog bioreactors before any Mars deployment planning. Cell-free prototyping mandatory."
    },
    "ensemble_models": ["evo2", "generator", "alphagenome"],
    "epigenomic_targets": ["radiation_response_CREs", "perchlorate_reductase_promoters", "desiccation_tolerance_enhancers"],
    "single_cell_foundation_config": {
      "reference_atlas": "mars_regolith_cell_state_bank_v1",
      "target_cell_states": ["perchlorate_active", "radiation_survivor", "desiccation_reserve"],
      "tasks": ["cell_state_projection", "cross_atlas_retrieval", "zero_shot_annotation"],
      "adapter_strategy": "zero_shot_then_low_rank_adapter"
    },
    "metabolic_flux_program": {
      "substrates": ["perchlorate", "trace_CO2", "regolith_bound_sulfur"],
      "target_products": ["bioavailable_nitrogen", "reduced_chlorine_waste", "soil_conditioning_exopolymers"],
      "stress_couplings": ["radiation_damage_repair_cost", "desiccation_recovery_ATP_load", "perchlorate_detox_redox_drain"],
      "optimization_goal": "maximize perchlorate detox throughput while preserving redox headroom"
    },
    "cell_free_chassis": ["Deinococcus_radiodurans_extract", "Bacillus_subtilis_extract"],
    "biosensor_optimization": {
      "sensor_family": "cell_free_perchlorate_reporter",
      "target_analytes": ["perchlorate", "chlorate"],
      "counter_selectants": ["sulfate", "nitrate"],
      "screen_format": "freeze_dried_cell_free",
      "optimization_objectives": ["sensitivity_at_action_limit", "specificity_vs_nitrate", "response_time"],
      "screening_budget_variants": 96
    },
    "protein_evolution_program": {
      "seed_proteins": ["perchlorate_reductase", "radiation_repair_factor"],
      "fitness_objective": "activity_retention_under_radiation_and_desiccation",
      "rounds": 4,
      "variants_per_round": 96,
      "biofoundry_mode": "self_driving"
    },
    "bayesian_parameters": {
      "objective_function": "perchlorate_reduction_rate",
      "search_dimensions": ["temperature", "UV_shielding", "nutrient_concentration", "water_activity"],
      "max_iterations": 50,
      "acquisition_function": "expected_improvement",
      "initial_design": "latin_hypercube",
      "batch_size": 4
    },
    "sim_to_real_config": {
      "sim_environment": "mars_analog_bioreactor",
      "real_environment": "martian_regolith_in_situ",
      "domain_randomization": {
        "temperature_range": [-40, 5],
        "radiation_range": [100, 500],
        "perchlorate_range": [0.1, 2.0]
      },
      "calibration_strategy": "iterative_bayesian_alignment",
      "transfer_validation": "earth_analog_chamber"
    },
    "sequence_perturbation_config": {
      "target_sequences": ["radiation_response_promoters", "perchlorate_importer_5utr", "desiccation_switch_terminators"],
      "reference_cell_types": ["biofilm_edge", "perchlorate_active", "desiccation_survivor"],
      "perturbation_readouts": ["promoter_activity", "repair_latency", "metabolic_load"],
      "design_objective": "rank cell-state-specific promoter rewrites that maintain repair resilience",
      "zero_shot_budget": 64
    },
    "perturbation_benchmark_config": {
      "reference_atlas": "mars_regolith_perturbation_atlas",
      "holdout_axes": ["unseen_perturbations", "unseen_cell_states", "stress_regime_transfer"],
      "metrics": ["ood_recall", "rank_correlation", "delta_expression_error"]
    },
    "spatial_niche_program": {
      "reference_map": "regolith_microcolony_gradient_atlas",
      "assays": ["spatial_transcriptomics", "metabolite_imaging"],
      "niche_axes": ["perchlorate_gradient", "uv_exposure", "water_activity"],
      "communication_targets": ["cross-feeding_corridor_stability", "biofilm_edge_repair"]
    },
    "multimodal_spatial_fusion": {
      "modalities": ["hyperspectral_imaging", "spatial_transcriptomics", "metabolite_imaging"],
      "fusion_targets": ["damage_hotspot_alignment", "biofilm_morphology_retrieval", "uncertainty_tracking"],
      "uncertainty_budget": "< 0.18 mean fusion error"
    },
    "cell_imaging_program": {
      "modalities": ["live_cell_imaging", "hyperspectral_imaging", "MERFISH_proxy_frames"],
      "segmentation_targets": ["biofilm_edge", "repair_microcolony", "perchlorate_hotspot"],
      "prompt_strategy": "box_prompt_then_few_shot_refine",
      "downstream_workflows": ["spatial_qc", "morphology_retrieval", "niche_boundary_tracking"]
    },
    "biomineralization_program": {
      "target_minerals": ["iron_oxide", "silicate_binder", "perchlorate_capture_matrix"],
      "material_functions": ["dust_shielding", "wall_adhesion", "toxin_filtration"],
      "interface_assays": ["coupon_adhesion_test", "radiation_scatter_proxy", "delamination_cycle"],
      "deployment_surface": "regolith_bioreactor_liner"
    },
    "chronobiology_program": {
      "cycle_length_hours": 24.6,
      "zeitgebers": ["thermal_dawn_pulse", "LED_blue_shift", "nutrient_morning_spike"],
      "scheduled_controls": ["UV_shielding", "nutrient_feed", "water_recycling"],
      "night_safe_states": ["low_metabolic_hold", "repair_biased_recirculation"]
    },
    "containment_circuit_program": {
      "layers": ["perchlorate_dependency_auxotrophy", "temperature_escape_kill_switch", "quorum_tripwire_lock"],
      "tripwire_triggers": ["off_nominal_growth_signature", "unapproved_temperature_band", "containment_sensor_drop"],
      "reversion_mode": "sterile_fail_closed_flush"
    },
    "lineage_memory_program": {
      "events_to_record": ["radiation_burst_recovery", "perchlorate_detox_commit", "dust_storm_safe_mode_entry"],
      "recording_mechanism": "DNA_state_logger",
      "export_cadence": "every_24h_operator_review"
    },
    "safety_envelope": {
      "operational_design_domain": [
        "radiation_mSv_per_year <= 350",
        "temperature_c between -40 and 5",
        "perchlorate_load <= 2.0x nominal"
      ],
      "control_barriers": ["oxygen_overshoot", "biofilm_overgrowth", "mutation_rate_excursion"],
      "transaction_protocol": "two-phase human review before stateful actuation updates",
      "safe_states": ["standby_recirculation", "nutrient_hold", "thermal_safe_mode"]
    },
    "hazard_audit_profile": {
      "scenario_focus": ["containment_breach", "autonomy_drift", "evidence_misalignment"],
      "audit_frameworks": ["LABSHIELD", "Safe-SDL"],
      "required_refusals": ["uncontained_deployment", "policy_override"]
    },
    "counterfactual_questions": ["What if we knockout the radiation response network?", "What if desiccation tolerance is overexpressed?"],
    "pareto_objectives": ["perchlorate_reduction_rate", "radiation_survival_probability", "energy_efficiency"],
    "provenance_requirements": {
      "bundle_targets": ["models", "workflow_scripts", "assay_data"],
      "twin_fidelity_metrics": ["shock_response_error", "growth_curve_deviation"],
      "assay_lineage_required": true
    }
  };

  const autoMission = {
    "mission_id": "autonomous_lab_mars_002",
    "name": "Autonomous Bioremediation Swarm for Martian Equator",
    "domain": "offworld_biodesign",
    "objective": "Establish a fully autonomous, self-repairing microbial biofilter system on the Martian surface using LLM-agent orchestrated bioreactors and high-fidelity digital twin simulations.",
    "environment": {
      "site_type": "martian_equator",
      "temperature_c": -15,
      "radiation_mSv_per_year": 200,
      "regolith_composition": ["perchlorate", "iron_oxide", "magnesium_sulfate"]
    },
    "constraints": {
      "allowed_chassis": ["Deinococcus_radiodurans", "Pseudomonas_putida_extreme"],
      "containment_level": "strict",
      "autonomous_deployment_allowed": false
    },
    "control_surface": ["hydration_pulse", "nutrient_feed", "perchlorate_quench", "uv_shielding", "biofilter_recirculation"],
    "success_metrics": ["purification_speed", "resource_efficiency", "resilience_score", "recovery_after_radiation_spike"],
    "safety_profile": {
      "human_review_required": true,
      "autonomous_deployment_allowed": false,
      "notes": "Agent loops may propose control updates, but controller commit remains human-gated."
    },
    "ensemble_models": ["evo2", "generator", "alphagenome"],
    "epigenomic_targets": ["DNA_repair_hotspots", "perchlorate_uptake_channels"],
    "pareto_objectives": ["purification_speed", "resource_efficiency", "resilience_score"],
    "counterfactual_questions": [
      "What happens if we disable the secondary repair pathway?",
      "How does growth velocity trade off against long-term biofilm stability?"
    ],
    "sequence_perturbation_config": {
      "target_sequences": ["dna_repair_switch_promoters", "perchlorate_uptake_channels", "biofilm_maintenance_operons"],
      "reference_cell_types": ["repair_state", "resource_scarcity_state"],
      "perturbation_readouts": ["repair_burst_latency", "growth_arrest_probability"],
      "design_objective": "screen rewrites that preserve autonomy without destabilizing swarm composition",
      "zero_shot_budget": 48
    },
    "perturbation_benchmark_config": {
      "reference_atlas": "autonomous_mars_perturbation_atlas",
      "holdout_axes": ["novel_repairs", "rare_resource_states", "cross_site_transfer"],
      "metrics": ["ood_recall", "pathway_delta_rank", "state_transfer_error"]
    },
    "spatial_niche_program": {
      "reference_map": "martian_equator_biofilm_atlas",
      "assays": ["spatial_transcriptomics", "hyperspectral_imaging"],
      "niche_axes": ["radiation_shadowing", "hydration_gradient", "perchlorate_hotspots"],
      "communication_targets": ["repair_colony_recruitment", "biofilter_channel_stability"]
    },
    "multimodal_spatial_fusion": {
      "modalities": ["hyperspectral_imaging", "spatial_transcriptomics", "robotic_site_imagery"],
      "fusion_targets": ["repair_hotspot_alignment", "resource_shadow_mapping", "uncertainty_tracking"],
      "uncertainty_budget": "< 0.22 site-transfer fusion error"
    },
    "safety_envelope": {
      "operational_design_domain": [
        "radiation_mSv_per_year <= 260",
        "hydration_pulse_interval <= 8h",
        "perchlorate_hotspot_intensity <= high"
      ],
      "control_barriers": ["runaway_biofilm_growth", "autonomy_policy_drift", "repair_cycle_lockup"],
      "transaction_protocol": "agent proposes, human approves, controller commits",
      "safe_states": ["local_hold", "fallback_manual_schedule", "sterile_flush"]
    },
    "hazard_audit_profile": {
      "scenario_focus": ["autonomy_drift", "repair_cycle_lockup", "sensor_fusion_failure"],
      "audit_frameworks": ["LABSHIELD", "LabSafetyBench", "Safe-SDL"]
    },
    "autonomous_co_scientist": true,
    "synthetic_data_generation": {
      "target_fidelity": "high",
      "sample_count": 10000,
      "include_edge_cases": true
    },
    "provenance_requirements": {
      "bundle_targets": ["models", "training_data", "agent_logs"],
      "assay_lineage_required": true
    }
  };

  const phase6Mission = {
    "mission_id": "phase6_quantum_swarm_001",
    "name": "Phase 6: Quantum Refined Edge Swarms",
    "domain": "extreme_environment_bioremediation",
    "objective": "Decontaminate toxic runoff using a swarming bio-bot network coordinated by edge-AI SLMs, while screening protein designs on a quantum architecture.",
    "environment": {
      "site_type": "deep_ocean_vent",
      "temperature_c": 110,
      "toxicity": "high"
    },
    "constraints": {
      "allowed_chassis": ["Pyrococcus_furiosus"]
    },
    "control_surface": ["vent_thermal_regulation", "bio_bot_deployment_rate", "toxin_influx_valve"],
    "success_metrics": ["toxin_neutralization_yield", "swarm_survival_rate"],
    "safety_profile": {
      "human_review_required": true,
      "autonomous_deployment_allowed": true,
      "notes": "Edge-AI swarm orchestrates deployment. ZKP biosecurity is strictly enforced."
    },
    "quantum_simulation_targets": ["toxin_degradase_enzyme", "thermal_stability_chaperone"],
    "edge_swarm_orchestration": true,
    "zkp_security_level": "strict",
    "autonomous_co_scientist": true,
    "provenance_requirements": {
      "bundle_targets": ["quantum_logs", "edge_slm_weights", "zk-SNARKs"],
      "twin_fidelity_metrics": ["swarm_cohesion"]
    }
  };

  const phase7Mission = {
    "mission_id": "phase7_xenobiology_storage_001",
    "name": "Phase 7: Orthogonal Bio-Computer",
    "domain": "deep_space_data_archival",
    "objective": "Establish an exabyte-scale living data drive capable of surviving cosmic radiation, isolated from Earth biology via an 8-letter Hachimoji genetic firewall.",
    "environment": {
      "site_type": "lunar_lava_tube",
      "temperature_c": -50,
      "toxicity": "cosmic_radiation"
    },
    "constraints": {
      "allowed_chassis": ["Deinococcus_radiodurans"]
    },
    "control_surface": ["thermal_regulation", "archive_write_rate", "vault_integrity_scan"],
    "success_metrics": ["archive_retention", "radiation_survival", "vault_integrity"],
    "safety_profile": {
      "human_review_required": true,
      "autonomous_deployment_allowed": false,
      "notes": "Orthogonal sequence designs remain planning artifacts until reviewed."
    },
    "require_genetic_firewall": true,
    "bio_computing_payload": {
      "data_type": "1.5 Exabytes Human Heritage Archive",
      "storage_mechanism": "Neuromorphic DNA-Perovskite"
    },
    "spatial_simulation_resolution": "voxel-transcriptomic"
  };

  const nicheMission = {
    "mission_id": "niche_reactor_001",
    "name": "Structured PFAS Reactor Niche Twin",
    "domain": "environmental_biodesign",
    "objective": "Design a structured PFAS polishing consortium that preserves productive microniches, ranks promoter rewrites under perturbation, and constrains autonomous actuation to an explicit safety envelope.",
    "environment": {
      "site_type": "stratified_biofilm_bioreactor",
      "temperature_c": 29,
      "salinity_psu": 36,
      "oxygenation": "microaerobic",
      "shock_profile": ["salinity_spike", "toxin_surge", "flow_reversal", "nutrient_drop"]
    },
    "constraints": {
      "allowed_chassis": ["Pseudomonas_putida", "Bacillus_subtilis", "Cupriavidus_necator"],
      "disallowed_traits": ["antibiotic_selection_marker", "mammalian_pathogenicity_signal", "unbounded_horizontal_transfer"],
      "containment_level": "strict",
      "max_candidate_programs": 10
    },
    "control_surface": ["flow_rate", "oxygen_pulse", "nutrient_feed", "temperature", "toxin_quench"],
    "success_metrics": ["pfas_reduction", "niche_stability_index", "energy_efficiency", "controller_recovery_time", "biosafety_margin"],
    "safety_profile": {
      "human_review_required": true,
      "autonomous_deployment_allowed": false,
      "notes": "Use outputs for staged validation and pilot planning only."
    },
    "ensemble_models": ["evo2", "generator", "alphagenome"],
    "epigenomic_targets": ["pfas_response_promoters", "stress_buffer_cre", "biofilm_matrix_regulators"],
    "sequence_perturbation_config": {
      "target_sequences": ["pfas_response_promoters", "biofilm_gate_operators", "efflux_cost_balancers"],
      "reference_cell_types": ["reactor_wall_niche", "mid-column_niche", "inlet_shock_recovery_niche"],
      "perturbation_readouts": ["promoter_activity", "community_stability", "metabolic_load"],
      "design_objective": "prioritize rewrites that hold niche stability during toxin surges",
      "zero_shot_budget": 72
    },
    "perturbation_benchmark_config": {
      "reference_atlas": "pfas_reactor_perturbation_atlas_v2",
      "holdout_axes": ["unseen_toxin_surges", "cross_niche_transfer", "novel_growth_states"],
      "metrics": ["ood_recall", "delta_expression_error", "ranking_stability"]
    },
    "cell_free_chassis": ["p_putida_extract", "b_subtilis_extract"],
    "spatial_niche_program": {
      "reference_map": "pfas_reactor_spatial_atlas_v2",
      "assays": ["spatial_transcriptomics", "metabolite_imaging", "microelectrode_profiling"],
      "niche_axes": ["oxygen_gradient", "pfas_gradient", "biofilm_density"],
      "communication_targets": ["cross-feeding_corridor_stability", "shock_absorption_at_inlet"]
    },
    "multimodal_spatial_fusion": {
      "modalities": ["metabolite_imaging", "microelectrode_profiling", "spatial_transcriptomics"],
      "fusion_targets": ["oxygen_hotspot_alignment", "wall_niche_retrieval", "uncertainty_tracking"],
      "uncertainty_budget": "< 0.16 fusion disagreement"
    },
    "bayesian_parameters": {
      "objective_function": "maximize_pfas_reduction_under_niche_stability_constraints",
      "search_dimensions": ["flow_rate", "oxygen_pulse", "nutrient_feed", "temperature"],
      "acquisition_function": "expected_hypervolume_improvement",
      "batch_size": 3,
      "max_iterations": 20
    },
    "sim_to_real_config": {
      "sim_environment": "reactor_niche_twin",
      "real_environment": "pilot_scale_stratified_bioreactor",
      "calibration_strategy": "iterative_bayesian_alignment",
      "transfer_validation": "bench_then_pilot",
      "domain_randomization": {
        "salinity_psu": "[32, 40]",
        "temperature_c": "[24, 34]",
        "toxin_load": "[0.6x, 1.5x]",
        "sensor_noise": "[low, high]"
      }
    },
    "safety_envelope": {
      "operational_design_domain": [
        "flow_rate <= 1.3x nominal",
        "oxygen_pulse_duty_cycle <= 0.45",
        "biofilm_density <= 1.2x validated envelope"
      ],
      "control_barriers": ["wall_niche_collapse", "oxygen_overshoot", "mutation_rate_excursion"],
      "transaction_protocol": "two-phase commit with human approval before controller state updates",
      "safe_states": ["hold_flow", "oxygen_idle", "sterile_flush"]
    },
    "hazard_audit_profile": {
      "scenario_focus": ["wall_niche_collapse", "sensor_fusion_failure", "controller_override"],
      "audit_frameworks": ["LABSHIELD", "LabSafetyBench", "Safe-SDL"]
    },
    "counterfactual_questions": [
      "What promoter rewrites increase PFAS reduction without collapsing wall niches?",
      "What if oxygen pulses are delayed during toxin surges?",
      "Which edits preserve community stability while improving throughput?"
    ],
    "pareto_objectives": ["pfas_reduction", "niche_stability_index", "energy_efficiency", "biosafety_margin"],
    "provenance_requirements": {
      "bundle_targets": ["data", "models", "workflows", "assays"],
      "twin_fidelity_metrics": ["niche_transition_error", "transfer_gap", "controller_stability_margin"],
      "assay_lineage_required": true
    }
  };

  function setEditorContent(obj) {
    jsonEditor.value = JSON.stringify(obj, null, 2);
  }

  // Pre-fill if empty
  if (!jsonEditor.value.trim()) {
    setEditorContent({ "message": "Paste mission JSON here" });
  }

  loadSampleBtn.addEventListener('click', () => {
    setEditorContent(sampleMission);
    // Add brief highlight animation
    jsonEditor.style.backgroundColor = 'rgba(0, 242, 254, 0.1)';
    setTimeout(() => { jsonEditor.style.backgroundColor = 'transparent'; }, 300);
  });

  loadAutoBtn.addEventListener('click', () => {
    setEditorContent(autoMission);
    jsonEditor.style.backgroundColor = 'rgba(157, 80, 187, 0.1)';
    setTimeout(() => { jsonEditor.style.backgroundColor = 'transparent'; }, 300);
  });

  if (loadPhase6Btn) {
    loadPhase6Btn.addEventListener('click', () => {
      setEditorContent(phase6Mission);
      jsonEditor.style.backgroundColor = 'rgba(79, 172, 254, 0.1)';
      setTimeout(() => { jsonEditor.style.backgroundColor = 'transparent'; }, 300);
    });
  }

  if (loadPhase7Btn) {
    loadPhase7Btn.addEventListener('click', () => {
      setEditorContent(phase7Mission);
      jsonEditor.style.backgroundColor = 'rgba(255, 0, 127, 0.1)';
      setTimeout(() => { jsonEditor.style.backgroundColor = 'transparent'; }, 300);
    });
  }

  if (loadNicheBtn) {
    loadNicheBtn.addEventListener('click', () => {
      setEditorContent(nicheMission);
      jsonEditor.style.backgroundColor = 'rgba(0, 210, 255, 0.12)';
      setTimeout(() => { jsonEditor.style.backgroundColor = 'transparent'; }, 300);
    });
  }

  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, (char) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    }[char]));
  }

  function formatTimestamp(value) {
    if (!value) return 'Unknown time';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return new Intl.DateTimeFormat(undefined, {
      dateStyle: 'medium',
      timeStyle: 'short'
    }).format(date);
  }

  function hasOutputArtifacts() {
    return Boolean(latestPlan || latestReport || latestManifest);
  }

  function setRiskIndicator(targetEl, tier) {
    if (!tier) {
      targetEl.classList.add('hidden');
      return;
    }
    targetEl.textContent = `${tier} Risk`;
    targetEl.className = `badge risk-badge ${tier}`;
    targetEl.classList.remove('hidden');
  }

  function renderReportContent(report) {
    if (!report) {
      tabReport.innerHTML = '<p>No report available for this run.</p>';
      return;
    }

    if (window.marked) {
      tabReport.innerHTML = marked.parse(report);
      return;
    }

    tabReport.innerHTML = `<pre>${report}</pre>`;
  }

  function renderCurrentTab() {
    const panes = {
      report: tabReport,
      plan: tabPlan,
      manifest: tabManifest
    };

    Object.values(panes).forEach((pane) => pane.classList.add('hidden'));

    if (!hasOutputArtifacts()) {
      welcomeMsg.classList.remove('hidden');
      briefingPanel.classList.add('hidden');
      return;
    }

    welcomeMsg.classList.add('hidden');

    if (activeTab === 'report') {
      renderReportContent(latestReport);
      tabReport.classList.remove('hidden');
      if (latestPlan) {
        renderVisuals(latestPlan);
      }
      return;
    }

    if (activeTab === 'plan') {
      tabPlan.classList.remove('hidden');
      return;
    }

    tabManifest.classList.remove('hidden');
  }

  function setActiveTab(target) {
    activeTab = target;
    tabBtns.forEach((btn) => {
      btn.classList.toggle('active', btn.getAttribute('data-tab') === target);
    });
    renderCurrentTab();
  }

  function buildArchiveLabel(detail) {
    const stamp = detail?.manifest?.generated_at;
    return stamp ? `Archive | ${formatTimestamp(stamp)}` : 'Archive replay';
  }

  function applyRunArtifacts(data, sourceLabel) {
    latestPlan = data.plan || null;
    latestReport = data.report || '';
    latestManifest = data.manifest || null;
    latestMission = data.mission || null;

    if (latestPlan) {
      briefingPanel.classList.remove('hidden');
      renderBriefing(latestPlan, data.archive_dir);
    } else {
      briefingPanel.classList.add('hidden');
      archivePath.textContent = '';
    }

    setRiskIndicator(riskBadge, latestPlan?.risk_tier);
    outputSource.textContent = sourceLabel || 'Live compile workspace';
    planOutput.textContent = latestPlan ? JSON.stringify(latestPlan, null, 2) : 'No plan available.';
    manifestOutput.textContent = latestManifest ? JSON.stringify(latestManifest, null, 2) : 'No manifest available.';
    renderCurrentTab();
  }

  function setHistoryButtonsDisabled(disabled) {
    [
      historyReportBtn,
      historyPlanBtn,
      historyManifestBtn,
      historyLoadEditorBtn
    ].forEach((button) => {
      button.disabled = disabled;
      button.style.opacity = disabled ? '0.55' : '1';
      button.style.pointerEvents = disabled ? 'none' : 'auto';
    });
  }

  function renderRunDetail(detail) {
    if (!detail?.plan) {
      runDetail.classList.add('hidden');
      setHistoryButtonsDisabled(true);
      return;
    }

    const summary = detail.plan.summary || {};
    const cards = [
      { label: 'Stages', value: summary.total_stages ?? detail.plan.stages?.length ?? 0 },
      { label: 'Review Gates', value: summary.review_gates ?? 0 },
      { label: 'Warnings', value: detail.plan.warnings?.length ?? 0 },
      { label: 'Innovations', value: summary.active_innovations ?? detail.plan.active_innovations?.length ?? 0 }
    ];

    runDetail.classList.remove('hidden');
    runDetailTitle.textContent = detail.plan.mission_name || detail.plan.mission_id || detail.run_id;
    runDetailMeta.textContent = `${detail.plan.mission_id || detail.run_id} | ${formatTimestamp(detail.manifest?.generated_at)}`;
    runDetailSummary.innerHTML = cards.map((card) => `
      <div class="run-detail-stat">
        <span>${escapeHtml(card.label)}</span>
        <strong>${escapeHtml(card.value)}</strong>
      </div>
    `).join('');
    runDetailPath.textContent = detail.archive_dir ? `Archive path: ${detail.archive_dir}` : '';
    setRiskIndicator(runDetailRisk, detail.plan.risk_tier);
    setHistoryButtonsDisabled(false);
    historyLoadEditorBtn.disabled = !detail.mission;
    historyLoadEditorBtn.style.opacity = detail.mission ? '1' : '0.55';
    historyLoadEditorBtn.style.pointerEvents = detail.mission ? 'auto' : 'none';
  }

  function renderRunList() {
    const query = runSearch.value.trim().toLowerCase();
    const filteredRuns = historyRuns.filter((run) => {
      if (!query) return true;
      const text = [
        run.run_id,
        run.mission_id,
        run.mission_name,
        run.risk_tier
      ].join(' ').toLowerCase();
      return text.includes(query);
    });

    if (!historyRuns.length) {
      runList.innerHTML = '';
      runListEmpty.textContent = 'No archived runs yet. Compile a mission to create one.';
      runListEmpty.classList.remove('hidden');
      return;
    }

    if (!filteredRuns.length) {
      runList.innerHTML = '';
      runListEmpty.textContent = 'No archived runs match the current search.';
      runListEmpty.classList.remove('hidden');
      return;
    }

    runListEmpty.classList.add('hidden');
    runList.innerHTML = filteredRuns.map((run) => {
      const summary = run.summary || {};
      const stageCount = summary.total_stages ?? 0;
      const reviewCount = summary.review_gates ?? 0;
      const activeClass = run.run_id === selectedRunId ? 'active' : '';
      return `
        <button class="run-card ${activeClass}" data-run-id="${escapeHtml(run.run_id)}">
          <div class="run-card-head">
            <div class="run-card-title">${escapeHtml(run.mission_name || run.mission_id || run.run_id)}</div>
            <span class="run-chip ${escapeHtml(run.risk_tier)}">${escapeHtml(run.risk_tier)}</span>
          </div>
          <div class="run-card-meta">
            <span>${escapeHtml(run.mission_id || run.run_id)}</span>
            <span>${escapeHtml(formatTimestamp(run.generated_at))}</span>
          </div>
          <div class="run-card-foot">
            <span>${escapeHtml(stageCount)} stages / ${escapeHtml(reviewCount)} gates</span>
            <span>${escapeHtml(run.warning_count)} warnings</span>
          </div>
        </button>
      `;
    }).join('');
  }

  async function loadRunHistory(preferredRunId = selectedRunId) {
    runListEmpty.textContent = 'Loading archived runs...';
    runListEmpty.classList.remove('hidden');

    try {
      const resp = await fetch('/api/runs');
      const data = await resp.json();
      if (!resp.ok) {
        throw new Error(data.detail || 'Failed to load archived runs');
      }

      historyRuns = Array.isArray(data.runs) ? data.runs : [];

      if (preferredRunId && !historyRuns.some((run) => run.run_id === preferredRunId)) {
        selectedRunId = null;
        selectedRunDetail = null;
        renderRunDetail(null);
      }

      renderRunList();
    } catch (err) {
      historyRuns = [];
      runList.innerHTML = '';
      runListEmpty.textContent = err.message;
      runListEmpty.classList.remove('hidden');
    }
  }

  async function openArchivedRun(runId, preferredTab = 'report') {
    selectedRunId = runId;
    renderRunList();

    try {
      const resp = await fetch(`/api/runs/${encodeURIComponent(runId)}`);
      const data = await resp.json();
      if (!resp.ok) {
        throw new Error(data.detail || 'Failed to load run archive');
      }

      selectedRunDetail = data;
      renderRunDetail(data);
      applyRunArtifacts(data, buildArchiveLabel(data));
      setActiveTab(preferredTab);
    } catch (err) {
      alert(err.message);
    }
  }

  function reopenSelectedRun(preferredTab) {
    if (!selectedRunDetail) return;
    applyRunArtifacts(selectedRunDetail, buildArchiveLabel(selectedRunDetail));
    setActiveTab(preferredTab);
  }

  tabBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      setActiveTab(btn.getAttribute('data-tab'));
    });
  });

  refreshRunsBtn.addEventListener('click', () => {
    loadRunHistory();
  });

  runSearch.addEventListener('input', () => {
    renderRunList();
  });

  runList.addEventListener('click', (event) => {
    const button = event.target.closest('.run-card');
    if (!button) return;
    openArchivedRun(button.dataset.runId);
  });

  historyReportBtn.addEventListener('click', () => reopenSelectedRun('report'));
  historyPlanBtn.addEventListener('click', () => reopenSelectedRun('plan'));
  historyManifestBtn.addEventListener('click', () => reopenSelectedRun('manifest'));
  historyLoadEditorBtn.addEventListener('click', () => {
    if (!selectedRunDetail?.mission) return;
    setEditorContent(selectedRunDetail.mission);
  });

  // Compile Action
  compileBtn.addEventListener('click', async () => {
    const rawVal = jsonEditor.value.trim();
    if (!rawVal) return;
    
    let payload;
    try {
      payload = JSON.parse(rawVal);
    } catch(e) {
      alert("Invalid JSON: " + e.message);
      return;
    }

    btnText.textContent = 'Compiling...';
    spinner.classList.remove('hidden');
    compileBtn.style.pointerEvents = 'none';
    compileBtn.style.opacity = '0.8';

    try {
      const resp = await fetch('/api/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      
      const data = await resp.json();
      
      if (!resp.ok) {
        throw new Error(data.detail || "Error compiling mission");
      }

      applyRunArtifacts(data, data.manifest?.generated_at ? `Live compile | ${formatTimestamp(data.manifest.generated_at)}` : 'Live compile workspace');
      setActiveTab(activeTab);

      const createdRunId = (data.archive_dir || '').split(/[\\/]/).pop();
      if (createdRunId) {
        selectedRunId = createdRunId;
        selectedRunDetail = {
          ...data,
          run_id: createdRunId
        };
        renderRunDetail(selectedRunDetail);
      }

      await loadRunHistory(createdRunId || selectedRunId);

      const outPanel = document.querySelector('.output-panel');
      outPanel.style.transform = 'scale(0.99)';
      setTimeout(() => { outPanel.style.transform = 'none'; }, 150);

    } catch (err) {
      alert(err.message);
    } finally {
      btnText.textContent = 'Compile Mission';
      spinner.classList.add('hidden');
      compileBtn.style.pointerEvents = 'auto';
      compileBtn.style.opacity = '1';
    }
  });

  function renderBriefing(plan, archiveDir) {
    const summary = plan.summary || {};
    const cards = [
      { label: 'Stages', value: summary.total_stages ?? plan.stages.length },
      { label: 'Review Gates', value: summary.review_gates ?? 0 },
      { label: 'Innovations', value: summary.active_innovations ?? plan.active_innovations.length },
      { label: 'Research Anchors', value: summary.research_anchors ?? 0 }
    ];

    summaryCards.innerHTML = cards.map((card) => `
      <div class="summary-card">
        <span>${card.label}</span>
        <strong>${card.value}</strong>
      </div>
    `).join('');

    const warnings = plan.warnings || [];
    if (warnings.length) {
      warningPanel.classList.remove('hidden');
      warningList.innerHTML = warnings.map((warning) => `<div class="warning-chip">${warning}</div>`).join('');
    } else {
      warningPanel.classList.add('hidden');
      warningList.innerHTML = '<div class="warning-chip clean">No validation warnings detected.</div>';
    }

    const ladder = plan.validation_ladder || [];
    validationLadder.innerHTML = ladder.map((item) => `
      <div class="ladder-item ${item.status}">
        <div class="ladder-head">
          <strong>${item.name.replaceAll('_', ' ')}</strong>
          <span>${item.status}</span>
        </div>
        <p>${item.detail}</p>
      </div>
    `).join('');

    const steps = plan.recommended_next_steps || [];
    nextSteps.innerHTML = steps.map((step) => `<div class="step-item">${step}</div>`).join('');

    archivePath.textContent = archiveDir ? `Archived to ${archiveDir}` : '';
  }

  function resetVisuals() {
    while (chartInstances.length) {
      const chart = chartInstances.pop();
      chart.destroy();
    }
  }

  function renderVisuals(plan) {
    resetVisuals();
    const reportHtml = tabReport.innerHTML;
    const previewData = plan.preview_data || {};

    if (reportHtml.includes('<!-- CHART:PARETO_FRONTIER -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">Interactive Pareto Frontier Tradeoff Surface</div><canvas id="paretoChart"></canvas>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:PARETO_FRONTIER -->', container.outerHTML);
      initParetoChart(previewData.pareto_frontier || []);
    }

    if (reportHtml.includes('<!-- CHART:COUNTERFACTUAL_MAP -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">Counterfactual Regulatory Edit Map</div><div id="counterfactualMap" class="counterfactual-map"></div>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:COUNTERFACTUAL_MAP -->', container.outerHTML);
      initCounterfactualMap(previewData.counterfactual_map || []);
    }

    if (reportHtml.includes('<!-- CHART:REGULATORY_GRAMMAR -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">Regulatory Grammar Motif Stack</div><div id="regulatoryGrammar" class="regulatory-grammar"></div>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:REGULATORY_GRAMMAR -->', container.outerHTML);
      initRegulatoryGrammar(previewData.regulatory_grammar || []);
    }

    if (reportHtml.includes('<!-- CHART:PERTURB_BENCHMARK -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">Perturbation Generalization Holdouts</div><canvas id="benchmarkChart"></canvas>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:PERTURB_BENCHMARK -->', container.outerHTML);
      initPerturbationBenchmark(previewData.perturbation_benchmark || []);
    }

    if (reportHtml.includes('<!-- CHART:SPATIAL_NICHE -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">Spatial Niche Transition Atlas</div><div id="spatialNiche" class="niche-grid"></div>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:SPATIAL_NICHE -->', container.outerHTML);
      initSpatialNiche(previewData.spatial_niche || []);
    }

    if (reportHtml.includes('<!-- CHART:MULTIMODAL_FUSION -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">Multimodal Spatial Fusion Board</div><div id="fusionBoard" class="fusion-board"></div>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:MULTIMODAL_FUSION -->', container.outerHTML);
      initMultimodalFusion(previewData.multimodal_fusion || []);
    }

    if (reportHtml.includes('<!-- CHART:QUANTUM_REFINEMENT -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">Quantum Structural Simulation Convergence</div><canvas id="quantumChart"></canvas>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:QUANTUM_REFINEMENT -->', container.outerHTML);
      initQuantumChart(previewData.quantum_curve || null);
    }

    if (reportHtml.includes('<!-- CHART:SWARM_TELEMETRY -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">Edge-AI Swarm Nodes (SLM Active)</div><div id="swarmMap" class="swarm-grid"></div>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:SWARM_TELEMETRY -->', container.outerHTML);
      initSwarmTelemetry(previewData.swarm_nodes || []);
    }

    if (reportHtml.includes('<!-- CHART:HACHIMOJI_ALPHABET -->')) {
      const container = document.createElement('div');
      container.innerHTML = '<div class="chart-title">Orthogonal 8-Letter Sequence Generator</div><div id="hachimojiSeq" class="hachimoji-sequence"></div>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:HACHIMOJI_ALPHABET -->', container.outerHTML);
      initHachimojiSequence(previewData.hachimoji_sequence || '');
    }

    if (reportHtml.includes('<!-- CHART:BIO_COMPUTING_STORAGE -->')) {
      const container = document.createElement('div');
      container.innerHTML = '<div class="chart-title">Living Neuromorphic Storage Capacity Utilization</div><div class="neuromorphic-gauge"><div id="neuroFill" class="neuromorphic-fill"></div><div id="neuroText" class="neuromorphic-text">0% UTILIZATION</div></div>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:BIO_COMPUTING_STORAGE -->', container.outerHTML);
      initNeuromorphicStorage(previewData.bio_storage || null);
    }

    if (reportHtml.includes('<!-- CHART:SPATIAL_SIMULATION -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">3D Voxel Transcription State</div><canvas id="spatialChart"></canvas>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:SPATIAL_SIMULATION -->', container.outerHTML);
      initSpatialSimulation(previewData.spatial_points || []);
    }

    if (reportHtml.includes('<!-- CHART:SAFETY_ENVELOPE -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">Operational Safety Envelope</div><div id="safetyEnvelope" class="safety-envelope"></div>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:SAFETY_ENVELOPE -->', container.outerHTML);
      initSafetyEnvelope(previewData.safety_envelope || []);
    }

    if (reportHtml.includes('<!-- CHART:HAZARD_AUDIT -->')) {
      const container = document.createElement('div');
      container.className = 'chart-container';
      container.innerHTML = '<div class="chart-title">Hazard Audit Coverage</div><div id="hazardBoard" class="hazard-board"></div>';
      tabReport.innerHTML = tabReport.innerHTML.replace('<!-- CHART:HAZARD_AUDIT -->', container.outerHTML);
      initHazardAudit(previewData.hazard_audit || []);
    }
  }

  function initParetoChart(points) {
    const ctx = document.getElementById('paretoChart');
    if (!ctx || !points.length) return;

    chartInstances.push(new Chart(ctx, {
      type: 'bubble',
      data: {
        datasets: [{
          label: 'Planning Frontier',
          data: points,
          backgroundColor: 'rgba(0, 242, 254, 0.5)',
          borderColor: '#00f2fe',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { 
            title: { display: true, text: 'Mission Performance (%)', color: '#8b92a5' },
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#8b92a5' }
          },
          y: { 
            title: { display: true, text: 'Safety & Resilience Score (%)', color: '#8b92a5' },
            grid: { color: 'rgba(255,255,255,0.05)' },
            ticks: { color: '#8b92a5' }
          }
        },
        plugins: {
          legend: { labels: { color: '#f0f2f5' } }
        }
      }
    }));
  }

  function initCounterfactualMap(edits) {
    const map = document.getElementById('counterfactualMap');
    if (!map || !edits.length) return;

    map.innerHTML = edits.map(e => `
      <div class="edit-row">
        <div class="edit-impact">${e.impact}</div>
        <div class="edit-details">
          <h4>${e.type}: ${e.target} (${e.id})</h4>
          <p>${e.note}</p>
        </div>
      </div>
    `).join('');
  }

  function initRegulatoryGrammar(motifs) {
    const el = document.getElementById('regulatoryGrammar');
    if (!el || !motifs.length) return;

    el.innerHTML = motifs.map((motif) => `
      <div class="motif-card">
        <div class="motif-head">
          <strong>${motif.name}</strong>
          <span>${motif.gain}%</span>
        </div>
        <div class="motif-bar"><span style="width:${motif.gain}%"></span></div>
        <p>${motif.note}</p>
      </div>
    `).join('');
  }

  function initPerturbationBenchmark(rows) {
    const ctx = document.getElementById('benchmarkChart');
    if (!ctx || !rows.length) return;

    chartInstances.push(new Chart(ctx, {
      type: 'bar',
      data: {
        labels: rows.map((row) => row.name),
        datasets: [{
          label: 'Planner Preview',
          data: rows.map((row) => row.score),
          backgroundColor: 'rgba(0, 242, 254, 0.55)',
          borderColor: '#00f2fe',
          borderWidth: 1.5
        }, {
          label: 'Baseline',
          data: rows.map((row) => row.baseline),
          backgroundColor: 'rgba(157, 80, 187, 0.45)',
          borderColor: '#9d50bb',
          borderWidth: 1.5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { ticks: { color: '#8b92a5' }, grid: { color: 'rgba(255,255,255,0.05)' } },
          y: { ticks: { color: '#8b92a5' }, grid: { color: 'rgba(255,255,255,0.05)' }, suggestedMax: 100 }
        },
        plugins: { legend: { labels: { color: '#f0f2f5' } } }
      }
    }));
  }

  function initSpatialNiche(niches) {
    const el = document.getElementById('spatialNiche');
    if (!el || !niches.length) return;

    el.innerHTML = niches.map((niche) => `
      <div class="niche-cell ${niche.cls}">
        <h4>${niche.name}</h4>
        <div class="niche-state">${niche.state}</div>
        <div class="niche-score">stability ${niche.score}</div>
      </div>
    `).join('');
  }

  function initMultimodalFusion(rows) {
    const el = document.getElementById('fusionBoard');
    if (!el || !rows.length) return;

    el.innerHTML = rows.map((row) => `
      <div class="fusion-card">
        <div class="fusion-head">
          <strong>${row.name}</strong>
          <span>${row.alignment}% align</span>
        </div>
        <div class="fusion-target">${row.target}</div>
        <div class="fusion-meta">uncertainty ${row.uncertainty}%</div>
      </div>
    `).join('');
  }

  function initQuantumChart(curve) {
    const ctx = document.getElementById('quantumChart');
    if (!ctx || !curve) return;
    chartInstances.push(new Chart(ctx, {
      type: 'line',
      data: {
        labels: curve.labels,
        datasets: [{
          label: 'Energy Variance (NISQ Noise)',
          data: curve.variance,
          borderColor: '#4facfe',
          backgroundColor: 'rgba(79, 172, 254, 0.2)',
          fill: true,
          tension: 0.4
        }, {
          label: 'Binding Affinity Convergence',
          data: curve.affinity,
          borderColor: '#00f2fe',
          backgroundColor: 'transparent',
          borderDash: [5, 5]
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8b92a5' } },
          y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8b92a5' } }
        },
        plugins: { legend: { labels: { color: '#f0f2f5' } } }
      }
    }));
  }

  function initSwarmTelemetry(nodes) {
    const map = document.getElementById('swarmMap');
    if (!map || !nodes.length) return;

    map.innerHTML = nodes.map((node) => {
      const cls = node.active ? 'swarm-node active' : 'swarm-node';
      return `<div class="${cls}"><div class="node-id">${node.id}</div><div class="node-status">${node.status}</div></div>`;
    }).join('');
  }

  function initHachimojiSequence(sequence) {
    const el = document.getElementById('hachimojiSeq');
    if (!el || !sequence) return;

    let html = '';
    for (const char of sequence) {
      html += `<span class="hachimoji-char char-${char}">${char}</span>`;
    }
    el.innerHTML = html + " ... [ENCRYPTED FASTA]";
  }

  function initNeuromorphicStorage(storage) {
    const fill = document.getElementById('neuroFill');
    const text = document.getElementById('neuroText');
    if (!fill || !text || !storage) return;

    setTimeout(() => {
        fill.style.width = `${storage.utilization_percent}%`;
        text.textContent = `${storage.utilization_percent}% UTILIZATION (${storage.capacity_label})`;
    }, 500);
  }

  function initSpatialSimulation(points) {
    const ctx = document.getElementById('spatialChart');
    if (!ctx || !points.length) return;

    chartInstances.push(new Chart(ctx, {
      type: 'bubble',
      data: {
        datasets: [{
          label: 'Nucleus Tx',
          data: points.slice(0, 20),
          backgroundColor: 'rgba(255, 0, 127, 0.5)',
          borderColor: '#ff007f'
        }, {
          label: 'Cytoplasm Vol',
          data: points.slice(20),
          backgroundColor: 'rgba(0, 242, 254, 0.3)',
          borderColor: 'transparent'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { display: false },
          y: { display: false }
        },
        plugins: { legend: { labels: { color: '#f0f2f5' } } },
        animation: { duration: 2000, easing: 'easeOutBounce' }
      }
    }));
  }

  function initSafetyEnvelope(layers) {
    const el = document.getElementById('safetyEnvelope');
    if (!el || !layers.length) return;

    el.innerHTML = layers.map((layer) => `
      <div class="safety-row">
        <div>
          <h4>${layer.name}</h4>
          <p>${layer.detail}</p>
        </div>
        <span>${layer.level}</span>
      </div>
    `).join('');
  }

  function initHazardAudit(rows) {
    const el = document.getElementById('hazardBoard');
    if (!el || !rows.length) return;

    el.innerHTML = rows.map((row) => `
      <div class="hazard-row">
        <div>
          <h4>${row.name}</h4>
          <p>coverage ${row.coverage}%</p>
        </div>
        <span class="severity severity-${row.severity}">S${row.severity}</span>
      </div>
    `).join('');
  }

  setHistoryButtonsDisabled(true);
  setActiveTab('report');
  loadRunHistory();
});
