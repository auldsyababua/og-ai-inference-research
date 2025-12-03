# Adding AI Inference to Existing Bitcoin Mining Infrastructure
## C-Suite Presentation Script

**Duration:** 25-35 minutes  
**Audience:** C-Suite Executive Team  
**Tone:** Technical, practical, focused on implementation

---

## Slide 1: Executive Summary

**[Pause for attention, make eye contact]**

Good morning. I'm here today to present a technical implementation plan for adding AI inference capability to our existing Bitcoin mining infrastructure.

**The core opportunity is this:** We can add latency-sensitive AI inference workloads to our existing mining operations with minimal incremental investment. We already have the power infrastructure, the sites, and the operational expertise. We just need to add GPU compute capability and coordinate it with our existing miners.

**The technical approach leverages what we already have:** Our existing Bitcoin miners serve as flexible, controllable load. When GPUs need to ramp up power for inference workloads, we can shed miners almost instantaneously—in 100 to 500 milliseconds—maintaining stable generator operation. This allows us to run both workloads simultaneously on the same infrastructure.

**The investment is incremental:** We're looking at **$2.9 to $4.6 million** per site to add 100 H100 PCIe GPUs, along with supporting infrastructure like a battery energy storage system for stability. The existing generator, site infrastructure, and mining equipment are already in place—we're just adding GPUs.

**The returns are compelling:** At 75 percent GPU utilization, we're looking at **$15 million in incremental annual revenue** with only **$880,000 to $1.37 million in incremental costs**. That's an **ROI of 295 to 486 percent annually**, with a payback period of just 2 to 4 months.

Let me walk you through the technical implementation and how this works with our existing operations.

---

## Slide 2: Current Infrastructure & Capabilities

**[Reference existing assets]**

Before we talk about what we're adding, let me remind you of what we already have.

**Our existing assets:**

We have established, operational Bitcoin mining infrastructure. We have off-grid generators that are already deployed and running. We have site infrastructure—cooling, connectivity, operational procedures—all in place. And we have proven operational expertise in running remote off-grid operations.

**Current infrastructure utilization:**

Our Bitcoin mining operations are consuming available generator capacity. The miners themselves have a key characteristic: they can be shed and restarted with a **100 to 500 millisecond response time**. This makes them perfect flexible load.

Our generators have either headroom available, or we can accommodate GPU addition. And our sites are in remote locations that are actually ideal for latency-sensitive inference work—low latency, data sovereignty, and we're already there.

**Why this approach works:**

We don't need to build new generator infrastructure—it already exists. We don't need new sites—we can leverage our operational knowledge and site relationships. The miners provide perfect flexible load for GPU power ramps. And this is incremental revenue—we're adding AI inference capability without disrupting our mining operations.

This is about leveraging what we've already built, not starting from scratch.

---

## Slide 3: Technical Implementation Strategy

**[Explain workload types and coordination]**

Let me explain the technical implementation strategy.

**Workload types:**

We're focusing on two types of inference work. First, **latency-sensitive inference**—this is our primary focus. Real-time inference workloads that require low latency, like real-time LLM inference for chat and completion, edge AI for industrial automation, and time-critical decision-making workloads. These require 1 to 10 milliseconds of local processing versus 50 to 200 milliseconds in the cloud.

Second, **batch inference work**—this is secondary but still valuable. Large-scale model inference, batch embeddings generation, scheduled processing jobs. These can be scheduled around latency-sensitive work and provide additional utilization.

**Load coordination strategy:**

Here's how the power management works. When inference workloads come in, GPUs need to ramp up power—this causes sudden power increases. Our existing miners can shed in **100 to 500 milliseconds** before the GPU ramp. The generator sees a minimal net load change, maintaining stable operation. When GPU load decreases, miners restart automatically.

**Operational model:**

Latency-sensitive work takes priority—miners shed first when GPUs need power. Batch work gets scheduled during low-latency demand periods. Mining continues when GPUs are idle or at low utilization. And we optimize revenue by balancing mining revenue versus inference revenue based on demand.

This is a sophisticated load coordination system, but it leverages infrastructure we already have.

---

## Slide 4: Incremental Financial Impact

**[Walk through incremental economics]**

Let me break down the incremental financial impact—this is where it gets interesting.

**Incremental capital expenditure:**

