#!/usr/bin/env python3
"""
Test script for BESS sizing logic after removing islanded parameter.
Tests different combinations of load_sequencing and risk_tolerance.
"""

import sys
sys.path.insert(0, '/srv/projects/og-ai-inference-research')

from streamlit_app import recommend_bess

def test_scenario(scenario_name, n_gpu, p_gpu, p_gen, gen_load_acceptance_pct,
                  gen_type, black_start, load_sequencing, risk_tolerance,
                  expected_type=None, expected_power_range=None):
    """Test a specific scenario and print results with optional assertions."""
    print(f"\n{'='*80}")
    print(f"SCENARIO: {scenario_name}")
    print(f"{'='*80}")
    print(f"Configuration:")
    print(f"  - GPUs: {n_gpu} x {p_gpu}kW = {n_gpu * p_gpu}kW total")
    print(f"  - Generator: {gen_type} ({p_gen}kW, {gen_load_acceptance_pct}% load acceptance)")
    print(f"  - Black Start: {black_start}")
    print(f"  - Load Sequencing: {load_sequencing}")
    print(f"  - Risk Tolerance: {risk_tolerance}")

    results = recommend_bess(
        n_gpu, p_gpu, p_gen, gen_load_acceptance_pct, gen_type,
        black_start, load_sequencing, risk_tolerance
    )

    print(f"\nResults:")
    print(f"  - BESS Type: {results['bess_type']}")
    print(f"  - BESS Power: {results['bess_power_kw']:.1f} kW")
    print(f"  - BESS Energy: {results['bess_energy_kwh']:.1f} kWh")
    print(f"  - BESS Cost: ${results['bess_cost_usd']:,.0f}")
    print(f"  - Rationale: {results['rationale']}")

    # Perform assertions if expected values provided
    if expected_type is not None:
        assert results['bess_type'] == expected_type, \
            f"Expected BESS type '{expected_type}', got '{results['bess_type']}'"
        print(f"  ✓ BESS type assertion passed: {expected_type}")

    if expected_power_range is not None:
        min_power, max_power = expected_power_range
        assert min_power <= results['bess_power_kw'] <= max_power, \
            f"Expected BESS power in range [{min_power}, {max_power}]kW, got {results['bess_power_kw']:.1f}kW"
        print(f"  ✓ BESS power assertion passed: {results['bess_power_kw']:.1f}kW in range [{min_power}, {max_power}]kW")

    return results

