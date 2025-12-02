# NVIDIA GPU Documentation Sources

**Date:** 2025-12-02  
**Status:** Documentation Collected ✅  
**Purpose:** Centralized list of NVIDIA GPU documentation sources for field deployment

---

## GPUs Planned for Field Deployment

Based on research analysis, the following GPUs are under consideration:

1. **H100 PCIe** - Primary choice for off-grid deployments (power efficiency, standard servers)
2. **H100 SXM5** - Secondary option for high-throughput workloads (requires liquid cooling)
3. **A100 PCIe** - Potential alternative/legacy option (if available at lower cost)

---

## Documentation Sources

### Primary Documentation Portals

1. **NVIDIA Developer Portal**
   - URL: `https://developer.nvidia.com`
   - Contains: CUDA Toolkit, programming guides, sample code
   - Access: Public

2. **NVIDIA Documentation Hub**
   - URL: `https://docs.nvidia.com`
   - Contains: Technical documentation, architecture guides, release notes
   - Access: Public

### GPU-Specific Documentation

#### H100 PCIe

**Technical Specifications:**
- Form Factor: Full-height, full-length (FHFL) dual-slot PCIe card
- Memory: 80 GB HBM2e
- Memory Bandwidth: 2,000 GB/s
- Power: 310W default, 350W TDP max
- PCIe: Gen5 x16 (128 GB/s)
- NVLink: 600 GB/s (with bridges)
- Cooling: Passive heat sink (requires system airflow)

**Key Documentation Needed:**
- [x] Datasheet/Technical Specifications PDF → `docs/nvidia-manuals/H100-PCIe-Product-Brief-PB-11133.pdf` ✅ COLLECTED
- [ ] User Guide/Installation Manual → Installation is OEM responsibility (not available as standalone NVIDIA doc)
- [x] Power Management Guide → `docs/nvidia-manuals/NVML-API-Reference-Guide.pdf` ✅ COLLECTED
- [ ] Thermal Design Guide → Thermal design is server manufacturer responsibility (not available as standalone NVIDIA doc)
- [ ] NVLink Configuration Guide → Covered in architecture whitepaper and DGX guides
- [x] MIG (Multi-Instance GPU) Configuration Guide → `docs/nvidia-manuals/H100-MIG-Configuration-Guide.md` ✅ COLLECTED
- [ ] Driver and Software Requirements → Available on NVIDIA Developer Portal (public)

**Search Terms:**
- "H100 PCIe datasheet"
- "H100 PCIe technical specifications"
- "H100 PCIe user guide"
- "H100 PCIe installation manual"

#### H100 SXM5 / HGX

**Technical Specifications:**
- Form Factor: SXM5 module (HGX baseboard)
- Memory: 80 GB HBM3
- Memory Bandwidth: 3,350 GB/s
- Power: Up to 700W TDP
- NVLink: 900 GB/s GPU-to-GPU
- Cooling: Integrated with HBM3 (requires liquid cooling)

**Key Documentation Needed:**
- [x] HGX H100 System Design Guide → `docs/nvidia-manuals/dgxh100-user-guide.pdf` ✅ COLLECTED (DGX H100 guide)
- [x] SXM5 Module Specifications → Covered in `docs/nvidia-manuals/NVIDIA H100 GPU Whitepaper.pdf` ✅ COLLECTED
- [x] Liquid Cooling Requirements → Covered in DGX guides ✅ COLLECTED
- [ ] NVSwitch Configuration Guide → Covered in architecture whitepaper and DGX guides
- [x] Multi-GPU Setup Guide → `docs/nvidia-manuals/dgxh100-user-guide.pdf` ✅ COLLECTED
- [x] Power and Thermal Design Guide → Covered in DGX guides and NVML API reference ✅ COLLECTED

**Search Terms:**
- "H100 SXM5 datasheet"
- "HGX H100 system guide"
- "H100 SXM5 technical specifications"
- "HGX H100 liquid cooling"

#### A100 PCIe (If Applicable)

**Key Documentation Needed:**
- [ ] A100 PCIe Datasheet
- [ ] A100 Technical Specifications
- [ ] A100 User Guide

---

## Documentation Search Status

### Completed Searches

✅ **H100 PCIe Technical Specifications** - Found via Perplexity search:
- Physical specifications (weight, form factor)
- Memory specifications (80GB HBM2e, 2TB/s bandwidth)
- Power specifications (310W default, 350W TDP max)
- PCIe interface details
- NVLink configuration
- **Source:** NVIDIA official documentation

✅ **H100 SXM5 Technical Specifications** - Found via Perplexity search:
- Performance metrics (FP8: 3,958 teraFLOPS)
- Memory architecture (80GB HBM3, 3.35TB/s)
- Interconnect (900GB/s NVLink)
- Power (700W TDP)
- HGX system configurations
- **Source:** NVIDIA official documentation

