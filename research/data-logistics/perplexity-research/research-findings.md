# Data Logistics Pricing Research Findings

**Project**: Off-Grid AI Inference Research  
**Date**: December 2, 2025  
**Purpose**: Validated pricing data for Starlink, Sneakernet, and Fiber connectivity options  
**Geographic Focus**: United States (Primary), with notes on international variations where applicable  
**Currency**: USD (2025 dollars)

---

## EXECUTIVE SUMMARY

### Key Findings

This research provides validated, current-market pricing data for three data connectivity modes relevant to off-grid AI inference deployments. Key findings include:

**Starlink Business (2025 Pricing)**:
- Base plans now use **data bucket model** (Priority data with overage charges)
- Local Priority plans: $65-$540/month for 50GB-2TB
- Business bandwidth: 100-350 Mbps download (actual tested speeds)
- **Major pricing change in 2025**: All unlimited plans eliminated, replaced with tiered data buckets

**Sneakernet**:
- **AWS Snowball**: ~$300/device for 10 days (80TB usable capacity)
- **Azure Data Box**: $250/device for 10 days (80TB usable capacity)
- **DIY approach**: $0.70/mile IRS standard rate (includes all vehicle costs)
- **Enterprise drives**: $13.50-$15.00 per TB (20TB Seagate Exos drives at ~$280-$300)

**Fiber (Last-Mile Rural)**:
- **Rural deployment**: $40,000-$80,000 per mile (median $60,000/mile)
- **Aerial installation**: $40,000-$60,000 per mile
- **Underground**: $79,200-$184,800 per mile ($15-$35 per foot)
- Labor comprises 60%+ of total costs

### Confidence Assessment

- **High Confidence**: Starlink official pricing, AWS/Azure published rates, IRS mileage rates, industry fiber reports
- **Medium Confidence**: Real-world Starlink bandwidth tests, DIY sneakernet component costs, fiber regional variations
- **Low Confidence**: Long-term fiber OpEx (limited public data)

### Data Gaps

1. Starlink **overhead factors** for actual usable throughput (protocol overhead, retransmissions)
2. Fiber **ongoing OpEx** breakdown by component (maintenance, monitoring, power)
3. Regional fiber cost variations beyond broad urban/rural categories
4. Starlink **priority data performance** under congestion (new 2025 throttling model)

---

## 1. STARLINK PRICING & PERFORMANCE

### 1.1 2025 Pricing Structure (Major Change)

**CRITICAL UPDATE**: Starlink eliminated unlimited business plans in early 2025, replacing them with a **data bucket model** with throttling.

#### Local Priority Plans

| Plan | Monthly Cost | Priority Data | Post-Limit Speed | Hardware Cost |
|------|--------------|---------------|------------------|---------------|
| 50GB | $65/month | 50GB | 1 Mbps | $2,500 (Business dish) |
| 500GB | $165/month | 500GB | 1 Mbps | $2,500 |
| 1TB | $290/month | 1TB | 1 Mbps | $2,500 |
| 2TB | $540/month | 2TB | 1 Mbps | $2,500 |

**Additional data blocks**:
- +50GB: $25/month
- +500GB: $125/month

**Critical throttling warning**: Once priority data is exhausted, speeds throttle to **1 Mbps** (99% reduction), effectively eliminating usable high-speed data transfer for AI inference workloads.

#### Global Priority Plans (for reference)

Higher pricing for maritime/global connectivity:
- 50GB: $250/month
- 500GB: $650/month
- 1TB: $1,150/month
- 2TB: $2,150/month

**Sources**: [1][8][9][11][14]  
**Confidence**: **High** (official Starlink pricing as of 2025)  
**Date Verified**: December 2025

---

### 1.2 Bandwidth Performance (Real-World Testing)

#### Official Specifications

| Service Tier | Download (Advertised) | Upload (Advertised) | Latency |
|--------------|----------------------|---------------------|---------|
| Business | 100-350 Mbps | 10-50 Mbps | 25-50ms |
| Residential | 80-200 Mbps | 15-35 Mbps | 25-60ms |

**Source**: [16]

#### Real-World Test Results (2024-2025)

**Independent Testing (PCMag, 2025)**:
- **Mean download speeds**: 177 Mbps (Q4 2024/Q1 2025)
- **Peak speeds**: Up to 325 Mbps
- **Upload speeds**: Mean 23 Mbps, peaks up to 64 Mbps
- **Latency**: 10-30ms (most results), significant improvement from prior years
- **Consistency**: Most speed tests fall between 140-200 Mbps

