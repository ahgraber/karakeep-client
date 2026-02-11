# demo-doc-readiness

## ADDED Requirements

### Requirement: Demo documentation states execution assumptions

Documentation that uses content from `notebooks/karakeep_client_demo.py` MUST explicitly state execution assumptions, including required environment variables and async execution context.

#### Scenario: User reads demo setup guidance

- **WHEN** a user opens demo-related documentation
- **THEN** they can see required `KARAKEEP_API_KEY` and `KARAKEEP_BASE_URL` configuration and async execution prerequisites

### Requirement: Demo examples handle notebook-only patterns clearly

Demo documentation MUST clearly identify notebook-oriented patterns (such as top-level `await`) and provide either caveats or adapted runnable examples for non-notebook execution contexts.

#### Scenario: Non-notebook user follows demo documentation

- **WHEN** a user runs demo guidance outside a notebook environment
- **THEN** the documentation either provides an adapted runnable pattern or clearly warns that the shown snippet is notebook-only

### Requirement: Placeholder values are not presented as directly runnable

Documentation derived from demo code MUST mark placeholder values and incomplete inputs so users do not treat them as production-ready commands.

#### Scenario: User encounters placeholder-based example

- **WHEN** a demo section includes placeholders such as file paths or source URLs
- **THEN** the documentation labels the placeholders and indicates the concrete values users must supply
