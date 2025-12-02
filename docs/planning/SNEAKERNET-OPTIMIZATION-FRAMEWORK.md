# Sneakernet Optimization Framework

**Version:** 1.0  
**Last Updated:** 2025-12-02  
**Purpose:** Comprehensive framework for optimizing physical data transport (sneakernet) operations for off-grid AI inference deployments

---

## Executive Summary

Sneakernet optimization requires balancing multiple factors: **distance to fiber POP**, **route reliability**, **storage capacity**, **transfer efficiency**, **security**, and **operational costs**. This framework provides a systematic approach to designing and operating an efficient sneakernet system.

**Key Optimization Strategy:** Minimize total cost per TB by:
1. Finding the nearest fiber POP (Point of Presence)
2. Maximizing storage capacity per trip
3. Optimizing trip frequency vs. storage costs
4. Ensuring reliable, secure transport
5. Minimizing transfer time at endpoints

---

## 1. Fiber POP Location Analysis

### 1.1 Finding the Nearest Fiber POP

**Objective:** Minimize drive distance while ensuring reliable high-speed data transfer capability.

**Key Considerations:**

1. **POP Identification:**
   - **Data Centers:** Major cloud providers (AWS, Azure, GCP) have regional data centers
   - **Internet Exchange Points (IXPs):** Carrier-neutral facilities with multiple providers
   - **ISP Hubs:** Regional fiber hubs operated by major ISPs
   - **Colocation Facilities:** Shared data center facilities with multiple connectivity options

2. **POP Selection Criteria:**
   - **Distance:** Primary factor - minimize drive time
   - **Ingress Speed:** Must support fast data upload (10 Gbps+ preferred)
   - **Egress Speed:** For model downloads, must support fast download
   - **Availability:** 24/7 access or scheduled access windows
   - **Cost:** Ingress/egress fees, colocation costs if needed
   - **Reliability:** Uptime guarantees, redundant connectivity

3. **Distance vs. Cost Trade-off:**
   - **Short distance (<50 miles):** Lower fuel costs, faster turnaround, more frequent trips possible
   - **Medium distance (50-200 miles):** Balance between distance and POP availability
   - **Long distance (>200 miles):** Higher costs, longer turnaround, but may be only option

**Recommendation:** Use **FCC Broadband Map** or **ISP coverage maps** to identify nearest fiber POP. Contact local ISPs for exact POP locations and access requirements.

---

## 2. Route Planning & Reliability

### 2.1 Route Selection

**Factors to Consider:**

1. **Road Conditions:**
   - **Paved vs. Unpaved:** Unpaved roads increase wear, reduce speed, risk damage to equipment
   - **Seasonal Accessibility:** Mountain passes, rural roads may be impassable in winter
   - **Weight Restrictions:** Bridges, rural roads may have weight limits
   - **Maintenance Status:** Poorly maintained roads increase vehicle wear

2. **Distance & Time:**
   - **One-way distance:** Directly impacts fuel and driver costs
   - **Drive time:** Affects driver fatigue, scheduling flexibility
   - **Traffic patterns:** Urban routes may have congestion delays
   - **Rest stops:** Long routes require driver breaks (DOT regulations)

3. **Reliability Factors:**
   - **Weather dependency:** Snow, flooding, extreme heat can delay or prevent trips
   - **Road closures:** Construction, accidents, seasonal closures
   - **Alternative routes:** Backup routes if primary route is blocked
   - **Emergency services:** Cell coverage, tow truck availability

**Recommendation:** Map multiple route options, test routes under different conditions, maintain backup routes.

---

## 3. Storage Capacity Optimization

### 3.1 Maximizing Data per Trip

**Current Capacity (Validated):**
- **DIY NAS:** 120 TB usable (6× 20TB drives, RAID-Z2)
- **Commercial:** 80-300 TB (Azure Data Box, Google Transfer Appliance)

**Optimization Strategies:**

