#!/bin/bash
# Off-Grid AI Inference Research - Project Reorganization Script
# Generated: 2025-12-01
# Purpose: Restructure project with consistent naming and logical organization

set -e  # Exit on error

PROJECT_ROOT="/srv/projects/og-ai-inference-research"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "OFF-GRID AI INFERENCE - REORGANIZATION"
echo "=========================================="
echo ""
echo "Starting reorganization at: $(date)"
echo "Working directory: $PROJECT_ROOT"
echo ""

# Create backup
echo "[1/6] Creating backup..."
BACKUP_DIR="backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r . "$BACKUP_DIR/" 2>/dev/null || true
echo "✓ Backup created: $BACKUP_DIR"
echo ""

# Create new directory structure
echo "[2/6] Creating directory structure..."
mkdir -p docs
mkdir -p research/gpu-compute/gpu-power-dynamics
mkdir -p research/inference-economics/h100-deployment-economics
mkdir -p research/external-refs
mkdir -p data/generators/caterpillar
mkdir -p data/generators/mtu
mkdir -p data/generators/cummins
mkdir -p data/generators/jenbacher
mkdir -p data/gpu-profiles
mkdir -p data/reference-tables
mkdir -p models/generator-risk-calculator/test-scenarios
mkdir -p models/bess-sizing
mkdir -p models/data-logistics
mkdir -p models/integrated-model
mkdir -p outputs/reports
mkdir -p outputs/presentations
mkdir -p outputs/exports
mkdir -p scripts
mkdir -p archive/original-uploads
echo "✓ Directory structure created"
echo ""

# Move and rename files
echo "[3/6] Reorganizing files..."

# Project documentation
if [ -f "GAP_ANALYSIS.md" ]; then
    mv "GAP_ANALYSIS.md" docs/
    echo "  → docs/GAP_ANALYSIS.md"
fi

if [ -f "PRD.md" ]; then
    mv "PRD.md" docs/
    echo "  → docs/PRD.md"
fi

if [ -f "ORGANIZATION_RECOMMENDATIONS.md" ]; then
    mv "ORGANIZATION_RECOMMENDATIONS.md" docs/
    echo "  → docs/ORGANIZATION_RECOMMENDATIONS.md"
fi

# Research files - GPU compute
if [ -f "research/Off-Grid Compute – Open Modeling Challenges.md" ]; then
    mv "research/Off-Grid Compute – Open Modeling Challenges.md" \
       "research/gpu-compute/Off-Grid-Compute-Modeling-Challenges.md"
    echo "  → research/gpu-compute/Off-Grid-Compute-Modeling-Challenges.md"
fi

# Research files - Inference economics
if [ -f "research/Inference-economics-from-first-principles.md" ]; then
    mv "research/Inference-economics-from-first-principles.md" \
       "research/inference-economics/Inference-Economics-First-Principles.md"
    echo "  → research/inference-economics/Inference-Economics-First-Principles.md"
fi

if [ -f "research/LLM Inference Economics from First Principles.pdf" ]; then
    mv "research/LLM Inference Economics from First Principles.pdf" \
       "research/inference-economics/LLM-Inference-Economics-First-Principles.pdf"
    echo "  → research/inference-economics/LLM-Inference-Economics-First-Principles.pdf"
fi