**Source**: [151]  
**Confidence**: **High** (extensive multi-year testing with Dish V4)

**Ookla Speedtest Data (Q1 2025, U.S. Nationwide)**:
- **Median download**: 104.71 Mbps (doubled from 53.95 Mbps in Q3 2022)
- **Median upload**: 14.84 Mbps (up from 7.50 Mbps in Q3 2022)
- **FCC 100/20 Mbps compliance**: Only 17.4% of users (primarily due to upload limitations)

**Source**: [13]  
**Confidence**: **High** (large sample, independent testing)

**BroadbandNow Testing (2025)**:
- **Calm environment**: 117 Mbps at 5 feet, 30.1 Mbps at 50 feet
- **Busy environment**: 62.7-67.2 Mbps (more consistent across distances)
- Notable: Performance **improved** under load in busy environments vs. light use

**Source**: [148]  
**Confidence**: **Medium** (limited sample size)

#### Performance Trends (2022-2025)

**Key improvements**:
- Download speeds **doubled** from 2022 to 2025
- Upload speeds improved **175%** since 2022
- Latency decreased **62%** since 2022
- Consistency vastly improved (fewer low-speed outliers)

**Source**: [151]

---

### 1.3 Capacity Calculations

#### Theoretical Capacity (Per Terminal/Month)

Assuming:
- **Sustained bandwidth**: 150 Mbps download (conservative, based on real-world median)
- **Overhead factor**: 0.85 (15% protocol overhead - **estimated, not verified**)
- **Uptime**: 99% (per official specs)

**Calculation**:
```
Usable bandwidth = 150 Mbps × 0.85 = 127.5 Mbps
Seconds per month = 30 days × 24 hours × 3600 seconds = 2,592,000 seconds
Data per month = (127.5 × 10^6 bits/s × 2,592,000 s) / (8 × 10^12) = 41.3 TB/month
Actual with 99% uptime = 41.3 TB × 0.99 = 40.9 TB/month
```

**HOWEVER**: With new 2025 data bucket limits:
- **1TB plan**: 1TB priority data, then 1 Mbps throttled = **effectively 1TB/month usable**
- **2TB plan**: 2TB priority data, then 1 Mbps throttled = **effectively 2TB/month usable**

**Critical finding**: For AI inference data logistics, **data bucket limits are the binding constraint**, not bandwidth capacity. Post-throttle 1 Mbps speeds are unusable for large data transfers.

**Confidence**: **Medium** (theoretical calculations, overhead factor estimated)

---

### 1.4 Cost Summary

| Metric | Value | Confidence | Notes |
|--------|-------|------------|-------|
| **Monthly service (1TB)** | $290/month | High | Local Priority plan |
| **Monthly service (2TB)** | $540/month | High | Local Priority plan |
| **Hardware (one-time)** | $2,500 | High | Business dish |
| **Effective bandwidth** | 100-350 Mbps | High | Advertised spec |
| **Actual sustained bandwidth** | 140-200 Mbps | High | Real-world median |
| **Usable TB/month** | 1-2 TB | High | **Data bucket limit** (2025 model) |
| **Overage cost** | $125/500GB | High | $250/TB effective |
| **Post-throttle speed** | 1 Mbps | High | 99% reduction |

**Major Caveat**: 2025 pricing model fundamentally changes Starlink economics for high-volume data transfer. Unlimited plans no longer available. For AI inference workloads requiring >2TB/month, overage costs are **$250/TB**, making Starlink extremely expensive at scale.

---

## 2. SNEAKERNET PRICING

### 2.1 Commercial Providers

#### AWS Snowball Edge Storage Optimized (210TB)

**Pricing Model** (On-Demand):
- **Service fee**: ~$300 per device per 10 days
- **Additional days**: ~$30/day
- **Usable capacity**: 80-100TB (pricing options for <100TB vs 100-210TB)
- **Data transfer IN** (to AWS): Free
- **Shipping**: Included (AWS-provided labels)

**Source**: [21][25][31]  
**Confidence**: **High** (official AWS pricing)

**Alternative Model** (Monthly pricing):
- Available for long-term edge compute deployments
- Example: ~$5,038/month for 104 vCPU configuration
- Not applicable for one-time data transport

