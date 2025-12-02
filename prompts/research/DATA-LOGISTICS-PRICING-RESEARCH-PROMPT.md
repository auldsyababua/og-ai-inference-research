# Deep Research Prompt: Data Logistics Pricing Research

**Project**: Off-Grid AI Inference Research  
**Date**: 2025-12-02  
**Purpose**: Research and validate pricing data for Starlink, Sneakernet (providers + DIY), and Fiber connectivity options  
**Target Deliverable**: Validated pricing parameters for Data Logistics Calculator (`models/data-logistics/`)

---

## EXECUTION INSTRUCTIONS

**Output Format**: 
1. **Initial Deliverable**: Create `research-findings.md` as a **Markdown report** with structured findings for review (pricing tables, provider comparisons, cost breakdowns, confidence levels). The report should be embedded directly in the response and structured for easy copy/paste into the file.
2. **After Review/Approval**: Update `models/data-logistics/formulas.md` with validated parameter values and create `models/data-logistics/pricing-data.md` with detailed pricing reference

**Research Approach**: 
- Focus on **2025-2026 pricing** (current market conditions)
- Prioritize **verifiable sources** (vendor websites, published pricing, industry reports)
- Document **confidence levels** for each data point
- Identify **regional variations** where significant
- Provide **cost ranges** (low/typical/high) rather than single point estimates where appropriate

### Research Scope Parameters

**Geographic Focus**:
- **Primary**: United States (rural/off-grid locations)
- **Secondary**: Eastern Europe (Romania, similar regions)
- **Rationale**: Off-grid AI inference deployments likely in rural areas with limited connectivity
- **Regional Priority**: **Prioritize U.S. pricing** where there's conflict or lack of regional parity. Include Romanian/Eastern European data when available, but clearly label as secondary/alternative data. U.S. data should be the default for calculator parameters.

**Currency Standard**:
- **Base Currency**: USD (2025 dollars)
- **Conversion**: Convert other currencies using exchange rates as of research date (December 2025)
- **Documentation**: **Include both original and converted values** for transparency and verification
- **Format**: Present as "€500/month (≈$540/month at Dec 2025 exchange rate)" or similar
- **Labeling**: Clearly label all cost figures with currency, year, geographic region, and conversion rate used
- **Rationale**: Original values allow verification and account for exchange rate fluctuations; converted values enable direct comparison

**Deployment Timeline Assumptions**:
- **Primary Timeline**: 2025-2026 deployment (current pricing)
- **TCO Analysis**: Consider multi-year contracts, volume discounts, price trends
- **Future Considerations**: Note projected cost trends but focus on actionable current data

---

## 1. EXECUTIVE CONTEXT

### 1.1 Research Objective

**Primary Goal**: Validate and research actual pricing data for three data connectivity modes to replace estimated values in the Data Logistics Calculator.

**Current Status**: Calculator uses unverified estimates:
- **Starlink**: $500/month (from Gap Analysis example, not verified)
- **Sneakernet**: $2/mile, 120 TB/trip (from Gap Analysis example, not verified)
- **Fiber**: $30,000/mile (general estimate, not site-specific)

**Critical Need**: Accurate pricing data is essential for:
- Site selection decisions
- Cost-benefit analysis
- Break-even calculations
- Connectivity mode recommendations

### 1.2 Calculator Context

**Target Calculator**: `models/data-logistics/DataLogistics-v1.csv`

**Required Parameters**:

**Starlink:**
- Cost per terminal per month ($/month)
- Effective bandwidth per terminal (Mbps)
- Overhead factor (0-1)
- Usable TB/month per terminal

**Sneakernet:**
- Cost per mile ($/mile) - for both providers and DIY
- Storage capacity per trip (TB/trip)
- Provider pricing models (if available)
- DIY cost breakdown (vehicle, fuel, driver, storage)

**Fiber:**
- Build cost per mile ($/mile)
- Amortization periods (years)
- Ongoing OpEx ($/month)
- Regional cost variations

---

## 2. STARLINK RESEARCH

