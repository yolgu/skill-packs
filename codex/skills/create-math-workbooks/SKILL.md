---
name: create-math-workbooks
description: Create foundation-focused mathematics workbooks with five options and exactly one correct answer per exercise. Design meaningful distractors, verify every option, and deliver Korean problem and detailed solution PDFs for mathematics for AI, discrete mathematics, digital signal processing, and related subjects. Also create targeted practice from submitted mistakes. Use for workbook or practice-set generation rather than isolated problem solving.
---

# Create Math Workbooks

Turn a subject and chapter into a coherent practice sequence for a beginner in that subject. Every practice item has five answer options and exactly one correct answer. Deliver two Korean PDFs: a problem workbook and a separate answer key with detailed solutions and explanations of all four distractors. Use available calculation and document tools to carry out this workflow.

A high-quality item exercises the intended mathematics, provides an unambiguous task, and makes each wrong option educationally meaningful. Its quality does not come from being difficult, having five options, or producing an impressive-looking answer key.

## Establish the scope

- Use supplied course materials, chapter contents, and learning objectives as the scope. Read the actual material; do not infer its contents from a title alone.
- Without materials, derive a reasonable introductory scope from the subject and chapter, and state the coverage and necessary prerequisites briefly in the workbook. Ask only if missing information would materially change the topic or make the request ambiguous.
- Start at the subject's introductory level. Supply only the prerequisite mathematics needed for this chapter, rather than assuming university knowledge or rebuilding an entire school curriculum.
- Generate the chapter's workbook and solutions together. Do not turn the request into an interactive lesson that waits for an answer after every question.

## Design the practice

1. Break the chapter into small learning objectives. Map each exercise to a specific concept, procedure, or reasoning move, and check that important objectives receive practice.
2. Introduce a new procedure with a fully worked example that explains both the action and its reason. Move through partially completed work toward independent basic practice, reducing help as the sequence progresses.
3. Choose the form of support for the objective. A partial solution can ask which next step is valid; a definition can ask which object satisfies a stated condition; a proof can ask which justification closes a specified gap. Keep the response format single-answer multiple choice. Recognizing a proof step is not evidence that the learner can construct a proof unaided.
4. Initially change a small number of meaningful features, such as signs, representations, or conditions. Later require selection of a method, interpretation, or transfer. Avoid long runs of number substitutions that add no learning value.
5. Include concept checks as well as calculations. Let learners select a valid reason, distinguish conditions, identify an error in a given step, or recognize a counterexample when these actions serve the objective. Each item should have one central testing point, even when advanced work connects earlier concepts.
6. After initial focused practice, mix learned problem types so the learner must choose an approach. Include a small revisit set to attempt later without first reading the solutions; do not impose one universal review interval.
7. Keep advanced work short and grounded in concepts already introduced. Do not manufacture difficulty through excessive arithmetic, trick wording, or unexplained prerequisites.

Treat difficulty and the amount of help as separate dimensions. Foundational practice can involve definitions, reasoning, and small proofs; it is not limited to arithmetic. A static workbook offers a learning sequence, not evidence of the learner's mastery.

Use an approximately 80% foundational, 15% variation/application, and 5% advanced exercise mix unless the user specifies otherwise. Count fully worked teaching examples separately. Classify exercises by their actual demands, not by their section labels. Round to sensible whole counts, keeping foundations dominant; do not add exercises merely to force a percentage or a minimum advanced count. This mix is a preference, not a claim of a universally optimal research result.

Determine the total count from the chapter's objectives and the practice needed to cover them. Honor a user-specified count and deliver that full set; do not substitute a shorter validation sample for the requested workbook. Balance coverage within that count rather than silently increasing it or treating every subpart as an extra exercise to inflate coverage.

## Write focused mathematical stems

