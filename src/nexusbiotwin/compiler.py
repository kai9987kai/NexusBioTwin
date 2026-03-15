from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .models import Mission, Stage


# ---------------------------------------------------------------------------
# Research links — anchoring every stage to published science
# ---------------------------------------------------------------------------

RESEARCH_LINKS = {
    # Genome and regulatory modeling
    "evo2": "https://www.nature.com/articles/s41586-026-10176-5",
    "alphagenome": "https://doi.org/10.1038/s41586-025-10014-0",
    "generator": "https://arxiv.org/abs/2502.07272",
    "gpn_msa": "https://doi.org/10.1038/s41592-025-02578-2",
    "dna_benchmarks": "https://doi.org/10.1101/2024.08.16.608288",
    "get_transcription": "https://doi.org/10.1038/s41586-024-08391-z",
    "parm": "https://doi.org/10.1038/s41586-025-10093-z",
    "strand": "https://doi.org/10.48550/arXiv.2602.10156",
    "perturb_benchmark": "https://doi.org/10.1038/s41592-025-02980-0",
    # Epigenomics
    "epiagent": "https://doi.org/10.1038/s41592-025-02597-z",
    "lornash": "https://doi.org/10.1101/2024.10.31.621427",
    "cellfm": "https://www.nature.com/articles/s41467-025-59926-5",
    "cellsam": "https://doi.org/10.1038/s41592-025-02879-w",
    "nicheformer": "https://doi.org/10.1038/s41592-025-02814-z",
    "omiclip": "https://doi.org/10.1038/s41592-025-02707-1",
    "vista": "https://doi.org/10.1038/s42003-025-09479-6",
    # Protein structure and generation
    "alphafold3": "https://doi.org/10.1038/s41586-024-07487-w",
    "sadit": "https://arxiv.org/abs/2602.04482",
    # Control and adaptive systems
    "neural_activity_fm": "https://doi.org/10.1038/s41586-025-08829-y",
    "diiid_control": "https://doi.org/10.1088/1741-4326/ae34c6",
    "consortium_control": "https://arxiv.org/abs/2511.08571",
    # Bayesian optimization for bioprocess
    "bo_bioprocess": "https://doi.org/10.1002/bit.28929",
    "cognitive_digital_twin": "https://doi.org/10.1016/j.bej.2025.109618",
    "bo_media_design": "https://doi.org/10.1016/j.bej.2024.109547",
    # Sim-to-real transfer
    "dual_dt_rl": "https://doi.org/10.3390/s25030601",
    "zero_shot_sim2real": "https://doi.org/10.48550/arXiv.2502.14371",
    # Cell-free synthetic biology
    "cfps_ai": "https://doi.org/10.1021/acssynbio.4c00671",
    "cellfree_design": "https://doi.org/10.1016/j.synbio.2025.01.003",
    "cellfree_biosensor_active_learning": "https://doi.org/10.1038/s41467-025-66964-6",
    "plmeae": "https://doi.org/10.1038/s41467-025-56751-8",
    "autonomous_enzyme_engineering": "https://doi.org/10.1038/s41467-025-61209-y",
    # Safety and digital twins
    "safe_sdl": "https://doi.org/10.48550/arXiv.2602.15061",
    "fair_twins": "https://doi.org/10.1038/s44185-025-00116-3",
    "labshield": "https://arxiv.org/abs/2603.11987",
    "lab_safety_bench": "https://www.nature.com/articles/s42256-025-01152-1",
}


# ---------------------------------------------------------------------------
# Mission loading
# ---------------------------------------------------------------------------

def load_mission(path: Path) -> Mission:
    raw = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "mission_id",
        "name",
        "domain",
        "objective",
        "environment",
        "constraints",
        "control_surface",
        "success_metrics",
        "safety_profile",
    }
    missing = sorted(required - set(raw))
    if missing:
        raise ValueError(f"mission is missing required keys: {', '.join(missing)}")
    return Mission(**raw)


# ---------------------------------------------------------------------------
# Risk assessment
# ---------------------------------------------------------------------------

def _risk_tier(mission: Mission) -> str:
    strict = mission.constraints.get("containment_level") == "strict"
    review = bool(mission.safety_profile.get("human_review_required"))
    offworld = "offworld" in mission.domain.lower() or "mars" in mission.objective.lower()
    if strict or review or offworld:
        return "high"
    if mission.environment.get("shock_profile"):
        return "medium"
    return "low"


def _stable_int(seed: str, low: int, high: int) -> int:
    if high <= low:
        return low
    value = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16)
    return low + (value % (high - low + 1))


def _stable_float(seed: str, low: float, high: float, digits: int = 2) -> float:
    if high <= low:
        return round(low, digits)
    value = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16) / 0xFFFFFFFF
    return round(low + (high - low) * value, digits)


def _preview_note(label: str) -> str:
    clean = label.replace("_", " ")
    return clean[0].upper() + clean[1:] if clean else "Mission signal"


# ---------------------------------------------------------------------------
# Helper: detect which innovation modules a mission activates
# ---------------------------------------------------------------------------

def _uses_ensemble(mission: Mission) -> bool:
    return bool(mission.ensemble_models)


def _uses_epigenomics(mission: Mission) -> bool:
    return bool(mission.epigenomic_targets)


def _uses_cell_free(mission: Mission) -> bool:
    return bool(mission.cell_free_chassis)


def _uses_bayesian(mission: Mission) -> bool:
    return bool(mission.bayesian_parameters)


def _uses_sim_to_real(mission: Mission) -> bool:
    return bool(mission.sim_to_real_config)


def _uses_counterfactuals(mission: Mission) -> bool:
    return bool(mission.counterfactual_questions)


def _uses_sequence_perturbation(mission: Mission) -> bool:
    return bool(mission.sequence_perturbation_config)


def _uses_perturbation_benchmark(mission: Mission) -> bool:
    return _uses_sequence_perturbation(mission) or bool(mission.perturbation_benchmark_config)


def _uses_single_cell_foundation(mission: Mission) -> bool:
    return bool(mission.single_cell_foundation_config)


def _uses_metabolic_flux(mission: Mission) -> bool:
    return bool(mission.metabolic_flux_program)


def _uses_spatial_niche(mission: Mission) -> bool:
    return bool(mission.spatial_niche_program)


def _uses_multimodal_fusion(mission: Mission) -> bool:
    return _uses_spatial_niche(mission) or bool(mission.multimodal_spatial_fusion)


def _uses_cell_imaging(mission: Mission) -> bool:
    return bool(mission.cell_imaging_program)


def _uses_biomineralization(mission: Mission) -> bool:
    return bool(mission.biomineralization_program)


def _uses_biosensor_optimization(mission: Mission) -> bool:
    return bool(mission.biosensor_optimization)


def _uses_protein_evolution(mission: Mission) -> bool:
    return bool(mission.protein_evolution_program)


def _uses_containment_circuit(mission: Mission) -> bool:
    return bool(mission.containment_circuit_program)


def _uses_chronobiology(mission: Mission) -> bool:
    return bool(mission.chronobiology_program)


def _uses_lineage_memory(mission: Mission) -> bool:
    return bool(mission.lineage_memory_program)


def _uses_safety_envelope(mission: Mission) -> bool:
    return bool(mission.safety_envelope)


def _uses_labshield_audit(mission: Mission) -> bool:
    return bool(mission.hazard_audit_profile) or _risk_tier(mission) == "high"


def _uses_pareto(mission: Mission) -> bool:
    return bool(mission.pareto_objectives)


def _uses_provenance(mission: Mission) -> bool:
    return bool(mission.provenance_requirements)


def _uses_co_scientist(mission: Mission) -> bool:
    return mission.autonomous_co_scientist


def _uses_synthetic_data(mission: Mission) -> bool:
    return bool(mission.synthetic_data_generation)


def _uses_quantum_sim(mission: Mission) -> bool:
    return bool(mission.quantum_simulation_targets)


def _uses_edge_swarm(mission: Mission) -> bool:
    return mission.edge_swarm_orchestration


def _uses_zkp_security(mission: Mission) -> bool:
    return mission.zkp_security_level and mission.zkp_security_level.lower() != "none"


def _uses_hachimoji(mission: Mission) -> bool:
    return mission.require_genetic_firewall


def _uses_bio_computing(mission: Mission) -> bool:
    return bool(mission.bio_computing_payload)


def _uses_spatial_sim(mission: Mission) -> bool:
    return mission.spatial_simulation_resolution and mission.spatial_simulation_resolution.lower() != "none"


# ---------------------------------------------------------------------------
# Stage builders
# ---------------------------------------------------------------------------

def _stage_mission_compile() -> Stage:
    return Stage(
        name="mission_compile",
        goal="Normalize mission intent, chassis limits, and safety posture into a machine-checkable plan.",
        engine="Mission compiler",
        outputs=[
            "normalized mission spec",
            "risk tier assignment",
            "search space boundaries",
        ],
        review_required=True,
        influences=["Habitat-Genome-Compiler", "OmniForge"],
        research_anchors=[RESEARCH_LINKS["safe_sdl"], RESEARCH_LINKS["fair_twins"]],
    )


def _stage_ensemble_genome_design(mission: Mission) -> Stage:
    chassis = ", ".join(mission.constraints.get("allowed_chassis", [])) or "unspecified chassis"
    models = ", ".join(mission.ensemble_models) if mission.ensemble_models else "Evo 2"

    base_outputs = [
        "candidate edit bundles",
        "regulatory program rankings",
        "uncertainty notes",
    ]
    if _uses_ensemble(mission):
        base_outputs.extend([
            "per-model score breakdown (Evo 2, GENERator, AlphaGenome)",
            "calibrated ensemble rankings",
            "inter-model disagreement flags",
        ])

    base_anchors = [
        RESEARCH_LINKS["evo2"],
        RESEARCH_LINKS["alphagenome"],
        RESEARCH_LINKS["dna_benchmarks"],
    ]
    if _uses_ensemble(mission):
        base_anchors.extend([
            RESEARCH_LINKS["generator"],
            RESEARCH_LINKS["gpn_msa"],
        ])

    return Stage(
        name="ensemble_genome_design" if _uses_ensemble(mission) else "genome_design",
        goal=(
            f"Use {models} to score variants, embed genomic neighborhoods, and propose "
            f"candidate regulatory programs for {chassis}."
        ),
        engine="Multi-Model Ensemble Engine" if _uses_ensemble(mission) else "Evo 2 adapter",
        outputs=base_outputs,
        review_required=True,
        influences=["ArcInstitute/evo2", "DNA-Helix"],
        research_anchors=base_anchors,
    )


def _stage_epigenomic_landscape(mission: Mission) -> Stage:
    targets = ", ".join(mission.epigenomic_targets)
    return Stage(
        name="epigenomic_landscape",
        goal=(
            f"Analyze chromatin accessibility patterns and plan CRE perturbation simulations "
            f"for regulatory targets: {targets}."
        ),
        engine="EpiAgent-style scATAC encoder",
        outputs=[
            "cre_perturbation_matrix",
            "chromatin_state_predictions",
            "regulatory_circuit_map",
            "in-silico knockout impact scores",
        ],
        review_required=True,
        influences=["EpiAgent", "LoRNASH"],
        research_anchors=[RESEARCH_LINKS["epiagent"], RESEARCH_LINKS["lornash"]],
    )


