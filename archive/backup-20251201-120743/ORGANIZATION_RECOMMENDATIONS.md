# ORGANIZATION RECOMMENDATIONS
**Off-Grid AI Inference Research Project**

**Generated:** 2025-12-01
**Purpose:** Optimize file structure before deep consolidation work

---

## CURRENT STRUCTURE ANALYSIS

### What You Have Now
```
og-ai-inference-research/
├── GAP_ANALYSIS.md                    # Gap analysis (root)
├── PRD.md                             # Product Requirements (root)
├── GeneratorRisk_Calculator.csv       # Working calculator (root)
├── data/
│   └── genset-libraries/
│       ├── CAT/
│       │   └── Caterpillar_Gas_Genset_Library_Phase1.md
│       └── Natural Gas Generator Data Library.md
└── research/
    ├── Inference-economics-from-first-principles.md
    ├── LLM Inference Economics from First Principles.pdf
    ├── Off-Grid Compute – Open Modeling Challenges.md
    └── h100-economics-research/
        ├── Economics of H100 PCIe vs H100 SXM....md
        ├── PCIe vs. SXM H100 for Inference....docx
        └── strategic-infra-analyses-for-h100-deployment-economics.md
```

### Issues with Current Structure
1. **Mixed content levels** - PRD and GAP_ANALYSIS at root alongside data
2. **Inconsistent naming** - Some files have spaces, some use hyphens
3. **Flat genset-libraries** - Natural Gas Generator Data Library not in CAT folder
4. **No outputs folder** - Calculator and future deliverables mixed with source
5. **No docs folder** - Project management docs at root level
6. **PDF and DOCX mixed with MD** - Different formats not separated

---

## RECOMMENDED STRUCTURE

```
og-ai-inference-research/
│
├── README.md                          # Project overview & navigation
├── STATUS.md                          # Current progress tracker
│
├── docs/                              # Project management & planning
│   ├── PRD.md                         # Product Requirements Document
│   ├── GAP_ANALYSIS.md                # Gap analysis
│   ├── GLOSSARY.md                    # Standardized terminology
│   ├── ROADMAP.md                     # Phase planning
│   └── CHANGELOG.md                   # Document version history
│
├── research/                          # Source research documents
│   ├── gpu-compute/
│   │   ├── Off-Grid-Compute-Modeling-Challenges.md
│   │   └── gpu-power-dynamics/
│   │       └── (future: per-phase power profiles)
│   │
│   ├── inference-economics/
│   │   ├── Inference-Economics-First-Principles.md
│   │   ├── LLM-Inference-Economics-First-Principles.pdf
│   │   └── h100-deployment-economics/
│   │       ├── H100-PCIe-vs-SXM-Economics-Q4-2025.md
│   │       ├── H100-PCIe-vs-SXM-Pricing-Q4-2025.docx
│   │       └── Strategic-Infrastructure-Analysis-H100.md
│   │
│   └── external-refs/                 # External papers, whitepapers
│       └── (future: ISO standards, OEM whitepapers)
│
├── data/                              # Structured technical data
│   ├── generators/
│   │   ├── caterpillar/
│   │   │   ├── CG-Series-Library.md
│   │   │   ├── G3500-Series-Library.md
│   │   │   ├── G3600-Series-Library.md
│   │   │   └── Caterpillar-Complete-Technical-Analysis.md
│   │   │
│   │   ├── mtu/                       # (future: Phase 2)
│   │   ├── cummins/                   # (future: Phase 2)
│   │   ├── jenbacher/                 # (future: Phase 2)
│   │   └── consolidated-generator-library.json
│   │
│   ├── gpu-profiles/
│   │   ├── nvidia-h100.json
│   │   ├── nvidia-h200.json
│   │   └── gpu-power-phases.md
│   │
│   └── reference-tables/
│       ├── iso-8528-performance-classes.md
│       ├── fuel-specifications.md
│       └── industry-standards.md
│
├── models/                            # Calculators & simulation tools
│   ├── generator-risk-calculator/
│   │   ├── GeneratorRisk_v1.csv
│   │   ├── README.md                  # How to use calculator
│   │   ├── formulas.md                # Formula documentation
│   │   └── test-scenarios/
│   │       ├── scenarios.csv
│   │       └── validation-results.md
│   │
│   ├── bess-sizing/                   # (future)
│   │   └── bess-calculator.csv
│   │
│   ├── data-logistics/                # (future)
│   │   └── connectivity-cost-model.csv
│   │
│   └── integrated-model/              # (future: Phase 3)
│       └── complete-ogai-calculator.xlsx
│
├── outputs/                           # Generated deliverables
│   ├── reports/
│   │   ├── Phase-1-Consolidated-Report.md
│   │   ├── Executive-Summary.md
│   │   └── Technical-Deep-Dive.md
│   │
│   ├── presentations/
│   │   └── (future: stakeholder decks)
│   │
│   └── exports/
│       ├── generator-library-export.csv
│       ├── gpu-generator-compatibility-matrix.csv
│       └── risk-scenarios-export.json
│
├── scripts/                           # Automation & data processing
│   ├── parse-generator-specs.py
│   ├── generate-compatibility-matrix.py
│   ├── export-to-json.py
│   └── README.md
│
└── archive/                           # Old versions & superseded docs
    └── original-uploads/
        ├── OG Compute Modeling PRD (1).md
        ├── Caterpillar_Gas_Genset_Library_Phase1 (1).md
        └── Natural Gas Generator Data Library (4).md
```