### 2.1 Primary Research Sources

**Official Sources (Priority 1)**:
1. **Starlink Business Website**
   - URL: `https://www.starlink.com/business`
   - Focus: Business tier pricing, service plans, bandwidth specifications
   - Extract: Monthly cost, bandwidth tiers, data caps (if any), contract terms

2. **Starlink Enterprise Website**
   - URL: `https://www.starlink.com/enterprise` (or similar)
   - Focus: Enterprise tier pricing, high-performance options
   - Extract: Monthly cost, bandwidth specifications, service level agreements

3. **Starlink Support/FAQ**
   - Focus: Bandwidth performance, real-world speeds, reliability
   - Extract: Actual vs advertised speeds, overhead factors, contention ratios

**Industry Reports (Priority 2)**:
4. **FCC Broadband Reports**
   - Focus: Starlink performance data, real-world speeds
   - Extract: Measured bandwidth, latency, reliability metrics

5. **Satellite Internet Comparison Sites**
   - Examples: BroadbandNow, HighSpeedInternet.com
   - Extract: Pricing comparisons, performance data, user reviews

6. **Academic/Research Papers**
   - Search: "Starlink performance measurement", "Starlink bandwidth analysis"
   - Extract: Empirical bandwidth data, overhead factors, real-world usage

**Community Sources (Priority 3)**:
7. **Reddit r/Starlink**
   - Focus: User-reported speeds, costs, real-world experiences
   - Extract: Actual bandwidth, cost variations, regional differences

8. **Starlink User Forums**
   - Extract: Performance data, cost experiences, bandwidth measurements

### 2.2 Research Questions

**Pricing:**
1. What is the current (2025) monthly cost for Starlink Business tier?
2. What is the current (2025) monthly cost for Starlink Enterprise tier?
3. Are there volume discounts for multiple terminals?
4. Are there contract terms (month-to-month vs annual)?
5. Are there setup/equipment costs (one-time fees)?
6. Are there data caps or throttling policies?

**Bandwidth:**
7. What is the advertised bandwidth for Business tier?
8. What is the advertised bandwidth for Enterprise tier?
9. What is the **actual sustained bandwidth** (not peak) in real-world usage?
10. How does bandwidth vary by:
    - Time of day
    - Geographic location
    - Network congestion
    - Weather conditions

**Overhead & Performance:**
11. What is the typical protocol overhead (TCP/IP, retransmissions)?
12. What is the contention ratio (users per satellite/cell)?
13. What is the typical latency (ms)?
14. What is the uptime/reliability percentage?

**Capacity Calculations:**
15. What is the realistic usable TB/month per terminal?
   - Formula: `(Bandwidth_Mbps × Overhead_Factor × seconds_per_month) / (8 × 10^6)`
   - Need: Actual sustained bandwidth and overhead factor

### 2.3 Data Extraction Requirements

**For Each Starlink Source:**

| Data Point | Required | Confidence Level | Notes |
|------------|----------|-----------------|-------|
| Business tier monthly cost | ✅ | High/Medium/Low | Verify if current |
| Enterprise tier monthly cost | ✅ | High/Medium/Low | Verify if current |
| Business tier bandwidth (advertised) | ✅ | High | Official spec |
| Business tier bandwidth (actual) | ✅ | Medium/Low | Real-world data |
| Enterprise tier bandwidth (advertised) | ✅ | High | Official spec |
| Enterprise tier bandwidth (actual) | ✅ | Medium/Low | Real-world data |
| Overhead factor | ✅ | Medium/Low | May need to calculate |
| Latency | ⚠️ | Medium/Low | Not in calculator but useful |
| Uptime/reliability | ⚠️ | Medium/Low | Not in calculator but useful |
| Setup/equipment costs | ✅ | High | One-time fees |
| Contract terms | ⚠️ | High | Month-to-month vs annual |
| Data caps/throttling | ✅ | High | May affect capacity |

**Output Format:**
- Create pricing table with tiers, costs, bandwidth
- Document confidence levels
- Note source dates (verify if 2025 data)
- Include regional variations if significant

