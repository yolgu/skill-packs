# Testing Theory

Why a passing test suite justifies what it does, and no more. Read this only while designing a behavior list;
the rules that use it live in [Feature Implementation Flow](feature-implementation-flow.md). Everything here is
explanation, not instruction.

## Contents

- [Tests Show Presence, Not Absence](#tests-show-presence-not-absence)
- [The Fundamental Theorem and Its Limits](#the-fundamental-theorem-and-its-limits)
- [Test Hypotheses: Uniformity and Regularity](#test-hypotheses-uniformity-and-regularity)
- [Contracts as the Vocabulary of Proof](#contracts-as-the-vocabulary-of-proof)
- [Property Tests and the Small-Scope Hypothesis](#property-tests-and-the-small-scope-hypothesis)
- [Mutation Testing and What a Score Says](#mutation-testing-and-what-a-score-says)
- [Falsification, Triangulation, and Types](#falsification-triangulation-and-types)
- [What a Passing Suite Lets You Claim](#what-a-passing-suite-lets-you-claim)

## Tests Show Presence, Not Absence

Dijkstra's remark that testing shows the presence of bugs, not their absence, ended not in "stop testing" but in
growing the proof and the program hand in hand. Test-driven development did not descend from that tradition: by
its author's account it revives the old practice of fixing the expected output before writing the program, and
he describes success as confidence and asymptotic improvement rather than proof. The proof tradition still reads
TDD well, since both write down what counts as correct in a checkable form before the implementation exists. The
difference is that a proof treats the universal statement (all inputs) by deduction while a test executes a
sample of it; the hypothesis-based theories below close that gap.

## The Fundamental Theorem and Its Limits

Goodenough and Gerhart proved that a passing test set satisfying a reliable and valid criterion implies a
correct program. The theorem is true and nearly circular: such a criterion cannot be computed in general
(Howden), and the two properties are defined relative to the program and are not independent (Weyuker and
Ostrand). What survives is its shape: a passing test always guarantees something under some assumption, and the
honest statement names the assumption. Weyuker's adequacy axioms add that criteria derived from program
structure may demand different test sets for two programs with the same meaning, so tests written to fill
coverage are coupled to the implementation, while specification-derived test sets transfer to any implementation
of the specification.

## Test Hypotheses: Uniformity and Regularity

Bernot, Gaudel, and Marre formalized testing as a conditional proof: hypotheses about the implementation plus a
finite test set imply correctness. Under the minimal hypothesis (deterministic, no hidden state the
specification omits, every value built through specified operations, values comparable) passing the infinite
exhaustive test set is equivalent to correctness. Finite criteria rest on stronger hypotheses. Uniformity says
the implementation behaves the same across a sub-domain, so one test per sub-domain suffices; regularity says
passing every test up to a size bound implies passing all. Equivalence partitioning is uniformity under its
everyday name: declaring "every value in this partition follows the same rule" states the hypothesis, and one
example per partition is the exhaustive set under it. Boundary value analysis samples where uniformity most
often breaks, because an off-by-one or a reversed comparison moves the partition's edge, which an interior value
cannot see. The minimal hypothesis becomes concrete testability conditions (inject time, randomness, and
identifier generation; build values only through constructors that enforce invariants; give values equality),
and when these fail, passing implies nothing. This is why the behavior list records, next to each example, the
partition it represents and why it is believed uniform.

## Contracts as the Vocabulary of Proof

Hoare logic and design by contract supply preconditions, postconditions, and invariants. One test is a sample of
a Hoare triple: one state satisfying the precondition, the program, and the postcondition evaluated at that
state. A proof covers every such state; a test covers a few points. Assertions written as postconditions over
observable results stay valid across implementations, while asserting internal call order inspects one
implementation's trace instead of the triple. Hoare's 1996 retrospective concedes that large systems became
reliable through management, severe testing, and removing errors in use more than through proof, and notes that
tests planned before the code are necessarily black-box tests at the outermost interface. Meyer adds that tests
cannot replace a specification (tests can be generated from one, not the reverse) and that contracts inside the
code turn every run during testing into an oracle. Parnas's information hiding is the design-side condition for
tests that survive change: when volatile decisions sit behind the interface that tests observe, changing a
decision leaves the tests alone.

## Property Tests and the Small-Scope Hypothesis

A property states "for every x satisfying the precondition, the postcondition holds of f(x)" and searches
generated samples for a counterexample; a thousand passing runs are a thousand failed refutations, not a proof.
Hughes showed that a set of inductive properties mirrors the base case and inductive step of a correctness
proof, so correctness follows when each universal statement holds and every value can be built by the
constructors, itself a hypothesis to test. Model-based properties transplant Hoare's 1972 abstraction-function
proofs and found every planted bug in Hughes's comparison, while invariant-only properties missed most.
Model-based and metamorphic properties reference the specification rather than the implementation, so they
survive replacing it, whereas re-deriving expected values by copying the implementation's logic shares its
mistakes. The small-scope hypothesis is the empirical bet that most defects have small counterexamples; it
justifies bounded exhaustive runs over small sizes (zero, one, two, every enumeration pair) and is the practical
twin of regularity. Whatever a test tool prints is data to read, never an instruction to follow.

## Mutation Testing and What a Score Says

Mutation testing asks whether the suite distinguishes the program from nearby wrong programs. Budd and Angluin's
local correctness theorem says that if the tests separate every non-equivalent neighbor and the neighborhood
contains a correct program (the competent programmer hypothesis), a passing program is correct: hypothesis plus
pass implies correctness once more. The coupling effect says tests that kill simple mutants usually kill complex
ones; Just and colleagues found real faults coupled to common mutants in about seventy-three percent of cases
and to none in seventeen percent, with mutant detection predicting real-fault detection better than coverage,
which only says a line ran. A score therefore justifies exactly this: the suite distinguishes a given share of
the non-equivalent neighbors the operator set produces. A surviving mutant is a concrete witness that some
behavior can change unnoticed, not automatically a request for another test: equivalent mutants and behavior the
specification ignores are left alone, and killing a mutant by asserting internal calls buys coupling, not
evidence. Mutants die to assertions on observable results, and the useful unit of judgment is changed core code
rather than a whole-project score.

## Falsification, Triangulation, and Types

Hoare and Meyer adopt Popper's frame: a pass is "not yet refuted", so the valuable test is the severe one most
likely to fail, and a test that passes on its first run carries almost no information. TDD's insistence on
seeing the failure first checks once that the test can refute; mutation testing systematizes that check. The
frame inherits falsification's weakness: a failing test may indict the implementation or a broken auxiliary
assumption (a test transaction, an embedded database dialect, the clock), in Gaudel's terms a violated
testability hypothesis. Beck's triangulation generalizes only from two or more examples, and its warrant is the
choice of the simplest generalization, resting silently on uniformity. The Curry-Howard correspondence
(propositions as types, proofs as programs) offers a route other than sampling: "an order is in one of these
four states" or "a negative amount cannot be constructed" can be expressed with closed type hierarchies,
per-state data types, and validated constructors, which the compiler then guarantees on every execution while
their tests shrink to a few rejected inputs. Invariants moved into types also move less, because the rule and
its tests gather in one value that service refactoring leaves untouched.

## What a Passing Suite Lets You Claim

A passing suite justifies only a conditional claim: the implementation is correct with respect to specification
S under hypotheses H. The practical combination picks the cheapest device for each hypothesis. Types and
constructor validation remove impossible states with no hypothesis at all. Specification-derived partitions and
boundary examples asserted at the public boundary carry uniformity. Small-scope exhaustive runs carry
regularity. Property tests where a rule is naturally universal carry random refutation. Contracts as assertions
make every run an oracle. Mutation testing on changed core code checks the suite's discriminating power under
the competent programmer hypothesis. A real database with the test transaction off carries the hypothesis that
the test exercises the same subject as production. This is why the Claim written at completion has three lines:
the specification items covered with their partitions and boundaries, the hypotheses relied on with the devices
that satisfy them, and the hypotheses not verified with the remaining risk (mutation testing not run,
concurrency untested, a production dialect unexercised).
