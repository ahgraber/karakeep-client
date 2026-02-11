# tasks

## 1. Docs Toolchain Setup

- [x] 1.1 Add MkDocs, Material, and mkdocstrings dependencies in project configuration for reproducible docs builds.
- [x] 1.2 Add repository docs configuration (`mkdocs.yml`) with navigation, Material theme, and mkdocstrings Python handler.
- [x] 1.3 Add baseline docs content structure (home/overview and API reference entry pages) aligned to package modules.

## 2. API Reference Site Implementation

- [x] 2.1 Configure mkdocstrings directives to render public API surfaces for `karakeep_client.karakeep` and `karakeep_client.models`.
- [x] 2.2 Ensure generated site output path is deterministic and documented for local builds.
- [x] 2.3 Verify built documentation includes API reference navigation entries for client and model modules.

## 3. Docstring Compliance Updates

- [x] 3.1 Audit public modules/classes/functions in `src/karakeep_client` for Google-style docstring compliance gaps.
- [x] 3.2 Update non-compliant public docstrings to consistent Google-style sections (Args/Returns/Raises) matching runtime behavior.
- [x] 3.3 Validate generated API pages render docstring sections without malformed formatting.

## 4. Demo Documentation Readiness

- [x] 4.1 Review `notebooks/karakeep_client_demo.py` for notebook-only patterns and placeholder inputs that can mislead users.
- [x] 4.2 Update demo documentation presentation to state env var and async execution assumptions.
- [x] 4.3 Add clear caveats or adapted runnable guidance for non-notebook execution contexts.

## 5. Docat-Deployable Artifact Path

- [x] 5.1 Define the deliverable as a built static docs artifact produced from the MkDocs build output.
- [x] 5.2 Add repository instructions describing artifact location and upload handoff expectations for self-hosted Docat.
- [x] 5.3 Confirm the documented workflow yields a single, identifiable artifact suitable for Docat upload.

## 6. Documentation and Verification

- [x] 6.1 Update `README.md` with concise docs build/serve instructions for contributors.
- [x] 6.2 Run project tests needed to confirm no runtime behavior regressions from documentation-focused changes.
- [x] 6.3 Build docs end-to-end and verify all required sections (API reference, demo guidance, Docat handoff) are present.
