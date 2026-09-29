---
name: skeptical-review
description: Critique a document the way a hard but fair expert referee would. It states the core claim, verifies the citations, searches for counter-evidence and prior art, scores against anchored 1–5 rubrics, flags hard fails (fabricated sources, fatal flaws, already-done ideas), ranks the issues by importance with fixes, and lists the decisions only the author can make. Use it whenever someone asks to review, critique, stress-test, poke holes in, sanity-check or "be brutally honest about" a white paper, essay, proposal, pitch, business idea, research plan, strategy doc, design doc or RFC, even if they don't say "review". Not for line-editing prose or reviewing code diffs.
---

# Skeptical review

A review exists to find out whether a document deserves its reader's attention and what would make
it deserve more. It isn't there to encourage anyone. Be direct and specific; be fair, too: say
clearly what's strong, so it survives the revision.

## Workflow

1. **Read everything.** That means the document, what it came from (a brief, a seed, an earlier
   version) and any earlier review. In a later round, check whether each earlier issue was actually
   fixed before looking for new ones.
2. **State the core claim in one sentence.** If you can't, that's the first issue.
3. **Pick the rubric** from `references/rubrics.md` by document type: an *argument* (paper, essay,
   thesis, white paper), a *proposal* (venture, product, project or grant pitch), or a *plan* (design
   doc, RFC, project or strategy plan). Mixed documents take the closest one plus any criteria that
   clearly apply from another.
4. **Verify the citations** the argument depends on. Open them, and check that each exists and says
   what the document claims. Prioritise load-bearing ones: five checked properly beat twenty
   skimmed. A fabricated or badly misrepresented source is a hard fail. Record every check with a
   verdict (see the output format), so the author can see exactly what was verified.
5. **Test the core claim.** Search for the strongest counter-evidence and the closest prior art. If
   the idea already exists or is well known, originality is low, whatever the document says. Check
   the internal consistency too: sections that contradict each other are often the most useful
   finding.
6. **Score last**, after the analysis, using the anchors. See *Calibration* below.
7. **Write the review** in the format below. If the user wants it in a file, append it as the next
   `## Round N` to `review.md` next to the document (or wherever they say).

Don't rewrite the document unless asked; the review says what to fix. If the user wants the fixes
applied too, do that as a separate step after the review.

## Calibration

A **3** is a decent, unremarkable piece of work. A **5** is rare and means you'd show it to someone.
If most of your scores are 4s and 5s, recalibrate before writing. Inflated scores make a review
useless as a filter, and the reader loses the ability to tell good from great. Score what's on the
page, not what the document could become.

## Output format

```markdown
## Round N — YYYY-MM-DD (reviewing <version or date>)

### Verdict
<Three to five sentences: what the document gets right, what most needs to change, and whether it
deserves the reader's attention as it stands.>

### Scores
| Criterion | Score (1–5) | Note |
|---|---|---|
| … | | one line: why this score |

**Hard fails:** none | <which, with evidence>

### What's strong (keep)
<Specific: name the sections, lines and ideas that carry the document.>

### Issues (ranked, most important first)
1. **<The problem, in one line.>** Why it matters · the evidence (with source) · the suggested fix.
…

### Decisions for the author
<Questions only the author can answer (scope, thesis, trade-offs), each with the options and your
recommendation.>

### Citations checked
| Reference | Verdict | Note |
|---|---|---|
| [n] as cited, linked to the URL opened | ok · misrepresented · not-found · unreachable | what the source actually says, or why it couldn't be checked |

*Unreachable* means unverified, not fabricated; say so rather than guessing.

**Recommendation:** accept | revise | reject, with one sentence explaining why.
```

Rank issues by how much they change the conclusion, not by where they appear. Most documents have
3–8 issues that matter; don't pad the list with typos. For each one, separate what can be fixed
from what needs the author's judgement. The second kind goes under *Decisions*.

## Tone

Write the way you'd want a respected colleague to review your own work: blunt about substance,
never snide. Quote the document when pointing at a problem, and back each claim about the outside
world with a source.
