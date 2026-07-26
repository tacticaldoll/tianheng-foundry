## ADDED Requirements

### Requirement: The skill activates narrowly
The `forge-law` skill description SHALL target agents adding or changing normative architecture
prose in a Rust project that uses Tianheng, or agents explicitly asked to adopt Tianheng. It SHALL
exclude non-Rust repositories, generic documentation, architecture-policy invention, and implicit
amendment of accepted law.

#### Scenario: A Rust Tianheng claim is eligible for inspection
- **WHEN** an agent is asked to replace a declared Rust architecture constraint with enforceable
  governance in a project that already uses Tianheng
- **THEN** the skill is eligible to activate and proceeds to structural eligibility checks

#### Scenario: Generic documentation does not activate generation
- **WHEN** an agent is writing explanatory documentation without a declared structural constraint
- **THEN** the skill does not treat that work as a Tianheng law-generation request

### Requirement: Structural eligibility gates every write
Before editing, the workflow SHALL discover a Cargo workspace root and SHALL confirm either an
existing Tianheng dependency or law source, or an explicit user request for first adoption. It
SHALL constrain candidate edits to the Cargo workspace subtree and SHALL stop without writing in a
non-Rust repository. A mixed-language monorepo SHALL NOT cause the workflow to claim governance
outside the discovered Cargo workspace.

#### Scenario: Existing Tianheng workspace passes eligibility
- **WHEN** a Cargo workspace contains a supported Tianheng dependency or existing Constitution
- **THEN** the workflow may inspect claims and candidate edit locations within that workspace

#### Scenario: Generic Rust workspace is not silently enrolled
- **WHEN** a Cargo workspace does not use Tianheng and the user did not request adoption
- **THEN** the workflow stops before editing and reports that Tianheng qualification is absent

#### Scenario: Mixed-language scope stays local
- **WHEN** a Cargo workspace is nested inside a larger mixed-language monorepo
- **THEN** the workflow limits its observation and edits to the Cargo workspace and states that
  cross-language claims remain outside the reaction perimeter

### Requirement: Only declared observable intent is admitted
The workflow SHALL cite project prose or direct human instruction as the authority for a candidate
claim. It SHALL classify the claim as structural, process, judgment, historical rationale, or API
explanation. Only a structural claim that maps to a real Tianheng observation source, target, and
supported rule SHALL proceed to generation. The workflow MUST narrow, clarify, or decline any claim
whose meaning exceeds the available observation perimeter.

#### Scenario: Observable structural intent is admitted
- **WHEN** project documentation declares that one Rust crate may depend only on a named set of
  crates and Cargo metadata exposes those declarations
- **THEN** the workflow records the intent source, observable fact, target, rule family, and
  perimeter before editing

#### Scenario: Subjective preference is declined
- **WHEN** prose says that a module must remain easy to maintain
- **THEN** the workflow declines Tianheng generation because no supported observation source
  measures maintainability

#### Scenario: Repository shape does not invent policy
- **WHEN** the repository happens to have layered crate names but no project or human statement
  declaring a dependency rule
- **THEN** the workflow does not infer and generate a layer law from naming alone

### Requirement: Recipe selection preserves observation honesty
The skill SHALL select recipes by observable architectural fact rather than architecture-fashion
labels. Each recipe reference SHALL identify its observation source, representative Tianheng
surface, required inputs, and explicit non-observations. A generated forward-looking reason SHALL
make no structural claim outside that perimeter.

#### Scenario: Fashion label is decomposed
- **WHEN** a user asks to keep a core "clean" or "hexagonal"
- **THEN** the workflow asks or infers from declared evidence which dependency, import, semantic
  exposure, clock, async, unsafe, or runtime-origin facts are actually intended

#### Scenario: Reason remains within the selected rule
- **WHEN** a manifest dependency rule is selected
- **THEN** the generated reason describes declared dependency direction and does not claim runtime
  call-graph or cross-language isolation

### Requirement: Candidate law includes bidirectional reaction proof
For every generated boundary candidate, the workflow SHALL establish an enforced violating case
and a clean precision case using the adopter repository's existing test conventions where
available. It SHALL record the commands and expected outcomes. A declaration that merely compiles,
projects, warns, or is fully baselined SHALL NOT count as proof that the new boundary reacts.

#### Scenario: Violating case proves teeth
- **WHEN** the candidate's governed fact is present in a focused violating fixture or case
- **THEN** the selected Tianheng evaluator reports an enforced violation or exit class `1`

#### Scenario: Clean case proves precision
- **WHEN** the governed fact is absent from a focused clean fixture or case
- **THEN** the selected Tianheng evaluator remains clean rather than reacting to unrelated code

#### Scenario: Failed proof is not suppressed
- **WHEN** candidate verification fails
- **THEN** the workflow repairs the candidate toward the declared reason or stops, and does not add
  warning severity, baseline the new fact, or weaken an accepted boundary merely to pass

### Requirement: Generated law remains a candidate
The workflow SHALL label generated edits and successful proofs as a `VerifiedCandidate`. It SHALL
NOT claim that tests, generation, or skill execution makes the candidate accepted project law.
Existing accepted law SHALL be changed only after an explicit amendment request.

#### Scenario: Successful generation preserves human authority
- **WHEN** candidate code and both reaction proofs succeed
- **THEN** the workflow reports a verified candidate awaiting human review

#### Scenario: Existing law is not silently weakened
- **WHEN** an accepted boundary blocks an unrelated requested change
- **THEN** the workflow stops the automatic materialization path and requires an explicit amendment
  decision rather than modifying the boundary

### Requirement: Prose disposition preserves distinct authority
The workflow SHALL classify source prose before proposing its disposition. Redundant normative
prose MAY be removed only after the reaction-proven candidate is accepted and covers the same
claim. Historical rationale, process rules, judgment, and API explanation SHALL remain in or move
to their appropriate authority surface. Partial observation coverage SHALL result in narrowed
prose rather than wholesale deletion.

#### Scenario: Fully reacted prose can dissolve
- **WHEN** an accepted boundary and its fresh projection carry the entire live structural claim
- **THEN** the workflow may remove the hand-maintained duplicate or replace it with a pointer to the
  generated law

#### Scenario: Historical rationale survives conversion
- **WHEN** a prose paragraph combines a live structural rule with the history behind it
- **THEN** the live rule moves to the boundary reason while the historical rationale remains in the
  project's decision or commit-history surface

### Requirement: Distribution and compatibility remain explicit
The repository SHALL package `forge-law` through host-neutral skill files and host-specific root
manifests. It SHALL declare its supported Tianheng line, use no git submodules, and provide
network-free repository, scenario, and optional local-source compatibility validation.

#### Scenario: Portable skill validates
- **WHEN** repository validation runs
- **THEN** every declared host manifest points to the same skill collection and the skill metadata,
  linked references, scenario corpus, and compatibility declaration are internally consistent

#### Scenario: Local Tianheng source validates representative vocabulary
- **WHEN** a compatible Tianheng checkout is supplied through the documented local-source input
- **THEN** the representative consumer fixture compiles against that source without cloning,
  downloading, or vendoring Tianheng