**Snowmobile** (retired 2024):
- Previously: $0.005/GB per month (~$500,000/month for 100PB)
- No longer available for new customers

**Source**: [28]

#### Azure Data Box

**Pricing Model**:
- **Standard Data Box (80TB usable)**: $250 per device per job (10 days included)
- **Additional days**: $30/day
- **Data processing fee**: $2.50 per TB transferred
- **Data Box Heavy (800TB usable)**: $1,000 per job (20 days included)
- **Additional days (Heavy)**: $50/day

**Total cost example** (100TB transfer):
- Device rental: $250 (10 days)
- Data processing: $250 ($2.50 × 100TB)
- **Total**: $500 for 100TB = **$5/TB**

**Source**: [26][29][32][35]  
**Confidence**: **High** (official Azure pricing)

#### Google Transfer Appliance

**Pricing**:
- **Rental**: $300 for smaller appliance
- **Shipping**: FedEx (extra cost)
- Limited public pricing information

**Source**: [33]  
**Confidence**: **Medium** (limited data)

---

### 2.2 DIY Sneakernet Cost Breakdown

#### Vehicle Costs (2025 Pricing)

**Light Cargo Van Purchase Prices**:

| Vehicle | Configuration | MSRP | Notes |
|---------|---------------|------|-------|
| Ford Transit-150 Cargo | Base, Low Roof | $47,400 | Standard cargo van |
| Ford Transit-250 Cargo | Med Roof, 148" WB | $49,800-$54,830 | Higher payload |
| Ram ProMaster 2500 | Tradesman, High Roof | $51,000-$57,000 | Competitive option |
| Ram ProMaster 1500 | Low Roof | $47,655 | Entry-level |

**Sources**: [62][63][66][75][78]  
**Confidence**: **High** (manufacturer MSRP, December 2025)

**Lease Pricing** (for reference):
- Commercial van leasing available but highly variable
- Example straight truck lease: ~$1,200/month (Ryder)
- Not optimal for occasional sneakernet use

**Source**: [76]

#### Operating Costs (Per Mile)

**IRS Standard Mileage Rate (2025)**:
- **Business use**: $0.70 per mile (up from $0.67 in 2024)
- Covers: fuel, maintenance, insurance, depreciation
- Applies to all vehicle types (gasoline, diesel, electric, hybrid)

**Source**: [81][83][84][85]  
**Confidence**: **High** (official IRS rate)

**Fuel Costs (December 2025)**:
- **Gasoline**: $3.00/gallon national average (range: $2.41-$4.56 by state)
- **Diesel**: $3.74/gallon national average (up 5.6% YoY)
- Regional variation: California $4.92 diesel, Oklahoma $2.41 gasoline

**Sources**: [141][142][143][145][160][168][170]  
**Confidence**: **High** (government data, December 2025)

**Commercial Trucking Operating Costs** (for context):
- **Total cost**: $2.27 per mile (2023 average for semi-trucks)
- **Fuel**: $0.55 per mile (2023, down from $0.64 in 2022)
- **Maintenance**: $0.09-$0.40 per mile depending on vehicle type
- **Insurance**: $0.06-$0.18 per mile

**Sources**: [82][86][89]  
**Confidence**: **High** (ATRI industry benchmark)

**Commercial Driver Wages (2025)**:
- **National median**: $53,560/year = $25.75/hour = $30.58/hour (BLS)
- **High-paying states**: California $64,700/year, New Jersey $63,900/year
- **Los Angeles market**: $78,817/year = $37.89/hour

**Sources**: [127][130][133][136]  
**Confidence**: **High** (BLS data, December 2025)

**Commercial Vehicle Insurance (2025)**:
- **Average**: $1,762/year = $147/month for small business
- **Range**: $58-$1,125/month depending on vehicle type and industry
- **Van/Light truck**: ~$150-$250/month typical

**Sources**: [161][163][164]  
**Confidence**: **Medium** (industry averages, varies significantly)

---

#### Storage Hardware Costs

**High-Capacity Enterprise Drives (2025)**:

