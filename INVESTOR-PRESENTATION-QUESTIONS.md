# Investor Presentation - Questions for Clarity

**Date:** 2025-12-03
**Purpose:** Gather information to create PowerPoint presentation for new investor (ex-Schlumberger C-suite)
**Presentation Date:** Tomorrow
**Goal:** Secure R&D budget for 12 H100 PCIe GPU validation experiment

---

## Audience Context (What I Know)
- **Investor Profile**: Ex-Schlumberger C-suite, deep O&G expertise
- **Knowledge Gap**: Understands oil/gas intimately, less familiar with AI inference market
- **What He Already Knows**: Scale of stranded gas available (terawatt potential)
- **Ultimate Strategy**: Validate technical approach → Partner with neo-cloud (CoreWeave/Lambda/Crusoe model)

---

## SECTION 1: Existing Infrastructure & Operations

### 1.1 Current Mining Operations
**Q1:** Do you currently have operational Bitcoin mining at one or more sites?
**A:** yes

**Q2:** At the intended R&D pilot site, what is the generator capacity? (kW or MW)
**A:** This is not really important. we have many sites. we will find one. This is more tehoretical to get the budget, then we will choose a sduitable site. 

**Q3:** Approximately how many Bitcoin miners (ASICs) are currently running at this site?
**A:**again doesnt really matter for this. We can just set up a hypothetical. 

**Q4:** What ASIC model(s)? (e.g., Whatsminer M60S, Antminer S21, etc.)
**A:** Whatsminer M60S

**Q5:** Is the pilot site currently operational or would this require bringing a site online?
**A:** Again we have many sites we will choose one. doesnt amtter for this pitch. 

---

## SECTION 2: Financial Parameters for R&D Phase

### 2.1 Budget & Funding
**Q6:** What is the target R&D budget you're requesting from this investor?
**A:** I actually need to know what a small bess + 12 PCIe h100 (assume $30k each, so ~$360k), plus any control systems we need to create. Like i said, maybe deep research is in order for these, but I know we priced them in a document in this in research/bess-decision-analysis and research/bess-discrepancy-reports

**Q7:** Is this investor funding the entire R&D phase, or is 10NetZero co-investing?
**A:** I dont know tbh. Just dont mention it in this pitch. He's already investing a lot. I think its more to say, "we would like to use some of this money for this R&D". 

**Q8:** What ownership/equity structure (if any) comes with this investment?
**A:** NA

### 2.2 Timeline & Milestones
**Q9:** What is the expected timeline for the R&D validation phase? (3 months? 6 months? 12 months?)
**A:** Id like to get started on the R&D within 3 months.

**Q10:** What are the key milestones/deliverables that define "R&D success"?
**A:** Stable dual-workload operation for 90 days

**Q11:** When do you plan to begin partnership discussions with neo-clouds? (Post R&D validation? 2026?)
**A:** Post R&D validation - sometime 2026

---

## SECTION 3: Technical Validation Goals

### 3.1 What Questions Must R&D Answer?
**Q12:** What are the top 3-5 technical questions this R&D experiment must answer?
**A:** 
- [ ] Does BESS + load shedding maintain generator frequency stability (<±2%)?
- [ ] Can we coordinate miner shedding within 100-500ms without generator trips?
- [ ] What are the thermal/cooling requirements at small scale?
- [ ] What control system complexity is required?

**Q13:** Are there specific operational risks you want to validate/mitigate during R&D?
**A:** Does adding this just make bitcoin mining harder as well? Would it be better if we separated them at the power level?

**Q14:** What would constitute a "failed" R&D outcome that would halt further investment?
**A:** Can not maintain power stability when doing inference work. Cannot maintain uptime well enough to serve the customers needs. Cannot profitably do these. 

---

## SECTION 4: Market Positioning & Customers

### 4.1 Batch Inference Workloads
**Q15:** Do you have any existing customer conversations, LOIs, or commitments for batch inference work?
**A:** no

**Q16:** What specific batch workload types are you targeting? (Rank by priority)
**A:** all latency-insenstivei work as outlined in research/inference-types/CONSOLIDATED-SUMMARY.md

**Q17:** Geographic positioning - any specific focus? (US-based? Texas? Proximity to oil fields?)
**A:** Almost all texas, but the investor is based out of romania and has access to A TON of gas and cheap labor. He said he can even build generators. 