---

## 3. SNEAKERNET RESEARCH

### 3.1 Research Scope

**Two Approaches to Research:**

**Approach A: Existing Sneakernet Providers**
- Research commercial services that transport data physically
- Examples: AWS Snowmobile, Azure Data Box, specialized data transport services
- Focus: Pricing models, capacity, service areas

**Approach B: DIY Sneakernet (Truck + NAS)**
- Research cost of building custom solution
- Components: Vehicle, fuel, driver, storage (NAS/drives), software
- Focus: Total cost of ownership, capacity, operational considerations

### 3.2 Existing Sneakernet Providers

**Cloud Provider Services (Priority 1)**:

1. **AWS Snowmobile**
   - URL: `https://aws.amazon.com/snowmobile/`
   - Focus: Large-scale data transport service
   - Extract: Pricing model, capacity, service areas, minimum commitments

2. **AWS Snowball**
   - URL: `https://aws.amazon.com/snowball/`
   - Focus: Smaller-scale data transport
   - Extract: Pricing, capacity, service model

3. **Azure Data Box**
   - URL: `https://azure.microsoft.com/en-us/products/azure-storage/data-box/`
   - Focus: Microsoft's data transport service
   - Extract: Pricing, capacity, service areas

4. **Google Transfer Appliance**
   - URL: `https://cloud.google.com/transfer-appliance`
   - Focus: Google Cloud data transport
   - Extract: Pricing, capacity, service model

**Specialized Data Transport Services (Priority 2)**:

5. **Search**: "data transport service", "sneakernet service", "physical data transfer"
   - Focus: Commercial services beyond cloud providers
   - Extract: Pricing models, capacity, service areas

6. **Courier Services with Data Transport**
   - Examples: FedEx, UPS specialized services
   - Extract: Pricing for large data transport, capacity options

**Research Questions for Providers:**
1. What is the pricing model? (per TB, per trip, flat fee?)
2. What is the capacity per trip?
3. What is the minimum commitment/order size?
4. What are the service areas/regions?
5. What is the typical turnaround time?
6. Are there volume discounts?
7. What are the setup/one-time costs?

### 3.3 DIY Sneakernet (Truck + NAS)

**Component Research:**

**Vehicle Costs:**
1. **Vehicle Purchase/Lease**
   - Research: Light truck/van costs (new vs used)
   - Examples: Ford Transit, Ram ProMaster, similar vehicles
   - Extract: Purchase price, lease rates, TCO over 5 years

2. **Vehicle Operating Costs**
   - Fuel costs (current 2025 prices)
   - Maintenance costs (per mile)
   - Insurance costs
   - Registration/licensing
   - Depreciation

**Storage Costs:**
3. **NAS/Storage Hardware**
   - Research: High-capacity NAS systems (both commercial and open-source)
   - **Commercial Examples**: Synology, QNAP, custom builds
   - **Open-Source Options**: TrueNAS, OpenMediaVault, custom Linux-based solutions
   - Extract: Cost per TB, total capacity, form factor
   - **Note**: Include open-source/open-hardware options as they may offer cost savings

4. **Drive Costs**
   - Research: High-capacity drives (12TB, 16TB, 20TB+)
   - Examples: Seagate Exos, Western Digital Red/Pro
   - Extract: Cost per TB, drive capacity, reliability

5. **Storage Enclosures**
   - Research: Drive enclosures, hot-swap bays
   - Extract: Cost, capacity, form factor

**Operational Costs:**
6. **Driver Costs**
   - Research: Driver wages (per hour, per mile, per trip)
   - Consider: Full-time vs part-time, contractor vs employee
   - Extract: Labor cost per mile/trip

7. **Software/Management**
   - Research: Data transfer software, monitoring tools
   - **Commercial Options**: Extract software costs, licensing
   - **Open-Source Options**: Include free/open-source alternatives (rsync, rclone, custom scripts, monitoring tools)
   - Extract: Software costs (including $0 for open-source), licensing models
   - **Note**: Open-source options may significantly reduce software costs