| Capacity | Model | Price Range | Cost per TB | Notes |
|----------|-------|-------------|-------------|-------|
| 20TB | Seagate Exos X20 | $270-$300 | $13.50-$15.00 | Most cost-effective |
| 18TB | Seagate Exos X18 | $260-$290 | $14.44-$16.11 | Good value |
| 16TB | Various enterprise | $230-$270 | $14.37-$16.87 | Alternate option |
| 12TB | Various NAS/Enterprise | $159-$193 | $13.25-$16.08 | "Sweet spot" historically |

**Sources**: [101][106][109][115]  
**Confidence**: **High** (current retail pricing, December 2025)

**Key finding**: 20TB drives offer best $/TB ratio at ~$13.50-$15/TB. Larger capacities (22TB, 24TB) exist but cost more per TB.

**NAS Hardware Costs**:

**Commercial Options**:
- **Synology DS423+**: $499 (4-bay, supports RAID)
- **QNAP TS-264-8G**: $424 (2-bay, 8GB RAM)
- **QNAP TS-464-8G**: $565 (4-bay, 8GB RAM)

**Sources**: [107][110][114]  
**Confidence**: **High** (retail pricing, December 2025)

**Open-Source/DIY Options**:
- **TrueNAS Core/SCALE**: Free (open-source, ZFS-based)
- **OpenMediaVault**: Free (open-source, Debian-based)
- **Hardware**: Build your own NAS using commodity PC parts

**Sources**: [121][124][125][126][129][134]  
**Confidence**: **High** (established open-source projects)

**Cost comparison**:
- Commercial NAS (4-bay Synology): $499 + drives
- Open-source NAS (custom build): $200-$400 for hardware + $0 software + drives

**Total storage cost example** (120TB capacity):
- 6× 20TB drives: 6 × $280 = $1,680
- NAS enclosure (commercial): $499
- **Total**: $2,179 for 120TB = **$18.16/TB** (hardware)

OR

- 6× 20TB drives: $1,680
- DIY NAS (custom PC): ~$300-$400
- TrueNAS (free software): $0
- **Total**: ~$2,080 for 120TB = **$17.33/TB** (hardware)

**Confidence**: **High** (component pricing well-documented)

---

#### DIY Sneakernet Total Cost Model

**Scenario**: 100-mile round trip, 120TB capacity per trip

**Vehicle operating cost**:
- 100 miles × $0.70/mile = $70/trip

**Driver cost** (if hired):
- 4 hours (2 hours drive each way) × $30/hour = $120/trip

**Total per trip**: $190

**Cost per TB**: $190 / 120TB = **$1.58/TB**

**Amortized storage hardware cost** (assuming 10 uses):
- $2,080 total / 10 uses = $208/trip
- Total cost: $190 + $208 = $398/trip
- **Cost per TB**: $398 / 120TB = **$3.32/TB** (including hardware amortization)

**Confidence**: **High** (well-defined component costs)

---

### 2.3 Sneakernet Cost Comparison

| Method | Capacity | Total Cost | Cost per TB | Turnaround | Notes |
|--------|----------|------------|-------------|------------|-------|
| **AWS Snowball** | 80-100TB | $300 | $3.00-$3.75 | ~1 week | Device rental only |
| **Azure Data Box** | 80TB | $500 | $6.25 | ~1 week | Includes processing |
| **DIY (trip only)** | 120TB | $190 | $1.58 | Same day | Excludes hardware |
| **DIY (with hardware)** | 120TB | $398 | $3.32 | Same day | 10-use amortization |
| **Commercial provider** | Variable | $2-$5/TB | $2-$5 | Variable | Estimated, limited data |

**Key findings**:
- **DIY is cost-competitive** with cloud providers when hardware costs are amortized
- **DIY offers faster turnaround** (same-day possible vs. ~1 week shipping)
- **Cloud providers** eliminate hardware purchase/management burden
- **Open-source software** (TrueNAS, OpenMediaVault) reduces costs vs. commercial NAS

---

## 3. FIBER PRICING

### 3.1 Last-Mile Rural Deployment Costs

#### Cost Per Mile (2025 Estimates)

**Industry Benchmarks**:

| Source | Cost Range (per mile) | Type | Confidence |
|--------|------------------------|------|------------|
| Conexon (2022) | $2,000/location avg | Per-location model | High |
| DoT (2017/2020) | $27,000/mile | Average fiber | Medium |
| Ceragon (2023) | $60,000-$80,000/mile | Rural fiber | High |
| Network Installers (2025) | $40,000-$60,000/mile | Aerial | High |
| Network Installers (2025) | $79,200-$184,800/mile | Underground (15-35/ft) | High |
| Reddit/Field Reports | $56,000/mile | Suburban FTTB | Medium |
| CPUC California (2020) | $4,058-$6,733/mile avg | State model | High |