def _stage_single_cell_foundation_mapping(mission: Mission) -> Stage:
    config = mission.single_cell_foundation_config
    atlas = config.get("reference_atlas", "mission single-cell atlas")
    tasks = ", ".join(config.get("tasks", [])) or "cell-state projection and retrieval"
    cell_states = ", ".join(config.get("target_cell_states", [])) or "mission-relevant cell states"
    adapter = config.get("adapter_strategy", "zero-shot transfer with light adaptation")
    return Stage(
        name="single_cell_foundation_mapping",
        goal=(
            f"Project candidates into {atlas} to support {tasks} across {cell_states}, "
            f"using {adapter} to preserve cell-state context during prioritization."
        ),
        engine="CellFM atlas projection stack",
        outputs=[
            "cell-state embedding table",
            "cross-atlas retrieval shortlist",
            "zero-shot annotation priors",
            "adapter and calibration plan",
        ],
        review_required=True,
        influences=["CellFM", "single-cell atlas transfer"],
        research_anchors=[RESEARCH_LINKS["cellfm"], RESEARCH_LINKS["epiagent"]],
    )


def _stage_metabolic_flux_sandbox(mission: Mission) -> Stage:
    config = mission.metabolic_flux_program
    substrates = ", ".join(config.get("substrates", [])) or "mission feedstocks"
    products = ", ".join(config.get("target_products", [])) or "mission outputs"
    stresses = ", ".join(config.get("stress_couplings", [])) or "environmental stress couplings"
    objective = config.get("optimization_goal", "maximize productive flux while preserving safety margins")
    return Stage(
        name="metabolic_flux_sandbox",
        goal=(
            f"Model flux from {substrates} into {products} while accounting for {stresses}, "
            f"to {objective} before chassis edits are frozen."
        ),
        engine="Constraint-based metabolic flux sandbox",
        outputs=[
            "flux envelope map",
            "redox and ATP budget sheet",
            "cofactor bottleneck shortlist",
            "pathway intervention candidates",
        ],
        review_required=True,
        influences=["constraint-based metabolism", "digital twin pathway economics", "media design"],
        research_anchors=[
            RESEARCH_LINKS["bo_media_design"],
            RESEARCH_LINKS["evo2"],
            RESEARCH_LINKS["consortium_control"],
        ],
    )


def _stage_regulatory_sequence_program(mission: Mission) -> Stage:
    config = mission.sequence_perturbation_config
    targets = ", ".join(config.get("target_sequences", [])) or "mission-critical regulatory sequences"
    cell_states = ", ".join(config.get("reference_cell_types", [])) or "mission cell states"
    readouts = ", ".join(config.get("perturbation_readouts", [])) or "transcriptional response panels"
    objective = config.get("design_objective", "rank perturbation-aware sequence rewrites")
    budget = config.get("zero_shot_budget")
    budget_text = f" within a zero-shot screen of {budget} candidate rewrites." if budget else "."
    return Stage(
        name="regulatory_sequence_program",
        goal=(
            f"Model promoter and enhancer grammar for {targets} across {cell_states} to "
            f"{objective}{budget_text}"
        ),
        engine="GET + PARM/STRAND regulatory foundation stack",
        outputs=[
            "promoter grammar scorecards",
            "motif interaction constraints",
            f"sequence perturbation priors ({readouts})",
            "cell-state-specific rewrite shortlist",
        ],
        review_required=True,
        influences=["GET", "PARM", "STRAND"],
        research_anchors=[
            RESEARCH_LINKS["get_transcription"],
            RESEARCH_LINKS["parm"],
            RESEARCH_LINKS["strand"],
        ],
    )


def _stage_perturbation_generalization_benchmark(mission: Mission) -> Stage:
    config = mission.perturbation_benchmark_config
    holdouts = ", ".join(config.get("holdout_axes", [])) or "unseen perturbations, unseen cell states"
    atlas = config.get("reference_atlas", "reference perturbation atlas")
    metrics = ", ".join(config.get("metrics", [])) or "OOD recall, delta-expression rank"
    return Stage(
        name="perturbation_generalization_benchmark",
        goal=(
            f"Benchmark perturbation-response generalization against {atlas} using holdout axes "
            f"[{holdouts}] and evaluation metrics [{metrics}] before trusting zero-shot rewrites."
        ),
        engine="Perturbation benchmark harness",
        outputs=[
            "generalization split registry",
            "holdout performance scorecard",
            "OOD failure case atlas",
            "benchmark reproducibility pack",
        ],
        review_required=True,
        influences=["Perturbation benchmark", "STRAND", "Counterfactual atlas"],
        research_anchors=[
            RESEARCH_LINKS["perturb_benchmark"],
            RESEARCH_LINKS["strand"],
        ],
    )


def _stage_counterfactual_variant_atlas(mission: Mission) -> Stage:
    questions = "; ".join(mission.counterfactual_questions)
    return Stage(
        name="counterfactual_variant_atlas",
        goal=(
            "Construct a counterfactual regulatory atlas that answers mission-specific "
            f"what-if edit questions: {questions}."
        ),
        engine="Counterfactual atlas planner",
        outputs=[
            "variant impact atlas",
            "regulatory what-if table",
            "safe edit exclusion list",
            "uncertainty-ranked intervention windows",
        ],
        review_required=True,
        influences=["ArcInstitute/evo2", "AlphaGenome"],
        research_anchors=[
            RESEARCH_LINKS["evo2"],
            RESEARCH_LINKS["alphagenome"],
            RESEARCH_LINKS["dna_benchmarks"],
        ],
    )


def _stage_protein_triage() -> Stage:
    return Stage(
        name="protein_triage",
        goal="Rank translated ORFs and enzyme candidates for deeper structural follow-up.",
        engine="Protein triage planner",
        outputs=[
            "candidate enzymes",
            "structure follow-up queue",
            "interaction screening shortlist",
        ],
        review_required=False,
        influences=["ProteinFoldingSimulation"],
        research_anchors=[RESEARCH_LINKS["alphafold3"], RESEARCH_LINKS["sadit"]],
    )


def _stage_protein_evolution_biofoundry(mission: Mission) -> Stage:
    config = mission.protein_evolution_program
    proteins = ", ".join(config.get("seed_proteins", [])) or "mission enzyme seeds"
    objective = config.get("fitness_objective", "improve protein fitness under mission stressors")
    rounds = config.get("rounds", 3)
    variants = config.get("variants_per_round", 96)
    mode = config.get("biofoundry_mode", "human-supervised")
    return Stage(
        name="protein_evolution_biofoundry",
        goal=(
            f"Run {mode} protein evolution cycles for {proteins} to {objective}, "
            f"planning {rounds} rounds at ~{variants} variants per round."
        ),
        engine="Protein language model plus self-driving biofoundry planner",
        outputs=[
            "round-by-round mutant library plan",
            "assay queue for each evolution round",
            "fitness uplift tracking sheet",
            "biofoundry handoff package",
        ],
        review_required=True,
        influences=["PLM-enabled automatic protein evolution", "iBioFAB", "protein language model"],
        research_anchors=[
            RESEARCH_LINKS["plmeae"],
            RESEARCH_LINKS["autonomous_enzyme_engineering"],
            RESEARCH_LINKS["sadit"],
        ],
    )


def _stage_cell_free_prototyping(mission: Mission) -> Stage:
    extracts = ", ".join(mission.cell_free_chassis)
    return Stage(
        name="cell_free_prototyping",
        goal=(
            f"Design cell-free validation experiments using {extracts} to test candidate "
            f"constructs before committing to full chassis engineering."
        ),
        engine="Cell-free experiment planner",
        outputs=[
            "cfps_experiment_designs",
            "rapid_screening_matrix",
            "go_no_go_criteria",
            "expected_yield_estimates",
        ],
        review_required=True,
        influences=["Safe-SDL", "AI-CFPS"],
        research_anchors=[
            RESEARCH_LINKS["cfps_ai"],
            RESEARCH_LINKS["cellfree_design"],
            RESEARCH_LINKS["safe_sdl"],
        ],
    )


def _stage_cell_free_biosensor_optimization(mission: Mission) -> Stage:
    config = mission.biosensor_optimization
    sensor_family = config.get("sensor_family", "cell-free biosensor family")
    analytes = ", ".join(config.get("target_analytes", [])) or "mission analytes"
    counter = ", ".join(config.get("counter_selectants", [])) or "mission confounders"
    screen_format = config.get("screen_format", "cell-free assay panel")
    objectives = ", ".join(config.get("optimization_objectives", [])) or "sensitivity, selectivity, and response time"
    budget = config.get("screening_budget_variants")
    budget_text = f" within a budget of {budget} variants" if budget else ""
    return Stage(
        name="cell_free_biosensor_optimization",
        goal=(
            f"Optimize {sensor_family} for {analytes} against counter-selectants [{counter}] "
            f"using active learning in {screen_format} with objectives [{objectives}]{budget_text}."
        ),
        engine="Active-learning cell-free biosensor optimizer",
        outputs=[
            "biosensor variant shortlist",
            "active-learning acquisition ledger",
            "selectivity and limit-of-detection scorecard",
            "freeze-dry and field-screening validation plan",
        ],
        review_required=True,
        influences=["Cell-free biosensors", "active learning", "rapid assay design"],
        research_anchors=[
            RESEARCH_LINKS["cellfree_biosensor_active_learning"],
            RESEARCH_LINKS["cfps_ai"],
            RESEARCH_LINKS["cellfree_design"],
        ],
    )


def _stage_habitat_twin(mission: Mission) -> Stage:
    shock_profile = ", ".join(mission.environment.get("shock_profile", [])) or "nominal conditions"
    return Stage(
        name="habitat_twin",
        goal=(
            f"Stress-test consortium behavior against habitat shocks and deployment conditions: "
            f"{shock_profile}."
        ),
        engine="Habitat twin planner",
        outputs=[
            "shock matrix",
            "resilience hypotheses",
            "failure mode checklist",
        ],
        review_required=False,
        influences=["didactic-lamp", "Habitat-Genome-Compiler"],
        research_anchors=[RESEARCH_LINKS["fair_twins"], RESEARCH_LINKS["consortium_control"]],
    )


def _stage_cell_imaging_foundation(mission: Mission) -> Stage:
    config = mission.cell_imaging_program
    modalities = ", ".join(config.get("modalities", [])) or "microscopy and spatial assay images"
    targets = ", ".join(config.get("segmentation_targets", [])) or "cells and microcolonies"
    prompt_strategy = config.get("prompt_strategy", "few-shot prompting")
    downstream = ", ".join(config.get("downstream_workflows", [])) or "spatial QC and morphology extraction"
    return Stage(
        name="cell_imaging_foundation",
        goal=(
            f"Segment {targets} from {modalities} using {prompt_strategy}, feeding masks into "
            f"{downstream} before downstream spatial inference is trusted."
        ),
        engine="CellSAM imaging foundation stack",
        outputs=[
            "segmentation mask bank",
            "prompt and fine-tune recipe",
            "morphology QC scorecard",
            "frame-level failure case atlas",
        ],
        review_required=True,
        influences=["CellSAM", "microscopy foundation models", "spatial QC"],
        research_anchors=[RESEARCH_LINKS["cellsam"], RESEARCH_LINKS["vista"]],
    )


def _stage_biomineral_interface_forge(mission: Mission) -> Stage:
    config = mission.biomineralization_program
    minerals = ", ".join(config.get("target_minerals", [])) or "mission minerals"
    functions = ", ".join(config.get("material_functions", [])) or "adhesion, shielding, and filtration"
    assays = ", ".join(config.get("interface_assays", [])) or "surface interaction assays"
    environment = config.get("deployment_surface", "mission habitat surfaces")
    return Stage(
        name="biomineral_interface_forge",
        goal=(
            f"Co-design biomineral interfaces for {minerals} on {environment} to support {functions}, "
            f"validated through {assays}."
        ),
        engine="Bio-material interface forge",
        outputs=[
            "biomineral recipe matrix",
            "surface adhesion and delamination risks",
            "shielding or filtration performance hypotheses",
            "interface scale-up checklist",
        ],
        review_required=True,
        influences=["biomineral interfaces", "habitat materials", "spatial niche engineering"],
        research_anchors=[
            RESEARCH_LINKS["fair_twins"],
            RESEARCH_LINKS["nicheformer"],
            RESEARCH_LINKS["consortium_control"],
        ],
    )


