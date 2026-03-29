# Client Lifecycle Specification

> Generated from code analysis on 2026-03-29
> Source files: src/karakeep_client/karakeep.py, src/karakeep_client/__init__.py

## Purpose

Define how the KarakeepClient is constructed, authenticated, manages its underlying HTTP connection, and cleans up resources. Covers both context-manager and manual lifecycle patterns.

## Requirements

### Requirement: Authenticate via API key

The client SHALL require an API key provided either as a constructor argument or via the `KARAKEEP_API_KEY` environment variable.

#### Scenario: API key provided as constructor argument

- __GIVEN__ a caller provides an `api_key` argument to the constructor
- __WHEN__ the client is instantiated
- __THEN__ the client uses the provided API key for all subsequent requests

#### Scenario: API key from environment variable

- __GIVEN__ no `api_key` argument is provided and `KARAKEEP_API_KEY` is set in the environment
- __WHEN__ the client is instantiated
- __THEN__ the client uses the environment variable value as the API key

#### Scenario: No API key available

- __GIVEN__ no `api_key` argument is provided and `KARAKEEP_API_KEY` is not set
- __WHEN__ the client is instantiated
- __THEN__ the client SHALL raise a `ValueError`

### Requirement: Require base URL for API target

The client SHALL require a base URL provided either as a constructor argument or via the `KARAKEEP_BASE_URL` environment variable.

#### Scenario: Base URL provided as constructor argument

- __GIVEN__ a caller provides a `base_url` argument to the constructor
- __WHEN__ the client is instantiated
- __THEN__ the client derives its API endpoint base from the provided URL

#### Scenario: No base URL available

- __GIVEN__ no `base_url` argument is provided and `KARAKEEP_BASE_URL` is not set
- __WHEN__ the client is instantiated
- __THEN__ the client SHALL raise a `ValueError`

### Requirement: Support async context manager lifecycle

The client SHALL support use as an async context manager that creates a reusable HTTP connection on entry and closes it on exit.

#### Scenario: Async context manager creates and closes connection

- __GIVEN__ a configured client instance
- __WHEN__ the client is used as an `async with` context manager
- __THEN__ a reusable HTTP client is created on entry and closed on exit

### Requirement: Support explicit connection management

The client SHALL support explicit `create()` for reusable connection setup and `aclose()` for async teardown outside of a context manager.

#### Scenario: Explicit create and close

- __GIVEN__ a configured client instance not used as a context manager
- __WHEN__ the caller invokes `create()` followed later by `aclose()`
- __THEN__ a reusable HTTP client is created and then closed

#### Scenario: Create reuses existing connection

- __GIVEN__ `create()` has already been called
- __WHEN__ `create()` is called again
- __THEN__ the same HTTP client instance is returned without creating a new one

### Requirement: Support synchronous close when no event loop is running

The client SHALL provide a synchronous `close()` method that tears down the connection when no event loop is running, and raises `RuntimeError` if an event loop is active.

#### Scenario: Synchronous close outside event loop

- __GIVEN__ a client with an active connection and no running event loop
- __WHEN__ `close()` is called
- __THEN__ the connection is closed synchronously

#### Scenario: Synchronous close inside event loop

- __GIVEN__ a client with an active connection and a running event loop
- __WHEN__ `close()` is called
- __THEN__ a `RuntimeError` is raised

### Requirement: Use temporary connections for one-off requests

The client SHALL create and dispose of a temporary HTTP connection for API calls made without a prior `create()` or context manager entry.

#### Scenario: One-off request without stored connection

- __GIVEN__ a client with no stored connection (no `create()` or context manager)
- __WHEN__ an API method is called
- __THEN__ a temporary HTTP client is created, used, and closed for that single request

## Technical Notes

- __Implementation__: `src/karakeep_client/karakeep.py` — `KarakeepClient.__init__`, `__aenter__`, `__aexit__`, `create`, `aclose`, `close`, `_ensure_client`, `_call`
- __Dependencies__: none
- __Schema reference__: karakeep-api.json `securitySchemes.bearerAuth` — all endpoints require `Authorization: Bearer {token}`; 401 response on invalid/missing token
