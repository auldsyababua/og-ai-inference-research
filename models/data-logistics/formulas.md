# DATA LOGISTICS CALCULATOR - FORMULAS

**Version:** 1.1  
**Last Updated:** 2025-12-02  
**Status:** Updated with validated parameters from consolidated research (December 2025)

---

## Input Parameters

| Symbol | Name | Units | Description |
|--------|------|-------|-------------|
| W_in | Workload_Inbound_TB_per_month | TB/month | Inbound data (model weights, training data) |
| W_out | Workload_Outbound_TB_per_month | TB/month | Outbound data (embeddings, results) |
| N_starlink | Starlink_Terminals | count | Number of Starlink terminals |
| C_starlink | Starlink_Cost_per_terminal_per_month | $/month | Monthly cost per Starlink terminal |
| B_starlink | Starlink_Effective_Bandwidth_Mbps | Mbps | Effective bandwidth per terminal (after overhead) |
| η_starlink | Starlink_Overhead_Factor | 0-1 | Usable fraction (accounts for protocol overhead, contention) |
| D_sneakernet | Sneakernet_Distance_miles | miles | One-way distance to site |
| C_sneakernet | Sneakernet_Cost_per_mile | $/mile | Vehicle cost per mile (fuel, maintenance, driver) |
| T_sneakernet | Sneakernet_Trips_per_month | trips/month | Frequency of trips |
| Cap_sneakernet | Sneakernet_TB_per_trip | TB/trip | Storage capacity per trip |
| D_fiber | Fiber_Distance_miles | miles | Distance to Point of Presence (POP) |
| C_fiber | Fiber_Cost_per_mile | $/mile | Fiber build cost per mile |
| Y_fiber | Fiber_Amortization_years | years | Amortization period |
| OpEx_fiber | Fiber_OpEx_per_month | $/month | Ongoing operational costs |

---

## Calculated Outputs

### 1. Total Data Requirement

```
Total_TB_per_month = W_in + W_out
```

**Interpretation:** Total data transfer requirement per month.

**Example:**
- 400 TB inbound + 50 TB outbound = 450 TB/month

---

### 2. Starlink Calculations

#### 2.1 Usable Bandwidth per Terminal

```
Starlink_Usable_TB_per_terminal = (B_starlink × η_starlink × seconds_per_month) / (8 × 10^6)
```

Where:
- `seconds_per_month = 30.44 × 24 × 3600 = 2,629,746 seconds`
- `8 × 10^6` converts Mbps to MB/s, then to TB (divide by 10^6 for TB)

**Simplified:**
```
Starlink_Usable_TB_per_terminal = B_starlink × η_starlink × 2.629746 / 8
```

**Example:**
- 100 Mbps × 0.8 × 2.629746 / 8 = 21.6 TB/month per terminal

#### 2.2 Total Starlink Capacity

```
Starlink_Usable_TB_per_month = N_starlink × Starlink_Usable_TB_per_terminal
```

**Example:**
- 15 terminals × 21.6 TB/month = 324 TB/month

#### 2.3 Starlink Cost

```
Starlink_Total_Cost_per_month = N_starlink × C_starlink
```

```
Starlink_Cost_per_TB = Starlink_Total_Cost_per_month / Total_TB_per_month
```

**Note:** If `Starlink_Usable_TB_per_month < Total_TB_per_month`, then Starlink cannot meet demand and cost/TB is undefined or infinite.

**Example:**
- 15 terminals × $500/month = $7,500/month
- $7,500 ÷ 450 TB = $16.67/TB

---

### 3. Sneakernet Calculations

#### 3.1 Trip Capacity

```
Sneakernet_Total_Capacity_per_month = T_sneakernet × Cap_sneakernet
```

**Example:**
- 4 trips/month × 120 TB/trip = 480 TB/month

#### 3.2 Sneakernet Cost

```
Sneakernet_Cost_per_trip = 2 × D_sneakernet × C_sneakernet
```

(2× for round trip)

```
Sneakernet_Total_Cost_per_month = T_sneakernet × Sneakernet_Cost_per_trip
```

```
Sneakernet_Cost_per_TB = Sneakernet_Total_Cost_per_month / Total_TB_per_month
```

**Example:**
- 2 × 200 miles × $2/mile = $800/trip
- 4 trips × $800 = $3,200/month
- $3,200 ÷ 450 TB = $7.11/TB