For adding 100 GPUs to an existing site, here's what we need. The GPUs themselves—100 H100 PCIe GPUs—cost **$2.5 to $3.8 million**. GPU server infrastructure adds **$200,000 to $400,000**. We're recommending a BESS—battery energy storage system at 100 kilowatt-hours—for **$40,000 to $60,000**. Control system integration is **$50,000 to $100,000**. And installation and commissioning adds **$100,000 to $200,000**.

**Total incremental CapEx: $2.9 to $4.6 million per site.**

The key point: existing generator, site infrastructure, and mining equipment are already in place. We're not building new infrastructure—we're adding GPUs.

**Incremental revenue:**

At 75 percent utilization, 100 GPUs generate **$15 million annually** at the market rate of $2.29 per GPU-hour. That's 6,570 hours per year per GPU.

**Bitcoin mining impact:**

Miners get shed during GPU operations, which reduces mining revenue. But mining continues when GPUs are idle or at low utilization. The net impact is variable and depends on inference utilization patterns. But remember—mining provides a revenue floor.

**Incremental operating costs:**

Additional fuel and power for GPUs is **$150,000 to $200,000 annually**. GPU maintenance is **$100,000 to $150,000**. Control system operations add **$50,000 to $100,000**. And amortization over 5 years for the GPUs is **$580,000 to $920,000**.

**Total incremental OpEx: $880,000 to $1.37 million.**

**Incremental economics:**

Incremental revenue of $15 million minus incremental costs of $0.88 to $1.37 million equals **incremental net income of $13.6 to $14.1 million**. That's an **ROI of 295 to 486 percent annually** on a $2.9 to $4.6 million incremental investment. Payback period is just **2 to 4 months**.

These numbers assume 75 percent utilization. Even at much lower utilization, the economics are compelling because our incremental costs are so low.

---

## Slide 5: Break-Even & Sensitivity Analysis

**[Emphasize low break-even point]**

Let me address break-even and sensitivity, because this is a key advantage of our approach.

**AI inference break-even:**

Our break-even utilization is only **15 to 20 percent** at the $2.29 per hour market rate. Compare that to a greenfield deployment where you'd need 68 percent utilization to break even.

**Why is our break-even so low?**

Incremental costs are minimal because existing infrastructure is already in place. Only GPU-specific costs are incremental. Fuel and power costs are shared with existing mining operations. And site operations are already staffed and operational.

**Sensitivity to utilization:**

At 20 percent utilization, we generate $3 million in incremental net income with an ROI of 65 to 103 percent. At 50 percent utilization, that jumps to $7.5 million and 163 to 259 percent ROI. At our target of 75 percent, we're at $13.6 to $14.1 million and 295 to 486 percent ROI. And at 90 percent utilization, we achieve $16.4 to $17.0 million and 357 to 586 percent ROI.

**Key risk factors:**

First, **inference demand**—we need sufficient latency-sensitive workload demand. Second, **market rate volatility**—AI inference pricing may fluctuate. Third, **technical complexity**—load balancing requires control system integration. Fourth, **mining revenue impact**—reduced mining revenue when miners shed for GPUs. And fifth, **operational learning curve**—new workload type requires operational expertise.

The good news: we have a very low break-even point, which provides significant buffer. And mining operations continue regardless of inference success, so the risk is low.

---

## Slide 6: Technical Implementation Architecture

**[Use visual aids, point to diagram]**

Let me walk you through the technical architecture.

**Existing infrastructure—no changes required:**

We already have operational generators providing power to mining operations. Generator capacity is sufficient or can accommodate GPU addition. Fuel supply is already established and operational.

We have existing Bitcoin miners—ASIC miners like Whatsminer M60S at 3.3 kilowatts each. Existing control systems that can be extended for load coordination. And existing container infrastructure that's operational.

**New infrastructure required:**

We need to add a GPU compute cluster—100 H100 PCIe GPUs at 350 watts each, about 35 kilowatts total plus overhead. Standard servers with H100 PCIe cards. We can leverage existing cooling infrastructure, though we may need minor expansion.

We need a load coordination system—software to coordinate GPU ramps with miner shedding. Response time is 100 to 500 milliseconds—miner shutdown before GPU power-on. And real-time monitoring of generator frequency, GPU power, and miner status.

**Stabilization—recommended:**

