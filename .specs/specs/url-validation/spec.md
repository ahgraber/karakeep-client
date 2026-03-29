# URL Validation Specification

> Generated from code analysis on 2026-03-29
> Source files: src/karakeep_client/karakeep.py

## Purpose

Provide URL validation and normalization used by bookmark operations to ensure URLs are well-formed before API interaction and to enable URL-based bookmark matching despite superficial formatting differences.

## Requirements

### Requirement: Validate URL format

The system SHALL validate URLs against a defined regex pattern and Pydantic's `HttpUrl` type, rejecting empty, blank, or malformed URLs.

#### Scenario: Valid URL passes validation

- **GIVEN** a well-formed HTTP or HTTPS URL
- **WHEN** `validate_url(url)` is called
- **THEN** the normalized URL string is returned

#### Scenario: Empty URL rejected

- **GIVEN** an empty or whitespace-only string
- **WHEN** `validate_url(url)` is called
- **THEN** a `ValueError` is raised with message indicating the URL cannot be empty

#### Scenario: Malformed URL rejected

- **GIVEN** a string that does not match the expected URL pattern
- **WHEN** `validate_url(url)` is called
- **THEN** a `ValueError` is raised with message indicating regex mismatch

### Requirement: Normalize URLs for comparison

The system SHALL normalize validated URLs through Pydantic's `HttpUrl` so that equivalent URLs (e.g., with or without trailing slash) produce the same normalized form.

#### Scenario: Trailing slash normalization

- **GIVEN** two URLs that differ only by a trailing slash
- **WHEN** both are passed through `validate_url()`
- **THEN** both return the same normalized string

### Requirement: Extract URL from bookmark content

The system SHALL provide a utility to extract the URL from a bookmark object based on its content type — `url` for link bookmarks, `source_url` for text and asset bookmarks.

#### Scenario: Extract URL from link bookmark

- **GIVEN** a bookmark with content type `"link"` and a `url` field
- **WHEN** `extract_url_from_bookmark(bookmark)` is called
- **THEN** the link URL is returned

#### Scenario: Extract URL from text bookmark with source URL

- **GIVEN** a bookmark with content type `"text"` and a `source_url` field
- **WHEN** `extract_url_from_bookmark(bookmark)` is called
- **THEN** the source URL is returned

#### Scenario: No URL extractable

- **GIVEN** a bookmark with no extractable URL (e.g., text without source URL)
- **WHEN** `extract_url_from_bookmark(bookmark)` is called
- **THEN** `None` is returned

## Technical Notes

- **Implementation**: `src/karakeep_client/karakeep.py` — `validate_url`, `extract_url_from_bookmark`, `URL_REGEX`, `temp_env_var`
- **Dependencies**: none