**Research Questions for DIY:**
1. What is the total cost per mile (vehicle + fuel + driver + maintenance)?
2. What is the storage capacity per trip (TB)?
3. What is the cost per TB of storage (hardware) - both commercial and open-source options?
4. What is the total cost per trip (all components)?
5. What is the cost per TB transported (total trip cost ÷ capacity)?
6. What are the operational considerations (security, reliability, maintenance)?
7. **What are the cost differences between commercial and open-source/open-hardware solutions?**
8. **What open-source software options exist for data transfer and management?**

**Data Extraction Requirements:**

| Component | Required | Research Focus | Notes |
|----------|----------|---------------|-------|
| Vehicle purchase/lease | ✅ | Cost, TCO | New vs used, lease vs buy |
| Fuel cost | ✅ | Current 2025 prices | Regional variations |
| Maintenance cost | ✅ | Per mile estimate | Typical maintenance schedule |
| Insurance | ✅ | Annual/monthly cost | Commercial vehicle insurance |
| Driver cost | ✅ | Per mile/hour | Labor costs |
| NAS hardware | ✅ | Cost, capacity | Pre-built vs custom |
| Drive costs | ✅ | Cost per TB | Current 2025 pricing |
| Storage enclosure | ✅ | Cost, capacity | Form factor considerations |
| Software | ⚠️ | Licensing costs | If applicable |

**Output Format:**
- Create cost breakdown table (vehicle, fuel, driver, storage, etc.)
- **Include separate breakdowns for commercial vs open-source options** (where applicable)
- Calculate total cost per mile (for both commercial and open-source scenarios)
- Calculate total cost per trip
- Calculate cost per TB (trip cost ÷ capacity)
- Compare DIY vs provider costs
- **Compare commercial vs open-source DIY costs**
- Document assumptions and confidence levels

---

## 4. FIBER RESEARCH

### 4.1 Primary Research Sources

**Industry Reports (Priority 1)**:

1. **FCC Broadband Deployment Reports**
   - Focus: Fiber build costs, **last-mile rural deployment costs** (primary)
   - Extract: Cost per mile data, regional variations
   - **Note**: Prioritize last-mile rural connectivity over long-haul runs

2. **NTIA BroadbandUSA**
   - Focus: Federal broadband programs, cost data
   - Extract: Fiber build cost estimates, grant data
   - **Note**: Focus on last-mile/rural deployment programs

3. **Rural Broadband Association Reports**
   - Examples: NTCA, NRECA reports
   - Extract: Member cost data, deployment costs
   - **Note**: These focus on last-mile rural connectivity

**ISP/Contractor Sources (Priority 2)**:

4. **ISP Websites**
   - Focus: Rural ISPs, regional providers
   - Extract: Service area maps, build cost estimates (if published)

5. **Fiber Construction Contractors**
   - Search: "fiber construction contractor", "fiber installation cost"
   - Extract: Cost estimates, pricing models

6. **Government Broadband Programs**
   - Examples: USDA ReConnect, state broadband programs
   - Extract: Grant data, cost per mile, project costs

**Academic/Research Sources (Priority 3)**:

7. **Academic Papers**
   - Search: "rural fiber deployment cost", "fiber build cost analysis"
   - Extract: Cost data, regional variations, cost factors

8. **Industry Publications**
   - Examples: Broadband Communities, Light Reading
   - Extract: Cost data, case studies, industry trends

### 4.2 Research Questions

**Build Costs:**
1. What is the typical cost per mile for **last-mile rural fiber deployment**? (Prioritize over long-haul runs)
2. How do costs vary by:
   - Terrain (flat vs mountainous, rocky vs soft soil)
   - Existing infrastructure (poles, conduits, rights-of-way)
   - Labor costs (regional variations)
   - Permitting/regulatory requirements
3. What is the cost range (low/typical/high)?
4. What are the cost components?
   - Fiber cable
   - Installation labor
   - Equipment (splices, enclosures, etc.)
   - Permitting/regulatory
   - Rights-of-way acquisition
