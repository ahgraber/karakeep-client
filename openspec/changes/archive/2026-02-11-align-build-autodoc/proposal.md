# proposal

## Why

The repository has no formal documentation build pipeline and inconsistent API docstring coverage, which makes onboarding and API discovery harder than it should be. Establishing MkDocs + Material + mkdocstrings now will align the published documentation with the actual Python client surface and reduce integration friction.

## What Changes

- Add a documentation capability that builds a browsable docs site for the async Karakeep client using MkDocs, Material, and mkdocstrings.
- Define the intended delivery output as a built static documentation artifact that can be uploaded to a self-hosted Docat instance.
- Define requirements for Google-style docstring compliance across public modules, classes, and functions so API reference output is complete and consistent.
- Define requirements for how `notebooks/karakeep_client_demo.py` is represented in docs (direct inclusion vs documented refactor path) to avoid publishing misleading or non-runnable examples.
- Add requirements for developer-facing docs build instructions in repository documentation.
- No intended runtime API behavior changes for bookmark, asset, tag, or search operations.

## Capabilities

### New Capabilities

- `api-reference-docs-site`: Build and structure a first-party documentation site that renders client API reference from source code.
- `docat-deployable-output`: Produce a built documentation artifact compatible with upload workflows for a self-hosted Docat instance.
- `docstring-compliance`: Standardize and enforce documentation-ready Google-style docstrings for public Python interfaces used by generated API docs.
- `demo-doc-readiness`: Define how the demo script is documented so examples are accurate, understandable, and appropriate for users.

### Modified Capabilities

- None.

## Impact

- Affected areas: `src/karakeep_client` public docstrings, docs configuration files, docs content files, and `README.md` documentation/build section.
- Tooling/dependencies: documentation toolchain additions for MkDocs, Material theme, and mkdocstrings, with output shaped for Docat upload.
- User impact: improved discoverability of bookmark/asset/tag/search APIs and clearer setup for local documentation builds.
- Compatibility: no breaking changes expected for existing client method signatures or request/response contracts.
