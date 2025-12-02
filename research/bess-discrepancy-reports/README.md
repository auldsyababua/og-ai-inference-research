# BESS Discrepancy Reports

**Purpose:** This folder contains research reports and analysis documents related to resolving the BESS sizing discrepancy between the Buffer BESS (50-100 kW) and Grid-Forming BESS (400-600 kW) recommendations.

---

## Background

Four comprehensive research reports analyzed the BESS sizing discrepancy for the same deployment scenario (1 MW generator + 0.5 MW GPU):

| Report                    | BESS Recommendation | Power Rating | Energy Capacity | Cost Estimate      |
|---------------------------|---------------------|--------------|-----------------|--------------------|
| **BESS Decision**         | Buffer BESS         | 50-100 kW    | 50-100 kWh      | $30,000-$60,000    |
| **GPU-Generator Stability** | Grid-Forming BESS   | 400-600 kW   | 100-200 kWh     | $350,000-$500,000 |

**Critical Question:** Can a Buffer BESS (50-100 kW) provide grid-forming capability, or is a Grid-Forming BESS (400-600 kW) required?

**Answer:** All four reports converge on **400-600 kW Grid-Forming BESS** as the technically required solution for natural gas generator + GPU cluster scenarios.

---

## Reports

### Individual Research Reports

1. **`report-1-compass-grid-forming-analysis.md`** (8.8K)
   - Grid-forming capability analysis
   - Vendor product research (Schneider, SMA, Victron, Dynapower)
   - Decision framework
   - Focus: Standards, commercial products, cost analysis

2. **`report-2-physics-of-stability.md`** (33K)
   - Detailed physics and control theory analysis
   - Inverter control topologies (Grid-Following vs Grid-Forming)
   - Current limiting physics
   - Focus: Technical deep-dive, control theory, physics

3. **`report-3-perplexity-comprehensive-research.md`** (584K)
   - Comprehensive Perplexity research with extensive citations
   - Vendor product analysis
   - Cost breakdown
   - Focus: Extensive research, citations, vendor analysis

4. **`report-4-direct-answers-unified-recommendation.md`** (50K)
   - Direct answers format
   - Detailed cost breakdown
   - Unified recommendation
   - Focus: Practical answers, cost analysis, decision framework

### Consolidated Analysis

- **`BESS-DISCREPANCY-CONSOLIDATED-ANALYSIS.md`** (23K)
  - Comparison matrix of all 4 reports
  - Agreement analysis
  - Unified recommendation
  - Decision framework

---

## Key Findings

**Consensus:** All four reports agree (95%+ consensus) on:

1. **Grid-forming capability:** Software/firmware control mode, no minimum power rating
2. **Natural gas generator:** 25-40% load acceptance (250-400 kW for 1 MW)
3. **GPU load steps:** 400-500 kW instantaneous (80-100% of capacity) worst-case
4. **BESS sizing formula:** P_BESS ≥ Load_Step - Gen_Acceptance
5. **Final recommendation:** 400-600 kW Grid-Forming BESS ($350-500k)
6. **50-100 kW limitations:** Only viable with diesel generator or aggressive load sequencing

**Unified Recommendation:**
- **Primary:** 400-600 kW / 100-200 kWh Grid-Forming BESS ($350-500k)
- **Alternative:** 150-200 kW Grid-Forming BESS + load sequencing ($80-120k) if budget constrained

---

## Research Prompt

See: `prompts/research/BESS-RECONCILIATION-RESEARCH-PROMPT.md`

The research prompt outlines:
- Core research questions (grid-forming capability, power rating logic, cost differences, synthetic inertia)
- Specific research tasks (vendor products, technical standards, case studies, cost validation)
- Expected deliverables (unified recommendation, decision framework)

---

## How This Informs Other Work

### Multi-Step Ramp Simulator
- **BESS Energy Requirements:** The simulator calculates BESS energy needed during CG260 ramp sequences. The reconciled BESS sizing validates/updates these calculations.
- **Power Rating:** Current simulator assumes BESS can handle peak deficit (688 kW for CG260-16). Verified that 400-600 kW BESS is appropriate for this scenario.

### Generator Risk Calculator
- **BESS Integration:** BESS sizing logic can be integrated into the risk calculator to show BESS requirements alongside generator risk levels.

### Future BESS Sizing Calculator
- **Primary Input:** This reconciliation directly informs the BESS sizing calculator (Phase 3 goal).

---

## File Naming Convention

Reports follow this naming pattern:
- `report-<number>-<descriptive-name>.md`
- `BESS-DISCREPANCY-CONSOLIDATED-ANALYSIS.md` (main analysis)

---

## References

- **Research Prompt:** `prompts/research/BESS-RECONCILIATION-RESEARCH-PROMPT.md`
- **BESS Decision Analysis:** `research/bess-decision-analysis/`
- **GPU-Generator Stability:** `research/gpu-generator-stability/`
- **Multi-Step Ramp Simulator:** `models/multistep-ramp-simulator/`

---

**Last Updated:** 2025-12-02
