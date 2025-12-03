---
allowed-tools: Read, Write, Edit, Bash, WebSearch, mcp__perplexity-ask__*, mcp__exasearch__*, mcp__ref__*, mcp__BetterST__sequentialthinking
description: RAEP development protocol - Systematic feature development workflow using Plan-Execute-Check cycles at every step
argument-hint: [feature description or requirements]
---

<agent_request>
<mode>conversation_only</mode>
<original_intent>User requested RAEP development protocol for systematic feature/component development with enforced Plan-Execute-Check cycles</original_intent>
<current_task_summary>Execute RAEP development protocol (Steps 0-10) with Plan-Execute-Check enforcement at every step, building working implementation with tests and validation</current_task_summary>
<workflow>raep-dev</workflow>
<conversation_message>

Execute the **RAEP Development Protocol (RAEP-DEV)** workflow as defined in `/srv/projects/instructorv2/skills/skills/raep-dev/SKILL.md`.

**User Request**: {{COMMAND_ARGUMENTS}}

**Instructions**:
1. Read the complete workflow from `/srv/projects/instructorv2/skills/skills/raep-dev/SKILL.md`
2. Follow all 11 steps sequentially (Steps 0-10)
3. Use BetterST at every planning decision point
4. Create working directory: `.scratch/raep-dev/{NN}-{feature-slug}/`
5. Enforce Plan-Execute-Check loops in Step 7 (CRITICAL)
6. Document all outputs per skill instructions

**Protocol Summary** (Full details in skill):
- **Step 0**: Setup - Create numbered working directory
- **Step 1**: Inventory - Requirements and environment
- **Step 2**: Theorize - Design approaches with BetterST
- **Step 3**: Ask Perplexity - Best practices research (2024/2025)
- **Step 4**: Validate Perplexity - Official documentation verification
- **Step 5**: Prototype - Proof-of-concept validation
- **Step 6**: Design - Detailed component specifications
- **Step 7**: Implement - Component-by-component with Plan-Execute-Check loops (CRITICAL)
- **Step 8**: Integrate - Wire components, integration tests
- **Step 9**: Validate - User acceptance and edge cases
- **Step 10**: Handoff - Deployment plan and summary

**CRITICAL - Step 7 Enforcement**:
For EACH component: PLAN (design) → EXECUTE (code) → CHECK (tests/lint/types) → MUST ALL PASS before next component
- No-Skip Rule: Never proceed if checks fail
- Fix-Forward Rule: If validation fails, PAUSE → research → fix → validate → resume

**Critical**:
- Use BetterST (`mcp__BetterST__sequentialthinking`) liberally at EVERY planning decision
- ALL validation checks must pass before proceeding
- Create numbered semantic folders: `01-feature-name`, `02-next-feature`, etc.
- Goal: Working, tested implementation ready for production

</conversation_message>
</agent_request>
