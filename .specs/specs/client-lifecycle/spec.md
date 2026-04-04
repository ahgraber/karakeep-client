# Client Lifecycle Specification

> Generated from code analysis on 2026-03-29
> Source files: src/karakeep_client/karakeep.py, src/karakeep_client/**init**.py

## Purpose

Define how the KarakeepClient is constructed, authenticated, manages its underlying HTTP connection, and cleans up resources.
Covers both context-manager and manual lifecycle patterns.

## Requirements

### Requirement: Authenticate via API key

The client SHALL require an API key provided either as a constructor argument or via the `KARAKEEP_API_KEY` environment variable.

#### Scenario: API key provided as constructor argument

- **GIVEN** a caller provides an `api_key` argument to the constructor
- **WHEN** the client is instantiated
- **THEN** the client uses the provided API key for all subsequent requests

#### Scenario: API key from environment variable

- **GIVEN** no `api_key` argument is provided and `KARAKEEP_API_KEY` is set in the environment
- **WHEN** the client is instantiated
- **THEN** the client uses the environment variable value as the API key

#### Scenario: No API key available

- **GIVEN** no `api_key` argument is provided and `KARAKEEP_API_KEY` is not set
- **WHEN** the client is instantiated
- **THEN** the client SHALL raise a `ValueError`

### Requirement: Require base URL for API target

The client SHALL require a base URL provided either as a constructor argument or via the `KARAKEEP_BASE_URL` environment variable.

#### Scenario: Base URL provided as constructor argument

- **GIVEN** a caller provides a `base_url` argument to the constructor
- **WHEN** the client is instantiated
- **THEN** the client derives its API endpoint base from the provided URL

#### Scenario: No base URL available

- **GIVEN** no `base_url` argument is provided and `KARAKEEP_BASE_URL` is not set
- **WHEN** the client is instantiated
- **THEN** the client SHALL raise a `ValueError`

### Requirement: Support async context manager lifecycle

The client SHALL support use as an async context manager that creates a reusable HTTP connection on entry and closes it on exit.

#### Scenario: Async context manager creates and closes connection

- **GIVEN** a configured client instance
- **WHEN** the client is used as an `async with` context manager
- **THEN** a reusable HTTP client is created on entry and closed on exit

### Requirement: Support explicit connection management

The client SHALL support explicit `create()` for reusable connection setup and `aclose()` for async teardown outside of a context manager.

#### Scenario: Explicit create and close

- **GIVEN** a configured client instance not used as a context manager
- **WHEN** the caller invokes `create()` followed later by `aclose()`
- **THEN** a reusable HTTP client is created and then closed

#### Scenario: Create reuses existing connection

- **GIVEN** `create()` has already been called
- **WHEN** `create()` is called again
- **THEN** the same HTTP client instance is returned without creating a new one

### Requirement: Support synchronous close when no event loop is running

The client SHALL provide a synchronous `close()` method that tears down the connection when no event loop is running, and raises `RuntimeError` if an event loop is active.

#### Scenario: Synchronous close outside event loop

- **GIVEN** a client with an active connection and no running event loop
- **WHEN** `close()` is called
- **THEN** the connection is closed synchronously

#### Scenario: Synchronous close inside event loop

- **GIVEN** a client with an active connection and a running event loop
- **WHEN** `close()` is called
- **THEN** a `RuntimeError` is raised

### Requirement: Use temporary connections for one-off requests

The client SHALL create and dispose of a temporary HTTP connection for API calls made without a prior `create()` or context manager entry.

#### Scenario: One-off request without stored connection

- **GIVEN** a client with no stored connection (no `create()` or context manager)
- **WHEN** an API method is called
- **THEN** a temporary HTTP client is created, used, and closed for that single request

## Technical Notes

- **Implementation**: `src/karakeep_client/karakeep.py` — `KarakeepClient.__init__`, `__aenter__`, `__aexit__`, `create`, `aclose`, `close`, `_ensure_client`, `_call`
- **Dependencies**: none
- **Schema reference**: karakeep-api.json `securitySchemes.bearerAuth` — all endpoints require `Authorization: Bearer {token}`; 401 response on invalid/missing token
