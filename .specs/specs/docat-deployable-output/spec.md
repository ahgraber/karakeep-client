# Docat Deployable Output Specification

> Translated from openspec on 2026-03-29
> Source: openspec/specs/docat-deployable-output/spec.md

## Purpose

Ensure the documentation workflow produces a built static artifact suitable for upload to a self-hosted Docat instance, and that the delivery path is documented for maintainers.

## Requirements

### Requirement: Produce Docat-uploadable documentation artifact

The documentation workflow SHALL produce a built static artifact derived from the MkDocs output that is suitable for upload to a self-hosted Docat instance.

#### Scenario: Built docs artifact is available for upload

- **GIVEN** the MkDocs documentation build has completed successfully
- **WHEN** the documented docs packaging workflow completes
- **THEN** maintainers can locate a single uploadable docs artifact produced from the built static site

### Requirement: Document Docat delivery path

The repository documentation SHALL describe the output location and handoff steps required to upload the built docs artifact to a self-hosted Docat deployment.

#### Scenario: Maintainer follows Docat handoff instructions

- **GIVEN** a maintainer needs to publish documentation to Docat
- **WHEN** the maintainer follows the repository documentation for docs delivery
- **THEN** they can identify the artifact and the intended Docat upload handoff without inspecting source code

## Technical Notes

- **Implementation**: `README.md` docs build section, MkDocs build output directory
- **Dependencies**: api-reference-docs-site (the artifact is produced by the docs build)