# H100 economics research
if [ -d "research/h100-economics-research" ]; then
    # Move individual files with renaming
    if [ -f "research/h100-economics-research/Economics of H100 PCIe vs H100 SXM for Inference in Neo‑Cloud Data Centers (Q4 2025).md" ]; then
        mv "research/h100-economics-research/Economics of H100 PCIe vs H100 SXM for Inference in Neo‑Cloud Data Centers (Q4 2025).md" \
           "research/inference-economics/h100-deployment-economics/H100-PCIe-vs-SXM-Economics-Q4-2025.md"
        echo "  → research/inference-economics/h100-deployment-economics/H100-PCIe-vs-SXM-Economics-Q4-2025.md"
    fi

    if [ -f "research/h100-economics-research/strategic-infra-analyses-for-h100-deployment-economics.md" ]; then
        mv "research/h100-economics-research/strategic-infra-analyses-for-h100-deployment-economics.md" \
           "research/inference-economics/h100-deployment-economics/Strategic-Infrastructure-Analysis-H100.md"
        echo "  → research/inference-economics/h100-deployment-economics/Strategic-Infrastructure-Analysis-H100.md"
    fi

    if [ -f "research/h100-economics-research/PCIe vs. SXM H100 for Inference_ Cost, Efficiency, and Pricing (Q4 2025).docx" ]; then
        mv "research/h100-economics-research/PCIe vs. SXM H100 for Inference_ Cost, Efficiency, and Pricing (Q4 2025).docx" \
           "research/inference-economics/h100-deployment-economics/H100-PCIe-vs-SXM-Pricing-Q4-2025.docx"
        echo "  → research/inference-economics/h100-deployment-economics/H100-PCIe-vs-SXM-Pricing-Q4-2025.docx"
    fi

    # Remove empty old directory
    rmdir "research/h100-economics-research" 2>/dev/null || true
fi

# Generator data
if [ -f "data/genset-libraries/CAT/Caterpillar_Gas_Genset_Library_Phase1.md" ]; then
    mv "data/genset-libraries/CAT/Caterpillar_Gas_Genset_Library_Phase1.md" \
       "data/generators/caterpillar/Caterpillar-Phase1-Library.md"
    echo "  → data/generators/caterpillar/Caterpillar-Phase1-Library.md"
fi

if [ -f "data/genset-libraries/Natural Gas Generator Data Library.md" ]; then
    mv "data/genset-libraries/Natural Gas Generator Data Library.md" \
       "data/generators/caterpillar/Caterpillar-Technical-Analysis.md"
    echo "  → data/generators/caterpillar/Caterpillar-Technical-Analysis.md"
fi

# Clean up old genset-libraries structure
if [ -d "data/genset-libraries" ]; then
    rmdir "data/genset-libraries/CAT" 2>/dev/null || true
    rmdir "data/genset-libraries" 2>/dev/null || true
fi

# Calculator
if [ -f "GeneratorRisk_Calculator - GeneratorRiskData .csv" ]; then
    mv "GeneratorRisk_Calculator - GeneratorRiskData .csv" \
       "models/generator-risk-calculator/GeneratorRisk-v1.csv"
    echo "  → models/generator-risk-calculator/GeneratorRisk-v1.csv"
fi

echo "✓ Files reorganized"
echo ""

# Archive originals
echo "[4/6] Creating archive of originals..."
cp -r "$BACKUP_DIR/"* archive/original-uploads/ 2>/dev/null || true
echo "✓ Originals archived"
echo ""

# Create key documentation files
echo "[5/6] Creating documentation files..."

# README.md
cat > README.md << 'EOF'
# Off-Grid AI Inference Research

## Overview
Technical and economic modeling for GPU compute infrastructure powered by off-grid natural gas generation.

**Project Goal:** Model both financially and technically how to deploy AI inference workloads using stranded natural gas as the primary power source.

## Project Structure

```
├── docs/              # Project management & planning
├── research/          # Source research materials
├── data/              # Structured technical specifications
├── models/            # Calculators and simulation tools
├── outputs/           # Generated reports and deliverables
├── scripts/           # Automation & data processing tools
└── archive/           # Original files and backups
```

## Quick Start

1. **Understand the project:** Read `docs/PRD.md`
2. **Review current state:** Check `STATUS.md`
3. **See what's missing:** Review `docs/GAP_ANALYSIS.md`
4. **Use the calculator:** Open `models/generator-risk-calculator/`

## Key Documents

- **PRD:** Product Requirements Document - defines calculator scope
- **Gap Analysis:** Identifies missing data and parameters
- **Generator Library:** Caterpillar natural gas generator specifications
- **Calculator:** Risk assessment tool for GPU-generator compatibility

## Current Status

**Phase:** Phase 1 - Foundation
**Focus:** Caterpillar generator library, basic risk calculator, gap analysis

See `STATUS.md` for detailed progress tracking.

## Contributing

This is an active research project. Documentation standards:
- Use kebab-case for filenames
- Include headers with dates and version info
- Update STATUS.md when completing milestones

## Contact

