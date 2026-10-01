# Prompt Pack: Flagged Category Narrative

## Trigger
- Activated when a category’s `is_flagged` result equals `"flagged"`.

## Input List
- {category}
- {previous_revenue}
- {current_revenue}
- {mom_pct}
- {prev_month}
- {month}

## Prompt
Use the following structure:

**Context:** State what is being measured, naming {category}, {prev_month}, and {month}.  
**Insight:** Report the exact {mom_pct} change, explicitly labeled as a fact, and reference {previous_revenue} and {current_revenue}.  
**Implication:** Provide a specific, actionable recommendation. If proposing a cause, label it as a hypothesis.  
Never invent numbers — only use the supplied placeholders.

## Checklist
1. Every number in the narrative matches a supplied placeholder exactly.  
2. Every claim is labeled as either fact or hypothesis.  
3. The recommendation is specific and actionable (e.g., “audit supply chain delays in {region}”), not vague.  
4. No raw reseller names appear; only aliases via `alias_for`.  