We're recommending a BESS—Battery Energy Storage System at 100 kilowatt-hours. This is a **$40,000 to $60,000 investment**, but it provides significant benefits. It gives us 5 to 15 seconds of ride-through for faults, simplifies control systems by 60 to 70 percent, and reduces risk of generator trips substantially.

**The technical innovation:**

Load coordination is the key. Existing miners serve as flexible load for GPU ramps. We maintain generator frequency within **±1 to 2 percent**, compared to ±3 to 7 percent without coordination. Both mining and inference run simultaneously. And miner shutdown happens in under 500 milliseconds to accommodate GPU loads.

This is sophisticated, but it leverages what we already have.

---

## Slide 7: Implementation Roadmap

**[Present phased approach]**

Our implementation roadmap is built in three phases.

**Phase 1: Pilot Site Retrofit—Months 1 to 4**

The objective is to add GPU capability to one existing mining site. We'll select a pilot site from our existing mining operations, install 100 H100 PCIe GPUs, deploy the recommended BESS, develop and test load balancing algorithms, integrate GPU control with existing miner control systems, and establish operational procedures for dual-workload operation.

The investment is **$2.9 to $4.6 million incremental**.

Success metrics: Stable generator operation with less than 2 percent frequency deviation. Successful load coordination—miners shed and restart on demand. 50 percent or higher GPU utilization within 3 months. And no disruption to existing mining operations.

**Phase 2: Operational Optimization—Months 5 to 8**

The objective is to optimize operations and validate economics. We'll refine load balancing algorithms based on real-world data, optimize workload scheduling between latency-sensitive and batch work, establish a customer pipeline for inference workloads, validate financial projections, and document operational procedures.

Success metrics: 75 percent or higher GPU utilization. Positive incremental cash flow. Operational procedures documented. And load balancing reliability above 99 percent.

**Phase 3: Multi-Site Rollout—Months 9 to 18**

The objective is to add GPU capability to additional mining sites. We'll retrofit 2 to 4 additional mining sites, scale load balancing software across sites, build customer base for inference workloads, and optimize operations based on multi-site experience.

The investment is **$5.8 to $9.2 million** for 2 to 4 additional sites. Our target is 300 to 500 GPUs across 3 to 5 sites.

This phased approach allows us to validate the technical implementation, learn from operations, and scale systematically.

---

## Slide 8: Why This Approach Works

**[Emphasize advantages]**

Let me explain why this approach works so well for us.

**Technical advantages:**

We're leveraging existing infrastructure—operational generators, sites, and expertise. Miners provide perfect flexible load with 100 to 500 millisecond response time. Incremental cost is low—only GPU equipment is new; everything else exists. And we have proven operations—mining operations are already stable and reliable.

**Operational advantages:**

We don't need new sites—we use existing mining sites, no new site development required. We leverage existing staff—operational knowledge and site relationships. We extend established procedures—build on what we already know. And we have risk mitigation—mining continues if inference demand drops.

**Financial advantages:**

We have a very low break-even—only 15 to 20 percent utilization needed. High ROI—295 to 486 percent annually on incremental investment. Fast payback—2 to 4 month payback period. And incremental revenue—we add revenue without disrupting mining operations.

This is about leveraging what we've built, not reinventing the wheel.

---

## Slide 9: Risk Assessment & Mitigation

**[Be transparent about risks]**

Let me address the risks head-on.

**Technical risks:**

**Load balancing failure** could cause generator trip and downtime. Our mitigation: BESS provides buffer, and we'll conduct extensive testing before deployment. **GPU integration complexity** could delay deployment. Our mitigation: We're using proven H100 PCIe hardware with standard server infrastructure. **Miner coordination issues** could cause operational disruption. Our mitigation: BESS simplifies operations, and phased rollout allows learning. **Generator capacity limits** could prevent GPU addition. Our mitigation: We'll assess generator headroom before deployment and upgrade if needed.

**Operational risks:**

**Inference demand insufficient** would result in low GPU utilization. Our mitigation: Low break-even of 15 to 20 percent provides buffer, and mining continues. **Mining revenue impact** from reduced mining income. Our mitigation: Miners restart when GPUs idle, and we balance based on relative profitability. **Operational learning curve** could cause initial inefficiency. Our mitigation: Pilot site allows learning, and existing operations team can adapt. **Workload scheduling complexity** could create operational overhead. Our mitigation: Automated load scheduler, and BESS reduces complexity.