**Sources**: [42][45][47][48][49][52][55][58][156]

**Consensus estimate for rural last-mile**:
- **Aerial**: $40,000-$60,000 per mile (median ~$50,000)
- **Underground**: $80,000-$180,000 per mile (median ~$130,000)
- **Blended average**: $60,000-$80,000 per mile

**Confidence**: **High** (multiple industry sources, 2023-2025 data)

---

#### Installation Method Breakdown

**Aerial Installation** ("Overlashing"):
- **Cost**: $8-$12 per linear foot = $42,240-$63,360 per mile
- **Method**: Attach fiber to existing utility poles
- **Advantages**: Lower cost, faster installation
- **Challenges**: Pole attachment fees ($5-$15/pole/year), make-ready costs ($500-$5,000/pole)

**Source**: [42][45][49]

**Underground Installation**:

| Method | Cost per Foot | Cost per Mile | Notes |
|--------|---------------|---------------|-------|
| Trenching | $15-$35 | $79,200-$184,800 | Most common |
| Directional boring | $20-$30 | $105,600-$158,400 | Obstacle avoidance |
| Direct burial | $1-$6 | $5,280-$31,680 | Simple installs only |

**Source**: [45][156]

**Underground advantages**: Better protection, lower long-term maintenance  
**Underground disadvantages**: Higher upfront cost, slower installation

---

#### Cost Components Breakdown

**Labor** (60%+ of total cost):
- Single largest cost component
- Regional variations: $20-$50/hour (US/Western Europe), $5-$15/hour (China/India)
- Skilled technicians required for splicing, testing

**Source**: [43][149][152]

**Materials**:
- Fiber cable: $0.09-$1.52 per foot (single-mode)
- Multimode fiber: $1.50-$6.00 per foot
- Armored cable: $6.00-$13.50 per foot

**Source**: [45][166][171]

**Equipment & Infrastructure**:
- Splice enclosures, distribution panels, termination equipment
- Fusion splicers, OTDRs (optical testing), trenching machinery

**Permitting & Regulatory**:
- Application fees, environmental assessments, zoning compliance
- Railroad crossings, bridge permits (significant barriers per NTCA)

**Source**: [44][152]

**Make-Ready Costs** (aerial):
- Pole preparation: $500-$5,000 per pole
- Pole ownership matters significantly (utility vs. private)
- Adds $5-$6 per foot to overall cost

**Source**: [42][49]

---

#### Regional Variations

**By Terrain/Density**:

| Area Type | Underground Cost/Foot | Notes |
|-----------|----------------------|-------|
| Low-density rural | $12.50 | <5 homes per mile |
| Standard rural | $14.63 | Typical rural |
| Suburban | $14.59 | Suburban density |
| Urban | Higher | Not specified, more obstructions |

**Source**: [42]

**By State/Region**:
- **Northeast**: Most expensive region to operate (2023 ATRI)
- **Southeast**: High driver benefit costs
- **California**: State broadband model shows $4,058-$6,733/mile average

**Sources**: [50][86]

---

### 3.2 Ongoing Operational Costs (OpEx)

**Limited public data available**. Key OpEx components:

**Maintenance & Monitoring**:
- Network monitoring systems
- Routine inspections
- Repair/replacement of damaged segments

**Power** (if active equipment):
- Fiber is passive, but network equipment requires power
- Minimal for passive fiber runs

**Insurance & Administrative**:
- Property insurance for infrastructure
- Administrative overhead

**Estimated OpEx**: $100-$500/month per mile (industry estimates, **low confidence**)

**Data Gap**: Detailed fiber OpEx breakdown not readily available in public sources. This would require direct quotes from fiber providers or detailed utility data.

---

### 3.3 Amortization & TCO

**Typical Amortization Periods**:
- **Private deployments**: 5-10 years
- **Public/utility fiber**: 15-30 years
- **Grant-funded projects**: Varies by program requirements

**Source**: Industry standards (not explicitly documented in research)

**Total Cost of Ownership Example** (10-mile rural deployment):

**CapEx**:
- Fiber installation: 10 miles × $60,000/mile = $600,000