1. **Increase Drive Density:**
   - **22TB drives:** Available but higher $/TB ($16-19/TB vs $13-15/TB for 20TB)
   - **24TB drives:** Emerging, premium pricing
   - **Multiple NAS units:** 2-3 NAS units per vehicle (240-360 TB total)

2. **Vehicle Capacity Constraints:**
   - **Cargo van:** ~500-600 cu ft cargo space
   - **Weight limits:** GVWR (Gross Vehicle Weight Rating) typically 8,500-10,000 lbs
   - **Power requirements:** NAS units need 110V AC power for data transfer
   - **Cooling:** Multiple NAS units generate heat, need ventilation

3. **Cost per TB Optimization:**
   - **Storage hardware:** $2,000-$3,200 for 120TB system
   - **Amortization:** Spread cost over multiple trips (10-20 trips typical)
   - **Break-even:** Hardware pays for itself after 5-6 trips vs. commercial rental

**Recommendation:** Start with 120TB capacity, scale to 240-360TB if volume justifies additional hardware investment.

---

## 4. Transfer Efficiency

### 4.1 Endpoint Transfer Speed

**Critical Factor:** Time spent transferring data at endpoints directly impacts operational efficiency.

**Considerations:**

1. **Source Site (Off-Grid):**
   - **Network speed:** Local network must support fast transfer to NAS
   - **10GbE preferred:** Minimize transfer time for large datasets
   - **Transfer time:** 120TB at 10 Gbps = ~27 hours (theoretical), ~40-50 hours (realistic with overhead)
   - **Scheduling:** Transfer during off-peak hours if power-constrained

2. **Destination POP:**
   - **Ingress speed:** POP must support fast upload (10 Gbps+ preferred)
   - **Colocation space:** May need to rent rack space for NAS during transfer
   - **Transfer time:** Same as source - 40-50 hours for 120TB
   - **Verification:** Checksum verification adds time but critical for data integrity

3. **Transfer Optimization:**
   - **Parallel transfers:** Multiple NAS units can transfer simultaneously
   - **Incremental sync:** Only transfer changed data (rsync, rclone)
   - **Compression:** May reduce transfer time if CPU-bound (rare for large files)
   - **Deduplication:** Identify duplicate data before transfer

**Recommendation:** Plan for **2-3 days** total transfer time (source + destination) for 120TB. Use parallel NAS units to reduce time.

---

## 5. Security Considerations

### 5.1 Physical Security

**Risks:**
- **Theft:** Vehicle and storage equipment are valuable targets
- **Tampering:** Data could be accessed or modified during transport
- **Loss:** Vehicle accident, equipment failure, natural disaster

**Mitigation Strategies:**

1. **Encryption:**
   - **At-rest encryption:** ZFS native encryption, LUKS, BitLocker
   - **Key management:** Secure key storage, separate from data
   - **Verification:** Checksums to detect tampering

2. **Physical Security:**
   - **Tamper-evident seals:** Detect if equipment was accessed
   - **Locked enclosures:** Secure NAS units in locked racks/cages
   - **GPS tracking:** Track vehicle location in real-time
   - **Insurance:** Commercial cargo insurance for equipment and data

3. **Operational Security:**
   - **Driver background checks:** Trusted personnel only
   - **Route confidentiality:** Don't publicize routes or schedules
   - **Escort:** Consider security escort for high-value shipments
   - **Backup:** Multiple copies, staggered shipments

**Recommendation:** Implement **full-disk encryption** (ZFS encryption or LUKS), **GPS tracking**, and **commercial cargo insurance**. Add 10-20% overhead to costs for security measures.

---

## 6. Operational Considerations

### 6.1 Trip Frequency Optimization

**Trade-off:** More frequent trips = lower storage requirements but higher operational costs.

**Factors:**

1. **Data Generation Rate:**
   - **Daily generation:** Determines minimum trip frequency
   - **Bursty workloads:** May require flexible scheduling
   - **Peak periods:** Schedule trips during high-generation periods

