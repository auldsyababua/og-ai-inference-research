# NVIDIA Multi-Instance GPU (MIG) User Guide

**Source:** https://docs.nvidia.com/datacenter/tesla/mig-user-guide/
**Scraped:** $(date +%Y-%m-%d)
**Purpose:** Complete MIG configuration guide for H100 GPU partitioning

---


---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
:::


 {.toctree-wrapper .compound}
:::
:::

 {.prev-next-info}
next

Introduction
:::
:::
:::


:::
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {.prev-next-info}
previous

MIG User Guide
:::

[](supported-gpus.html "next page"){.right-next}


:::
:::


:::
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


[]{.fa-solid .fa-outdent}
:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {#terminology .section}
Terminology[\#](concepts.html#terminology "Link to this heading")
------------------------------------------------------------------------------

This section introduces some terminology used to describe the concepts
behind MIG.

**Streaming Multiprocessor**

A streaming multiprocessor (SM) executes compute instructions on the
GPU.

**GPU Context**

A GPU context is analogous to a CPU process. It encapsulates all the
resources necessary to execute operations on the GPU, including a
distinct address space, memory allocations, etc. A GPU context has the
following properties:

-   Fault isolation

-   Individually scheduled

-   Distinct address space

**GPU Engine**

A GPU engine is what executes work on the GPU. The most commonly used
engine is the Compute/Graphics engine that executes the compute
instructions. Other engines include the copy engine (CE) that is
responsible for performing DMAs, NVDEC for video decoding, NVENC for
encoding, etc. Each engine can be scheduled independently and execute
work for different GPU contexts.

**GPU Memory Slice**

A GPU memory slice is the smallest fraction of the GPU's memory,
including the corresponding memory controllers and cache. A GPU memory
slice is roughly one eighth of the total GPU memory resources, including
both capacity and bandwidth.

**GPU SM Slice**

A GPU SM slice is the smallest fraction of the SMs on the GPU. A GPU SM
slice is roughly one seventh of the total number of SMs available in the
GPU when configured in MIG mode.

**GPU Slice**

A GPU slice is the smallest fraction of the GPU that combines a single
GPU memory slice and a single GPU SM slice.

**GPU Instance**

A GPU Instance (GI) is a combination of GPU slices and GPU engines
(DMAs, NVDECs, and so on). Anything within a GPU instance always shares
all the GPU memory slices and other GPU engines, but it's SM slices can
be further subdivided into compute instances (CI). A GPU instance
provides memory QoS. Each GPU slice includes dedicated GPU memory
resources which limit both the available capacity and bandwidth, and
provide memory QoS. Each GPU memory slice gets 1/8 of the total GPU
memory resources and each GPU SM slice gets 1/7 of the total number of
SMs.

**Compute Instance**

A GPU instance can be subdivided into multiple compute instances. A
Compute Instance (CI) contains a subset of the parent GPU instance's SM
slices and other GPU engines (DMAs, NVDECs, etc.). The CIs share memory
and engines.
:::

 {.admonition .note}
Note

The table below shows the profile names on the A100-SXM4-40GB product.
For A100-SXM4-80GB, the profile names will change according to the
memory proportion - for example, `1g.10gb`{.docutils .literal
.notranslate}, `2g.20gb`{.docutils .literal .notranslate},
`3g.40gb`{.docutils .literal .notranslate}, `4g.40gb`{.docutils .literal
.notranslate}, `7g.80gb`{.docutils .literal .notranslate} respectively.
:::

For a list of all supported combinations of profiles on MIG-enabled
GPUs, refer to the section on [[supported profiles]{.std
.std-ref}](mig-device-names.html#mig-device-names){.reference
.internal}.


The diagram below shows a pictorial representation of how to build all
valid combinations of GPU instances.

![[Figure 7 ]{.caption-number}[MIG Profiles on
A100]{.caption-text}[\#](concepts.html#mig-partitioning-ex6 "Link to this image")](_images/mig-partitioning-ex6.png)

In this diagram, a valid combination can be built by starting with an
instance profile on the left and combining it with other instance
profiles as you move to the right, such that no two profiles overlap
vertically. For a list of all supported combinations and placements of
profiles on A100 and A30, refer to the section on [[supported
profiles]{.std
.std-ref}](mig-device-names.html#mig-device-names){.reference
.internal}.

Note that prior to NVIDIA driver release R510, the combination of a (4
memory, 4 compute) and a (4 memory, 3 compute) profile was not
supported. This restriction no longer applies on newer drivers.

![[Figure 8 ]{.caption-number}[Profile Placements on
A100]{.caption-text}[\#](concepts.html#mig-partitioning-ex7 "Link to this image")](_images/mig-partitioning-ex7.png)

Note that the diagram represents the physical layout of where the GPU
Instances will exist once they are instantiated on the GPU. As GPU
Instances are created and destroyed at different locations,
fragmentation can occur, and the physical position of one GPU Instance
will play a role in which other GPU Instances can be instantiated next
to it.
:::

 {.pst-scrollable-table-container}
                             Streams          MPS                                     MIG
  -------------------------- ---------------- --------------------------------------- -------------
  Partition Type             Single Process   Logical                                 Physical
  Max Partitions             Unlimited        48                                      7
  SM Performance Isolation   No               Yes (by percentage, not partitioning)   Yes
  Memory Protection          No               Yes                                     Yes
  Memory Bandwidth QoS       No               No                                      Yes
  Error Isolation            No               No                                      Yes
  Cross-Partition Interop    Always           IPC                                     Limited IPC
  Reconfigure                Dynamic          Process Launch                          When Idle

  : [Table 3 ]{.caption-number}[CUDA Concurrency
  Mechanisms]{.caption-text}[\#](concepts.html#id3 "Link to this table")
:::
:::
:::

 {.prev-next-info}
previous

Virtualization
:::

[](deployment-considerations.html "next page"){.right-next}


:::
:::

 {.sidebar-secondary-items .sidebar-secondary__inner}
 {#pst-page-navigation-heading-2 .page-toc .tocsection .onthispage}
On this page
:::

-   [Terminology](concepts.html#terminology){.reference .internal
    .nav-link}
-   [Partitioning](concepts.html#partitioning){.reference .internal
    .nav-link}
-   [CUDA Concurrency
    Mechanisms](concepts.html#cuda-concurrency-mechanisms){.reference
    .internal .nav-link}
:::
:::
:::
:::
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {.pst-scrollable-table-container}
  Product                                            Architecture                 Microarchitecture   Compute Capability   Memory Size   Max Number of Instances
  -------------------------------------------------- ---------------------------- ------------------- -------------------- ------------- -------------------------
  RTX PRO 6000 Blackwell Server Edition              Blackwell                    GB202               12.0                 96GB          4
  RTX PRO 6000 Blackwell Workstation Edition         Blackwell                    GB202               12.0                 96GB          4
  RTX PRO 6000 Blackwell Max-Q Workstation Edition   Blackwell                    GB202               12.0                 96GB          4
  RTX PRO 5000 Blackwell                             Blackwell                    GB202               12.0                 48GB          2
  GB200                                              Blackwell                    GB100               10.0                 186GB         7
  B200                                               Blackwell                    GB100               10.0                 180GB         7
  H100-SXM5                                          Hopper                       GH100               9.0                  80GB          7
  H100-PCIE                                          Hopper                       GH100               9.0                  80GB          7
  H100-SXM5                                          Hopper                       GH100               9.0                  94GB          7
  H100-PCIE                                          Hopper                       GH100               9.0                  94GB          7
  H100 on GH200                                      Hopper                       GH100               9.0                  96GB          7
  H20                                                Hopper                       GH100               9.0                  96GB          7
  H200-SXM5                                          Hopper                       GH100               9.0                  141GB         7
  H200 NVL                                           Hopper                       GH100               9.0                  141GB         7
  A100-SXM4                                          NVIDIA Ampere architecture   GA100               8.0                  40GB          7
  A100-SXM4                                          NVIDIA Ampere architecture   GA100               8.0                  80GB          7
  A100-PCIE                                          NVIDIA Ampere architecture   GA100               8.0                  40GB          7
  A100-PCIE                                          NVIDIA Ampere architecture   GA100               8.0                  80GB          7
  A30                                                NVIDIA Ampere architecture   GA100               8.0                  24GB          4

  : [Table 1 ]{.caption-number}[Supported GPU
  Products]{.caption-text}[\#](supported-gpus.html#id2 "Link to this table")
:::

Additionally, MIG is supported on systems that include the supported
products above such as DGX, DGX Station and HGX.
:::

 {.prev-next-info}
previous

Introduction
:::

[](supported-configurations.html "next page"){.right-next}


:::
:::


:::
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {.prev-next-info}
previous

Supported GPUs
:::

[](virtualization.html "next page"){.right-next}


:::
:::


:::
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


[]{.fa-solid .fa-outdent}
:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {#a30-mig-profiles .section}
A30 MIG Profiles[\#](supported-mig-profiles.html#a30-mig-profiles "Link to this heading")
------------------------------------------------------------------------------------------------------

The following diagram shows the profiles supported on the NVIDIA A30:

![[Figure 10 ]{.caption-number}[Profiles on
A30]{.caption-text}[\#](supported-mig-profiles.html#a30-profiles-v2 "Link to this image")](_images/a30-profiles-v2.png)

The following table shows the supported profiles on the A30-24GB
product.


:::

 {.pst-scrollable-table-container}
  Profile Name    Fraction of Memory   Fraction of SMs   Hardware Units            L2 Cache Size   Copy Engines   Number of Instances Available
  --------------- -------------------- ----------------- ------------------------- --------------- -------------- ------------------------------------------------------
  MIG 1g.5gb      1/8                  1/7               0 NVDECs /0 JPEG /0 OFA   1/8             1              7
  MIG 1g.5gb+me   1/8                  1/7               1 NVDEC /1 JPEG /1 OFA    1/8             1              1 (A single 1g profile can include media extensions)
  MIG 1g.10gb     1/8                  1/7               1 NVDEC /0 JPEG /0 OFA    1/8             1              4
  MIG 2g.10gb     2/8                  2/7               1 NVDEC /0 JPEG /0 OFA    2/8             2              3
  MIG 3g.20gb     4/8                  3/7               2 NVDECs /0 JPEG /0 OFA   4/8             3              2
  MIG 4g.20gb     4/8                  4/7               2 NVDECs /0 JPEG /0 OFA   4/8             4              1
  MIG 7g.40gb     Full                 7/7               5 NVDECs /1 JPEG /1 OFA   Full            7              1

  : [Table 6 ]{.caption-number}[GPU Instance Profiles on
  A100]{.caption-text}[\#](supported-mig-profiles.html#id2 "Link to this table")
:::


:::

 {.pst-scrollable-table-container}
  Profile Name     Fraction of Memory   Fraction of SMs   Hardware Units            L2 Cache Size   Copy Engines   Number of Instances Available
  ---------------- -------------------- ----------------- ------------------------- --------------- -------------- ------------------------------------------------------
  MIG 1g.10gb      1/8                  1/7               1 NVDEC /1 JPEG /0 OFA    1/8             1              7
  MIG 1g.10gb+me   1/8                  1/7               1 NVDEC /1 JPEG /1 OFA    1/8             1              1 (A single 1g profile can include media extensions)
  MIG 1g.20gb      1/4                  1/7               1 NVDEC /1 JPEG /0 OFA    1/8             1              4
  MIG 2g.20gb      2/8                  2/7               2 NVDECs /2 JPEG /0 OFA   2/8             2              3
  MIG 3g.40gb      4/8                  3/7               3 NVDECs /3 JPEG /0 OFA   4/8             3              2
  MIG 4g.40gb      4/8                  4/7               4 NVDECs /4 JPEG /0 OFA   4/8             4              1
  MIG 7g.80gb      Full                 7/7               7 NVDECs /7 JPEG /1 OFA   Full            8              1

  : [Table 7 ]{.caption-number}[GPU Instance Profiles on
  H100]{.caption-text}[\#](supported-mig-profiles.html#id3 "Link to this table")
:::

The following table shows the supported profiles on the H100 94GB
product (PCIe and SXM5).


The following table shows the supported profiles on the H100 96GB
product (H100 on GH200).


:::

 {.pst-scrollable-table-container}
  Profile Name     Fraction of Memory   Fraction of SMs   Hardware Units            L2 Cache Size   Copy Engines   Number of Instances Available
  ---------------- -------------------- ----------------- ------------------------- --------------- -------------- ------------------------------------------------------
  MIG 1g.18gb      1/8                  1/7               1 NVDECs /1 JPEG /0 OFA   1/8             1              7
  MIG 1g.18gb+me   1/8                  1/7               1 NVDEC /1 JPEG /1 OFA    1/8             1              1 (A single 1g profile can include media extensions)
  MIG 1g.35gb      1/4                  1/7               1 NVDECs /1 JPEG /0 OFA   1/8             1              4
  MIG 2g.35gb      2/8                  2/7               2 NVDECs /2 JPEG /0 OFA   2/8             2              3
  MIG 3g.71gb      4/8                  3/7               3 NVDECs /3 JPEG /0 OFA   4/8             3              2
  MIG 4g.71gb      4/8                  4/7               4 NVDECs /4 JPEG /0 OFA   4/8             4              1
  MIG 7g.141gb     Full                 7/7               7 NVDECs /7 JPEG /1 OFA   Full            8              1

  : [Table 8 ]{.caption-number}[GPU Instance Profiles on
  H200]{.caption-text}[\#](supported-mig-profiles.html#id4 "Link to this table")
:::
:::

 {.pst-scrollable-table-container}
[Table 9 ]{.caption-number}[GPU Instance Profiles on
B200]{.caption-text}[\#](supported-mig-profiles.html#id5 "Link to this table")

Profile Name
:::
:::
:::
:::
:::
:::
:::
:::

Fraction of Memory

Fraction of SMs

Hardware Units

L2 Cache Size

Copy Engines

Number of Instances

NVDEC

JPEG

OFA

MIG 1g.23gb

1/8

1/7

1

1

0

1/8

2

7

MIG 1g.23gb+me

1/8

1/7

1

1

1

1/8

2

1 (A single 1g profile can include media extensions)

MIG 1g.45gb

2/8

1/7

1

1

0

2/8

2

4

MIG 2g.45gb

2/8

2/7

1

1

0

2/8

3

3

MIG 3g.90gb

4/8

3/7

1

1

0

4/8

6

2

MIG 4g.90gb

4/8

4/7

1

1

0

4/8

8

1

MIG 7g.180gb

Full

Full

1

1

1

Full

16

1

 {.pst-scrollable-table-container}
[Table 10 ]{.caption-number}[GPU Instance Profiles on RTX PRO
5000]{.caption-text}[\#](supported-mig-profiles.html#id6 "Link to this table")

Profile Name
:::
:::

Fraction of Memory

Fraction of SMs

Hardware Units

L2 Cache Size

Copy Engines

Number of Instances

NVDEC

NVENC

JPEG

OFA

MIG 1g.12gb

1/4

1/4

1

1

1

0

1/4

1

1

MIG 1g.12gb+me

1/4

1/4

1

1

1

1

1/4

1

1

MIG 1g.12gb+gfx

1/4

1/4

1

1

1

0

1/4

1

1

MIG 1g.12gb-me

1/4

1/4

0

0

0

0

1/4

1

3

MIG 2g.24gb-me

1/2

1/2

0

0

0

0

1/2

2

1

MIG 4g.48gb

Full

Full

3

3

1

1

Full

4

1

MIG 4g.48gb+gfx

Full

Full

3

3

1

1

Full

4

1

 {.pst-scrollable-table-container}
[Table 11 ]{.caption-number}[GPU Instance Profiles on RTX PRO
6000]{.caption-text}[\#](supported-mig-profiles.html#id7 "Link to this table")

Profile Name
:::
:::

Fraction of Memory

Fraction of SMs

Hardware Units

L2 Cache Size

Copy Engines

Number of Instances

NVDEC

NVENC

JPEG

OFA

MIG 1g.24gb

1/4

1/4

1

1

1

0

1/4

1

4

MIG 1g.24gb+me

1/4

1/4

1

1

1

1

1/4

1

1

MIG 1g.24gb+gfx

1/4

1/4

1

1

1

0

1/4

1

4

MIG 1g.24gb+me.all

1/4

1/4

4

4

4

1

1/4

1

1

MIG 1g.24gb-me

1/4

1/4

0

0

0

0

1/4

1

4

MIG 2g.48gb

1/2

1/2

2

2

2

0

1/2

2

2

MIG 2g.48gb+gfx

1/2

1/2

2

2

2

0

1/2

2

2

MIG 2g.48gb+me.all

1/2

1/2

4

4

4

1

1/2

2

1

MIG 2g.48gb-me

1/2

1/2

0

0

0

0

1/2

2

2

MIG 4g.96gb

Full

Full

4

4

4

1

Full

4

1

MIG 4g.96gb+gfx

Full

Full

4

4

4

1

Full

4

1

**Universal MIG**

Universal MIG enables both compute and graphics workloads to run on the
same GPU with hardware isolation. This feature is available on RTX PRO
6000 GPUs. `+gfx profiles`{.docutils .literal .notranslate} which are
new in GB20X architecture, enables graphics support in MIG instances.

**Profile References**

-   `+me profiles`{.docutils .literal .notranslate}: Include at least
    one media engine (NVDEC, NVENC, NVJPG, or OFA).

-   `+gfx`{.docutils .literal .notranslate}: Adds support for graphics
    APIs (new in GB20X).

-   `+me.all`{.docutils .literal .notranslate}: Allocates all available
    media engines to this instance (does not include graphics support).

-   `-me`{.docutils .literal .notranslate}: Excludes all media engines
    for pure compute workloads.

 {.prev-next-info}
previous

MIG Device Names
:::

[](getting-started-with-mig.html "next page"){.right-next}


:::

 {.sidebar-secondary-items .sidebar-secondary__inner}
 {#pst-page-navigation-heading-2 .page-toc .tocsection .onthispage}
On this page
:::

-   [A30 MIG
    Profiles](supported-mig-profiles.html#a30-mig-profiles){.reference
    .internal .nav-link}
-   [A100 MIG
    Profiles](supported-mig-profiles.html#a100-mig-profiles){.reference
    .internal .nav-link}
-   [H100 MIG
    Profiles](supported-mig-profiles.html#h100-mig-profiles){.reference
    .internal .nav-link}
-   [H200 MIG
    Profiles](supported-mig-profiles.html#h200-mig-profiles){.reference
    .internal .nav-link}
-   [B200 MIG
    Profiles](supported-mig-profiles.html#b200-mig-profiles){.reference
    .internal .nav-link}
-   [RTX PRO 5000 Blackwell MIG
    Profiles](supported-mig-profiles.html#rtx-pro-5000-blackwell-mig-profiles){.reference
    .internal .nav-link}
-   [RTX PRO 6000 Blackwell MIG
    Profiles](supported-mig-profiles.html#rtx-pro-6000-blackwell-mig-profiles){.reference
    .internal .nav-link}
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


[]{.fa-solid .fa-outdent}
:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {#prerequisites .section}
Prerequisites[\#](getting-started-with-mig.html#prerequisites "Link to this heading")
--------------------------------------------------------------------------------------------------

The following prerequisites and minimum software versions are
recommended when using supported GPUs in MIG mode:

-   MIG is supported only on GPUs and systems listed [[here]{.std
    .std-ref}](supported-gpus.html#supported-gpus){.reference
    .internal}.

-   It is recommended to install the latest NVIDIA datacenter driver.
    The minimum versions are given in the below table:

    

-   Linux operating system distributions supported by
    [CUDA](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html){.reference
    .external}.

-   If running containers or using Kubernetes, then:

    -   NVIDIA Container Toolkit (nvidia-docker2): v2.5.0 or later

    -   NVIDIA K8s Device Plugin: v0.7.0 or later

    -   NVIDIA gpu-feature-discovery: v0.2.0 or later

MIG can be managed programmatically using NVIDIA Management Library
(NVML) APIs or its command-line-interface, `nvidia-smi`{.docutils
.literal .notranslate}. Note that for brevity, some of the nvidia-smi
output in the following examples may be cropped to showcase the relevant
sections of interest.

For more information on the MIG commands, see the `nvidia-smi`{.docutils
.literal .notranslate} man page or `nvidia-smi mig --help`{.docutils
.literal .notranslate}. For information on the MIG management APIs, see
the NVML header (`nvml.h`{.docutils .literal .notranslate}) included in
the CUDA Toolkit packages (`cuda-nvml-dev-*`{.docutils .literal
.notranslate}; installed under
`/usr/local/cuda/include/nvml.h`{.docutils .literal .notranslate}). For
automated tooling support with configuring MIG, refer to the [NVIDIA MIG
Partition Editor](https://github.com/nvidia/mig-parted){.reference
.external} (or `mig-parted`{.docutils .literal .notranslate}) tools.

 {.pst-scrollable-table-container}
  GPU                                                Minimum vBIOS version
  -------------------------------------------------- -----------------------
  RTX PRO 5000 Blackwell                             98.02.73.00.00
  RTX PRO 6000 Blackwell Workstation Edition         98.02.55.00.00
  RTX PRO 6000 Blackwell Max-Q Workstation Edition   98.02.6A.00.00
:::

To check the current vBIOS version:

 {.highlight}
    $ nvidia-smi --query-gpu=vbios_version --format=csv
:::
:::

If a vBIOS update is needed, contact your reseller or system provider
for assistance.

Display mode by default will be set to graphics, this must be set to
compute before MIG can be enabled for Workstation Edition and Max-Q
Workstation Edition GPUs. This is done using
[DisplayModeSelector](https://developer.nvidia.com/displaymodeselector){.reference
.external} (\>=1.72.0).


To set display mode to compute:

 {.highlight}
    sudo ./DisplayModeSelector --gpumode=compute --gpu=<GPU_ID>
:::
:::

To switch back to graphics mode:

 {.highlight}
    sudo ./DisplayModeSelector --gpumode=graphics --gpu=<GPU_ID>
:::
:::
:::
:::

 {.highlight-text .notranslate}

:::

MIG mode can be enabled on a per-GPU basis with the following command:

 {.highlight}
    nvidia-smi -i <GPU IDs> -mig 1
:::
:::

The GPUs can be selected using comma separated GPU indexes, PCI Bus IDs
or UUIDs. If no GPU ID is specified, then MIG mode is applied to all the
GPUs on the system.

When MIG is enabled on the GPU, depending on the GPU product, the driver
will attempt to reset the GPU so that MIG mode can take effect.

 {.highlight}
    $ sudo nvidia-smi -i 0 -mig 1
    Enabled MIG Mode for GPU 00000000:36:00.0
    All done.

    $ nvidia-smi -i 0 --query-gpu=pci.bus_id,mig.mode.current --format=csv
    pci.bus_id, mig.mode.current
    00000000:36:00.0, Enabled
:::
:::


 {.admonition .note}
Note

If you are using MIG inside a VM with NVIDIA Ampere GPUs (A100 or A30)
in passthrough, then you may need to reboot the VM to allow the GPU to
be in MIG mode as in some cases, GPU reset is not allowed via the
hypervisor for security reasons. This can be seen in the following
example:

 {.highlight}
    $ sudo nvidia-smi -i 0 -mig 1
    Warning: MIG mode is in pending enable state for GPU 00000000:00:03.0:Not Supported
    Reboot the system or try nvidia-smi --gpu-reset to make MIG mode effective on GPU 00000000:00:03.0
    All done.

    $ sudo nvidia-smi --gpu-reset
    Resetting GPU 00000000:00:03.0 is not supported.
:::
:::
:::
:::

 {.highlight-text .notranslate}

:::

In this specific DGX example, you would have to stop the
`nvsm`{.docutils .literal .notranslate} and `dcgm`{.docutils .literal
.notranslate} services, enable MIG mode on the desired GPU and then
restore the monitoring services:

 {.highlight}
    $ sudo systemctl stop nvsm

    $ sudo systemctl stop dcgm

    $ sudo nvidia-smi -i 0 -mig 1
    Enabled MIG Mode for GPU 00000000:07:00.0
    All done.
:::
:::

The examples shown in the document use super-user privileges. As
described in the [[Device Nodes]{.std
.std-ref}](device-nodes-and-capabilities.html#dev-based-nvidia-capabilities){.reference
.internal} section, granting read access to `mig/config`{.docutils
.literal .notranslate} capabilities allows non-root users to manage
instances once the GPU has been configured into MIG mode. The default
file permissions on the `mig/config`{.docutils .literal .notranslate}
file are as follows.

 {.highlight}
    $ ls -l /proc/driver/nvidia/capabilities/*
    /proc/driver/nvidia/capabilities/mig:
    total 0
    -r-------- 1 root root 0 May 24 16:10 config
    -r--r--r-- 1 root root 0 May 24 16:10 monitor
:::
:::
:::
:::

 {.highlight-text .notranslate}

:::

List the possible placements available using the following command. The
syntax of the placement is `{<index>}:<GPU Slice Count>`{.docutils
.literal .notranslate} and shows the placement of the instances on the
GPU. The placement index shown indicates how the profiles are mapped on
the GPU as shown in the [[supported profiles tables]{.std
.std-ref}](mig-device-names.html#mig-device-names){.reference
.internal}.

 {.highlight}
    $ nvidia-smi mig -lgipp
    GPU  0 Profile ID 19 Placements: {0,1,2,3,4,5,6}:1
    GPU  0 Profile ID 20 Placements: {0,1,2,3,4,5,6}:1
    GPU  0 Profile ID 15 Placements: {0,2,4,6}:2
    GPU  0 Profile ID 14 Placements: {0,2,4}:2
    GPU  0 Profile ID  9 Placements: {0,4}:4
    GPU  0 Profile ID  5 Placement : {0}:4
    GPU  0 Profile ID  0 Placement : {0}:8
:::
:::

The command shows that the user can create two instances of type
`3g.20gb`{.docutils .literal .notranslate} (profile ID 9) or seven
instances of `1g.5gb`{.docutils .literal .notranslate} (profile ID 19).
:::

 {.admonition .note}
Note

Without creating GPU instances (and corresponding compute instances),
CUDA workloads cannot be run on the GPU. In other words, simply enabling
MIG mode on the GPU is not sufficient. Also note that, the created MIG
devices are not persistent across system reboots. Thus, the user or
system administrator needs to recreate the desired MIG configurations if
the GPU or system is reset. For automated tooling support for this
purpose, refer to the [NVIDIA MIG Partition
Editor](https://github.com/nvidia/mig-parted){.reference .external} (or
`mig-parted`{.docutils .literal .notranslate}) tool, including creating
a systemd service that could recreate the MIG geometry at system
startup.
:::

The following example shows how the user can create GPU instances (and
corresponding compute instances). In this example, the user can create
two GPU instances (of type `3g.20gb`{.docutils .literal .notranslate}),
with each GPU instance having half of the available compute and memory
capacity. In this example, we purposefully use profile ID and short
profile name to showcase how either option can be used:

 {.highlight}
    $ sudo nvidia-smi mig -cgi 9,3g.20gb -C
    Successfully created GPU instance ID  2 on GPU  0 using profile MIG 3g.20gb (ID  9)
    Successfully created compute instance ID  0 on GPU  0 GPU instance ID  2 using profile MIG 3g.20gb (ID  2)
    Successfully created GPU instance ID  1 on GPU  0 using profile MIG 3g.20gb (ID  9)
    Successfully created compute instance ID  0 on GPU  0 GPU instance ID  1 using profile MIG 3g.20gb (ID  2)
:::
:::

Now list the available GPU instances:

 {.highlight}
    $ sudo nvidia-smi mig -lgi
    +----------------------------------------------------+
    | GPU instances:                                     |
    | GPU   Name          Profile  Instance   Placement  |
    |                       ID       ID       Start:Size |
    |====================================================|
    |   0  MIG 3g.20gb       9        1          4:4     |
    +----------------------------------------------------+
    |   0  MIG 3g.20gb       9        2          0:4     |
    +----------------------------------------------------+
:::
:::

Now verify that the GIs and corresponding CIs are created:

 {.highlight}
    $ nvidia-smi
    +-----------------------------------------------------------------------------+
    | MIG devices:                                                                |
    +------------------+----------------------+-----------+-----------------------+
    | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
    |      ID  ID  Dev |                      | SM     Unc| CE  ENC  DEC  OFA  JPG|
    |                  |                      |        ECC|                       |
    |==================+======================+===========+=======================|
    |  0    1   0   0  |     11MiB / 20224MiB | 42      0 |  3   0    2    0    0 |
    +------------------+----------------------+-----------+-----------------------+
    |  0    2   0   1  |     11MiB / 20096MiB | 42      0 |  3   0    2    0    0 |
    +------------------+----------------------+-----------+-----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |  No running processes found                                                 |
    +-----------------------------------------------------------------------------+
:::
:::

 {.highlight-text .notranslate}

:::

Example 2: Creation of a 3-2-1-1 geometry.

Note: Due to a known issue with the APIs, the profile ID 9 or
`3g.20gb`{.docutils .literal .notranslate} must be specified first in
order. Not doing so, will result in the following error:

> <div>
>
>  {.highlight}
>     $ sudo nvidia-smi mig -cgi 19,19,14,9
>     Successfully created GPU instance ID 13 on GPU  0 using profile MIG 1g.5gb (ID 19)
>     Successfully created GPU instance ID 11 on GPU  0 using profile MIG 1g.5gb (ID 19)
>     Successfully created GPU instance ID  3 on GPU  0 using profile MIG 2g.10gb (ID 14)
>     Unable to create a GPU instance on GPU  0 using profile 9: Insufficient Resources
>     Failed to create GPU instances: Insufficient Resources
> :::
> :::
>
> </div>

Specify the correct order for the 3g.20gb profile. The remaining
combinations of the profiles do not have this requirement.

 {.highlight}
    $ sudo nvidia-smi mig -cgi 9,19,14,19
    Successfully created GPU instance ID  2 on GPU  0 using profile MIG 3g.20gb (ID  9)
    Successfully created GPU instance ID  7 on GPU  0 using profile MIG 1g.5gb (ID 19)
    Successfully created GPU instance ID  4 on GPU  0 using profile MIG 2g.10gb (ID 14)
    Successfully created GPU instance ID  8 on GPU  0 using profile MIG 1g.5gb (ID 19)


    $ sudo nvidia-smi mig -lgi
    +----------------------------------------------------+
    | GPU instances:                                     |
    | GPU   Name          Profile  Instance   Placement  |
    |                       ID       ID       Start:Size |
    |====================================================|
    |   0  MIG 1g.5gb       19        7          0:1     |
    +----------------------------------------------------+
    |   0  MIG 1g.5gb       19        8          1:1     |
    +----------------------------------------------------+
    |   0  MIG 2g.10gb      14        4          2:2     |
    +----------------------------------------------------+
    |   0  MIG 3g.20gb       9        2          4:4     |
    +----------------------------------------------------+
:::
:::

Example 3: Creation of a 2-1-1-1-1-1 geometry:

 {.highlight}
    $ sudo nvidia-smi mig -cgi 14,19,19,19,19,19
    Successfully created GPU instance ID  5 on GPU  0 using profile MIG 2g.10gb (ID 14)
    Successfully created GPU instance ID 13 on GPU  0 using profile MIG 1g.5gb (ID 19)
    Successfully created GPU instance ID  7 on GPU  0 using profile MIG 1g.5gb (ID 19)
    Successfully created GPU instance ID  8 on GPU  0 using profile MIG 1g.5gb (ID 19)
    Successfully created GPU instance ID  9 on GPU  0 using profile MIG 1g.5gb (ID 19)
    Successfully created GPU instance ID 10 on GPU  0 using profile MIG 1g.5gb (ID 19)


    $ sudo nvidia-smi mig -lgi
    +----------------------------------------------------+
    | GPU instances:                                     |
    | GPU   Name          Profile  Instance   Placement  |
    |                       ID       ID       Start:Size |
    |====================================================|
    |   0  MIG 1g.5gb       19        7          0:1     |
    +----------------------------------------------------+
    |   0  MIG 1g.5gb       19        8          1:1     |
    +----------------------------------------------------+
    |   0  MIG 1g.5gb       19        9          2:1     |
    +----------------------------------------------------+
    |   0  MIG 1g.5gb       19       10          3:1     |
    +----------------------------------------------------+
    |   0  MIG 1g.5gb       19       13          6:1     |
    +----------------------------------------------------+
    |   0  MIG 2g.10gb      14        5          4:2     |
    +----------------------------------------------------+
:::
:::
:::
:::

 {#gpu-instances .section}
### GPU Instances[\#](getting-started-with-mig.html#gpu-instances "Link to this heading")

The following example shows how two CUDA applications can be run in
parallel on two different GPU instances. In this example, the
BlackScholes CUDA sample is run simultaneously on the two GIs created on
the A100.

 {.highlight}
    $ nvidia-smi -L
    GPU 0: A100-SXM4-40GB (UUID: GPU-e86cb44c-6756-fd30-cd4a-1e6da3caf9b0)
      MIG 3g.20gb Device 0: (UUID: MIG-c7384736-a75d-5afc-978f-d2f1294409fd)
      MIG 3g.20gb Device 1: (UUID: MIG-a28ad590-3fda-56dd-84fc-0a0b96edc58d)


    $ CUDA_VISIBLE_DEVICES=MIG-c7384736-a75d-5afc-978f-d2f1294409fd ./BlackScholes &
    $ CUDA_VISIBLE_DEVICES=MIG-a28ad590-3fda-56dd-84fc-0a0b96edc58d ./BlackScholes &
:::
:::

Now verify the two CUDA applications are running on two separate GPU
instances:

 {.highlight}
    $ nvidia-smi
    +-----------------------------------------------------------------------------+
    | MIG devices:                                                                |
    +------------------+----------------------+-----------+-----------------------+
    | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
    |      ID  ID  Dev |                      | SM     Unc| CE  ENC  DEC  OFA  JPG|
    |                  |                      |        ECC|                       |
    |==================+======================+===========+=======================|
    |  0    1   0   0  |    268MiB / 20224MiB | 42      0 |  3   0    2    0    0 |
    +------------------+----------------------+-----------+-----------------------+
    |  0    2   0   1  |    268MiB / 20096MiB | 42      0 |  3   0    2    0    0 |
    +------------------+----------------------+-----------+-----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |    0    1    0      58866      C   ./BlackScholes                    253MiB |
    |    0    2    0      58856      C   ./BlackScholes                    253MiB |
    +-----------------------------------------------------------------------------+
:::
:::
:::

 {.highlight-text .notranslate}

:::

For monitoring MIG devices on MIG capable GPUs such as the A100,
including attribution of GPU metrics (including utilization and other
profiling metrics), it is recommended to use NVIDIA DCGM v2.0.13 or
later. See the [Profiling
Metrics](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html#profiling){.reference
.external} section in the DCGM User Guide for more details on getting
started.
:::

 {.highlight-text .notranslate}

:::

Create 3 CIs, each of type 1c compute capacity (profile ID 0) on the
first GI.

 {.highlight}
    $ sudo nvidia-smi mig -cci 0,0,0 -gi 1
    Successfully created compute instance on GPU  0 GPU instance ID  1 using profile MIG 1c.3g.20gb (ID  0)
    Successfully created compute instance on GPU  0 GPU instance ID  1 using profile MIG 1c.3g.20gb (ID  0)
    Successfully created compute instance on GPU  0 GPU instance ID  1 using profile MIG 1c.3g.20gb (ID  0)
:::
:::

Using `nvidia-smi`{.docutils .literal .notranslate}, the following CIs
are now created on GI 1:

 {.highlight}
    $ sudo nvidia-smi mig -lci -gi 1
    +-------------------------------------------------------+
    | Compute instances:                                    |
    | GPU     GPU       Name             Profile   Instance |
    |       Instance                       ID        ID     |
    |         ID                                            |
    |=======================================================|
    |   0      1       MIG 1c.3g.20gb       0         0     |
    +-------------------------------------------------------+
    |   0      1       MIG 1c.3g.20gb       0         1     |
    +-------------------------------------------------------+
    |   0      1       MIG 1c.3g.20gb       0         2     |
    +-------------------------------------------------------+
:::
:::

And the GIs and CIs created on the A100 are now enumerated by the
driver:

 {.highlight}
    $ nvidia-smi
    +-----------------------------------------------------------------------------+
    | MIG devices:                                                                |
    +------------------+----------------------+-----------+-----------------------+
    | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
    |      ID  ID  Dev |                      | SM     Unc| CE  ENC  DEC  OFA  JPG|
    |                  |                      |        ECC|                       |
    |==================+======================+===========+=======================|
    |  0    1   0   0  |     11MiB / 20224MiB | 14      0 |  3   0    2    0    0 |
    +------------------+                      +-----------+-----------------------+
    |  0    1   1   1  |                      | 14      0 |  3   0    2    0    0 |
    +------------------+                      +-----------+-----------------------+
    |  0    1   2   2  |                      | 14      0 |  3   0    2    0    0 |
    +------------------+----------------------+-----------+-----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |  No running processes found                                                 |
    +-----------------------------------------------------------------------------+
:::
:::

Now, three BlackScholes applications can be created and run in parallel:

 {.highlight}
    $ CUDA_VISIBLE_DEVICES=MIG-c7384736-a75d-5afc-978f-d2f1294409fd ./BlackScholes &
    $ CUDA_VISIBLE_DEVICES=MIG-c376546e-7559-5610-9721-124e8dbb1bc8 ./BlackScholes &
    $ CUDA_VISIBLE_DEVICES=MIG-928edfb0-898f-53bd-bf24-c7e5d08a6852 ./BlackScholes &
:::
:::

And seen using nvidia-smi as running processes on the three CIs:

 {.highlight}
    $ nvidia-smi
    +-----------------------------------------------------------------------------+
    | MIG devices:                                                                |
    +------------------+----------------------+-----------+-----------------------+
    | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
    |      ID  ID  Dev |                      | SM     Unc| CE  ENC  DEC  OFA  JPG|
    |                  |                      |        ECC|                       |
    |==================+======================+===========+=======================|
    |  0    1   0   0  |    476MiB / 20224MiB | 14      0 |  3   0    2    0    0 |
    +------------------+                      +-----------+-----------------------+
    |  0    1   1   1  |                      | 14      0 |  3   0    2    0    0 |
    +------------------+                      +-----------+-----------------------+
    |  0    1   2   2  |                      | 14      0 |  3   0    2    0    0 |
    +------------------+----------------------+-----------+-----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |    0    1    0      59785      C   ./BlackScholes                    153MiB |
    |    0    1    1      59796      C   ./BlackScholes                    153MiB |
    |    0    1    2      59885      C   ./BlackScholes                    153MiB |
    +-----------------------------------------------------------------------------+
:::
:::
:::
:::

 {.highlight-text .notranslate}

:::

In this example, we delete the specific CIs created under GI 1.

 {.highlight}
    $ sudo nvidia-smi mig -dci -ci 0,1,2 -gi 1
    Successfully destroyed compute instance ID  0 from GPU  0 GPU instance ID  1
    Successfully destroyed compute instance ID  1 from GPU  0 GPU instance ID  1
    Successfully destroyed compute instance ID  2 from GPU  0 GPU instance ID  1
:::
:::

It can be verified that the CI devices have now been torn down on the
GPU:

 {.highlight}
    $ nvidia-smi
    +-----------------------------------------------------------------------------+
    | MIG devices:                                                                |
    +------------------+----------------------+-----------+-----------------------+
    | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
    |      ID  ID  Dev |                      | SM     Unc| CE  ENC  DEC  OFA  JPG|
    |                  |                      |        ECC|                       |
    |==================+======================+===========+=======================|
    |  No MIG devices found                                                       |
    +-----------------------------------------------------------------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |  No running processes found                                                 |
    +-----------------------------------------------------------------------------+
:::
:::

Now the GIs have to be deleted:

 {.highlight}
    $ sudo nvidia-smi mig -dgi
    Successfully destroyed GPU instance ID  1 from GPU  0
    Successfully destroyed GPU instance ID  2 from GPU  0
:::
:::
:::

 {.admonition .note}
Note

On NVIDIA Ampere architecture GPUs (A100 or A30), NVML (and nvidia-smi)
does not support attribution of utilization metrics to MIG devices. From
the previous example, the utilization is displayed as N/A when running
CUDA programs:

 {.highlight}
    $ nvidia-smi

    +-----------------------------------------------------------------------------+
    | MIG devices:                                                                |
    +------------------+----------------------+-----------+-----------------------+
    | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
    |      ID  ID  Dev |           BAR1-Usage | SM     Unc| CE  ENC  DEC  OFA  JPG|
    |                  |                      |        ECC|                       |
    |==================+======================+===========+=======================|
    |  0    1   0   0  |    268MiB / 20096MiB | 42      0 |  3   0    2    0    0 |
    |                  |      4MiB / 32767MiB |           |                       |
    +------------------+----------------------+-----------+-----------------------+
    |  0    2   0   1  |    268MiB / 20096MiB | 42      0 |  3   0    2    0    0 |
    |                  |      4MiB / 32767MiB |           |                       |
    +------------------+----------------------+-----------+-----------------------+

    +-----------------------------------------------------------------------------+
    | Processes:                                                                  |
    |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
    |        ID   ID                                                   Usage      |
    |=============================================================================|
    |    0    1    0       6217      C   ...inux/release/BlackScholes      253MiB |
    |    0    2    0       6223      C   ...inux/release/BlackScholes      253MiB |
    +-----------------------------------------------------------------------------+
:::
:::
:::
:::

 {#workflow .section}
### Workflow[\#](getting-started-with-mig.html#workflow "Link to this heading")

In summary, the workflow for running with MPS is as follows:

-   Configure the desired MIG geometry on the GPU.

-   Setup the `CUDA_MPS_PIPE_DIRECTORY`{.docutils .literal .notranslate}
    variable to point to unique directories so that the multiple MPS
    servers and clients can communicate with each other using named
    pipes and Unix domain sockets.

-   Launch the application by specifying the MIG device using
    `CUDA_VISIBLE_DEVICES`{.docutils .literal .notranslate}.


:::

 {.highlight-console .notranslate}

:::

Verify configuration:

 {.highlight}
    $ nvidia-smi

    +-----------------------------------------------------------------------------------------+
    | NVIDIA-SMI 580.65.06              Driver Version: 580.65.06      CUDA Version: 13.0     |
    +-----------------------------------------+------------------------+----------------------+
    | GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
    |                                         |                        |               MIG M. |
    |=========================================+========================+======================|
    |   0  NVIDIA H100 80GB HBM3          Off |   00000000:42:00.0 Off |                   On |
    | N/A   30C    P0            141W /  700W |      87MiB /  81559MiB |     N/A      Default |
    |                                         |                        |              Enabled |
    +-----------------------------------------+------------------------+----------------------+

    +-----------------------------------------------------------------------------------------+
    | MIG devices:                                                                            |
    +------------------+----------------------------------+-----------+-----------------------+
    | GPU  GI  CI  MIG |              Shared Memory-Usage |        Vol|        Shared         |
    |      ID  ID  Dev |                Shared BAR1-Usage | SM     Unc| CE ENC  DEC  OFA  JPG |
    |                  |                                  |        ECC|                       |
    |==================+==================================+===========+=======================|
    |  0    1   0   0  |              44MiB / 40448MiB    | 60      0 |  3   0    3    0    3 |
    |                  |               0MiB / 24740MiB    |           |                       |
    +------------------+----------------------------------+-----------+-----------------------+
    |  0    2   0   1  |              44MiB / 40448MiB    | 60      0 |  3   0    3    0    3 |
    |                  |               0MiB / 24740MiB    |           |                       |
    +------------------+----------------------------------+-----------+-----------------------+
:::
:::
:::

 {.highlight-text .notranslate}

:::
:::

 {.highlight-text .notranslate}

:::
:::

 {.highlight-bash .notranslate}

:::

When the script is running, you should see two MPS servers and the
corresponding CUDA programs as MPS clients using `nvidia-smi`{.docutils
.literal .notranslate}:

 {.highlight}
    +-----------------------------------------------------------------------------------------+
    | Processes:                                                                              |
    |  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
    |        ID   ID                                                               Usage      |
    |=========================================================================================|
    |    0    1    0             3805    M+C   ./bin/BlackScholes                      326MiB |
    |    0    1    0             3809      C   nvidia-cuda-mps-server                   60MiB |
    |    0    2    0             3817    M+C   ./bin/BlackScholes                      326MiB |
    |    0    2    0             3819      C   nvidia-cuda-mps-server                   60MiB |
    +-----------------------------------------------------------------------------------------+
:::
:::
:::
:::

 {#install-docker .section}
### Install Docker[\#](getting-started-with-mig.html#install-docker "Link to this heading")

Many Linux distributions may come with Docker-CE pre-installed. If not,
use the Docker installation script to install Docker.

 {.highlight}
    $ curl https://get.docker.com | sh \
        && sudo systemctl start docker \
        && sudo systemctl enable docker
:::
:::
:::

 {.highlight-text .notranslate}

:::

Install the NVIDIA Container Toolkit packages (and their dependencies):

 {.highlight}
    $ sudo apt-get install -y nvidia-docker2 \
        && sudo systemctl restart docker
:::
:::
:::

 {.highlight-text .notranslate}

:::

A more complex example is to run a TensorFlow container to do a training
run using GPUs on the MNIST dataset. This is shown below:

 {.highlight}
    $ sudo docker run --gpus '"device=0:1"' \
        nvcr.io/nvidia/pytorch:20.11-py3 \
        /bin/bash -c 'cd /opt/pytorch/examples/upstream/mnist && python main.py'

    =============
    == PyTorch ==
    =============

    NVIDIA Release 20.11 (build 17345815)
    PyTorch Version 1.8.0a0+17f8c32

    Container image Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.

    Copyright (c) 2014-2020 Facebook Inc.
    Copyright (c) 2011-2014 Idiap Research Institute (Ronan Collobert)
    Copyright (c) 2012-2014 Deepmind Technologies    (Koray Kavukcuoglu)
    Copyright (c) 2011-2012 NEC Laboratories America (Koray Kavukcuoglu)
    Copyright (c) 2011-2013 NYU                      (Clement Farabet)
    Copyright (c) 2006-2010 NEC Laboratories America (Ronan Collobert, Leon Bottou, Iain Melvin, Jason Weston)
    Copyright (c) 2006      Idiap Research Institute (Samy Bengio)
    Copyright (c) 2001-2004 Idiap Research Institute (Ronan Collobert, Samy Bengio, Johnny Mariethoz)
    Copyright (c) 2015      Google Inc.
    Copyright (c) 2015      Yangqing Jia
    Copyright (c) 2013-2016 The Caffe contributors
    All rights reserved.

    NVIDIA Deep Learning Profiler (dlprof) Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.

    Various files include modifications (c) NVIDIA CORPORATION.  All rights reserved.
    NVIDIA modifications are covered by the license terms that apply to the underlying project or file.

    NOTE: Legacy NVIDIA Driver detected.  Compatibility mode ENABLED.

    9920512it [00:01, 7880654.53it/s]
    32768it [00:00, 129950.31it/s]
    1654784it [00:00, 2353765.88it/s]
    8192it [00:00, 41020.33it/s]
    /opt/conda/lib/python3.6/site-packages/torchvision/datasets/mnist.py:480: UserWarning: The given NumPy array is not writeable, and PyTorch does not support non-writeable tensors. This means you can write to the underlying (supposedly non-writeable) NumPy array using the tensor. You may want to copy the array to protect its data or make it writeable before converting it to a tensor. This type of warning will be suppressed for the rest of this program. (Triggered internally at  ../torch/csrc/utils/tensor_numpy.cpp:141.)
      return torch.from_numpy(parsed.astype(m[2], copy=False)).view(*s)
    Downloading http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz to ../data/MNIST/raw/train-images-idx3-ubyte.gz
    Extracting ../data/MNIST/raw/train-images-idx3-ubyte.gz to ../data/MNIST/raw
    Downloading http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz to ../data/MNIST/raw/train-labels-idx1-ubyte.gz
    Extracting ../data/MNIST/raw/train-labels-idx1-ubyte.gz to ../data/MNIST/raw
    Downloading http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz to ../data/MNIST/raw/t10k-images-idx3-ubyte.gz
    Extracting ../data/MNIST/raw/t10k-images-idx3-ubyte.gz to ../data/MNIST/raw
    Downloading http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz to ../data/MNIST/raw/t10k-labels-idx1-ubyte.gz
    Extracting ../data/MNIST/raw/t10k-labels-idx1-ubyte.gz to ../data/MNIST/raw
    Processing...
    Done!
    Train Epoch: 1 [0/60000 (0%)]   Loss: 2.320747
    Train Epoch: 1 [640/60000 (1%)] Loss: 1.278727
:::
:::
:::
:::


:::

 {.prev-next-info}
previous

Supported MIG Profiles
:::

[](device-nodes-and-capabilities.html "next page"){.right-next}


:::
:::

 {.sidebar-secondary-items .sidebar-secondary__inner}
 {#pst-page-navigation-heading-2 .page-toc .tocsection .onthispage}
On this page
:::

-   [Prerequisites](getting-started-with-mig.html#prerequisites){.reference
    .internal .nav-link}
    -   [Additional Prerequisites for RTX PRO Blackwell
        GPUs](getting-started-with-mig.html#additional-prerequisites-for-rtx-pro-blackwell-gpus){.reference
        .internal .nav-link}
-   [Enable MIG
    Mode](getting-started-with-mig.html#enable-mig-mode){.reference
    .internal .nav-link}
    -   [GPU Reset on Hopper+
        GPUs](getting-started-with-mig.html#gpu-reset-on-hopper-gpus){.reference
        .internal .nav-link}
    -   [GPU Reset on NVIDIA Ampere Architecture
        GPUs](getting-started-with-mig.html#gpu-reset-on-nvidia-ampere-architecture-gpus){.reference
        .internal .nav-link}
    -   [Driver
        Clients](getting-started-with-mig.html#driver-clients){.reference
        .internal .nav-link}
-   [List GPU Instance
    Profiles](getting-started-with-mig.html#list-gpu-instance-profiles){.reference
    .internal .nav-link}
-   [Creating GPU
    Instances](getting-started-with-mig.html#creating-gpu-instances){.reference
    .internal .nav-link}
    -   [Instance
        Geometry](getting-started-with-mig.html#instance-geometry){.reference
        .internal .nav-link}
-   [Running CUDA Applications on
    Bare-Metal](getting-started-with-mig.html#running-cuda-applications-on-bare-metal){.reference
    .internal .nav-link}
    -   [GPU
        Instances](getting-started-with-mig.html#gpu-instances){.reference
        .internal .nav-link}
    -   [GPU Utilization
        Metrics](getting-started-with-mig.html#gpu-utilization-metrics){.reference
        .internal .nav-link}
    -   [Compute
        Instances](getting-started-with-mig.html#compute-instances){.reference
        .internal .nav-link}
-   [Destroying GPU
    Instances](getting-started-with-mig.html#destroying-gpu-instances){.reference
    .internal .nav-link}
-   [Monitoring MIG
    Devices](getting-started-with-mig.html#monitoring-mig-devices){.reference
    .internal .nav-link}
-   [MIG with CUDA
    MPS](getting-started-with-mig.html#mig-with-cuda-mps){.reference
    .internal .nav-link}
    -   [Workflow](getting-started-with-mig.html#workflow){.reference
        .internal .nav-link}
    -   [Configure GPU
        Instances](getting-started-with-mig.html#configure-gpu-instances){.reference
        .internal .nav-link}
    -   [Set Up the MPS Control
        Daemons](getting-started-with-mig.html#set-up-the-mps-control-daemons){.reference
        .internal .nav-link}
    -   [Launch the
        Application](getting-started-with-mig.html#launch-the-application){.reference
        .internal .nav-link}
    -   [A Complete
        Example](getting-started-with-mig.html#a-complete-example){.reference
        .internal .nav-link}
-   [Running CUDA Applications as
    Containers](getting-started-with-mig.html#running-cuda-applications-as-containers){.reference
    .internal .nav-link}
    -   [Install
        Docker](getting-started-with-mig.html#install-docker){.reference
        .internal .nav-link}
    -   [Install NVIDIA Container
        Toolkit](getting-started-with-mig.html#install-nvidia-container-toolkit){.reference
        .internal .nav-link}
    -   [Running
        Containers](getting-started-with-mig.html#running-containers){.reference
        .internal .nav-link}
-   [MIG with
    Kubernetes](getting-started-with-mig.html#mig-with-kubernetes){.reference
    .internal .nav-link}
-   [MIG with
    Slurm](getting-started-with-mig.html#mig-with-slurm){.reference
    .internal .nav-link}
:::
:::
:::
:::
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


[]{.fa-solid .fa-outdent}
:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {.admonition .note}
Note

The description below shows the profile names on the A100-SXM4-40GB
product. For A100-SXM4-80GB, the profile names will change according to
the memory proportion - for example, `1g.10gb`{.docutils .literal
.notranslate}, `2g.20gb`{.docutils .literal .notranslate},
`3g.40gb`{.docutils .literal .notranslate}, `4g.40gb`{.docutils .literal
.notranslate}, `7g.80gb`{.docutils .literal .notranslate}, respectively.
:::


Each GI can be further sub-divided into multiple CIs as required by
users depending on their workloads. The following table highlights what
the name of a MIG device would look like in this case. The example shown
is for subdividing a 3g.20gb device into a set of sub-devices with
different Compute Instance slice counts.


:::
:::
:::
:::
:::
:::

20gb

20gb

GPU Instance

3g

3g

Compute Instance

1c

1c

1c

2c

1c

MIG Device

1c.3g.20gb

1c.3g.20gb

1c.3g.20gb

2c.3g.20gb

1c.3g.20gb

GPC

GPC

GPC

GPC GPC

GPC

 {.highlight-text .notranslate}

:::

The corresponding device nodes (in `mig-minors`{.docutils .literal
.notranslate}) are created under `/dev/nvidia-caps`{.docutils .literal
.notranslate}. Refer to [[CUDA Device Enumeration]{.std
.std-ref}](mig-device-names.html#cuda-device-enumeration){.reference
.internal} for more information.
:::

 {.sd-tab-set .docutils}
Driver \>= 570

 {.admonition .note}
Note

Increase the open files limit above the common default of
`1024`{.docutils .literal .notranslate} using
`ulimit -n <limit>`{.docutils .literal .notranslate}.
:::

These constraints may be relaxed in future NVIDIA driver releases for
MIG.

**CUDA\_VISIBLE\_DEVICES and MIG**

-   `CUDA_VISIBLE_DEVICES`{.docutils .literal .notranslate} has been
    extended to support MIG.

-   You can specify compute instance UUIDs (at most one per GPU
    instance).

-   If multiple compute instances exist within a GPU instance and more
    than one are listed in `CUDA_VISIBLE_DEVICES`{.docutils .literal
    .notranslate}, CUDA will pick one from the list.

-   If `CUDA_VISIBLE_DEVICES`{.docutils .literal .notranslate} is not
    set, CUDA will pick one from each GPU instance.

**Example: CI UUID assignment on H100 (R570 drivers)**

With the R570 NVIDIA datacenter drivers (470.42.01+), the example below
shows how each CI is assigned GPU UUIDs in an H100 GPU:

 {.highlight}
    $ nvidia-smi -L
    GPU 0: NVIDIA H100 80GB HBM3 (UUID: GPU-c08d91cb-e324-655c-71ba-7570956445bc)
      MIG 1c.3g.40gb  Device  0: (UUID: MIG-c788539f-c1ea-5a36-8b4d-9b07d024b1bb)
      MIG 1c.3g.40gb  Device  1: (UUID: MIG-405bbda1-6b05-535f-9702-f95e8cd170ce)
      MIG 1c.3g.40gb  Device  2: (UUID: MIG-df7e5a27-eeea-51a0-9055-b36d5a552879)
      MIG 1g.10gb     Device  3: (UUID: MIG-b4b2228d-6933-5839-bc0e-41ab9edb61c6)
      MIG 1g.10gb     Device  4: (UUID: MIG-c71dc464-b9f9-5611-9d29-d601a47cffd6)
:::
:::
:::

Driver \< 570

 {.admonition .note}
Note

With the R470 NVIDIA datacenter drivers (470.42.01+), the example below
shows how MIG devices are assigned GPU UUIDs in an 8-GPU system with
each GPU configured differently.
:::

 {.highlight}
    $ nvidia-smi -L

     GPU 0: A100-SXM4-40GB (UUID: GPU-5d5ba0d6-d33d-2b2c-524d-9e3d8d2b8a77)
        MIG 1g.5gb      Device  0: (UUID: MIG-c6d4f1ef-42e4-5de3-91c7-45d71c87eb3f)
        MIG 1g.5gb      Device  1: (UUID: MIG-cba663e8-9bed-5b25-b243-5985ef7c9beb)
        MIG 1g.5gb      Device  2: (UUID: MIG-1e099852-3624-56c0-8064-c5db1211e44f)
        MIG 1g.5gb      Device  3: (UUID: MIG-8243111b-d4c4-587a-a96d-da04583b36e2)
        MIG 1g.5gb      Device  4: (UUID: MIG-169f1837-b996-59aa-9ed5-b0a3f99e88a6)
        MIG 1g.5gb      Device  5: (UUID: MIG-d5d0152c-e3f0-552c-abee-ebc0195e9f1d)
        MIG 1g.5gb      Device  6: (UUID: MIG-7df6b45c-a92d-5e09-8540-a6b389968c31)
     GPU 1: A100-SXM4-40GB (UUID: GPU-0aa11ebd-627f-af3f-1a0d-4e1fd92fd7b0)
        MIG 2g.10gb     Device  0: (UUID: MIG-0c757cd7-e942-5726-a0b8-0e8fb7067135)
        MIG 2g.10gb     Device  1: (UUID: MIG-703fb6ed-3fa0-5e48-8e65-1c5bdcfe2202)
        MIG 2g.10gb     Device  2: (UUID: MIG-532453fc-0faa-5c3c-9709-a3fc2e76083d)
     GPU 2: A100-SXM4-40GB (UUID: GPU-08279800-1cbe-a71d-f3e6-8f67e15ae54a)
        MIG 3g.20gb     Device  0: (UUID: MIG-aa232436-d5a6-5e39-b527-16f9b223cc46)
        MIG 3g.20gb     Device  1: (UUID: MIG-3b12da37-7fa2-596c-8655-62dab88f0b64)
     GPU 3: A100-SXM4-40GB (UUID: GPU-71086aca-c858-d1e0-aae1-275bed1008b9)
        MIG 7g.40gb     Device  0: (UUID: MIG-3e209540-03e2-5edb-8798-51d4967218c9)
     GPU 4: A100-SXM4-40GB (UUID: GPU-74fa9fb7-ccf6-8234-e597-7af8ace9a8f5)
        MIG 1c.3g.20gb  Device  0: (UUID: MIG-79c62632-04cc-574b-af7b-cb2e307120d8)
        MIG 1c.3g.20gb  Device  1: (UUID: MIG-4b3cc0fd-6876-50d7-a8ba-184a86e2b958)
        MIG 1c.3g.20gb  Device  2: (UUID: MIG-194837c7-0476-5b56-9c45-16bddc82e1cf)
        MIG 1c.3g.20gb  Device  3: (UUID: MIG-291820db-96a4-5463-8e7b-444c2d2e3dfa)
        MIG 1c.3g.20gb  Device  4: (UUID: MIG-5a97e28a-7809-5e93-abae-c3818c5ea801)
        MIG 1c.3g.20gb  Device  5: (UUID: MIG-3dfd5705-b18a-5a7c-bcee-d03a0ccb7a96)
     GPU 5: A100-SXM4-40GB (UUID: GPU-3301e6dd-d38f-0eb5-4665-6c9659f320ff)
        MIG 4g.20gb     Device  0: (UUID: MIG-6d96b9f9-960e-5057-b5da-b8a35dc63aa8)
     GPU 6: A100-SXM4-40GB (UUID: GPU-bb40ed7d-cbbb-d92c-50ac-24803cda52c5)
        MIG 1c.7g.40gb  Device  0: (UUID: MIG-66dd01d7-8cdb-5a13-a45d-c6eb0ee11810)
        MIG 2c.7g.40gb  Device  1: (UUID: MIG-03c649cb-e6ae-5284-8e94-4b1cf767e06c)
        MIG 3c.7g.40gb  Device  2: (UUID: MIG-8abf68e0-2808-525e-9133-ba81701ed6d3)
     GPU 7: A100-SXM4-40GB (UUID: GPU-95fac899-e21a-0e44-b0fc-e4e3bf106feb)
        MIG 4g.20gb     Device  0: (UUID: MIG-219c765c-e07f-5b85-9c04-4afe174d83dd)
        MIG 2g.10gb     Device  1: (UUID: MIG-25884364-137e-52cc-a7e4-ecf3061c3ae1)
        MIG 1g.5gb      Device  2: (UUID: MIG-83e71a6c-f0c3-5dfc-8577-6e8b17885e1f)
:::
:::
:::
:::
:::

 {.prev-next-info}
previous

Deployment Considerations
:::

[](supported-mig-profiles.html "next page"){.right-next}


:::

 {.sidebar-secondary-items .sidebar-secondary__inner}
 {#pst-page-navigation-heading-2 .page-toc .tocsection .onthispage}
On this page
:::

-   [Device
    Enumeration](mig-device-names.html#device-enumeration){.reference
    .internal .nav-link}
-   [CUDA Device
    Enumeration](mig-device-names.html#cuda-device-enumeration){.reference
    .internal .nav-link}
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


[]{.fa-solid .fa-outdent}
:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {.highlight-text .notranslate}

:::

Starting with CUDA 11/R450, a new abstraction known as
`nvidia-capabilities`{.docutils .literal .notranslate} has been
introduced. The idea being that access to a specific capability is
required to perform certain actions through the driver. If a user has
access to the capability, the action will be carried out. If a user does
not have access to the capability, the action will fail. The one
exception being if you are the root-user (or any user with
`CAP_SYS_ADMIN`{.docutils .literal .notranslate} privileges). With
`CAP_SYS_ADMIN`{.docutils .literal .notranslate} privileges, you
implicitly have access to all `nvidia-capabilities`{.docutils .literal
.notranslate}.

For example, the `mig-config`{.docutils .literal .notranslate}
capability allows one to create and destroy MIG instances on any
MIG-capable GPU (for example, the A100 GPU). Without this capability,
all attempts to create or destroy a MIG instance will fail. Likewise,
the `fabric-mgmt`{.docutils .literal .notranslate} capability allows one
to run the Fabric Manager as a non-root but privileged daemon. Without
this capability, all attempts to launch the Fabric Manager as a non-root
user will fail.

The following sections walk through the system level interface for
managing these new `nvidia-capabilities`{.docutils .literal
.notranslate}, including the steps necessary to grant and revoke access
to them.

 {.highlight-text .notranslate}

:::

 {.highlight-text .notranslate}

:::

Second, the exact same set of files exist under
`/proc/driver/nvidia/capabilities`{.docutils .literal .notranslate}.
These files no longer control access to the capability directly and
instead, the contents of these files point at a device node under
`/dev`{.docutils .literal .notranslate}, through which cgroups can be
used to control access to the capability.

This can be seen in the following example:

 {.highlight}
    $ cat /proc/driver/nvidia/capabilities/mig/config
    DeviceFileMinor: 1
    DeviceFileMode: 256
    DeviceFileModify: 1
:::
:::

The combination of the device major for `nvidia-caps`{.docutils .literal
.notranslate} and the value of `DeviceFileMinor`{.docutils .literal
.notranslate} in this file indicate that the `mig-config`{.docutils
.literal .notranslate} capability (which allows a user to create and
destroy MIG devices) is controlled by the device node with a
`major:minor`{.docutils .literal .notranslate} of `238:1`{.docutils
.literal .notranslate}. As such, one will need to use
`cgroups`{.docutils .literal .notranslate} to grant a process read
access to this device in order to configure MIG devices. The purpose of
the `DeviceFileMode`{.docutils .literal .notranslate} and
`DeviceFileModify`{.docutils .literal .notranslate} fields in this file
are explained later on in this section.

The standard location for these device nodes is under
`/dev/nvidia-caps`{.docutils .literal .notranslate}:

 {.highlight}
    $ ls -l /dev/nvidia-caps
    total 0
    cr-------- 1 root root 508,  1 Nov 21 17:16 nvidia-cap1
    cr--r--r-- 1 root root 508,  2 Nov 21 17:16 nvidia-cap2
    ...
:::
:::

Unfortunately, these device nodes cannot be automatically
created/deleted by the NVIDIA driver at the same time it creates/deletes
files under `/proc/driver/nvidia/capabilities`{.docutils .literal
.notranslate} (due to GPL compliance issues). Instead, a user-level
program called `nvidia-modprobe`{.docutils .literal .notranslate} is
provided, that can be invoked from user-space in order to do this. For
example:

 {.highlight}
    $ nvidia-modprobe \
        -f /proc/driver/nvidia/capabilities/mig/config \
        -f /proc/driver/nvidia/capabilities/mig/monitor

    $ ls -l /dev/nvidia-caps
    total 0
    cr-------- 1 root root 508,  1 Nov 21 17:16 nvidia-cap1
    cr--r--r-- 1 root root 508,  2 Nov 21 17:16 nvidia-cap2
:::
:::

`nvidia-modprobe`{.docutils .literal .notranslate} looks at the
`DeviceFileMode`{.docutils .literal .notranslate} in each capability
file and creates the device node with the permissions indicated (for
example, `+ur`{.docutils .literal .notranslate} from a value of 256
(o400) from our example for `mig-config`{.docutils .literal
.notranslate}).

Programs such as `nvidia-smi`{.docutils .literal .notranslate} will
automatically invoke `nvidia-modprobe`{.docutils .literal .notranslate}
(when available) to create these device nodes on your behalf. In other
scenarios it is not necessarily required to use nvidia-modprobe to
create these device nodes, but it does make the process simpler.

If you actually want to prevent `nvidia-modprobe`{.docutils .literal
.notranslate} from ever creating a particular device node on your
behalf, you can do the following:

 {.highlight}
    # Give a user write permissions to the capability file under /proc
    $ chmod +uw /proc/driver/nvidia/capabilities/mig/config

    # Update the file with a "DeviceFileModify" setting of 0
    $ echo "DeviceFileModify: 0" > /proc/driver/nvidia/capabilities/mig/config
:::
:::

You will then be responsible for managing creation of the device node
referenced by `/proc/driver/nvidia/capabilities/mig/config`{.docutils
.literal .notranslate} going forward. If you want to change that in the
future, simply reset it to a value of `DeviceFileModify: 1`{.docutils
.literal .notranslate} with the same command sequence.

This is important in the context of containers because we may want to
give a container access to a certain capability even if it doesn't exist
in the `/proc`{.docutils .literal .notranslate} hierarchy yet.

For example, granting a container the `mig-config`{.docutils .literal
.notranslate} capability implies that we should also grant it
capabilities to access all possible gis and cis that could be created
for any GPU on the system. Otherwise the container will have no way of
working with those gis and cis once they have actually been created.

One final thing to note about `/dev`{.docutils .literal .notranslate}
based capabilities is that the minor numbers for all possible
capabilities are predetermined and can be queried under various files of
the form:

 {.highlight}
    /proc/driver/nvidia-caps/*-minors
:::
:::

For example, all capabilities related to MIG can be looked up as:

 {.highlight}
    $ cat /proc/driver/nvidia-caps/mig-minors
    config 1
    monitor 2
    gpu0/gi0/access 3
    gpu0/gi0/ci0/access 4
    gpu0/gi0/ci1/access 5
    gpu0/gi0/ci2/access 6
    ...
    gpu31/gi14/ci6/access 4321
    gpu31/gi14/ci7/access 4322
:::
:::

The format of the content is:
`GPU<deviceMinor>/gi<GPU instance ID>/ci<compute instance ID>`{.docutils
.literal .notranslate}

Note that the GPU device minor number can be obtained by using either of
these mechanisms:

-   The NVML API `nvmlDeviceGetMinorNumber()`{.docutils .literal
    .notranslate} so it returns the device minor number

-   Or use the PCI BDF available under
    `/proc/driver/nvidia/gpus/domain:bus:device:function/information`{.docutils
    .literal .notranslate}. This file contains a "Device Minor" field.


For example, if the MIG geometry was created as below:

 {.highlight}
    +-----------------------------------------------------------------------------+
    | MIG devices:                                                                |
    +------------------+----------------------+-----------+-----------------------+
    | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
    |      ID  ID  Dev |           BAR1-Usage | SM     Unc| CE  ENC  DEC  OFA  JPG|
    |                  |                      |        ECC|                       |
    |==================+======================+===========+=======================|
    |  0    1   0   0  |     19MiB / 40192MiB | 14      0 |  3   0    3    0    3 |
    |                  |      0MiB / 65535MiB |           |                       |
    +------------------+                      +-----------+-----------------------+
    |  0    1   1   1  |                      | 14      0 |  3   0    3    0    3 |
    |                  |                      |           |                       |
    +------------------+                      +-----------+-----------------------+
    |  0    1   2   2  |                      | 14      0 |  3   0    3    0    3 |
    |                  |                      |           |                       |
    +------------------+----------------------+-----------+-----------------------+
:::
:::

Then the corresponding device nodes: `/dev/nvidia-cap12`{.docutils
.literal .notranslate}, `/dev/nvidia-cap13`{.docutils .literal
.notranslate}, `/dev/nvidia-cap14`{.docutils .literal .notranslate}, and
`/dev/nvidia-cap15`{.docutils .literal .notranslate} would be created.
:::

 {.highlight-text .notranslate}

:::

Likewise, the capabilities required to run workloads on a MIG device
once it has been created are represented as follows (namely as access to
the GPU Instance and Compute Instance that comprise the MIG device):

 {.highlight}
    /proc/driver/nvidia/capabilities
    └── gpu0
        └── mig
            ├── gi0
            │   ├── access
            │   └── ci0
            │       └── access
            ├── gi1
            │   ├── access
            │   └── ci0
            │       └── access
            └── gi2
                ├── access
                └── ci0
                    └── access
:::
:::

And the corresponding file system layout is shown below with read
permissions:

 {.highlight}
    $ ls -l /proc/driver/nvidia/capabilities/gpu0/mig/gi*
    /proc/driver/nvidia/capabilities/gpu0/mig/gi1:
    total 0
    -r--r--r-- 1 root root 0 May 24 17:38 access
    dr-xr-xr-x 2 root root 0 May 24 17:38 ci0

    /proc/driver/nvidia/capabilities/gpu0/mig/gi2:
    total 0
    -r--r--r-- 1 root root 0 May 24 17:38 access
    dr-xr-xr-x 2 root root 0 May 24 17:38 ci0
:::
:::

For a CUDA process to be able to run on top of MIG, it needs access to
the Compute Instance capability and its parent GPU Instance. Thus a MIG
device is identified by the following format:

 {.highlight}
    MIG-<GPU-UUID>/<GPU instance ID>/<compute instance ID>
:::
:::

As an example, having read access to the following paths would allow one
to run workloads on the MIG device represented by
`<gpu0, gi0, ci0>`{.docutils .literal .notranslate}:

 {.highlight}
    /proc/driver/nvidia/capabilities/gpu0/mig/gi0/access
    /proc/driver/nvidia/capabilities/gpu0/mig/gi0/ci0/access
:::
:::

Note that there is no access file representing a capability to run
workloads on gpu0 (only on gi0 and ci0 that sit underneath gpu0). This
is because the traditional mechanism of using cgroups to control access
to top level GPU devices (and any required meta devices) is still
required. As shown earlier in the document, the cgroups mechanism
applies to:

 {.highlight}
    /dev/nvidia0
    /dev/nvidiactl
    /dev/nvidiactl-uvm
    ...
:::
:::

In the context of containers, a new mount namespace should be overlaid
on top of the path for `/proc/driver/nvidia/capabilities`{.docutils
.literal .notranslate}, and only those capabilities a user wishes to
grant to a container should be **bind-mounted** in. Since the host's
user/group information is retained across the bind-mount, it must be
ensured that the correct user permissions are set for these capabilities
on the host before injecting them into a container.
:::
:::
:::

 {.prev-next-info}
previous

Getting Started with MIG
:::

[](Notices.html "next page"){.right-next}


:::
:::

 {.sidebar-secondary-items .sidebar-secondary__inner}
 {#pst-page-navigation-heading-2 .page-toc .tocsection .onthispage}
On this page
:::

-   [System Level
    Interface](device-nodes-and-capabilities.html#system-level-interface){.reference
    .internal .nav-link}
    -   [/dev Based
        nvidia-capabilities](device-nodes-and-capabilities.html#dev-based-nvidia-capabilities){.reference
        .internal .nav-link}
    -   [/proc based nvidia-capabilities
        (**Deprecated**)](device-nodes-and-capabilities.html#proc-based-nvidia-capabilities-deprecated){.reference
        .internal .nav-link}
:::
:::
:::
:::
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


[]{.fa-solid .fa-outdent}
:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {.pst-scrollable-table-container}
+-----------------------+-----------------------+-----------------------+
| GPU                   | CUDA Version          | NVIDIA Driver Version |
+=======================+=======================+=======================+
| A100 / A30            | CUDA 11               | R525 (\>= 525.53) or  |
|                       |                       | later                 |
+-----------------------+-----------------------+-----------------------+
| H100 / H200           | CUDA 12               | R450 (\>= 450.80.02)  |
|                       |                       | or later              |
+-----------------------+-----------------------+-----------------------+
| B200                  | CUDA 12               | R570 (\>= 570.133.20) |
|                       |                       | or later              |
+-----------------------+-----------------------+-----------------------+
| RTX PRO 6000          | CUDA 12               | R575 (\>= 575.51.03)  |
| Blackwell (All        |                       | or later              |
| editions)             |                       |                       |
|                       |                       |                       |
| RTX PRO 5000          |                       |                       |
| Blackwell             |                       |                       |
+-----------------------+-----------------------+-----------------------+
:::

 {.admonition .note}
    Note

    Also note the device nodes and `nvidia-capabilities`{.docutils
    .literal .notranslate} for exposing the MIG devices. The
    `/proc`{.docutils .literal .notranslate} mechanism for system-level
    interfaces is deprecated as of 450.51.06 and it is recommended to
    use the `/dev`{.docutils .literal .notranslate} based system-level
    interface for controlling access mechanisms of MIG devices through
    cgroups. This functionality is available starting with 450.80.02+
    drivers.
    :::

-   Supported configurations include:

    -   Bare-metal, including containers

    -   GPU pass-through virtualization to Linux guests on top of
        supported hypervisors

    -   vGPU on top of supported hypervisors

    MIG allows multiple vGPUs (and thereby VMs) to run in parallel on a
    single A100, while preserving the isolation guarantees that vGPU
    provides. For more information on GPU partitioning using vGPU and
    MIG, refer to the [technical
    brief](https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/TB-10226-001_v01.pdf){.reference
    .external}.

-   Setting MIG mode on the A100/A30 requires a GPU reset (and thus
    super-user privileges). Once the GPU is in MIG mode, instance
    management is then dynamic. Note that the setting is on a per-GPU
    basis.

-   On NVIDIA Ampere architecture GPUs, similar to ECC mode, MIG mode
    setting is persistent across reboots until the user toggles the
    setting explicitly

-   All daemons holding handles on driver modules need to be stopped
    before MIG enablement.

-   This is true for systems such as DGX which may be running system
    health monitoring services such as
    [nvsm](https://docs.nvidia.com/nvidia-system-management-nvsm/){.reference
    .external} or GPU health monitoring or telemetry services such as
    DCGM.

-   Toggling MIG mode requires the `CAP_SYS_ADMIN`{.docutils .literal
    .notranslate} capability. Other MIG management, such as creating and
    destroying instances, requires superuser by default, but can be
    delegated to non-privileged users by adjusting permissions to MIG
    capabilities in `/proc/`{.docutils .literal .notranslate}.
:::


:::

 {.prev-next-info}
previous

Concepts
:::

[](mig-device-names.html "next page"){.right-next}


:::
:::

 {.sidebar-secondary-items .sidebar-secondary__inner}
 {#pst-page-navigation-heading-2 .page-toc .tocsection .onthispage}
On this page
:::

-   [System
    Considerations](deployment-considerations.html#system-considerations){.reference
    .internal .nav-link}
-   [Application
    Considerations](deployment-considerations.html#application-considerations){.reference
    .internal .nav-link}
:::
:::
:::
:::
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {.prev-next-info}
previous

Supported Configurations
:::

[](concepts.html "next page"){.right-next}


:::
:::


:::
:::
:::
:::

---


Back to top

[[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd}]{.search-button__kbd-shortcut}


 {.col-lg-3 .navbar-header-items__start}

:::

 {.me-auto .navbar-header-items__center}

:::

 {.navbar-item .navbar-persistent--container}
[Search]{.search-button__default-text} [[Ctrl]{.kbd
.kbd-shortcut__modifier}+[K]{.kbd
.kbd-shortcut__modifier}]{.search-button__kbd-shortcut}
:::


:::
:::


[]{.fa-solid .fa-outdent}
:::

 {.bd-container__inner .bd-page-width}
 {.sidebar-header-items .sidebar-primary__section}
 {.navbar-item}
<div>

-   v580 \|
-   [PDF](https://docs.nvidia.com/datacenter/tesla/pdf/MIG_User_Guide.pdf){.nav-link
    .nav-external}
-   \|

</div>
:::
:::

 {.navbar-item}
:::
:::
:::

 {.sidebar-primary-item}
Table of Contents


:::
:::


:::

 {.bd-content}
 {.bd-header-article .d-print-none}
 {.header-article-items__start}

:::
:::
:::


 {#notice .section}
Notice[\#](Notices.html#notice "Link to this heading")
-------------------------------------------------------------------

This document is provided for information purposes only and shall not be
regarded as a warranty of a certain functionality, condition, or quality
of a product. NVIDIA Corporation ("NVIDIA") makes no representations or
warranties, expressed or implied, as to the accuracy or completeness of
the information contained in this document and assumes no responsibility
for any errors contained herein. NVIDIA shall have no liability for the
consequences or use of such information or for any infringement of
patents or other rights of third parties that may result from its use.
This document is not a commitment to develop, release, or deliver any
Material (defined below), code, or functionality.

NVIDIA reserves the right to make corrections, modifications,
enhancements, improvements, and any other changes to this document, at
any time without notice.

Customer should obtain the latest relevant information before placing
orders and should verify that such information is current and complete.

NVIDIA products are sold subject to the NVIDIA standard terms and
conditions of sale supplied at the time of order acknowledgement, unless
otherwise agreed in an individual sales agreement signed by authorized
representatives of NVIDIA and customer ("Terms of Sale"). NVIDIA hereby
expressly objects to applying any customer general terms and conditions
with regards to the purchase of the NVIDIA product referenced in this
document. No contractual obligations are formed either directly or
indirectly by this document.

NVIDIA products are not designed, authorized, or warranted to be
suitable for use in medical, military, aircraft, space, or life support
equipment, nor in applications where failure or malfunction of the
NVIDIA product can reasonably be expected to result in personal injury,
death, or property or environmental damage. NVIDIA accepts no liability
for inclusion and/or use of NVIDIA products in such equipment or
applications and therefore such inclusion and/or use is at customer's
own risk.

NVIDIA makes no representation or warranty that products based on this
document will be suitable for any specified use. Testing of all
parameters of each product is not necessarily performed by NVIDIA. It is
customer's sole responsibility to evaluate and determine the
applicability of any information contained in this document, ensure the
product is suitable and fit for the application planned by customer, and
perform the necessary testing for the application in order to avoid a
default of the application or the product. Weaknesses in customer's
product designs may affect the quality and reliability of the NVIDIA
product and may result in additional or different conditions and/or
requirements beyond those contained in this document. NVIDIA accepts no
liability related to any default, damage, costs, or problem which may be
based on or attributable to: (i) the use of the NVIDIA product in any
manner that is contrary to this document or (ii) customer product
designs.

No license, either expressed or implied, is granted under any NVIDIA
patent right, copyright, or other NVIDIA intellectual property right
under this document. Information published by NVIDIA regarding
third-party products or services does not constitute a license from
NVIDIA to use such products or services or a warranty or endorsement
thereof. Use of such information may require a license from a third
party under the patents or other intellectual property rights of the
third party, or a license from NVIDIA under the patents or other
intellectual property rights of NVIDIA.

Reproduction of information in this document is permissible only if
approved in advance by NVIDIA in writing, reproduced without alteration
and in full compliance with all applicable export laws and regulations,
and accompanied by all associated conditions, limitations, and notices.

THIS DOCUMENT AND ALL NVIDIA DESIGN SPECIFICATIONS, REFERENCE BOARDS,
FILES, DRAWINGS, DIAGNOSTICS, LISTS, AND OTHER DOCUMENTS (TOGETHER AND
SEPARATELY, "MATERIALS") ARE BEING PROVIDED "AS IS." NVIDIA MAKES NO
WARRANTIES, EXPRESSED, IMPLIED, STATUTORY, OR OTHERWISE WITH RESPECT TO
THE MATERIALS, AND EXPRESSLY DISCLAIMS ALL IMPLIED WARRANTIES OF
NONINFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.
TO THE EXTENT NOT PROHIBITED BY LAW, IN NO EVENT WILL NVIDIA BE LIABLE
FOR ANY DAMAGES, INCLUDING WITHOUT LIMITATION ANY DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, PUNITIVE, OR CONSEQUENTIAL DAMAGES, HOWEVER CAUSED
AND REGARDLESS OF THE THEORY OF LIABILITY, ARISING OUT OF ANY USE OF
THIS DOCUMENT, EVEN IF NVIDIA HAS BEEN ADVISED OF THE POSSIBILITY OF
SUCH DAMAGES. Notwithstanding any damages that customer might incur for
any reason whatsoever, NVIDIA's aggregate and cumulative liability
towards customer for the products described herein shall be limited in
accordance with the Terms of Sale for the product.
:::


:::

 {.prev-next-info}
previous

Device Nodes and Capabilities
:::
:::
:::

 {.sidebar-secondary-items .sidebar-secondary__inner}
 {#pst-page-navigation-heading-2 .page-toc .tocsection .onthispage}
On this page
:::

-   [Notice](Notices.html#notice){.reference .internal .nav-link}
-   [OpenCL](Notices.html#opencl){.reference .internal .nav-link}
-   [Trademarks](Notices.html#trademarks){.reference .internal
    .nav-link}
:::
:::
:::
:::
:::
:::
:::
