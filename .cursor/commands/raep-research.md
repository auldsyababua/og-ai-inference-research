---
allowed-tools: Read, Write, Bash, WebSearch, mcp__perplexity-ask__*, mcp__exasearch__*, mcp__ref__*, mcp__BetterST__sequentialthinking
description: Research Agent Enrichment Protocol - 11-step systematic research workflow with BetterST-powered planning
argument-hint: [research topic or issue description]
---

<agent_request>
<mode>conversation_only</mode>
<original_intent>User requested Research Agent Enrichment Protocol (RAEP) for systematic research and investigation workflows</original_intent>
<current_task_summary>Execute the 11-step RAEP research protocol with liberal BetterST usage for planning, hypothesis formation, and decision-making</current_task_summary>
<workflow>raep-research</workflow>
<conversation_message>

Execute the **Research Agent Enrichment Protocol (RAEP)** workflow as defined in `/srv/projects/instructorv2/skills/skills/raep-research/SKILL.md`.

**User Request**: {{COMMAND_ARGUMENTS}}

**Instructions**:
1. Read the complete workflow from `/srv/projects/instructorv2/skills/skills/raep-research/SKILL.md`
2. Follow all 11 steps sequentially (Steps 0-10)
3. Use BetterST at every planning decision point
4. Create working directory: `.scratch/raep-research/{NN}-{research-topic-slug}/`
5. Document all outputs per skill instructions

**Protocol Summary** (Full details in skill):
- **Step 0**: Setup - Create numbered working directory
- **Step 1**: Inventory - Validate all references
- **Step 2**: Theorize - Generate hypotheses with BetterST
- **Step 3**: Ask Perplexity - Research lead generation
- **Step 4**: Validate Perplexity - Independent verification
- **Step 5**: Quick Tests - Disqualification tests
- **Step 6**: Research - Deep validation
- **Step 7**: Decompose - Component validation
- **Step 8**: Evaluate - Approach assessment
- **Step 9**: Enrich Story - Dual format output (TLDR + XML)
- **Step 10**: Handoff - Summary to Planning Agent

**Critical**:
- Use BetterST (`mcp__BetterST__sequentialthinking`) liberally at EVERY planning decision
- Perplexity is for RESEARCH LEADS only, not solutions
- All claims must be validated via official documentation
- Create numbered semantic folders: `01-topic-name`, `02-next-topic`, etc.

</conversation_message>
</agent_request>
