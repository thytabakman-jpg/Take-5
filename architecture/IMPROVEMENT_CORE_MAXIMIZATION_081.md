# ImprovementCore Maximization 081

Date: 2026-09-26
Status: IMPLEMENTED STRICT-GAIN CANDIDATE / VALIDATION REQUIRED
Canonical repository: Take-5

## Governing job

Re-evaluate the current ImprovementCore using the full current conversation and
cross-repository lineage, then change Take-5 only where recovered behavior
demonstrates strict gain over the current controller path.

## Evidence used

- current Take-5 rich manager and dispatch
- Take-5 usage audit 078
- cross-repository lineage choice 080
- Reaserch current ImprovementCore mathematical state
- Reaserch IC-030 recursive manager
- Reaserch learning-memory runtime
- Take-2 surface/transition discipline
- Take-3 strict-gain admission rule
- Take-4 cumulative autonomous controller goal

## Strict-gain dispositions

### Parent-owned recursive ImprovementCore delegation
Disposition: STRICT_GAIN

Why:
Take-5's IC-028 operator already performs recursive stage reentry, but it did not
provide the explicit parent-child contract recovered in IC-030:

parent selects child job
-> child executes
-> child result returns
-> parent admits/rejects/reconciles
-> parent updates
-> parent reselects/reenters.

Imported as:
runtime/improvement_core_recursive_manager.py

Protected anti-regression:
a live continuation cannot silently end because no next child/action was selected.
A child return without continuation-relevant delta cannot count as progress.

### Basis-relative learning / NoGain memory
Disposition: STRICT_GAIN

Why:
current Take-5 reentry protects continuation but does not itself preserve a typed
memory that blocks unchanged NO_GAIN / REJECTED / FAILED routes relative to their
dependency footprints.

Imported as:
runtime/improvement_core_learning_memory.py

A route reopens only when a changed coordinate intersects its recorded dependency
footprint.

### Cumulative-autonomous regime surface
Disposition: STRICT_GAIN AS COMPOSITION

Imported as:
runtime/improvement_core_regime.py

This is deliberately a composition surface rather than a new controller ontology.
It identifies the current regime as:

- rich IC-028 stage manager
- recursive parent/child manager
- basis-relative learning memory

The user-facing dispatcher now resolves ordinary ImproveCore invocation to this
regime surface.

### Zero-request / upstream discovery
Disposition: OPEN

The semantic behavior is materially valuable:
corpus-first observation and relation generation can change the candidate job universe
before a substantive job is supplied.

It is not promoted in this change because the Reaserch source itself records:
- complete relation-generator basis OPEN
- exact relation-admission semantics OPEN
- zero-request host input boundary OPEN
- prospective holdouts OPEN.

Take-3 strict-gain discipline therefore blocks premature runtime promotion.

### Full-autonomy effectiveness profile
Disposition: PARTIALLY RECONSTRUCTED / OPEN

Current Take-5 now reconstructs more of the profile:
- manager-owned control
- inquiry/work generation
- rich execution/admission/persistence/reentry
- recursive child management
- learning/no-gain memory
- canonical user dispatch

Still OPEN:
- validated zero-request upstream discovery
- evidence that the full materially distinct repertoire is reachable in the desired way
- historical matched replays
- unlike prospective autonomy holdouts
- empirical cheap-route versus broad-attack behavior
- global host interception.

## Mathematical organization

The current improvement does not replace the recovered abstract controller:

C_(J,K) = <Z,D,A_(J,K),pi_(J,K),T_(J,K),Tau_(J,K)>.

It strengthens the configured realization:

L0
endogenous continuation control

L1
observer/inquiry/execution/admission/integration/persistence/verification/reentry

L2
invocation/self-management envelope

L3
basis-relative learning memory and recursive parent/child realization.

L3 is a realization layer, not a new primitive mathematical kernel.

## Take-2 / Take-3 guards

No new standalone repository or large registry was created.

The new regime is a composition over existing and recovered components.

This satisfies the Take-2 preference for views/compositions before new operating
surfaces and the Take-3 rule that architecture enters only after demonstrated
result-sensitive failure or strict gain.

## Activation correction

Before this change:

ImproveCore invocation
-> rich manager entry.

After this change:

ImproveCore invocation
-> cumulative-autonomous regime
-> rich manager entry

with recursive self-management and learning-memory substrates now canonical parts of
the regime rather than historical orphan capabilities.

The generic stage invocation does not fabricate child jobs or route evidence when the
job does not supply them. Recursive delegation and learning memory remain available
to the parent regime and require typed inputs.

## Remaining gap

Repository activation is not universal host interception.

A host session that never loads the Take-5 dispatcher can still fail to invoke the
regime. That external boundary remains OPEN and must not be represented as solved.

## Closure status

STRICT_GAIN_IMPLEMENTATION = CANDIDATE
VALIDATION = REQUIRED
ZERO_REQUEST_DISCOVERY = OPEN
GLOBAL_IMPROVEMENTCORE_MAXIMALITY = OPEN