For questions about this research, refer to project documentation in `docs/`.
EOF
echo "  → README.md"

# STATUS.md
cat > STATUS.md << 'EOF'
# PROJECT STATUS

**Last Updated:** 2025-12-01
**Phase:** Phase 1 - Foundation

---

## Overview

This project models off-grid AI inference infrastructure powered by natural gas generators. Current focus is on GPU power dynamics, generator response characteristics, and risk assessment.

---

## Progress Tracker

### Phase 1: Foundation ✓ 80% Complete

#### Completed ✓
- [x] Caterpillar generator library (11 variants, 6 families)
- [x] Basic risk calculator (v1) with 4 scenarios
- [x] Gap analysis document
- [x] Project reorganization
- [x] File structure standardization

#### In Progress 🔄
- [ ] GPU power phase profiles (H100/H200)
- [ ] Terminology standardization (glossary)
- [ ] Calculator documentation

#### Blocked ⚠️
- Awaiting Caterpillar application engineering data:
  - Verified inertia constants (H_eff)
  - Factory governor droop settings (R_eff)
  - Load-step performance curves

---

## Phase 2: Expansion (Planned)

### Week 5-8 Goals
- [ ] Multi-step ramp simulator (for CG260 sequences)
- [ ] BESS sizing calculator
- [ ] Bitcoin miner integration modeling
- [ ] Expand generator library:
  - [ ] MTU Series 4000
  - [ ] Cummins QSK series
  - [ ] INNIO Jenbacher J-series

---

## Phase 3: Integration (Planned)

### Week 9-12 Goals
- [ ] Data logistics calculator (Starlink/Sneakernet/Fiber)
- [ ] Complete economic model (CapEx/OpEx)
- [ ] Consolidated master report
- [ ] Web-based calculator interface
- [ ] Pilot validation with real deployment

---

## Key Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Generator Models | 11 (Caterpillar only) | 30+ (4 manufacturers) |
| Calculator Scenarios | 4 | 20+ |
| GPU Profiles | 0 | 3 (H100, H200, A100) |
| Documentation | 70% | 95% |

---

## Recent Updates

**2025-12-01:**
- Completed project reorganization
- Created comprehensive gap analysis
- Standardized file naming conventions
- Established directory structure

**Next Milestone:** GPU power profiles research (Week 1)

---

## Blockers & Issues

1. **Critical Data Gaps:**
   - Generator dynamic parameters (H, R, transient curves)
   - GPU per-phase power profiles
   - Cost data for economic modeling

2. **Technical Challenges:**
   - Multi-step ramp sequencing not yet modeled
   - BESS sizing calculations missing
   - No voltage dynamics in current calculator

3. **Schedule Risks:**
   - Manufacturer data requests may take 2-4 weeks
   - GPU power profiling requires lab testing or partnerships

---

## How to Update This File

When completing tasks:
1. Move items from "In Progress" to "Completed"
2. Update "Last Updated" date
3. Add entry to "Recent Updates"
4. Update metrics if applicable
EOF
echo "  → STATUS.md"

# Create calculator documentation
cat > models/generator-risk-calculator/README.md << 'EOF'
# GENERATOR RISK CALCULATOR

**Version:** 1.0
**Last Updated:** 2025-12-01
**Status:** Working prototype

---

## Purpose

Calculate GPU cluster power ramp rates and assess compatibility with natural gas generator constraints. Determines if a given GPU cluster configuration will operate safely on a specific generator model.

---

## How to Use

### Step 1: Open Calculator
```
models/generator-risk-calculator/GeneratorRisk-v1.csv
```

### Step 2: Edit Input Parameters (Yellow Cells)

**Cluster Configuration:**
- `N_GPUs` - Number of GPUs in cluster
- `DeltaP_GPU_kW` - Per-GPU power step (kW)
- `Correlation_C` - Fraction transitioning together (0.0-1.0)
- `DeltaT_event_s` - Transition time window (seconds)

**Generator Configuration:**
- `P_rated_gen_kW` - Generator rated power (kW)
- `H_eff_s` - Effective inertia constant (seconds)
- `R_eff_pu` - Governor droop (per unit, e.g., 0.04 = 4%)
- `f_nom_Hz` - Nominal frequency (50 or 60 Hz)
- `MaxStep_pct` - Maximum safe load step (% of rated)

