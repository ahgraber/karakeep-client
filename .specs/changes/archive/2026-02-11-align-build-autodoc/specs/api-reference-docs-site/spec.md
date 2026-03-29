# Delta for API Reference Docs Site

## ADDED Requirements

### Requirement: Build static API documentation site

The project SHALL provide a documentation build that generates a static site from repository docs content and Python API reference extracted from `src/karakeep_client`.

#### Scenario: Successful local docs build

- **GIVEN** a developer has the docs dependencies installed
- **WHEN** the developer runs the documented docs build command
- **THEN** a static site artifact is generated in a predictable output directory

### Requirement: Include public Karakeep client API reference

The generated documentation site SHALL include API reference pages for public client interfaces in `karakeep_client.karakeep` and `karakeep_client.models`.

#### Scenario: API reference pages are present

- **GIVEN** the docs dependencies and source code are available
- **WHEN** the documentation site is built
- **THEN** the site navigation includes API reference entries for the public client and model modules
