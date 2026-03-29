# Demo Doc Readiness Specification

> Translated from openspec on 2026-03-29
> Source: openspec/specs/demo-doc-readiness/spec.md

## Purpose

Define how the demo script (`notebooks/karakeep_client_demo.py`) is represented in documentation so that examples are accurate, understandable, and appropriate for users in both notebook and non-notebook execution contexts.

## Requirements

### Requirement: Demo documentation states execution assumptions

Documentation that uses content from `notebooks/karakeep_client_demo.py` MUST explicitly state execution assumptions, including required environment variables and async execution context.

#### Scenario: User reads demo setup guidance

- **GIVEN** a user is reading demo-related documentation
- **WHEN** the user opens demo-related documentation
- **THEN** they can see required `KARAKEEP_API_KEY` and `KARAKEEP_BASE_URL` configuration and async execution prerequisites

### Requirement: Demo examples handle notebook-only patterns clearly

Demo documentation MUST clearly identify notebook-oriented patterns (such as top-level `await`) and provide either caveats or adapted runnable examples for non-notebook execution contexts.

#### Scenario: Non-notebook user follows demo documentation

- **GIVEN** a user is running demo guidance outside a notebook environment
- **WHEN** the user runs demo guidance outside a notebook environment
- **THEN** the documentation either provides an adapted runnable pattern or clearly warns that the shown snippet is notebook-only

### Requirement: Placeholder values are not presented as directly runnable

Documentation derived from demo code MUST mark placeholder values and incomplete inputs so users do not treat them as production-ready commands.

#### Scenario: User encounters placeholder-based example

- **GIVEN** a demo section includes placeholders such as file paths or source URLs
- **WHEN** the user encounters the placeholder-based example
- **THEN** the documentation labels the placeholders and indicates the concrete values users must supply

## Technical Notes

- **Implementation**: `notebooks/karakeep_client_demo.py`, docs content pages
- **Dependencies**: api-reference-docs-site (demo content is part of the docs site)
