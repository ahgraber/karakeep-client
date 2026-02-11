# align-build-autodoc

## Context

`karakeep-client` is an async Python package (`src/karakeep_client`) with public client APIs in `karakeep.py` and API/data contracts in `models.py`. The current repository has user-facing usage guidance in `README.md` and a demo script in `notebooks/karakeep_client_demo.py`, but no reproducible documentation build pipeline and incomplete docstring coverage for generated API reference.

The change introduces documentation infrastructure and documentation-quality requirements without changing bookmark/asset/tag/search runtime behavior. Constraints from project conventions apply: Python 3.12+, uv-managed dependencies, Google-style docstrings for public APIs, and no unnecessary feature expansion.

## Goals / Non-Goals

**Goals:**

- Add a deterministic docs build path using MkDocs + Material + mkdocstrings.
- Ensure public modules/classes/functions are documented with Google-style docstrings suitable for API reference rendering.
- Define how the existing demo script is surfaced in docs so examples are accurate and not misleading.
- Document local docs build commands in repository documentation.

**Non-Goals:**

- Changing runtime API semantics, request/response models, or method signatures.
- Adding new product features to bookmark/asset/tag/search flows.
- Introducing notebook execution infrastructure (Jupyter build tooling, CI notebook runners) unless required by follow-up scope.

## Decisions

### 1. Use MkDocs + Material + mkdocstrings as the only docs generation stack

- Decision: Configure a single documentation site with MkDocs as the builder, Material as the theme, and mkdocstrings (Python handler) for API reference extraction from source.
- Rationale: Matches requested tooling, minimizes custom glue code, and keeps docs generation close to source definitions.
- Alternatives considered:
  - Sphinx/autodoc: mature but outside requested stack and would require a parallel docs architecture.
  - Hand-written Markdown-only docs: lower setup cost but drifts from source and does not scale for API coverage.

### 2. Keep API reference scope aligned to `src/karakeep_client` public surfaces

- Decision: Reference generation targets public package modules and exported symbols, while preserving existing module boundaries (`karakeep.py`, `models.py`, package init).
- Rationale: Avoids documenting tests/internal scaffolding and keeps output relevant for integrators.
- Alternatives considered:
  - Include all modules automatically: risks exposing internals/noise.
  - Curate only selected methods: simpler initially but brittle and easy to forget during evolution.

### 3. Normalize docstrings to Google style before depending on generated reference

- Decision: Treat docstring normalization as first-class design scope, including module/class/function docstrings for public interfaces.
- Rationale: mkdocstrings quality depends directly on source docstrings; improving consistency reduces ambiguity and future maintenance burden.
- Alternatives considered:
  - Leave existing docstrings as-is: produces inconsistent rendered docs and lower trust.
  - Add separate manual docs instead of fixing docstrings: duplicates documentation effort and increases drift risk.

### 4. Document demo script as a guided example, not as a guaranteed runnable notebook export

- Decision: Use `notebooks/karakeep_client_demo.py` in docs as curated examples with explicit caveats; update content where placeholders or notebook-only patterns would mislead users.
- Rationale: Current file includes top-level await assumptions and placeholder values; publishing it verbatim as runnable documentation would create false expectations.
- Alternatives considered:
  - Exclude demo entirely: avoids risk but loses practical onboarding value.
  - Fully convert to notebook execution docs pipeline now: higher complexity than needed for this change.

### 5. Preserve backward compatibility for client and model contracts

- Decision: Documentation work must not modify runtime method signatures, env var names, or response model contracts.
- Rationale: This is a documentation-alignment change, not an API revision.
- Alternatives considered:
  - Fold API cleanup into this effort: tempting but violates scope and increases regression risk.

## Risks / Trade-offs

- [Risk] Added docs dependencies increase maintenance surface. -> Mitigation: confine to documentation config and pin via existing uv dependency workflow.
- [Risk] Generated reference may include noisy internals if selection is too broad. -> Mitigation: explicitly scope reference pages to public modules/symbols.
- [Risk] Docstring updates may accidentally change wording of behavioral expectations. -> Mitigation: keep docstring edits descriptive and non-semantic; avoid changing code behavior.
- [Risk] Demo content could still be interpreted as fully executable in all contexts. -> Mitigation: label execution assumptions and ensure placeholders are clearly marked or replaced with safe examples.

## Migration Plan

1. Introduce docs configuration and dependency wiring.
2. Add docs structure/pages and API reference directives.
3. Update public docstrings for rendering quality and consistency.
4. Adjust demo documentation presentation for clarity.
5. Add README docs build/serve instructions.

Rollback strategy:

- Revert docs config/pages and dependency additions as a single change set.
- Runtime client behavior remains unchanged, so rollback affects docs availability only.

## Open Questions

- Should docs include only API reference + quickstart, or also a dedicated tutorial page derived from demo flows?
- Should demo examples be split into "runnable script" and "notebook-style" variants for clearer expectations?
