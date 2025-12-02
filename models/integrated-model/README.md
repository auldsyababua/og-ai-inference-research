# Integrated Model: GPU-ASIC-Generator Operational Model

This directory contains the **core operational model** that describes how a 1 MW natural gas generator can safely power 500 kW of Bitcoin miners (ASICs) and 500 kW of H100 GPUs through **shaped ramps** and **optional miner shedding**.

## Key Document

- **`GPU-ASIC-GENERATOR-OPERATIONAL-MODEL.md`** - Complete operational model describing:
  - System setup and state variables
  - Two paths for bringing GPUs online (with/without miner shedding)
  - Phase transition management (preload → full-power)
  - BESS sizing implications
  - Implementation considerations

## Key Insight

**Small steps are effectively free.** By bringing GPUs online in small batches (1-10 GPUs at a time) and optionally shedding equivalent ASIC load, the generator only ever sees small, controlled changes in net kW. This makes BESS **optional rather than required** for GPU ramp control.

## Relationship to Other Models

This operational model **informs** the sizing in other model directories:

- **`../bess-sizing/`** - BESS sizing can be 3-5× smaller (100-200 kW vs 400-600 kW) with proper operational controls
- **`../bitcoin-miner-integration/`** - Miner shedding strategies and coordination
- **`../multistep-ramp-simulator/`** - Generator response to controlled load steps
- **`../generator-risk-calculator/`** - Risk assessment with shaped ramps

## One-Sentence Summary

> We run a 1 MW gas generator feeding up to 500 kW of ASIC miners and 500 kW of H100 GPUs; we bring GPUs online in small batches and, when needed, shed equivalent ASIC load so the generator only ever sees small, controlled changes in net kW — making a BESS optional rather than fundamental to safe operation.