5. **How do last-mile costs compare to long-haul costs?** (Include for context, but prioritize last-mile)

**Operational Costs:**
5. What is the typical monthly OpEx for fiber?
6. What are the OpEx components?
   - Maintenance
   - Monitoring
   - Power (if applicable)
   - Insurance
7. How do OpEx costs vary by:
   - Fiber length
   - Service level
   - Provider type

**Amortization:**
8. What are typical amortization periods for fiber infrastructure?
9. How do amortization periods vary by:
   - Provider type (ISP vs private)
   - Financing source (private vs public)
   - Project scale

**Regional Variations:**
10. What are the cost differences by region?
    - US regions (Northeast, Southeast, Midwest, West, etc.)
    - Urban vs rural
    - State-specific variations

### 4.3 Data Extraction Requirements

**For Each Fiber Source:**

| Data Point | Required | Confidence Level | Notes |
|------------|----------|-----------------|-------|
| Cost per mile (rural) | ✅ | High/Medium/Low | Primary metric |
| Cost per mile (urban) | ⚠️ | Medium/Low | For comparison |
| Cost range (low/typical/high) | ✅ | Medium | Better than single point |
| Cost by terrain | ⚠️ | Medium/Low | If available |
| Cost components breakdown | ✅ | Medium | Cable, labor, etc. |
| Monthly OpEx | ✅ | Medium/Low | Ongoing costs |
| OpEx components | ⚠️ | Medium/Low | If available |
| Amortization periods | ✅ | Medium | Typical ranges |
| Regional variations | ⚠️ | Low | If significant |
| Project scale factors | ⚠️ | Low | If available |

**Output Format:**
- Create cost per mile table with ranges
- Document cost factors (terrain, infrastructure, etc.)
- Provide OpEx estimates
- Note regional variations
- Document confidence levels

---

## 5. DATA VALIDATION & CONFIDENCE ASSESSMENT

### 5.1 Confidence Levels

**High Confidence:**
- Official vendor pricing (current 2025)
- Published industry reports from reputable sources
- Government data (FCC, NTIA)
- Multiple sources confirming same data

**Medium Confidence:**
- User-reported data (Reddit, forums)
- Older pricing data (2023-2024) adjusted for inflation
- Single source industry reports
- Estimated calculations based on components

**Low Confidence:**
- Outdated data (>2 years old)
- Single anecdotal reports
- Estimated calculations with significant assumptions
- Regional data applied to different regions

### 5.2 Validation Checklist

**For Each Data Point:**
- [ ] Source identified and documented
- [ ] Date of data noted
- [ ] Geographic region specified
- [ ] Confidence level assigned
- [ ] Cross-referenced with other sources (if available)
- [ ] Assumptions documented
- [ ] Limitations noted

### 5.3 Data Gaps Documentation

**Document:**
- Parameters where no data found
- Parameters with only low-confidence data
- Regional variations not captured
- Time-sensitive data that may change

---

## 6. OUTPUT REQUIREMENTS

### 6.1 Research Findings Document

**File**: `research/data-logistics-pricing/research-findings.md`

**Structure:**
1. **Executive Summary**
   - Key findings
   - Confidence assessment
   - Data gaps

2. **Starlink Pricing**
   - Pricing tables (Business, Enterprise)
   - Bandwidth data (advertised vs actual)
   - Overhead factors
   - Capacity calculations
   - Source citations

3. **Sneakernet Pricing**
   - Provider comparison table
   - DIY cost breakdown
   - Cost per mile calculations
   - Cost per TB calculations
   - Source citations

4. **Fiber Pricing**
   - Cost per mile (rural, ranges)
   - Cost factors (terrain, infrastructure)
   - OpEx estimates
   - Amortization periods
   - Regional variations
   - Source citations

5. **Recommendations**
   - Recommended default values for calculator
   - Confidence levels
   - Data gaps requiring additional research
   - Regional considerations

### 6.2 Updated Calculator Parameters

**File**: `models/data-logistics/pricing-data.md` (new file)

