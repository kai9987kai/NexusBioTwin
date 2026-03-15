# NexusBioTwin

NexusBioTwin is a local-first mission compiler for a genome-to-habitat digital twin stack.

It turns a mission JSON file into:

- a staged pipeline plan
- a safety and review checklist
- a structured run archive
- a Markdown dossier that ties the design back to the repo portfolio and current research

The concept combines ideas from:

- ProteinFoldingSimulation and DNA-Helix for molecular inspection
- Habitat-Genome-Compiler for mission specs, auditability, and safe-first planning
- didactic-lamp for ecosystem and stress simulation
- NeuroPulse-CableLab and NeuroFusion-Reactor for closed-loop controller design
- nexusflow, OmniForge, and Supermix_29 for workflow orchestration, local AI, and scientific copilot behavior
- Arc Institute's Evo 2 as the genome-scale scoring, embedding, and generation engine

## Why this exists

Most bio-AI projects stop at one layer:

- sequence design
- structure prediction
- bioreactor control
- ecosystem simulation

NexusBioTwin treats them as one stack. A mission definition drives the search for regulatory DNA, enzyme candidates, consortium policies, and controller behavior under environmental stress.

## Quick start

```bash
pip install -e .
python -m nexusbiotwin examples/pfas_brine_mission.json --output runs/pfas_brine_demo
```

The command writes:

- `manifest.json`
- `plan.json`
- `report.md`

## Sample output

The generated plan includes:

- policy and biosafety compilation
- Evo 2 genome proposal and ranking
- CellFM single-cell atlas mapping and transfer priors
- metabolic flux sandbox and cofactor budget analysis
- counterfactual variant atlas generation
- regulatory grammar and sequence perturbation planning
- perturbation generalization benchmarking
- protein and enzyme triage
- autonomous protein evolution biofoundry planning
- habitat and consortium twin simulation
- CellSAM microscopy and assay-image segmentation
- biomineral interface and habitat-material co-design
- spatial niche and microenvironment modeling
- multimodal spatial evidence fusion
- active-learning cell-free biosensor optimization
- Pareto frontier planning across performance, safety, and energy
- chronobiology pulse scheduling and phase-drift review
- layered containment circuit lattice planning
- Safe-SDL operational safety envelope compilation
- hazard audit and refusal-gap review
- DNA lineage memory recorder and forensic decode planning
- BioControl DSL controller synthesis
- FAIR provenance and twin fidelity packaging
- human review and escalation gates

## Files

- `ARCHITECTURE.md` describes the system design
- `RESEARCH.md` captures the research basis and linked papers
- `ROADMAP.md` breaks the build into implementation phases
- `examples/` contains mission specs

## Current state

This scaffold does not execute Evo 2, AlphaFold 3, or wet-lab workflows. It builds the planning, safety, and audit layer needed to integrate those systems sanely.
