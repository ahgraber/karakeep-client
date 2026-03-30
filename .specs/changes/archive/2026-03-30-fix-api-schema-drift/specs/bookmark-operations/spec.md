# Delta for Bookmark Operations

## ADDED Requirements

### Requirement: Skip non-URL candidates in URL lookup

During `get_bookmark_id_by_url`, the client SHALL skip any search result whose extracted URL
is not a valid URL (i.e., would raise `ValueError` from `validate_url`), rather than
propagating the error to the caller.

#### Scenario: Text bookmark with non-URL source_url is skipped

- **GIVEN** search results include a text bookmark whose `source_url` is not a valid URL,
  followed by a link bookmark whose URL matches the lookup target
- **WHEN** `get_bookmark_id_by_url(url)` is called
- **THEN** the text bookmark is skipped silently and the matching link bookmark's ID is returned

#### Scenario: All candidates have non-URL source_url

- **GIVEN** all search results have non-URL or absent extractable URLs
- **WHEN** `get_bookmark_id_by_url(url)` is called
- **THEN** `None` is returned

## MODIFIED Requirements

### Requirement: Update a bookmark by ID

The client SHALL provide a method to partially update a bookmark by its ID, returning a
`BookmarkUpdateResponse` reflecting the fields present in the PATCH response.
(Previously: the method returned a `Bookmark`, which required `tags`, `content`, and `assets`
fields that the PATCH endpoint does not include, causing a `ValidationError` on real server
responses.)

#### Scenario: Successful update returns partial response model

- **GIVEN** a valid bookmark ID and non-empty update data
- **WHEN** `update_bookmark(bookmark_id, update_data)` is called
- **THEN** a `BookmarkUpdateResponse` is returned containing the updated metadata fields

#### Scenario: Empty update data

- **GIVEN** an empty `update_data` dictionary
- **WHEN** `update_bookmark()` is called
- **THEN** a `ValueError` is raised