### 4.2 Competitive Advantages
**Q18:** Beyond cheap power, what unique advantages does 10NetZero offer customers?
**A:** Off-grid exeprtise. I guess it depends on who you are thinking is the customer. A neo-cloud or the neo-clouds customers? I assume the former. If so, I'd say leveraging our existing operational expertise and infrastructure to provide a unique, differentiated offering in the neo-cloud space. The biggest bottleneck to scaling AI is power. Not GPUs or model innovation. Grid power is fucked (see report i wrote below - you can include this in the presentation). Efven with all the new renewables...they cant get drig hookups. I am claiming the only realistic way for these companies to scale in the short to medium term (and maybe longterm) is finding a way to tap into the plethora of off-grid stranded gas. We are perfect for this and it should be us. The investor already buys this vision, but I dont think he realizes how big it could be. We want to make him excited to give us half a million (or whatever it is) for this. Even if it fails, its a massive assymetric bet. Its a small price to pay for a potentially outsized return. And even if it fails, we will learn a ton about how to optimize our bitcoin operations anyway. so there is no losing IMO. 

```
Harnessing Stranded Gas to Power the
Future of Compute
By:
Colin Aulds,
CTO, 10NetZero, Inc.
Executive Summary
10NetZero is pioneering a new approach to powering the rapidly growing demand for
high-performance computing (HPC), driven by the rise of artificial intelligence (AI) and the
increasing adoption of blockchain technologies like Bitcoin. The company deploys modular data
centers at stranded gas well sites, converting a previously wasted resource into a source of
low-cost, reliable energy for computationally intensive tasks. This innovative approach offers
several key advantages:
●
Low-cost energy: Stranded gas, often flared or vented due to economic and logistical
constraints, provides a significant cost advantage compared to traditional data centers
that rely on grid power.
●
ESG benefits: By utilizing stranded gas, 10NetZero reduces flaring and its associated
environmental impact, generating revenue from a wasted resource and contributing to a
cleaner environment. See our publication Methane Mitigation Through Natural Gas
Turbines.
●
Convergence of industries: 10NetZero's business model uniquely positions it to take
advantage of the fastest growing industry on the planet, as 10NetZero has already
acquired most of the experience, expertise, and infrastructure required to make off-grid
inference compute work. By combining oilfield services, Bitcoin mining, and cloud
computing, 10NetZero will enjoy multiple revenue streams, diversifying risk, and
positioning the company for long-term growth.
●
Decentralized and scalable: The ability to deploy small-scale, off-grid data centers in
remote locations offers advantages over large, centralized facilities, particularly when it
comes to cost savings for less urgent workloads.
This report provides a detailed analysis of 10NetZero's business model, market opportunity, and
financial projections.
Industry Overview
The data center market is experiencing rapid growth, driven by increased digitization, cloud
adoption, and the rise of AI. The AI market in particular is estimated to reach $2T by 2030,
requiring “both new bespoke data centres and upgrades to existing data centres”1
. This growth
is particularly pronounced in the United States, where data centers consumed an estimated
4.4% of total electricity in 2023. Projections indicate that data center electricity consumption
could more than double by 2028, potentially reaching 12% of total U.S. electricity demand. Even
the lowest projection estimates a minimum power consumption of 6.7% of total electricity
consumption2
.
Total server annual electricity consumption by type -
“what kinds of servers are being used?”
2024 U.S. Data Center Energy Usage Report - U.S. Dept. of Energy, pgs. 40
Total annual server electricity consumption by space type -
“who is running the servers?”
2024 U.S. Data Center Energy Usage Report - U.S. Dept. of Energy, pgs. 50
Supply Side Issues in U.S. Energy
This surge in demand for AI services only adds to an already bleak outlook for meeting energy
demands in the near and medium term.
Several supply side issues plague energy production as well.
Difficulties Integrating Renewables
University of California’s Lawrence Berkeley National Laboratory (Berkeley Lab) released
a report in April of 2024, stating
“Only ~20% of projects (14% of capacity) requesting interconnection from
2000-2018 reached commercial operations by the end of 2023. Completion
rates are even lower for solar (14%) and battery (11%) projects. The average
time projects spent in queues before being built has increased markedly. The
typical project built in 2023 took nearly 5 years from the interconnection
request to commercial operations1, compared to 3 years in 2015 and <2
years in 2008.
”
- Lawrence Berkeley National Laboratory, Queued Up: 2024 Edition3
2023 Regional Interconnection Queues
4
Generation, Storage, and Hybrid Capacity in Interconnection Queues - Lawrence Berkeley National Laboratory
Aging Infrastructure & Severe Weather
Part of the reason for the inability to get grid-hookups is due to our aging infrastructure.
In their 2021 report card, The American Society of Civil Engineers issued U.S. energy
infrastructure a score of C- in their 2021 report card.
“Distribution is a key failure point in the electric grid in terms of system reliability.
The distribution system accounts for 92% of all electric service interruptions, a
result of aging infrastructure, severe weather events, and vandalism….The
majority of the nation’s grid is aging, with some components over a century old
— far past their 50-year life expectancy — and others, including 70% of
transmission & data lines, are well into the second half of their lifespans.
”
- American Society of Civil Engineers, 2021 Report Card for America’s
Infrastructure5
The 2025 report card is set to release on march 25, 2025, so we will have to wait until then to
know how much this issue has improved, but the current outlook is not good.
Rising Cost of Grid Upgrades
One consequence of the race to adopt renewable energies has been making an already
expensive grid even more expensive to upgrade.
“Take power-grid transformers. These essential voltage-converting components
are designed to cool down at night, when power consumption is typically low. But
with more people charging their EVs at home at night, the 30-year design life of a
transformer will drop—to perhaps no more than three years once mass adoption
of EVs takes hold. Transformers can cost more than US $20,000 each, and
they're already in short supply in many countries.
”
- IEEE, Robert N. Charette, The Staggering Scale of the EV Transition6
These factors are creating an opportunity for innovators that can address the growing demand
for data center capacity while mitigating the challenges faced by conventional power grids.
Works cited
1. Data Centre Trends 2024 | Clifford Chance,
https://www.cliffordchance.com/content/dam/cliffordchance/briefings/2024/01/2024-data-centre-i
ndustry-outlook.pdf
2. 2024 United States Data Center Energy
Usage Report | U.S. Dept. of Energy,
https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-en
ergy-usage-report.pdf
3. Queued Up: 2024 Edition | Lawrence Berkeley National Laboratory,
https://emp.lbl.gov/sites/default/files/2024-04/Queued%20Up%202024%20Edition_1.pdf
4. Generation, Storage, and Hybrid Capacity in Interconnection Queues | Lawrence Berkeley
National Laboratory, https://emp.lbl.gov/generation-storage-and-hybrid-capacity
5. 2021 Report Card for America’s Infrastructure | American Society of Civil Engineers,
https://infrastructurereportcard.org/wp-content/uploads/2020/12/Energy-2021.pdf
6. The Staggering Scale of the EV Transition | IEEE, Robert N. Charette,
https://spectrum.ieee.org/files/52329/The%20EV%20Transition.final.pdf
```