2. **Storage Capacity:**
   - **On-site storage:** Limited by available space, power, cooling
   - **Overflow handling:** What happens when on-site storage fills?
   - **Buffer capacity:** Maintain buffer for unexpected delays

3. **Cost Optimization:**
   - **Fixed costs:** Vehicle lease, driver salary (if full-time)
   - **Variable costs:** Fuel, maintenance, per-trip costs
   - **Break-even:** Find optimal trip frequency that minimizes total cost

**Recommendation:** Start with **weekly trips**, adjust based on data generation rate and storage capacity.

---

### 6.2 Driver & Vehicle Management

**Considerations:**

1. **Driver Options:**
   - **Full-time employee:** Higher cost but dedicated, reliable
   - **Part-time/contractor:** Lower cost, flexible scheduling
   - **Third-party courier:** FedEx Custom Critical, specialized data transport
   - **Self-service:** Site personnel drive (if feasible)

2. **Vehicle Selection:**
   - **Cargo van:** Ford Transit, Ram ProMaster (optimal for NAS transport)
   - **Lease vs. Purchase:** Lease provides flexibility, purchase reduces long-term costs
   - **Backup vehicle:** Critical for reliability - what if primary vehicle breaks down?

3. **Maintenance & Reliability:**
   - **Preventive maintenance:** Regular service to prevent breakdowns
   - **Roadside assistance:** AAA, commercial towing insurance
   - **Spare parts:** Critical components (tires, battery) on-site
   - **Vehicle tracking:** GPS for route optimization and security

**Recommendation:** Use **full-time driver** for reliability, **lease vehicle** for flexibility, maintain **backup vehicle** or **backup route** (third-party courier).

---

## 7. Cost Optimization Model

### 7.1 Total Cost Components

**Per-Trip Costs:**
- **Vehicle:** $0.70/mile (IRS rate) × distance × 2 (round trip)
- **Driver:** $0.30-$0.50/mile ($25-$30/hour at 60 mph)
- **Fuel:** Included in IRS rate
- **Maintenance:** Included in IRS rate
- **Storage hardware amortization:** $2,000-$3,200 ÷ 10-20 trips = $100-$320/trip
- **Security:** 10-20% overhead = $50-$200/trip
- **POP access fees:** Variable (may be $0 if using cloud provider ingress)

**Monthly Costs:**
- **Vehicle lease:** $800-$1,100/month (if leased)
- **Driver salary:** $3,000-$5,000/month (if full-time)
- **Storage hardware:** One-time cost, amortized
- **POP colocation:** $100-$500/month (if renting rack space)

**Cost per TB (Example - 200 miles, 120TB):**
- **Trip cost:** ($0.70 + $0.40) × 200 × 2 = $440
- **Hardware amortization:** $200/trip (10-trip amortization)
- **Security overhead:** $64 (15%)
- **Total per trip:** $704
- **Cost per TB:** $704 ÷ 120TB = **$5.87/TB**

**Optimization:** Increase capacity to 240TB (2 NAS units) reduces cost to **$3.50/TB** (hardware cost doubles but capacity doubles).

---

## 8. Reliability & Redundancy

### 8.1 Failure Modes & Mitigation

**Failure Modes:**

1. **Vehicle Breakdown:**
   - **Mitigation:** Preventive maintenance, roadside assistance, backup vehicle
   - **Impact:** Delayed data transfer, potential data loss if on-site storage fills

2. **Storage Hardware Failure:**
   - **Mitigation:** RAID-Z2 (tolerates 2 drive failures), spare drives, multiple NAS units
   - **Impact:** Data loss if >2 drives fail simultaneously (low probability)

3. **Route Blockage:**
   - **Mitigation:** Backup routes, flexible scheduling, third-party courier backup
   - **Impact:** Delayed transfer, potential data loss

