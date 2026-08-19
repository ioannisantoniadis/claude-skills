# Voice and Structure Reference

## The one fixed structural rule

Every real topic file (all 15, confirmed) opens with `## Core Idea` and closes with
`## Interview Check` (singular "Check" — note `templates/topic-note.md` says "Interview
Checkpoints", plural; the real files don't follow that, use the singular form that's
actually proven). Everything between those two bookends is bespoke per topic — there is no
fixed middle template despite `templates/topic-note.md` implying one (that template's
"Problem It Solves" / "Assumptions" / "Key Equations Or Algorithms" / "References" headers
don't appear verbatim in any real topic file — treat the template as a starting skeleton to
freely deviate from, not a spec to fill in literally).

Real header sets vary a lot by subject, e.g.:
- A landscape/orientation topic: Core Idea → The Main Axes → Where Methods Fit → Common
  Confusions → What To Be Able To Explain
- A methods-survey topic: Core Idea → [one subsection per sub-method, e.g. Markov Chains →
  Hidden Markov Models → State-Space Models → Neural Sequence Models] → Interview Check
- A systems/applied topic: Core Idea → System Components → Production Failure Modes →
  Evaluation Layers → Inference Optimization → Interview Check

Pick a middle structure that fits how the actual subject decomposes — don't force an
unrelated topic's header set onto a new one.

## Tone and density

Dense, declarative reference prose — short paragraphs and bullets, not long expository
writing. Occasional tables. Occasional plain-text pseudo-diagrams in fenced ` ```text ` ```
blocks for simple state transitions (e.g. `hidden state_t -> hidden state_t+1`) rather than
Mermaid (Mermaid is reserved for `OVERVIEW.md`'s field-connection diagram, not used inside
individual topic files). No LaTeX math and no code snippets in the topic files themselves —
this is a conceptual map, not a textbook or a code reference.

Calibration excerpts (real, from existing topic files):

> "A model can be generative without being a modern GenAI model."

> "Causal inference is about interventions, not higher-accuracy prediction."

> "An HMM has hidden states and observed emissions: ... Use when observations are noisy
> signals of an underlying state."

That's the register: short, declarative, definitional statements that preempt a specific
confusion or answer a specific "when do I use this" question — not a general-purpose
explainer.

## `## Interview Check` (closing section)

One short paragraph naming what the reader should be able to explain or walk through after
this topic — not a question list, a capability statement. E.g. (paraphrased shape, not a
real quote): "You should be able to explain X, walk through Y, and say why Z fails when
W happens."

## Length

38-70 lines total per existing topic file. A new topic file — or a new subsection inside an
existing one — should land in a comparable range for its scope. Don't pad; the existing
files are proof that terse is the house style, not a minimum draft to expand later.
