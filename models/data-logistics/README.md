# DATA LOGISTICS CALCULATOR

**Version:** 1.1  
**Last Updated:** 2025-12-02  
**Status:** Working prototype with validated 2025 pricing parameters

---

## Purpose

Calculate and compare data transfer costs for off-grid AI inference deployments using three connectivity modes: Starlink satellite, Sneakernet (physical transport), and Fiber build. Determines the most cost-effective mode based on data volume, distance, and cost parameters.

---

## Quick Start Guide

### Step 1: Open Calculator
Open the CSV file in Excel, Google Sheets, or any spreadsheet application:
```
models/data-logistics/DataLogistics-v1.csv
```

### Step 2: Configure Scenario

**Workload Requirements:**
- `Workload_Inbound_TB_per_month` - Inbound data (model weights, training data)
- `Workload_Outbound_TB_per_month` - Outbound data (embeddings, results)
- `Total_TB_per_month` - **Formula:** `=B2+C2` (column B = inbound, column C = outbound)

**Starlink Configuration:**
- `Starlink_Terminals` - Number of terminals
- `Starlink_Cost_per_terminal_per_month` - Monthly cost per terminal ($290 for 1TB plan, $540 for 2TB plan)
- `Starlink_Effective_Bandwidth_Mbps` - Effective bandwidth per terminal (100-150 Mbps sustained, real-world median)
- `Starlink_Overhead_Factor` - Usable fraction after overhead (0.60 for TCP conservative, 0.90 for UDP-accelerated)

**Sneakernet Configuration:**
- `Sneakernet_Distance_miles` - One-way distance to site
- `Sneakernet_Cost_per_mile` - Vehicle cost per mile ($0.70 IRS rate + $0.30-$0.50 driver labor = $1.00-$1.20 total)
- `Sneakernet_Trips_per_month` - Frequency of trips
- `Sneakernet_TB_per_trip` - Storage capacity per trip (120 TB typical with 6× 20TB drives, RAID-Z2)

**Fiber Configuration:**
- `Fiber_Distance_miles` - Distance to Point of Presence (POP)
- `Fiber_Cost_per_mile` - Build cost per mile ($50,000 aerial, $70,000-$96,000 underground rural, $150,000 rocky terrain)
- `Fiber_Amortization_years` - Amortization period (20 years typical for private deployments)
- `Fiber_OpEx_per_month` - Ongoing operational costs ($208/month per mile = $2,500/year, LOW confidence - obtain site-specific quotes)

### Step 3: Review Outputs

**Starlink:**
- `Starlink_Usable_TB_per_month` - **Formula:** `=D2*H2*I2*2.629746/8` (terminals × bandwidth × overhead × conversion)
- `Starlink_Total_Cost_per_month` - **Formula:** `=D2*E2` (terminals × cost per terminal)
- `Starlink_Cost_per_TB` - **Formula:** `=IF(I2>=D2, J2/D2, 999999)` (total cost ÷ total TB, or 999999 if capacity insufficient)

**Sneakernet:**
- `Sneakernet_Total_Cost_per_month` - **Formula:** `=N2*2*L2*M2` (trips × round trip × distance × cost per mile)
- `Sneakernet_Cost_per_TB` - **Formula:** `=IF(O2*P2>=D2, Q2/D2, 999999)` (total cost ÷ total TB, or 999999 if capacity insufficient)

**Fiber:**
- `Fiber_Total_CapEx` - **Formula:** `=R2*S2` (distance × cost per mile)
- `Fiber_Monthly_CapEx_Amortized` - **Formula:** `=U2/(T2*12)` (CapEx ÷ amortization years ÷ 12)
- `Fiber_Total_Cost_per_month` - **Formula:** `=V2+W2` (amortized CapEx + OpEx)
- `Fiber_Cost_per_TB` - **Formula:** `=W2/D2` (total cost ÷ total TB)

**Recommendation:**
- `Recommended_Mode` - **Formula:** `=IF(MIN(K2,Q2,X2)=K2,"Starlink",IF(MIN(K2,Q2,X2)=Q2,"Sneakernet","Fiber"))` (lowest cost option)
- `Cost_Savings_vs_Next_Best` - **Formula:** `=LARGE({K2,Q2,X2},2)-MIN(K2,Q2,X2)` (second-best cost - best cost)