**Annual OpEx** (estimated):
- Maintenance: 10 miles × $300/mile/month × 12 = $36,000/year

**10-year TCO**:
- CapEx: $600,000
- OpEx: $360,000
- **Total**: $960,000

**Amortized monthly cost**: $960,000 / 120 months = $8,000/month

**Confidence**: **Medium** (CapEx well-documented, OpEx estimated)

---

### 3.4 Fiber Cost Summary

| Metric | Value | Confidence | Notes |
|--------|-------|------------|-------|
| **Aerial install** | $40,000-$60,000/mile | High | Overlashing to poles |
| **Underground install** | $80,000-$180,000/mile | High | Trenching/boring |
| **Blended average** | $60,000-$80,000/mile | High | Rural last-mile |
| **Make-ready** | $500-$5,000/pole | High | Aerial add-on |
| **Pole attachment fees** | $5-$15/pole/year | High | Ongoing OpEx |
| **Labor component** | 60%+ of total | High | Largest cost driver |
| **Monthly OpEx** | $100-$500/mile | Low | Estimated, limited data |
| **Typical amortization** | 5-10 years (private) | Medium | Industry standard |

**Critical finding**: Fiber is a **high CapEx, low OpEx** solution with long payback periods. Rural deployments face significantly higher per-mile costs due to lower density and longer cable runs.

---

## 4. CROSS-COMPARISON & RECOMMENDATIONS

### 4.1 Cost per TB Delivered

**Starlink** (2025 model):
- 1TB plan: $290/month = **$290/TB**
- 2TB plan: $540/month = **$270/TB**
- Overage: $125/500GB = **$250/TB**
- **Plus**: $2,500 hardware one-time

**Sneakernet**:
- AWS Snowball: **$3.00-$3.75/TB** (device rental)
- Azure Data Box: **$6.25/TB** (device + processing)
- DIY (with hardware): **$3.32/TB** (amortized)
- DIY (trip only): **$1.58/TB** (excludes hardware)

**Fiber**:
- Not directly comparable (sunk CapEx for infrastructure)
- Amortized cost depends on total data volume and utilization
- Unlimited bandwidth once installed

---

### 4.2 Recommended Default Values for Calculator

#### Starlink

| Parameter | Recommended Value | Confidence | Source |
|-----------|-------------------|------------|--------|
| **Monthly cost (1TB)** | $290/month | High | Official pricing [9] |
| **Monthly cost (2TB)** | $540/month | High | Official pricing [9] |
| **Hardware cost** | $2,500 | High | Business dish [9] |
| **Bandwidth (sustained)** | 150 Mbps | High | Real-world median [151] |
| **Usable TB/month** | 1-2 TB | High | Data bucket limit [8][9] |
| **Overage cost** | $250/TB | High | Calculated from [9] |
| **Overhead factor** | 0.85 | **Low** | **ESTIMATED** |

**Caveat**: Post-2025, Starlink is **not suitable for high-volume data transfer** (>2TB/month) due to data bucket limits and prohibitive overage costs ($250/TB).

#### Sneakernet

| Parameter | Recommended Value | Confidence | Source |
|-----------|-------------------|------------|--------|
| **Cost per mile (DIY)** | $0.70/mile | High | IRS rate [81] |
| **Cost per TB (DIY, amortized)** | $3.32/TB | High | Calculated |
| **Cost per TB (AWS Snowball)** | $3.50/TB | High | AWS pricing [21] |
| **Cost per TB (Azure)** | $6.25/TB | High | Azure pricing [26] |
| **Storage capacity (DIY)** | 120 TB/trip | High | 6× 20TB drives [101] |
| **Storage hardware cost** | $2,080 for 120TB | High | Component pricing [101] |
| **Driver cost** | $30/hour | High | Median wage [127] |

**Note**: DIY sneakernet with open-source NAS software (TrueNAS) offers best $/TB ratio.

#### Fiber

| Parameter | Recommended Value | Confidence | Source |
|-----------|-------------------|------------|--------|
| **Cost per mile (rural aerial)** | $50,000/mile | High | Industry median [45][58] |
| **Cost per mile (rural underground)** | $130,000/mile | Medium | Industry estimate [45] |
| **Cost per mile (blended)** | $70,000/mile | High | Conservative median [58] |
| **Labor component** | 60% of total | High | Industry report [43] |
| **Monthly OpEx** | $300/mile/month | **Low** | **ESTIMATED** |
| **Amortization period** | 7 years | Medium | Industry average |