def _stage_spatial_niche_modeling(mission: Mission) -> Stage:
    config = mission.spatial_niche_program
    assays = ", ".join(config.get("assays", [])) or "spatial omics assays"
    axes = ", ".join(config.get("niche_axes", [])) or "local stress gradients"
    reference_map = config.get("reference_map", "mission spatial atlas")
    communication = ", ".join(config.get("communication_targets", [])) or "cell-cell coordination"
    return Stage(
        name="spatial_niche_modeling",
        goal=(
            f"Embed structured microenvironments from {assays} against {reference_map} to "
            f"map niche transitions over {axes} and coordination targets: {communication}."
        ),
        engine="Nicheformer spatial foundation twin",
        outputs=[
            "niche embedding atlas",
            "microenvironment transition graph",
            "cell-cell communication risk map",
            "spatial exclusion and enrichment zones",
        ],
        review_required=True,
        influences=["Nicheformer", "Habitat twin", "FAIR digital twins"],
        research_anchors=[
            RESEARCH_LINKS["nicheformer"],
            RESEARCH_LINKS["fair_twins"],
            RESEARCH_LINKS["consortium_control"],
        ],
    )


def _stage_multimodal_spatial_fusion(mission: Mission) -> Stage:
    config = mission.multimodal_spatial_fusion
    modalities = ", ".join(config.get("modalities", [])) or "histology, imaging, transcriptomics"
    targets = ", ".join(config.get("fusion_targets", [])) or "spatial signal recovery and morphology alignment"
    uncertainty = config.get("uncertainty_budget", "mission-defined uncertainty tolerance")
    return Stage(
        name="multimodal_spatial_fusion",
        goal=(
            f"Fuse {modalities} to support {targets}, while tracking an uncertainty budget of "
            f"{uncertainty} across spatial evidence layers."
        ),
        engine="OmiCLIP + VISTA multimodal evidence fusion stack",
        outputs=[
            "cross-modal alignment map",
            "spatial signal confidence surface",
            "morphology-expression retrieval board",
            "fusion uncertainty heatmap",
        ],
        review_required=True,
        influences=["OmiCLIP", "VISTA", "Nicheformer"],
        research_anchors=[
            RESEARCH_LINKS["omiclip"],
            RESEARCH_LINKS["vista"],
            RESEARCH_LINKS["nicheformer"],
        ],
    )


def _stage_multiobjective_frontier(mission: Mission) -> Stage:
    objectives = ", ".join(mission.pareto_objectives)
    return Stage(
        name="multiobjective_frontier",
        goal=(
            "Compute a Pareto frontier across mission tradeoffs to avoid collapsing the "
            f"search into a single score. Frontier objectives: {objectives}."
        ),
        engine="Pareto frontier planner",
        outputs=[
            "pareto frontier candidates",
            "tradeoff matrix",
            "dominated candidate rejects",
            "budget-aware follow-up recommendations",
        ],
        review_required=True,
        influences=["Bayesian-Optimization", "Habitat twin", "Consortium control"],
        research_anchors=[
            RESEARCH_LINKS["bo_bioprocess"],
            RESEARCH_LINKS["cognitive_digital_twin"],
            RESEARCH_LINKS["consortium_control"],
        ],
    )


def _stage_bayesian_experiment_design(mission: Mission) -> Stage:
    bp = mission.bayesian_parameters
    objective = bp.get("objective_function", "unspecified")
    dims = ", ".join(bp.get("search_dimensions", []))
    acq = bp.get("acquisition_function", "expected_improvement")
    batch = bp.get("batch_size", 1)
    max_iter = bp.get("max_iterations", 25)

    return Stage(
        name="bayesian_experiment_design",
        goal=(
            f"Plan adaptive Bayesian optimization loops to maximize {objective} over "
            f"search dimensions [{dims}] using {acq} acquisition with batch size {batch} "
            f"for up to {max_iter} iterations."
        ),
        engine="BO acquisition planner with cognitive digital twin",
        outputs=[
            "experiment_arms",
            "acquisition_function_policy",
            "stopping_criteria",
            "expected_improvement_surface",
            "surrogate_model_spec",
        ],
        review_required=True,
        influences=["Bayesian-Optimization", "Cognitive-Digital-Twin"],
        research_anchors=[
            RESEARCH_LINKS["bo_bioprocess"],
            RESEARCH_LINKS["cognitive_digital_twin"],
            RESEARCH_LINKS["bo_media_design"],
        ],
    )


def _stage_chronobiology_scheduler(mission: Mission) -> Stage:
    config = mission.chronobiology_program
    cycle = config.get("cycle_length_hours", 24)
    zeitgebers = ", ".join(config.get("zeitgebers", [])) or "light, thermal, and nutrient cues"
    schedules = ", ".join(config.get("scheduled_controls", [])) or "mission actuation lanes"
    safe_night = ", ".join(config.get("night_safe_states", [])) or "reduced-energy safe states"
    return Stage(
        name="chronobiology_scheduler",
        goal=(
            f"Align {schedules} to a {cycle}-hour rhythm using zeitgebers [{zeitgebers}], "
            f"with explicit night-safe states [{safe_night}] and phase-drift tests."
        ),
        engine="Chronobiology pulse scheduler",
        outputs=[
            "cycle-aware actuation calendar",
            "phase drift stress tests",
            "day-night pulse ladder",
            "rhythm-aware fallback schedule",
        ],
        review_required=True,
        influences=["chronobiology", "cognitive digital twin", "safe scheduling"],
        research_anchors=[
            RESEARCH_LINKS["cognitive_digital_twin"],
            RESEARCH_LINKS["consortium_control"],
            RESEARCH_LINKS["safe_sdl"],
        ],
    )


def _stage_containment_circuit_lattice(mission: Mission) -> Stage:
    config = mission.containment_circuit_program
    layers = ", ".join(config.get("layers", [])) or "auxotrophy, kill-switches, and quorum locks"
    triggers = ", ".join(config.get("tripwire_triggers", [])) or "escape and policy tripwires"
    recovery = config.get("reversion_mode", "sterile fail-closed recovery")
    return Stage(
        name="containment_circuit_lattice",
        goal=(
            f"Compile a layered containment circuit lattice over {layers}, keyed to triggers "
            f"[{triggers}] with recovery mode {recovery}."
        ),
        engine="Biocontainment circuit planner",
        outputs=[
            "layered containment architecture",
            "tripwire and reversion logic table",
            "escape pathway audit",
            "containment assay matrix",
        ],
        review_required=True,
        influences=["Safe-SDL", "biocontainment engineering", "hazard audit"],
        research_anchors=[
            RESEARCH_LINKS["safe_sdl"],
            RESEARCH_LINKS["labshield"],
            RESEARCH_LINKS["dna_benchmarks"],
        ],
    )


def _stage_controller_design(mission: Mission) -> Stage:
    control_goal = ", ".join(mission.control_surface)
    base_outputs = [
        "controller templates",
        "closed-loop observability plan",
        "intervention escalation rules",
    ]
    base_anchors = [
        RESEARCH_LINKS["neural_activity_fm"],
        RESEARCH_LINKS["diiid_control"],
        RESEARCH_LINKS["consortium_control"],
    ]

    if _uses_sim_to_real(mission):
        s2r = mission.sim_to_real_config
        sim_env = s2r.get("sim_environment", "unspecified")
        real_env = s2r.get("real_environment", "unspecified")
        cal_strategy = s2r.get("calibration_strategy", "manual")
        base_outputs.extend([
            f"domain_randomization_spec ({sim_env} -> {real_env})",
            "transfer_gap_estimate",
            f"calibration_protocol ({cal_strategy})",
            "reality_gap_test_matrix",
        ])
        base_anchors.extend([
            RESEARCH_LINKS["dual_dt_rl"],
            RESEARCH_LINKS["zero_shot_sim2real"],
        ])

    if _uses_safety_envelope(mission):
        base_outputs.extend([
            "barrier-aware controller policy",
            "safe-state transition hooks",
        ])
        base_anchors.append(RESEARCH_LINKS["safe_sdl"])

    return Stage(
        name="controller_design",
        goal=(
            f"Compile a BioControl DSL policy over the control surface: {control_goal}."
            + (f" Include sim-to-real transfer bridge from {s2r.get('sim_environment', '?')} "
               f"to {s2r.get('real_environment', '?')}."
               if _uses_sim_to_real(mission) else "")
            + (" Constrain the policy to the declared operational safety envelope."
               if _uses_safety_envelope(mission) else "")
        ),
        engine=(
            "BioControl DSL planner"
            + (" + Sim-to-Real Transfer Bridge" if _uses_sim_to_real(mission) else "")
            + (" + Safe-SDL Envelope" if _uses_safety_envelope(mission) else "")
        ),
        outputs=base_outputs,
        review_required=True,
        influences=(
            ["NeuroPulse-CableLab", "NeuroFusion-Reactor"]
            + (["Dual-DT-RL"] if _uses_sim_to_real(mission) else [])
            + (["Safe-SDL"] if _uses_safety_envelope(mission) else [])
        ),
        research_anchors=base_anchors,
    )


def _stage_operational_safety_envelope(mission: Mission) -> Stage:
    config = mission.safety_envelope
    odd = "; ".join(config.get("operational_design_domain", [])) or "mission-defined operating limits"
    barriers = ", ".join(config.get("control_barriers", [])) or "state and actuation barriers"
    protocol = config.get("transaction_protocol", "human-in-the-loop gated actuation")
    safe_states = ", ".join(config.get("safe_states", [])) or "fallback safe states"
    return Stage(
        name="operational_safety_envelope",
        goal=(
            "Compile a Safe-SDL execution envelope with an explicit operational design "
            f"domain [{odd}], barrier monitors for {barriers}, and transactional control "
            f"under {protocol}."
        ),
        engine="Safe-SDL envelope compiler",
        outputs=[
            "operational design domain specification",
            "control barrier monitors",
            f"transaction-safe execution contract ({protocol})",
            f"fallback safe-state ladder ({safe_states})",
        ],
        review_required=True,
        influences=["Safe-SDL", "BioControl DSL", "Human review queue"],
        research_anchors=[
            RESEARCH_LINKS["safe_sdl"],
            RESEARCH_LINKS["fair_twins"],
        ],
    )


def _stage_labshield_hazard_audit(mission: Mission) -> Stage:
    config = mission.hazard_audit_profile
    focus = ", ".join(config.get("scenario_focus", [])) or "chemical, biological, and autonomy hazard classes"
    frameworks = ", ".join(config.get("audit_frameworks", [])) or "LABSHIELD, LabSafetyBench, Safe-SDL"
    return Stage(
        name="labshield_hazard_audit",
        goal=(
            f"Audit the mission against {frameworks} with emphasis on {focus}, surfacing hazard "
            "blind spots and refusal-trigger scenarios before escalation."
        ),
        engine="LABSHIELD hazard audit board",
        outputs=[
            "hazard reasoning scorecard",
            "refusal-trigger checklist",
            "blind-spot taxonomy",
            "safety review handoff pack",
        ],
        review_required=True,
        influences=["LABSHIELD", "LabSafetyBench", "Safe-SDL"],
        research_anchors=[
            RESEARCH_LINKS["labshield"],
            RESEARCH_LINKS["lab_safety_bench"],
            RESEARCH_LINKS["safe_sdl"],
        ],
    )


def _stage_orchestration() -> Stage:
    return Stage(
        name="orchestration_and_review",
        goal="Assemble the pipeline into an auditable run with artifacts, retries, and human review.",
        engine="NexusFlow and OmniForge orchestration",
        outputs=[
            "run manifest",
            "review queue",
            "artifact index",
        ],
        review_required=True,
        influences=["nexusflow", "OmniForge", "Supermix_29"],
        research_anchors=[RESEARCH_LINKS["safe_sdl"], RESEARCH_LINKS["fair_twins"]],
    )