**Note:** If `Sneakernet_Total_Capacity_per_month < Total_TB_per_month`, then sneakernet cannot meet demand.

---

### 4. Fiber Calculations

#### 4.1 Capital Expenditure (CapEx)

```
Fiber_Total_CapEx = D_fiber × C_fiber
```

**Example:**
- 10 miles × $30,000/mile = $300,000

#### 4.2 Amortized Monthly CapEx

```
Fiber_Monthly_CapEx_Amortized = Fiber_Total_CapEx / (Y_fiber × 12)
```

**Example:**
- $300,000 ÷ (10 years × 12 months) = $2,500/month

#### 4.3 Total Monthly Cost

```
Fiber_Total_Cost_per_month = Fiber_Monthly_CapEx_Amortized + OpEx_fiber
```

**Example:**
- $2,500 + $500 = $3,000/month

#### 4.4 Cost per TB

```
Fiber_Cost_per_TB = Fiber_Total_Cost_per_month / Total_TB_per_month
```

**Note:** Fiber capacity is effectively unlimited (or very high), so cost/TB decreases with volume.

**Example:**
- $3,000 ÷ 450 TB = $6.67/TB

---

### 5. Mode Recommendation

```
Recommended_Mode = MIN(Starlink_Cost_per_TB, Sneakernet_Cost_per_TB, Fiber_Cost_per_TB)
```

**Logic:**
- Compare cost/TB for all three modes
- Select mode with lowest cost/TB
- If a mode cannot meet capacity requirements, exclude it from comparison

**Excel Formula:**
```
=IF(Starlink_Usable_TB_per_month >= Total_TB_per_month, Starlink_Cost_per_TB, 999999)
=IF(Sneakernet_Total_Capacity_per_month >= Total_TB_per_month, Sneakernet_Cost_per_TB, 999999)
=MIN(Starlink_Cost_per_TB_valid, Sneakernet_Cost_per_TB_valid, Fiber_Cost_per_TB)
```

---

### 6. Cost Savings

```
Cost_Savings_vs_Next_Best = Next_Best_Cost_per_TB - Recommended_Mode_Cost_per_TB
```

**Interpretation:** Monthly savings from choosing optimal mode vs second-best option.

---

## Assumptions & Limitations

1. **Starlink Bandwidth:** Assumes consistent bandwidth availability. Real-world performance varies with weather, satellite coverage, and network congestion.

2. **Sneakernet Capacity:** Assumes fixed storage capacity per trip. Actual capacity depends on drive types and vehicle constraints.

3. **Fiber Capacity:** Assumes unlimited or very high capacity. Real-world fiber may have capacity limits depending on infrastructure.

4. **No Latency Modeling:** Calculator focuses on cost, not latency. Starlink has high latency (~20-40ms), sneakernet has days/weeks latency, fiber has low latency (~1-5ms).

5. **Fixed Costs:** Assumes fixed costs per mode. Real-world costs may vary with volume discounts, seasonal factors, etc.

6. **No Redundancy:** Does not account for redundancy requirements (multiple Starlink terminals for reliability, backup sneakernet routes, etc.).

---

## Default Parameter Values

**⚠️ IMPORTANT:** These are **initial estimates** based on:
1. Example calculations from `docs/GAP_ANALYSIS.md` (Starlink $500/month, Sneakernet $2/mile)
2. General industry knowledge (fiber build costs, bandwidth estimates)
3. **NOT verified with current vendor quotes or recent research**

**These values should be validated before use in production planning.**

### Starlink (2025 Pricing - ✅ VALIDATED)

**✅ UPDATED:** Parameters validated from consolidated research (December 2025)

- **Cost per terminal (Local Priority 1TB):** $290/month
  - **Source:** Official Starlink pricing, December 2025 (`research/data-logistics/CONSOLIDATED-SUMMARY.md`)
  - **Status:** ✅ **HIGH CONFIDENCE** - All sources agree
  - **Alternative:** $540/month for 2TB plan
- **Cost per terminal (Local Priority 2TB):** $540/month
  - **Source:** Official Starlink pricing, December 2025
  - **Status:** ✅ **HIGH CONFIDENCE** - All sources agree
- **Hardware cost:** $349 (standard) or $2,500 (high-performance kit)
  - **Source:** Official Starlink pricing
  - **Status:** ✅ **HIGH CONFIDENCE**