✅ **A100 Technical Specifications** - Found via Perplexity search:
- PCIe: 300W default, 80GB HBM2e, 1,935 GB/s bandwidth
- SXM: 400W max, 80GB HBM2e, 2,039 GB/s bandwidth
- NVLink: 600 GB/s
- **Source:** NVIDIA official documentation

✅ **NVIDIA Documentation Portals** - Identified:
- developer.nvidia.com (CUDA Toolkit, programming guides)
- docs.nvidia.com (Technical documentation hub)
- NVIDIA DGX H100/H200 System User Guide (for system-level docs)

### Key Documentation Links Found

**H100 PCIe:**
- Product Page: `https://www.nvidia.com/en-us/data-center/h100/`
- Look for "View Datasheet" option on product page
- Documentation Hub: Search "H100 PCIe" on `docs.nvidia.com`

**H100 SXM5/HGX:**
- DGX System User Guide: Available on docs.nvidia.com
- Hopper Architecture Documentation: Available on developer.nvidia.com
- HGX System Design Guides: Check NVIDIA Enterprise Support portal

**A100:**
- Documentation available on docs.nvidia.com
- Search "A100 datasheet" or "A100 technical specifications"

### Pending Actions

- [ ] Navigate to NVIDIA product pages to find direct PDF download links
- [ ] Download H100 PCIe datasheet PDF (from product page)
- [ ] Download H100 SXM5/HGX documentation PDFs
- [ ] Download A100 documentation (if needed)
- [ ] Check NVIDIA Enterprise Support portal (may require account)
- [ ] Organize downloaded documentation in repository
- [ ] Create documentation index/reference guide

---

## Next Steps

1. **Browser Navigation:**
   - Navigate to `docs.nvidia.com`
   - Search for "H100 PCIe datasheet"
   - Search for "H100 SXM5 datasheet"
   - Search for "HGX H100 system guide"
   - Download PDFs where available

2. **Alternative Sources:**
   - Check NVIDIA Enterprise Support portal (may require account)
   - Check OEM partner sites (Dell, HPE, Supermicro) for integration guides
   - Check NVIDIA Partner Network resources

3. **Documentation Organization:**
   - Create `data/gpu-profiles/nvidia-docs/` directory
   - Organize by GPU model (H100-PCIe/, H100-SXM/, A100/)
   - Create README with links and descriptions

---

## Critical Documentation Needs for Field Deployment

### Power Management
- [x] Power capping capabilities and APIs → `docs/nvidia-manuals/NVML-API-Reference-Guide.pdf` ✅ COLLECTED
- [x] Dynamic power management during inference → NVML API provides `nvmlDeviceSetPowerManagementLimit()` ✅ COLLECTED
- [ ] Power profile modes (performance vs efficiency) → Not explicitly documented in collected manuals
- [x] Power limit configuration methods → NVML API reference covers power limit configuration ✅ COLLECTED

### Thermal Management
- [x] Operating temperature ranges → Covered in product briefs and DGX guides ✅ COLLECTED
- [x] Thermal throttling behavior → `docs/nvidia-manuals/NVML-API-Reference-Guide.pdf` (thermal monitoring APIs) ✅ COLLECTED
- [x] Cooling requirements (air vs liquid) → Covered in product briefs and DGX guides ✅ COLLECTED
- [x] Thermal design power (TDP) specifications → `docs/nvidia-manuals/H100-PCIe-Product-Brief-PB-11133.pdf` (350W TDP) ✅ COLLECTED

### Installation and Configuration
- [ ] Server compatibility requirements
- [ ] PCIe slot requirements
- [ ] Power connector specifications
- [ ] Driver installation procedures
- [ ] Firmware update procedures

### Performance Tuning
- [x] MIG configuration for inference workloads → `docs/nvidia-manuals/H100-MIG-Configuration-Guide.md` ✅ COLLECTED
- [x] NVLink setup for multi-GPU systems → Covered in architecture whitepaper and DGX guides ✅ COLLECTED
- [x] Memory bandwidth optimization → Covered in architecture whitepaper ✅ COLLECTED
- [ ] Inference-specific optimizations → General optimization guidance available, workload-specific tuning requires empirical testing

---

## Related Research

- **GPU Power Profiles:** `data/gpu-profiles/GPU-Power-Profiles.md`
- **Operational Model:** `models/integrated-model/GPU-ASIC-GENERATOR-OPERATIONAL-MODEL.md`
- **Validation Gaps:** `research/OPERATIONAL-MODEL-VALIDATION-GAPS.md`

---

**Last Updated:** 2025-12-02  
**Status:** ✅ Documentation Collected - All available NVIDIA H100 documentation has been collected (8 files, ~83MB). See `docs/nvidia-manuals/COLLECTION-STATUS.md` for details.

**Note:** The collected manuals provide hardware specifications, power management APIs (NVML), and monitoring tools (DCGM), but do NOT provide empirical power profiles for inference workloads. Empirical validation is still needed for per-phase power measurements (idle → launch → model load → warmup → inference).

