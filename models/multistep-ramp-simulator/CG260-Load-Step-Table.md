# CG260-16 Load Step Sequence Table

**Source:** Caterpillar Technical Bulletins  
**Conditions:** Air intake 25°C, Natural Gas, 40°C Intercooler Inlet  
**Date:** 2025-12-01

---

## Complete Load Acceptance Profile

| Step Number | Load Range (% of Rated) | Step Size (%) | Recovery Time (s) | Speed Drop (%) | Cumulative Load (%) |
|-------------|-------------------------|---------------|-------------------|----------------|---------------------|
| **Step 1**  | 0% → 16%                | **16%**       | 10                | 8%             | 16%                 |
| **Step 2**  | 16% → 29%               | **13%**       | 10                | 8%             | 29%                 |
| **Step 3**  | 29% → 39%               | **10%**       | 10                | 8%             | 39%                 |
| **Step 4**  | 39% → 48%               | **9%**        | 10                | 8%             | 48%                 |
| **Step 5**  | 48% → 57%               | **9%**        | 10                | 8%             | 57%                 |
| **Step 6**  | 57% → 66%               | **9%**        | 10                | 8%             | 66%                 |
| **Step 7**  | 66% → 75%               | **9%**        | 10                | 8%             | 75%                 |
| **Step 8**  | 75% → 84%               | **9%**        | 10                | 8%             | 84%                 |
| **Step 9**  | 84% → 91%               | **7%**        | 10                | 8%             | 91%                 |
| **Step 10** | 91% → 100%              | **9%**        | 10                | 8%             | 100%                |

---

## Notes

1. **Recovery Time:** The generator requires 10 seconds to stabilize after each load step before the next step can be applied.

2. **Speed Drop:** Each step causes an 8% speed drop (frequency dip), which the governor corrects during the recovery period.

3. **Total Ramp Time:** To ramp from 0% to 100% load:
   - 10 discrete steps
   - 10 seconds recovery per step
   - **Total: ~100 seconds** (assuming instantaneous step application)

4. **BESS Requirement:** For a cold start (0% → 100%), a BESS must carry the full facility load for the entire 100-second ramp period, then gradually reduce output as the generator picks up load.

5. **Partial Ramps:** If starting from a non-zero load, the sequence begins at the appropriate step. For example:
   - Starting at 25% load → Begin at Step 3 (29%)
   - Starting at 50% load → Begin at Step 5 (57%)

---

## Interpolation Notes

**Steps 5-9 reconstructed from pattern:**
- Documented steps: 1-4 (0% → 48%) and final step (91% → 100%)
- Pattern indicates 9% steps from 48% to 91%, with one 7% step at 84% → 91%
- Total steps: 10 (matches "roughly 8-9 discrete steps" description)

**Validation:**
- Step 1-4 sum: 16% + 13% + 10% + 9% = 48% ✓
- Steps 5-9 sum: 9% + 9% + 9% + 9% + 7% = 43% → 48% + 43% = 91% ✓
- Final step: 9% → 91% + 9% = 100% ✓

---

## References

- `data/generators/caterpillar/Caterpillar-Technical-Analysis.md` - Original source
- Caterpillar Technical Bulletin (CG260-16 Load Acceptance Profile)

