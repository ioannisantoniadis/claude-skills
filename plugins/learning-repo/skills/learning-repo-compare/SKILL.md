---
name: learning-repo-compare
description: Compare the output quality of several learning repositories (technical books, notes collections) on equal terms, or monitor one over time, by counting confirmed defects rather than scoring process. It makes blinded copies (process documents removed), plants known errors to measure the auditor's sensitivity, draws a seeded sample of checkable claims, runs one fresh low-cost auditor per repo, confirms every reported defect against the original, and reports defects per 10,000 words plus a merge-readiness inventory (notation clashes, shared devices). Use it when the user asks which of their repos is more reliable, whether more process produced better quality, how books compare before a merge, or wants a cheap periodic quality check across repos. For a single deep audit with rubric scores, use learning-repo-audit instead.
---

# Learning-repo compare

A comparison is only fair if every repo is measured the same way, by an auditor who cannot be
impressed by a paper trail, and whose own miss rate is known. This skill does that cheaply.
The full procedure, definitions and metrics are in `references/protocol.md`; read it before
starting. The first run, on four books, is in `references/baseline-2026-10.md`: use it to
calibrate expectations (densities of about 3–14 confirmed defects per 10,000 words; 92% of
planted errors found).

## Ground rules

- **Measure, don't fix.** The audited repos are never modified. Fixes are a separate step: in
  the user's current repo, or as a GitHub issue per other repo listing the confirmed defects.
- **Blind and plant.** Auditors see a copy without plans, decision logs, research logs or
  earlier audits, containing four planted errors whose key they never see. A clean result
  then means something, and a paper trail cannot raise a score.
- **Confirm before counting.** A defect counts when two auditors report it independently, or
  when one reports it and you find it in the original repository.
- **Keep it cheap.** One auditor per repo, on a mid-size model, in lean mode (no site rebuild,
  no figure re-runs, no browser), started one at a time. A full audit cost about 230,000–320,000
  tokens; a lean one about 110,000. Add a second auditor only to measure agreement.

## Workflow

1. **Blind.** For each repo: `python scripts/blind_copy.py <repo> <scratch>/<name>`.
2. **Plant, then sample.** Plant four errors per copy (a number, a quotation, an equation
   factor or sign, a caption that contradicts its figure; two in places likely to be sampled),
   record the key outside the copy, then draw the sample from the planted copy:
   `python scripts/inventory.py <scratch>/<name> <scratch>/sample-<name>.md`. Drawing the
   sample before planting lets the auditor spot plants by comparing texts.
3. **Brief.** Write an auditor brief from protocol §3, §5 and §6, with the planting rules
   removed and two lines added: the copy may contain planted errors; return the report as the
   final message and keep scratch files inside the copy.
4. **Audit.** Start one fresh auditor (a subagent with no context) per repo, one at a time,
   confined to its copy and to primary sources fetched with `curl` or a fetch tool.
5. **Confirm and score.** Save each report. Check every non-planted defect against the original
   repository. Count confirmed defects per 10,000 prose words by severity, and planted errors
   found. With two auditors per repo, `python scripts/metrics.py verdicts.json` gives sampled
   rates, Wilson intervals and kappa.
6. **Report.** One results file: a table per repo (audits, words, confirmed defects, density,
   major, planted found), what it shows, the actions taken (fixes made, issues filed), and the
   merge inventory (symbols and their meanings across repos, shared devices, templates).

## Pitfalls seen in the first run

- Subagents cannot write report files; ask for the report as the final message.
- A general-purpose auditor may open a browser to view interactive figures; forbid it.
- Removing files the tests read breaks the build; `blind_copy.py` keeps them.
- Running many full auditors in parallel exhausted the usage limit twice; go one at a time.
- Typed numbers drift from script output; generated numbers and executable cells had the
  fewest numeric errors. Most defects in every repo were cross-references, captions,
  near-verbatim quotations and notation reuse, not computation.
