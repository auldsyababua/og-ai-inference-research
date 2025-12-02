# Excel Formula Reference for Data Logistics Calculator

**Version:** 1.0  
**Last Updated:** 2025-12-02

---

## Quick Setup in Excel

1. Open `DataLogistics-v1.csv` in Excel
2. Add formulas to row 2 (or your first data row)
3. Copy formulas down for additional scenarios

**Column Reference (assuming row 2):**
- Column B: `Workload_Inbound_TB_per_month`
- Column C: `Workload_Outbound_TB_per_month`
- Column D: `Starlink_Terminals`
- Column E: `Starlink_Cost_per_terminal_per_month`
- Column F: `Starlink_Effective_Bandwidth_Mbps`
- Column G: `Starlink_Overhead_Factor`
- Column H: `Starlink_Usable_TB_per_month` (calculated)
- Column I: `Starlink_Total_Cost_per_month` (calculated)
- Column J: `Starlink_Cost_per_TB` (calculated)
- Column K: `Sneakernet_Distance_miles`
- Column L: `Sneakernet_Cost_per_mile`
- Column M: `Sneakernet_Trips_per_month`
- Column N: `Sneakernet_TB_per_trip`
- Column O: `Sneakernet_Total_Cost_per_month` (calculated)
- Column P: `Sneakernet_Cost_per_TB` (calculated)
- Column Q: `Fiber_Distance_miles`
- Column R: `Fiber_Cost_per_mile`
- Column S: `Fiber_Amortization_years`
- Column T: `Fiber_OpEx_per_month`
- Column U: `Fiber_Total_CapEx` (calculated)
- Column V: `Fiber_Monthly_CapEx_Amortized` (calculated)
- Column W: `Fiber_Total_Cost_per_month` (calculated)
- Column X: `Fiber_Cost_per_TB` (calculated)
- Column Y: `Recommended_Mode` (calculated)
- Column Z: `Cost_Savings_vs_Next_Best` (calculated)

---

## Formula List (Row 2)

### Column D: Total_TB_per_month
```
=B2+C2
```

### Column I: Starlink_Usable_TB_per_month
```
=E2*G2*H2*2.629746/8
```

**Note:** `2.629746` = seconds per month (30.44 days × 24 hours × 3600 seconds) / 10^6 (Mbps to TB conversion)

### Column J: Starlink_Total_Cost_per_month
```
=E2*F2
```

### Column K: Starlink_Cost_per_TB
```
=IF(I2>=D2, J2/D2, 999999)
```

**Note:** Returns 999999 if capacity is insufficient (excludes from comparison)

### Column O: Sneakernet_Total_Cost_per_month
```
=M2*2*K2*L2
```

**Note:** `2*` accounts for round trip

### Column P: Sneakernet_Cost_per_TB
```
=IF(M2*N2>=C2, O2/C2, 999999)
```

**Note:** Checks if total capacity (trips × TB per trip) meets demand

### Column V: Fiber_Total_CapEx
```
=R2*S2
```

### Column W: Fiber_Monthly_CapEx_Amortized
```
=V2/(T2*12)
```

### Column X: Fiber_Total_Cost_per_month
```
=W2+U2
```

### Column Y: Fiber_Cost_per_TB
```
=X2/D2
```

### Column Z: Recommended_Mode
```
=IF(MIN(K2,Q2,Y2)=K2,"Starlink",IF(MIN(K2,Q2,Y2)=Q2,"Sneakernet","Fiber"))
```

**Note:** Assumes all modes can meet capacity. If a mode returns 999999, it's excluded.

### Column AA: Cost_Savings_vs_Next_Best
```
=LARGE({IF(K2=999999,0,K2),IF(Q2=999999,0,Q2),IF(Y2=999999,0,Y2)},2)-MIN(IF(K2=999999,999999,K2),IF(Q2=999999,999999,Q2),IF(Y2=999999,999999,Y2))
```

**Simplified version** (if all modes can meet capacity):
```
=LARGE({K2,Q2,Y2},2)-MIN(K2,Q2,Y2)
```

---

## Example: Complete Row 2 Formulas

Copy these into Excel row 2:

| Column | Formula |
|--------|---------|
| D | `=B2+C2` (inbound + outbound) |
| I | `=E2*G2*H2*2.629746/8` |
| J | `=E2*F2` |
| K | `=IF(I2>=D2, J2/D2, 999999)` |
| P | `=N2*2*L2*M2` |
| Q | `=IF(N2*O2>=D2, P2/D2, 999999)` |
| V | `=R2*S2` |
| W | `=V2/(T2*12)` |
| X | `=W2+U2` |
| Y | `=X2/D2` |
| Z | `=IF(MIN(K2,Q2,Y2)=K2,"Starlink",IF(MIN(K2,Q2,Y2)=Q2,"Sneakernet","Fiber"))` |
| AA | `=LARGE({K2,Q2,Y2},2)-MIN(K2,Q2,Y2)` |

---

## Troubleshooting Formulas

### Issue: #DIV/0! Error
- **Cause:** Total_TB_per_month is zero
- **Solution:** Ensure inbound + outbound > 0

### Issue: Recommended mode shows wrong option
- **Cause:** One mode may have 999999 (insufficient capacity)
- **Solution:** Check that Starlink_Usable_TB_per_month >= Total_TB_per_month and Sneakernet capacity >= Total_TB_per_month

### Issue: Cost savings is negative
- **Cause:** Formula error or all modes have 999999
- **Solution:** Verify all three modes can meet capacity requirements

---

## Advanced: Capacity Validation

Add helper columns to validate capacity:

**Column AB: Starlink_Capacity_Check**
```
=IF(I2>=D2,"OK","INSUFFICIENT")
```

**Column AC: Sneakernet_Capacity_Check**
```
=IF(N2*O2>=D2,"OK","INSUFFICIENT")
```

**Column AC: Fiber_Capacity_Check**
```
="OK"
```
(Fiber assumed unlimited capacity)

---

## References

- `formulas.md` - Detailed formula documentation with derivations
- `README.md` - User guide and examples

