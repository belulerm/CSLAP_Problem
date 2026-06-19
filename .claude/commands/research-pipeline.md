---
name: research-pipeline
description: Triggers the multi-agent optimization research and formulation pipeline for CSLAP under uncertainty.
usage: /research-pipeline "<topic_prompt>"
---

# Command: /research-pipeline

This command automates the orchestration of the 6-agent research-to-writing loop inside this repository.

## Execution Sequence

```bash
# 1. Initialize research topic from user input
TOPIC="$1"

# 2. Run Academic Researcher (opus)
# Uses: skills/deep-research, skills/literature-review-citation, skills/operations-research-scientific-writing
echo "Step 1: Running Academic Researcher on topic: $TOPIC..."
claude run academic-researcher "Perform deep research on: $TOPIC" > reports/1_research_report.md

# 3. Run Method Selector (claude-fable-5)
# Uses: skills/stochastic-modeling, skills/robust-modeling, skills/mathematical-formulation, skills/sparring-partner-review
echo "Step 2: Running Method Selector..."
claude run method-selector "Read reports/1_research_report.md and select the best optimization model. Sketch the formulation." > reports/2_method_report.md

# 4. Start Iterative Code & Review Loop (Max 5 iterations)
ITERATION=1
ACCEPTED=false

while [ $ITERATION -le 5 ] && [ "$ACCEPTED" = false ]; do
    echo "Iteration $ITERATION: Running Optimization Coder..."
    # Uses: skills/karpathy-guidelines-code, skills/algorithm-documentation, skills/stochastic-modeling, skills/robust-modeling
    claude run optimization-coder "Implement the formulation in reports/2_method_report.md inside Different_Solution_Approaches/Full_Package_Code_With_All_Approaches/CSLAP-Synthetic/Baselines/ following .claude/rules/code-standards.md" > reports/3_coder_log.md
    
    echo "Iteration $ITERATION: Running Code Reviewer..."
    # Uses: skills/karpathy-guidelines-code, skills/mathematical-formulation, skills/algorithm-documentation
    claude run code-reviewer "Review the code created or modified in reports/3_coder_log.md against reports/2_method_report.md" > reports/4_review_report.md
    
    # Check if Code Reviewer passed or failed
    if grep -q "VERDICT: FAIL" reports/4_review_report.md; then
        echo "Code review failed. Returning to coder."
        ITERATION=$((ITERATION+1))
        continue
    fi
    
    echo "Iteration $ITERATION: Running Scientific Reviewer..."
    # Uses: skills/sparring-partner-review, skills/experimental-results-presentation, skills/operations-research-scientific-writing
    claude run scientific-reviewer "Audit the code, test logs, and results in reports/3_coder_log.md. Verify scientific rigor." > reports/5_scientific_report.md
    
    # Parse YAML status block output from Scientific Reviewer
    STATUS=$(grep -E "^STATUS:" reports/5_scientific_report.md | awk '{print $2}')
    
    case "$STATUS" in
        "ACCEPTED")
            echo "Scientific Reviewer ACCEPTED results!"
            ACCEPTED=true
            ;;
        "REVISE_CODE")
            echo "Status: REVISE_CODE. Re-running coder..."
            ;;
        "REVISE_METHOD")
            echo "Status: REVISE_METHOD. Re-running Method Selector..."
            claude run method-selector "Revise formulation based on feedback in reports/5_scientific_report.md" > reports/2_method_report.md
            ;;
        "MORE_TESTING")
            echo "Status: MORE_TESTING. Running more scenarios..."
            ;;
        *)
            echo "Unknown status: $STATUS. Escalating to human."
            exit 1
            ;;
    esac
    
    ITERATION=$((ITERATION+1))
done

if [ "$ACCEPTED" = false ]; then
    echo "Maximum loop limit reached. Escalating pipeline state to human supervisor."
    exit 1
fi

# 5. Run Academic Writer (opus)
# Uses: skills/humanizer-writer, skills/academic-paper, skills/operations-research-scientific-writing, skills/thesis-chapter-drafting, skills/latex-thesis-build
echo "Step 5: Running Academic Writer to compile LaTeX draft..."
claude run academic-writer "Draft the paper sections in LaTeX using reports/2_method_report.md and reports/5_scientific_report.md. Enforce humanizer-writer rules." > reports/6_writer_report.md

echo "Pipeline execution finished successfully!"
```
