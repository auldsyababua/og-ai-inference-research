Data Connectivity Pricing (Off-Grid AI Inference, 2025--2026)
=============================================================

Executive Summary
-----------------

-   **Starlink**: Business service plans in the U.S. cost
    \~\$65--540/month (for 50 GB--2 TB data caps) with a one-time
    hardware charge (\$349 for standard
    kit)[\[1\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=Reliable%20high,a%20hardware%20cost%20of%20%24349)[\[2\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=LOCAL%20PRIORITY%20).
    Advertised top speeds are "up to 400+ Mbps" (with gigabit support
    coming in
    2026)[\[3\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=Service%20plan%20upgrades%20will%20be,connectivity%20whenever%20you%20need%20it),
    but median real-world speeds are \~105 Mbps down, \~15 Mbps up (Q1
    2025)[\[4\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=,84%20Mbps%20in%20Q1%202025).
    Latency is \~45 ms
    median[\[5\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=Starlink%20users%20in%20the%20U,median%20latency%20of%2045%20ms).
    After data cap, speed falls to 1 Mbps (down)/0.5 Mbps
    (up)[\[6\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=Unlimited%20Data%20at%20up%20to,Includes%20service%20level%20agreement).
    Equipment upgrades (e.g. Performance Kit) cost
    \~\$2,000[\[7\]](https://seabits.com/starlink-performance-kit-unboxing/#:~:text=Starlink%20released%20a%20new%20version,my%20initial%20unboxing%20and%20impressions).
    **(Data gap:** few independent enterprise benchmarks;
    **Confidence:** High for pricing, Medium for performance data).
-   **Sneakernet**: **Commercial** appliances -- e.g. AWS Snowball Edge
    (80 TB) costs \$300 service fee (+\$30/day
    extra)[\[8\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=Service%20Fee%24300%20per%20device%24500%20per,day%24125%20per%20day%24165%20per%20day);
    Azure Data Box (100 TB) costs \~\$250
    (+\$15/day)[\[9\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=Data%20Box%20Data%20Box%20Disk,Starting%20at%29%20%241%2C500).
    These include shipping (\~\$30--\$150/way) and no ingress fees, but
    egress cloud charges (e.g. AWS \$0.05/GB out). **DIY** costs: a
    mid-size van costs \~\\\$0.70/mile to operate (IRS mileage
    rate)[\[10\]](https://www.irs.gov/pub/irs-drop/n-25-05.pdf?utm_source=telarus?wtime#:~:text=SECTION%203,See);
    plus driver labor (\~\\\$0.4--0.5/mile at \\\$30/h, Low confidence).
    Storage media: commodity HDDs \~\\\$10--15/TB (24 TB
    \~\\\$13/TB[\[11\]](https://diskprices.com/#:~:text=%240,6Tb)); LTO
    tape
    \~\\\$5/TB[\[12\]](https://diskprices.com/#:~:text=%240,8%20Data%20Cartridge%2FTape).
    A 500-mi round trip (\~\\\$350 fuel+maintenance + \\\$160 driver,
    \~\\\$0.7--1.0/mi) carrying 240 TB yields \~\$2--3 per TB.
    Open-source tools (e.g. **rsync**, **Syncthing**) can replace
    commercial sync software (e.g. Resilio) at minimal cost (Low
    confidence). **(Confidence:** Medium for provider fees, Medium--Low
    for DIY estimates).
-   **Rural Fiber**: Costs vary widely by method and terrain. Median
    **underground** build is \~\$11--24/ft (roughly \\\$58k--126k/mile);
    **aerial** \~\$4--9/ft
    (\\\$21k--48k/mile)[\[13\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,per%20foot%20for%20aerial%20deployment).
    Rural areas often see lower densities: median \~\\\$5/ft
    (\\\$26k/mile) for
    aerial[\[14\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,54%2Fft%20for%20urban%20areas).
    Rocky or difficult terrain roughly doubles trenching cost
    (\~\\\$20/ft,
    \\\$105k/mile)[\[15\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=%245,in%20rocky%20terrain%20at%20%2420%2Fft).
    Labor is 2/3+ of
    cost[\[16\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=underground,54%2Fft%20for%20urban%20areas).
    OPEX is low (mostly repair/power): perhaps 1--5% of capex/year
    (\~\\\$500--2,000/mile-year, *Low confidence*). Amortize fiber
    (\~\\\$50--125k/mi) over \~20--30 years. Europe (e.g. Romania)
    likely sees lower labor and permitting costs (Medium confidence).
    **(Data gap:** few open figures on non-U.S. builds; **Confidence:**
    Medium for U.S., Low for Romania).
-   **Key Data Gaps**: Independent end-to-end tests of Starlink
    enterprise plans; precise DIY labor costs; rural fiber build costs
    outside U.S. **Priority recommendations** are to use: Starlink
    Business 1 TB plan (\\\$290/mo, equipment \\\$349, Median speed
    \~100 Mbps, Latency \~45 ms; *High confidence*); Snowball Edge
    (80 TB, \\\$300/10 d) and Data Box (100 TB, \\\$250/10 d) for
    providers (*High*); DIY estimates \~\$0.70/mi + \\\$10/TB for drives
    (*Low--Medium*); fiber build \\\$5--\\\$20/ft depending on
    conditions (*Medium*).

Starlink (Business) Pricing and Performance
-------------------------------------------

-   **Service Plans**: Starlink Fixed-Site ("Business") offers 4 preset
    data caps. *Local-Priority* plans (U.S.) are 50 GB for \\\$65/mo,
    500 GB for \\\$165, 1 TB for \\\$290, and 2 TB for
    \\\$540[\[2\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=LOCAL%20PRIORITY%20).
    *(High confidence)* Additional data blocks are \\\$25/50 GB or
    \\\$125/500 GB[\[17\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=%2B50GB).
    *Global-Priority* (network-priority) plans cost \~3--4× more
    (\\\$250--\\\$2,150 for
    50 GB--2 TB)[\[18\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=GLOBAL%20PRIORITY%20).
    Hardware is extra: standard dish kit
    \\\$349[\[1\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=Reliable%20high,a%20hardware%20cost%20of%20%24349).
    (Note: new free-equipment offers require 1-year term, but typical
    plans appear month-to-month.)
-   **Data Usage**: Plans include full-speed data up to cap. After the
    cap, service continues at 1 Mbps down/0.5 Mbps up (unlimited
    low-speed)[\[6\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=Unlimited%20Data%20at%20up%20to,Includes%20service%20level%20agreement).
    No per-GB overage fees. (Applies to both Local- and Global-Priority
    plans.)
-   **Bandwidth**: Officially, Starlink Performance (Gen3) "Performance
    Kit" supports up to *400+ Mbps*
    download[\[3\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=Service%20plan%20upgrades%20will%20be,connectivity%20whenever%20you%20need%20it).
    Ookla Speedtest data show **median** U.S. speeds in Q1 2025 of
    \~104.7 Mbps down and 14.8 Mbps
    up[\[4\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=,84%20Mbps%20in%20Q1%202025),
    up from \~54/7.5 Mbps in late 2022. Only \~17% of users achieve
    100/20 Mbps broadband-standard
    speeds[\[19\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=%2A%20Only%2017.4,to%20its%20low%20upload%20speeds).
    Variability is high: some users see \>130 Mbps, others
    \~70 Mbps[\[20\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=,65%20Mbps%20in%20Alaska).
    *User reports:* priority plans can improve speeds under congestion,
    but in practice many report only marginal gains during busy
    periods[\[21\]](https://www.reddit.com/r/Starlink/comments/16e0igw/starlink_standard_vs_priority/#:~:text=Based%20on%20experience%2C%20prioritized%20or,Virginia%20regardless%20of%20your%20plan)[\[22\]](https://www.reddit.com/r/Starlink/comments/16e0igw/starlink_standard_vs_priority/#:~:text=IMO%20the%20biggest%20reason%20for,variable%20nature%20of%20Starlink%27s%20network)
    (user experience, *Low confidence*).
-   **Latency & Overhead**: LEO orbits give low latency (\~45 ms median
    in
    Q1'25)[\[5\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=Starlink%20users%20in%20the%20U,median%20latency%20of%2045%20ms),
    much better than GEO satellites. Contention under peak load can
    still slow all users
    somewhat[\[21\]](https://www.reddit.com/r/Starlink/comments/16e0igw/starlink_standard_vs_priority/#:~:text=Based%20on%20experience%2C%20prioritized%20or,Virginia%20regardless%20of%20your%20plan).
    Network Priority plans offer better support and may reduce
    throttling under
    load[\[23\]](https://www.reddit.com/r/Starlink/comments/16e0igw/starlink_standard_vs_priority/#:~:text=%E2%80%A2%20%202y%20ago),
    but do not guarantee 24/7 max speed. (Starlink advertises business
    SLA only for Global Priority plans.)
-   **Equipment**: The standard Business kit is
    \\\$349[\[1\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=Reliable%20high,a%20hardware%20cost%20of%20%24349).
    The new *Performance Kit* (marine-grade) costs
    \~\\\$2,000[\[7\]](https://seabits.com/starlink-performance-kit-unboxing/#:~:text=Starlink%20released%20a%20new%20version,my%20initial%20unboxing%20and%20impressions)
    and is fully waterproof, 10-year rated. No router included by
    default (but can add free). The Performance Kit is needed for
    gigabit-class service (coming
    2026)[\[24\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=GIGABIT%20SPEEDS%20AVAILABLE%20IN%202026).

Sneakernet Solutions
--------------------

### Cloud Provider Appliances

-   **AWS Snowball**: *Storage Optimized (210 TB)* device has \\\$3,200
    service (15 days
    included)[\[25\]](https://aws.amazon.com/snowball/pricing/#:~:text=Suppose%20you%20use%20the%20Snowball,day%20fees.%20Since%20you%20are)
    and \\\$250/day extra; *Compute Optimized (many vCPUs)* is
    \\\$5,038/month or \\\$1,250 service+
    \\\$125/day[\[8\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=Service%20Fee%24300%20per%20device%24500%20per,day%24125%20per%20day%24165%20per%20day).
    The 80 TB (Gen1 Snowball) is \\\$300 +
    \\\$30/day[\[8\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=Service%20Fee%24300%20per%20device%24500%20per,day%24125%20per%20day%24165%20per%20day).
    Shipping is extra (examples indicate \\\$150--\\\$200 round-trip,
    but varies by region). Ingress to AWS S3 is free; egress
    \~\\\$0.05/GB (50¢/TB). *Example:* Importing 80 TB via Snowball to
    AWS costs \\\$300 +
    shipping[\[26\]](https://aws.amazon.com/snowball/pricing/#:~:text=You%20would%20pay%20a%20service,ship%20it%20back%20to%20AWS)
    (no per-GB fee if \<15 days). (High confidence on pricing; actual
    shipping and taxes vary.)
-   **Azure Data Box**: *Data Box (100 TB)*: \\\$250 service (10-day),
    \\\$15/day extra, \\\$95 round-trip
    shipping[\[9\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=Data%20Box%20Data%20Box%20Disk,Starting%20at%29%20%241%2C500).
    *Data Box Disk (40 TB)*: \\\$50 service, \\\$10/day, \\\$30
    shipping[\[9\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=Data%20Box%20Data%20Box%20Disk,Starting%20at%29%20%241%2C500).
    Data ingress is free; egress adds Azure bandwidth charges (e.g.
    \~\$0.02/GB). *Example:* 50 TB import = \\\$250 + \\\$95
    shipping[\[27\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=To%20give%20you%20a%20better,provide%20two%20example%20scenarios%20below).
    (High confidence for fees; actual cost depends on usage days.)
-   **Other Providers**: Google no longer markets an appliance; IBM
    offers similar but less common. **Third-party**: Resilio Connect
    (software sync, commercial) vs open tools (rsync, Syncthing) for
    real-time or incremental transfers (not physically shipping).

### DIY Sneakernet

-   **Vehicle & Fuel**: A work van or truck cost is \~\\\$0.70/mile (IRS
    business rate for
    2025[\[10\]](https://www.irs.gov/pub/irs-drop/n-25-05.pdf?utm_source=telarus?wtime#:~:text=SECTION%203,See),
    which covers fuel, maintenance, etc). Driver labor (\~\\\$20--30/hr)
    adds \~\\\$0.30--0.50/mile (e.g. \\\$25/hr at 60 mph ≈\\\$0.42/mile)
    (Medium confidence). Thus **total** \~\\\$1/mile (round-trip
    fuel+vehicle+wage).
-   **Storage Hardware**: Can use rugged NAS or portable disks.
    Commodity HDDs cost \~\\\$10--13/TB (e.g. 24 TB \~\\\$313 →
    \\\$13.06/TB[\[11\]](https://diskprices.com/#:~:text=%240,6Tb)).
    Enterprise or refurbished might reach \\\$8--10/TB. LTO tapes
    (\~18 TB native) cost
    \~\\\$5/TB[\[12\]](https://diskprices.com/#:~:text=%240,8%20Data%20Cartridge%2FTape)
    (media only; need tape drive \~\\\$10--15k). A budget 4-bay NAS
    (diskless) is \\\$400--500 retail. Open-source storage (ZFS,
    FreeNAS, etc.) is free.
-   **Software & Ops**: For transfer, simple tools (rsync, ZFS send,
    Syncthing) are free. Commercial WAN-sync (e.g. Resilio) charges per
    node. Shipping procedures (encryption, handling) add negligible
    cost.
-   **Cost Metrics**: For example, a 500 mi round trip (\~\\\$350
    vehicle + \\\$175 driver ≈\\\$525 total) carrying 240 TB (10×24TB
    disks) yields \~\\\$2.2/TB for that trip. Per-mile cost \~\\\$1.05
    (Medium confidence). If only carrying 50 TB, cost/TB \~\\\$10.
    Overnight trips add lodging (\~\\\$100) and lower payload
    utilization (High/Low scenarios). We estimate **per-trip**
    \\\$100--1000, **per-mile** \\\$0.5--1.5, **per-TB** \\\$2--\\\$20,
    depending on capacity and distance (Low confidence on extremes).

Rural Fiber Deployment Costs
----------------------------

-   **Build Costs** (per foot): Industry surveys find aerial fiber at
    \\\$4--9/ft and underground at
    \\\$11--24/ft[\[13\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,per%20foot%20for%20aerial%20deployment).
    In rural areas, median aerial is \~\$5/ft (≈\\\$26k/mile) and urban
    \~\$6.54/ft[\[14\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,54%2Fft%20for%20urban%20areas).
    Underground trenching in soft soil is \~\\\$10/ft (\\\$53k/mile) but
    up to \\\$20/ft on rocky
    terrain[\[15\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=%245,in%20rocky%20terrain%20at%20%2420%2Fft).
    Poles vs buried cables, make-ready work, and labor (70% of cost)
    heavily influence final
    cost[\[28\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,54%2Fft%20for%20urban%20areas).
    Typical **low/high ranges** (US rural): aerial \\\$20--30k/mi,
    underground \\\$50--100k/mi, with extremes perhaps \~\\\$15k/mi
    (light pull) to \\\$200k/mi (deep rock) (Medium confidence).
-   **Cost Factors**: Trenching/plowing vs microtrenching, pole
    attachment vs new poles, permitting delays can add 10--30% to
    budgets. Labor rates vary regionally (Western US
    higher)[\[29\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,54%2Fft%20for%20urban%20areas).
    In Europe (e.g. Romania), lower labor may reduce by \~20% (Low
    confidence).
-   **OpEx & Amortization**: Fiber's fixed O&M is low: just power for
    amplifiers/switches and occasional repairs. Fiber amortizes over
    \~20--30 years (typical IT equipment life). If built for
    \\\$50k/mile, annualized (\~4% cost of capital) ≈\\\$2k/mile-year.
    Actual maintenance (cut/fix, lights) might be on order
    \\\$500--\\\$2000/mile-year (Low confidence estimate).
-   **Regional Variations**: US data above. Romania/E. Europe likely
    somewhat cheaper (lower labor/tax), though terrain and density
    matter. We found no published Romanian fiber cost per km; use U.S.
    as proxy (*data gap*, Low confidence).

Recommendations & Data Notes
----------------------------

-   **Default Parameters**: Use Starlink Business 1 TB plan (\\\$290/mo,
    \\\$349 hardware) for baseline (advertised 400+ Mbps, measured
    \~100 Mbps
    median)[\[1\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=Reliable%20high,a%20hardware%20cost%20of%20%24349)[\[4\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=,84%20Mbps%20in%20Q1%202025)
    (High/Med confidence). Use AWS Snowball Edge (80 TB) at \\\$300 per
    10-day job, and Azure Data Box (100 TB) at \\\$250/10 days (High
    confidence). For DIY, assume \\\$0.70/mi vehicle + \\\$0.5/mi labor
    (IRS rate +
    wage)[\[10\]](https://www.irs.gov/pub/irs-drop/n-25-05.pdf?utm_source=telarus?wtime#:~:text=SECTION%203,See),
    HDD at \\\$13/TB[\[11\]](https://diskprices.com/#:~:text=%240,6Tb)
    or tape
    \\\$5/TB[\[12\]](https://diskprices.com/#:~:text=%240,8%20Data%20Cartridge%2FTape).
    Fiber: assume \\\$5/ft aerial, \\\$12/ft underground in rural U.S.
    (Medium).
-   **Confidence Levels**: Starlink official prices (High). Starlink
    speed/latency data (High from Ookla). User forum reports on priority
    (Low). Cloud appliance fees (High). DIY cost estimates
    (Low--Medium). Rural fiber (Medium for U.S., Low for non-U.S.).
-   **Data Gaps**: Real-world uplink speeds, cell-based (bulk fiber)
    throughput tests; broad Sneakernet studies; rural build costs
    outside N. America. Note that quoted prices are 2025 USD; some
    sources (e.g. \[60\]) list mid-2025 prices, others expected to hold.

**Sources:** Official Starlink
site[\[1\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=Reliable%20high,a%20hardware%20cost%20of%20%24349)[\[2\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=LOCAL%20PRIORITY%20),
Ookla Speedtest
data[\[4\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=,84%20Mbps%20in%20Q1%202025)[\[5\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=Starlink%20users%20in%20the%20U,median%20latency%20of%2045%20ms),
user
reports[\[21\]](https://www.reddit.com/r/Starlink/comments/16e0igw/starlink_standard_vs_priority/#:~:text=Based%20on%20experience%2C%20prioritized%20or,Virginia%20regardless%20of%20your%20plan)[\[22\]](https://www.reddit.com/r/Starlink/comments/16e0igw/starlink_standard_vs_priority/#:~:text=IMO%20the%20biggest%20reason%20for,variable%20nature%20of%20Starlink%27s%20network),
AWS/Azure pricing
pages[\[8\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=Service%20Fee%24300%20per%20device%24500%20per,day%24125%20per%20day%24165%20per%20day)[\[9\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=Data%20Box%20Data%20Box%20Disk,Starting%20at%29%20%241%2C500),
industry
reports[\[28\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,54%2Fft%20for%20urban%20areas),
and public cost-data
aggregators[\[12\]](https://diskprices.com/#:~:text=%240,8%20Data%20Cartridge%2FTape)[\[11\]](https://diskprices.com/#:~:text=%240,6Tb)[\[10\]](https://www.irs.gov/pub/irs-drop/n-25-05.pdf?utm_source=telarus?wtime#:~:text=SECTION%203,See).
(All values are in 2025 USD; ranges indicate low/typical/high
scenarios.)

[\[1\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=Reliable%20high,a%20hardware%20cost%20of%20%24349)
[\[3\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=Service%20plan%20upgrades%20will%20be,connectivity%20whenever%20you%20need%20it)
[\[24\]](https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa#:~:text=GIGABIT%20SPEEDS%20AVAILABLE%20IN%202026)
Starlink Business \| Fixed Site

<https://starlink.com/business/fixed-site?srsltid=AfmBOop-5YRkUlk5ABgzk3kTlKthkbhlHrE_WdBH5ybdzUI5-xyDWcTa>

[\[2\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=LOCAL%20PRIORITY%20)
[\[6\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=Unlimited%20Data%20at%20up%20to,Includes%20service%20level%20agreement)
[\[17\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=%2B50GB)
[\[18\]](https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b#:~:text=GLOBAL%20PRIORITY%20)
Starlink \| Service Plans

<https://starlink.com/service-plans/business?srsltid=AfmBOopUliD8LKLrGoB3TJbmQdUEn9LKKo8uyFIkl3zyPFCO-9htvr2b>

[\[4\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=,84%20Mbps%20in%20Q1%202025)
[\[5\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=Starlink%20users%20in%20the%20U,median%20latency%20of%2045%20ms)
[\[19\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=%2A%20Only%2017.4,to%20its%20low%20upload%20speeds)
[\[20\]](https://www.ookla.com/articles/starlink-us-performance-2025#:~:text=,65%20Mbps%20in%20Alaska)
Starlink's U.S. Performance is on the Rise, Making it a Viable Broadband
Option in Some States \| Ookla®

<https://www.ookla.com/articles/starlink-us-performance-2025>

[\[7\]](https://seabits.com/starlink-performance-kit-unboxing/#:~:text=Starlink%20released%20a%20new%20version,my%20initial%20unboxing%20and%20impressions)
Starlink Performance Kit Unboxing

<https://seabits.com/starlink-performance-kit-unboxing/>

[\[8\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=Service%20Fee%24300%20per%20device%24500%20per,day%24125%20per%20day%24165%20per%20day)
[\[9\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=Data%20Box%20Data%20Box%20Disk,Starting%20at%29%20%241%2C500)
[\[27\]](https://www.resilio.com/blog/aws-snowball-vs-azure-data-box#:~:text=To%20give%20you%20a%20better,provide%20two%20example%20scenarios%20below)
AWS Snowball vs Azure Data Box vs Resilio Connect: Which Is Best?

<https://www.resilio.com/blog/aws-snowball-vs-azure-data-box>

[\[10\]](https://www.irs.gov/pub/irs-drop/n-25-05.pdf?utm_source=telarus?wtime#:~:text=SECTION%203,See)
N-2025-05

<https://www.irs.gov/pub/irs-drop/n-25-05.pdf?utm_source=telarus?wtime>

[\[11\]](https://diskprices.com/#:~:text=%240,6Tb)
[\[12\]](https://diskprices.com/#:~:text=%240,8%20Data%20Cartridge%2FTape)
Disk Prices (US)

<https://diskprices.com/>

[\[13\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,per%20foot%20for%20aerial%20deployment)
[\[14\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,54%2Fft%20for%20urban%20areas)
[\[15\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=%245,in%20rocky%20terrain%20at%20%2420%2Fft)
[\[16\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=underground,54%2Fft%20for%20urban%20areas)
[\[28\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,54%2Fft%20for%20urban%20areas)
[\[29\]](https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report#:~:text=,54%2Fft%20for%20urban%20areas)
Fiber Deployment Annual Report \| Benton Institute for Broadband &
Society

<https://www.benton.org/headlines/fiber-broadband-association-fiber-deployment-annual-report>

[\[21\]](https://www.reddit.com/r/Starlink/comments/16e0igw/starlink_standard_vs_priority/#:~:text=Based%20on%20experience%2C%20prioritized%20or,Virginia%20regardless%20of%20your%20plan)
[\[22\]](https://www.reddit.com/r/Starlink/comments/16e0igw/starlink_standard_vs_priority/#:~:text=IMO%20the%20biggest%20reason%20for,variable%20nature%20of%20Starlink%27s%20network)
[\[23\]](https://www.reddit.com/r/Starlink/comments/16e0igw/starlink_standard_vs_priority/#:~:text=%E2%80%A2%20%202y%20ago)
Starlink Standard vs Priority : r/Starlink

<https://www.reddit.com/r/Starlink/comments/16e0igw/starlink_standard_vs_priority/>

[\[25\]](https://aws.amazon.com/snowball/pricing/#:~:text=Suppose%20you%20use%20the%20Snowball,day%20fees.%20Since%20you%20are)
[\[26\]](https://aws.amazon.com/snowball/pricing/#:~:text=You%20would%20pay%20a%20service,ship%20it%20back%20to%20AWS)
AWS Snowball Pricing \| Amazon Web Services

<https://aws.amazon.com/snowball/pricing/>