---

## SECTION 5: Neo-Cloud Partnership Strategy

### 5.1 Target Partners
**Q19:** Which neo-cloud providers are you most interested in partnering with? (Rank by priority)
**A:** Literally any of them. Crusoe is last choice because they used to be a competitor and we dont like them very much but wouldnt let that stop us if it was the best choice. They also understand bitcoin mining. 

**Q20:** Have you had any preliminary conversations with neo-clouds, or is this post-validation?
**A:** post

**Q21:** What deal structure are you envisioning? (Examples below - modify as needed)
**A:** Same as terawulf - longterm take or pay agreement with an advance to help pay for it all.

### 5.2 Scale Potential for Partner Discussions
**Q22:** Across all 10NetZero sites/relationships, what is the realistic scale you could offer a neo-cloud partner in 12-24 months?
**A:** I would say within 12-24 months its possible to deliver a similar sized datacenter that terawulf built for coreweave. Perhaps even bigger. 

**Q23:** Is the partnership strategy focused on a single large partner (CoreWeave model) or multiple smaller partners?
**A:** Open - not important now. 

---

## SECTION 6: Presentation Tone & Investor Expectations

### 6.1 Technical Depth
**Q24:** How technical should the presentation be?
**A:** High-level business case (65% market/financials, 35% technical)