def _stage_safety_red_team(mission: Mission) -> Stage:
    disallowed = ", ".join(mission.constraints.get("disallowed_traits", [])) or "no explicit blocked traits"
    return Stage(
        name="safety_red_team",
        goal=(
            "Stress-test the proposed plan against misuse, blocked traits, autonomy creep, "
            f"and hidden safety regressions. Disallowed traits: {disallowed}."
        ),
        engine="Policy and refusal planner",
        outputs=[
            "red-team scenarios",
            "blocked action list",
            "review escalation triggers",
            "deployment refusal conditions",
        ],
        review_required=True,
        influences=["Safe-SDL", "Habitat-Genome-Compiler"],
        research_anchors=[
            RESEARCH_LINKS["safe_sdl"],
            RESEARCH_LINKS["dna_benchmarks"],
        ],
    )


def _stage_lineage_memory_recorder(mission: Mission) -> Stage:
    config = mission.lineage_memory_program
    events = ", ".join(config.get("events_to_record", [])) or "mission-critical cell-state transitions"
    mechanism = config.get("recording_mechanism", "DNA event recorder")
    cadence = config.get("export_cadence", "end-of-run archive")
    return Stage(
        name="lineage_memory_recorder",
        goal=(
            f"Plan a {mechanism} that records {events}, with archive export cadence "
            f"{cadence} for later forensic review."
        ),
        engine="Lineage memory and event logging planner",
        outputs=[
            "recording cassette blueprint",
            "event encoding schema",
            "decode and assay plan",
            "memory burden and retention budget",
        ],
        review_required=True,
        influences=["auditability", "biological event logging", "FAIR provenance"],
        research_anchors=[
            RESEARCH_LINKS["fair_twins"],
            RESEARCH_LINKS["safe_sdl"],
            RESEARCH_LINKS["dna_benchmarks"],
        ],
    )


def _stage_fair_provenance(mission: Mission) -> Stage:
    targets = ", ".join(mission.provenance_requirements.get("bundle_targets", [])) or "data, models, workflows"
    return Stage(
        name="fair_provenance_bundle",
        goal=(
            "Package the twin as a FAIR artifact bundle with explicit provenance, model lineage, "
            f"and assay traceability targets for {targets}."
        ),
        engine="FAIR twin bundle planner",
        outputs=[
            "artifact lineage graph",
            "model and assay provenance bundle",
            "twin fidelity checklist",
            "reproducibility handoff pack",
        ],
        review_required=False,
        influences=["FAIR digital twins", "OmniForge", "nexusflow"],
        research_anchors=[
            RESEARCH_LINKS["fair_twins"],
            RESEARCH_LINKS["safe_sdl"],
        ],
    )


def _stage_autonomous_co_scientist() -> Stage:
    return Stage(
        name="autonomous_co_scientist",
        goal=(
            "Execute an LLM-based autonomous agent loop to review the digital twin plan, "
            "recommend multi-agent coordination strategies, and identify cross-stage "
            "optimization bottlenecks for self-driving lab alignment."
        ),
        engine="Autonomous Researcher Agent (Agents4Science loop)",
        outputs=[
            "agent orchestration graph",
            "cross-stage optimization recs",
            "autonomous lab safety config",
            "multi-agent coordination policy",
        ],
        review_required=True,
        influences=["Agents4Science", "NexusFlow", "OmniForge"],
        research_anchors=[
            RESEARCH_LINKS["safe_sdl"],
            "https://emergentmind.com/papers/agents4science",
        ],
    )


def _stage_synthetic_twin_data(mission: Mission) -> Stage:
    config = mission.synthetic_data_generation
    fidelity = config.get("target_fidelity", "high")
    return Stage(
        name="synthetic_twin_data",
        goal=(
            f"Generate {fidelity}-fidelity synthetic twin datasets to bridge the data "
            "exhaustion gap and train closed-loop surrogate models prior to real-world "
            "bioreactor deployment."
        ),
        engine="Synthetic Data Twin Generator",
        outputs=[
            "high-fidelity synthetic dataset",
            "data distribution report",
            "out-of-distribution edge cases",
            "surrogate training baseline",
        ],
        review_required=False,
        influences=["Cognitive-Digital-Twin", "Dual-DT-RL"],
        research_anchors=[
            RESEARCH_LINKS["cognitive_digital_twin"],
            "https://zartom.com/synthetic-twin-data-solution",
        ],
    )


def _stage_quantum_structural_refinement(mission: Mission) -> Stage:
    targets = ", ".join(mission.quantum_simulation_targets)
    return Stage(
        name="quantum_structural_refinement",
        goal=(
            f"Offload high-complexity molecular docking and structural refinement for [{targets}] "
            "to a hybrid Quantum-Classical (AQuaRef) simulation cluster."
        ),
        engine="AQuaRef NISQ + Classical GPU Cluster",
        outputs=[
            "quantum-refined interaction surface grid",
            "qubit allocation and convergence log",
            "drug/substrate binding affinities",
        ],
        review_required=False,
        influences=["AlphaFold 3", "AQuaRef", "IBM Heron"],
        research_anchors=[
            RESEARCH_LINKS["alphafold3"],
            "https://lbl.gov/aquaref-quantum-refinement",
        ],
    )


def _stage_edge_ai_swarm_orchestration() -> Stage:
    return Stage(
        name="edge_ai_swarm_orchestration",
        goal=(
            "Deploy highly-compressed Small Language Models (SLMs) to Edge-AI nodes (bioreactors or "
            "bio-bots) for distributed, zero-latency autonomous swarm coordination."
        ),
        engine="Decentralized SLM Edge Swarm Controller",
        outputs=[
            "edge device deployment manifest",
            "swarm consensus protocols",
            "local autonomy bounds configuration",
        ],
        review_required=True,
        influences=["Edge AI 2026", "Agentic Swarms", "ANTS 2026"],
        research_anchors=[
            RESEARCH_LINKS["safe_sdl"],
            "https://ants2026.org/swarm-intelligence",
        ],
    )


def _stage_zkp_biosecurity_anchor(mission: Mission) -> Stage:
    level = mission.zkp_security_level
    return Stage(
        name="zkp_biosecurity_anchor",
        goal=(
            f"Secure the digital twin under {level} Zero-Knowledge Proof (ZKP) cryptography to "
            "guarantee biological data sovereignty, protecting proprietary bioreactor state and "
            "genomic assays from model weight leakage."
        ),
        engine="ZKP Bio-Digital Sovereign Vault",
        outputs=[
            "zk-SNARK privacy circuits",
            "cryptographic safety proofs",
            "sovereign telemetry keys",
        ],
        review_required=False,
        influences=["Web3 Biosecurity", "BioSecure Digital Twin", "ZK Compliance 2026"],
        research_anchors=[
            RESEARCH_LINKS["fair_twins"],
            "https://zkproof.org/biosecurity-2026",
        ],
    )


def _stage_hachimoji_transpilation() -> Stage:
    return Stage(
        name="hachimoji_transpilation",
        goal=(
            "Expand the canonical 4-letter DNA alphabet to an 8-letter synthetic alphabet "
            "(A, T, C, G, Z, P, S, B) to establish a strict genetic firewall and true functional orthogonality."
        ),
        engine="Orthogonal XB Sequence Transpiler",
        outputs=[
            "8-letter orthogonal sequence map",
            "synthetic polymerase structural models",
            "genetic firewall safety proof",
        ],
        review_required=True,
        influences=["Xenobiology", "Hachimoji DNA", "Synthetic Biology 2026"],
        research_anchors=[
            "https://pubmed.ncbi.nlm.nih.gov/30787435/",
            "https://synbioconference.org/2026",
        ],
    )


def _stage_bio_hybrid_data_storage(mission: Mission) -> Stage:
    payload = mission.bio_computing_payload.get("data_type", "exabytes")
    return Stage(
        name="bio_hybrid_data_storage",
        goal=(
            f"Engineer the consortium to act as a living hard drive, encoding [{payload}] of data "
            "into the swarm's genome using semiconducting perovskite-DNA neuromorphic memory resistors."
        ),
        engine="Neuromorphic DNA Storage Encoder",
        outputs=[
            "bio-orthogonal memory resistor design",
            "neuromorphic data capacity limits",
            "DNA-perovskite interaction lattice",
        ],
        review_required=False,
        influences=["Bio-Data Revolution", "Neuromorphic DNA", "Biological Computing 2026"],
        research_anchors=[
            "https://www.eurekalert.org/news-releases/1033002",
        ],
    )


def _stage_spatial_whole_cell_sim(mission: Mission) -> Stage:
    res = mission.spatial_simulation_resolution
    return Stage(
        name="spatial_whole_cell_sim",
        goal=(
            f"Run a {res} 3D whole-cell physics simulation powered by a spatial transcriptomics "
            "foundation model to validate spatial cellular context prior to synthesis."
        ),
        engine="Spatial-FM Whole Cell Physics Sandbox",
        outputs=[
            "voxel-by-voxel transcriptomic state map",
            "3D cellular physics render",
        ],
        review_required=False,
        influences=["scSpatialSIM", "Spatial Transcriptomics FM", "Whole-Cell Simulation 2026"],
        research_anchors=[
            "https://www.biorxiv.org/content/10.1101/2024.02.26.582046v1",
            "https://pubmed.ncbi.nlm.nih.gov/38848113/",
        ],
    )


# ---------------------------------------------------------------------------
# Stage assembly — builds the full pipeline for a mission
# ---------------------------------------------------------------------------

def build_stages(mission: Mission) -> list[Stage]:
    stages: list[Stage] = [
        _stage_mission_compile(),
        _stage_ensemble_genome_design(mission),
    ]

    # Insert epigenomic landscape stage if mission has targets
    if _uses_epigenomics(mission):
        stages.append(_stage_epigenomic_landscape(mission))

    if _uses_single_cell_foundation(mission):
        stages.append(_stage_single_cell_foundation_mapping(mission))

    if _uses_metabolic_flux(mission):
        stages.append(_stage_metabolic_flux_sandbox(mission))

    if _uses_sequence_perturbation(mission):
        stages.append(_stage_regulatory_sequence_program(mission))

    if _uses_perturbation_benchmark(mission):
        stages.append(_stage_perturbation_generalization_benchmark(mission))

    if _uses_counterfactuals(mission):
        stages.append(_stage_counterfactual_variant_atlas(mission))

    if _uses_hachimoji(mission):
        stages.append(_stage_hachimoji_transpilation())

    stages.append(_stage_protein_triage())

    if _uses_protein_evolution(mission):
        stages.append(_stage_protein_evolution_biofoundry(mission))

    # Insert cell-free prototyping if mission has cell-free chassis
    if _uses_cell_free(mission):
        stages.append(_stage_cell_free_prototyping(mission))

    if _uses_biosensor_optimization(mission):
        stages.append(_stage_cell_free_biosensor_optimization(mission))

    stages.append(_stage_habitat_twin(mission))

    if _uses_cell_imaging(mission):
        stages.append(_stage_cell_imaging_foundation(mission))

    if _uses_biomineralization(mission):
        stages.append(_stage_biomineral_interface_forge(mission))

    if _uses_spatial_niche(mission):
        stages.append(_stage_spatial_niche_modeling(mission))

    if _uses_multimodal_fusion(mission):
        stages.append(_stage_multimodal_spatial_fusion(mission))

    if _uses_pareto(mission):
        stages.append(_stage_multiobjective_frontier(mission))

    if _uses_synthetic_data(mission):
        stages.append(_stage_synthetic_twin_data(mission))

    if _uses_bio_computing(mission):
        stages.append(_stage_bio_hybrid_data_storage(mission))

    # Insert Bayesian experiment design if mission specifies BO parameters
    if _uses_bayesian(mission):
        stages.append(_stage_bayesian_experiment_design(mission))

    if _uses_chronobiology(mission):
        stages.append(_stage_chronobiology_scheduler(mission))

    if _uses_containment_circuit(mission):
        stages.append(_stage_containment_circuit_lattice(mission))

    if _uses_quantum_sim(mission):
        stages.append(_stage_quantum_structural_refinement(mission))

    if _uses_safety_envelope(mission):
        stages.append(_stage_operational_safety_envelope(mission))

    stages.append(_stage_controller_design(mission))

    if _uses_spatial_sim(mission):
        stages.append(_stage_spatial_whole_cell_sim(mission))

    if _uses_edge_swarm(mission):
        stages.append(_stage_edge_ai_swarm_orchestration())

    if _uses_co_scientist(mission):
        stages.append(_stage_autonomous_co_scientist())

    if _uses_labshield_audit(mission):
        stages.append(_stage_labshield_hazard_audit(mission))

    stages.append(_stage_safety_red_team(mission))

    if _uses_zkp_security(mission):
        stages.append(_stage_zkp_biosecurity_anchor(mission))

    if _uses_lineage_memory(mission):
        stages.append(_stage_lineage_memory_recorder(mission))

    if _uses_provenance(mission):
        stages.append(_stage_fair_provenance(mission))
    stages.append(_stage_orchestration())

    return stages


