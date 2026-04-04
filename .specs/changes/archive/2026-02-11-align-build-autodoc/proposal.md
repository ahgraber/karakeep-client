# Proposal: align-build-autodoc

## Intent

The repository has no formal documentation build pipeline and inconsistent API docstring coverage, making onboarding and API discovery harder than necessary.
Establishing MkDocs + Material + mkdocstrings aligns published documentation with the actual Python client surface and reduces integration friction.

## Scope

**In scope:**

- Documentation capability that builds a browsable docs site using MkDocs, Material, and mkdocstrings
- Delivery output defined as a built static artifact uploadable to a self-hosted Docat instance
- Google-style docstring compliance for public modules, classes, and functions
- Demo script documentation presentation with execution assumptions and placeholder clarity
- Developer-facing docs build instructions in repository documentation
- No runtime API behavior changes

**Out of scope:**

- Changing runtime API semantics, request/response models, or method signatures
- Adding new product features to bookmark/asset/tag/search flows
- Introducing notebook execution infrastructure (Jupyter build tooling, CI notebook runners)