**Note**: Fiber costs are highly site-specific. Use conservative estimates and obtain local quotes for actual deployments.

---

### 4.3 Break-Even Analysis (Example)

**Scenario**: 10-mile fiber run vs. Starlink vs. Sneakernet for 100TB/month data transfer

**Fiber**:
- CapEx: 10 miles × $70,000 = $700,000
- Monthly OpEx: 10 miles × $300 = $3,000/month
- 7-year TCO: $700,000 + ($3,000 × 84) = $952,000
- Monthly amortized: $11,333/month

**Starlink** (2TB plan + overages):
- Base: $540/month (2TB)
- Overage: 98TB × $250 = $24,500/month
- **Total**: $25,040/month
- 7-year TCO: $25,040 × 84 = **$2,103,360**

**Sneakernet** (DIY, weekly trips):
- Cost per trip: $3.32/TB × 100TB = $332/trip
- Monthly cost: $332 × 4.3 trips = $1,428/month
- 7-year TCO: $1,428 × 84 = **$119,952**

**Finding**: For high-volume data transfer (>10TB/month), **sneakernet is most cost-effective**, followed by fiber (if volume justifies CapEx), with Starlink prohibitively expensive under 2025 pricing model.

---

## 5. DATA GAPS & FUTURE RESEARCH

### 5.1 High-Priority Gaps

1. **Starlink overhead factor**: Need empirical testing to determine actual usable throughput accounting for protocol overhead, retransmissions, and network congestion under 2025 priority data model.

2. **Fiber OpEx breakdown**: Detailed maintenance, monitoring, and operational cost data from fiber providers or utility operators.

3. **Starlink priority data performance under congestion**: How does performance degrade when multiple users exhaust priority data buckets? Impact of 1 Mbps throttling on real-world workflows.

4. **Regional fiber cost variations**: State-by-state or terrain-specific cost multipliers (mountainous vs. flat, rocky vs. soft soil, etc.).

5. **Sneakernet security costs**: Physical security, insurance, and tamper-evident containers for sensitive data transport.

---

### 5.2 Medium-Priority Gaps

6. **Starlink Business multi-terminal discounts**: Pricing for fleets of dishes (not publicly documented).

7. **Fiber maintenance schedules**: Frequency and cost of routine fiber maintenance, repair cycles.

8. **DIY sneakernet software costs** (if not using open-source): Licensing for commercial data transfer/monitoring tools.

9. **Starlink performance in extreme weather**: Impact of snow, heavy rain, high winds on bandwidth and reliability.

10. **Fiber permitting timelines**: How long does permitting take? Impact on deployment schedules.

---

### 5.3 Low-Priority Gaps (Nice to Have)

11. **Starlink future pricing trends**: Will 2025 data bucket model persist or revert to unlimited?

12. **Fiber long-haul vs. last-mile cost ratios**: How much cheaper is long-haul fiber per mile?

13. **Sneakernet carbon footprint**: Environmental impact comparison across transport modes.

---

## 6. METHODOLOGY & SOURCES

### 6.1 Research Approach

**Primary sources prioritized**:
1. Official vendor pricing (Starlink, AWS, Azure)
2. Government data (IRS, EIA, BLS, FCC)
3. Industry reports (ATRI, Fiber Broadband Association, NTCA)
4. Independent testing (PCMag, Ookla, BroadbandNow)

**Secondary sources**:
5. Reddit user reports (cross-referenced when possible)
6. Industry publications (FreightWaves, etc.)

**Data validation**:
- Cross-reference multiple sources
- Prioritize recent data (2024-2025)
- Document confidence levels
- Note regional variations

### 6.2 Currency & Exchange Rates

**All costs in USD** (December 2025 dollars). No currency conversion required for this research (U.S.-focused).

For future international research:
- Document original currency and converted USD
- Note exchange rate and date
- Example: "€500/month (≈$540/month at 1.08 EUR/USD, Dec 2025)"

---

## 7. CONCLUSION

This research provides validated, current-market pricing data for three data connectivity modes relevant to off-grid AI inference deployments:

1. **Starlink**: 2025 pricing model shift to data buckets fundamentally changes economics. No longer viable for high-volume (>2TB/month) data transfer due to $250/TB overage costs. Suitable for remote connectivity where alternatives don't exist, but not cost-effective for bulk data logistics.

