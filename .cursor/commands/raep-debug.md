---
allowed-tools: Read, Write, Bash, WebSearch, mcp__perplexity-ask__*, mcp__exasearch__*, mcp__ref__*, mcp__BetterST__sequentialthinking
description: RAEP debugging protocol - Systematic debugging workflow using RAEP methodology for root cause analysis and investigation
argument-hint: [issue description or error details]
---

<agent_request>
<mode>conversation_only</mode>
<original_intent>User requested RAEP debugging protocol for systematic debugging workflows focused on root cause analysis and investigation</original_intent>
<current_task_summary>Execute RAEP debugging protocol (Steps 0,1-8,10) with focus on investigation, root cause analysis, and debugging findings - skipping story enrichment</current_task_summary>
<workflow>raep-debug</workflow>
<conversation_message>

Execute the **RAEP Debug Protocol** workflow as defined in `/srv/projects/instructorv2/skills/raep-debug/SKILL.md`.

**User Request**: {{COMMAND_ARGUMENTS}}

**Instructions**:
1. Read the complete workflow from `/srv/projects/instructorv2/skills/skills/raep-debug/SKILL.md`
2. Follow Steps 0, 1-8, and Step 10 sequentially (Step 9 skipped for debugging)
3. Use BetterST at every planning decision point
4. Create working directory: `.scratch/raep-debug/{NN}-{issue-slug}/`
5. Document all outputs per skill instructions

**Protocol Summary** (Full details in skill):
- **Step 0**: Setup - Create numbered working directory
- **Step 1**: Inventory - Validate files, dependencies, locate error logs
- **Step 2**: Theorize - Generate root cause hypotheses with BetterST
- **Step 3**: Ask Perplexity - Query for known issues and troubleshooting
- **Step 4**: Validate Perplexity - Cross-reference with official docs
- **Step 5**: Quick Tests - Minimal disqualification tests
- **Step 6**: Research - Deep validation and investigation
- **Step 7**: Decompose - Component breakdown and failure modes
- **Step 8**: Evaluate - Fix strategy comparison
- **Step 9**: SKIPPED - Story enrichment not needed for debugging
- **Step 10**: Handoff - Investigation log with root cause and fix recommendations

**Critical**:
- Use BetterST (`mcp__BetterST__sequentialthinking`) liberally at EVERY planning decision
- Fix-Forward Rule: If investigative step fails, PAUSE → research blocker → fix → validate → resume
- All claims must be validated via official documentation
- Create numbered semantic folders: `01-issue-name`, `02-next-issue`, etc.
- Goal: Root cause identification with actionable fix recommendations

</conversation_message>
</agent_request>