- **Overage rate:** $0.50/GB ($250/TB) after priority data exhausted
  - **Source:** Official Starlink pricing
  - **Status:** ✅ **HIGH CONFIDENCE** - All sources agree
- **Effective bandwidth:** 100-150 Mbps per terminal (sustained, real-world median)
  - **Source:** Ookla Speedtest data Q1 2025 (`research/data-logistics/CONSOLIDATED-SUMMARY.md`)
  - **Status:** ✅ **HIGH CONFIDENCE** - Validated from independent testing
- **Overhead factor (TCP):** 0.60 (conservative) to 0.85 (optimized)
  - **Source:** Protocol analysis - TCP congestion collapse during 15-second satellite handovers
  - **Status:** ⚠️ **MEDIUM CONFIDENCE** - Disagreement exists (Claude: 0.60, Gemini/Perplexity: 0.85)
  - **Recommendation:** Use 0.60 for conservative design, 0.75-0.80 for optimized TCP (Rclone multi-stream)
- **Overhead factor (UDP-accelerated):** 0.90
  - **Source:** Protocol analysis - UDP-based transfers achieve near-line speed
  - **Status:** ✅ **MEDIUM-HIGH CONFIDENCE** - All sources agree
- **Throttle speed:** 1 Mbps (download) / 0.5 Mbps (upload) after priority data exhausted
  - **Source:** Official Starlink policy
  - **Status:** ✅ **HIGH CONFIDENCE** - All sources agree

**⚠️ CRITICAL FINDING:** 2025 pricing model fundamentally changes Starlink economics:
- **Before 2025:** Unlimited plans available
- **After 2025:** Data buckets with hard throttling (1 Mbps post-cap)
- **Impact:** Overage costs ($250-$500/TB) make Starlink prohibitively expensive for high-volume data transfer (>2TB/month)
- **Recommendation:** Starlink suitable for low-bandwidth control plane (<2TB/month), NOT for bulk data transfer

### Sneakernet (✅ VALIDATED)

**✅ UPDATED:** Parameters validated from consolidated research (December 2025)

- **Vehicle cost per mile:** $0.70/mile (IRS standard rate)
  - **Source:** IRS Notice 2025-05 (`research/data-logistics/CONSOLIDATED-SUMMARY.md`)
  - **Status:** ✅ **HIGH CONFIDENCE** - Official IRS rate, covers fuel, maintenance, insurance, depreciation
- **Driver labor cost:** $0.30-$0.50/mile ($25-$30/hour at 60 mph)
  - **Source:** BLS wage data, December 2025
  - **Status:** ✅ **MEDIUM CONFIDENCE** - Varies by region and driver type
- **Total cost per mile:** $1.00-$1.20/mile (vehicle + driver)
  - **Source:** Calculated from validated components
  - **Status:** ✅ **MEDIUM-HIGH CONFIDENCE**
- **Storage per trip:** 120 TB (6× 20TB drives with RAID-Z2)
  - **Source:** Component pricing analysis (`research/data-logistics/CONSOLIDATED-SUMMARY.md`)
  - **Status:** ✅ **HIGH CONFIDENCE** - Validated from drive specifications
- **Storage cost:** $13-$15/TB (new enterprise drives, Seagate Exos 20TB)
  - **Source:** Retail pricing, December 2025
  - **Status:** ✅ **HIGH CONFIDENCE** - Current market pricing
- **DIY NAS build cost:** $2,000-$3,200 for 120TB capacity
  - **Source:** Component pricing analysis
  - **Status:** ✅ **HIGH CONFIDENCE** - Well-documented component costs
- **Commercial providers:**
  - **AWS Snowball:** $300/10 days (80TB) - ⚠️ **No longer available to new customers** (Nov 2025)
  - **Azure Data Box:** $250/10 days (80TB) - ✅ Available
  - **Google Transfer Appliance:** $1,800 (300TB) - ✅ Available
  - **Backblaze Fireball:** $550/month (96TB) - ✅ Available
  - **Source:** Official provider pricing, December 2025
  - **Status:** ✅ **HIGH CONFIDENCE** - All sources agree

**Key Finding:** DIY sneakernet offers **10-50x cost advantage** over Starlink at scale ($1.50-$3.50/TB vs $250-$500/TB)

### Fiber (✅ PARTIALLY VALIDATED)