def _validation_warnings(mission: Mission, risk_tier: str) -> list[str]:
    warnings: list[str] = []

    if risk_tier == "high" and not _uses_cell_free(mission):
        warnings.append("High-risk mission has no declared cell-free validation gate.")
    if risk_tier == "high" and not _uses_provenance(mission):
        warnings.append("High-risk mission does not declare FAIR provenance requirements.")
    if _uses_sim_to_real(mission) and not _uses_safety_envelope(mission):
        warnings.append("Sim-to-real transfer is configured without an operational safety envelope.")
    if _uses_co_scientist(mission) and not mission.safety_profile.get("human_review_required"):
        warnings.append("Autonomous co-scientist is enabled while human review is not required.")
    if mission.safety_profile.get("autonomous_deployment_allowed") and not _uses_safety_envelope(mission):
        warnings.append("Autonomous deployment is allowed without Safe-SDL control barriers and safe states.")
    if _uses_edge_swarm(mission) and not _uses_zkp_security(mission):
        warnings.append("Edge-AI swarm coordination lacks a declared ZKP biosecurity anchor.")
    if _uses_single_cell_foundation(mission) and not (_uses_epigenomics(mission) or _uses_spatial_niche(mission)):
        warnings.append("Single-cell atlas mapping is enabled without epigenomic or spatial context; embeddings may be weakly grounded.")
    if _uses_metabolic_flux(mission) and not mission.metabolic_flux_program.get("substrates"):
        warnings.append("Metabolic flux sandbox is enabled without explicit substrates; feedstock assumptions will be generic.")
    if _uses_sequence_perturbation(mission) and not _uses_epigenomics(mission):
        warnings.append("Sequence perturbation planning is enabled without epigenomic target context.")
    if _uses_sequence_perturbation(mission) and not mission.perturbation_benchmark_config:
        warnings.append("No explicit perturbation benchmark configuration is declared; default holdout benchmarking will be assumed.")
    if _uses_biosensor_optimization(mission) and not _uses_cell_free(mission):
        warnings.append("Cell-free biosensor optimization is configured without a declared cell-free chassis gate.")
    if _uses_cell_imaging(mission) and not (_uses_spatial_niche(mission) or mission.multimodal_spatial_fusion):
        warnings.append("Cell imaging segmentation is active without downstream spatial or multimodal consumers.")
    if _uses_biomineralization(mission) and not (_uses_spatial_niche(mission) or _uses_cell_imaging(mission)):
        warnings.append("Biomineral interface planning is active without spatial or imaging evidence to ground the interface geometry.")
    if _uses_chronobiology(mission) and not mission.chronobiology_program.get("scheduled_controls"):
        warnings.append("Chronobiology scheduling is enabled without explicit scheduled controls; pulse plans may be underspecified.")
    if _uses_containment_circuit(mission) and not _uses_safety_envelope(mission):
        warnings.append("Containment circuit lattice is configured without an operational safety envelope to govern tripwire actions.")
    if _uses_lineage_memory(mission) and not _uses_provenance(mission):
        warnings.append("Lineage memory recording is configured without FAIR provenance requirements; audit value will be limited.")
    if _uses_spatial_niche(mission) and not mission.multimodal_spatial_fusion:
        warnings.append("Spatial niche modeling is active without an explicit multimodal fusion uncertainty budget.")
    if _uses_bio_computing(mission) and not _uses_spatial_sim(mission):
        warnings.append("Bio-hybrid storage planning lacks a spatial whole-cell simulation gate.")
    if _risk_tier(mission) == "high" and not mission.hazard_audit_profile:
        warnings.append("High-risk mission is using the default hazard audit profile; review hazard scopes explicitly before escalation.")
    if not mission.constraints.get("disallowed_traits"):
        warnings.append("Mission constraints do not declare disallowed traits.")

    return warnings


def _validation_ladder(mission: Mission) -> list[dict[str, str]]:
    ladder = [
        {
            "name": "in_silico_ranking",
            "status": "ready",
            "detail": "Foundation-model ranking and safety triage can proceed locally.",
        },
        {
            "name": "cell_free_validation",
            "status": "required" if _uses_cell_free(mission) else "recommended",
            "detail": (
                "Cell-free extracts are configured for fast validation."
                if _uses_cell_free(mission)
                else "No cell-free gate is configured yet."
            ),
        },
        {
            "name": "analog_environment",
            "status": "required" if _uses_sim_to_real(mission) or _uses_spatial_niche(mission) else "recommended",
            "detail": (
                "Analog chamber or structured habitat validation is needed before transfer."
                if _uses_sim_to_real(mission) or _uses_spatial_niche(mission)
                else "Analog validation remains advisable before scaling."
            ),
        },
        {
            "name": "controller_commit",
            "status": "gated" if _uses_safety_envelope(mission) else "blocked",
            "detail": (
                "Controller updates are gated by the operational safety envelope."
                if _uses_safety_envelope(mission)
                else "Controller commits should remain blocked until an operational envelope is defined."
            ),
        },
        {
            "name": "pilot_deployment",
            "status": "blocked" if not mission.safety_profile.get("autonomous_deployment_allowed") else "gated",
            "detail": (
                "Deployment remains blocked by policy unless human review clears a staged pilot."
                if not mission.safety_profile.get("autonomous_deployment_allowed")
                else "Pilot deployment is policy-allowed but still requires staged review."
            ),
        },
    ]
    return ladder


def _recommended_next_steps(mission: Mission, warnings: list[str]) -> list[str]:
    steps: list[str] = []
    if warnings:
        steps.append("Resolve the validation warnings before promoting any controller or genome proposal.")
    if _uses_single_cell_foundation(mission):
        steps.append("Benchmark atlas transfer and zero-shot label quality before using cell-state projections to prioritize edits.")
    if _uses_metabolic_flux(mission):
        steps.append("Review the flux envelope and redox bottlenecks before locking pathway edits or feed schedules.")
    if _uses_sequence_perturbation(mission):
        steps.append("Review promoter rewrites against reporter or MPRA-style assays before escalating to chassis work.")
    if _uses_perturbation_benchmark(mission):
        steps.append("Inspect unseen-perturbation and unseen-cell-state holdout failures before trusting zero-shot response predictions.")
    if _uses_protein_evolution(mission):
        steps.append("Keep each protein evolution round human-gated and promote only variants that pass assay QC.")
    if _uses_cell_free(mission):
        steps.append("Run the declared cell-free validation matrix before organism-level engineering.")
    if _uses_biosensor_optimization(mission):
        steps.append("Screen counter-selectants and freeze-dried biosensor variants before any operational deployment plan.")
    if _uses_cell_imaging(mission):
        steps.append("Audit CellSAM segmentation masks on representative assay frames before downstream spatial decisions.")
    if _uses_biomineralization(mission):
        steps.append("Validate biomineral adhesion, delamination, and shielding assumptions on representative habitat surfaces.")
    if _uses_spatial_niche(mission):
        steps.append("Validate niche exclusion zones and communication corridors in a structured analog assay.")
    if _uses_multimodal_fusion(mission):
        steps.append("Review multimodal fusion uncertainty maps before using imputed spatial signals in decisions.")
    if _uses_chronobiology(mission):
        steps.append("Stress-test phase drift and day-night fallback schedules before automating rhythm-aware control.")
    if _uses_containment_circuit(mission):
        steps.append("Bench-test every containment tripwire and reversion path before allowing autonomous runtime transitions.")
    if _uses_sim_to_real(mission):
        steps.append("Calibrate the sim-to-real bridge in an Earth-analog or pilot chamber before deployment.")
    if _uses_safety_envelope(mission):
        steps.append("Approve the operational design domain, control barriers, and safe-state ladder with operators.")
    if _uses_labshield_audit(mission):
        steps.append("Have a human reviewer sign off the hazard audit blind spots and refusal triggers.")
    if _uses_lineage_memory(mission):
        steps.append("Verify event logging burden and decode plans before relying on lineage memory for audits.")
    if not steps:
        steps.append("Preserve artifacts and route the dossier to human review before any real-world action.")
    return steps[:5]


def _summary_metrics(mission: Mission, plan: dict[str, Any]) -> dict[str, Any]:
    unique_anchors = {
        anchor
        for stage in plan["stages"]
        for anchor in stage.get("research_anchors", [])
    }
    return {
        "total_stages": len(plan["stages"]),
        "review_gates": sum(1 for stage in plan["stages"] if stage.get("review_required")),
        "active_innovations": len(plan["active_innovations"]),
        "research_anchors": len(unique_anchors),
        "control_surface_count": len(mission.control_surface),
        "success_metric_count": len(mission.success_metrics),
    }


def _preview_counterfactual_type(question: str) -> str:
    q = question.lower()
    if "knock" in q or "disable" in q:
        return "Knockout"
    if "overexpress" in q or "strength" in q or "increase" in q:
        return "Upregulate"
    if "delay" in q or "timing" in q:
        return "Timing Shift"
    return "What-If Edit"