---

## KEY ORGANIZATIONAL PRINCIPLES

### 1. **Separation of Concerns**
- **`research/`** = Input materials (as-received, minimal editing)
- **`data/`** = Structured, normalized technical data
- **`models/`** = Working calculators and tools
- **`outputs/`** = Generated deliverables for stakeholders
- **`docs/`** = Project management and planning

### 2. **Consistent Naming Convention**
- **Use kebab-case** for files: `generator-risk-calculator.csv`
- **No spaces** in filenames (causes shell issues)
- **Descriptive names**: `H100-PCIe-vs-SXM-Economics-Q4-2025.md` not `Economics of H100...md`
- **Version suffixes**: `GeneratorRisk_v1.csv`, `GeneratorRisk_v2.csv`

### 3. **Format Segregation**
- **Working files**: `.md`, `.csv`, `.json` in main folders
- **Reference PDFs/DOCX**: Keep in `research/` for archive
- **Generated exports**: `.xlsx`, `.pdf` in `outputs/`

### 4. **Manufacturer-Specific Organization**
```
data/generators/
├── caterpillar/         # All CAT data together
├── mtu/                 # Future: MTU data
└── cummins/             # Future: Cummins data
```
Not:
```
data/genset-libraries/
├── CAT/
└── Natural Gas Generator Data Library.md  # Which manufacturer?
```

### 5. **Versioning Strategy**
- Keep **original uploads** in `archive/original-uploads/`
- **Working versions** in main folders with version suffixes
- Track changes in `docs/CHANGELOG.md`

---

## SPECIFIC REORGANIZATION STEPS

### Step 1: Create New Directory Structure
```bash
mkdir -p docs
mkdir -p research/{gpu-compute,inference-economics,external-refs}
mkdir -p data/{generators/{caterpillar,mtu,cummins,jenbacher},gpu-profiles,reference-tables}
mkdir -p models/{generator-risk-calculator/test-scenarios,bess-sizing,data-logistics}
mkdir -p outputs/{reports,presentations,exports}
mkdir -p scripts
mkdir -p archive/original-uploads
```

### Step 2: Move & Rename Files

**Project Docs:**
```bash
mv GAP_ANALYSIS.md docs/
mv PRD.md docs/
```

**Research Files:**
```bash
mv research/Off-Grid\ Compute\ –\ Open\ Modeling\ Challenges.md \
   research/gpu-compute/Off-Grid-Compute-Modeling-Challenges.md

mv research/Inference-economics-from-first-principles.md \
   research/inference-economics/Inference-Economics-First-Principles.md

mv research/LLM\ Inference\ Economics\ from\ First\ Principles.pdf \
   research/inference-economics/

mv research/h100-economics-research \
   research/inference-economics/h100-deployment-economics
```

**Generator Data:**
```bash
mv data/genset-libraries/CAT/Caterpillar_Gas_Genset_Library_Phase1.md \
   data/generators/caterpillar/Caterpillar-Phase1-Library.md

mv data/genset-libraries/Natural\ Gas\ Generator\ Data\ Library.md \
   data/generators/caterpillar/Caterpillar-Technical-Analysis.md
```

**Calculator:**
```bash
mv GeneratorRisk_Calculator\ -\ GeneratorRiskData\ .csv \
   models/generator-risk-calculator/GeneratorRisk_v1.csv
```

**Archive Originals:**
```bash
# Keep copies of as-received files
cp -r data/genset-libraries/* archive/original-uploads/
```

### Step 3: Create Key Documentation Files

**README.md** (project overview)
**STATUS.md** (current progress)
**docs/GLOSSARY.md** (terminology)
**docs/ROADMAP.md** (phase planning)
**models/generator-risk-calculator/README.md** (calculator usage)

---

## FILE NAMING STANDARDS

### DO:
```
✓ generator-risk-calculator.csv
✓ H100-PCIe-vs-SXM-Economics.md
✓ Caterpillar-CG260-Specs.json
✓ gpu-power-phases-v2.md
✓ Phase-1-Consolidated-Report.md
```

### DON'T:
```
✗ Generator Risk Calculator - Data.csv      (spaces)
✗ Economics of H100 PCIe vs....md          (too long, spaces)
✗ Caterpillar_Gas_Genset_Library_Phase1 (1).md  (mixed case, dup marker)
✗ data.csv                                  (too vague)
✗ report.md                                 (too generic)
```

### Naming Pattern:
```
[Category]-[Specific-Item]-[Detail]-[Version].[ext]

Examples:
- Generator-Risk-Calculator-v1.csv
- Caterpillar-G3520-Specs.json
- GPU-Power-Phases-H100-v2.md
- Consolidated-Report-Phase1.md
```

---

## METADATA & DOCUMENTATION