2. **Sneakernet**: Most cost-effective solution for bulk data transfer at $1.58-$6.25/TB depending on approach. DIY with open-source NAS software offers best economics. Same-day turnaround possible. Scales well with data volume.

3. **Fiber**: High upfront CapEx ($60,000-$80,000/mile rural) but unlimited bandwidth. Suitable for permanent installations with high sustained data needs. Last-mile rural costs are binding constraint. Requires 5-10 year planning horizon to justify investment.

**Key recommendation**: For off-grid AI inference data logistics, **sneakernet is the optimal solution** for most scenarios, with fiber as a long-term investment for permanent sites with sustained high-volume needs. Starlink is no longer competitive for bulk data transfer under 2025 pricing.

---

## 8. CITATIONS

### Starlink Sources
[1] Starlink Service Plans (official, Dec 2025)  
[8] Metrowireless Starlink 2025 Plan Changes  
[9] OneStopComm Starlink Business Guide  
[11] Concordelectronics Starlink Plan Changes  
[13] Ookla Starlink U.S. Performance 2025  
[14] PCMag Starlink Cost Explainer  
[16] Starlink Official Specifications  
[148] BroadbandNow Starlink Review 2025  
[151] PCMag Starlink 2025 Performance Tests (Multi-Year)  

### Sneakernet Sources
[21] AWS Snowball Pricing (official)  
[25] CloudOptimo AWS Snowball Analysis  
[26] Intellipaat Azure Data Box Overview  
[28] DatacenterDynamics AWS Snowmobile Retirement  
[29] Microsoft Azure Data Box FAQ  
[32] Azure Data Box FAQ (Azure.cn)  
[33] 1310nm.net Google Transfer Appliance  
[35] Azure Data Box Official Pricing  
[81] NerdWallet IRS Mileage Rates 2025  
[83] IRS Newsroom 2025 Mileage Rate  
[101] DiskPrices.com Hard Drive Pricing  
[106] Reddit Seagate Exos 20TB Pricing  
[109] GoHardDrive 20TB Drive Pricing  
[115] eBay Seagate Exos X20 Recertified  
[121] TrueNAS Community Edition (official)  
[124] TrueNAS FreeNAS Evolution  
[125] TrueNAS CORE Overview  
[126] Foxcloud OpenMediaVault  
[127] HMD Trucking Driver Salary 2025  
[130] Geotab Truck Driver Salary Guide  
[133] ZipRecruiter CDL Driver Salary LA  
[161] InsuredBetter Commercial Vehicle Insurance  
[163] MoneyGeek Cheapest Commercial Auto  
[164] Insurify Commercial Auto Average Cost  

### Fiber Sources
[42] 3-GIS Rural vs Urban Fiber Planning  
[43] Fiber Broadband Association 2024 Deployment Cost Report  
[44] BroadbandBreakfast NTCA Middle Mile Costs  
[45] TheNetworkInstallers Fiber Installation Cost 2025  
[47] Conexon Fiber to Every Rural Home  
[48] USTelecom Dig Once Solution  
[49] SatelliteToday Space-Based Last-Mile Race  
[50] CPUC California Broadband Cost Model  
[52] Reddit Networking Fiber Cost Discussion  
[55] RockinState Broadband Expansion Costs  
[58] Ceragon True Costs of Fiber  
[149] Owire Optical Fiber Manufacturing Cost  
[152] DataField Fiber Deployment Cost Factors  
[156] Dgtl Infra Fiber Network Construction Costs  
[166] JXL Fiber Optic Cable Cost Guide  
[171] Aimi Fiber Single-Mode Cable Costs  

### Fuel & Operating Cost Sources
[141] Marca Gas Prices December 2025  
[142] CBS News Gas Prices Below $3  
[143] NPR Thanksgiving Gas Prices  
[145] BTS Motor Fuel Prices November 2025  
[159] Rigzone EIA Diesel Price Projections  
[160] AlamoNews Gas Price Changes  
[168] RioGrandeGuardian Gas/Diesel Prices  
[170] EIA Gasoline and Diesel Fuel Update  
[82] ATRI Operational Costs of Trucking  
[86] Fleetio Trucking Cost Analysis 2025  
[89] FreightWaves Total Cost Per Mile  

---

**End of Research Findings Document**