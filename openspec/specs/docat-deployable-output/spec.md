# docat-deployable-output

## Purpose

TBD

## Requirements

### Requirement: Produce Docat-uploadable documentation artifact

The documentation workflow MUST produce a built static artifact derived from the MkDocs output that is suitable for upload to a self-hosted Docat instance.

#### Scenario: Built docs artifact is available for upload

- **WHEN** the documented docs packaging/build workflow completes
- **THEN** maintainers can locate a single uploadable docs artifact produced from the built static site

### Requirement: Document Docat delivery path

The repository documentation MUST describe the output location and handoff steps required to upload the built docs artifact to a self-hosted Docat deployment.

#### Scenario: Maintainer follows Docat handoff instructions

- **WHEN** a maintainer follows the repository documentation for docs delivery
- **THEN** they can identify the artifact and the intended Docat upload handoff without inspecting source code