**Market risks:**

**AI inference rate decline** would reduce revenue. Our mitigation: Low break-even provides buffer, and mining operations continue. **Latency-sensitive demand insufficient** would result in low utilization. Our mitigation: We can serve batch workloads, and mining provides revenue floor. **Competition** could erode market share. Our mitigation: Existing infrastructure provides cost advantage.

We've thought through these risks, and we have mitigation strategies. The low break-even and continued mining operations provide natural risk mitigation.

---

## Slide 10: Investment Requirements & Returns

**[Present investment case]**

Let me summarize the investment requirements and returns.

**Incremental capital requirements:**

For a pilot site retrofit with 100 GPUs, we need **$2.9 to $4.6 million in incremental CapEx**. Timeline to operational is 3 to 4 months, and we expect break-even within 2 to 4 months post-deployment at 15 to 20 percent utilization.

For multi-site rollout—300 to 500 GPUs across 3 to 5 sites—we're looking at **$8.7 to $18.4 million in incremental CapEx** over 9 to 18 months. Target revenue at that scale is **$45 to $75 million annually** at 75 percent utilization.

**Return profile:**

**Year 1 for pilot site—100 GPUs:** Incremental revenue of $15 million at 75 percent utilization, incremental costs of $0.88 to $1.37 million, incremental net income of **$13.6 to $14.1 million**. That's an **ROI of 295 to 486 percent**.

**Year 2 at 3 sites—300 GPUs:** Incremental revenue of $45 million, incremental costs of $2.6 to $4.1 million, incremental net income of **$40.9 to $42.4 million**. Cumulative ROI over 2 years is **470 to 920 percent**.

**Funding considerations:**

This is incremental investment—only GPU equipment and supporting infrastructure. Existing assets—generator, site, mining infrastructure—are already in place. Low risk—mining operations continue regardless of inference demand. And fast payback—2 to 4 months at low utilization, faster at higher utilization.

The returns justify the investment, and the incremental nature reduces risk significantly.

---

## Slide 11: Key Success Factors

**[Emphasize what we need to execute]**

Let me outline what we need to succeed.

**Critical success factors:**

First, **technical execution**. We must deliver reliable load balancing and generator stability. This is foundational. Second, **workload acquisition**. We need to secure latency-sensitive inference customers. Third, **operational integration**. We need seamless dual-workload operation without disrupting mining. And fourth, **load coordination**. We need successful miner shedding and restart coordination.

**Required capabilities:**

We need **engineering** capabilities—control systems integration, extending existing miner control. We need **operations** capabilities—dual-workload operational procedures, extending existing procedures. We need **workload acquisition**—secure inference customers, this is a new capability. And we need **monitoring**—real-time load coordination monitoring, extending existing systems.

**Advantages we have:**

We have **existing operations**—proven ability to run remote off-grid operations. We have **site infrastructure**—already operational and maintained. We have **technical expertise**—generator and mining operations expertise. And we have **low risk**—mining operations continue regardless of inference success.

We have most of what we need. We just need to add GPU capability and extend our operations.

---

## Slide 12: Recommendations & Next Steps

**[Be clear and actionable]**

Let me present our recommendations and next steps.

**Immediate actions—next 30 days:**

First, **approve pilot retrofit**. We're requesting authorization for $2.9 to $4.6 million for pilot site GPU addition. Second, **select site**. Choose existing mining site for pilot retrofit. Third, **assess generators**. Verify generator capacity and headroom. And fourth, **select vendors**. Identify GPU suppliers for H100 PCIe and BESS vendors.

**Short-term—3 to 4 months:**

Retrofit pilot site—install GPUs, BESS, and control systems. Develop load balancing—develop and test miner-GPU coordination. Establish procedures—establish dual-workload operational procedures. And conduct initial testing—validate load balancing and generator stability.

**Medium-term—4 to 8 months:**

Begin workload acquisition—secure latency-sensitive inference customers. Optimize operations—refine load balancing based on real-world data. Validate economics—confirm financial projections with actual operations. And document procedures—document procedures for multi-site rollout.

**Long-term—9 to 18 months:**

Roll out to multiple sites—add GPU capability to 2 to 4 additional mining sites. Scale operations—build customer base and optimize across sites. Develop platform—develop software platform for multi-site management. And evaluate expansion—assess additional sites based on success.

