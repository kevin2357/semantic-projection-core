# Release Engineering Sprint 1 Retrospective

## Outcome

SPC 0.10.0 moved from a source-checkout-oriented project to a reproducible,
installed-wheel-qualified private release without redesigning the projection
engine. The semantic architecture was already strong; most release work made
its package boundary, validation behavior, provenance, and supported consumer
contract explicit.

## Important surprises

- Context examples used successfully by repository tools were outside the
  installed package. The authoritative contexts now live in the package;
  repository examples are tested compatibility copies.
- Contract validation changed depth when `jsonschema` happened to be installed.
  Full validation is now an invariant runtime dependency.
- Declarative-resource hashes could not identify Python mapping and
  source-selection behavior. Runtime and profile-policy fingerprints now cover
  executable semantic policy.
- Clean Git archives normalized line endings and therefore produced different
  packaged byte hashes from checkout-built candidates. Parsed JSON semantics
  matched, but the difference was correctly treated as release-provenance drift
  and final installed QA was rerun against the reproducible archive-built wheel.
- Ella's original canonical package was unavailable. Qualification did not
  reconstruct upstream truth from downstream artifacts; it used AGF's complete
  checked-in Kevin fixture instead.
- GitHub's release object was not platform-immutable and the annotated tag was
  unsigned. The release makes no stronger claim: consumer immutability rests on
  the non-moving tag and exact wheel SHA-256 pin.

## What was more direct than expected

- Static, temporal, and synastry execution already shared a coherent generic
  engine and profile model. Packaging and provenance could be added without
  splitting or rewriting the semantic compiler.
- Existing deterministic IDs, registries, receipts, schemas, and source lineage
  made exact installed-runtime QA and the AGF-to-SPC-to-SBE proof tractable.
- SBE accepted all four exact Woofmapping contexts once the installed artifact
  boundary was made explicit; no reader-facing prose run was required to prove
  semantic compatibility.

## Durable decisions promoted from the log

- [Executable semantic policy is part of release identity](../../../../../decisions/ADR-0001%20-%20Include%20Executable%20Semantic%20Policy%20in%20Release%20Identity.md).
- [Full schema validation is mandatory runtime behavior](../../../../../decisions/ADR-0002%20-%20Require%20Invariant%20Full%20Schema%20Validation%20at%20Runtime.md).
- [Qualification evidence and publication receipts are separate artifacts](../../../../../decisions/ADR-0003%20-%20Separate%20Qualification%20Evidence%20from%20Publication%20Receipts.md).

## Remaining boundaries

- AGF still needs to replace its permissive SPC dependency and internal mapping
  imports in any production orchestration path.
- The AstroWoof API must install and smoke-test the exact wheel in its target
  Linux image; release publication is not deployment qualification.
- Reproducible build controls are documented and evidenced but not yet automated
  as a single maintained release command.
- Cryptographically signed tags or GitHub's platform immutability feature may be
  adopted later, but are not properties of the 0.10.0 release.

## AstroWoof project reconciliation

An end-of-day comparison with the project control plane confirmed SPC's
component boundaries and corrected two stale project assumptions: the four
exact Woofmapping natal contexts are now a formal 0.10.0 compatibility set, and
native artifacts now embed a profile-policy fingerprint within the complete
runtime identity. In the reverse direction, the project establishes `full` as
AstroWoof's conservative initial SBE materialization. SPC continues to support
all row-bearing modes, but its consumer handoff now distinguishes that native
capability from the downstream project choice.