**Note:** Column references assume:
- Row 2 = first data row (after header)
- Column D = Total_TB_per_month (calculated)
- Column K = Starlink_Cost_per_TB
- Column Q = Sneakernet_Cost_per_TB  
- Column X = Fiber_Cost_per_TB

See `EXCEL-FORMULAS.md` for complete column mapping and formula reference.

---

## Example Scenarios (✅ **UPDATED with 2025 validated pricing**)

### Scenario 1: High Volume, Close Site (Example_100TB_Week)
- **Workload:** 450 TB/month (400 inbound + 50 outbound)
- **Distance:** 200 miles
- **Starlink:** $290/month (1TB plan) × 15 terminals = $4,350/month = $9.67/TB (⚠️ **Cannot meet demand** - only 197 TB capacity with 15 terminals)
- **Sneakernet:** $1.20/mile × 200 miles × 2 (round trip) × 4 trips = $1,920/month = $4.27/TB
- **Fiber:** $50,000/mile × 10 miles ÷ 20 years ÷ 12 months + $208/month = $2,291/month = $5.09/TB
- **Result:** Sneakernet wins at $2.13/TB (updated with validated 2025 pricing)
- **Note:** Starlink cannot meet demand due to 2025 data bucket limits (max 2TB per terminal)

### Scenario 2: Low Volume (Low_Volume_10TB_Month)
- **Workload:** 11 TB/month
- **Starlink:** $290/month (1TB plan) = $26.36/TB ✅ **Can meet demand**
- **Sneakernet:** $240/month (1 trip) = $21.82/TB
- **Fiber:** $2,291/month = $208.27/TB (high fixed cost amortized over low volume)
- **Result:** Sneakernet wins at $21.82/TB (updated with validated 2025 pricing)
- **Note:** For very low volumes, Sneakernet is most economical

### Scenario 3: Medium Volume (Medium_Volume_100TB_Month)
- **Workload:** 110 TB/month
- **Starlink:** $290/month × 4 terminals = $1,160/month = $10.55/TB (⚠️ **Cannot meet demand** - only 52.6 TB capacity)
- **Sneakernet:** $240/month (1 trip) = $2.18/TB ✅ **Can meet demand**
- **Fiber:** $2,291/month = $20.83/TB
- **Result:** Sneakernet wins at $2.18/TB (updated with validated 2025 pricing)

### Scenario 4: Very High Volume (Very_High_Volume_500TB_Month)
- **Workload:** 550 TB/month
- **Starlink:** $290/month × 20 terminals = $5,800/month = $10.55/TB (⚠️ **Cannot meet demand** - only 262.8 TB capacity)
- **Sneakernet:** $1,200/month (5 trips) = $2.18/TB ✅ **Can meet demand**
- **Fiber:** $2,291/month = $4.17/TB
- **Result:** Sneakernet wins at $2.18/TB (updated with validated 2025 pricing)
- **Note:** At high volumes, Sneakernet remains cost-effective; Fiber requires higher volume to justify CapEx

**⚠️ Critical Finding:** With 2025 Starlink pricing (data bucket model), Starlink cannot meet high-volume demands (>2TB/month per terminal) due to hard throttling to 1 Mbps after priority data exhausted. Sneakernet is optimal for most scenarios.

---

## Formulas

See: `formulas.md` for detailed formula documentation

---

## Key Insights

### Break-Even Analysis (✅ **UPDATED with 2025 pricing**)

**Starlink vs Sneakernet:**
- ⚠️ **2025 Pricing Impact:** Starlink data bucket model limits capacity to 1-2 TB/month per terminal
- **Low volume (<2TB/month):** Starlink competitive ($26.36/TB for 11 TB/month)
- **Medium-high volume (>2TB/month):** Sneakernet wins ($1.50-$3.50/TB vs Starlink $250-$500/TB overage)
- **Break-even:** ~1TB/month (Starlink becomes prohibitively expensive due to overage costs)

**Fiber vs Others:**
- Fiber requires high upfront investment ($50,000-$150,000/mile) but becomes cost-effective at high volumes
- **Break-even vs Starlink:** ~50-100 TB/month (Starlink cannot meet demand at higher volumes)
- **Break-even vs Sneakernet:** ~500-1,000 TB/month (depends on distance and amortization)
- For 10-mile build: Break-even typically at 200-500 TB/month vs Sneakernet
- For 50-mile build: Break-even typically at 1,000+ TB/month vs Sneakernet