4. **POP Access Issues:**
   - **Mitigation:** Multiple POP options, scheduled access windows, backup cloud providers
   - **Impact:** Delayed transfer, potential data loss

**Recommendation:** Maintain **2x redundancy** - two NAS units per trip, backup vehicle or courier option, multiple POP access points.

---

## 9. Integration with Data Generation

### 9.1 Scheduling Optimization

**Considerations:**

1. **Data Generation Patterns:**
   - **Continuous:** Steady data generation requires regular trips
   - **Bursty:** Large batches require flexible scheduling
   - **Predictable:** Scheduled workloads allow optimized trip timing

2. **Transfer Windows:**
   - **Source site:** Transfer during off-peak power periods if power-constrained
   - **Destination POP:** Schedule during POP off-peak hours (may reduce costs)
   - **Driver availability:** Coordinate with driver schedule

3. **Buffer Management:**
   - **On-site buffer:** Maintain 2-3x trip capacity buffer for delays
   - **Overflow handling:** What happens when buffer fills? (May need emergency trips)
   - **Priority data:** Identify critical data that must be transferred immediately

**Recommendation:** Use **predictive scheduling** based on data generation rate, maintain **2-3x buffer capacity**, implement **priority queuing** for critical data.

---

## 10. Regulatory & Compliance

### 10.1 Cross-Border Considerations

**If crossing international borders:**

1. **Customs:**
   - **Data declaration:** May need to declare data storage devices
   - **Duty/taxes:** Equipment may be subject to import/export duties
   - **Documentation:** Commercial invoices, export licenses if required

2. **Data Privacy:**
   - **GDPR (EU):** Personal data subject to strict regulations
   - **Data localization:** Some countries require data to remain in-country
   - **Encryption requirements:** Some countries restrict encryption

3. **Equipment Regulations:**
   - **Radio equipment:** NAS units with Wi-Fi may require FCC/CE certification
   - **Power equipment:** Voltage converters, power supplies may need certification

**Recommendation:** Consult with **legal counsel** and **customs broker** before implementing cross-border sneakernet. Consider **data residency requirements** and **encryption regulations**.

---

## 11. Monitoring & Verification

### 11.1 Data Integrity

**Critical:** Ensure data is transferred correctly and completely.

**Verification Methods:**

1. **Checksums:**
   - **MD5/SHA-256:** File-level checksums
   - **ZFS checksums:** Block-level checksums (automatic)
   - **Transfer verification:** Compare checksums before/after transfer

2. **Transfer Logs:**
   - **rsync logs:** Detailed transfer logs with verification
   - **rclone logs:** Transfer progress and verification
   - **ZFS send/receive:** Built-in verification

3. **Monitoring:**
   - **Transfer progress:** Real-time monitoring of transfer speed
   - **Error detection:** Automatic retry on errors
   - **Completion verification:** Confirm all data transferred successfully

**Recommendation:** Use **ZFS send/receive** or **rsync with checksums** for automatic verification. Maintain **transfer logs** for audit trail.

---

## 12. Optimization Checklist

### 12.1 Pre-Deployment

- [ ] **Identify nearest fiber POP** (use FCC Broadband Map, ISP coverage maps)
- [ ] **Map route options** (primary + backup routes)
- [ ] **Test routes** under different conditions (weather, traffic)
- [ ] **Calculate optimal storage capacity** (120TB vs 240TB vs 360TB)
- [ ] **Select vehicle** (cargo van, lease vs purchase)
- [ ] **Plan driver strategy** (full-time vs contractor vs third-party)
- [ ] **Design security measures** (encryption, tracking, insurance)
- [ ] **Identify POP access requirements** (colocation, ingress fees, scheduling)
- [ ] **Plan transfer windows** (source site + destination POP)
- [ ] **Establish monitoring** (GPS tracking, transfer verification)

### 12.2 Operational