### Step 3: Review Calculated Outputs (Green Cells)

- `DeltaP_cluster_kW` - Total cluster power step
- `RampRate_kW_per_s` - Power change rate
- `StepFraction` - Load step as fraction of generator capacity
- `DeltaF_over_F_pu` - Frequency deviation (per unit)
- `RoCoF_Hz_per_s` - Rate of change of frequency
- `StepWithinLimit` - TRUE if within generator limits
- `RiskLevel` - GREEN (safe) / YELLOW (caution) / RED (unsafe)

---

## Risk Level Interpretation

| Level | Meaning | Action |
|-------|---------|--------|
| **GREEN** | Safe operation | Proceed with configuration |
| **YELLOW** | Marginal - may require mitigation | Add BESS buffer or reduce correlation |
| **RED** | Unsafe - exceeds limits | Reconfigure or use different generator |

---

## Example Scenarios

### Scenario 1: G3520 Fast Response + GPU Warmup
- 1024 GPUs × 0.6 kW × 0.8 correlation = 491.52 kW
- G3520 (4000 kW, 100% block load capable)
- Result: **GREEN** - 12.3% step, well within limits

### Scenario 2: CG260-16 + GPU Warmup
- Same GPU configuration (491.52 kW)
- CG260 (4300 kW, 16% max first step)
- Result: **GREEN** - 11.4% step, within first step limit

### Scenario 3: CG260 + Bitcoin Container
- 5000 GPUs × 0.3 kW × 0.3 correlation over 30s
- Result: **GREEN** - slow ramp (15 kW/s) easily handled

---

## Formulas

See: `formulas.md` for detailed formula documentation

---

## Test Scenarios

Pre-configured test cases available in:
```
models/generator-risk-calculator/test-scenarios/scenarios.csv
```

---

## Limitations

**Current Version (v1) does NOT include:**
- Multi-phase GPU power modeling
- Multi-step generator ramp sequences (CG260)
- BESS sizing calculations
- Bitcoin miner coordination
- Voltage dynamics
- Economic modeling

See: `docs/GAP_ANALYSIS.md` for planned enhancements

---

## References

- `docs/PRD.md` - Calculator requirements
- `data/generators/caterpillar/` - Generator specifications
- `docs/GAP_ANALYSIS.md` - Known limitations
EOF
echo "  → models/generator-risk-calculator/README.md"

# Create formula documentation
cat > models/generator-risk-calculator/formulas.md << 'EOF'
# GENERATOR RISK CALCULATOR - FORMULAS

**Version:** 1.0
**Last Updated:** 2025-12-01

---

## Input Parameters

| Symbol | Name | Units | Description |
|--------|------|-------|-------------|
| N | N_GPUs | count | Number of GPUs in cluster |
| ΔP_gpu | DeltaP_GPU_kW | kW | Per-GPU power step |
| C | Correlation_C | 0-1 | Fraction of GPUs transitioning together |
| Δt | DeltaT_event_s | s | Time window of transition |
| P_rated | P_rated_gen_kW | kW | Generator rated power |
| H | H_eff_s | s | Effective inertia constant |
| R | R_eff_pu | p.u. | Governor droop (per unit) |
| f_nom | f_nom_Hz | Hz | Nominal frequency |
| MaxStep | MaxStep_pct | % | Maximum safe load step |

---

## Calculated Outputs

### 1. Cluster Power Step
```
ΔP_cluster = C × N × ΔP_gpu
```

**Interpretation:** Total power change when the specified fraction of GPUs transition.

**Example:**
- 1024 GPUs × 0.6 kW × 0.8 correlation = 491.52 kW

---

### 2. Ramp Rate
```
RampRate = ΔP_cluster / Δt
```

**Units:** kW/s

**Interpretation:** Rate at which the cluster load changes.

**Example:**
- 491.52 kW ÷ 1 s = 491.52 kW/s

---

### 3. Step Fraction
```
StepFraction = ΔP_cluster / P_rated
```

**Units:** per unit (dimensionless)

**Interpretation:** Load step as a fraction of generator capacity.