**Sneakernet vs Fiber:**
- Sneakernet wins for low-to-medium volumes (<500 TB/month) and short distances (<100 miles)
- Fiber wins for high volumes (>500 TB/month) regardless of distance (after amortization)
- **Key Finding:** DIY Sneakernet offers 10-50x cost advantage over Starlink at scale

---

## Limitations

**Current Version (v1) does NOT include:**
- Latency modeling (Starlink: 20-40ms, Sneakernet: days/weeks, Fiber: 1-5ms)
- Redundancy requirements (multiple terminals, backup routes)
- Volume discounts (Starlink, fiber providers may offer discounts)
- Time-of-day bandwidth variations (Starlink performance varies)
- Regional cost variations (fiber costs vary by terrain, regulations)
- Multi-mode hybrid strategies (e.g., Starlink for real-time + Sneakernet for bulk)

---

## Parameter Validation

**✅ UPDATED:** Default parameter values are now **validated from consolidated research** (December 2025):

1. **Starlink:** ✅ **VALIDATED**
   - $290/month (1TB plan) and $540/month (2TB plan) from official Starlink pricing (December 2025)
   - 100-150 Mbps sustained bandwidth from Ookla Speedtest data (Q1 2025)
   - Overhead factor: 0.60 (TCP conservative) or 0.90 (UDP-accelerated) from protocol analysis
   - **Source:** `research/data-logistics/CONSOLIDATED-SUMMARY.md`
   - **Note:** 2025 pricing model uses data buckets with 1 Mbps throttling after cap - not suitable for high-volume (>2TB/month) data transfer

2. **Sneakernet:** ✅ **VALIDATED**
   - $0.70/mile (IRS standard rate) + $0.30-$0.50/mile (driver labor) = $1.00-$1.20 total
   - 120 TB/trip validated (6× 20TB drives with RAID-Z2)
   - Storage cost: $13-$15/TB (new enterprise drives)
   - **Source:** `research/data-logistics/CONSOLIDATED-SUMMARY.md`
   - **Note:** AWS Snowball no longer available to new customers (Nov 2025) - use Azure Data Box or DIY

3. **Fiber:** ✅ **PARTIALLY VALIDATED**
   - $50,000/mile (aerial) and $70,000-$96,000/mile (underground rural) from industry reports
   - OpEx: $2,500/mile/year (LOW confidence - wide variation $500-$3,800/year)
   - **Source:** `research/data-logistics/CONSOLIDATED-SUMMARY.md`
   - **Action Required:** Obtain site-specific quotes for actual deployments (terrain-dependent)

**See `formulas.md` Section "Default Parameter Values" for detailed source attribution and remaining research gaps.**

---

## Troubleshooting

### Common Issues

**Issue: Starlink cost/TB seems very high**
- **Cause:** May need more terminals to meet capacity requirements
- **Solution:** Increase `Starlink_Terminals` until `Starlink_Usable_TB_per_month >= Total_TB_per_month`

**Issue: Fiber cost/TB is very high for low volumes**
- **Cause:** Fixed CapEx amortized over small volume
- **Solution:** This is expected - consider Starlink or Sneakernet for low volumes

**Issue: Sneakernet cannot meet capacity**
- **Cause:** `Sneakernet_Trips_per_month × Sneakernet_TB_per_trip < Total_TB_per_month`
- **Solution:** Increase trip frequency or storage capacity per trip

**Issue: Recommended mode doesn't make sense**
- **Cause:** Check that all modes can meet capacity requirements
- **Solution:** Verify `Starlink_Usable_TB_per_month` and `Sneakernet_Total_Capacity_per_month` are sufficient

---

## References

- `docs/PRD.md` - Section 3.5: Data Logistics Modeling requirements
- `docs/GAP_ANALYSIS.md` - Section 6: Data Logistics Modeling Gaps
- `formulas.md` - Detailed formula documentation
- `docs/GLOSSARY.md` - Standardized terminology

---

## Future Enhancements

See `formulas.md` for planned v2 enhancements.

