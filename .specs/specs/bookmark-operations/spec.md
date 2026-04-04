# Bookmark Operations Specification

> Generated from code analysis on 2026-03-29
> Source files: src/karakeep_client/karakeep.py, src/karakeep_client/models.py

## Purpose

Define the client's bookmark CRUD operations, paginated listing, search, and URL-based lookup against the Karakeep API.
All operations are asynchronous and return validated Pydantic models.

## Requirements

### Requirement: Retrieve paginated bookmarks

The client SHALL provide a method to retrieve a single page of bookmarks with optional filters for archived status, favourited status, sort order, page size, cursor, and content inclusion.

#### Scenario: Fetch one page of bookmarks

- **GIVEN** the client is authenticated and connected
- **WHEN** `get_bookmarks_paged()` is called with optional filter parameters
- **THEN** a `PaginatedBookmarks` object is returned containing bookmarks and an optional next cursor

**Schema reference:** karakeep-api.json `GET /bookmarks` — query params `archived`, `favourited`, `sortOrder`, `limit`, `cursor`, `includeContent`; response `PaginatedBookmarks`

#### Scenario: Page size limit enforced

- **GIVEN** a caller requests bookmarks with `limit` greater than 100
- **WHEN** `get_bookmarks_paged()` is called
- **THEN** a `ValueError` is raised before any API request is made

### Requirement: Retrieve a single bookmark by ID

The client SHALL provide a method to retrieve a single bookmark by its ID, with optional content inclusion control.

#### Scenario: Fetch bookmark by ID

- **GIVEN** the client is authenticated and a valid bookmark ID is known
- **WHEN** `get_bookmark(bookmark_id)` is called
- **THEN** a `Bookmark` object is returned

**Schema reference:** karakeep-api.json `GET /bookmarks/{bookmarkId}` — path param `bookmarkId`; response `Bookmark`

### Requirement: Search bookmarks by query

The client SHALL provide a method to search bookmarks by a required query string, with optional sort order, page size, cursor, and content inclusion.

#### Scenario: Search returns matching bookmarks

- **GIVEN** the client is authenticated
- **WHEN** `search_bookmarks(q)` is called with a query string
- **THEN** a `PaginatedBookmarks` object is returned containing matching bookmarks

**Schema reference:** karakeep-api.json `GET /bookmarks/search` — query params `q`, `sortOrder`, `limit`, `cursor`, `includeContent`; response `PaginatedBookmarks`

#### Scenario: Search page size limit enforced

- **GIVEN** a caller requests search results with `limit` greater than 100
- **WHEN** `search_bookmarks()` is called
- **THEN** a `ValueError` is raised before any API request is made

### Requirement: Look up bookmark ID by URL

The client SHALL provide a method to find a bookmark's ID by its URL, performing URL normalization to match bookmarks that differ only by trailing slash or scheme normalization.
Search results whose extracted URL is not a valid URL SHALL be skipped rather than aborting the lookup.

#### Scenario: URL match found

- **GIVEN** a bookmark exists with a URL that normalizes to the same value as the input
- **WHEN** `get_bookmark_id_by_url(url)` is called
- **THEN** the matching bookmark's ID is returned

#### Scenario: No URL match found

- **GIVEN** no bookmark exists matching the normalized input URL
- **WHEN** `get_bookmark_id_by_url(url)` is called
- **THEN** `None` is returned

#### Scenario: Empty or blank URL

- **GIVEN** the input URL is empty or whitespace-only
- **WHEN** `get_bookmark_id_by_url(url)` is called
- **THEN** `None` is returned without making an API request

#### Scenario: Text bookmark with non-URL source_url is skipped

- **GIVEN** search results include a text bookmark whose `source_url` is not a valid URL,
  followed by a link bookmark whose URL matches the lookup target
- **WHEN** `get_bookmark_id_by_url(url)` is called
- **THEN** the text bookmark is skipped silently and the matching link bookmark's ID is returned

#### Scenario: All candidates have non-URL source_url

- **GIVEN** all search results have non-URL or absent extractable URLs
- **WHEN** `get_bookmark_id_by_url(url)` is called
- **THEN** `None` is returned

### Requirement: Create bookmarks by type

The client SHALL provide a method to create bookmarks of type `link`, `text`, or `asset`, validating that type-specific required fields are present before making the API call.

#### Scenario: Create link bookmark

- **GIVEN** `bookmark_type` is `"link"` and `url` is provided
- **WHEN** `create_bookmark()` is called
- **THEN** a `Bookmark` object representing the created bookmark is returned

**Schema reference:** karakeep-api.json `POST /bookmarks` — request body discriminated by `type` (`link`, `text`, `asset`); response `Bookmark`

#### Scenario: Create link bookmark without URL

- **GIVEN** `bookmark_type` is `"link"` and `url` is not provided
- **WHEN** `create_bookmark()` is called
- **THEN** a `ValueError` is raised

#### Scenario: Create text bookmark without text

- **GIVEN** `bookmark_type` is `"text"` and `text` is not provided
- **WHEN** `create_bookmark()` is called
- **THEN** a `ValueError` is raised

#### Scenario: Create asset bookmark without required fields

- **GIVEN** `bookmark_type` is `"asset"` and `asset_type` or `asset_id` is missing
- **WHEN** `create_bookmark()` is called
- **THEN** a `ValueError` is raised

### Requirement: Delete a bookmark by ID

The client SHALL provide a method to delete a bookmark by its ID, returning `None` on success.

#### Scenario: Successful deletion

- **GIVEN** a valid bookmark ID
- **WHEN** `delete_bookmark(bookmark_id)` is called
- **THEN** `None` is returned

**Schema reference:** karakeep-api.json `DELETE /bookmarks/{bookmarkId}` — 204 No Content

### Requirement: Update a bookmark by ID

The client SHALL provide a method to partially update a bookmark by its ID, returning a `BookmarkUpdateResponse` reflecting the metadata fields present in the PATCH response.
Tags, content, and assets are not included in the PATCH response.

#### Scenario: Successful update returns partial response model

- **GIVEN** a valid bookmark ID and non-empty update data
- **WHEN** `update_bookmark(bookmark_id, update_data)` is called
- **THEN** a `BookmarkUpdateResponse` is returned containing the updated metadata fields

**Schema reference:** karakeep-api.json `PATCH /bookmarks/{bookmarkId}` — partial update request body; response partial bookmark (metadata only, no `tags`/`content`/`assets`)

#### Scenario: Empty update data

- **GIVEN** an empty `update_data` dictionary
- **WHEN** `update_bookmark()` is called
- **THEN** a `ValueError` is raised

## Technical Notes

- **Implementation**: `src/karakeep_client/karakeep.py` — `get_bookmarks_paged`, `get_bookmark`, `search_bookmarks`, `get_bookmark_id_by_url`, `create_bookmark`, `delete_bookmark`, `update_bookmark`
- **Dependencies**: client-lifecycle, data-models, url-validation