### Every Major File Should Have:
1. **Header block** with:
   - Title
   - Generated/Updated date
   - Author/Source
   - Version
   - Purpose/Scope

2. **Status indicator**:
   - Draft / In Progress / Review / Final

3. **Dependencies**:
   - Which other files does it reference?
   - Which files depend on it?

### Example Header:
```markdown
# GENERATOR RISK CALCULATOR - USER GUIDE

**Version:** 1.0
**Last Updated:** 2025-12-01
**Status:** Draft
**Author:** [Your Team]
**Dependencies:**
- data/generators/caterpillar/Caterpillar-Phase1-Library.md
- docs/PRD.md (Section 4.1)

**Purpose:** Calculate GPU cluster ramp rates and assess generator compatibility
```

---

## RECOMMENDED NEW FILES TO CREATE

### 1. **README.md** (Root)
```markdown
# Off-Grid AI Inference Research

## Overview
Technical and economic modeling for GPU compute powered by off-grid
natural gas generation.

## Project Structure
- `docs/` - Project management & planning
- `research/` - Source research materials
- `data/` - Structured technical specifications
- `models/` - Calculators and simulation tools
- `outputs/` - Generated reports and deliverables

## Quick Start
1. Read: docs/PRD.md
2. Review: docs/GAP_ANALYSIS.md
3. Use: models/generator-risk-calculator/

## Current Status
See: STATUS.md
```

### 2. **STATUS.md**
```markdown
# PROJECT STATUS

**Last Updated:** 2025-12-01

## Current Phase: Phase 1 - Foundation

### Completed ✓
- Generator library (Caterpillar, 11 variants)
- Basic calculator (v1) with 4 scenarios
- Gap analysis

### In Progress 🔄
- File reorganization
- Terminology standardization
- GPU power profile research

### Planned 📋
- Multi-step ramp simulator
- BESS sizing calculator
- Phase 2 generator expansion (MTU, Cummins)

## Blockers
- Awaiting Caterpillar dynamic parameters (H, R, load curves)
- Need NVIDIA H100 power phase data
```

### 3. **docs/GLOSSARY.md**
```markdown
# TERMINOLOGY GLOSSARY

## Generator Terms
- **Ramp Rate (kW/s):** Rate of power change
- **Correlation (C):** Fraction of GPUs transitioning together (0-1)
- **H_eff (s):** Effective inertia constant
- **R_eff (p.u.):** Governor droop setting
...
```

### 4. **docs/ROADMAP.md**
```markdown
# PROJECT ROADMAP

## Phase 1: Foundation (Current)
- [x] Caterpillar generator library
- [x] Basic calculator
- [ ] File reorganization
- [ ] GPU power profiles

## Phase 2: Expansion (Weeks 5-8)
- [ ] MTU, Cummins, Jenbacher libraries
- [ ] Multi-step ramp simulator
- [ ] BESS sizing

## Phase 3: Integration (Weeks 9-12)
- [ ] Complete economic model
- [ ] Web calculator interface
- [ ] Pilot validation
```

### 5. **models/generator-risk-calculator/README.md**
```markdown
# GENERATOR RISK CALCULATOR

## Purpose
Calculate GPU cluster ramp rates and assess generator compatibility.

## Usage
1. Open: GeneratorRisk_v1.csv
2. Edit yellow input cells (N_GPUs, DeltaP_GPU, etc.)
3. Review calculated outputs (green cells)
4. Check RiskLevel: GREEN/YELLOW/RED

## Formulas
See: formulas.md

## Test Scenarios
See: test-scenarios/scenarios.csv
```

---

## BENEFITS OF THIS ORGANIZATION

### For You:
1. **Easy to find things** - Logical categorization
2. **Easy to collaborate** - Clear file ownership
3. **Easy to version** - Originals preserved in archive
4. **Easy to deliver** - Outputs folder ready for stakeholders

### For Future Work:
1. **Scalable** - Easy to add Phase 2 manufacturers
2. **Modular** - Calculators independent
3. **Maintainable** - Clear documentation trail
4. **Professional** - Looks like a real research project

---

## MIGRATION SCRIPT

Would you like me to create a bash script to automatically:
1. Create the directory structure
2. Move and rename files
3. Create stub documentation files
4. Update cross-references

This would take ~5 minutes to run and give you a clean slate.

---

## RECOMMENDATIONS PRIORITY

### CRITICAL (Do Before Hard Work):
1. ✅ Move files to logical folders
2. ✅ Rename files to consistent convention
3. ✅ Create README.md and STATUS.md
4. ✅ Create docs/GLOSSARY.md

### HIGH (Do Soon):
5. Split large files by manufacturer (CAT → CG/G3500/G3600)
6. Create calculator documentation
7. Add headers to all major files

### MEDIUM (Do Eventually):
8. Create exports/templates
9. Set up scripts/ folder
10. Archive old versions

---

## NEXT STEPS

Would you like me to:

**Option A:** Create a bash script to automatically reorganize everything?

**Option B:** Do it manually, step-by-step with your review?

**Option C:** Just create the new folders and key docs, leave files for now?

**Option D:** Something else?

Let me know and I'll proceed!