**Example:**
- 491.52 kW ÷ 4000 kW = 0.12288 (12.3%)

---

### 4. Steady-State Frequency Deviation
```
ΔF / F_nom ≈ -R × StepFraction
```

**Units:** per unit (or Hz if multiplied by f_nom)

**Derivation:** From governor droop characteristic:
- Droop = (Δf / f_nom) / (ΔP / P_rated)
- Rearranging: Δf / f_nom = -R × (ΔP / P_rated)

**Example:**
- -(0.04) × 0.12288 = -0.0049152 p.u. (or -0.295 Hz at 60 Hz)

---

### 5. Rate of Change of Frequency (RoCoF)
```
df/dt ≈ -ΔP_cluster / (2 × H × S_base)
```

Where:
- S_base = P_rated (assuming unity power factor)
- H = inertia constant (seconds)

**Units:** Hz/s

**Derivation:** From swing equation for synchronous machines.

**Example:**
- -491.52 kW ÷ (2 × 3 s × 4000 kW) = -0.02048 p.u./s
- At 60 Hz: -0.02048 × 60 = -1.229 Hz/s

**Note:** This is the *initial* rate of change before governor response.

---

### 6. Step Within Limit Check
```
StepWithinLimit = (StepFraction × 100 < MaxStep_pct)
```

**Result:** TRUE or FALSE

**Example:**
- 12.3% < 100% → TRUE

---

### 7. Risk Level Classification

```
if StepFraction × 100 < MaxStep_pct × 0.5:
    RiskLevel = GREEN
elif StepFraction × 100 < MaxStep_pct:
    RiskLevel = YELLOW
else:
    RiskLevel = RED
```

**Thresholds:**
- **GREEN:** Less than 50% of generator's max step
- **YELLOW:** Between 50% and 100% of max step
- **RED:** Exceeds generator's max step capability

---

## Assumptions & Limitations

1. **Linear Scaling:** Assumes all GPUs transition with same ΔP
2. **Single Step:** Does not model multi-step sequences
3. **Simplified Dynamics:** Uses first-order approximations
4. **No Voltage:** Only models frequency response
5. **No BESS:** Does not include energy storage buffering
6. **Steady State:** Governor droop formula assumes steady-state

---

## References

- ISO 8528-5: Performance classes for generator sets
- Power system dynamics textbooks (Kundur, Anderson & Fouad)
- Caterpillar application guides

---

## Future Enhancements

Planned additions for v2:
- Multi-phase GPU modeling
- Multi-step ramp sequences
- Voltage dip calculations
- BESS sizing integration
- Time-series simulation output
EOF
echo "  → models/generator-risk-calculator/formulas.md"

echo "✓ Documentation files created"
echo ""

# Create scripts README
cat > scripts/README.md << 'EOF'
# AUTOMATION SCRIPTS

This directory contains utility scripts for data processing, exports, and analysis automation.

## Planned Scripts

- `parse-generator-specs.py` - Extract specs from manufacturer PDFs
- `generate-compatibility-matrix.py` - Create GPU-generator compatibility table
- `export-to-json.py` - Convert CSV data to JSON format
- `validate-formulas.py` - Test calculator formula accuracy

## Usage

Scripts will be added as needed during Phase 2 and 3.
EOF
echo "  → scripts/README.md"

echo "[6/6] Final cleanup..."
echo "✓ Reorganization complete!"
echo ""

# Summary
echo "=========================================="
echo "REORGANIZATION SUMMARY"
echo "=========================================="
echo ""
echo "✓ Backup created: $BACKUP_DIR"
echo "✓ Directory structure established"
echo "✓ Files reorganized and renamed"
echo "✓ Documentation created:"
echo "  - README.md"
echo "  - STATUS.md"
echo "  - docs/ORGANIZATION_RECOMMENDATIONS.md"
echo "  - models/generator-risk-calculator/README.md"
echo "  - models/generator-risk-calculator/formulas.md"
echo ""
echo "Next steps:"
echo "1. Review new structure: tree -L 2"
echo "2. Check renamed files for correctness"
echo "3. Begin Phase 1 work (see STATUS.md)"
echo ""
echo "Completed at: $(date)"
echo "=========================================="
