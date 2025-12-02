# NVIDIA Data Center GPU Manager (DCGM) User Guide

**Source:** https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/
**Scraped:** $(date +%Y-%m-%d)
**Purpose:** Complete DCGM documentation for off-grid GPU management

---


---

 {.wy-side-scroll}
 
:::
:::


:::

 {.wy-nav-content}
 {role="navigation" aria-label="Page navigation"}
-   [ Select Version]{.icon .icon-home}
    [latest]{.version_switcher_placeholder}
-   »
-   Overview
-   

------------------------------------------------------------------------
:::

 {itemprop="articleBody"}
 {#terminology .section}
Terminology[](index.html#terminology "Link to this heading"){.headerlink}
--------------------------------------------------------------------------

+-----------------+-----------------------------------------------------+
| Term            | Meaning                                             |
+=================+=====================================================+
| DCGM            | NVIDIA's Datacenter GPU Manager                     |
+-----------------+-----------------------------------------------------+
| NVIDIA Host     | Standalone executable wrapper for DCGM shared       |
| Engine          | library                                             |
+-----------------+-----------------------------------------------------+
| Host Engine     | Daemon mode of operation for the NVIDIA Host Engine |
| daemon          |                                                     |
+-----------------+-----------------------------------------------------+
| Fabric Manager  | A module within the Host Engine daemon that         |
|                 | supports NVSwitch fabric on DGX-2 or HGX-2.         |
+-----------------+-----------------------------------------------------+
| 3rd-party DCGM  | Any node-level process from a 3rd-party that runs   |
| Agent           | DCGM in Embedded Mode                               |
+-----------------+-----------------------------------------------------+
| Embedded Mode   | DCGM executing as a shared library within a         |
|                 | 3rd-party DCGM agent                                |
+-----------------+-----------------------------------------------------+
| Standalone Mode | DCGM executing as a standalone process via the Host |
|                 | Engine                                              |
+-----------------+-----------------------------------------------------+
| System          | Health checks encompassing the GPU, board and       |
| Validation      | surrounding environment                             |
+-----------------+-----------------------------------------------------+
| HW diagnostic   | System validation component focusing on GPU         |
|                 | hardware correctness                                |
+-----------------+-----------------------------------------------------+
| RAS event       | Reliability, Availability, Serviceability event.    |
|                 | Corresponding to both fatal and non-fatal GPU       |
|                 | issues                                              |
+-----------------+-----------------------------------------------------+
| NVML            | NVIDIA Management Library                           |
+-----------------+-----------------------------------------------------+

: [Terms used in this
document]{.caption-text}[](index.html#id1 "Link to this table"){.headerlink}
:::

 {#provide-robust-online-health-and-diagnostics .section}
### Provide robust, online health and diagnostics[](index.html#provide-robust-online-health-and-diagnostics "Link to this heading"){.headerlink}

The ability to ascertain the health of a GPU and its interaction with
the surrounding system is a critical management need. This need comes in
various forms, from passive background monitoring to quick system
validation to extensive hardware diagnostics. In all cases it is
important to provide these features with minimal impact on the system
and minimal additional environmental requirements. DCGM provides
extensive automated and non-automated health and diagnostic
capabilities.
:::


 {.admonition .note}
Note

As of v2.x, DCGM no longer includes the Fabric Manager, which is a
separate component that needs to be installed for NVSwitch based
systems.
:::
:::


:::


:::
:::
:::


------------------------------------------------------------------------


Built with [Sphinx](https://www.sphinx-doc.org/) using a
[theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by
[Read the Docs](https://readthedocs.org).
:::
:::
:::
:::

---

 {.wy-side-scroll}
 
:::
:::


:::

 {.wy-nav-content}
 {role="navigation" aria-label="Page navigation"}
-   [ Select Version]{.icon .icon-home}
    [latest]{.version_switcher_placeholder}
-   »
-   Getting Started
-   

------------------------------------------------------------------------
:::

 {itemprop="articleBody"}
 {#supported-platforms .section}
Supported Platforms[](getting-started.html#supported-platforms "Link to this heading"){.headerlink}
----------------------------------------------------------------------------------------------------

DCGM currently supports the following products and environments:

-   All NVIDIA Kepler™ (K80) and newer NVIDIA datacenter (previously,
    NVIDIA Tesla®) GPUs

-   NVIDIA® NVSwitch™ on NVIDIA DGX™ A100, NVIDIA HGX™ A100 and newer.

-   All NVIDIA Maxwell™ and newer non-datacenter (e.g. NVIDIA® GeForce®
    or NVIDIA® Quadro®) GPUs

-   CUDA® 7.5+ and NVIDIA Driver R450+

-   Bare metal and virtualized (full passthrough only)


:::

 {#system-requirements .section}
### System Requirements[](getting-started.html#system-requirements "Link to this heading"){.headerlink}


+-----------------------------------+-----------------------------------+
| Resource                          | Requirement                       |
+===================================+===================================+
| Minimum System Memory (Host RAM)  | \>= 16GB                          |
+-----------------------------------+-----------------------------------+
| Minimum CPU Cores                 | \>= Number of GPUs                |
+-----------------------------------+-----------------------------------+
:::

 {.admonition .warning}
    >     Warning
    >
    >     DCGM is tested and designed to run with NVIDIA Datacenter
    >     Drivers. Attempting to run on other drivers, such as a
    >     developer driver, could result in missing functionality.
    >     :::
    >
    >     Please refer to the
    >     [documentation](https://docs.nvidia.com/datacenter/tesla/drivers/index.html#cuda-drivers){.reference
    >     .external} on the various types of branches and support
    >     timelines.
    >
    > 2.  On systems with NVSwitch™ hardware, such as NVIDIA DGX™
    >     systems and NVIDIA HGX™ systems,
    >
    >     > <div>
    >     >
    >     > -   the Fabric Manager package
    >     >
    >     > -   the NVSwitch™ Configuration & Query (NSCQ) package for
    >     >     Hopper or earlier generation GPUs
    >     >
    >     > -   the NVIDIA Switch Device Monitoring (NVSDM) package for
    >     >     Blackwell or later generation GPUs
    >     >
    >     > </div>
    >
    >     
    >
    >     For more information regarding the Fabric Manager package,
    >     please refer to the [Fabric Manager User
    >     Guide](https://docs.nvidia.com/datacenter/tesla/fabric-manager-user-guide/index.html#installation){.reference
    >     .external}
    >
    >     For more information regarding the NSCQ package, please refer
    >     to the [HGX Software
    >     Guide](https://docs.nvidia.com/datacenter/tesla/hgx-software-guide/index.html#nscq){.reference
    >     .external}.
    >
    >     For more information regarding the NVIDIA Switch Device
    >     Monitoring package, please refer to the [NVSDM User
    >     Guide](https://docs.nvidia.com/datacenter/tesla/nvsdm/#getting-started){.reference
    >     .external} and [Driver Installation
    >     Guide](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/index.html#nvswitch){.reference
    >     .external}.
    >
    > </div>

3.  A user needs sufficient permissions to install packages through the
    system package manager. This could be either a root user or a user
    with appropriate sudo privileges.

4.  Any existing datacenter gpu manager system services have been
    stopped, e.g.

     {.highlight}
        $ sudo systemctl list-unit-files nvidia-dcgm.service > /dev/null && \
          sudo systemctl stop nvidia-dcgm
    :::
    :::

5.  Determine the CUDA major version appropriate for the system

    For each NVIDIA GPU driver, there is a corresponding CUDA user-mode
    driver. DCGM binaries targeting a specific major version of the
    user-mode driver are segregated into dedicated packages. The
    user-mode driver major version targeted by binaries installed by a
    given DCGM package is indicated by a `-cuda*`{.docutils .literal
    .notranslate} suffix on the package name, e.g.
    `datacenter-gpu-manager-4-cuda12`{.docutils .literal .notranslate}.

    *Generally speaking*, users should install binaries targeting the
    major version of the CUDA user-mode driver that's installed on their
    system.

    The respective versions of the NVIDIA GPU driver and associated CUDA
    user-mode driver can queried using the `nvidia-smi`{.docutils
    .literal .notranslate} command-line utility, e.g.

     {.highlight}
        $ nvidia-smi -q | grep -E 'Driver Version|CUDA Version'
        Driver Version                            : 575.57.08
        CUDA Version                              : 12.9
    :::
    :::

    In the example above, the major version of the CUDA user-mode driver
    is `12`{.docutils .literal .notranslate}.

     {.highlight-console .notranslate}
    
    :::
    :::

    
:::

 {#amazon-linux-2023 .section}
#### Amazon Linux 2023[](getting-started.html#amazon-linux-2023 "Link to this heading"){.headerlink}

1.  Install the datacenter-gpu-manager-4 package corresponding to the
    CUDA user-mode driver major version, its dependencies, and
    respective associated recommended packages.

     {.highlight}
        $ CUDA_VERSION=<major version of CUDA user-mode driver>
        $ sudo dnf install --assumeyes \
                           --setopt=install_weak_deps=True \
                           datacenter-gpu-manager-4-cuda${CUDA_VERSION}
    :::
    :::

    Installing the recommended packages provides additional DCGM
    functionality which is not present in the [DCGM opensource
    product](https://github.com/NVIDIA/DCGM){.reference .external}. To
    opt out of these packages and the associated functionality, replace
    `--setopt=install_weak_deps=True`{.docutils .literal .notranslate}
    with `--setopt=install_weak_deps=False`{.docutils .literal
    .notranslate}.

2.  (Optional) Install the datacenter-gpu-manager-4 multinode diagnostic
    plugin

     {.highlight}
        $ sudo dnf install --assumeyes datacenter-gpu-manager-4-multinode-cuda${CUDA_VERSION}
    :::
    :::

    

3.  (Optional) Install the datacenter-gpu-manager-4 development files

     {.highlight}
        $ sudo dnf install --assumeyes datacenter-gpu-manager-4-dev
    :::
    :::
:::

 {.highlight-console .notranslate}
    
    :::

    Installing the recommended packages provides additional DCGM
    functionality which is not present in the [DCGM opensource
    product](https://github.com/NVIDIA/DCGM){.reference .external}. To
    opt out of these packages and the associated functionality, replace
    `--setopt=install_weak_deps=True`{.docutils .literal .notranslate}
    with `--setopt=install_weak_deps=False`{.docutils .literal
    .notranslate}.

2.  (Optional) Install the datacenter-gpu-manager-4 multinode diagnostic
    plugin

     {.highlight}
        $ sudo tdnf install --assumeyes datacenter-gpu-manager-4-multinode-cuda${CUDA_VERSION}
    :::
    :::

    

3.  (Optional) Install the datacenter-gpu-manager-4 development files

     {.highlight}
        $ sudo tdnf install --assumeyes datacenter-gpu-manager-4-dev
    :::
    :::
:::

 {.highlight-console .notranslate}
    
    :::

2.  Update the package registry cache

     {.highlight}
        $ sudo apt-get update
    :::
    :::

3.  Install the datacenter-gpu-manager-4 package corresponding to the
    CUDA user-mode driver major version, its dependencies, and
    respective associated recommended packages.

     {.highlight}
        $ CUDA_VERSION=<major version of CUDA user-mode driver>
        $ sudo apt-get install --yes \
                               --install-recommends \
                               datacenter-gpu-manager-4-cuda${CUDA_VERSION}
    :::
    :::

    Installing the recommended packages provides additional DCGM
    functionality which is not present in the [DCGM opensource
    product](https://github.com/NVIDIA/DCGM){.reference .external}. To
    opt out of these packages and the associated functionality, replace
    `--install-recommends`{.docutils .literal .notranslate} with
    `--no-install-recommends`{.docutils .literal .notranslate}.

4.  (Optional) Install the datacenter-gpu-manager-4 multinode diagnostic
    plugin

     {.highlight}
        $ sudo apt install --yes datacenter-gpu-manager-4-multinode-cuda${CUDA_VERSION}
    :::
    :::

    

5.  (Optional) Install the datacenter-gpu-manager-4 development files

     {.highlight}
        $ sudo apt install --yes datacenter-gpu-manager-4-dev
    :::
    :::
:::

 {.highlight-console .notranslate}
    
    :::

2.  Update the package registry cache.

     {.highlight}
        $ sudo dnf clean expire-cache
    :::
    :::

3.  Install the datacenter-gpu-manager-4 package corresponding to the
    CUDA user-mode driver major version, its dependencies, and
    respective associated recommended packages.

     {.highlight}
        $ CUDA_VERSION=<major version of CUDA user-mode driver>
        $ sudo dnf install --assumeyes \
                           --setopt=install_weak_deps=True \
                           datacenter-gpu-manager-4-cuda${CUDA_VERSION}
    :::
    :::

    Installing the recommended packages provides additional DCGM
    functionality which is not present in the [DCGM opensource
    product](https://github.com/NVIDIA/DCGM){.reference .external}. To
    opt out of these packages and the associated functionality, replace
    `--setopt=install_weak_deps=True`{.docutils .literal .notranslate}
    with `--setopt=install_weak_deps=False`{.docutils .literal
    .notranslate}.

4.  (Optional) Install the datacenter-gpu-manager-4 multinode diagnostic
    plugin

     {.highlight}
        $ sudo dnf install --assumeyes datacenter-gpu-manager-4-multinode-cuda${CUDA_VERSION}
    :::
    :::

    

5.  (Optional) Install the datacenter-gpu-manager-4 development files

     {.highlight}
        $ sudo dnf install --assumeyes datacenter-gpu-manager-4-devel
    :::
    :::
:::

 {.highlight-console .notranslate}
    
    :::

2.  Update the package registry cache

     {.highlight}
        $ sudo zypper refresh
    :::
    :::

3.  Install the datacenter-gpu-manager-4 package corresponding to the
    CUDA user-mode driver major version, its dependencies, and
    respective associated recommended packages.

     {.highlight}
        $ CUDA_VERSION=<major version of CUDA user-mode driver>
        $ sudo zypper install --no-confirm \
                              --recommends \
                              datacenter-gpu-manager-4-cuda${CUDA_VERSION}
    :::
    :::

    Installing the recommended packages provides additional DCGM
    functionality which is not present in the [DCGM opensource
    product](https://github.com/NVIDIA/DCGM){.reference .external}. To
    opt out of these packages and the associated functionality, replace
    `--recommends`{.docutils .literal .notranslate} with
    `--no-recommends`{.docutils .literal .notranslate}.

4.  (Optional) Install the datacenter-gpu-manager-4 multinode diagnostic
    plugin

     {.highlight}
        $ sudo zypper install --no-confirm datacenter-gpu-manager-4-multinode-cuda${CUDA_VERSION}
    :::
    :::

    

5.  (Optional) Install the datacenter-gpu-manager-4 development files

     {.highlight}
        $ sudo zypper install --no-confirm datacenter-gpu-manager-4-devel
    :::
    :::
:::
:::

 {.admonition .note}
Note

Note that the default `nvidia-dcgm.service`{.docutils .literal
.notranslate} files included in the installation package use the
`systemd`{.docutils .literal .notranslate} format. If DCGM is being
installed on OS distributions that use the `init.d`{.docutils .literal
.notranslate} format, then these files will need to be modified.
:::

Enable the DCGM systemd service (on reboot) and start it now

 {.highlight}
    $ sudo systemctl --now enable nvidia-dcgm
:::
:::

 {.highlight}
    ● dcgm.service - DCGM service
      Loaded: loaded (/usr/lib/systemd/system/nvidia-dcgm.service; disabled; vendor preset: enabled)
      Active: active (running) since Mon 2024-12-17 12:18:57 EDT; 14s ago
    Main PID: 32847 (nv-hostengine)
        Tasks: 7 (limit: 39321)
      CGroup: /system.slice/nvidia-dcgm.service
              └─32847 /usr/bin/nv-hostengine -n --service-account nvidia-dcgm

    Oct 12 12:18:57 ubuntu1804 systemd[1]: Started DCGM service.
    Oct 12 12:18:58 ubuntu1804 nv-hostengine[32847]: DCGM initialized
    Oct 12 12:18:58 ubuntu1804 nv-hostengine[32847]: Host Engine Listener Started
:::
:::

To verify installation, use `dcgmi`{.docutils .literal .notranslate} to
query the system. You should see a listing of all supported GPUs (and
any NVSwitches) found in the system:

 {.highlight}
    $ dcgmi discovery -l
:::
:::

 {.highlight}
    8 GPUs found.
    +--------+----------------------------------------------------------------------+
    | GPU ID | Device Information                                                   |
    +--------+----------------------------------------------------------------------+
    | 0      | Name: A100-SXM4-40GB                                                 |
    |        | PCI Bus ID: 00000000:07:00.0                                         |
    |        | Device UUID: GPU-1d82f4df-3cf9-150d-088b-52f18f8654e1                |
    +--------+----------------------------------------------------------------------+
    | 1      | Name: A100-SXM4-40GB                                                 |
    |        | PCI Bus ID: 00000000:0F:00.0                                         |
    |        | Device UUID: GPU-94168100-c5d5-1c05-9005-26953dd598e7                |
    +--------+----------------------------------------------------------------------+
    | 2      | Name: A100-SXM4-40GB                                                 |
    |        | PCI Bus ID: 00000000:47:00.0                                         |
    |        | Device UUID: GPU-9387e4b3-3640-0064-6b80-5ace1ee535f6                |
    +--------+----------------------------------------------------------------------+
    | 3      | Name: A100-SXM4-40GB                                                 |
    |        | PCI Bus ID: 00000000:4E:00.0                                         |
    |        | Device UUID: GPU-cefd0e59-c486-c12f-418c-84ccd7a12bb2                |
    +--------+----------------------------------------------------------------------+
    | 4      | Name: A100-SXM4-40GB                                                 |
    |        | PCI Bus ID: 00000000:87:00.0                                         |
    |        | Device UUID: GPU-1501b26d-f3e4-8501-421d-5a444b17eda8                |
    +--------+----------------------------------------------------------------------+
    | 5      | Name: A100-SXM4-40GB                                                 |
    |        | PCI Bus ID: 00000000:90:00.0                                         |
    |        | Device UUID: GPU-f4180a63-1978-6c56-9903-ca5aac8af020                |
    +--------+----------------------------------------------------------------------+
    | 6      | Name: A100-SXM4-40GB                                                 |
    |        | PCI Bus ID: 00000000:B7:00.0                                         |
    |        | Device UUID: GPU-8b354e3e-0145-6cfc-aec6-db2c28dae134                |
    +--------+----------------------------------------------------------------------+
    | 7      | Name: A100-SXM4-40GB                                                 |
    |        | PCI Bus ID: 00000000:BD:00.0                                         |
    |        | Device UUID: GPU-a16e3b98-8be2-6a0c-7fac-9cb024dbc2df                |
    +--------+----------------------------------------------------------------------+
    6 NvSwitches found.
    +-----------+
    | Switch ID |
    +-----------+
    | 11        |
    | 10        |
    | 13        |
    | 9         |
    | 12        |
    | 8         |
    +-----------+
:::
:::
:::
:::

 {#dcgm-shared-library .section}
### DCGM shared library[](getting-started.html#dcgm-shared-library "Link to this heading"){.headerlink}

The user space shared library, `libdcgm.so.4`{.docutils .literal
.notranslate}, is the core component of DCGM. This library implements
the major underlying functionality and exposes this as a set of C-based
APIs. It sits on top of the NVIDIA driver, NVML, and the CUDA Toolkit.
:::

 {.admonition .note}
Note

-   DCGM can run as root or non-root. Some DCGM functionality, such as
    configuration management, are not allowed to be run as non-root.

-   On DGX-2 or HGX-2, nv-hostengine must run as root to enable the
    Fabric Manager.
:::
:::


:::

 {.admonition .note}
Note

In both modes the DCGM library should be run as root. Many features will
not work without privileged access to the GPU, including various
configuration settings and diagnostics.
:::

 {.admonition .warning}
Warning

In this mode it is important that the various DCGM management interfaces
be executed by the 3rd-party within the designated frequency ranges, as
described in the API definitions. Running too frequently will waste
resources with no noticeable gain. Running too infrequently will allow
for gaps in monitoring and management coverage.
:::

Working in this mode requires a sequence of setup steps and a management
thread within the 3rd-party agent that periodically triggers all
necessary DCGM background work. The logic is roughly as follows:

-   On Agent startup

     {.highlight}
        dcgmInit()

        System or job-level setup, e.g.
        call dcgmGroupCreate() to set up GPU groups
        call dcgmWatchFields() to manage watched metrics
        call dcgmPolicySet() to set policy
    :::
    :::

-   Periodic Background Tasks (managed)

     {.highlight}
        Trigger system management behavior, i.e.
        call dcgmUpdateAllFields() to manage metrics
        call dcgmPolicyTrigger() to manage policies

        Gather system data, e.g.
        call dcgmHealthCheck() to check health
        call dcgmGetLatestValues() to get metric updates
    :::
    :::

-   On Agent shutdown

     {.highlight}
        dcgmShutdown()
    :::
    :::


:::

 {.admonition .note}
Note

On DGX-2 or HGX-2 systems, nv-hostengine is automatically started at
system boot time, so that the Fabric Manager can configure and monitor
the NVSwitches.
:::
:::
:::

 {.highlight-console .notranslate}

:::
:::
:::
:::
:::


------------------------------------------------------------------------


Built with [Sphinx](https://www.sphinx-doc.org/) using a
[theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by
[Read the Docs](https://readthedocs.org).
:::
:::
:::
:::

---

 {.wy-side-scroll}
 
:::
:::


:::

 {.wy-nav-content}
 {role="navigation" aria-label="Page navigation"}
-   [ Select Version]{.icon .icon-home}
    [latest]{.version_switcher_placeholder}
-   »
-   Feature Overview
-   

------------------------------------------------------------------------
:::

 {itemprop="articleBody"}
 {.admonition .note}
Note

While DCGM interfaces are shown, all functionality below is accessible
via the C, Python and Go APIs as well.
:::

 {.admonition .note}
Note

Today DCGM does not enforce group behavior beyond itself, e.g. through
OS isolation mechanisms like cgroups. It is expected that clients do
this externally. The ability for clients to opt-in to DCGM enforcement
of this state is likely in the future.
:::

In machines with only one GPU the group concept can be ignored
altogether, as all DCGM operations that require a group can use one
containing that sole GPU. For convenience, at init, DCGM creates a
default group representing all supported GPUs in the system. Groups in
DCGM need not be disjoint. In many cases it may make sense to maintain
overlapping groups for different needs. Global groups, consisting of all
GPUs in the system, are useful for node-level concepts such as global
configuration or global health. Partitioned groups, consisting of only a
subset of GPUs, are useful for job-level concepts such as job stats and
health.

As of DCGM 4, a total of 64 groups, including the 2 system groups, can
be supported. Each group can support up to 1024 entities.


For example, a group created to manage the GPUs associated with a single
job might have the following lifecycle. During prologue operations the
group is created, configured, and used to verify the GPUs are ready for
work. During epilogue operations the groups is used to extract target
information. And while the job is running, DCGM works in the background
to handle the requested behaviors.

Managing groups is very simple. Using the `dcgmi group`{.docutils
.literal .notranslate} subcommand, the following example shows how to
create, list and delete a group.

[![](../_images/managing-groups.png)](../_images/managing-groups.png){.reference
.internal .image-reference}

 {.highlight}
    $ dcgmi group -c GPU_Group
:::
:::

 {.highlight}
    Successfully created group "GPU_Group" with a group ID of 1
:::
:::

 {.highlight}
    $ dcgmi group -l
:::
:::

 {.highlight}
    1 group found.
    +----------------------------------------------------------------------------+
    | GROUPS                                                                     |
    +============+===============================================================+
    | Group ID   | 1                                                             |
    | Group Name | GPU_Group                                                     |
    | GPU ID(s)  | None                                                          |
    +------------+---------------------------------------------------------------+
:::
:::

 {.highlight}
    $ dcgmi group -d 1
:::
:::

 {.highlight}
    Successfully removed group 1
:::
:::

To add GPUs to a group it is first necessary to identify them. This can
be done by first asking DCGM for all supported GPUs in the system.

 {.highlight}
    $ dcgmi discovery -l
:::
:::

 {.highlight}
    2 GPUs found.
    +--------+-------------------------------------------------------------------+
    | GPU ID | Device Information                                                |
    +========+===================================================================+
    | 0      | Name: Tesla K80                                                   |
    |        | PCI Bus ID: 0000:07:00.0                                          |
    |        | Device UUID: GPU-000000000000000000000000000000000000             |
    +--------+-------------------------------------------------------------------+
    | 1      | Name: Tesla K80                                                   |
    |        | PCI Bus ID: 0000:08:00.0                                          |
    |        | Device UUID: GPU-111111111111111111111111111111111111             |
    +--------+-------------------------------------------------------------------+
:::
:::

 {.highlight}
    $ dcgmi group -g 1 -a 0,1
:::
:::

 {.highlight}
    Add to group operation successful.
:::
:::

 {.highlight}
    $ dcgmi group -g 1 -i
:::
:::

 {.highlight}
    +----------------------------------------------------------------------------+
    | GROUPS                                                                     |
    +============+===============================================================+
    | Group ID   | 1                                                             |
    | Group Name | GPU_Group                                                     |
    | GPU ID(s)  | 0, 1                                                          |
    +------------+---------------------------------------------------------------+
:::
:::
:::

 {.highlight-console .notranslate}

:::

 {.highlight}
    Configuration successfully set.
:::
:::

 {.highlight}
    $ dcgmi config -g 1 --get
:::
:::

 {.highlight}
    +--------------------------+------------------------+------------------------+
    | GPU_Group                |                        |                        |
    | Group of 2 GPUs          | TARGET CONFIGURATION   | CURRENT CONFIGURATION  |
    +==========================+========================+========================+
    | Sync Boost               | Not Specified          | Disabled               |
    | SM Application Clock     | Not Specified          | ****                   |
    | Memory Application Clock | Not Specified          | ****                   |
    | ECC Mode                 | Not Specified          | ****                   |
    | Power Limit              | Not Specified          | ****                   |
    | Compute Mode             | E. Process             | E. Process             |
    | Power Profile            | Not Specified          | Not Specified          |
    +--------------------------+------------------------+------------------------+
    **** Non-homogenous settings across group. Use with -v flag to see details.
:::
:::

 {.highlight}
    $ dcgmi config -g 1 --get --verbose
:::
:::

 {.highlight}
    +--------------------------+------------------------+------------------------+
    | GPU ID: 0                |                        |                        |
    | Tesla K20c               | TARGET CONFIGURATION   | CURRENT CONFIGURATION  |
    +==========================+========================+========================+
    | Sync Boost               | Not Specified          | Disabled               |
    | SM Application Clock     | Not Specified          | 705                    |
    | Memory Application Clock | Not Specified          | 2600                   |
    | ECC Mode                 | Not Specified          | Disabled               |
    | Power Limit              | Not Specified          | 225                    |
    | Compute Mode             | E. Process             | E. Process             |
    | Power Profile            | Not Specified          | Not Specified          |
    +--------------------------+------------------------+------------------------+
    +--------------------------+------------------------+------------------------+
    | GPU ID: 1                |                        |                        |
    | GeForce GT 430           | TARGET CONFIGURATION   | CURRENT CONFIGURATION  |
    +==========================+========================+========================+
    | Sync Boost               | Not Specified          | Disabled               |
    | SM Application Clock     | Not Specified          | 562                    |
    | Memory Application Clock | Not Specified          | 2505                   |
    | ECC Mode                 | Not Specified          | Enabled                |
    | Power Limit              | Not Specified          | 200                    |
    | Compute Mode             | E. Process             | E. Process             |
    | Power Profile            | Not Specified          | Not Specified          |
    +--------------------------+------------------------+------------------------+
:::
:::

Once a configuration is set, DCGM maintains the notion of Target and
Current state. Target tracks the user's request for configuration state
while Current tracks the actual state of the GPU and group. These are
generally maintained such that they are equivalent with DCGM restoring
current state to target in situations where that state is lost or
changed. This is common in situations where DCGM has executed some
invasive policy like a health check or GPU reset.
:::

 {#notifications .section}
### Notifications[](feature-overview.html#notifications "Link to this heading"){.headerlink}

The simplest form of a policy is to instruct DCGM to notify a client
when the target condition is met. No further action is performed beyond
this. This is primarily interesting as a callback mechanism within the
programmatic interfaces, as a way to avoid polling.

When running DCGM in embedded mode such callbacks are invoked
automatically by DCGM each time a registered condition is hit, at which
point the client can deal with that event as desired. The client must
register through the appropriate API calls to receive these callbacks.
Doing so transparently instructs DCGM to track the conditions that
trigger those results.


The `dcgmi policy`{.docutils .literal .notranslate} subcommand does
allow access to some of this functionality from the command line via
setting of conditions and via a blocking notification mechanism. This
can be useful when watching for a particular problem, e.g. during a
debugging session.

As an example, the following shows setting a notification policy for
PCIe fatal and non-fatal events:

 {.highlight}
    $ dcgmi policy -g 2 --set 0,0 -p
:::
:::

 {.highlight}
    Policy successfully set.
:::
:::

 {.highlight}
    $ dcgmi policy -g 2 --get
:::
:::

 {.highlight}
    Policy information
    +---------------------------+------------------------------------------------+
    | GPU_Group                 | Policy Information                             |
    +===========================+================================================+
    | Violation conditions      | PCI errors and replays                         |
    | Isolation mode            | Manual                                         |
    | Action on violation       | None                                           |
    | Validation after action   | None                                           |
    | Validation failure action | None                                           |
    +---------------------------+------------------------------------------------+
    **** Non-homogenous settings across group. Use with -v flag to see details.
:::
:::

 {.highlight}
    $ dcgmi policy -g 2 --get --verbose
:::
:::

 {.highlight}
    Policy information
    +---------------------------+------------------------------------------------+
    | GPU ID: 0                 | Policy Information                             |
    +===========================+================================================+
    | Violation conditions      | PCI errors and replays                         |
    | Isolation mode            | Manual                                         |
    | Action on violation       | None                                           |
    | Validation after action   | None                                           |
    | Validation failure action | None                                           |
    +---------------------------+------------------------------------------------+
    +---------------------------+------------------------------------------------+
    | GPU ID: 1                 | Policy Information                             |
    +===========================+================================================+
    | Violation conditions      | PCI errors and replays                         |
    | Isolation mode            | Manual                                         |
    | Action on violation       | None                                           |
    | Validation after action   | None                                           |
    | Validation failure action | None                                           |
    +---------------------------+-----------------------------------------------
:::
:::

Once such a policy is set the client will receive notifications
accordingly. While this is primarily interesting for programmatic use
cases, `dcgmi policy`{.docutils .literal .notranslate} can be invoked to
wait for policy notifications:

 {.highlight}
    $ dcgmi policy -g 2 --reg
:::
:::

 {.highlight}
    Listening for violations
    ...
    A PCIe error has violated policy manager values.
    ...
:::
:::
:::

 {.highlight-console .notranslate}

:::

 {.highlight}
    Policy successfully set.
:::
:::

 {.highlight}
    $ dcgmi policy -g 1 --get
:::
:::

 {.highlight}
    Policy information for group 1
    +----------------------------------------------------------------------------+
    | GPU ID: 0                 | Policy Information                             |
    +===========================+================================================+
    | Violation Conditions      | Double-bit ECC errors                          |
    | Isolation mode            | Manual                                         |
    | Action on violation       | Reset GPU                                      |
    | Validation after action   | NVVS (Short)                                   |
    | Validation failure action | None                                           |
    +---------------------------+------------------------------------------------+
    ...
:::
:::

As shown in the previous section, dcgmi policy can also be used to watch
for notifications associated with this policy.
:::
:::

 {.highlight-console .notranslate}

:::

 {.highlight}
    Successfully started process watches on group 1.
:::
:::

Stats recording must be enabled prior to the start of the target
workload(s) for reliable information to be available.

Once a job has completed DCGM can be queried for information about that
job, both at the summary level of a group and, if needed, broken down
individually between the GPUs within that group. The suggested behavior
is that clients perform this query in epilogue scripts as part of job
cleanup.

An example of group-level data provided by `dcgmi stats`{.docutils
.literal .notranslate}. Note: the `-v`{.docutils .literal .notranslate}
flag, which adds fields that offer additional detail, is required to get
all of the details seen in the output below.

 {.highlight}
    $ dcgmi stats --pid 1234 -v
:::
:::

 {.highlight}
    Successfully retrieved process info for pid: 1234. Process ran on 1 GPUs.
    +----------------------------------------------------------------------------+
    | GPU ID: 0                                                                  |
    +==================================+=========================================+
    |------- Execution Stats ----------+-----------------------------------------|
    | Start Time *                     | Tue Nov 3 17:36:43 2015                 |
    | End Time *                       | Tue Nov 3 17:38:33 2015                 |
    | Total Execution Time (sec) *     | 110.33                                  |
    | No. of Conflicting Processes *   | 0                                       |
    +------- Performance Stats --------+-----------------------------------------+
    | Energy Consumed (Joules)         | 15758                                   |
    | Power Usage (Watts)              | Avg: 150, Max: 250, Min: 100            |
    | Max GPU Memory Used (bytes) *    | 213254144                               |
    | SM Clock (MHz)                   | Avg: 837, Max: 875, Min: 679            |
    | Memory Clock (MHz)               | Avg: 2505, Max: 2505, Min: 2505         |
    | SM Utilization (%)               | Avg: 99, Max: 100, Min: 99              |
    | Memory Utilization (%)           | Avg: 2, Max: 3, Min: 0                  |
    | PCIe Rx Bandwidth (megabytes)    | Avg: N/A, Max: N/A, Min: N/A            |
    | PCIe Tx Bandwidth (megabytes)    | Avg: N/A, Max: N/A, Min: N/A            |
    +------- Event Stats --------------+-----------------------------------------+
    | Single Bit ECC Errors            | 0                                       |
    | Double Bit ECC Errors            | 0                                       |
    | PCIe Replay Warnings             | 0                                       |
    | Critical XID Errors              | 0                                       |
    +------- Slowdown Stats -----------+-----------------------------------------+
    | Due to - Power (%)               | 0                                       |
    | - Thermal (%)                    | 0                                       |
    | - Reliability (%)                | 0                                       |
    | - Board Limit (%)                | 0                                       |
    | - Low Utilization (%)            | 0                                       |
    | - Sync Boost (%)                 | Not Supported                           |
    +----------------------------------+-----------------------------------------+
    (*) Represents a process statistic. Otherwise device statistic during process lifetime listed.
:::
:::

For certain frameworks the processes and their PIDs cannot be associated
with a job directly, and the process associated with a job may spawn
many children. In order to get job-level stats for such a scenario, DCGM
must be notified when a job starts and stops. It is required that the
client notifies DCGM with the user defined job id and the corresponding
GPU group at job prologue, and notifies with the job id at the job
epilogue. The user can query the job stats using the job id and get
aggregated stats across all the pids during the window of interest.

An example of notifying DCGM at the beginning and end of the job using
`dcgmi`{.docutils .literal .notranslate}:

 {.highlight}
    $ dcgmi stats -g 1 -s <user-provided-jobid>
:::
:::

 {.highlight}
    Successfully started recording stats for <user-provided-jobid>
:::
:::

 {.highlight}
    $ dcgmi stats -x <user-provided-jobid>
:::
:::

 {.highlight}
    Successfully stopped recording stats for <user-provided-jobid>
:::
:::

The stats corresponding to the job id already watched can be retrieved
using `dcgmi`{.docutils .literal .notranslate}. Note: the `-v`{.docutils
.literal .notranslate} flag is required to get all of the details seen
in the output below.

 {.highlight}
    $ dcgmi stats -j <user-provided-jobid> -v
:::
:::

 {.highlight}
    Successfully retrieved statistics for <user-provided-jobid>
    +----------------------------------------------------------------------------+
    | GPU ID: 0                                                                  |
    +==================================+=========================================+
    |------- Execution Stats ----------+-----------------------------------------|
    | Start Time                       | Tue Nov 3 17:36:43 2015                 |
    | End Time                         | Tue Nov 3 17:38:33 2015                 |
    | Total Execution Time (sec)       | 110.33                                  |
    | No. of Processes                 | 0                                       |
    +----- Performance Stats ----------+-----------------------------------------+
    | Energy Consumed (Joules)         | 15758                                   |
    | Power Usage (Watts)              | Avg: 150, Max: 250, Min 100             |
    | Max GPU Memory Used (bytes)      | 213254144                               |
    | SM Clock (MHz)                   | Avg: 837, Max: 875, Min: 679            |
    | Memory Clock (MHz)               | Avg: 2505, Max: 2505, Min: 2505         |
    | SM Utilization (%)               | Avg: 99, Max: 100, Min: 99              |
    | Memory Utilization (%)           | Avg: 2, Max: 3, Min: 0                  |
    | PCIe Rx Bandwidth (megabytes)    | Avg: N/A, Max: N/A, Min: N/A            |
    | PCIe Tx Bandwidth (megabytes)    | Avg: N/A, Max: N/A, Min: N/A            |
    +----- Event Stats ----------------+-----------------------------------------+
    | Single Bit ECC Errors            | 0                                       |
    | Double Bit ECC Errors            | 0                                       |
    | PCIe Replay Warnings             | 0                                       |
    | Critical XID Errors              | 0                                       |
    +----- Slowdown Stats -------------+-----------------------------------------+
    | Due to - Power (%)               | 0                                       |
    | - Thermal (%)                    | 0                                       |
    | - Reliability (%)                | 0                                       |
    | - Board Limit (%)                | 0                                       |
    | - Low Utilization (%)            | 0                                       |
    | - Sync Boost (%)                 | Not Supported                           |
    +----------------------------------+-----------------------------------------+
:::
:::
:::

 {.admonition .warning}
Warning

All of these are online diagnostics, meaning they run within the current
environment. There is potential for factors beyond the GPU to influence
behavior in negative ways. While these tools try to identify those
situations, full offline diagnostics delivered via a different NVIDIA
tool are required for complete hardware validation, and are required for
RMA.
:::

 {.highlight-console .notranslate}

:::

 {.highlight}
    Health monitor systems set successfully.
:::
:::

To view the current status of all GPUs in the group the client can
simply query for the overall group health. The result is an overall
health score for the group as well as individual results for each
impacted GPU, identifying key problems.

For example, DCGM would show the following when excessive PCIe replay
events or InfoROM issues are detected:

 {.highlight}
    $ dcgmi health -g 1 -c
:::
:::

 {.highlight}
    Health Monitor Report
    +----------------------------------------------------------------------------+
    | Group 1          | Overall Health: Warning                                 |
    +==================+=========================================================+
    | GPU ID: 0        | Warning                                                 |
    |                  | PCIe system: Warning - Detected more than 8 PCIe        |
    |                  | replays per minute for GPU 0: 13                        |
    +------------------+---------------------------------------------------------+
    | GPU ID: 1        | Warning                                                 |
    |                  | InfoROM system: Warning - A corrupt InfoROM has been    |
    |                  | detected in GPU 1.                                      |
    +------------------+---------------------------------------------------------+
:::
:::

+---+-----------+------------------------------------------------------+
| S | Error     | Cause                                                |
| y | Code      |                                                      |
| s |           |                                                      |
| t |           |                                                      |
| e |           |                                                      |
| m |           |                                                      |
+===+===========+======================================================+
| P | DCGM\_FR\ | There were more than 8 PCIe replays in the last      |
| C | _PCI\_REP | minute.                                              |
| I | LAY\_RATE |                                                      |
| e |           |                                                      |
+---+-----------+------------------------------------------------------+
| M | DCGM\_    | One or more volatile DBEs are rerpoted               |
| e | FR\_VOLAT | (non-recoverable memory errors since the last GPU    |
| m | ILE\_DBE\ | reset)                                               |
| o | _DETECTED |                                                      |
| r |           |                                                      |
| y |           |                                                      |
+---+-----------+------------------------------------------------------+
| M | DCGM\_FR\ | There is one or more pending page retirement.        |
| e | _PENDING\ |                                                      |
| m | _PAGE\_RE |                                                      |
| o | TIREMENTS |                                                      |
| r |           |                                                      |
| y |           |                                                      |
+---+-----------+------------------------------------------------------+
| M | DCGM      | 63 or more retired pages have occurred on one GPU.   |
| e | \_FR\_RET |                                                      |
| m | IRED\_PAG |                                                      |
| o | ES\_LIMIT |                                                      |
| r |           |                                                      |
| y |           |                                                      |
+---+-----------+------------------------------------------------------+
| M | DCGM\_FR\ | There have been more than 15 total retired pages due |
| e | _RETIRED\ | to DBEs and at least one in the last week.           |
| m | _PAGES\_D |                                                      |
| o | BE\_LIMIT |                                                      |
| r |           |                                                      |
| y |           |                                                      |
+---+-----------+------------------------------------------------------+
| M | DC        | One or more row remapping failures occurred.         |
| e | GM\_FR\_R |                                                      |
| m | OW\_REMAP |                                                      |
| o | \_FAILURE |                                                      |
| r |           |                                                      |
| y |           |                                                      |
+---+-----------+------------------------------------------------------+
| M | D         | A GPU experienced an uncontained error (XID 95       |
| e | CGM\_FR\_ | occurred).                                           |
| m | UNCONTAIN |                                                      |
| o | ED\_ERROR |                                                      |
| r |           |                                                      |
| y |           |                                                      |
+---+-----------+------------------------------------------------------+
| I | DCGM\_FR  | Inforom corruption detected.                         |
| n | \_CORRUPT |                                                      |
| f | \_INFOROM |                                                      |
| o |           |                                                      |
| r |           |                                                      |
| o |           |                                                      |
| m |           |                                                      |
+---+-----------+------------------------------------------------------+
| T | DCGM\     | A thermal violation was detected on a GPU in the     |
| h | _FR\_CLOC | last minute.                                         |
| e | KS\_EVENT |                                                      |
| r | \_THERMAL |                                                      |
| m |           |                                                      |
| a |           |                                                      |
| l |           |                                                      |
+---+-----------+------------------------------------------------------+
| T | DCGM      | A CPU's temperature one minute ago and its current   |
| h | \_FR\_FIE | temperature are both above the warning temperature.  |
| e | LD\_THRES |                                                      |
| r | HOLD\_DBL |                                                      |
| m |           |                                                      |
| a |           |                                                      |
| l |           |                                                      |
+---+-----------+------------------------------------------------------+
| T | DCGM      | A CPU's current temperature is above the critical    |
| h | \_FR\_FIE | temperature.                                         |
| e | LD\_THRES |                                                      |
| r | HOLD\_DBL |                                                      |
| m |           |                                                      |
| a |           |                                                      |
| l |           |                                                      |
+---+-----------+------------------------------------------------------+
| P | DCG       | A GPU had a power violation detected in the last     |
| o | M\_FR\_CL | minute.                                              |
| w | OCKS\_EVE |                                                      |
| e | NT\_POWER |                                                      |
| r |           |                                                      |
+---+-----------+------------------------------------------------------+
| P | DCGM      | A CPU's power usage is above its power limit.        |
| o | \_FR\_FIE |                                                      |
| w | LD\_THRES |                                                      |
| e | HOLD\_DBL |                                                      |
| r |           |                                                      |
+---+-----------+------------------------------------------------------+
| N | DCGM\_    | An NVLink reported 1 or more replay or recovery      |
| V | FR\_NVLIN | errors.                                              |
| L | K\_ERROR\ |                                                      |
| i | _CRITICAL |                                                      |
| n |           |                                                      |
| k |           |                                                      |
+---+-----------+------------------------------------------------------+
| N | DCG       | An NVLink reported more than 100 CRC errors per      |
| V | M\_FR\_NV | second.                                              |
| L | LINK\_CRC |                                                      |
| i | \_ERROR\_ |                                                      |
| n | THRESHOLD |                                                      |
| k |           |                                                      |
+---+-----------+------------------------------------------------------+
| N | DCGM\     | An NVSwitch reported one or more fatal errors        |
| V | _FR\_NVSW |                                                      |
| S | ITCH\_FAT |                                                      |
| W | AL\_ERROR |                                                      |
| i |           |                                                      |
| t |           |                                                      |
| c |           |                                                      |
| h |           |                                                      |
| F |           |                                                      |
| a |           |                                                      |
| t |           |                                                      |
| a |           |                                                      |
| l |           |                                                      |
+---+-----------+------------------------------------------------------+
| N | DCGM      | One or more NVLinks is being reported as down.       |
| V | \_FR\_NVL |                                                      |
| S | INK\_DOWN |                                                      |
| W |           |                                                      |
| i |           |                                                      |
| t |           |                                                      |
| c |           |                                                      |
| h |           |                                                      |
| F |           |                                                      |
| a |           |                                                      |
| t |           |                                                      |
| a |           |                                                      |
| l |           |                                                      |
+---+-----------+------------------------------------------------------+
| N | D         | An NVSwitch reported one or more non-fatal errors    |
| V | CGM\_FR\_ |                                                      |
| S | NVSWITCH\ |                                                      |
| W | _NON\_FAT |                                                      |
| i | AL\_ERROR |                                                      |
| t |           |                                                      |
| c |           |                                                      |
| h |           |                                                      |
| N |           |                                                      |
| o |           |                                                      |
| n |           |                                                      |
| - |           |                                                      |
| F |           |                                                      |
| a |           |                                                      |
| t |           |                                                      |
| a |           |                                                      |
| l |           |                                                      |
+---+-----------+------------------------------------------------------+

: [Failure
Conditions]{.caption-text}[](feature-overview.html#id4 "Link to this table"){.headerlink}


:::


:::
:::
:::
:::
:::
:::
:::
:::

Run Level

Test Duration

Test Classes

Software

Hardware

Integration

Stress

Quick

-r 1

\~ seconds

Deployment

--

--

Medium

-r 2

\~ 2 minutes

Deployment

Memory Test

PCIe/NVLink

--

Long

-r 3

\~ 15 minutes

Deployment

-   Memory Test

-   Memory Bandwidth

-   HW Diagnostic Tests

PCIe/NVLink

-   Diagnostic

-   Targeted Stress

-   Targeted Power

While simple tests of runtime libraries and configuration are possible
on non-Tesla GPUs (Run Level 1), DCGM is also able to perform hardware
diagnostics, connectivity diagnostics, and a suite of stress tests on
Tesla GPUs to help validate health and isolate problems. The actions in
each test type are further described in the section GPU Parameters.

For example, running the full system validation (long test):

 {.highlight}
    $ dcgmi diag -r 3
:::
:::

 {.highlight}
    Successfully ran diagnostic for group.
    +---------------------------+------------------------------------------------+
    | Diagnostic                | Result                                         |
    +===========================+================================================+
    |-----  Metadata  ----------+------------------------------------------------|
    | DCGM Version              | 4.0.0                                          |
    | Driver Version Detected   | 550.90.07                                      |
    | GPU Device IDs Detected   | 25b6, 25b6, 25b6, 25b6                         |
    |-----  Deployment  --------+------------------------------------------------|
    | software                  | Pass                                           |
    |                           | GPU0: Pass                                     |
    |                           | GPU1: Pass                                     |
    |                           | GPU2: Pass                                     |
    |                           | GPU3: Pass                                     |
    +-----  Hardware  ----------+------------------------------------------------+
    | memory                    | Pass                                           |
    |                           | GPU0: Pass                                     |
    |                           | GPU1: Pass                                     |
    |                           | GPU2: Pass                                     |
    |                           | GPU3: Pass                                     |
    | diagnostic                | Pass                                           |
    |                           | GPU0: Pass                                     |
    |                           | GPU1: Pass                                     |
    |                           | GPU2: Pass                                     |
    |                           | GPU3: Pass                                     |
    +-----  Integration  -------+------------------------------------------------+
    | pcie                      | Pass                                           |
    |                           | GPU0: Pass                                     |
    |                           | GPU1: Pass                                     |
    |                           | GPU2: Pass                                     |
    |                           | GPU3: Pass                                     |
    +-----  Stress  ------------+------------------------------------------------+
    | memory_bandwidth          | Pass                                           |
    |                           | GPU0: Pass                                     |
    |                           | GPU1: Pass                                     |
    |                           | GPU2: Pass                                     |
    |                           | GPU3: Pass                                     |
    | targeted_stress           | Pass                                           |
    |                           | GPU0: Pass                                     |
    |                           | GPU1: Pass                                     |
    |                           | GPU2: Pass                                     |
    |                           | GPU3: Pass                                     |
    | targeted_power            | Pass                                           |
    |                           | GPU0: Pass                                     |
    |                           | GPU1: Pass                                     |
    |                           | GPU2: Pass                                     |
    |                           | GPU3: Pass                                     |
    +---------------------------+------------------------------------------------+
:::
:::

The diagnostic tests can also be run as part of the validation phase of
action-based policies. A common scenario, for example, would be to run
the short version of the test as a validation to a DBE page retirement
action.

DCGM will store logs from these tests on the host file system. Two types
of logs exist:

-   Hardware diagnostics include an encrypted binary log, only viewable
    by NVIDIA.

-   System validation and stress checks provide additional time series
    data via JSON text files. These can be viewed in numerous programs
    to see much more detailed information about GPU behavior during each
    test.

 {.highlight-console .notranslate}

:::

 {.highlight}
    +-------------------+--------------------------------------------------------+
    | GPU ID: 0         | Topology Information                                   |
    +===================+========================================================+
    | CPU Core Affinity | 0 - 11                                                 |
    +-------------------+--------------------------------------------------------+
    | To GPU 1          | Connected via an on-board PCIe switch                  |
    | To GPU 2          | Connected via a PCIe host bridge                       |
    +-------------------+--------------------------------------------------------+
:::
:::

And for the group-level view:

 {.highlight}
    $ dcgmi topo -g 1
:::
:::

 {.highlight}
    +-------------------+--------------------------------------------------------+
    | MyGroup           | Topology Information                                   |
    +===================+========================================================+
    | CPU Core Affinity | 0 - 11                                                 |
    +-------------------+--------------------------------------------------------+
    | NUMA Optimal      | True                                                   |
    +-------------------+--------------------------------------------------------+
    | Worst Path        | Connected via a PCIe host bridge                       |
    +-------------------+--------------------------------------------------------+
    .........
:::
:::
:::

 {.highlight-console .notranslate}

:::

 {.highlight}
    +-------------------------------------------------------------+
    | GPU ID: 0 | NVLINK Error Counts                             |
    +-------------------------------------------------------------+
    |Link 0     | CRC FLIT Error      | 0                         |
    |Link 0     | CRC Data Error      | 0                         |
    |Link 0     | Replay Error        | 0                         |
    |Link 0     | Recovery Error      | 0                         |
    |Link 1     | CRC FLIT Error      | 0                         |
    |Link 1     | CRC Data Error      | 0                         |
    |Link 1     | Replay Error        | 0                         |
    |Link 1     | Recovery Error      | 0                         |
    |Link 2     | CRC FLIT Error      | 0                         |
    |Link 2     | CRC Data Error      | 0                         |
    |Link 2     | Replay Error        | 0                         |
    |Link 2     | Recovery Error      | 0                         |
    |Link 3     | CRC FLIT Error      | 0                         |
    |Link 3     | CRC Data Error      | 0                         |
    |Link 3     | Replay Error        | 0                         |
    |Link 3     | Recovery Error      | 0                         |
    +-------------------------------------------------------------+
:::
:::
:::

 {.highlight-console .notranslate}

:::

 {.highlight}
    4 field groups found.
    +----------------------------------------------------------------------------+
    | FIELD GROUPS                                                               |
    +============+===============================================================+
    | ID         | 1                                                             |
    | Name       | DCGM_INTERNAL_1SEC                                            |
    | Field IDs  | 38, 73, 86, 112, 113, 119, 73, 51, 47, 46, 66, 72, 61, 118,...|
    +------------+---------------------------------------------------------------+
    | ID         | 2                                                             |
    | Name       | DCGM_INTERNAL_30SEC                                           |
    | Field IDs  | 124, 125, 126, 130, 131, 132, 133, 134, 135, 136, 137, 138,...|
    +------------+---------------------------------------------------------------+
    | ID         | 3                                                             |
    | Name       | DCGM_INTERNAL_HOURLY                                          |
    | Field IDs  | 117, 55, 56, 64, 62, 63, 6, 5, 26, 8, 17, 107, 22, 108, 30, 31|
    +------------+---------------------------------------------------------------+
    | ID         | 4                                                             |
    | Name       | DCGM_INTERNAL_JOB                                             |
    | Field IDs  | 111, 65, 36, 37, 38, 101, 102, 77, 78, 40, 41, 121, 115, 11...|
    +------------+---------------------------------------------------------------+
:::
:::

If you want to create your own field group, pick a unique name for it,
decide which field IDs you want inside of it, and run:

 {.highlight}
    $ dcgmi fieldgroup -c mygroupname -f 50,51,52
:::
:::

 {.highlight}
    Successfully created field group "mygroupname" with a field group ID of 5
:::
:::

Note that field IDs come from dcgm\_fields.h and are the macros that
start with `DCGM_FI_`{.docutils .literal .notranslate}.

Once you have created a field group, you can query its info:

 {.highlight}
    $ dcgmi fieldgroup -i --fieldgroup 5
:::
:::

 {.highlight}
    +----------------------------------------------------------------------------+
    | FIELD GROUPS                                                               |
    +============+===============================================================+
    | ID         | 5                                                             |
    | Name       | mygroupname                                                   |
    | Field IDs  | 50, 51, 52                                                    |
    +------------+---------------------------------------------------------------+
:::
:::

If you want to delete a field group, run the following command:

 {.highlight}
    $ dcgmi fieldgroup -d -g 5
:::
:::

 {.highlight}
    Successfully removed field group 5
:::
:::

Note that DCGM creates a few field groups internally. Field groups that
are created internally, like the ones above, cannot be removed. Here is
an example of trying to delete a DCGM-internal field group:

 {.highlight}
    $ dcgmi fieldgroup -d -g 1
:::
:::

 {.highlight}
    Error: Cannot destroy field group 1. Return: No permission.
:::
:::
:::

 {.highlight-console .notranslate}

:::
:::

 {#overview .section}
### Overview[](feature-overview.html#overview "Link to this heading"){.headerlink}

DCGM supports CPU monitoring for NVIDIA datacenter CPUs. In general, CPU
fields are treated the same way as other NVIDIA hardware entities. This
section includes additional information to help you get started.
:::


 {.highlight-console .notranslate}

:::

Watch field temperatures using dcgmi dmon

 {.highlight}
    $ dcgmi dmon --entity-id cpu:{0-3} -e 1130
:::
:::
:::
:::

 {#metrics .section}
### Metrics[](feature-overview.html#metrics "Link to this heading"){.headerlink}

The following new device-level profiling metrics are supported. The
definitions and corresponding DCGM field IDs are listed. By default,
DCGM provides the metrics at a sample rate of 1Hz (every 1000ms). Users
can query the metrics at any configurable frequency (minimum is 100ms)
from DCGM (for example, see `dcgmi dmon -d`{.docutils .literal
.notranslate}).

+-----------+-----------------------------------------------+-----------+
| Metric    | Definition                                    | DCGM      |
|           |                                               | Field     |
|           |                                               | Name      |
|           |                                               | (DCGM     |
|           |                                               | \_FI\_\*) |
|           |                                               | and ID    |
+===========+===============================================+===========+
| Graphics  | The fraction of time any portion of the       | PROF\_    |
| Engine    | graphics or compute engines were active. The  | GR\_ENGIN |
| Activity  | graphics engine is active if a                | E\_ACTIVE |
|           | graphics/compute context is bound and the     | (ID:      |
|           | graphics/compute pipe is busy. The value      | 1001)     |
|           | represents an average over a time interval    |           |
|           | and is not an instantaneous value.            |           |
+-----------+-----------------------------------------------+-----------+
| SM        | The fraction of time at least one warp was    | PROF\_S   |
| Activity  | active on a multiprocessor, averaged over all | M\_ACTIVE |
|           | multiprocessors. Note that "active" does not  | (ID:      |
|           | necessarily mean a warp is actively           | 1002)     |
|           | computing. For instance, warps waiting on     |           |
|           | memory requests are considered active. The    |           |
|           | value represents an average over a time       |           |
|           | interval and is not an instantaneous value. A |           |
|           | value of 0.8 or greater is necessary, but not |           |
|           | sufficient, for effective use of the GPU. A   |           |
|           | value less than 0.5 likely indicates          |           |
|           | ineffective GPU usage.                        |           |
|           |                                               |           |
|           | Given a simplified GPU architectural view, if |           |
|           | a GPU has N SMs then a kernel using N blocks  |           |
|           | that runs over the entire time interval will  |           |
|           | correspond to an activity of 1 (100%). A      |           |
|           | kernel using N/5 blocks that runs over the    |           |
|           | entire time interval will correspond to an    |           |
|           | activity of 0.2 (20%). A kernel using N       |           |
|           | blocks that runs over one fifth of the time   |           |
|           | interval, with the SMs otherwise idle, will   |           |
|           | also have an activity of 0.2 (20%). The value |           |
|           | is insensitive to the number of threads per   |           |
|           | block (see                                    |           |
|           | `DCGM_FI_PROF_SM_OCCUPANCY`{.docutils         |           |
|           | .literal .notranslate}).                      |           |
+-----------+-----------------------------------------------+-----------+
| SM        | The fraction of resident warps on a           | P         |
| Occupancy | multiprocessor, relative to the maximum       | ROF\_SM\_ |
|           | number of concurrent warps supported on a     | OCCUPANCY |
|           | multiprocessor. The value represents an       | (ID:      |
|           | average over a time interval and is not an    | 1003)     |
|           | instantaneous value. Higher occupancy does    |           |
|           | not necessarily indicate better GPU usage.    |           |
|           | For GPU memory bandwidth limited workloads    |           |
|           | (see `DCGM_FI_PROF_DRAM_ACTIVE`{.docutils     |           |
|           | .literal .notranslate}), higher occupancy is  |           |
|           | indicative of more effective GPU usage.       |           |
|           | However if the workload is compute limited    |           |
|           | (i.e. not GPU memory bandwidth or latency     |           |
|           | limited), then higher occupancy does not      |           |
|           | necessarily correlate with more effective GPU |           |
|           | usage.                                        |           |
|           |                                               |           |
|           | Calculating occupancy is not simple and       |           |
|           | depends on factors such as the GPU            |           |
|           | properties, the number of threads per block,  |           |
|           | registers per thread, and shared memory per   |           |
|           | block. Use the [CUDA Occupancy                |           |
|           | Calculator](https://docs.nvidia.com/cuda/cud  |           |
|           | a-occupancy-calculator/index.html){.reference |           |
|           | .external} to explore various occupancy       |           |
|           | scenarios.                                    |           |
+-----------+-----------------------------------------------+-----------+
| Tensor    | The fraction of cycles the tensor (HMMA /     | PROF\_PI  |
| Activity  | IMMA) pipe was active. The value represents   | PE\_TENSO |
|           | an average over a time interval and is not an | R\_ACTIVE |
|           | instantaneous value. Higher values indicate   | (ID:      |
|           | higher utilization of the Tensor Cores. An    | 1004)     |
|           | activity of 1 (100%) is equivalent to issuing |           |
|           | a tensor instruction every other cycle for    |           |
|           | the entire time interval. An activity of 0.2  |           |
|           | (20%) could indicate 20% of the SMs are at    |           |
|           | 100% utilization over the entire time period, |           |
|           | 100% of the SMs are at 20% utilization over   |           |
|           | the entire time period, 100% of the SMs are   |           |
|           | at 100% utilization for 20% of the time       |           |
|           | period, or any combination in between (see    |           |
|           | `DCGM_FI_PROF_SM_ACTIVE`{.docutils .literal   |           |
|           | .notranslate} to help disambiguate these      |           |
|           | possibilities).                               |           |
+-----------+-----------------------------------------------+-----------+
| FP64      | The fraction of cycles the FP64 (double       | PROF\_    |
| Engine    | precision) pipe was active. The value         | PIPE\_FP6 |
| Activity  | represents an average over a time interval    | 4\_ACTIVE |
|           | and is not an instantaneous value. Higher     | (ID:      |
|           | values indicate higher utilization of the     | 1006)     |
|           | FP64 cores. An activity of 1 (100%) is        |           |
|           | equivalent to a FP64 instruction on [every SM |           |
|           | every fourth                                  |           |
|           | c                                             |           |
|           | ycle](https://docs.nvidia.com/cuda/volta-tuni |           |
|           | ng-guide/index.html#sm-scheduling){.reference |           |
|           | .external} on Volta over the entire time      |           |
|           | interval. An activity of 0.2 (20%) could      |           |
|           | indicate 20% of the SMs are at 100%           |           |
|           | utilization over the entire time period, 100% |           |
|           | of the SMs are at 20% utilization over the    |           |
|           | entire time period, 100% of the SMs are at    |           |
|           | 100% utilization for 20% of the time period,  |           |
|           | or any combination in between (see            |           |
|           | DCGM\_FI\_PROF\_SM\_ACTIVE to help            |           |
|           | disambiguate these possibilities).            |           |
+-----------+-----------------------------------------------+-----------+
| FP32      | The fraction of cycles the FMA (FP32 (single  | PROF\_    |
| Engine    | precision), and integer) pipe was active. The | PIPE\_FP3 |
| Activity  | value represents an average over a time       | 2\_ACTIVE |
|           | interval and is not an instantaneous value.   | (ID:      |
|           | Higher values indicate higher utilization of  | 1007)     |
|           | the FP32 cores. An activity of 1 (100%) is    |           |
|           | equivalent to a FP32 instruction every other  |           |
|           | cycle over the entire time interval. An       |           |
|           | activity of 0.2 (20%) could indicate 20% of   |           |
|           | the SMs are at 100% utilization over the      |           |
|           | entire time period, 100% of the SMs are at    |           |
|           | 20% utilization over the entire time period,  |           |
|           | 100% of the SMs are at 100% utilization for   |           |
|           | 20% of the time period, or any combination in |           |
|           | between (see                                  |           |
|           | `DCGM_FI_PROF_SM_ACTIVE`{.docutils .literal   |           |
|           | .notranslate} to help disambiguate these      |           |
|           | possibilities).                               |           |
+-----------+-----------------------------------------------+-----------+
| FP16      | The fraction of cycles the FP16 (half         | PROF\_    |
| Engine    | precision) pipe was active. The value         | PIPE\_FP1 |
| Activity  | represents an average over a time interval    | 6\_ACTIVE |
|           | and is not an instantaneous value. Higher     | (ID:      |
|           | values indicate higher utilization of the     | 1008)     |
|           | FP16 cores. An activity of 1 (100%) is        |           |
|           | equivalent to a FP16 instruction every other  |           |
|           | cycle over the entire time interval. An       |           |
|           | activity of 0.2 (20%) could indicate 20% of   |           |
|           | the SMs are at 100% utilization over the      |           |
|           | entire time period, 100% of the SMs are at    |           |
|           | 20% utilization over the entire time period,  |           |
|           | 100% of the SMs are at 100% utilization for   |           |
|           | 20% of the time period, or any combination in |           |
|           | between (see                                  |           |
|           | `DCGM_FI_PROF_SM_ACTIVE`{.docutils .literal   |           |
|           | .notranslate} to help disambiguate these      |           |
|           | possibilities).                               |           |
+-----------+-----------------------------------------------+-----------+
| Memory BW | The fraction of cycles where data was sent to | PROF\_DRA |
| Ut        | or received from device memory. The value     | M\_ACTIVE |
| ilization | represents an average over a time interval    | (ID:      |
|           | and is not an instantaneous value. Higher     | 1005)     |
|           | values indicate higher utilization of device  |           |
|           | memory. An activity of 1 (100%) is equivalent |           |
|           | to a DRAM instruction every cycle over the    |           |
|           | entire time interval (in practice a peak of   |           |
|           | \~0.8 (80%) is the maximum achievable). An    |           |
|           | activity of 0.2 (20%) indicates that 20% of   |           |
|           | the cycles are reading from or writing to     |           |
|           | device memory over the time interval.         |           |
+-----------+-----------------------------------------------+-----------+
| NVLink    | The rate of data transmitted / received over  | PROF\     |
| Bandwidth | NVLink, not including protocol headers, in    | _NVLINK\_ |
|           | bytes per second. The value represents an     | TX\_BYTES |
|           | average over a time interval and is not an    | (1011)    |
|           | instantaneous value. The rate is averaged     | and       |
|           | over the time interval. For example, if 1 GB  | PROF\     |
|           | of data is transferred over 1 second, the     | _NVLINK\_ |
|           | rate is 1 GB/s regardless of the data         | RX\_BYTES |
|           | transferred at a constant rate or in bursts.  | (1012)    |
|           | The theoretical maximum NVLink Gen2 bandwidth |           |
|           | is 25 GB/s per link per direction.            |           |
+-----------+-----------------------------------------------+-----------+
| PCIe      | The rate of data transmitted / received over  | P         |
| Bandwidth | the PCIe bus, including both protocol headers | ROF\_PCIE |
|           | and data payloads, in bytes per second. The   | \_\[T\|R\ |
|           | value represents an average over a time       | ]X\_BYTES |
|           | interval and is not an instantaneous value.   | (ID: 1009 |
|           | The rate is averaged over the time interval.  | (TX);     |
|           | For example, if 1 GB of data is transferred   | 1010      |
|           | over 1 second, the rate is 1 GB/s regardless  | (RX))     |
|           | of the data transferred at a constant rate or |           |
|           | in bursts. The theoretical maximum PCIe Gen3  |           |
|           | bandwidth is 985 MB/s per lane.               |           |
+-----------+-----------------------------------------------+-----------+

: [Device Level GPU
Metrics]{.caption-text}[](feature-overview.html#id5 "Link to this table"){.headerlink}

Profiling of the GPU counters requires administrator privileges starting
with Linux drivers 418.43 or later. This is documented
[here](https://developer.nvidia.com/nvidia-development-tools-solutions-ERR_NVGPUCTRPERM-permission-issue-performance-counters){.reference
.external}. When using profiling metrics from DCGM, ensure that
nv-hostengine is started with superuser privileges.
:::

 {.highlight-console .notranslate}

:::

From the output above, we can determine that for this GPU (in this
example, an NVIDIA T4), a metric from each letter group can be collected
without multiplexing. From this example, a metric from `A.1`{.docutils
.literal .notranslate} can be collected with another metric from
`A.1`{.docutils .literal .notranslate} without multiplexing. A metric
from `A.1`{.docutils .literal .notranslate} will be multiplexed with
another metric from `A.2`{.docutils .literal .notranslate} or
`A.3`{.docutils .literal .notranslate}. Metrics from different letter
groups can be combined for concurrent collection (without requiring
multiplexing by DCGM).

Building on this example further, on T4 these metrics can be collected
together without multiplexing:

 {.highlight}
    sm_active + sm_occupancy + tensor_active + fp32_active
:::
:::

The above DCGM command will show what groupings are supported by the
hardware for concurrent collection.
:::

 {.highlight-console .notranslate}

:::

To allow DCGM to co-exist with the usage of other profiling tools, it is
recommended to pause metrics collection with DCGM when the tools are in
use and then resume after the usage of the tools is complete.

With `dcgmi profile`{.docutils .literal .notranslate}, the
`--pause`{.docutils .literal .notranslate} and `--resume`{.docutils
.literal .notranslate} options can be used:

 {.highlight}
    $ dcgmi profile --pause
    $ dcgmi profile --resume
:::
:::

When using DCGM APIs, the following APIs can be called from the
monitoring process: `dcgmProfPause()`{.docutils .literal .notranslate}
and `dcgmProfResume()`{.docutils .literal .notranslate}

When paused, DCGM will publish `BLANK`{.docutils .literal .notranslate}
values for profiling metrics. These `BLANK`{.docutils .literal
.notranslate} values can be tested with
`DCGM_FP64_IS_BLANK(value)`{.docutils .literal .notranslate} in the C or
Python bindings.
:::

 {.highlight-console .notranslate}

:::

 {.highlight}
    Skipping CreateDcgmGroups() since DCGM validation is disabled
    Skipping CreateDcgmGroups() since DCGM validation is disabled
    Skipping WatchFields() since DCGM validation is disabled
    Skipping CreateDcgmGroups() since DCGM validation is disabled
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm 0.000 (250362.2 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm 0.000 (252917.0 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm 0.000 (253971.7 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm 0.000 (253700.2 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm 0.000 (252599.0 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm 0.000 (253134.6 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm 0.000 (252676.7 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm 0.000 (252861.4 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm 0.000 (252764.1 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm 0.000 (253109.4 gflops)
    Worker 0:0[1004]: Message: Bus ID 00000000:00:04.0 mapped to cuda device ID 0
    DCGM CudaContext Init completed successfully.

    CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_MULTIPROCESSOR: 2048
    CUDA_VISIBLE_DEVICES:
    CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT: 108
    CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_MULTIPROCESSOR: 167936
    CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR: 8
    CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR: 0
    CU_DEVICE_ATTRIBUTE_GLOBAL_MEMORY_BUS_WIDTH: 5120
    CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE: 1215
    Max Memory bandwidth: 1555200000000 bytes (1555.2 GiB)
    CU_DEVICE_ATTRIBUTE_ECC_SUPPORT: true
:::
:::

In another console, use the `dcgmi dmon -e`{.docutils .literal
.notranslate} command to view the various performance metrics (streamed
to stdout) reported by DCGM as the CUDA workload runs on the GPU. In
this example, DCGM reports the GPU activity, TensorCore activity and
Memory utilization at a frequency of 1Hz (or 1000ms). As can be seen,
the GPU is busy doing work (\~99% of Graphics Activity showing that the
SMs are busy), with the TensorCore activity pegged to \~93%. Note that
`dcgmi`{.docutils .literal .notranslate} is currently returning the
metrics for GPU ID: 0. On a multi-GPU system, you can specify the GPU ID
for which DCGM should return the metrics. By default, the metrics are
returned for all the GPUs in the system.

 {.highlight}
    $ dcgmi dmon -e 1001,1004,1005
:::
:::

 {.highlight}
    # Entity  GRACT  TENSO  DRAMA
          Id
        GPU 0  0.000  0.000  0.000
        GPU 0  0.000  0.000  0.000
        GPU 0  0.000  0.000  0.000
        GPU 0  0.552  0.527  0.000
        GPU 0  0.969  0.928  0.000
        GPU 0  0.973  0.931  0.000
        GPU 0  0.971  0.929  0.000
        GPU 0  0.969  0.927  0.000
        GPU 0  0.971  0.929  0.000
        GPU 0  0.971  0.930  0.000
        GPU 0  0.973  0.931  0.000
        GPU 0  0.974  0.931  0.000
        GPU 0  0.971  0.930  0.000
        GPU 0  0.974  0.932  0.000
        GPU 0  0.972  0.930  0.000
:::
:::
:::

 {#example-1 .section}
#### Example 1[](feature-overview.html#example-1 "Link to this heading"){.headerlink}

In this example, let's generate a CUDA workload using dcgmproftester and
observe metrics using `dcgmi dmon`{.docutils .literal .notranslate}.

In this example, we follow these steps to demonstrate the collection of
metrics for MIG devices:

-   Create MIG devices (assumes that the GPU has MIG mode enabled)

-   Verify DCGM can list the devices

-   Create a group of devices for DCGM to monitor

-   Run CUDA workloads on the desired MIG device(s)

-   Use dcgmi dmon to stream metrics

 {.line}
Step 1: Create MIG Devices
:::


:::

 {.highlight}
    $ sudo nvidia-smi mig -cgi 9,9 -C
:::
:::

 {.highlight}
    ...
    +-----------------------------------------------------------------------------+
    | MIG devices:                                                                |
    +------------------+----------------------+-----------+-----------------------+
    | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
    |      ID  ID  Dev |           BAR1-Usage | SM     Unc| CE  ENC  DEC  OFA  JPG|
    |                  |                      |        ECC|                       |
    |==================+======================+===========+=======================|
    |  0    1   0   0  |     11MiB / 20096MiB | 42      0 |  3   0    2    0    0 |
    |                  |      0MiB / 32767MiB |           |                       |
    +------------------+----------------------+-----------+-----------------------+
    |  0    2   0   1  |     11MiB / 20096MiB | 42      0 |  3   0    2    0    0 |
    |                  |      0MiB / 32767MiB |           |                       |
    +------------------+----------------------+-----------+-----------------------+
:::
:::

 {.line}
Step 2: Verify enumeration by DCGM
:::


:::

 {.highlight}
    $ dcgmi discovery -c
:::
:::

 {.highlight}
    +-------------------+--------------------------------------------------------------------+
    | Instance Hierarchy                                                                     |
    +===================+====================================================================+
    | GPU 0             | GPU GPU-5fd15f35-e148-2992-4ecb-9825e534f253 (EntityID: 0)         |
    | -> I 0/1          | GPU Instance (EntityID: 0)                                         |
    |    -> CI 0/1/0    | Compute Instance (EntityID: 0)                                     |
    | -> I 0/2          | GPU Instance (EntityID: 1)                                         |
    |    -> CI 0/2/0    | Compute Instance (EntityID: 1)                                     |
    +-------------------+--------------------------------------------------------------------+
:::
:::

 {.line}
Step 3: Creation of MIG device groups
:::


:::

 {.highlight}
    $ dcgmi group -c mig-ex1 -a 0,i:0,i:1
:::
:::

 {.highlight}
    Successfully created group "mig-ex1" with a group ID of 8
    Specified entity ID is valid but unknown: i:0. ParsedResult: ParsedGpu(i:0)
    Specified entity ID is valid but unknown: i:1. ParsedResult: ParsedGpu(i:1)
    Add to group operation successful.
:::
:::

Now, we can list the devices added to the group and see that the group
contains the GPU (GPU:0), GPU Instances (0 and 1):

 {.highlight}
    $ dcgmi group -l
:::
:::

 {.highlight}
    +-------------------+----------------------------------------------------------+
    | GROUPS                                                                       |
    | 1 group found.                                                               |
    +===================+==========================================================+
    | Groups            |                                                          |
    | -> 8              |                                                          |
    |    -> Group ID    | 8                                                        |
    |    -> Group Name  | mig-ex1                                                  |
    |    -> Entities    | GPU 0, GPU_I 0, GPU_I 1                                  |
    +-------------------+----------------------------------------------------------+
:::
:::

 {.line}
Step 4: Run CUDA workloads
:::


:::

 {.highlight}
    $ sudo dcgmproftester11 --no-dcgm-validation -t 1004 -d 120
:::
:::

 {.highlight}
    Skipping CreateDcgmGroups() since DCGM validation is disabled
    Skipping CreateDcgmGroups() since DCGM validation is disabled
    Skipping CreateDcgmGroups() since DCGM validation is disabled
    Skipping WatchFields() since DCGM validation is disabled
    Skipping CreateDcgmGroups() since DCGM validation is disabled
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm { GPU: 0.000, GI: 0.000, CI: 0.000 } (102659.5 gflops)
    Worker 0:1[1004]: TensorEngineActive: generated ???, dcgm { GPU: 0.000, GI: 0.000, CI: 0.000 } (102659.8 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm { GPU: 0.000, GI: 0.000, CI: 0.000 } (107747.3 gflops)
    Worker 0:1[1004]: TensorEngineActive: generated ???, dcgm { GPU: 0.000, GI: 0.000, CI: 0.000 } (107787.3 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm { GPU: 0.000, GI: 0.000, CI: 0.000 } (108107.6 gflops)
    Worker 0:1[1004]: TensorEngineActive: generated ???, dcgm { GPU: 0.000, GI: 0.000, CI: 0.000 } (108102.3 gflops)
    Worker 0:0[1004]: TensorEngineActive: generated ???, dcgm { GPU: 0.000, GI: 0.000, CI: 0.000 } (108001.2 gflops)

    snip...snip

    Worker 0:0[1004]: Message: DCGM CudaContext Init completed successfully.

    CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_MULTIPROCESSOR: 2048
    CUDA_VISIBLE_DEVICES: MIG-GPU-5fd15f35-e148-2992-4ecb-9825e534f253/1/0
    CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT: 42
    CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_MULTIPROCESSOR: 167936
    CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR: 8
    CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR: 0
    CU_DEVICE_ATTRIBUTE_GLOBAL_MEMORY_BUS_WIDTH: 5120
    CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE: 1215
    Max Memory bandwidth: 1555200000000 bytes (1555.2 GiB)
    CU_DEVICE_ATTRIBUTE_ECC_SUPPORT: true

    Worker 0:1[1004]: Message: DCGM CudaContext Init completed successfully.

    CU_DEVICE_ATTRIBUTE_MAX_THREADS_PER_MULTIPROCESSOR: 2048
    CUDA_VISIBLE_DEVICES: MIG-GPU-5fd15f35-e148-2992-4ecb-9825e534f253/2/0
    CU_DEVICE_ATTRIBUTE_MULTIPROCESSOR_COUNT: 42
    CU_DEVICE_ATTRIBUTE_MAX_SHARED_MEMORY_PER_MULTIPROCESSOR: 167936
    CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MAJOR: 8
    CU_DEVICE_ATTRIBUTE_COMPUTE_CAPABILITY_MINOR: 0
    CU_DEVICE_ATTRIBUTE_GLOBAL_MEMORY_BUS_WIDTH: 5120
    CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE: 1215
    Max Memory bandwidth: 1555200000000 bytes (1555.2 GiB)
    CU_DEVICE_ATTRIBUTE_ECC_SUPPORT: true

    Skipping UnwatchFields() since DCGM validation is disabled
:::
:::

 {.line}
Step 5: Stream metrics via `dcgmi dmon`{.docutils .literal .notranslate}
:::


:::

 {.highlight}
    $ dcgmi dmon -e 1001,1004 -g 8
:::
:::

 {.highlight}
    # Entity  GRACT  TENSO
          Id
        GPU 0  0.000  0.000
      GPU-I 0  0.000  0.000
      GPU-I 1  0.000  0.000
        GPU 0  0.000  0.000
      GPU-I 0  0.000  0.000
      GPU-I 1  0.000  0.000
        GPU 0  0.457  0.442
      GPU-I 0  0.534  0.516
      GPU-I 1  0.533  0.515
        GPU 0  0.845  0.816
      GPU-I 0  0.986  0.953
      GPU-I 1  0.985  0.952
        GPU 0  0.846  0.817
      GPU-I 0  0.987  0.953
      GPU-I 1  0.986  0.953
        GPU 0  0.846  0.817
      GPU-I 0  0.987  0.954
      GPU-I 1  0.986  0.953
        GPU 0  0.843  0.815
      GPU-I 0  0.985  0.951
      GPU-I 1  0.983  0.950
        GPU 0  0.845  0.817
      GPU-I 0  0.987  0.953
      GPU-I 1  0.985  0.952
        GPU 0  0.844  0.816
      GPU-I 0  0.985  0.952
      GPU-I 1  0.984  0.951
        GPU 0  0.845  0.816
      GPU-I 0  0.986  0.952
      GPU-I 1  0.985  0.952
:::
:::
:::

 {.highlight-console .notranslate}

:::

 {.highlight}
    +--------------------------------------------------------------------------+
    | GPU instance profiles:                                                   |
    | GPU   Name          ID    Instances   Memory     P2P    SM    DEC   ENC  |
    |                           Free/Total   GiB              CE    JPEG  OFA  |
    |==========================================================================|
    |   0  MIG 1g.5gb     19     0/7        4.75       No     14     0     0   |
    |                                                          1     0     0   |
    +--------------------------------------------------------------------------+
    |   0  MIG 2g.10gb    14     0/3        9.75       No     28     1     0   |
    |                                                          2     0     0   |
    +--------------------------------------------------------------------------+
    |   0  MIG 3g.20gb     9     0/2        19.62      No     42     2     0   |
    |                                                          3     0     0   |
    +--------------------------------------------------------------------------+
    |   0  MIG 4g.20gb     5     0/1        19.62      No     56     2     0   |
    |                                                          4     0     0   |
    +--------------------------------------------------------------------------+
    |   0  MIG 7g.40gb     0     0/1        39.50      No     98     5     0   |
    |                                                          7     1     1   |
    +--------------------------------------------------------------------------+
:::
:::

Because the MIG geometry in this example is 3g.20gb, the compute
resources are = 2\*42/98 or 85.71%. We can now interpret GRACT from the
`dcgmi dmon`{.docutils .literal .notranslate} output:

 {.highlight}
      GPU 0  0.845  0.816
    GPU-I 0  0.986  0.952
    GPU-I 1  0.985  0.952
:::
:::

Since each GPU instance is 98.6% active, the entire GPU = 0.8571\*0.986
or 84.5% utilized. The same interpretation can be extended to Tensor
Core utilization.
:::


:::
:::


------------------------------------------------------------------------


Built with [Sphinx](https://www.sphinx-doc.org/) using a
[theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by
[Read the Docs](https://readthedocs.org).

---

 {.wy-side-scroll}
 
:::
:::


:::

 {.wy-nav-content}
 {role="navigation" aria-label="Page navigation"}
-   [ Select Version]{.icon .icon-home}
    [latest]{.version_switcher_placeholder}
-   »
-   DCGM Modularity
-   

------------------------------------------------------------------------
:::

 {itemprop="articleBody"}
 {#module-list .section}
Module List[](dcgm-modularity.html#module-list "Link to this heading"){.headerlink}
------------------------------------------------------------------------------------

The following modules have been added to DCGM.

+--------------+-----+-------------------------------------------------+
| Module ID    | Num | Description                                     |
|              | ber |                                                 |
+==============+=====+=================================================+
| DcgmModu     | 1   | Manages NVSwitches and is required in order for |
| leIdNvSwitch |     | DGX-2 / HGX-2 systems to function properly.     |
|              |     | This can be loaded explicitly by adding         |
|              |     | `-l -g`{.docutils .literal .notranslate} to     |
|              |     | your nv-hostengine command line.                |
|              |     |                                                 |
|              |     | Requires nv-hostengine to run as root.          |
+--------------+-----+-------------------------------------------------+
| Dcgm         | 2   | Provides telemetry on paravirtualized GPUs.     |
| ModuleIdVGPU |     |                                                 |
+--------------+-----+-------------------------------------------------+
| DcgmModule   | 3   | Provides time-series data about the running     |
| IdIntrospect |     | state of nv-hostengine.                         |
+--------------+-----+-------------------------------------------------+
| DcgmMo       | 4   | Provides passive health checks of GPUs and      |
| duleIdHealth |     | NVSwitches                                      |
+--------------+-----+-------------------------------------------------+
| DcgmMo       | 5   | Allows users to register callbacks based off    |
| duleIdPolicy |     | GPU events like XIDs and overtemp.              |
+--------------+-----+-------------------------------------------------+
| DcgmMo       | 6   | Allows users to set GPU configuration. Requires |
| duleIdConfig |     | nv-hostengine to run as root.                   |
+--------------+-----+-------------------------------------------------+
| Dcgm         | 7   | Enables users to call the DCGM GPU Diagnostic   |
| ModuleIdDiag |     |                                                 |
+--------------+-----+-------------------------------------------------+
| DcgmModul    | 8   | Enables users to monitor profiling metrics.     |
| eIdProfiling |     |                                                 |
+--------------+-----+-------------------------------------------------+
| DcgmMo       | 9   | Enables users to monitor supported Nvidia CPUs. |
| duleIdSysmon |     |                                                 |
+--------------+-----+-------------------------------------------------+
| DcgmMo       | 10  | Enables users to run multi-node diagnostics.    |
| duleIdMndiag |     |                                                 |
+--------------+-----+-------------------------------------------------+
:::

 {.highlight-console .notranslate}

:::

Note that NVSwitch must be explicitly loaded with the `-l`{.docutils
.literal .notranslate} and `-g`{.docutils .literal .notranslate}
options. To only load the NVSwitch module and disable all others, use
the following command line:

 {.highlight}
    $ nv-hostengine -l -g --blacklist-modules 2,3,4,5,6,7
:::
:::

You can query the status of all of the dcgm modules with the following
command:

 {.highlight}
    $ dcgmi modules -l
:::
:::

 {.highlight}
    +-----------+--------------------+------------------------------------------+
    | List Modules                                                              |
    | Status: Success                                                           |
    +===========+====================+==========================================+
    | Module ID | Name               | State                                    |
    +-----------+--------------------+------------------------------------------+
    | 0         | Core               | Loaded                                   |
    | 1         | NvSwitch           | Not loaded                               |
    | 2         | VGPU               | Not loaded                               |
    | 3         | Introspection      | Not loaded                               |
    | 4         | Health             | Not loaded                               |
    | 5         | Policy             | Not loaded                               |
    | 6         | Config             | Not loaded                               |
    | 7         | Diag               | Not loaded                               |
    | 8         | Profiling          | Not loaded                               |
    | 9         | Sysmon             | Not loaded                               |
    | 10        | Mndiag             | Not loaded                               |
    +-----------+--------------------+------------------------------------------+
:::
:::

Only modules that are Not Loaded can be disabled.

To disable a module, take note of its module name from the table above.
We'll disable module Policy for this example:

 {.highlight}
    $ dcgmi modules --blacklist Policy
:::
:::

 {.highlight}
    +-----------------------------+---------------------------------------------+
    | Blacklist Module                                                          |
    | Status: Success                                                           |
    | Successfully blacklisted module Policy                                    |
    +=============================+=============================================+
    +-----------------------------+---------------------------------------------+
:::
:::

Once a module has been disabled, you can verify that by listing modules
again:

 {.highlight}
    $ dcgmi modules -l
:::
:::

 {.highlight}
    +-----------+--------------------+------------------------------------------+
    | List Modules                                                              |
    | Status: Success                                                           |
    +===========+====================+==========================================+
    | Module ID | Name               | State                                    |
    +-----------+--------------------+------------------------------------------+
    | 0         | Core               | Loaded                                   |
    | 1         | NvSwitch           | Not loaded                               |
    | 2         | VGPU               | Not loaded                               |
    | 3         | Introspection      | Not loaded                               |
    | 4         | Health             | Not loaded                               |
    | 5         | Policy             | Blacklisted                              |
    | 6         | Config             | Not loaded                               |
    | 7         | Diag               | Not loaded                               |
    | 8         | Profiling          | Not loaded                               |
    | 9         | Sysmon             | Not loaded                               |
    | 10        | Mndiag             | Not loaded                               |
    +-----------+--------------------+------------------------------------------+
:::
:::
:::
:::
:::
:::


------------------------------------------------------------------------


Built with [Sphinx](https://www.sphinx-doc.org/) using a
[theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by
[Read the Docs](https://readthedocs.org).
:::
:::
:::
:::

---

 {.wy-side-scroll}
 
:::
:::


:::

 {.wy-nav-content}
 {role="navigation" aria-label="Page navigation"}
-   [ Select Version]{.icon .icon-home}
    [latest]{.version_switcher_placeholder}
-   »
-   DCGM Diagnostics
-   

------------------------------------------------------------------------
:::

 {itemprop="articleBody"}
 {#overview .section}
Overview[](dcgm-diagnostics.html#overview "Link to this heading"){.headerlink}
-------------------------------------------------------------------------------

The NVIDIA Validation Suite (NVVS) is now called DCGM Diagnostics. As of
DCGM v1.5, running NVVS as a standalone utility is now deprecated and
all the functionality (including command line options) is available via
the DCGM command-line utility ('dcgmi'). For brevity, the rest of the
document may use DCGM Diagnostics and NVVS interchangeably.


     | :::     | :::     | :::     |
|                   | name    |  {.line |  {.line |  {.line |  {.line |
|                   | (m      | -block} | -block} | -block} | -block} |
|                   | easured | :::     | :::     | :::     | :::     |
|                   | on      | {.line} | {.line} | {.line} | {.line} |
|                   | Hopper  | r1      | r2      | r3      | r4      |
|                   | GPU     | (Short) | (       | (Long)  | (Extra  |
|                   | s       | :::     | Medium) | :::     | Long)   |
|                   | ystems) |         | :::     |         | :::     |
|                   |         | :::     |         | :::     |         |
|                   |         | {.line} | :::     | {.line} | :::     |
|                   |         | \< 2.5  | {.line} | \< 10   | {.line} |
|                   |         | S       | \< 2.5  | mins on | \< 45   |
|                   |         | econds. | mins on | 4 GPU   | mins on |
|                   |         | :::     | 4 GPU   | s       | 4 GPU   |
|                   |         | :::     | s       | ystems, | s       |
|                   |         |         | ystems, | \< 35   | ystems, |
|                   |         |         | \< 10.5 | mins on | \< 2.25 |
|                   |         |         | mins on | 8 GPU   | hours   |
|                   |         |         | 8 GPU   | s       | on 8    |
|                   |         |         | s       | ystems. | GPU     |
|                   |         |         | ystems. | :::     | s       |
|                   |         |         | :::     | :::     | ystems. |
|                   |         |         | :::     |         | :::     |
|                   |         |         |         |         | :::     |
+===================+=========+=========+=========+=========+=========+
| Software          | `softw  | Yes     | Yes     | Yes     | Yes     |
|                   | are`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
| PCIe + NVLink     | `p      |         | Yes     | Yes     | Yes     |
|                   | cie`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
| GPU Memory        | `mem    |         | Yes     | Yes     | Yes     |
|                   | ory`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
| Memory Bandwidth  | `memory |         | Yes     | Yes     | Yes     |
|                   | _bandwi |         |         |         |         |
|                   | dth`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
| Diagnostics       | `       |         |         | Yes     | Yes     |
|                   | diagnos |         |         |         |         |
|                   | tic`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
| Targeted Stress   | `targe  |         |         | Yes     | Yes     |
|                   | ted_str |         |         |         |         |
|                   | ess`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
| Targeted Power    | `targ   |         |         | Yes     | Yes     |
|                   | eted_po |         |         |         |         |
|                   | wer`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
| NVBandwidth       | `n      |         |         | Yes     | Yes     |
|                   | vbandwi |         |         |         |         |
|                   | dth`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
| Memory Stress     | `memt   |         |         |         | Yes     |
|                   | est`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
| Input EDPp        | `pu     |         |         |         | Yes     |
|                   | lse`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
:::
:::

 {#command-line-options .section}
### Command Line options[](dcgm-diagnostics.html#command-line-options "Link to this heading"){.headerlink}

The various command line options are designed to control general
execution parameters, whereas detailed changes to execution behavior are
contained within the configuration files detailed in the next section.

The following table lists the various options supported by DCGM
Diagnostics:

+-----------+-----------+-----------+--------------------------------+
| Short     | Long      | Parameter | Description                    |
| option    | option    |           |                                |
+===========+===========+===========+================================+
| `-g`{     | `         | groupId   | The device group ID to query.  |
| .docutils | --group`{ |           |                                |
| .literal  | .docutils |           |                                |
| .not      | .literal  |           |                                |
| ranslate} | .not      |           |                                |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
|           | `--host`{ | IP/FQDN   | Connects to specified IP or    |
|           | .docutils |           | fully-qualified domain name.   |
|           | .literal  |           | To connect to a host engine    |
|           | .not      |           | that was started with -d (unix |
|           | ranslate} |           | socket), prefix the unix       |
|           |           |           | socket filename with           |
|           |           |           | `unix://`{.docutils .literal   |
|           |           |           | .notranslate}. \[default =     |
|           |           |           | `localhost`{.docutils .literal |
|           |           |           | .notranslate}\]                |
+-----------+-----------+-----------+--------------------------------+
| `-h`{     | `--help`{ |           | Displays usage information and |
| .docutils | .docutils |           | exits.                         |
| .literal  | .literal  |           |                                |
| .not      | .not      |           |                                |
| ranslate} | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
| `-r`{     | `--run`{  | diag      | Run a diagnostic. (Note:       |
| .docutils | .docutils |           | higher numbered tests include  |
| .literal  | .literal  |           | all beneath.):                 |
| .not      | .not      |           |                                |
| ranslate} | ranslate} |           | -   1 - Quick (System          |
|           |           |           |     Validation                 |
|           |           |           |                                |
|           |           |           | -   2 - Medium (Extended       |
|           |           |           |     System Validation)         |
|           |           |           |                                |
|           |           |           | -   3 - Long (System HW        |
|           |           |           |     Diagnostics)               |
|           |           |           |                                |
|           |           |           | -   4 - Extended               |
|           |           |           |     (Longer-running System HW  |
|           |           |           |     Diagnostics)               |
|           |           |           |                                |
|           |           |           | Specific tests to run may be   |
|           |           |           | specified by name, and         |
|           |           |           | multiple tests may be          |
|           |           |           | specified as a comma separated |
|           |           |           | list. For example, the         |
|           |           |           | command:                       |
|           |           |           |                                |
|           |           |           | dcgmi diag -r                  |
|           |           |           | "pcie,diagnostic"              |
|           |           |           |                                |
|           |           |           | would run the PCIe and         |
|           |           |           | Diagnostic tests together.     |
+-----------+-----------+-----------+--------------------------------+
| `-p`{     | `--par    | test      | Test parameters to set for     |
| .docutils | ameters`{ | \_name.va | this run.                      |
| .literal  | .docutils | riable\_n |                                |
| .not      | .literal  | ame=varia |                                |
| ranslate} | .not      | ble\_name |                                |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
| `-c`{     | `--con    | full/p    | Path to the configuration      |
| .docutils | figfile`{ | ath/to/co | file.                          |
| .literal  | .docutils | nfig/file |                                |
| .not      | .literal  |           |                                |
| ranslate} | .not      |           |                                |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
| `-f`{     | `--fakeGp |           | A comma-separated list of the  |
| .docutils | uListfake |           | fake gpus on which the         |
| .literal  | GpuList`{ |           | diagnostic should run. For     |
| .not      | .docutils |           | internal/testing use only.     |
| ranslate} | .literal  |           | Cannot be used with            |
|           | .not      |           | `-g/-i`{.docutils .literal     |
|           | ranslate} |           | .notranslate}.                 |
+-----------+-----------+-----------+--------------------------------+
| `-i`{     | `--       | gpuList   | A comma-separated list of the  |
| .docutils | gpuList`{ |           | gpus on which the diagnostic   |
| .literal  | .docutils |           | should run. Cannot be used     |
| .not      | .literal  |           | with `-g`{.docutils .literal   |
| ranslate} | .not      |           | .notranslate}.                 |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
| `-v`{     | `-        |           | Show information and warnings  |
| .docutils | verbose`{ |           | for each test.                 |
| .literal  | .docutils |           |                                |
| .not      | .literal  |           |                                |
| ranslate} | .not      |           |                                |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
|           | `stat     |           | Only output the statistics     |
|           | sonfail`{ |           | files if there was a failure   |
|           | .docutils |           |                                |
|           | .literal  |           |                                |
|           | .not      |           |                                |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
|           | `--d      | file      |                                |
|           | ebugLogFi |           |                                |
|           | ledebug`{ |           |                                |
|           | .docutils |           |                                |
|           | .literal  |           |                                |
|           | .not      |           |                                |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
|           | `--st     | plugin    | Write the plugin statistics to |
|           | atspath`{ | s         | the given path rather than the |
|           | .docutils | tatistics | current directory              |
|           | .literal  | path      |                                |
|           | .not      |           |                                |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
| `-d`{     | `--deb    | debug     | Debug level (One of NONE,      |
| .docutils | ugLevel`{ | level     | FATAL, ERROR, WARN, INFO,      |
| .literal  | .docutils |           | DEBUG, VERB). Default: DEBUG.  |
| .not      | .literal  |           | The logfile can be specified   |
| ranslate} | .not      |           | by the --debugLogFile          |
|           | ranslate} |           | parameter.                     |
+-----------+-----------+-----------+--------------------------------+
| `-j`{     | `--json`{ |           | Print the output in a json     |
| .docutils | .docutils |           | format.                        |
| .literal  | .literal  |           |                                |
| .not      | .not      |           |                                |
| ranslate} | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
|           | `--       |           | Specify which clocks event     |
|           | clockseve |           | reasons should be ignored. You |
|           | nt-mask`{ |           | can provide a comma separated  |
|           | .docutils |           | list of reasons. For example,  |
|           | .literal  |           | specifying 'HW\_SLOWDOWN       |
|           | .not      |           | ,SW\_THERMAL' would ignore the |
|           | ranslate} |           | HW\_SLOWDOWN and SW\_THERMAL   |
|           |           |           | reasons. Alternatively, you    |
|           |           |           | can specify the integer value  |
|           |           |           | of the ignore bitmask. For the |
|           |           |           | bitmask, multiple reasons may  |
|           |           |           | be specified by the sum of     |
|           |           |           | their bit masks. For example,  |
|           |           |           | specifying '40' would ignore   |
|           |           |           | the HW\_SLOWDOWN and           |
|           |           |           | SW\_THERMAL reasons.           |
|           |           |           |                                |
|           |           |           | Valid clocks event reasons and |
|           |           |           | their corresponding bitmasks   |
|           |           |           | (given in parentheses) are:    |
|           |           |           |                                |
|           |           |           | -   HW\_SLOWDOWN (8)           |
|           |           |           |                                |
|           |           |           | -   SW\_THERMAL (32)           |
|           |           |           |                                |
|           |           |           | -   HW\_THERMAL (64)           |
|           |           |           |                                |
|           |           |           | -   HW\_POWER\_BRAKE (128)     |
+-----------+-----------+-----------+--------------------------------+
|           | `--thrott |           | Deprecated: please use         |
|           | le-mask`{ |           | `--clocksevent-mask`{.docutils |
|           | .docutils |           | .literal .notranslate}         |
|           | .literal  |           | instead.                       |
|           | .not      |           |                                |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
|           | `--fai    |           | Enable early failure checks    |
|           | l-early`{ |           | for the Targeted Power ,       |
|           | .docutils |           | Targeted Stress, and           |
|           | .literal  |           | Diagnostic tests. When         |
|           | .not      |           | enabled, these tests check for |
|           | ranslate} |           | a failure once every 5 seconds |
|           |           |           | (can be modified by the        |
|           |           |           | --check-interval parameter)    |
|           |           |           | while the test is running      |
|           |           |           | instead of a single check      |
|           |           |           | performed after the test is    |
|           |           |           | complete. Disabled by default. |
+-----------+-----------+-----------+--------------------------------+
|           | `--check  | check     | Specify the interval (in       |
|           | -interval | interval  | seconds) at which the early    |
|           | failure`{ |           | failure checks should occur    |
|           | .docutils |           | for the Targeted Power,        |
|           | .literal  |           | Targeted Stress, SM Stress,    |
|           | .not      |           | and Diagnostic tests when      |
|           | ranslate} |           | early failure checks are       |
|           |           |           | enabled. Default is once every |
|           |           |           | 5 seconds. Interval must be    |
|           |           |           | between 1 and 300              |
+-----------+-----------+-----------+--------------------------------+
|           | `--ite    | i         | Specify a number of iterations |
|           | rations`{ | terations | of the diagnostic to run       |
|           | .docutils |           | consecutively. (Must be        |
|           | .literal  |           | greater than 0.)               |
|           | .not      |           |                                |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
|           | `--igno   |           | Ignores the rest of the        |
|           | re_rest`{ |           | labeled arguments following    |
|           | .docutils |           | this flag.                     |
|           | .literal  |           |                                |
|           | .not      |           |                                |
|           | ranslate} |           |                                |
+-----------+-----------+-----------+--------------------------------+
:::

 {.highlight-console .notranslate}

:::

A standard configuration file for H100 would look like below:

 {.highlight}
    version: "@CMAKE_PROJECT_VERSION@"
    spec: dcgm-diag-v1
    skus:
      - name: H100 80GB PCIe
        id: 2331
        targeted_power:
          is_allowed: true
          starting_matrix_dim: 1024.0
          target_power: 350.0
          use_dgemm: false
        targeted_stress:
          is_allowed: true
          use_dgemm: false
          target_stress: 15375
        sm_stress:
          is_allowed: true
          target_stress: 15375.0
          use_dgemm: false
        pcie:
          is_allowed: true
          h2d_d2h_single_pinned:
            min_pci_generation: 3.0
            min_pci_width: 16.0
          h2d_d2h_single_unpinned:
            min_pci_generation: 3.0
            min_pci_width: 16.0
        memory:
          is_allowed: true
          l1cache_size_kb_per_sm: 192.0
        diagnostic:
          is_allowed: true
          matrix_dim: 8192.0
        memory_bandwidth:
          is_allowed: true
          minimum_bandwidth: 1230000
        pulse_test:
          is_allowed: true
:::
:::
:::


 {#custom-configuration-file .section}
#### Custom Configuration File[](dcgm-diagnostics.html#custom-configuration-file "Link to this heading"){.headerlink}

The default configuration file can be overridden using the
`-c`{.docutils .literal .notranslate} option.

 {.highlight}
    $ dcgmi diag -r 2 -c custom-diag-tests.yaml
:::
:::

where desired tests and parameters are included in the
custom-diag-tests.yaml file.
:::

 {.highlight-console .notranslate}

:::
:::

 {.highlight-console .notranslate}

:::
:::
:::
:::

 {.highlight-console .notranslate}

:::

 {.highlight}
    ...
    {
      "category": "Integration",
      "tests": [
        {
          "name": "pcie",
          "results": [
            {
              "entity_group": "GPU",
              "entity_group_id": 1,
              "entity_id": 0,
              "info": [
                "GPU to Host bandwidth:\t\t13.53 GB/s",
                "Host to GPU bandwidth:\t\t12.05 GB/s",
                "bidirectional bandwidth:\t23.69 GB/s",
                "GPU to Host latency:\t\t0.791 us",
                "Host to GPU latency:\t\t1.201 us",
                "bidirectional latency:\t\t1.468 us"
              ],
              "status": "Pass"
            }
          ],
          "test_summary": {
            "status": "Pass"
          }
        }
      ]
    }
    ...
:::
:::
:::

 {#deployment-plugin .section}
### Deployment Plugin[](dcgm-diagnostics.html#deployment-plugin "Link to this heading"){.headerlink}

The deployment plugin's purpose is to verify the compute environment is
ready to run CUDA applications and is able to load the NVML library.


:::

 {#id2 .section}
#### Overview[](dcgm-diagnostics.html#id2 "Link to this heading"){.headerlink}

The Diagnostic plugin is part of the level 3 tests. It performs large
matrix multiplies while copying data to various addresses in the frame
buffer and checking that the data can be written and read correctly.

This test performs large matrix multiplications; by default it will
alternate running these multiplications at all available among 64, 32,
and 16-bit precisions. It will also walk the frame buffer, writing
values to different addresses and making sure that the values are
written and read correctly.
:::


     | This is the precision to use: half,  |
| ecision |         |  {.line | single, or double                    |
|         |         | -block} |                                      |
|         |         | :::     |                                      |
|         |         | {.line} |                                      |
|         |         | \       |                                      |
|         |         | :::     |                                      |
|         |         | :::     |                                      |
|         |         |         |                                      |
|         |         | Half    |                                      |
|         |         | Single  |                                      |
|         |         | Double  |                                      |
+---------+---------+---------+--------------------------------------+
| gf      | Double  | 0.0     | This is the percent of mean below    |
| lops\_t |         |         | which gflops are treated as errors.  |
| oleranc |         |         |                                      |
| e\_pcnt |         |         |                                      |
+---------+---------+---------+--------------------------------------+
:::

 {.highlight-console .notranslate}

:::

Run the diagnostic, stopping if max temperature exceeds 28 degrees:

 {.highlight}
    $ dcgmi diag -r 3 -p diagnostic.temperature_max=28.0
:::
:::

Run the diagnostic, with a smaller starting dimension for matrix
operations:

 {.highlight}
    $ dcgmi diag -r 3 -p diagnostic.matrix_dim=1024.0
:::
:::

Run the diagnostic, reporting an error if a GPU reports gflops not
within 60% of the mean gflops across all GPUs:

 {.highlight}
    $ dcgmi diag -r 3 -p diagnostic.gflops_tolerance_pcnt=0.60
:::
:::

Run the diagnostic, using double precision:

 {.highlight}
    $ dcgmi diag -r 3 -p diagnostic.precision=double
:::
:::
:::


:::

 {#id3 .section}
#### Overview[](dcgm-diagnostics.html#id3 "Link to this heading"){.headerlink}

The PCIe plugin's purpose is to stress the communication from the host
to the GPUs as well as among the GPUs on the system. It checks for p2p
(peer-to-peer) correctness, any errors or replays while writing the
data, and can be used to measure the bandwidth and latency to and from
the GPUs and the host.
:::


:::

 {#id5 .section}
#### Overview[](dcgm-diagnostics.html#id5 "Link to this heading"){.headerlink}

The GPU Memory Plugin is a hardware diagnostic test that validates GPU
memory integrity and functionality. It performs comprehensive memory
testing to detect hardware faults, ECC errors, and memory corruption
issues on NVIDIA GPUs.
:::


 {.highlight-console .notranslate}

:::

With L1 Cache Test Enabled

 {.highlight}
    $ dcgmi diag -r memory -p "memory.is_allowed=True;memory.l1_is_allowed=True"
:::
:::

Controlling Memory Allocation with max\_free\_memory\_mb

 {.highlight}
    $ dcgmi diag -r memory -p "memory.is_allowed=True;memory.max_free_memory_mb=0.1"

    $ dcgmi diag -r memory -p "memory.is_allowed=True;memory.max_free_memory_mb=512"

    $ dcgmi diag -r memory -p "memory.is_allowed=True;memory.max_free_memory_mb=100"
:::
:::
:::


:::

 {#id10 .section}
#### Overview[](dcgm-diagnostics.html#id10 "Link to this heading"){.headerlink}

The Targeted Power plugin is part of the level 3 and higher tests. Its
goal is to drive a GPU towards TDP power usage and sustain that
throughout the test in order to ensure that the GPU can perform under a
power load. This is achieved by using matrix sizes and gemms that are
emprically determined to sustain the required power load on the GPU.
:::


 {.highlight-console .notranslate}

:::

Run the level 3 diagnostic with a 5 minute targeted power test:

 {.highlight}
    $ dcgmi diag -r 3 -p targeted_power.test_duration=300.0
:::
:::

Run the target power test targeting 200 W of power usage:

 {.highlight}
    $ dcgmi diag -r targeted_power -p targeted_power.target_power=200.0
:::
:::

Run the level 4 test, skipping targeted power:

 {.highlight}
    $ dcgmi diag -r 4 -p targeted_power.is_allowed=false
:::
:::

Run the targeted power test, using single precision (32 bit):

 {.highlight}
    $ dcgmi diag -r targeted_power -p targeted_power.use_dgemm=false
:::
:::
:::


:::

 {#id15 .section}
#### Overview[](dcgm-diagnostics.html#id15 "Link to this heading"){.headerlink}

The Targeted Stress plugin is part of the level 3 tests. The plugin
maintains a constant stress level on the GPU by continuously queuing
matrix operations and adjusting the workload to achieve the target
performance.

This test is designed to stress the GPU at a specific performance target
rather than maximum stress, allowing for controlled performance testing
and validation of GPU stability under sustained load.
:::


 {.highlight-console .notranslate}

:::

Run the targeted stress test targeting 200 GFLOPS performance:

 {.highlight}
    $ dcgmi diag -r targeted_stress -p targeted_stress.target_stress=200.0
:::
:::

Run the targeted stress test with single precision operations:

 {.highlight}
    $ dcgmi diag -r targeted_stress -p targeted_stress.use_dgemm=False
:::
:::

Run the targeted stress test with stricter performance requirements (90%
of target):

 {.highlight}
    $ dcgmi diag -r targeted_stress -p targeted_stress.target_perf_min_ratio=0.90
:::
:::

Run the targeted stress test with temperature limit of 85°C:

 {.highlight}
    $ dcgmi diag -r targeted_stress -p targeted_stress.temperature_max=85.0
:::
:::

Run the targeted stress test with custom stream configuration:

 {.highlight}
    $ dcgmi diag -r targeted_stress -p targeted_stress.cuda_streams_per_gpu=4.0 -p targeted_stress.ops_per_stream_queue=50.0
:::
:::

Run the targeted stress test as part of level 3 diagnostics:

 {.highlight}
    $ dcgmi diag -r targeted_stress -p targeted_stress.test_duration=120.0
:::
:::
:::


:::

 {#id20 .section}
#### Overview[](dcgm-diagnostics.html#id20 "Link to this heading"){.headerlink}

Beginning with 2.4.0 DCGM diagnostics support an additional level 4
diagnostics (`-r 4`{.docutils .literal .notranslate}). The first of
these additional diagnostics is memtest. Similar to
[memtest86](https://www.memtest86.com/tech_memtest-algoritm.html){.reference
.external}, the DCGM memtest will exercise GPU memory with various test
patterns. These patterns each given a separate test and can be enabled
and disabled by administrators.
:::

 {.admonition .note}
Note

Test runtimes refer to average seconds per single iteration on a single
A100 40gb GPU.
:::

**Test0 \[Walking 1 bit\]** - This test changes one bit at a time in
memory to see if it goes to a different memory location. It is designed
to test the address wires. Runtime: \~3 seconds.

**Test1 \[Address check\]** - Each Memory location is filled with its
own address followed by a check to see if the value in each memory
location still agrees with the address. Runtime: \< 1 second.

**Test 2 \[Moving inversions, ones&zeros\]** - This test uses the moving
inversions algorithm from memtest86 with patterns of all ones and zeros.
Runtime: \~4 seconds.

**Test 3 \[Moving inversions, 8 bit pat\]** - Same as test 1 but uses a
8 bit wide pattern of "walking" ones and zeros. Runtime: \~4 seconds.

**Test 4 \[Moving inversions, random pattern\]** - Same algorithm as
test 1 but the data pattern is a random number and it's complement. A
total of 60 patterns are used. The random number sequence is different
with each pass so multiple passes can increase effectiveness. Runtime:
\~2 seconds.

**Test 5 \[Block move, 64 moves\]** - This test moves blocks of memory.
Memory is initialized with shifting patterns that are inverted every 8
bytes. Then these blocks of memory are moved around. After the moves are
completed the data patterns are checked. Runtime: \~1 second.

**Test 6 \[Moving inversions, 32 bit pat\]** - This is a variation of
the moving inversions algorithm that shifts the data pattern left one
bit for each successive address. To use all possible data patterns 32
passes are made during the test. Runtime: \~155 seconds.

**Test 7 \[Random number sequence\]** - A 1MB block of memory is
initialized with random patterns. These patterns and their complements
are used in moving inversion tests with rest of memory. Runtime: \~2
seconds.

**Test 8 \[Modulo 20, random pattern\]** - A random pattern is
generated. This pattern is used to set every 20th memory location in
memory. The rest of the memory location is set to the compliment of the
pattern. Repeat this for 20 times and each time the memory location to
set the pattern is shifted right. Runtime: \~10 seconds.

**Test 9 \[Bit fade test, 2 patterns\]** - The bit fade test initializes
all memory with a pattern and then sleeps for 1 minute. Then memory is
examined to see if any memory bits have changed. All ones and all zero
patterns are used. Runtime: \~244 seconds.

**Test10 \[Memory stress\]** - A random pattern is generated and a large
kernel is launched to set all memory to the pattern. A new read and
write kernel is launched immediately after the previous write kernel to
check if there is any errors in memory and set the memory to the
compliment. This process is repeated for 1000 times for one pattern. The
kernel is written as to achieve the maximum bandwidth between the global
memory and GPU. Runtime: \~6 seconds.


:::


 {.highlight-console .notranslate}

:::

Run each test serially for 1 hour then display results:

 {.highlight}
    $ dcgmi diag -r 4 \
       -p memtest.test0=true\;memtest.test1=true\;memtest.test2=true\;memtest.test3=true\;memtest.test4=true\;memtest.test5=true\;memtest.test6=true\;memtest.test7=true\;memtest.test8=true\;memtest.test9=true\;memtest.test10=true\;memtest.test_duration=3600
:::
:::

Run test0 for one minute 10 times, displaying the results each minute:

 {.highlight}
    $ dcgmi diag \
       --iterations 10 \
       -r 4 \
       -p memtest.test0=true\;memtest.test7=false\;memtest.test10=false\;memtest.test_duration=60
:::
:::
:::
:::

 {#id23 .section}
#### Overview[](dcgm-diagnostics.html#id23 "Link to this heading"){.headerlink}

The Pulse Test is part of the new level 4 tests. The pulse test is meant
to fluctuate the power usage to create spikes in current flow on the
board to ensure that the power supply is fully functional and can handle
wide fluctuations in current.
:::

 {.admonition .note}
Note

In some cases with DCGM 2.4 and DCGM 3.0, users may encounter the
following issue with running the Pulse test:

 {.highlight}
    | Pulse Test | Fail - All |
    | Warning | GPU 0There was an internal error during the t |
    | | est: 'The pulse test exited with non-zero sta |
    | | tus 1', GPU 0There was an internal error duri |
    | | ng the test: 'The pulse test reported the err |
    | | or: Exception raised during execution: Faile |
    | | d opening file ubergemm.log for writing: Perm |
    | | ission denied terminate called after throwing |
    | | an instance of 'boost::wrapexcept<boost::pro |
    | | perty_tree::xml_parser::xml_parser_error>' |
    | | what(): result.xml: cannot open file ' |
:::
:::

When running GPU diagnostics, by default, DCGM drops privileges and uses
a (unprivileged) service account to run the diagnostics. If the service
account does not have write access to the directory where diagnostics
are run, then users may encounter this issue. To summarize, the issue
happens when both these conditions are true:

1.  The `nvidia-dcgm`{.docutils .literal .notranslate} service is active
    and the `nv-hostengine`{.docutils .literal .notranslate} process is
    running (and no changes have been made to DCGM's default install
    configurations)

2.  The users attempts to run `dcgmi diag -r 4`{.docutils .literal
    .notranslate}. In this case, `dcgmi diag`{.docutils .literal
    .notranslate} connects to the running `nv-hostengine`{.docutils
    .literal .notranslate} (which was started by default under
    `/root`{.docutils .literal .notranslate}) and thus the Pulse test is
    unable to create any logs.

This issue will be fixed in a future release of DCGM. In the meantime,
users can do either of the following to work-around the issue:

1.  Stop the nvidia-dcgm service before running the pulse\_test

     {.highlight}
        $ sudo systemctl stop nvidia-dcgm
    :::
    :::

    Now run the `pulse_test`{.docutils .literal .notranslate}:

     {.highlight}
        $ dcgmi diag -r pulse_test
    :::
    :::

    Restart the `nvidia-dcgm`{.docutils .literal .notranslate} service
    once the diagnostics are completed:

     {.highlight}
        $ sudo systemctl restart nvidia-dcgm
    :::
    :::

2.  Edit the `systemd`{.docutils .literal .notranslate} unit service
    file to include a `WorkingDirectory`{.docutils .literal
    .notranslate} option, so that the service is started in a location
    writeable by the `nvidia-dcgm`{.docutils .literal .notranslate} user
    (be sure that the directory shown in the example below
    `/tmp/dcgm-temp`{.docutils .literal .notranslate} is created):

     {.highlight}
        [Service]

         ...

         WorkingDirectory=/tmp/dcgm-temp
         ExecStart=/usr/bin/nv-hostengine -n --service-account nvidia-dcgm

         ...
    :::
    :::

    Reload the systemd configuration and start the
    `nvidia-dcgm`{.docutils .literal .notranslate} service:

     {.highlight}
        $ sudo systemctl daemon-reload
    :::
    :::

     {.highlight}
        $ sudo systemctl start nvidia-dcgm
    :::
    :::
:::
:::

 {.highlight-console .notranslate}

:::

Run just the pulse test:

 {.highlight}
    $ dcgmi diag -r pulse_test
:::
:::

Run just the pulse test, but at a lower frequency:

 {.highlight}
    $ dcgmi diag -r pulse_test -p pulse_test.freq0=3000
:::
:::

Run just the pulse test at a lower frequency and for a shorter time:

 {.highlight}
    $ dcgmi diag -r pulse_test -p "pulse_test.freq0=5000;pulse_test.test_duration=180"
:::
:::
:::


:::

 {#id27 .section}
#### Overview[](dcgm-diagnostics.html#id27 "Link to this heading"){.headerlink}

The NVBandwidth plugin is part of the level 3 and higher tests.
NVBandwidth performs bandwidth measurements on NVIDIA GPUs on a single
host.
:::


 {.highlight-console .notranslate}

:::

Run the test, specifying only testcase 1

 {.highlight}
    $ dcgmi diag -r nvbandwidth -p nvbandwidth.testcases=1
:::
:::

Run the test, specifying multiple testcases

 {.highlight}
    $ dcgmi diag -r nvbandwidth -p nvbandwidth.testcases=1,2,3
:::
:::

Run the level 3 test, indicating the nvbandwidth test should be allowed
to run:

 {.highlight}
    $ dcgmi diag -r 3 -p nvbandwidth.is_allowed=true
:::
:::
:::


:::

 {#id32 .section}
#### Supported Products[](dcgm-diagnostics.html#id32 "Link to this heading"){.headerlink}

CPU EUD supports the following Nvidia products:

-   Nvidia Grace CPU
:::

 {.admonition .note}
Note

By default, the CPU EUD will run one or more tests from each of the
other test suites if not specified otherwise.
:::
:::

 {#installing-the-cpu-eud-packages .section}
##### Installing the CPU EUD packages[](dcgm-diagnostics.html#installing-the-cpu-eud-packages "Link to this heading"){.headerlink}

Install the Nvidia CPU EUD package using the appropriate package manager
of the Linux distribution flavor.

> <div>
>
>  {.closeable aria-label="Tabbed content" role="tablist"}
> Debian-based
>
> RPM (RHEL 8, 9)
> :::
>
>  {.highlight-console .notranslate}
>     
>     :::
>
> -   Install the local repo package
>
>      {.highlight}
>         $ sudo dpkg -i cpueud-local-tegra-repo-ubuntu2204-$VERSION-mode1_1.0-1_arm64.deb
>         // $VERSION: The version number of the package you are installing. Replace $VERSION with the actual version number of the package you're using.
>         // Example:
>         // $ sudo dpkg -i cpueud-local-tegra-repo-ubuntu2204-535.169-mode1_1.0-1_arm64.deb
>     :::
>     :::
>
> -   Copy the keyring file to the correct location, the exact copy
>     command will be in the output of the dpkg command.
>
>      {.highlight}
>         $ sudo cp /var/cpueud-local-tegra-repo-ubuntu2204-535.169/cpueud-local-tegra-FFCE45E1-keyring.gpg /usr/share/keyrings/
>     :::
>     :::
>
> -   Update the apt-get and use it install cpueud
>
>      {.highlight}
>         $ sudo apt-get update
>         $ sudo apt-get install cpueud
>     :::
>     :::
> :::
>
>  {.highlight-console .notranslate}
>     
>     :::
>
> -   Install the local repo file, then install the diagnostic. Ensure
>     the diagnostic version matches the major version specified in the
>     local repo RPM file.
>
>      {.highlight}
>         $ sudo yum install libxcrypt-compat
>         $ sudo rpm -i cpueud-local-tegra-repo-rhel9-$VERSION-mode1-1.0-1.aarch64.rpm
>         // $VERSION: The version number of the package you are installing. Replace $VERSION with the actual version number of the package you're using.
>         // Example:
>         // $ sudo rpm -i cpueud-local-tegra-repo-rhel9-535.169-mode1-1.0-1.aarch64.rpm
>
>         $ sudo dnf install cpueud
>     :::
>     :::
> :::
> :::
>
> </div>

The files for the EUD should be installed under
`/usr/share/nvidia/cpu/diagnostic/`{.docutils .literal .notranslate}
:::
:::

 {#id33 .section}
##### Run Levels and Tests[](dcgm-diagnostics.html#id33 "Link to this heading"){.headerlink}

The duration and comprehensiveness of CPU EUD tests run can be varied by
choosing a different diagnostic run level. The following table describes
which tests are run at each level in DCGM diagnostics.

+-------------------+---------+---------+---------+---------+---------+
| Plugin            | Test    | :::     | :::     | :::     | :::     |
|                   | name    |  {.line |  {.line |  {.line |  {.line |
|                   |         | -block} | -block} | -block} | -block} |
|                   |         | :::     | :::     | :::     | :::     |
|                   |         | {.line} | {.line} | {.line} | {.line} |
|                   |         | r1      | r2      | r3      | r4      |
|                   |         | (Short) | (       | (Long)  | (Extra  |
|                   |         | :::     | Medium) | :::     | Long)   |
|                   |         |         | :::     |         | :::     |
|                   |         | :::     |         | :::     |         |
|                   |         | {.line} | :::     | {.line} | :::     |
|                   |         | Seconds | {.line} | \< 30   | {.line} |
|                   |         | :::     | \< 2    | mins    | 1-2     |
|                   |         | :::     | mins    | :::     | hours   |
|                   |         |         | :::     | :::     | :::     |
|                   |         |         | :::     |         | :::     |
+===================+=========+=========+=========+=========+=========+
| CPU EUD           | `Opp    |         |         | Yes     |         |
|                   | ortunis |         |         |         |         |
|                   | tic`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
| CPU EUD           | `RmaF   |         |         |         | Yes     |
|                   | ull`{.d |         |         |         |         |
|                   | ocutils |         |         |         |         |
|                   | .       |         |         |         |         |
|                   | literal |         |         |         |         |
|                   | .notra  |         |         |         |         |
|                   | nslate} |         |         |         |         |
+-------------------+---------+---------+---------+---------+---------+
:::

 {.highlight-shell .notranslate}

:::

Running DCGM with the `-r cpu_eud`{.docutils .literal .notranslate}
parameter instead of a runlevel such as -r 3 runs the default CPU tests,
which are the RmaFull tests.
:::
:::


 {#default .section}
##### Default[](dcgm-diagnostics.html#default "Link to this heading"){.headerlink}

To obtain the results in tabular format, use the following command:

 {.highlight}
    # dcgmi diag -r cpu_eud
:::
:::

 {.highlight-console .notranslate}

:::

-   Failure case

 {.highlight}
    Successfully ran diagnostic for group.
    +---------------------------+------------------------------------------------+
    | Diagnostic                | Result                                         |
    +===========================+================================================+
    |-----  Metadata  ----------+------------------------------------------------|
    | DCGM Version              | 4.0.0                                          |
    | Number of CPUs Detected   | 1                                              |
    | CPU EUD Test Version      | eud.535.161                                    |
    +-----  Hardware  ----------+------------------------------------------------+
    | cpu_eud                   | Fail                                           |
    |                           | CPU0: Fail                                     |
    | Warning: CPU0             | Error : bad command line argument              |
    +---------------------------+------------------------------------------------+
:::
:::
:::
:::

 {.highlight-shell .notranslate}

:::

JSON schema for the element in tests

 {.highlight}
    {
      "$schema": "http://json-schema.org/schema#",
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "results": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "entity_group": {
                "type": "string"
              },
              "entity_group_id": {
                "type": "integer"
              },
              "entity_id": {
                "type": "integer"
              },
              "status": {
                "type": "string"
              },
              "info": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "warnings": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "error_category": {
                      "type": "integer"
                    },
                    "error_id": {
                      "type": "integer"
                    },
                    "error_severity": {
                      "type": "integer"
                    },
                    "warning": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "error_category",
                    "error_id",
                    "error_severity",
                    "warning"
                  ]
                }
              }
            },
            "required": [
              "entity_group",
              "entity_group_id",
              "entity_id",
              "status"
            ]
          }
        },
        "test_summary": {
          "type": "object",
          "properties": {
            "status": {
              "type": "string"
            },
            "info": {
              "type": "array",
              "items": {
                "type": "string"
              }
            },
            "warnings": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "error_category": {
                    "type": "integer"
                  },
                  "error_id": {
                    "type": "integer"
                  },
                  "error_severity": {
                    "type": "integer"
                  },
                  "warning": {
                    "type": "string"
                  }
                },
                "required": [
                  "error_category",
                  "error_id",
                  "error_severity",
                  "warning"
                ]
              }
            }
          },
          "required": [
            "status"
          ]
        }
      },
      "required": [
        "name",
        "results",
        "test_summary"
      ]
    }
:::
:::

 {.highlight-json .notranslate}

:::

-   Failure case

 {.highlight}
    {
      "category": "Hardware",
      "tests": [
        {
          "name": "cpu_eud",
          "results": [
            {
              "entity_group": "CPU",
              "entity_group_id": 7,
              "entity_id": 0,
              "status": "Fail",
              "warnings": [
                {
                  "error_category": 7,
                  "error_id": 95,
                  "error_severity": 2,
                  "warning": "Error : bad command line argument"
                }
              ]
            },
            {
              "entity_group": "CPU",
              "entity_group_id": 7,
              "entity_id": 1,
              "status": "Skip"
            }
          ],
          "test_summary": {
            "status": "Fail"
          }
        }
      ]
    }
:::
:::
:::
:::
:::
:::

 {#id36 .section}
#### Overview[](dcgm-diagnostics.html#id36 "Link to this heading"){.headerlink}

Automating workflows based on DCGM diagnostics can enable sites to
handle GPU errors more efficiently. Additional data for determining the
severity of errors and potential next steps is available using either
the API or by parsing the JSON returned on the CLI. Besides simply
reporting human readable strings of which errors occurred during the
diagnostic, each error also includes a specific ID, Severity, and
Category that can be useful when deciding how to handle the failure.

The latest versions of these enums can be found in
[dcgm\_errors.h](https://github.com/NVIDIA/DCGM/blob/master/dcgmlib/dcgm_errors.h){.reference
.external}.

  Error Category Enum                VALUE
  ---------------------------------- -------
  DCGM\_FR\_EC\_NONE                 0
  DCGM\_FR\_EC\_PERF\_THRESHOLD      1
  DCGM\_FR\_EC\_PERF\_VIOLATION      2
  DCGM\_FR\_EC\_SOFTWARE\_CONFIG     3
  DCGM\_FR\_EC\_SOFTWARE\_LIBRARY    4
  DCGM\_FR\_EC\_SOFTWARE\_XID        5
  DCGM\_FR\_EC\_SOFTWARE\_CUDA       6
  DCGM\_FR\_EC\_SOFTWARE\_EUD        7
  DCGM\_FR\_EC\_SOFTWARE\_OTHER      8
  DCGM\_FR\_EC\_HARDWARE\_THERMAL    9
  DCGM\_FR\_EC\_HARDWARE\_MEMORY     10
  DCGM\_FR\_EC\_HARDWARE\_NVLINK     11
  DCGM\_FR\_EC\_HARDWARE\_NVSWITCH   12
  DCGM\_FR\_EC\_HARDWARE\_PCIE       13
  DCGM\_FR\_EC\_HARDWARE\_POWER      14
  DCGM\_FR\_EC\_HARDWARE\_OTHER      15
  DCGM\_FR\_EC\_INTERNAL\_OTHER      16

  Error Severity Enum    VALUE
  ---------------------- -------
  DCGM\_ERROR\_NONE      0
  DCGM\_ERROR\_MONITOR   1
  DCGM\_ERROR\_ISOLATE   2
  DCGM\_ERROR\_UNKNOWN   3
  DCGM\_ERROR\_TRIAGE    4
  DCGM\_ERROR\_CONFIG    5
  DCGM\_ERROR\_RESET     6

  Error Enum                                     Value   Severity               Category
  ---------------------------------------------- ------- ---------------------- ----------------------------------
  DCGM\_FR\_OK                                   0       DCGM\_ERROR\_UNKNOWN   DCGM\_FR\_EC\_NONE
  DCGM\_FR\_UNKNOWN                              1       DCGM\_ERROR\_UNKNOWN   DCGM\_FR\_EC\_NONE
  DCGM\_FR\_UNRECOGNIZED                         2       DCGM\_ERROR\_UNKNOWN   DCGM\_FR\_EC\_NONE
  DCGM\_FR\_PCI\_REPLAY\_RATE                    3       DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_PCIE
  DCGM\_FR\_VOLATILE\_DBE\_DETECTED              4       DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_VOLATILE\_SBE\_DETECTED              5       DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_PENDING\_PAGE\_RETIREMENTS           6       DCGM\_ERROR\_RESET     DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_RETIRED\_PAGES\_LIMIT                7       DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_RETIRED\_PAGES\_DBE\_LIMIT           8       DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_CORRUPT\_INFOROM                     9       DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_HARDWARE\_OTHER
  DCGM\_FR\_CLOCKS\_EVENT\_THERMAL               10      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_THERMAL
  DCGM\_FR\_POWER\_UNREADABLE                    11      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_POWER
  DCGM\_FR\_CLOCKS\_EVENT\_POWER                 12      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_POWER
  DCGM\_FR\_NVLINK\_ERROR\_THRESHOLD             13      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_NVLINK
  DCGM\_FR\_NVLINK\_DOWN                         14      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_HARDWARE\_NVLINK
  DCGM\_FR\_NVSWITCH\_FATAL\_ERROR               15      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_NVSWITCH
  DCGM\_FR\_NVSWITCH\_NON\_FATAL\_ERROR          16      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_NVSWITCH
  DCGM\_FR\_NVSWITCH\_DOWN                       17      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_NVSWITCH
  DCGM\_FR\_NO\_ACCESS\_TO\_FILE                 18      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_NVML\_API                            19      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_SOFTWARE\_LIBRARY
  DCGM\_FR\_DEVICE\_COUNT\_MISMATCH              20      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_BAD\_PARAMETER                       21      DCGM\_ERROR\_UNKNOWN   DCGM\_FR\_EC\_INTERNAL\_OTHER
  DCGM\_FR\_CANNOT\_OPEN\_LIB                    22      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_LIBRARY
  DCGM\_FR\_DENYLISTED\_DRIVER                   23      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_CONFIG
  DCGM\_FR\_NVML\_LIB\_BAD                       24      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_SOFTWARE\_LIBRARY
  DCGM\_FR\_GRAPHICS\_PROCESSES                  25      DCGM\_ERROR\_RESET     DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_HOSTENGINE\_CONN                     26      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_INTERNAL\_OTHER
  DCGM\_FR\_FIELD\_QUERY                         27      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_INTERNAL\_OTHER
  DCGM\_FR\_BAD\_CUDA\_ENV                       28      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_CUDA
  DCGM\_FR\_PERSISTENCE\_MODE                    29      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_LOW\_BANDWIDTH                       30      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_HARDWARE\_PCIE
  DCGM\_FR\_HIGH\_LATENCY                        31      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_HARDWARE\_PCIE
  DCGM\_FR\_CANNOT\_GET\_FIELD\_TAG              32      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_INTERNAL\_OTHER
  DCGM\_FR\_FIELD\_VIOLATION                     33      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_OTHER
  DCGM\_FR\_FIELD\_THRESHOLD                     34      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_PERF\_VIOLATION
  DCGM\_FR\_FIELD\_VIOLATION\_DBL                35      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_PERF\_VIOLATION
  DCGM\_FR\_FIELD\_THRESHOLD\_DBL                36      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_PERF\_VIOLATION
  DCGM\_FR\_UNSUPPORTED\_FIELD\_TYPE             37      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_INTERNAL\_OTHER
  DCGM\_FR\_FIELD\_THRESHOLD\_TS                 38      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_PERF\_THRESHOLD
  DCGM\_FR\_FIELD\_THRESHOLD\_TS\_DBL            39      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_PERF\_THRESHOLD
  DCGM\_FR\_THERMAL\_VIOLATIONS                  40      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_THERMAL
  DCGM\_FR\_THERMAL\_VIOLATIONS\_TS              41      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_THERMAL
  DCGM\_FR\_TEMP\_VIOLATION                      42      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_THERMAL
  DCGM\_FR\_CLOCKS\_EVENT\_VIOLATION             43      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_OTHER
  DCGM\_FR\_INTERNAL                             44      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_INTERNAL\_OTHER
  DCGM\_FR\_PCIE\_GENERATION                     45      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_HARDWARE\_PCIE
  DCGM\_FR\_PCIE\_WIDTH                          46      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_HARDWARE\_PCIE
  DCGM\_FR\_ABORTED                              47      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_TEST\_DISABLED                       48      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_CONFIG
  DCGM\_FR\_CANNOT\_GET\_STAT                    49      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_INTERNAL\_OTHER
  DCGM\_FR\_STRESS\_LEVEL                        50      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_PERF\_THRESHOLD
  DCGM\_FR\_CUDA\_API                            51      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_SOFTWARE\_CUDA
  DCGM\_FR\_FAULTY\_MEMORY                       52      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_CANNOT\_SET\_WATCHES                 53      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_INTERNAL\_OTHER
  DCGM\_FR\_CUDA\_UNBOUND                        54      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_CUDA
  DCGM\_FR\_ECC\_DISABLED                        55      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_MEMORY\_ALLOC                        56      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_CUDA\_DBE                            57      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_MEMORY\_MISMATCH                     58      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_CUDA\_DEVICE                         59      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_CUDA
  DCGM\_FR\_ECC\_UNSUPPORTED                     60      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_ECC\_PENDING                         61      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_MEMORY\_BANDWIDTH                    62      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_PERF\_THRESHOLD
  DCGM\_FR\_TARGET\_POWER                        63      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_HARDWARE\_POWER
  DCGM\_FR\_API\_FAIL                            64      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_API\_FAIL\_GPU                       65      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_CUDA\_CONTEXT                        66      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_CUDA
  DCGM\_FR\_DCGM\_API                            67      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_INTERNAL\_OTHER
  DCGM\_FR\_CONCURRENT\_GPUS                     68      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_CONFIG
  DCGM\_FR\_TOO\_MANY\_ERRORS                    69      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_NVLINK\_CRC\_ERROR\_THRESHOLD        70      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_NVLINK
  DCGM\_FR\_NVLINK\_ERROR\_CRITICAL              71      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_NVLINK
  DCGM\_FR\_ENFORCED\_POWER\_LIMIT               72      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_HARDWARE\_POWER
  DCGM\_FR\_MEMORY\_ALLOC\_HOST                  73      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_GPU\_OP\_MODE                        74      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_SOFTWARE\_CONFIG
  DCGM\_FR\_NO\_MEMORY\_CLOCKS                   75      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_NO\_GRAPHICS\_CLOCKS                 76      DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_HARDWARE\_OTHER
  DCGM\_FR\_HAD\_TO\_RESTORE\_STATE              77      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_L1TAG\_UNSUPPORTED                   78      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_OTHER
  DCGM\_FR\_L1TAG\_MISCOMPARE                    79      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_ROW\_REMAP\_FAILURE                  80      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_UNCONTAINED\_ERROR                   81      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_SOFTWARE\_XID
  DCGM\_FR\_EMPTY\_GPU\_LIST                     82      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_CONFIG
  DCGM\_FR\_DBE\_PENDING\_PAGE\_RETIREMENTS      83      DCGM\_ERROR\_RESET     DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_UNCORRECTABLE\_ROW\_REMAP            84      DCGM\_ERROR\_RESET     DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_PENDING\_ROW\_REMAP                  85      DCGM\_ERROR\_RESET     DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_BROKEN\_P2P\_MEMORY\_DEVICE          86      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_PCIE
  DCGM\_FR\_BROKEN\_P2P\_WRITER\_DEVICE          87      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_PCIE
  DCGM\_FR\_NVSWITCH\_NVLINK\_DOWN               88      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_NVLINK
  DCGM\_FR\_EUD\_BINARY\_PERMISSIONS             89      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_EUD
  DCGM\_FR\_EUD\_NON\_ROOT\_USER                 90      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_EUD
  DCGM\_FR\_EUD\_SPAWN\_FAILURE                  91      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_EUD
  DCGM\_FR\_EUD\_TIMEOUT                         92      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_EUD
  DCGM\_FR\_EUD\_ZOMBIE                          93      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_EUD
  DCGM\_FR\_EUD\_NON\_ZERO\_EXIT\_CODE           94      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_EUD
  DCGM\_FR\_EUD\_TEST\_FAILED                    95      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_SOFTWARE\_EUD
  DCGM\_FR\_FILE\_CREATE\_PERMISSIONS            96      DCGM\_ERROR\_CONFIG    DCGM\_FR\_EC\_SOFTWARE\_CONFIG
  DCGM\_FR\_PAUSE\_RESUME\_FAILED                97      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_INTERNAL\_OTHER
  DCGM\_FR\_PCIE\_H\_REPLAY\_VIOLATION           98      DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_PCIE
  DCGM\_FR\_GPU\_EXPECTED\_NVLINKS\_UP           99      DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_HARDWARE\_NVLINK
  DCGM\_FR\_NVSWITCH\_EXPECTED\_NVLINKS\_UP      100     DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_HARDWARE\_NVLINK
  DCGM\_FR\_XID\_ERROR                           101     DCGM\_ERROR\_TRIAGE    DCGM\_FR\_EC\_SOFTWARE\_XID
  DCGM\_FR\_SBE\_VIOLATION                       102     DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_DBE\_VIOLATION                       103     DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_PCIE\_REPLAY\_VIOLATION              104     DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_PCIE
  DCGM\_FR\_SBE\_THRESHOLD\_VIOLATION            105     DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_DBE\_THRESHOLD\_VIOLATION            106     DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_MEMORY
  DCGM\_FR\_PCIE\_REPLAY\_THRESHOLD\_VIOLATION   107     DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_HARDWARE\_PCIE
  DCGM\_FR\_CUDA\_FM\_NOT\_INITIALIZED           108     DCGM\_ERROR\_MONITOR   DCGM\_FR\_EC\_SOFTWARE\_CUDA
  DCGM\_FR\_SXID\_ERROR                          109     DCGM\_ERROR\_ISOLATE   DCGM\_FR\_EC\_SOFTWARE\_XID

These relationships are codified in
[dcgm\_errors.c](https://github.com/NVIDIA/DCGM/blob/master/dcgmlib/src/dcgm_errors.c){.reference
.external}.

In general, DCGM has high confidence that errors with the ISOLATE and
RESET severities should be handled immediately. Other severities may
require more site-specific analysis, a re-run of the diagnostic, or a
scanning of DCGM and system logs to determine the best course of action.
Gathering and recording the failure types and rates over time can give
datacenters insight into the best way to automate handling of GPU
diagnostic errors.
:::
:::

 {#id37 .section}
#### Overview[](dcgm-diagnostics.html#id37 "Link to this heading"){.headerlink}

The Memory Bandwidth plugin tests and validates the memory bandwidth
performance of individual NVIDIA GPUs. It measures how fast each GPU can
read from and write to its own memory, which is critical for
applications that require high memory throughput.

The plugin targets the following aspects of GPU memory performance:

-   Memory Bandwidth: Measures the rate at which data can be read from
    and written to GPU memory within a single GPU

-   Memory Subsystem Stability: Validates that the memory subsystem can
    handle sustained high-bandwidth operations without errors

-   Memory Performance Validation: Ensures the GPU meets expected memory
    performance thresholds
:::


 {.highlight-console .notranslate}

:::

Run the test with a custom minimum bandwidth threshold:

 {.highlight}
    $ dcgmi diag -r memory_bandwidth -p "memory_bandwidth.is_allowed=True;memory_bandwidth.minimum_bandwidth=500"
:::
:::

Run the test with a custom log file:

 {.highlight}
    $ dcgmi diag -r memory_bandwidth -p "memory_bandwidth.is_allowed=True;memory_bandwidth.logfile=my_membw_test.json"
:::
:::

Run the test with multiple parameters:

 {.highlight}
    $ dcgmi diag -r memory_bandwidth -p "memory_bandwidth.is_allowed=True;memory_bandwidth.minimum_bandwidth=300;memory_bandwidth.logfile=detailed_membw.json"
:::
:::
:::


:::
:::
:::
:::
:::


------------------------------------------------------------------------


Built with [Sphinx](https://www.sphinx-doc.org/) using a
[theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by
[Read the Docs](https://readthedocs.org).
:::
:::
:::
:::

---

 {.wy-side-scroll}
 
:::
:::


:::

 {.wy-nav-content}
 {role="navigation" aria-label="Page navigation"}
-   [ Select Version]{.icon .icon-home}
    [latest]{.version_switcher_placeholder}
-   »
-   DCGM Multi-Node Diagnostics
-   

------------------------------------------------------------------------
:::

 {itemprop="articleBody"}
 {#overview .section}
Overview[](dcgm-multinode-diagnostics.html#overview "Link to this heading"){.headerlink}
-----------------------------------------------------------------------------------------

The DCGM multi-node diagnostics (mndiag) feature enables users to
validate the performance and stress resilience of GPUs across an entire
cluster by actively stressing the GPUs and their interconnections in a
coordinated and automated fashion.


 {.admonition .note}
Note

Each node is required to be using the same NVIDIA driver version.
:::
:::


:::

 {#command-line-options .section}
### Command-line Options[](dcgm-multinode-diagnostics.html#command-line-options "Link to this heading"){.headerlink}

The command line options are designed to control general execution
parameters. The following table lists the various options supported by
DCGM Diagnostics:

+---+------------------+-----------+-----------------------------------+
| S | Long option      | Parameter | Description                       |
| h |                  |           |                                   |
| o |                  |           |                                   |
| r |                  |           |                                   |
| t |                  |           |                                   |
| o |                  |           |                                   |
| p |                  |           |                                   |
| t |                  |           |                                   |
| i |                  |           |                                   |
| o |                  |           |                                   |
| n |                  |           |                                   |
+===+==================+===========+===================================+
|   | `--hos           | host\_    | Required. List of hosts to run    |
|   | tList`{.docutils | name:port | diagnostics on. Each entry can    |
|   | .literal         | or        | specify a port or Unix socket.    |
|   | .notranslate}    | host\_na  |                                   |
|   |                  | me:socket |                                   |
|   |                  | \_address |                                   |
|   |                  |           |                                   |
|   |                  | Example:  |                                   |
|   |                  | node1:50  |                                   |
|   |                  | 00;node2; |                                   |
|   |                  | node3:uni |                                   |
|   |                  | x:///tmp/ |                                   |
|   |                  | dcgm.sock |                                   |
+---+------------------+-----------+-----------------------------------+
|   | `--hostEngineAd  | IP/FQDN   | Connects to the specified IP or   |
|   | dress`{.docutils |           | FQDN for the head node host       |
|   | .literal         |           | engine. Default: localhost.       |
|   | .notranslate}    |           |                                   |
+---+------------------+-----------+-----------------------------------+
| ` | `                | t         | Multi-node diagnostics test to    |
| - | --run`{.docutils | est\_name | run. Only mnubergemm is currently |
| r | .literal         |           | supported and is the default      |
| ` | .notranslate}    |           | value.                            |
| { |                  |           |                                   |
| . |                  |           |                                   |
| d |                  |           |                                   |
| o |                  |           |                                   |
| c |                  |           |                                   |
| u |                  |           |                                   |
| t |                  |           |                                   |
| i |                  |           |                                   |
| l |                  |           |                                   |
| s |                  |           |                                   |
| . |                  |           |                                   |
| l |                  |           |                                   |
| i |                  |           |                                   |
| t |                  |           |                                   |
| e |                  |           |                                   |
| r |                  |           |                                   |
| a |                  |           |                                   |
| l |                  |           |                                   |
| . |                  |           |                                   |
| n |                  |           |                                   |
| o |                  |           |                                   |
| t |                  |           |                                   |
| r |                  |           |                                   |
| a |                  |           |                                   |
| n |                  |           |                                   |
| s |                  |           |                                   |
| l |                  |           |                                   |
| a |                  |           |                                   |
| t |                  |           |                                   |
| e |                  |           |                                   |
| } |                  |           |                                   |
+---+------------------+-----------+-----------------------------------+
| ` | `--param         | test\     | Test parameters to set for this   |
| - | eters`{.docutils | _name.var | run. Multiple parameters can be   |
| p | .literal         | iable\_na | separated by semicolons.          |
| ` | .notranslate}    | me=variab | Currently only                    |
| { |                  | le\_value | mnubergemm.time\_to\_run is       |
| . |                  |           | supported.                        |
| d |                  | Example:  |                                   |
| o |                  | mnuberge  |                                   |
| c |                  | mm.time\_ |                                   |
| u |                  | to\_run=3 |                                   |
| t |                  | 00;mnuber |                                   |
| i |                  | gemm.flag |                                   |
| l |                  |           |                                   |
| s |                  |           |                                   |
| . |                  |           |                                   |
| l |                  |           |                                   |
| i |                  |           |                                   |
| t |                  |           |                                   |
| e |                  |           |                                   |
| r |                  |           |                                   |
| a |                  |           |                                   |
| l |                  |           |                                   |
| . |                  |           |                                   |
| n |                  |           |                                   |
| o |                  |           |                                   |
| t |                  |           |                                   |
| r |                  |           |                                   |
| a |                  |           |                                   |
| n |                  |           |                                   |
| s |                  |           |                                   |
| l |                  |           |                                   |
| a |                  |           |                                   |
| t |                  |           |                                   |
| e |                  |           |                                   |
| } |                  |           |                                   |
+---+------------------+-----------+-----------------------------------+
| ` | `-               |           | Print the output in JSON format.  |
| - | -json`{.docutils |           |                                   |
| j | .literal         |           |                                   |
| ` | .notranslate}    |           |                                   |
| { |                  |           |                                   |
| . |                  |           |                                   |
| d |                  |           |                                   |
| o |                  |           |                                   |
| c |                  |           |                                   |
| u |                  |           |                                   |
| t |                  |           |                                   |
| i |                  |           |                                   |
| l |                  |           |                                   |
| s |                  |           |                                   |
| . |                  |           |                                   |
| l |                  |           |                                   |
| i |                  |           |                                   |
| t |                  |           |                                   |
| e |                  |           |                                   |
| r |                  |           |                                   |
| a |                  |           |                                   |
| l |                  |           |                                   |
| . |                  |           |                                   |
| n |                  |           |                                   |
| o |                  |           |                                   |
| t |                  |           |                                   |
| r |                  |           |                                   |
| a |                  |           |                                   |
| n |                  |           |                                   |
| s |                  |           |                                   |
| l |                  |           |                                   |
| a |                  |           |                                   |
| t |                  |           |                                   |
| e |                  |           |                                   |
| } |                  |           |                                   |
+---+------------------+-----------+-----------------------------------+
|   | `-               |           | Displays usage information and    |
|   | -help`{.docutils |           | exits.                            |
|   | .literal         |           |                                   |
|   | .notranslate}    |           |                                   |
+---+------------------+-----------+-----------------------------------+
:::

 {#basic-multi-node-diagnostics .section}
#### Basic Multi-Node Diagnostics[](dcgm-multinode-diagnostics.html#basic-multi-node-diagnostics "Link to this heading"){.headerlink}

Dcgmi should be launched on any one of the nodes in the cluster (the
head node) with a list of hostnames/IP addresses of all the nodes that
need to be targeted by the test, including the head node. The head node
will orchestrate the test run on all the nodes in the list.

 {.highlight}
    dcgmi mndiag --hostList "node1;node2;node3"
:::
:::
:::

 {.highlight-console .notranslate}

:::
:::

 {.highlight-console .notranslate}

:::
:::

 {.highlight-console .notranslate}

:::
:::

 {.highlight-console .notranslate}

:::
:::
:::

 {#test-setup .section}
#### Test Setup[](dcgm-multinode-diagnostics.html#test-setup "Link to this heading"){.headerlink}

-   An installation of OpenMPI (version 4.1.1 or any later ABI
    compatible version) on each of participating machines.


-   The value of the DCGM\_MNDIAG\_MPIRUN\_PATH environment variable for
    the nv-hostengine process should be set to the path of the mpirun
    command.

-   The value of the LD\_LIBRARY\_PATH environment variable for the
    nv-hostengine process should be set to the directory containing the
    OpenMPI libraries.


-   An account is available on all participating machines with the same
    name as the user invoking `dcgmi`{.docutils .literal .notranslate}
    to launch the the multi-node diagnostics.

-   Either

    1.  login shells associated for the user launching the multi-node
        diagnostic are configured to use OpenMPI, or

    2.  the installation root directory of OpenMPI is the same on each
        participating machine and OpenMPI has been configured to
        propagate the installation root by default.

-   Non-interactive ssh needs to be configured between all the nodes.
    Dcgmi and OpenMPI will expect SSH keys to be configured such that
    the following works:

     {.highlight}
        ssh <remote node>
    :::
    :::

 {.highlight-console .notranslate}
> 
> :::
>
> </div>

This is because the SSH sessions required by the diagnostic are spawned
by the nv-hostengine process (managed by the nvidia-dcgm service), not
as a child of the user's shell or dcgmi process. As a result, the
agent's environment is not inherited by these SSH sessions, and the
agent cannot provide the key. The SSH private key must be available
unencrypted on disk for passwordless access to work in this context.

For more information, see the [OpenMPI documentation on non-interactive
SSH](https://docs.open-mpi.org/en/v5.0.x/launching-apps/ssh.html#non-interactive-ssh-logins){.reference
.external}.
:::

-   The nv-hostengine daemon should be started on all the nodes.

-   Each node should have the same NVIDIA driver version.
:::


:::

 {.highlight-console .notranslate}

:::
:::


:::
:::
:::
:::


------------------------------------------------------------------------


Built with [Sphinx](https://www.sphinx-doc.org/) using a
[theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by
[Read the Docs](https://readthedocs.org).
:::
:::
:::
:::

---

 {.wy-side-scroll}
 
:::
:::


:::

 {.wy-nav-content}
 {role="navigation" aria-label="Page navigation"}
-   [ Select Version]{.icon .icon-home}
    [latest]{.version_switcher_placeholder}
-   »
-   Error Injection
-   

------------------------------------------------------------------------
:::

 {itemprop="articleBody"}
 {#overview .section}
Overview[](dcgm-error-injection.html#overview "Link to this heading"){.headerlink}
-----------------------------------------------------------------------------------

DCGM includes an error injection framework allows users to simulate the
error handling behavior of the DCGM APIs when GPU errors are
encountered.


 {#thermal-violation .section}
#### Thermal Violation[](dcgm-error-injection.html#thermal-violation "Link to this heading"){.headerlink}

This example demonstrates an excursion above the specified GPU thermal
threshold.

In this example, use the DCGM policy to watch for violations from the
target temperature threshold of 50C.

In one "listening" terminal:

 {.highlight}
    $ dcgmi policy --set 0,0 -T 50
    Policy successfully set.
:::
:::

Register DCGM to watch for violations

 {.highlight}
    $ dcgmi policy --reg
    Listening for violations.
:::
:::

In another "application" terminal, launch a workload. The provided DCGM
CUDA load generator can be used for this purpose. For this example,
launch an FP16 GEMM on the GPU:

 {.highlight}
    $ dcgmproftester11 --no-dcgm-validation -t 1004 -d 30
:::
:::

Back in the "listening" console, DCGM reports the thermal violations as
the GPU temperature increases due to compute work:

 {.highlight}
    Timestamp: Wed Sep 21 22:23:18 2022
    The maximum thermal limit has violated policy manager values.
    Temperature: 56
    Timestamp: Wed Sep 21 22:23:28 2022
    The maximum thermal limit has violated policy manager values.
    Temperature: 60
:::
:::
:::

 {.highlight-console .notranslate}

:::

In another terminal, inject a contrived value of 99999:

 {.highlight}
    $ dcgmi test --inject --gpuid 0 -f 202 -v 99999
    Successfully injected field info.
:::
:::

And in the "listening" terminal, DCGM reports these PCIe replay
violations

 {.highlight}
    Listening for violations.
    Timestamp: Thu Sep 22 01:30:34 2022
    A PCIe replay event has violated policy manager values.
    PCIe replay count: 99999
:::
:::

The same violation can also be observed when using Health watches with
DCGM:

 {.highlight}
    $ dcgmi health -c
    +---------------------------+----------------------------------------------------------+
    | Health Monitor Report                                                                |
    +===========================+==========================================================+
    | Overall Health            | Warning                                                  |
    | GPU                       |                                                          |
    | -> 0                      | Warning                                                  |
    |    -> Errors              |                                                          |
    |       -> PCIe system      | Warning                                                  |
    |                           | Detected more than 8 PCIe replays per minute for GPU 0   |
    |                           | : 99999 Reconnect PCIe card. Run system side PCIE        |
    |                           | diagnostic utilities to verify hops off the GPU board    |
    |                           | If issue is on the board, run the field diagnostic.      |
    +---------------------------+----------------------------------------------------------+
:::
:::
:::

 {.highlight-console .notranslate}

:::

In another terminal, inject a value of 4:

 {.highlight}
    $ dcgmi test --inject --gpuid 0 -f 319 -v 4
    Successfully injected field info.
:::
:::

And in the "listening" terminal, DCGM reports the ECC errors

 {.highlight}
    Timestamp: Thu Sep 22 04:44:12 2022
    A double-bit ECC error has violated policy manager values.
    DBE error count: 2
:::
:::
:::
:::


:::
:::
:::
:::


------------------------------------------------------------------------


Built with [Sphinx](https://www.sphinx-doc.org/) using a
[theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by
[Read the Docs](https://readthedocs.org).
:::
:::
:::
:::

---

 {.wy-side-scroll}
 
:::
:::


:::

 {.wy-nav-content}
 {role="navigation" aria-label="Page navigation"}
-   [ Select Version]{.icon .icon-home}
    [latest]{.version_switcher_placeholder}
-   »
-   Debugging and Troubleshooting
-   

------------------------------------------------------------------------
:::

 {itemprop="articleBody"}
 {#general-problem-reporting .section}
General Problem Reporting[](debugging-and-troubleshooting.html#general-problem-reporting "Link to this heading"){.headerlink}
------------------------------------------------------------------------------------------------------------------------------

When reporting a problem, please always include:

-   `nvidia-bug-report.log.gz`{.docutils .literal .notranslate} -
    produced by `nvidia-bug-report.sh`{.docutils .literal .notranslate}

-   Full output of `dcgmi -v`{.docutils .literal .notranslate}

-   Relevant and/or requested logs, below
:::

 {#enable-logging-using-standalone-hostengine .section}
### Enable Logging Using Standalone Hostengine[](debugging-and-troubleshooting.html#enable-logging-using-standalone-hostengine "Link to this heading"){.headerlink}

When launching `nv-hostengine`{.docutils .literal .notranslate}:

-   Add the `-f /path/to/log`{.docutils .literal .notranslate} parameter
    to specify where to write the log

-   Add the `--log-level DEBUG`{.docutils .literal .notranslate}
    parameter to specify DEBUG logging

This example will collect debug logs from the standalone hostengine for
the duration of its lifetime. The log file will be written to
`/tmp/nv-hostengine.log`{.docutils .literal .notranslate}. Example:

 {.highlight}
    % sudo nv-hostengine -f /tmp/nv-hostengine.log --log-level DEBUG
:::
:::
:::

 {.highlight-console .notranslate}

:::
:::

 {.highlight-console .notranslate}

:::
:::

 {.admonition .note}
Note

If using the standalone hostengine, a separate
`__NVML_DBG_FILE`{.docutils .literal .notranslate} should be specified
for the hostengine and the desired command. See the example that
follows.
:::

This example will collect NVML logs and debug logs from a standalone
hostengine, as well as NVML and debug logs from the long diagnostic. The
NVML logs for the hostengine will be written to
`/tmp/hostengine.nvml.log`{.docutils .literal .notranslate}, and the
NVML logs for the diagnostic will be written to
`/tmp/nvvs.nvml.log`{.docutils .literal .notranslate}. Example:

 {.highlight}
    % sudo -i
    (prompts for password)
    # export __NVML_DBG_FILE=/tmp/hostengine.nvml.log
    # export __NVML_DBG_LVL=DEBUG
    # env | grep __NVML_DBG
    (output)
    __NVML_DBG_FILE=/tmp/hostengine.nvml.log
    __NVML_DBG_LVL=DEBUG
    # nv-hostengine -f /tmp/nv-hostengine.log --log-level DEBUG
    # export __NVML_DBG_FILE=/tmp/nvvs.nvml.log
    # env | grep __NVML_DBG
    (output)
    __NVML_DBG_FILE=/tmp/nvvs.nvml.log
    __NVML_DBG_LVL=DEBUG
    # dcgmi diag -r long --debugLogFile /tmp/nvvs.log -d DEBUG
    ...
:::
:::
:::
:::

 {#host-engine-environment-variables-affecting-hang-detection .section}
[]{#hostengine-hangdetect-environment}

### Host Engine Environment Variables Affecting Hang Detection[](debugging-and-troubleshooting.html#host-engine-environment-variables-affecting-hang-detection "Link to this heading"){.headerlink}

The `nv-hostengine`{.docutils .literal .notranslate} program accepts
environment variables that control hang detection. See
[environ(7)](https://www.man7.org/linux/man-pages/man7/environ.7.html){.reference
.external} to learn about environment variables.

The following environment variables affect hang detection in the
hostengine and in hostengine modules:

+-----------------------------------+-----------------------------------+
| `D                                | When set, disables the hang       |
| CGM_HANGDETECT_DISABLE`{.docutils | detection system in the           |
| .literal .notranslate}            | hostengine and in hostengine      |
|                                   | modules. Hang detection is        |
|                                   | enabled by default and monitors   |
|                                   | select capabilities for hangs.    |
|                                   | This does not change the response |
|                                   | to hangs in the diagnostic. See   |
|                                   | [[Environment]{.std               |
|                                   | .std-re                           |
|                                   | f}](dcgm-diagnostics.html#dcgm-di |
|                                   | agnostics-environment){.reference |
|                                   | .internal} in [[DCGM              |
|                                   | Diagnostics]{.std                 |
|                                   | .std-ref}](dcgm-diagnostics.      |
|                                   | html#dcgm-diagnostics){.reference |
|                                   | .internal} for more information.  |
+-----------------------------------+-----------------------------------+
| `DCGM                             | Sets the time period (in seconds) |
| _HANGDETECT_EXPIRY_SEC`{.docutils | after which unresponsive          |
| .literal .notranslate}            | threads/processes may be          |
|                                   | considered hung. Values must be   |
|                                   | at least 120 seconds and also be  |
|                                   | divisible by 60 (e.g., 120, 180,  |
|                                   | 300, 360).                        |
+-----------------------------------+-----------------------------------+
| `DCG                              | When set, attempts to terminate   |
| M_HANGDETECT_TERMINATE`{.docutils | the hostengine process if a hang  |
| .literal .notranslate}            | is detected. By default, the      |
|                                   | hostengine will attempt to log a  |
|                                   | message and continue, allowing    |
|                                   | the reported hang to continue.    |
|                                   | This does not change the response |
|                                   | to hangs in DCGM modules, which   |
|                                   | are logged.                       |
+-----------------------------------+-----------------------------------+
:::
:::
:::
:::
:::


------------------------------------------------------------------------


Built with [Sphinx](https://www.sphinx-doc.org/) using a
[theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by
[Read the Docs](https://readthedocs.org).
:::
:::
:::
:::
