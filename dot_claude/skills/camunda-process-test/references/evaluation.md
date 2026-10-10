# Evaluate behavioral acceptance gaps

Read the stated goal, minimal acceptance criteria, affected process and worker contracts, and existing scenarios. Map each criterion to the actual observation that proves it, including relevant success, failure, preservation, or recovery conditions.

Prefer existing E2E coverage through the real entry point. Where E2E cannot run, explain the concrete constraint and assess integration coverage across the real affected components. Identify what a fake or manually completed job leaves unverified. Recommend the smallest set of scenario changes needed to close material behavioral gaps; do not assign a structural coverage tier or require every node to be visited.

For each useful scenario, state its business outcome, triggering conditions, public boundary, existing coverage to reuse, and actual execution result or pending status. Use BPMN branch, boundary, and DMN coverage to investigate possible omissions. Do not equate process completion or rule selection alone with correct produced data or external effects.

Review redundancy by required observations. Retain scenarios with distinct outcomes even when their paths overlap. Summarize uncovered behavior and why it remains uncovered in the existing review record. No new document or approval is required for routine test selection.
