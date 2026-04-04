# Design: align-build-autodoc

## Context

`karakeep-client` is an async Python package (`src/karakeep_client`) with public client APIs in `karakeep.py` and API/data contracts in `models.py`.
The repository has user-facing usage guidance in `README.md` and a demo script in `notebooks/karakeep_client_demo.py`, but no reproducible documentation build pipeline and incomplete docstring coverage for generated API reference.

The change introduces documentation infrastructure and documentation-quality requirements without changing bookmark/asset/tag/search runtime behavior.
Constraints: Python 3.12+, uv-managed dependencies, Google-style docstrings for public APIs, no unnecessary feature expansion.

## Decisions

### Decision: MkDocs + Material + mkdocstrings as sole docs stack

**Chosen:** Configure a single documentation site with MkDocs as the builder, Material as the theme, and mkdocstrings (Python handler) for API reference extraction.

**Rationale:** Matches requested tooling, minimizes custom glue code, keeps docs generation close to source definitions.

**Alternatives considered:**

- Sphinx/autodoc: mature but outside requested stack, would require a parallel docs architecture
- Hand-written Markdown-only: lower setup cost but drifts from source and does not scale for API coverage

### Decision: Scope API reference to public surfaces only

**Chosen:** Reference generation targets public package modules and exported symbols, preserving existing module boundaries.

**Rationale:** Avoids documenting tests/internal scaffolding, keeps output relevant for integrators.

**Alternatives considered:**

- Include all modules automatically: risks exposing internals/noise
- Curate only selected methods: simpler initially but brittle

### Decision: Normalize docstrings before depending on generated reference

**Chosen:** Treat docstring normalization as first-class scope, including module/class/function docstrings.

**Rationale:** mkdocstrings quality depends directly on source docstrings; improving consistency reduces ambiguity.

**Alternatives considered:**

- Leave existing docstrings as-is: produces inconsistent rendered docs
- Add separate manual docs: duplicates effort and increases drift risk

### Decision: Demo as guided examples with caveats, not runnable notebook export

**Chosen:** Use demo script in docs as curated examples with explicit caveats; update where placeholders or notebook-only patterns would mislead.

**Rationale:** Current file includes top-level await assumptions and placeholder values; publishing verbatim would create false expectations.

**Alternatives considered:**

- Exclude demo entirely: avoids risk but loses onboarding value
- Full notebook execution pipeline: higher complexity than needed

### Decision: Preserve backward compatibility

**Chosen:** Documentation work must not modify runtime method signatures, env var names, or response model contracts.

**Rationale:** This is a documentation-alignment change, not an API revision.

## Risks

- **Added docs dependencies increase maintenance surface**: Confine to documentation config and pin via existing uv dependency workflow
- **Generated reference may include noisy internals**: Explicitly scope reference pages to public modules/symbols
- **Docstring updates may accidentally change behavioral expectations**: Keep edits descriptive and non-semantic; avoid changing code behavior
- **Demo content could still be interpreted as fully executable**: Label execution assumptions and ensure placeholders are clearly marked
