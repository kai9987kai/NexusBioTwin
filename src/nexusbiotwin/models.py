from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Mission:
    mission_id: str
    name: str
    domain: str
    objective: str
    environment: dict[str, Any]
    constraints: dict[str, Any]
    control_surface: list[str]
    success_metrics: list[str]
    safety_profile: dict[str, Any]
    # Optional fields for new innovation modules
    ensemble_models: list[str] = field(default_factory=list)
    epigenomic_targets: list[str] = field(default_factory=list)
    cell_free_chassis: list[str] = field(default_factory=list)
    bayesian_parameters: dict[str, Any] = field(default_factory=dict)
    sim_to_real_config: dict[str, Any] = field(default_factory=dict)
    counterfactual_questions: list[str] = field(default_factory=list)
    sequence_perturbation_config: dict[str, Any] = field(default_factory=dict)
    perturbation_benchmark_config: dict[str, Any] = field(default_factory=dict)
    single_cell_foundation_config: dict[str, Any] = field(default_factory=dict)
    metabolic_flux_program: dict[str, Any] = field(default_factory=dict)
    spatial_niche_program: dict[str, Any] = field(default_factory=dict)
    multimodal_spatial_fusion: dict[str, Any] = field(default_factory=dict)
    cell_imaging_program: dict[str, Any] = field(default_factory=dict)
    biomineralization_program: dict[str, Any] = field(default_factory=dict)
    biosensor_optimization: dict[str, Any] = field(default_factory=dict)
    protein_evolution_program: dict[str, Any] = field(default_factory=dict)
    containment_circuit_program: dict[str, Any] = field(default_factory=dict)
    chronobiology_program: dict[str, Any] = field(default_factory=dict)
    lineage_memory_program: dict[str, Any] = field(default_factory=dict)
    safety_envelope: dict[str, Any] = field(default_factory=dict)
    hazard_audit_profile: dict[str, Any] = field(default_factory=dict)
    pareto_objectives: list[str] = field(default_factory=list)
    provenance_requirements: dict[str, Any] = field(default_factory=dict)
    autonomous_co_scientist: bool = False
    synthetic_data_generation: dict[str, Any] = field(default_factory=dict)
    quantum_simulation_targets: list[str] = field(default_factory=list)
    edge_swarm_orchestration: bool = False
    zkp_security_level: str = "none"
    require_genetic_firewall: bool = False
    bio_computing_payload: dict[str, Any] = field(default_factory=dict)
    spatial_simulation_resolution: str = "none"


@dataclass(slots=True)
class Stage:
    name: str
    goal: str
    engine: str
    outputs: list[str]
    review_required: bool
    influences: list[str]
    research_anchors: list[str]


@dataclass(slots=True)
class EnsembleProposal:
    """A ranked genomic proposal produced by the multi-model ensemble engine."""

    candidate_id: str
    locus: str
    evo2_score: float
    generator_score: float
    alphagenome_score: float
    ensemble_score: float
    calibrated_uncertainty: float
    dominant_model: str
    notes: str = ""


@dataclass(slots=True)
class ExperimentArm:
    """One arm of a Bayesian optimization experiment."""

    arm_id: str
    parameters: dict[str, Any] = field(default_factory=dict)
    acquisition_value: float = 0.0
    expected_improvement: float = 0.0
    exploration_weight: float = 0.5
    status: str = "proposed"


@dataclass(slots=True)
class SimToRealCalibration:
    """Domain randomization parameters and transfer gap metrics."""

    parameter_name: str
    sim_range_low: float = 0.0
    sim_range_high: float = 1.0
    real_measured: float | None = None
    transfer_gap: float | None = None
    randomization_strategy: str = "uniform"
    notes: str = ""


@dataclass(slots=True)
class CREPerturbation:
    """A cis-regulatory element perturbation plan from the epigenomic landscape analyzer."""

    cre_id: str
    region: str
    perturbation_type: str  # knockout, activation, repression
    predicted_effect: str
    confidence: float = 0.0
    cell_type_context: str = ""


@dataclass(slots=True)
class CellFreeExperiment:
    """A cell-free rapid prototyping experiment design."""

    experiment_id: str
    construct: str
    chassis_extract: str
    reaction_conditions: dict[str, Any] = field(default_factory=dict)
    expected_yield: str = "unknown"
    go_no_go_threshold: str = ""
    safety_notes: str = ""