def _preview_data(mission: Mission, plan: dict[str, Any]) -> dict[str, Any]:
    preview: dict[str, Any] = {}

    if _uses_pareto(mission):
        points = []
        for index, label in enumerate(mission.pareto_objectives[:6]):
            seed = f"{mission.mission_id}:pareto:{label}:{index}"
            points.append({
                "label": _preview_note(label),
                "x": _stable_int(seed + ":x", 62, 96),
                "y": _stable_int(seed + ":y", 64, 98),
                "r": _stable_int(seed + ":r", 8, 16),
            })
        preview["pareto_frontier"] = points

    if _uses_counterfactuals(mission):
        rows = []
        for index, question in enumerate(mission.counterfactual_questions[:6], start=1):
            seed = f"{mission.mission_id}:counterfactual:{question}:{index}"
            sign = "+" if _stable_int(seed + ":sign", 0, 1) else "-"
            rows.append({
                "id": f"CF-{index:02d}",
                "type": _preview_counterfactual_type(question),
                "target": question.rstrip("?"),
                "impact": f"{sign}{_stable_int(seed + ':impact', 4, 24)}%",
                "note": "Planner preview only. Use this as a review prompt, not empirical evidence.",
            })
        preview["counterfactual_map"] = rows

    if _uses_sequence_perturbation(mission):
        config = mission.sequence_perturbation_config
        cell_types = config.get("reference_cell_types", []) or ["reference state"]
        motifs = []
        for index, target in enumerate(config.get("target_sequences", [])[:6]):
            seed = f"{mission.mission_id}:motif:{target}:{index}"
            motifs.append({
                "name": _preview_note(target),
                "gain": _stable_int(seed + ":gain", 61, 95),
                "note": (
                    f"Best transfer in {cell_types[index % len(cell_types)].replace('_', ' ')}. "
                    "Planning proxy derived from mission structure."
                ),
            })
        preview["regulatory_grammar"] = motifs

    if _uses_perturbation_benchmark(mission):
        config = mission.perturbation_benchmark_config
        holdouts = config.get("holdout_axes", []) or [
            "unseen_perturbations",
            "unseen_cell_states",
            "cross_context_transfer",
        ]
        rows = []
        for index, holdout in enumerate(holdouts[:4], start=1):
            seed = f"{mission.mission_id}:benchmark:{holdout}:{index}"
            rows.append({
                "name": _preview_note(holdout),
                "score": _stable_int(seed + ":score", 58, 93),
                "baseline": _stable_int(seed + ":baseline", 41, 78),
            })
        preview["perturbation_benchmark"] = rows

    if _uses_spatial_niche(mission):
        config = mission.spatial_niche_program
        axes = config.get("niche_axes", []) or ["stress_gradient"]
        comms = config.get("communication_targets", []) or ["cell coordination"]
        niche_rows = []
        for index, axis in enumerate((axes + comms)[:6]):
            seed = f"{mission.mission_id}:niche:{axis}:{index}"
            score = _stable_float(seed + ":score", 0.61, 0.97)
            if score >= 0.86:
                cls = "stable"
                state = "Stable"
            elif score >= 0.74:
                cls = "mid"
                state = "Transition"
            else:
                cls = "hot"
                state = "Vulnerable"
            niche_rows.append({
                "name": _preview_note(axis),
                "state": state,
                "score": f"{score:.2f}",
                "cls": cls,
            })
        preview["spatial_niche"] = niche_rows

    if _uses_multimodal_fusion(mission):
        config = mission.multimodal_spatial_fusion
        modalities = config.get("modalities", []) or ["histology", "imaging", "transcriptomics"]
        targets = config.get("fusion_targets", []) or ["signal recovery", "morphology alignment", "uncertainty tracking"]
        rows = []
        for index, modality in enumerate(modalities[:4], start=1):
            target = targets[(index - 1) % len(targets)]
            seed = f"{mission.mission_id}:fusion:{modality}:{target}:{index}"
            rows.append({
                "name": _preview_note(modality),
                "target": _preview_note(target),
                "alignment": _stable_int(seed + ":align", 63, 95),
                "uncertainty": _stable_int(seed + ":uncertainty", 5, 28),
            })
        preview["multimodal_fusion"] = rows

    if _uses_quantum_sim(mission):
        targets = mission.quantum_simulation_targets or ["target"]
        offset = max(len(targets) - 1, 0)
        preview["quantum_curve"] = {
            "labels": ["0", "10", "20", "30", "40", "50"],
            "variance": [120 - offset * 6, 82 - offset * 5, 49 - offset * 4, 24 - offset * 3, 17 - offset * 2, 12],
            "affinity": [-14 - offset, -30 - offset * 2, -61 - offset * 3, -82 - offset * 3, -91 - offset * 2, -95],
        }

    if _uses_edge_swarm(mission):
        nodes = []
        for index in range(1, 13):
            seed = f"{mission.mission_id}:swarm:{index}"
            active = _stable_int(seed, 0, 9) > 1
            nodes.append({
                "id": f"NOD-{index:03d}",
                "active": active,
                "status": "Sync" if active else "Wait",
            })
        preview["swarm_nodes"] = nodes

    if _uses_hachimoji(mission):
        alphabet = "ATCGZPSB"
        preview["hachimoji_sequence"] = "".join(
            alphabet[_stable_int(f"{mission.mission_id}:hachimoji:{index}", 0, len(alphabet) - 1)]
            for index in range(30)
        )

    if _uses_bio_computing(mission):
        preview["bio_storage"] = {
            "capacity_label": mission.bio_computing_payload.get("data_type", "1.0 Exabyte Archive"),
            "utilization_percent": _stable_int(f"{mission.mission_id}:storage", 58, 92),
        }

    if _uses_spatial_sim(mission):
        points = []
        for index in range(60):
            points.append({
                "x": _stable_int(f"{mission.mission_id}:spatial:x:{index}", -50, 50),
                "y": _stable_int(f"{mission.mission_id}:spatial:y:{index}", -50, 50),
                "r": _stable_int(f"{mission.mission_id}:spatial:r:{index}", 2, 8),
            })
        preview["spatial_points"] = points

    if _uses_safety_envelope(mission):
        config = mission.safety_envelope
        odd = config.get("operational_design_domain", [])
        barriers = config.get("control_barriers", [])
        preview["safety_envelope"] = [
            {
                "name": "ODD Bounds",
                "detail": f"{max(len(odd), 1)} active operating limits declared.",
                "level": f"{_stable_int(f'{mission.mission_id}:safety:odd', 88, 99)}%",
            },
            {
                "name": "Barrier Monitors",
                "detail": ", ".join(barriers[:3]) if barriers else "No explicit barriers declared.",
                "level": f"{_stable_int(f'{mission.mission_id}:safety:barriers', 80, 97)}%",
            },
            {
                "name": "Transaction Guard",
                "detail": config.get("transaction_protocol", "human-in-the-loop gated actuation"),
                "level": f"{_stable_int(f'{mission.mission_id}:safety:txn', 90, 100)}%",
            },
            {
                "name": "Fallback States",
                "detail": ", ".join(config.get("safe_states", [])[:3]) or "No fallback safe states declared.",
                "level": f"{_stable_int(f'{mission.mission_id}:safety:safe', 86, 99)}%",
            },
        ]

    if _uses_labshield_audit(mission):
        config = mission.hazard_audit_profile
        focuses = config.get("scenario_focus", []) or [
            "biological containment",
            "autonomy drift",
            "cross-modal evidence failure",
        ]
        rows = []
        for index, focus in enumerate(focuses[:4], start=1):
            seed = f"{mission.mission_id}:hazard:{focus}:{index}"
            severity = _stable_int(seed + ":severity", 2, 5)
            rows.append({
                "name": _preview_note(focus),
                "severity": severity,
                "coverage": _stable_int(seed + ":coverage", 61, 96),
            })
        preview["hazard_audit"] = rows

    return preview


# ---------------------------------------------------------------------------
# Plan compilation
# ---------------------------------------------------------------------------