**Structure:**
- Validated parameter values
- Confidence levels
- Source citations
- Regional variations
- Update instructions for `formulas.md`

### 6.3 Source Citations

**Format:**
- Author/Organization
- Title
- URL (if available)
- Date accessed
- Date of data (if different from access date)
- Geographic scope
- Confidence level

---

## 7. RESEARCH PRIORITY

### Phase 1: High Priority (Do First)
1. **Starlink Business/Enterprise pricing** (official sources)
2. **Starlink bandwidth** (actual vs advertised)
3. **Fiber cost per mile** (rural, industry reports)
4. **DIY Sneakernet cost breakdown** (vehicle, fuel, driver, storage)

### Phase 2: Medium Priority
5. **Starlink overhead factors** (real-world performance)
6. **Sneakernet providers** (AWS, Azure, etc.)
7. **Fiber OpEx** (ongoing costs)
8. **Regional variations** (where significant)

### Phase 3: Low Priority (If Time Permits)
9. **Fiber cost factors** (terrain, infrastructure breakdown)
10. **Volume discounts** (Starlink, providers)
11. **Contract terms** (monthly vs annual)
12. **Future cost trends** (projections)

---

## 8. RESEARCH TIMELINE

**Estimated Time**: 4-6 hours

**Breakdown:**
- Starlink research: 1-2 hours
- Sneakernet research: 1.5-2 hours
- Fiber research: 1-1.5 hours
- Documentation: 0.5-1 hour

---

## 9. NOTES FOR RESEARCH AGENT

**Key Considerations:**
- Focus on **2025-2026 pricing** (current market)
- Prioritize **verifiable sources** over anecdotal data
- Document **confidence levels** for all data points
- Note **geographic scope** (US vs international)
- Provide **ranges** where single point estimates are uncertain
- **Cross-reference** multiple sources when possible
- **Document assumptions** clearly

**Calculator Integration:**
- Research should directly inform `models/data-logistics/formulas.md` default values
- Update "Default Parameter Values" section with validated data
- Replace "UNVERIFIED" warnings with confidence levels
- Add source citations

**Future Research:**
- Note any data that requires regular updates (pricing changes, new services)
- Identify areas where site-specific quotes are still needed (fiber build costs)
- Document any significant regional variations

---

## 10. CLARIFYING ANSWERS

### 10.1 Regional Priority

**Answer**: **Prioritize U.S. pricing** where there's conflict or lack of regional parity. Include Romanian/Eastern European data when available, but clearly label as secondary/alternative data. U.S. data should be the default for calculator parameters. If Romanian/Eastern European data differs significantly, include both but note which is primary.

### 10.2 Currency Exchange

**Answer**: **Include both original and converted values** for transparency and verification. Format as "€500/month (≈$540/month at Dec 2025 exchange rate)" or similar. This allows:
- Verification of conversion accuracy
- Account for exchange rate fluctuations
- Direct comparison in USD for calculator use
- Preservation of original context

### 10.3 Documentation Format

**Answer**: **Markdown report directly embedded** in the response. Structure the `research-findings.md` content so it can be easily copied/pasted into the file. Use standard Markdown formatting with tables, headers, and code blocks as appropriate.

### 10.4 Open Source Options

**Answer**: **Yes, include open-source/open-hardware options** for DIY Sneakernet. Research:
- Open-source NAS solutions (TrueNAS, OpenMediaVault, custom Linux builds)
- Open-source data transfer software (rsync, rclone, custom scripts)
- Open-source monitoring tools
- Cost comparison: commercial vs open-source solutions
- Document cost savings from open-source options

### 10.5 Fiber Deployment

**Answer**: **Lean toward last-mile rural connectivity** over long-haul fiber runs. Off-grid AI inference sites are typically in rural areas requiring last-mile connections. However, include long-haul cost context where relevant for comparison. Prioritize:
- Last-mile rural fiber deployment costs
- Rural ISP build costs
- Federal/state rural broadband program data
- Include long-haul costs for context/comparison only

---

**END OF RESEARCH PROMPT**