**✅ UPDATED:** Parameters validated from consolidated research (December 2025)

- **Cost per mile (Aerial):** $40,000-$60,000/mile (median $50,000/mile)
  - **Source:** Fiber Broadband Association 2024 Annual Report (`research/data-logistics/CONSOLIDATED-SUMMARY.md`)
  - **Status:** ✅ **HIGH CONFIDENCE** - Multiple industry sources agree
- **Cost per mile (Underground Rural):** $60,000-$150,000/mile (median $70,000-$96,000/mile)
  - **Source:** Industry reports, 2023-2025 data
  - **Status:** ✅ **HIGH CONFIDENCE** - Strong consensus
- **Cost per mile (Underground Rocky):** $100,000-$200,000/mile (median $150,000/mile)
  - **Source:** Industry reports
  - **Status:** ✅ **HIGH CONFIDENCE** - All sources agree
- **Labor component:** 60-80% of total cost (median 70%)
  - **Source:** Industry reports
  - **Status:** ✅ **HIGH CONFIDENCE** - All sources agree
- **Make-ready costs (Aerial):** $10,000-$30,000/mile (median $15,000/mile)
  - **Source:** Industry reports
  - **Status:** ✅ **HIGH CONFIDENCE** - All sources agree
- **Amortization period:** 20 years (private deployments), 25 years (public/utility)
  - **Source:** Industry standards, IRS guidelines
  - **Status:** ✅ **MEDIUM CONFIDENCE** - Varies by financing structure (5-30 years range)
- **Annual OpEx:** $500-$3,800 per mile per year (median $2,500/mile/year)
  - **Source:** Industry estimates (`research/data-logistics/CONSOLIDATED-SUMMARY.md`)
  - **Status:** ⚠️ **LOW CONFIDENCE** - Wide variation, limited public data
  - **Monthly OpEx:** $42-$317 per mile per month (median $208/mile/month)
  - **Recommendation:** Use $2,500/mile/year ($208/month) with LOW confidence, obtain site-specific quotes

**⚠️ CRITICAL:** Fiber costs are highly site-specific:
- **Terrain:** Rocky terrain can double costs vs. soft soil
- **Existing infrastructure:** Aerial overlashing cheaper if poles available
- **Regional variations:** Labor costs vary significantly by region
- **Action Required:** Obtain site-specific quotes for actual deployments

---

## References

- PRD Section 3.5: Data Logistics Modeling requirements
- Gap Analysis Section 6: Data Logistics Modeling Gaps (contains example calculations, not verified research)
- **Missing:** Actual Starlink Business/Enterprise pricing research
- **Missing:** Actual fiber build cost research or quotes
- **Missing:** Actual sneakernet cost validation for target deployment regions

## Research Gaps

**✅ UPDATED:** Most parameters now validated. Remaining gaps:

1. **Starlink TCP Overhead Factor** ⚠️ **MEDIUM PRIORITY**
   - **Status:** Disagreement exists (0.60 vs 0.85)
   - **Resolution Needed:** Empirical testing of Starlink TCP performance during satellite handovers
   - **Recommendation:** Use 0.60 for conservative design, 0.75-0.80 for optimized TCP

2. **Fiber OpEx** ⚠️ **HIGH PRIORITY**
   - **Status:** Wide variation ($500-$3,800/mile/year)
   - **Resolution Needed:** Direct quotes from fiber providers or utility operators
   - **Recommendation:** Use $2,500/mile/year with LOW confidence, obtain site-specific quotes

3. **Regional Fiber Cost Variations** ⚠️ **MEDIUM PRIORITY**
   - **Status:** Limited data for Eastern Europe (Romania) and other regions
   - **Resolution Needed:** Regional cost studies or local contractor quotes
   - **Recommendation:** Use US pricing as proxy, adjust for known labor cost differentials

4. **DIY Sneakernet Security Costs** ⚠️ **LOW PRIORITY**
   - **Status:** Not addressed in research
   - **Resolution Needed:** Physical security, insurance, tamper-evident containers
   - **Recommendation:** Add 10-20% overhead for security measures

---

## Future Enhancements

Planned additions for v2:
- Latency modeling
- Redundancy requirements
- Volume discount modeling
- Multi-mode hybrid strategies (e.g., Starlink + Sneakernet)
- Regional cost variations
- Time-of-day bandwidth variations (Starlink)

