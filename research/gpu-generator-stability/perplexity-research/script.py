import math

# Generator specifications from search results
generators = {
    "CG170-16": {
        "power_kw": 1560,  # ekW @ 1.0pf from [9][13]
        "rpm": 1500,  # 50 Hz from [13]
        "poles": 4,  # 1500 rpm for 50 Hz = 4 poles (120*50/1500 = 4)
        "efficiency": 0.433,  # from [9]
        "inertia_kg_m2": 44.6,  # from prompt table (>44.6)
    },
    "CG260-16": {
        "power_kw": 4300,  # ekW @ 1.0pf from [17][20]
        "rpm": 1000,  # 50 Hz from [17]
        "poles": 6,  # 1000 rpm for 50 Hz = 6 poles (120*50/1000 = 6)
        "efficiency": 0.441,  # from [17]
        "inertia_kg_m2": 710,  # from prompt table
    },
    "G3516C": {
        "power_kw": 1555,  # ekW from [18][75]
        "rpm": 1500,  # 50 Hz from [15]
        "poles": 4,  # 1500 rpm for 50 Hz = 4 poles
        "efficiency": 0.377,  # from [18][75]
        "inertia_kg_m2": 150,  # estimated from prompt table
    }
}

# Calculate inertia constant H for each generator
def calculate_H(power_kw, rpm, poles, inertia_kg_m2):
    """
    Calculate inertia constant H (seconds) using formula:
    H = J × ω² / (2 × S_base)
    
    Where:
    - J = mass moment of inertia (kg·m²)
    - ω = angular velocity (rad/s) = 2π × f / p
    - f = frequency (Hz) = rpm × poles / 120
    - p = pole pairs = poles / 2
    - S_base = generator MVA rating (assuming pf = 1.0, so MVA = MW)
    """
    # Calculate frequency
    f = rpm * poles / 120  # Hz
    
    # Calculate pole pairs
    p = poles / 2
    
    # Calculate angular velocity (rad/s)
    omega = 2 * math.pi * f / p
    
    # Calculate S_base in MVA (assuming pf = 1.0)
    S_base = power_kw / 1000  # MW = MVA at pf=1.0
    
    # Calculate H in seconds
    H = (inertia_kg_m2 * omega**2) / (2 * S_base * 1_000_000)  # Convert to MWs/MVA
    
    return H, f, omega, S_base

# Calculate for each generator
results = {}
for model, specs in generators.items():
    H, f, omega, S_base = calculate_H(
        specs["power_kw"],
        specs["rpm"],
        specs["poles"],
        specs["inertia_kg_m2"]
    )
    
    results[model] = {
        "H_seconds": H,
        "frequency_hz": f,
        "omega_rad_s": omega,
        "S_base_mva": S_base,
        "inertia_kg_m2": specs["inertia_kg_m2"],
        "power_kw": specs["power_kw"],
        "efficiency": specs["efficiency"]
    }

# Display results
for model, data in results.items():
    print(f"\n{model}:")
    print(f"  Power: {data['power_kw']} kW")
    print(f"  Frequency: {data['frequency_hz']} Hz")
    print(f"  Angular Velocity: {data['omega_rad_s']:.2f} rad/s")
    print(f"  Inertia (kg·m²): {data['inertia_kg_m2']}")
    print(f"  H (seconds): {data['H_seconds']:.3f}")
