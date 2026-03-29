# Tasks: align-build-autodoc

## Docs Toolchain Setup

- [x] Add MkDocs, Material, and mkdocstrings dependencies in project configuration
- [x] Add `mkdocs.yml` with navigation, Material theme, and mkdocstrings Python handler
- [x] Add baseline docs content structure (home/overview and API reference entry pages)

## API Reference Site Implementation

- [x] Configure mkdocstrings directives for `karakeep_client.karakeep` and `karakeep_client.models`
- [x] Ensure generated site output path is deterministic and documented
- [x] Verify built documentation includes API reference navigation entries

## Docstring Compliance Updates

- [x] Audit public modules/classes/functions for Google-style docstring compliance gaps
- [x] Update non-compliant public docstrings to consistent Google-style sections
- [x] Validate generated API pages render docstring sections without malformed formatting

## Demo Documentation Readiness

- [x] Review demo script for notebook-only patterns and placeholder inputs
- [x] Update demo documentation to state env var and async execution assumptions
- [x] Add caveats or adapted runnable guidance for non-notebook contexts

## Docat-Deployable Artifact Path

- [x] Define deliverable as a built static docs artifact from MkDocs build output
- [x] Add repository instructions for artifact location and Docat upload handoff
- [x] Confirm documented workflow yields a single identifiable artifact for Docat

## Documentation and Verification

- [x] Update `README.md` with docs build/serve instructions
- [x] Run tests to confirm no runtime behavior regressions
- [x] Build docs end-to-end and verify all required sections are present
