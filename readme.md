# Meesho Reseller Growth & Alert Intelligence Pipeline
Capstone Project IIT Roorkee.

This repository implements a complete, end-to-end pipeline for monitoring reseller growth and generating monthly stakeholder updates. It is designed to be **repeatable, guarded, and human-reviewed**, ensuring that every number is traceable and no narrative is invented.


## 📂 Repository Structure
  - `generate_dataset.py` → deterministic dataset generator (24 resellers, 900 orders).  
  - Outputs: `resellers.csv`, `orders.csv`, `meesho_reseller.db`.

  - `queries.sql` → SQL queries answering business questions.  
  - `output/` → CSV outputs (monthly revenue, region totals, top resellers, etc.).

  - `growth_engine.py` → functions for MoM growth, flagging, and feed validation.  
  - `test_growth_engine.py` → Given-When-Then unit tests.  
  - `fixtures/` → corrupted feed and validated monthly feed.

  - `prompt_pack.md` → reusable narrative prompt pack.  
  - `narrative_report.md` → worked narratives, chart-choice justification, self-scoring.  
  - `masking.py` → aliasing and leak-prevention functions.

  - `agent_spec.md` → agent specification (goal, tools, planner, guardrails).  
  - `mock_agent_runner.py` → orchestrates the pipeline, outputs structured JSON.


## 🚀 How to Run

### 1. Generate Dataset
```bash
cd data
python generate_dataset.py
