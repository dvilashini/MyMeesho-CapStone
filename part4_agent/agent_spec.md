# Agent Specification

## Goal
Keep Meesho category managers informed of any category whose month‑on‑month revenue moves beyond the 8% threshold, with a human approving every message before it goes out.

## Tools
- `validate_feed` (Part 2)  
- `mom_growth` (Part 2)  
- `is_flagged` (Part 2)  
- Prompt‑pack template fill (Part 3)

## Memory / State
- Previous month’s revenue per category, stored between runs, to compute MoM growth.

## Planner (Ordered Subtasks)
1. Load the monthly revenue feed and run `validate_feed`.  
2. If invalid → Hard Stop, report errors.  
3. If valid → compute `mom_growth` for every category vs previous month.  
4. Run `is_flagged` on every category.  
5. Sort flagged categories by `abs(mom_pct)` descending.  
6. Draft a message (via prompt‑pack template) for at most the top 3 flagged categories.  
7. Log remaining flagged categories as “suppressed, review manually.”  
7b. Log any `"escalate_exact_boundary"` categories into `escalated_categories`.  
8. Emit one structured JSON object per run.

## Feedback Loop
- Human approval checkpoint before any drafted message is considered “sent.”  
- Simulated as `action_taken = "drafted_and_held_for_approval"` in JSON output.

## Guardrails
- **Input:** `validate_feed` must pass before anything else runs.  
- **Action:** No message is ever auto‑sent, only drafted and held.  
- **Output:** Every number in a drafted message must trace back to Part 1/Part 2 values.

## Success / Error Conditions
- **Success:** Drafts produced (or zero drafts if nothing flagged), all numbers traceable.  
- **Error:** `validate_feed` returns False → Hard Stop with surfaced errors.

## Given‑When‑Then Specs
- **GIVEN** April→May Ethnic Wear revenue moves from 104520.77 to 185107.61, **WHEN** agent runs, **THEN** Ethnic Wear flagged with +77.1% and drafted message produced.  
- **GIVEN** May→June Beauty & Personal Care revenue moves from 35542.11 to 37559.07, **WHEN** agent runs, **THEN** flagged result is “not_flagged” and no draft produced.  
- **GIVEN** synthetic previous=100000, current=108000, **WHEN** agent runs, **THEN** escalate_exact_boundary logged, no draft produced.  
- **GIVEN** corrupted_feed.csv, **WHEN** agent runs, **THEN** validation_status = invalid, action_taken = hard_stop, with exactly 3 validation errors surfaced.