**My recommendation:**

I recommend we **approve the pilot retrofit** and move forward with site selection and generator assessment immediately. The incremental investment is modest, the returns are compelling, and we're leveraging infrastructure we've already built. The risk is low because mining operations continue regardless of inference success.

This is a measured approach that allows us to validate the technical implementation, learn from operations, and scale based on results.

---

## Slide 13: Appendix: Key Assumptions

**[Quick reference]**

Let me quickly cover our key assumptions.

**Financial assumptions:**

GPU market rate is **$2.29 per hour**—benchmarked against RunPod Secure Cloud pricing. GPU utilization target is **75 percent average**, with break-even at 15 to 20 percent. Incremental GPU cost is **$0.15 to $0.20 per hour**—only fuel, maintenance, and amortization. Existing infrastructure—generator, site, mining infrastructure—already operational. Fuel costs are shared with mining operations. And Bitcoin mining continues when GPUs idle; miners shed during GPU operations.

**Technical assumptions:**

GPU model is **H100 PCIe at 350 watts per GPU**. Existing miners are Whatsminer M60S or similar at 3.3 kilowatts per unit. Load balancing response time is **100 to 500 milliseconds**. BESS recommendation is **100 kilowatt-hours at $40,000 to $60,000**. And generators are existing with sufficient capacity or upgradeable.

**Operational assumptions:**

Existing sites—mining operations already operational and stable. Existing staff—operations team can extend to dual-workload operation. Workload types—latency-sensitive inference primary, batch inference secondary. And mining continuity—mining operations continue regardless of inference demand.

These assumptions are based on extensive research and our existing operations. We've been conservative in our projections, and the low break-even provides significant buffer.

---

## Closing Remarks

**[Summarize and call for decision]**

Let me summarize:

We have an opportunity to add **AI inference capability to our existing Bitcoin mining infrastructure** with minimal incremental investment. We're leveraging **infrastructure we've already built**—generators, sites, operational expertise. We have **compelling financial returns**—295 to 486 percent ROI annually on incremental investment, with 2 to 4 month payback. We have **low risk**—mining operations continue regardless of inference success, and break-even is only 15 to 20 percent utilization. And we have a **clear implementation plan** with phased deployment and defined success metrics.

The risks are manageable. We have mitigation strategies for technical, operational, and market risks. The low break-even and continued mining operations provide natural risk mitigation.

**The question isn't whether we can do this—we can. The question is whether we should.**

I recommend we move forward with the pilot retrofit. We can start with a $2.9 to $4.6 million incremental investment, validate the technical implementation in 4 months, and then decide on scaling. This is a measured approach that leverages what we've already built.

I'm happy to answer any questions you have, and I'm ready to move forward immediately upon approval.

Thank you.

---

## Q&A Preparation

### "Why add AI inference to mining operations?"

This is incremental revenue with minimal incremental cost. We leverage existing infrastructure—generators, sites, operational expertise. Miners provide perfect flexible load for GPU power ramps. And mining operations continue regardless of inference success, so risk is low.

### "What if inference demand is insufficient?"

We have a very low break-even—only 15 to 20 percent utilization needed. Mining operations continue, providing revenue floor. And we can serve batch workloads if latency-sensitive demand is low. The low break-even provides significant buffer.

### "What's the impact on mining operations?"

Miners shed during GPU operations—this reduces mining revenue temporarily. But miners restart when GPUs idle or at low utilization. We balance based on relative profitability—if inference is more profitable, we prioritize it. Mining provides revenue floor and load balancing capability.

### "How complex is the technical implementation?"

BESS simplifies operations significantly—60 to 70 percent complexity reduction. We're extending existing control systems, not building from scratch. And phased rollout allows learning. The technical complexity is manageable, especially with BESS.

### "What if the capital requirements are too high?"

This is incremental investment—only GPU equipment is new. Existing infrastructure is already in place. We can start with one site and scale based on results. And payback is fast—2 to 4 months. The incremental nature reduces capital requirements significantly.

### "How do we know this will work?"

We have existing infrastructure and operational expertise. The technical approach leverages proven hardware—H100 PCIe GPUs, standard servers. Load balancing is well-understood—miners can shed/restart quickly. And pilot site allows validation before scaling. We're not betting everything—mining continues regardless.

---

**End of Presentation Script**