- [ ] **Schedule trips** based on data generation rate
- [ ] **Maintain buffer capacity** (2-3x trip capacity)
- [ ] **Monitor transfer progress** (real-time verification)
- [ ] **Track vehicle location** (GPS monitoring)
- [ ] **Verify data integrity** (checksums, transfer logs)
- [ ] **Maintain equipment** (preventive maintenance, spare parts)
- [ ] **Review costs** (optimize trip frequency, capacity)

---

## 13. Cost-Benefit Analysis Framework

### 13.1 Decision Matrix

**Compare Sneakernet vs Alternatives:**

| Factor | Sneakernet | Starlink | Fiber Build |
|--------|------------|----------|-------------|
| **Initial CapEx** | $2,000-$6,400 (storage) | $2,500 (hardware) | $50,000-$150,000/mile |
| **Monthly OpEx** | $1,000-$3,000 (trips) | $290-$540 (1-2TB) | $208/mile (amortized) |
| **Cost per TB** | $1.50-$5.87/TB | $250-$500/TB (overage) | Variable (depends on volume) |
| **Latency** | Days/weeks | 20-40ms | 1-5ms |
| **Capacity** | Unlimited (scales with trips) | 1-2TB/month (2025 limits) | Unlimited |
| **Reliability** | High (if planned) | Medium (weather dependent) | Very High |
| **Security** | Physical risk | Network risk | Network risk |

**Break-Even Analysis:**
- **Sneakernet vs Starlink:** Sneakernet wins at >1TB/month (Starlink overage costs)
- **Sneakernet vs Fiber:** Fiber wins at >500-1,000 TB/month (depends on distance)

---

## 14. Recommendations

### 14.1 Optimal Sneakernet Configuration

**For Typical Off-Grid AI Inference Site:**

1. **Storage:** 240TB capacity (2× 120TB NAS units)
2. **Vehicle:** Cargo van (Ford Transit or Ram ProMaster)
3. **Driver:** Full-time employee (reliability)
4. **Trip Frequency:** Weekly (adjust based on data generation)
5. **Route:** Nearest fiber POP (<100 miles preferred)
6. **Security:** Full-disk encryption, GPS tracking, insurance
7. **Redundancy:** Backup vehicle or third-party courier option

**Expected Costs:**
- **Initial CapEx:** $4,000-$6,400 (storage hardware)
- **Monthly OpEx:** $2,000-$4,000 (trips + driver + vehicle)
- **Cost per TB:** $2.50-$4.00/TB (at 200-mile distance, weekly trips)

---

## 15. Future Enhancements

### 15.1 Potential Optimizations

1. **Automated Transfer:**
   - **Scheduled transfers:** Automatic data transfer to NAS during off-peak hours
   - **Priority queuing:** Automatic prioritization of critical data
   - **Incremental sync:** Only transfer changed data

2. **Route Optimization:**
   - **Dynamic routing:** Adjust routes based on traffic, weather
   - **Multi-stop:** Combine multiple sites in single trip
   - **Load balancing:** Distribute data across multiple NAS units

3. **Capacity Scaling:**
   - **Modular NAS:** Add/remove NAS units based on demand
   - **Cloud hybrid:** Use cloud for overflow, sneakernet for bulk
   - **Compression:** Reduce transfer time with compression (if CPU-bound)

---

## References

- **Data Optimization Strategies:** `docs/planning/DATA-OPTIMIZATION-STRATEGIES.md` - ✅ **See this document for data optimization techniques** (weight deltas, compression, incremental sync)
- **Data Logistics Pricing:** `research/data-logistics/CONSOLIDATED-SUMMARY.md`
- **PRD Section 3.5:** `docs/PRD.md`
- **FCC Broadband Map:** https://broadbandmap.fcc.gov/
- **IRS Mileage Rates:** https://www.irs.gov/tax-professionals/standard-mileage-rates

---

**Document Status:** Living document - update as operational experience is gained  
**Last Updated:** 2025-12-02