**Q25:** Should I explain AI inference market basics (model types, latency sensitivity, batch vs real-time), or assume he's already researched?
**A:** explain AI inference market basics (model types, latency sensitivity, batch vs real-time. Distinguich between the rates that real-time inference providers cabn charge vs the kind of work we can do. 

### 6.2 Risk & Opportunity Framing
**Q26:** What should I emphasize more - "low risk validation" or "massive upside potential"?
**A:** massive upside potential with knowledge assets gained either way, making this a bet that is very hard to lose even if we fail at the main goal. Absolute worst-case: we learn enough to consult others with projects that are viable (maybe they can optionally connect to a grid) and we could partner on those as a rev-share. 

**Q27:** Are there specific investor concerns or objections you want me to preemptively address?
**A:** "Why not just expand mining?", "What if the capital requirements are too high?", "What if the R&D experiment fails?", "What if neo-clouds don't partner?", others you can think of. 

**Q28:** Should the presentation show financial projections for the R&D phase, the partnership phase, or both?
**A:** Both but make the R&D a lot more detailed than the latter. Just paint a plausible "Big Picture" back of the napkin calcs for the partnership phase but ground it in the terawulf/coreweve deal. You can find the details of that deal here: 2025-10-28_TeraWulf_Expands_Strategic_Partnership_with_121.pdf (use pandoc to convert to markdown if you need to. install if not installed). Make sure that for the partnership phase, you include the costs of data logistics to get data in and out (likely using a sneakernet).

---

## SECTION 7: R&D Experiment Itemization (For Deep Research)

### 7.1 Smallest Viable Experiment Scope
**Q29:** Besides the 12 H100 PCIe GPUs and BESS, what other infrastructure might you need that you DON'T already have?
**A:** GPU servers/racks, monitoring systems (we have these for asics but not for GPUs), cooling upgrades (we have cooling good enough for asics but GPUs are much more picky), and control system software. We also probably need to put in a line item to at least temporarily contract a devops engineer to help set up all the monitoring and control systems. Is that the right kind of expert for this or something else? The investor already has tons of oilfield services staff he can fly in to help. But I think we will need some kind of developor to help.

**Q30:** Do you need to include any site preparation costs (electrical work, space preparation, etc.)?
**A:** Any that wouldnt already be there for an offgrid bitcoin mine. 

**Q31:** Are there any regulatory/permitting costs to budget for (emissions monitoring, grid interconnection studies, etc.)?
**A:** No

**Q32:** Should the R&D budget include initial customer acquisition costs (sales/marketing, pilot customer incentives)?
**A:** no since the point of the R&D is not get customers.

---

## SECTION 8: Fact-Checking & Sourcing Priorities

### 8.1 Claims That Need Rock-Solid Sources
**Q33:** What claims are most critical to have impeccable sourcing for this investor?
**A:** _[Examples below - rank by importance or add others]_
- [ ] Total AI inference market size & growth (2024-2030)
- [ ] Batch inference market segment size & growth
- [ ] H100 PCIe specifications (TDP, performance, cost) - all of this is in the research in this project. You can check docs/nvidia-manuals
- [ ] BESS costs & specifications - use the existing research
- [ ] CoreWeave-Terawulf deal structure (if publicly available) - i already gave you the doc above so use that. 
- [ ] Neo-cloud market landscape - use the existing research. If neocloud specific data is not in the research, output a deep reseach prompt i can run on all the frontier models to created a consolidated report and then we will use that report to enrich the presentation and the models. 
- [ ] Stranded gas power costs vs grid power - dont inlcude. Just assume our ALL-IN power costs (the full price we will pay to create 1kwh of energy) is $0.03/kWh - this includes all our infra and gennys, etc.)
- [ ] I really want you to verify these estimates for fact-checking: 
        BESS (100 kWh) = $40-60K (I think we have research on this pricing)
        Control Systems = $50-100K (I dont think we ahve priced this out and I dont know how to for a small experiment vs a full thing. I also dont know how much of this cost is a 1 time thing because you can just copy and paste it to other instances?)
        Server Infrastructure = ~$50K (same questions as the control system).

**Q34:** Are there any claims in previous presentation drafts that you know are questionable/wrong that I should avoid?
**A:** I would say trust nothing from the existing presentation docs. Rely ONLY on deep research in this repo via the consolidated reports, exasearch, your own web searches, and if any more deep research is needed, all i need is a prompt! 

---

## SECTION 9: Deliverables & Format

### 9.1 What I Will Create (Confirm)
**Q35:** Confirm deliverables:
- [ ] PowerPoint-ready outline with slide-by-slide content (narrative + bullet points)
- [ ] List of all factual claims requiring sources
- [ ] Deep research report on "smallest viable experiment" with itemized costs
- [ ] Source citations for all market data, technical specs, and financial assumptions (many of these can be found in the original deep research reports but you should doublecheck them to make sure they arent hallucinated)

**Q36:** Slide count target? (10 slides? 15? 20? No preference?)
**A:** no more and no less than are needed. Target around a 30 min presentation, give or take 10 min. You have a wide latitude here. i will tell you if its too long or too short. 

**Q37:** Any specific visual/chart requests? (Market size chart, technical architecture diagram, financial waterfall, etc.)
**A:** Id like it to be very visual - helps me more than it helps them tbh. I have bad adhd. I would love to see a visual timeline of the project phases, a technical architecture diagram, and a financial waterfall chart to illustrate the ROI and payback periods. I can also generate images using gemini 3 nano banana. Just provide detailed prompts! And if you can build these visualizations programatticaly in a way that they get rendered beautoifully, thats probably even better because then we can update them easily. Im imagining something like an ascii to image type thing. Im open to ideas. 

---

## SECTION 10: Anything Else?

**Q38:** Is there anything else I should know about this investor, this opportunity, or your expectations that would help me nail this?
**A:** Just reference the streamlist app i have already developed myself as a starting point for further research and modeling. 

---

## Next Steps
1. **You fill in answers above**
2. **I create presentation outline + research scope**
3. **We fact-check & source everything with RAEP protocol**
4. **You look like a genius tomorrow**

---

**Status:** Awaiting your answers
**ETA After Answers Received:** 2-4 hours for complete presentation package
