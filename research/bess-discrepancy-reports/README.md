# BESS Discrepancy Reports

**Purpose:** This folder contains research reports and analysis documents related to resolving the BESS sizing discrepancy between the Buffer BESS (50-100 kW) and Grid-Forming BESS (400-600 kW) recommendations.

---

## Background

Two consolidated reports provide conflicting BESS recommendations for the same deployment scenario (1 MW generator + 0.5 MW GPU):

| Report                    | BESS Recommendation | Power Rating | Energy Capacity | Cost Estimate      |
|---------------------------|---------------------|--------------|-----------------|--------------------|
| **BESS Decision**         | Buffer BESS         | 50-100 kW    | 50-100 kWh      | $30,000-$60,000    |
| **GPU-Generator Stability** | Grid-Forming BESS   | 400-600 kW   | 100-200 kWh     | $350,000-$500,000 |

**Critical Question:** Can a Buffer BESS (50-100 kW) provide grid-forming capability, or is a Grid-Forming BESS (400-600 kW) required?

---

## Research Prompt

See: `/srv/projects/og-ai-inference-research/prompts/research/BESS-RECONCILIATION-RESEARCH-PROMPT.md`

The research prompt outlines:
- Core research questions (grid-forming capability, power rating logic, cost differences, synthetic inertia)
- Specific research tasks (vendor products, technical standards, case studies, cost validation)
- Expected deliverables (unified recommendation, decision framework)

---

## How This Informs Other Work

### Multi-Step Ramp Simulator
- **BESS Energy Requirements:** The simulator calculates BESS energy needed during CG260 ramp sequences. The reconciled BESS sizing will validate/update these calculations.
- **Power Rating:** Current simulator assumes BESS can handle peak deficit (688 kW for CG260-16). Need to verify if smaller BESS (50-100 kW) can provide sufficient transient buffering.

### Generator Risk Calculator
- **BESS Integration:** Once reconciled, BESS sizing logic can be integrated into the risk calculator to show BESS requirements alongside generator risk levels.

### Future BESS Sizing Calculator
- **Primary Input:** This reconciliation will directly inform the BESS sizing calculator (Phase 3 goal).

---

## Expected Reports

Add research reports here as they are completed:

- [ ] Vendor product research (BYD, Sungrow, Fluence, Tesla, etc.)
- [ ] Technical standards analysis (IEEE 1547-2018, UL 1741-SA)
- [ ] Case studies (small grid-forming BESS deployments)
- [ ] Cost breakdown analysis (inverter vs battery vs installation)
- [ ] Synthetic inertia sizing formulas
- [ ] Unified recommendation document
- [ ] Decision framework (when to use Buffer vs Grid-Forming BESS)

---

## File Naming Convention

Use descriptive names:
- `vendor-research-<vendor-name>.md`
- `standards-analysis-<standard>.md`
- `case-study-<project-name>.md`
- `cost-analysis-<source>.md`
- `unified-recommendation.md`
- `decision-framework.md`

---

## References

- **Research Prompt:** `prompts/research/BESS-RECONCILIATION-RESEARCH-PROMPT.md`
- **BESS Decision Analysis:** `research/bess-decision-analysis/`
- **GPU-Generator Stability:** `research/gpu-generator-stability/`
- **Multi-Step Ramp Simulator:** `models/multistep-ramp-simulator/`

---

**Last Updated:** 2025-12-01

