# agent-pipeline-protocol

This file defines the immutable protocol governing coordination, communication, and state transition between the 6 specialized agents in the CSLAP research pipeline.

```
┌──────────────────────┐
│  1. RESEARCHER        │──► Research report on the target topic
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  2. METHOD SELECTOR   │──► Method selection + math formulation sketch
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  3. CODER             │──► Python implementation
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│  4. CODE REVIEWER     │──► Bug report + math compliance matrix
└──────────┬───────────┘
           │
      PASS │         FAIL ──► Returns to CODER (3)
           ▼
┌──────────────────────┐     ACCEPTED    ┌──────────────────────┐
│  5. SCIENTIFIC        │───────────────►│  6. ACADEMIC WRITER   │
│     REVIEWER          │                │     (humanized)       │
└──────────┬───────────┘                └──────────────────────┘
           │
           ├── REVISE_CODE ──► Returns to CODER (3)
           ├── REVISE_METHOD ──► Returns to METHOD SELECTOR (2)
           └── MORE_TESTING ──► Returns to CODER (3) with scenario instructions
```

## Protocol Steps & Handoff Specifications

### Step 1: Academic Researcher
* **Input**: User-provided research prompt (e.g., "uncertainty in demand data for CSLAP").
* **Process**: Conducts literature review using academic databases.
* **Output**: **State-of-the-Art (SotA) Report** detailing existing methods, theoretical models, and relevant papers.

### Step 2: Method Selector
* **Input**: SotA Report and existing CSLAP formulations in `LaTeX_Articles_We_Have_Drafted/`.
* **Process**: Evaluates at least three candidate modeling approaches under OR, stochastic programming, and robust optimization frameworks.
* **Output**: **Method Selection Report** with a detailed mathematical formulation sketch.

### Step 3: Optimization Coder
* **Input**: Method Selection Report.
* **Process**: Writes Python solvers inside `Baselines/` extending CSLAP capabilities.
* **Output**: **Executable Python Code** + **Solver Log Files**.

### Step 4: Code Reviewer
* **Input**: Implementation Code.
* **Process**: Conducts static and mathematical compliance checks.
* **Output**: **Code Review Verdict** (`PASS` or `FAIL`) and a **Math-to-Code Compliance Matrix**.
  * If `FAIL`: Returns directly to **Step 3 (Coder)** with correction notes.
  * If `PASS`: Advances to **Step 5 (Scientific Reviewer)**.

### Step 5: Scientific Reviewer
* **Input**: Code, Code Review Verdict, and Solver Results.
* **Process**: Audits results statistical significance and experimental setups.
* **Output**: **Scientific Audit Report** + **Status Decision YAML block**.
  * `STATUS: ACCEPTED` -> Advances to **Step 6 (Academic Writer)**.
  * `STATUS: REVISE_CODE` -> Returns to **Step 3 (Coder)**.
  * `STATUS: REVISE_METHOD` -> Returns to **Step 2 (Method Selector)**.
  * `STATUS: MORE_TESTING` -> Returns to **Step 3 (Coder)**.

### Step 6: Academic Writer
* **Input**: Final math models, code, and verified computational results.
* **Process**: Drafts journal-grade article sections.
* **Filter**: **MANDATORY** processing through `skills/humanizer-writer/SKILL.md` to strip AI styling.
* **Output**: **LaTeX Draft File** compatible with `elsarticle`.

## Loop Governance Rules
1. **Loop Limit**: To prevent infinite loops and token exhaustion, the pipeline loop (Coder ↔ Reviewers) is constrained to a **maximum of 5 iterations**.
2. **Escalation**: If the loop exceeds 5 iterations without reaching `STATUS: ACCEPTED`, the Scientific Reviewer must halt and escalate the session to the human developer with a summary of the bottlenecks.
3. **Immutability of Rules**: Agents cannot alter, bypass, or rewrite rules. State transitions must be documented via status blocks.