def compile_mission(mission: Mission) -> dict[str, Any]:
    stages = build_stages(mission)
    risk_tier = _risk_tier(mission)

    # Detect which innovation modules are active
    active_innovations = []
    if _uses_ensemble(mission):
        active_innovations.append("multi_model_ensemble")
    if _uses_epigenomics(mission):
        active_innovations.append("epigenomic_landscape")
    if _uses_single_cell_foundation(mission):
        active_innovations.append("single_cell_foundation_mapping")
    if _uses_metabolic_flux(mission):
        active_innovations.append("metabolic_flux_sandbox")
    if _uses_cell_free(mission):
        active_innovations.append("cell_free_prototyping")
    if _uses_biosensor_optimization(mission):
        active_innovations.append("cell_free_biosensor_optimization")
    if _uses_bayesian(mission):
        active_innovations.append("bayesian_experiment_design")
    if _uses_chronobiology(mission):
        active_innovations.append("chronobiology_scheduler")
    if _uses_containment_circuit(mission):
        active_innovations.append("containment_circuit_lattice")
    if _uses_sim_to_real(mission):
        active_innovations.append("sim_to_real_bridge")
    if _uses_counterfactuals(mission):
        active_innovations.append("counterfactual_variant_atlas")
    if _uses_sequence_perturbation(mission):
        active_innovations.append("regulatory_sequence_program")
    if _uses_perturbation_benchmark(mission):
        active_innovations.append("perturbation_generalization_benchmark")
    if _uses_spatial_niche(mission):
        active_innovations.append("spatial_niche_modeling")
    if _uses_multimodal_fusion(mission):
        active_innovations.append("multimodal_spatial_fusion")
    if _uses_cell_imaging(mission):
        active_innovations.append("cell_imaging_foundation")
    if _uses_biomineralization(mission):
        active_innovations.append("biomineral_interface_forge")
    if _uses_safety_envelope(mission):
        active_innovations.append("operational_safety_envelope")
    if _uses_labshield_audit(mission):
        active_innovations.append("labshield_hazard_audit")
    if _uses_pareto(mission):
        active_innovations.append("multiobjective_frontier")
    if _uses_provenance(mission):
        active_innovations.append("fair_provenance_bundle")
    if _uses_co_scientist(mission):
        active_innovations.append("autonomous_co_scientist")
    if _uses_synthetic_data(mission):
        active_innovations.append("synthetic_twin_data")
    if _uses_protein_evolution(mission):
        active_innovations.append("protein_evolution_biofoundry")
    if _uses_quantum_sim(mission):
        active_innovations.append("quantum_structural_refinement")
    if _uses_edge_swarm(mission):
        active_innovations.append("edge_ai_swarm_orchestration")
    if _uses_zkp_security(mission):
        active_innovations.append("zkp_biosecurity_anchor")
    if _uses_lineage_memory(mission):
        active_innovations.append("lineage_memory_recorder")
    if _uses_hachimoji(mission):
        active_innovations.append("hachimoji_transpilation")
    if _uses_bio_computing(mission):
        active_innovations.append("bio_hybrid_data_storage")
    if _uses_spatial_sim(mission):
        active_innovations.append("spatial_whole_cell_sim")

    plan = {
        "mission_id": mission.mission_id,
        "mission_name": mission.name,
        "risk_tier": risk_tier,
        "domain": mission.domain,
        "objective": mission.objective,
        "active_innovations": active_innovations,
        "stages": [asdict(stage) for stage in stages],
        "review_policy": {
            "human_review_required": bool(mission.safety_profile.get("human_review_required")),
            "autonomous_deployment_allowed": bool(
                mission.safety_profile.get("autonomous_deployment_allowed", False)
            ),
        },
    }
    warnings = _validation_warnings(mission, risk_tier)
    plan["warnings"] = warnings
    plan["recommended_next_steps"] = _recommended_next_steps(mission, warnings)
    plan["validation_ladder"] = _validation_ladder(mission)
    plan["summary"] = _summary_metrics(mission, plan)
    plan["preview_data"] = _preview_data(mission, plan)
    return plan


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def render_report(mission: Mission, plan: dict[str, Any]) -> str:
    lines = [
        f"# {mission.name}",
        "",
        f"- Mission ID: `{mission.mission_id}`",
        f"- Domain: `{mission.domain}`",
        f"- Risk tier: `{plan['risk_tier']}`",
        "",
    ]

    # Innovation summary
    innovations = plan.get("active_innovations", [])
    if innovations:
        lines.extend([
            "## Active Innovation Modules",
            "",
        ])
        labels = {
            "multi_model_ensemble": "Multi-Model Ensemble Genomic Engine (Evo 2 + GENERator + AlphaGenome)",
            "epigenomic_landscape": "Epigenomic Landscape Analyzer (EpiAgent-style CRE perturbation)",
            "single_cell_foundation_mapping": "Single-Cell Atlas Mapping Tool (CellFM transfer and retrieval)",
            "metabolic_flux_sandbox": "Metabolic Flux Sandbox Tool (cofactor, redox, and pathway economics)",
            "cell_free_prototyping": "Cell-Free Rapid Prototyping Planner",
            "cell_free_biosensor_optimization": "Cell-Free Biosensor Optimization Tool (active-learning screen design)",
            "bayesian_experiment_design": "Bayesian Optimization Closed-Loop Experiment Design",
            "chronobiology_scheduler": "Chronobiology Pulse Scheduler Tool",
            "containment_circuit_lattice": "Containment Circuit Lattice Tool",
            "sim_to_real_bridge": "Sim-to-Real Transfer Bridge for BioControl",
            "counterfactual_variant_atlas": "Counterfactual Variant Atlas for What-If Regulatory Design",
            "regulatory_sequence_program": "Regulatory Grammar and Sequence Perturbation Planner (GET + PARM/STRAND)",
            "perturbation_generalization_benchmark": "Perturbation Generalization Benchmark Harness",
            "spatial_niche_modeling": "Spatial Niche and Microenvironment Twin (Nicheformer)",
            "multimodal_spatial_fusion": "Multimodal Spatial Fusion Board (OmiCLIP + VISTA)",
            "cell_imaging_foundation": "Cell Imaging Segmentation Tool (CellSAM assay masks and QC)",
            "biomineral_interface_forge": "Biomineral Interface Forge Tool",
            "operational_safety_envelope": "Operational Safety Envelope Compiler (Safe-SDL)",
            "labshield_hazard_audit": "LABSHIELD Hazard Audit Layer",
            "multiobjective_frontier": "Multi-Objective Pareto Frontier Planner",
            "fair_provenance_bundle": "FAIR Provenance and Twin Fidelity Bundle",
            "autonomous_co_scientist": "Autonomous LLM Co-Scientist Agent Loop",
            "synthetic_twin_data": "Synthetic Twin Data Generation Service",
            "protein_evolution_biofoundry": "Autonomous Protein Evolution Biofoundry Tool",
            "quantum_structural_refinement": "AQuaRef Hybrid Quantum-Classical Simulation",
            "edge_ai_swarm_orchestration": "Agentic Edge-AI Swarm Orchestration",
            "zkp_biosecurity_anchor": "Zero-Knowledge Proof (ZKP) BioSecure Sovereign Vault",
            "lineage_memory_recorder": "DNA Lineage Memory Recorder Tool",
            "hachimoji_transpilation": "Hachimoji 8-Letter DNA Orthogonal Transpiler (Genetic Firewall)",
            "bio_hybrid_data_storage": "Bio-Hybrid DNA Neuromorphic Memory Storage",
            "spatial_whole_cell_sim": "Spatial Transcriptomics FM Whole-Cell Physics Sandbox",
        }
        for inn in innovations:
            lines.append(f"- **{labels.get(inn, inn)}**")
        lines.append("")

    lines.extend([
        "## Objective",
        "",
        mission.objective,
        "",
        "## Integrated idea",
        "",
        (
            "NexusBioTwin turns a mission spec into a cross-scale plan that starts with "
            "genome design, filters through protein and enzyme triage, tests habitat and "
            "consortium behavior under stress, and ends in a closed-loop controller plan."
        ),
        "",
        "The stack centers Evo 2 as the genomic proposal engine while preserving strict "
        "human review and audit boundaries.",
        "",
        "Visual previews in the studio are deterministic planning proxies derived from the mission spec, "
        "not empirical assay outputs.",
        "",
    ])

    warnings = plan.get("warnings", [])
    if warnings:
        lines.extend([
            "## Validation Warnings",
            "",
        ])
        lines.extend([f"- {warning}" for warning in warnings])
        lines.append("")

    # Innovation-specific notes
    if _uses_ensemble(mission):
        models = ", ".join(mission.ensemble_models)
        lines.extend([
            "### Multi-Model Ensemble Strategy",
            "",
            f"This mission activates the multi-model ensemble engine with: **{models}**. "
            "Each candidate is scored by all models independently, then a calibrated ensemble "
            "score is computed. Inter-model disagreements are flagged for human review.",
            "",
        ])

    if _uses_epigenomics(mission):
        targets = ", ".join(mission.epigenomic_targets)
        lines.extend([
            "### Epigenomic Landscape Analysis",
            "",
            f"Targeted CRE analysis for: **{targets}**. "
            "The epigenomic analyzer encodes chromatin accessibility into cell sentences "
            "and predicts the regulatory impact of CRE perturbations using EpiAgent-style "
            "bidirectional attention.",
            "",
        ])

    if _uses_single_cell_foundation(mission):
        config = mission.single_cell_foundation_config
        atlas = config.get("reference_atlas", "mission single-cell atlas")
        tasks = ", ".join(config.get("tasks", [])) or "cell-state projection and retrieval"
        lines.extend([
            "### Single-Cell Atlas Mapping",
            "",
            f"The planner projects mission candidates into **{atlas}** to support **{tasks}**. "
            "This adds cell-state transfer, atlas retrieval, and zero-shot labeling priors before "
            "regulatory edits are escalated.",
            "",
        ])

    if _uses_metabolic_flux(mission):
        config = mission.metabolic_flux_program
        substrates = ", ".join(config.get("substrates", [])) or "mission feedstocks"
        products = ", ".join(config.get("target_products", [])) or "mission outputs"
        lines.extend([
            "### Metabolic Flux Sandbox",
            "",
            f"The planner adds a flux economics pass from **{substrates}** into **{products}**. "
            "This stage surfaces cofactor, ATP, and redox bottlenecks before pathway changes get "
            "locked into downstream assays.",
            "",
        ])

    if _uses_sequence_perturbation(mission):
        config = mission.sequence_perturbation_config
        targets = ", ".join(config.get("target_sequences", [])) or "mission-critical regulatory sequences"
        readouts = ", ".join(config.get("perturbation_readouts", [])) or "transcriptional response readouts"
        lines.extend([
            "### Regulatory Grammar and Sequence Perturbation",
            "",
            f"This mission activates sequence-conditioned design for: **{targets}**. "
            "The planner combines transcriptional foundation modeling with promoter grammar "
            f"priors so zero-shot rewrites can be ranked against {readouts}.",
            "",
            "<!-- CHART:REGULATORY_GRAMMAR -->",
            "",
        ])

    if _uses_perturbation_benchmark(mission):
        config = mission.perturbation_benchmark_config
        holdouts = ", ".join(config.get("holdout_axes", [])) or "unseen perturbations, unseen cell states"
        lines.extend([
            "### Perturbation Generalization Benchmark",
            "",
            f"The planner benchmarks zero-shot perturbation response under holdout settings for: **{holdouts}**. "
            "This reduces the chance that a model looks strong in-distribution but fails on the first novel context.",
            "",
            "<!-- CHART:PERTURB_BENCHMARK -->",
            "",
        ])

    if _uses_pareto(mission):
        frontier = ", ".join(mission.pareto_objectives)
        lines.extend([
            "### Multi-Objective Frontier Planning",
            "",
            f"The planner preserves a Pareto frontier over: **{frontier}**. "
            "This avoids hiding safety, resilience, or energy penalties inside a single "
            "aggregate score.",
            "",
            "<!-- CHART:PARETO_FRONTIER -->",
            "",
        ])

    if _uses_counterfactuals(mission):
        lines.extend([
            "### Counterfactual Variant Atlas",
            "",
            "The planner builds an explicit what-if table for genome edits rather than "
            "only emitting ranked candidates. This makes the output more useful for human "
            "review.",
            "",
            "<!-- CHART:COUNTERFACTUAL_MAP -->",
            "",
        ])

    if _uses_cell_free(mission):
        extracts = ", ".join(mission.cell_free_chassis)
        lines.extend([
            "### Cell-Free Rapid Prototyping",
            "",
            f"Before committing to full chassis engineering, this mission gates constructs "
            f"through cell-free validation using: **{extracts}**. "
            "This shortens the design-build-test cycle from weeks to hours.",
            "",
        ])

    if _uses_biosensor_optimization(mission):
        config = mission.biosensor_optimization
        sensor = config.get("sensor_family", "cell-free biosensor family")
        analytes = ", ".join(config.get("target_analytes", [])) or "mission analytes"
        lines.extend([
            "### Cell-Free Biosensor Optimization",
            "",
            f"The planner adds an active-learning biosensor screen around **{sensor}** for **{analytes}**. "
            "This stage prioritizes variant batches, counter-selectant panels, and freeze-dried "
            "validation plans rather than brute-force screening the full design space.",
            "",
        ])

    if _uses_protein_evolution(mission):
        config = mission.protein_evolution_program
        proteins = ", ".join(config.get("seed_proteins", [])) or "mission enzymes"
        objective = config.get("fitness_objective", "improve protein fitness")
        lines.extend([
            "### Autonomous Protein Evolution Biofoundry",
            "",
            f"A protein evolution loop is configured for **{proteins}** to **{objective}**. "
            "The planner emits round-by-round mutant batches and keeps the self-driving "
            "biofoundry workflow under human review.",
            "",
        ])

    if _uses_cell_imaging(mission):
        config = mission.cell_imaging_program
        modalities = ", ".join(config.get("modalities", [])) or "microscopy and spatial assay imagery"
        targets = ", ".join(config.get("segmentation_targets", [])) or "mission structures"
        lines.extend([
            "### Cell Imaging Segmentation",
            "",
            f"The planner uses foundation-model segmentation over **{modalities}** to isolate **{targets}**. "
            "Mask quality control is surfaced explicitly before morphology or spatial evidence is trusted.",
            "",
        ])

    if _uses_biomineralization(mission):
        config = mission.biomineralization_program
        minerals = ", ".join(config.get("target_minerals", [])) or "mission minerals"
        functions = ", ".join(config.get("material_functions", [])) or "material interface functions"
        lines.extend([
            "### Biomineral Interface Forge",
            "",
            f"The planner co-designs biomineral interfaces for **{minerals}** to support **{functions}**. "
            "This creates a dedicated stage for biofilm-material adhesion, shielding, and filtration ideas "
            "instead of burying them inside generic habitat notes.",
            "",
        ])

    if _uses_spatial_niche(mission):
        config = mission.spatial_niche_program
        reference_map = config.get("reference_map", "mission spatial atlas")
        assays = ", ".join(config.get("assays", [])) or "spatial omics"
        lines.extend([
            "### Spatial Niche and Microenvironment Twin",
            "",
            f"The planner uses **{assays}** against **{reference_map}** to preserve local "
            "context instead of flattening the mission into bulk averages. Niche transitions, "
            "communication corridors, and exclusion zones are surfaced before controller design.",
            "",
            "<!-- CHART:SPATIAL_NICHE -->",
            "",
        ])

    if _uses_multimodal_fusion(mission):
        config = mission.multimodal_spatial_fusion
        modalities = ", ".join(config.get("modalities", [])) or "histology, imaging, transcriptomics"
        lines.extend([
            "### Multimodal Spatial Evidence Fusion",
            "",
            f"The planner fuses **{modalities}** so morphology, imaging, and transcriptomic evidence can be "
            "aligned with explicit uncertainty tracking before spatial decisions are trusted.",
            "",
            "<!-- CHART:MULTIMODAL_FUSION -->",
            "",
        ])

    if _uses_bayesian(mission):
        bp = mission.bayesian_parameters
        lines.extend([
            "### Bayesian Optimization Strategy",
            "",
            f"- Objective: `{bp.get('objective_function', 'unspecified')}`",
            f"- Search dimensions: `{', '.join(bp.get('search_dimensions', []))}`",
            f"- Acquisition function: `{bp.get('acquisition_function', 'EI')}`",
            f"- Batch size: `{bp.get('batch_size', 1)}`",
            f"- Max iterations: `{bp.get('max_iterations', 25)}`",
            "",
            "The cognitive digital twin runs surrogate model updates after each batch, "
            "recomputing the acquisition surface to select the next set of experiment arms.",
            "",
        ])

    if _uses_chronobiology(mission):
        config = mission.chronobiology_program
        cycle = config.get("cycle_length_hours", 24)
        scheduled = ", ".join(config.get("scheduled_controls", [])) or "mission controls"
        lines.extend([
            "### Chronobiology Pulse Scheduler",
            "",
            f"A cycle-aware scheduler is active over **{scheduled}** with a **{cycle}-hour** rhythm. "
            "The planner now preserves phase drift tests, day-night safe modes, and zeitgeber-driven "
            "actuation windows as first-class artifacts.",
            "",
        ])

    if _uses_containment_circuit(mission):
        config = mission.containment_circuit_program
        layers = ", ".join(config.get("layers", [])) or "biocontainment layers"
        lines.extend([
            "### Containment Circuit Lattice",
            "",
            f"A layered biocontainment plan is compiled over **{layers}**. "
            "Tripwires, reversion modes, and escape-path audits are made explicit before any "
            "autonomous runtime privileges are considered.",
            "",
        ])

    if _uses_sim_to_real(mission):
        s2r = mission.sim_to_real_config
        lines.extend([
            "### Sim-to-Real Transfer Bridge",
            "",
            f"- Simulation environment: `{s2r.get('sim_environment', '?')}`",
            f"- Real environment: `{s2r.get('real_environment', '?')}`",
            f"- Calibration strategy: `{s2r.get('calibration_strategy', 'manual')}`",
            f"- Transfer validation: `{s2r.get('transfer_validation', 'N/A')}`",
            "",
        ])
        dr = s2r.get("domain_randomization", {})
        if dr:
            lines.append("Domain randomization ranges:")
            lines.append("")
            for param, rng in dr.items():
                lines.append(f"- `{param}`: {rng}")
            lines.append("")

    if _uses_safety_envelope(mission):
        config = mission.safety_envelope
        lines.extend([
            "### Operational Safety Envelope",
            "",
            f"- Transaction protocol: `{config.get('transaction_protocol', 'human-in-the-loop gated actuation')}`",
            f"- Safe states: `{', '.join(config.get('safe_states', [])) or 'fallback safe states'}`",
            "",
            "Safe-SDL style operational design domains and control barrier monitors are compiled "
            "before stateful actuation updates are allowed.",
            "",
            "<!-- CHART:SAFETY_ENVELOPE -->",
            "",
        ])
        odd = config.get("operational_design_domain", [])
        if odd:
            lines.append("Operational design domain:")
            lines.append("")
            for item in odd:
                lines.append(f"- `{item}`")
            lines.append("")

    if _uses_labshield_audit(mission):
        config = mission.hazard_audit_profile
        focus = ", ".join(config.get("scenario_focus", [])) or "biological containment, autonomy drift, evidence failure"
        lines.extend([
            "### LABSHIELD Hazard Audit",
            "",
            f"A hazard audit layer is active with focus on: **{focus}**. "
            "This stage looks for reasoning blind spots, refusal-trigger gaps, and weak hazard coverage before escalation.",
            "",
            "<!-- CHART:HAZARD_AUDIT -->",
            "",
        ])

    if _uses_lineage_memory(mission):
        config = mission.lineage_memory_program
        events = ", ".join(config.get("events_to_record", [])) or "mission events"
        lines.extend([
            "### DNA Lineage Memory Recorder",
            "",
            f"The planner includes a biological event logging layer for **{events}**. "
            "Recorder burden, decode workflows, and archive cadence are preserved as operational "
            "audit artifacts rather than left implicit.",
            "",
        ])

    if _uses_quantum_sim(mission):
        targets = ", ".join(mission.quantum_simulation_targets)
        lines.extend([
            "### AQuaRef Quantum Simulation Cluster",
            "",
            f"Offloading structural refinement for: **{targets}**.",
            "This stage uses hybrid NISQ quantum-classical algorithms to solve non-linear molecular "
            "docking problems exponentially faster.",
            "",
            "<!-- CHART:QUANTUM_REFINEMENT -->",
            "",
        ])

    if _uses_edge_swarm(mission):
        lines.extend([
            "### Edge-AI Swarm Orchestration",
            "",
            "The physical deployment is guided by decentralized Small Language Models running on the edge. "
            "Coordination happens locally without cloud latency, ensuring high-resilience swarm logic.",
            "",
            "<!-- CHART:SWARM_TELEMETRY -->",
            "",
        ])

    if _uses_zkp_security(mission):
        level = mission.zkp_security_level
        lines.extend([
            f"### Zero-Knowledge Proof (ZKP) Biosecurity Vault (Level: {level})",
            "",
            "All model weights, sequence data, and biometric telemetry are cryptographically wrapped. "
            "The twin can prove it adheres to safety bounds without disclosing proprietary formulas or "
            "sensitive omics data to regulators or external platforms.",
            "",
        ])

    if _uses_hachimoji(mission):
        lines.extend([
            "### Hachimoji DNA Genetic Firewall",
            "",
            "Standard sequence transpiled into an 8-letter synthetic alphabet (A, T, C, G, **Z, P, S, B**). "
            "This creates an absolute biological quarantine, preventing gene transfer into natural biospheres.",
            "",
            "<!-- CHART:HACHIMOJI_ALPHABET -->",
            "",
        ])

    if _uses_bio_computing(mission):
        payload = mission.bio_computing_payload.get("data_type", "exabytes")
        lines.extend([
            "### Bio-Hybrid Neuromorphic DNA Storage",
            "",
            f"The swarm is optimized not just for survival, but to act as a living memory resistor encoding [{payload}] of data.",
            "This leverages DNA-perovskite interaction lattices for near-zero power storage.",
            "",
            "<!-- CHART:BIO_COMPUTING_STORAGE -->",
            "",
        ])

    if _uses_spatial_sim(mission):
        res = mission.spatial_simulation_resolution
        lines.extend([
            f"### Spatial-FM Whole-Cell Simulation ({res})",
            "",
            "The organism's 3D internal physics and transcription states have been completely modeled via "
            "a Spatial Transcriptomics Foundation Model, replacing fluid approximations with true spatial reality.",
            "",
            "<!-- CHART:SPATIAL_SIMULATION -->",
            "",
        ])

    if _uses_provenance(mission):
        req = mission.provenance_requirements
        lines.extend([
            "### FAIR Provenance Bundle",
            "",
            f"- Bundle targets: `{', '.join(req.get('bundle_targets', []))}`",
            f"- Twin fidelity metrics: `{', '.join(req.get('twin_fidelity_metrics', []))}`",
            f"- Assay lineage required: `{req.get('assay_lineage_required', False)}`",
            "",
        ])

    ladder = plan.get("validation_ladder", [])
    if ladder:
        lines.extend([
            "## Validation Ladder",
            "",
        ])
        for item in ladder:
            lines.append(f"- `{item['name']}` [{item['status']}]: {item['detail']}")
        lines.append("")

    lines.extend(["## Stage plan", ""])

    for index, stage in enumerate(plan["stages"], start=1):
        lines.extend([
            f"### {index}. {stage['name']}",
            "",
            f"- Goal: {stage['goal']}",
            f"- Engine: {stage['engine']}",
            f"- Influences: {', '.join(stage['influences'])}",
            f"- Review required: {stage['review_required']}",
            "- Outputs:",
        ])
        lines.extend([f"  - {item}" for item in stage["outputs"]])
        lines.append("- Research anchors:")
        lines.extend([f"  - {link}" for link in stage["research_anchors"]])
        lines.append("")

    lines.extend([
        "## Safety notes",
        "",
        "- Use Evo 2 and related models for proposal and ranking, not direct execution.",
        "- Preserve uncertainty at every stage and block autonomous deployment by default.",
        "- Archive mission, plan, and review artifacts for every run.",
    ])

    if _uses_ensemble(mission):
        lines.append("- Flag all inter-model disagreements above threshold for human review.")
    if _uses_single_cell_foundation(mission):
        lines.append("- Treat atlas projections as priors; verify transfer quality before relying on zero-shot labels.")
    if _uses_metabolic_flux(mission):
        lines.append("- Review redox, ATP, and cofactor bottlenecks before turning pathway suggestions into build plans.")
    if _uses_cell_free(mission):
        lines.append("- Gate full organism engineering behind successful cell-free validation.")
    if _uses_biosensor_optimization(mission):
        lines.append("- Test cross-reactivity and freeze-dried performance before using biosensor recommendations operationally.")
    if _uses_sim_to_real(mission):
        lines.append("- Validate sim-to-real transfer in Earth-analog chambers before any deployment.")
    if _uses_bayesian(mission):
        lines.append("- Enforce stopping criteria and budget limits on Bayesian optimization loops.")
    if _uses_counterfactuals(mission):
        lines.append("- Preserve explicit no-go edit zones in the counterfactual atlas.")
    if _uses_sequence_perturbation(mission):
        lines.append("- Keep sequence rewrites inside experimentally supported promoter grammar regimes.")
    if _uses_perturbation_benchmark(mission):
        lines.append("- Reject perturbation predictions that fail generalization holdouts, even if in-distribution scores are high.")
    if _uses_spatial_niche(mission):
        lines.append("- Respect spatial exclusion zones and niche collapse risks before scale-up.")
    if _uses_multimodal_fusion(mission):
        lines.append("- Treat imputed spatial signals as provisional until uncertainty and alignment budgets are reviewed.")
    if _uses_cell_imaging(mission):
        lines.append("- Reject low-QC segmentation masks before they influence spatial or morphology-driven decisions.")
    if _uses_biomineralization(mission):
        lines.append("- Validate material adhesion and delamination assumptions experimentally before scaling biomineral designs.")
    if _uses_protein_evolution(mission):
        lines.append("- Keep autonomous protein evolution loops human-gated and archive every round's assay evidence.")
    if _uses_chronobiology(mission):
        lines.append("- Stress-test phase drift and circadian fallback schedules before automating time-based actuation.")
    if _uses_containment_circuit(mission):
        lines.append("- Bench-test each containment tripwire and fail-closed reversion path before runtime use.")
    if _uses_safety_envelope(mission):
        lines.append("- Enforce operational design domain checks and control barrier monitors at runtime.")
    if _uses_labshield_audit(mission):
        lines.append("- Escalate any unresolved hazard blind spots or refusal-trigger gaps to human review.")
    if _uses_lineage_memory(mission):
        lines.append("- Treat lineage memory readouts as audit evidence only after decode burden and retention limits are validated.")
    if _uses_pareto(mission):
        lines.append("- Keep safety and resilience as first-class Pareto objectives, not soft penalties.")

    next_steps = plan.get("recommended_next_steps", [])
    if next_steps:
        lines.extend([
            "",
            "## Recommended Next Steps",
            "",
        ])
        lines.extend([f"- {step}" for step in next_steps])

    lines.extend([
        "",
        "## Success metrics",
        "",
    ])
    lines.extend([f"- {metric}" for metric in mission.success_metrics])
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Run writer
# ---------------------------------------------------------------------------

def write_run(output_dir: Path, mission: Mission, plan: dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)

    active_innovations = plan.get("active_innovations", [])

    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "compiler": "nexusbiotwin 0.1.0",
        "mission_id": mission.mission_id,
        "mission_name": mission.name,
        "risk_tier": plan.get("risk_tier"),
        "summary": plan.get("summary", {}),
        "active_innovations": active_innovations,
        "files": [
            "manifest.json",
            "mission.json",
            "plan.json",
            "report.md",
        ],
    }
    (output_dir / "mission.json").write_text(
        json.dumps(asdict(mission), indent=2),
        encoding="utf-8",
    )
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    (output_dir / "plan.json").write_text(
        json.dumps(plan, indent=2),
        encoding="utf-8",
    )
    (output_dir / "report.md").write_text(
        render_report(mission, plan),
        encoding="utf-8",
    )
    return output_dir