def main():
    """Run all test scenarios."""
    print("\n" + "="*80)
    print("BESS SIZING LOGIC TEST SUITE (Islanded Operation Assumed)")
    print("="*80)

    # Test 1: Small cluster (≤4 GPUs) + Fast Response + High Risk → No BESS
    test_scenario(
        "Test 1: Small Cluster + Fast Generator + High Risk → No BESS",
        n_gpu=4,
        p_gpu=400,  # 1600 kW total
        p_gen=1000,
        gen_load_acceptance_pct=50,
        gen_type='1000_kW_Fast_Response_NG',
        black_start=False,
        load_sequencing=False,
        risk_tolerance='High',
        expected_type='No_BESS',
        expected_power_range=(0, 0)
    )

    # Test 2: Aggressive load sequencing + High risk → 50-100kW Buffer BESS
    test_scenario(
        "Test 2: Aggressive Load Sequencing + High Risk → 50-100kW Buffer BESS",
        n_gpu=8,
        p_gpu=400,  # 3200 kW total
        p_gen=1000,
        gen_load_acceptance_pct=50,
        gen_type='1000_kW_Lean_Burn_NG',
        black_start=False,
        load_sequencing=True,
        risk_tolerance='High',
        expected_type='Buffer',
        expected_power_range=(50, 100)
    )

    # Test 3: Moderate load sequencing + Medium risk → 150-200kW Grid-Forming BESS
    test_scenario(
        "Test 3: Moderate Load Sequencing + Medium Risk → 150-200kW Grid-Forming BESS",
        n_gpu=8,
        p_gpu=400,  # 3200 kW total
        p_gen=1000,
        gen_load_acceptance_pct=50,
        gen_type='1000_kW_Lean_Burn_NG',
        black_start=False,
        load_sequencing=True,
        risk_tolerance='Medium',
        expected_type='Grid_Forming',
        expected_power_range=(150, 200)
    )

    # Test 4: No load sequencing + Generator can handle step → 400-600kW Grid-Forming BESS
    test_scenario(
        "Test 4: No Load Sequencing + Gen Can Handle → 400-600kW Grid-Forming BESS",
        n_gpu=4,
        p_gpu=400,  # 1600 kW total
        p_gen=2000,
        gen_load_acceptance_pct=80,  # 1600 kW acceptance
        gen_type='2000_kW_Rich_Burn_NG',
        black_start=False,
        load_sequencing=False,
        risk_tolerance='Medium',
        expected_type='Grid_Forming',
        expected_power_range=(400, 600)
    )

    # Test 5: Large cluster + No load sequencing → 400-600kW Grid-Forming BESS
    test_scenario(
        "Test 5: Large Cluster + No Load Sequencing → 400-600kW Grid-Forming BESS",
        n_gpu=10,
        p_gpu=400,  # 4000 kW total
        p_gen=1000,
        gen_load_acceptance_pct=50,  # 500 kW acceptance
        gen_type='1000_kW_Lean_Burn_NG',
        black_start=False,
        load_sequencing=False,
        risk_tolerance='Low',
        expected_type='Grid_Forming',
        expected_power_range=(400, 600)
    )

    # Test 6: Load sequencing reduces step to <200kW → 150-200kW Grid-Forming BESS
    test_scenario(
        "Test 6: Load Sequencing Reduces Step <200kW → 150-200kW Grid-Forming BESS",
        n_gpu=6,
        p_gpu=400,  # 2400 kW total
        p_gen=2000,
        gen_load_acceptance_pct=60,  # 1200 kW acceptance, step = 1200 kW
        gen_type='2000_kW_Rich_Burn_NG',
        black_start=False,
        load_sequencing=True,
        risk_tolerance='Medium',
        expected_type='Grid_Forming',
        expected_power_range=(150, 200)
    )

    # Test 7: CG260 generator (first step limited) → Grid-Forming BESS
    test_scenario(
        "Test 7: CG260 Generator (First Step Limited) → Grid-Forming BESS",
        n_gpu=8,
        p_gpu=400,  # 3200 kW total
        p_gen=1000,
        gen_load_acceptance_pct=25,  # 250 kW first step
        gen_type='1000_kW_CG260',
        black_start=False,
        load_sequencing=False,
        risk_tolerance='Medium',
        expected_type='Grid_Forming',
        expected_power_range=(400, 600)
    )

    # Test 8: Edge case - Generator barely can't handle step
    test_scenario(
        "Test 8: Generator Barely Can't Handle Step → Grid-Forming BESS",
        n_gpu=5,
        p_gpu=400,  # 2000 kW total
        p_gen=1000,
        gen_load_acceptance_pct=49,  # 490 kW acceptance (10 kW short)
        gen_type='1000_kW_Lean_Burn_NG',
        black_start=False,
        load_sequencing=False,
        risk_tolerance='Medium',
        expected_type='Grid_Forming',
        expected_power_range=(400, 600)
    )

    # Test 9: Edge case - Very large cluster + Aggressive load sequencing → 100kW Buffer BESS (capped)
    test_scenario(
        "Test 9: Very Large Cluster (50 GPUs) + Aggressive Sequencing → 100kW Buffer BESS (capped)",
        n_gpu=50,
        p_gpu=400,  # 20,000 kW total (huge cluster)
        p_gen=2000,
        gen_load_acceptance_pct=50,
        gen_type='2000_kW_Rich_Burn_NG',
        black_start=False,
        load_sequencing=True,
        risk_tolerance='High',
        expected_type='Buffer',
        expected_power_range=(100, 100)  # Should cap at exactly 100kW
    )

    print(f"\n{'='*80}")
    print("ALL TESTS COMPLETED")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    main()