- State the requested task and every condition needed to solve it: domains, dimensions, units, index origins, boundary values, probability spaces, or transform conventions where relevant.
- Use manageable values for early practice. Constructing a valid object or an intended result first can help choose suitable parameters, but still solve the final written question independently of that construction.
- Write original exercises aligned with the learning objectives. Do not reproduce source problems or merely replace their numbers while preserving distinctive wording.
- Specify what a complete answer must contain. A question about all solutions needs an option containing the complete solution set; a question about a counterexample needs exactly one qualifying option. Do not turn a binary distinction into five near-duplicate choices.
- Make the task understandable before reading the options. Include relevant conditions in the stem and omit unrelated narrative. For a next-step or explanation question, specify the exact mathematical decision to be made.
- Prefer direct wording. Highlight a necessary negative when error detection is the learning objective. Preserve mathematically necessary negations and quantifiers; do not remove them under a blanket wording rule.
- Make required notation understandable at the stated level. Keep ordinary exercise answers out of the problem workbook; fully worked teaching examples are intentionally visible there.

## Build five meaningful options

Solve the stem without relying on the choices first. Establish the correct value, conclusion, or complete response before designing distractors.

For each of the four wrong options, identify a specific plausible error or misconception and derive the resulting response. Keep a concise internal association between the option, the erroneous step or interpretation, and its correction. Prefer errors evidenced by supplied learner work; otherwise describe them as plausible errors, not empirically established misconceptions.

Useful error sources depend on the objective: pairing the wrong components, dropping a term, changing a sign, applying a rule outside its conditions, confusing a converse with an implication, omitting a case, using the wrong signal index, or reporting an intermediate result as the final answer. Select errors relevant to this stem and level rather than using this list as a quota. Do not start with arbitrary numbers and invent implausible stories to justify them afterward.

Select four distinct, defensible distractors. Each must be wrong under the stated task, understandable to the intended learner, and connected to a concrete mathematical mistake. If four such options cannot be produced, revise the values, representation, or question focus while preserving its objective and difficulty, or replace the item. Do not pad the list, reduce it below five, or escalate the mathematics merely to fill the slots.

Review the options together:

- Use comparable response types, units, notation, precision, and wording. A difference in type or dimension belongs in an option only when distinguishing it is itself the learning objective.
- Avoid absurd magnitudes, irrelevant concepts, joke answers, and choices that can be discarded without the intended mathematics. A nearby number is not automatically a plausible error.
- Do not use label-based combinations, all-of-the-above, or none-of-the-above shortcuts. A specific mathematical claim that no solution exists is allowed when that claim itself is being assessed.
- Remove unintended clues from unequal detail, repeated wording, grammatical fit, conspicuous precision, or a subset of choices that already exhausts the logical possibilities. Do not disguise two or three real alternatives as five.
- Use numerical or another natural order when it improves readability. Otherwise vary positions without a predictable cycle. Review the set for answer-position cues, but do not distort valid options or sacrifice natural ordering to force an exact position quota.
- Check that a mistaken method does not accidentally produce the correct result for the chosen parameters. Change the parameters when they conceal the error the item is meant to distinguish.

Do not make the key merely the "most correct" of several mathematically correct responses. If the task involves choosing a best method, provide an explicit criterion that makes exactly one option satisfy the requested decision.

## Verify and repair the mathematics

Draft the intended answer and solution with each problem, then re-solve the final wording using only its stated conditions. Check that the problem is well-defined and that the proposed solution answers exactly what is asked. Apply this review to worked teaching examples as well as exercises.

Evaluate every option against the stem, not only the intended key. Establish exactly one correct response and four incorrect responses. Verify that each error path actually produces its associated distractor and that the correction explains the failure. Check full statements, domains, endpoint conventions, and requested answer forms rather than just matching strings.

For value questions, reduce equivalent fractions, expressions, units, sets, or matrices to comparable meanings and detect duplicates. Check whether rounding makes different options indistinguishable. A required representation may distinguish equal values only when that representation is the explicit learning target, such as a fraction in lowest terms; verify compliance with that requirement.

Choose checks for the concrete failure modes of the problem:

| Problem type | Useful verification | Limits to respect |
|---|---|---|
| Numerical calculation | Execute a recalculation, inverse operation, substitution, or independent formula. Use exact integers or rational values when suitable. | For approximations, choose tolerances appropriate to scale and rounding; check units and reported precision. |
| Algebra and equations | Substitute into the original equations, check domains, and use symbolic operations when useful. | Account for excluded values, extraneous roots, and lost cases. An unresolved symbolic result is not proof that no solution exists; one numerical root is not all roots. |
| Calculus | Check applicable hypotheses, reverse differentiation or integration, and use numerical checks as supporting evidence. | Agreement at sampled points does not establish a general identity or theorem. |
| Linear algebra | Recompute operations and substitute into defining relations such as a linear system or eigenvector equation. | Verify dimensions and assumptions, and distinguish existence from uniqueness. |
| Finite logic and counting | Enumerate all cases when feasible, build a complete truth table, or use an independent counting argument. | State whether coverage is exhaustive. Do not describe sampled cases as all cases. |
| Proofs and general claims | Review definitions, assumptions, quantifiers, implications, case coverage, and possible counterexamples. | Finding no counterexample is not a proof. Numerical evidence cannot replace the required reasoning. |
| Discrete signals | Compute the defining sums and, when useful, compare another representation. | Preserve sample indices, support, boundaries, transform signs, normalization, and linear versus circular convolution. |

For computable exercises, actually execute an appropriate calculation when the environment supports it. Do not present an imagined tool run as evidence. A comparison against a supplied reference answer only establishes agreement with that reference; it does not establish the reference's correctness or validate the explanation.

Use enough checking to address the mathematical risk, not a fixed number of methods per item. A second pass should test the written conditions or a meaningful alternative calculation, not simply repeat the draft answer. Retain concise working evidence of actual results and necessary corrections internally; a separate student-facing verification report is not required.

If a check exposes an error, revise the affected stem, options, worked steps, option explanations, and answer together, then recheck affected items. After ordering or changing options, verify that the answer label still points to the correct content. Do not publish an unresolved item as correct: repair it or replace it with a verified item serving the same objective. If verification or PDF production remains unavailable, state the specific limitation honestly and preserve useful work rather than claiming completion.

Mathematical verification and distractor plausibility are different judgments. Passing calculations does not establish diagnostic accuracy or statistical discrimination. If actual response data later becomes available, use repeated errors, rarely chosen distractors, and unexpected answer patterns to revise items. Do not invent response statistics or require classroom trials before producing a practice workbook.

## Explain every answer

Provide a complete explanation for every exercise, including routine ones. Identify the target, explain how to start and why the relevant definition or formula applies, show the necessary intermediate steps, and state both the correct option label and its mathematical content with conditions or units. Teach the solution itself, not only how to eliminate the other choices.

Adjust length to the item while preserving the steps a beginner needs. Do not substitute a bare answer or a reference to another exercise for that explanation. Address a likely misconception when it is relevant. A correction to a problem must appear consistently in its solution and answer key.

Explain all four wrong choices concisely: identify the mathematical mistake or failed condition and show what must be corrected. Do not write only "incorrect," repeat the option, or claim that selecting it proves a particular misconception. Where helpful, give the erroneous calculation or a decisive counterexample.

Keep student-facing reasoning within the chapter's stated knowledge. A more advanced internal verification method does not need to appear in the teaching solution.

## Produce the two Korean PDFs

- Write titles, directions, questions, explanations, table headings, captions, and delivery notes in natural Korean. Keep standard mathematical symbols and necessary abbreviations; introduce technical terms with an understandable Korean explanation.
- Put coverage, brief prerequisites and concepts, worked examples, and numbered five-option practice with usable working space in the problem workbook. Tell the learner to choose one answer. Label options consistently from 1 through 5 and keep each stem with its options where possible.
- Put a concise answer key, detailed numbered solutions, and the four distractor explanations in the separate solution PDF. Match the problem identifiers, option labels, conditions, notation, and final answers exactly.
- Keep the numbering stable through corrections and make a correction in both documents. Do not expose authoring logs, research summaries, or verification machinery as part of the learner's task.
- Use an available PDF workflow with Korean-capable fonts and readable mathematical notation. Render and inspect the final PDFs, checking missing glyphs, clipped formulas, page breaks, writing space, and the correspondence between the two files. Text extraction alone does not establish visual correctness.
- Deliver the two PDFs with a brief Korean description of their coverage. Internal calculation files and build artifacts are not additional required student deliverables.

## Respond to mistakes

When the learner later supplies incorrect answers or working, identify the demonstrated gap and create focused supplementary practice. Restore only the support needed, then return to independent attempts and a small transfer check. Include explanations and apply the same verification process. If an answer alone does not reveal the cause, address plausible gaps without claiming to know the learner's reasoning or inventing a mastery score.
