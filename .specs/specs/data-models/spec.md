# Data Models Specification

> Generated from code analysis on 2026-03-29
> Source files: src/karakeep_client/models.py

## Purpose

Define the Pydantic data models that represent Karakeep API payloads. All models support both camelCase (API wire format) and snake_case (Python convention) field access, with discriminated content types for bookmark payloads.

## Requirements

### Requirement: Support camelCase and snake_case field access

All Karakeep data models SHALL accept both camelCase (API alias) and snake_case (Python name) input, and serialize to camelCase by default.

#### Scenario: Parse camelCase API response

- **GIVEN** a JSON payload with camelCase field names from the Karakeep API
- **WHEN** the payload is validated by a Karakeep model
- **THEN** fields are accessible via snake_case attribute names

#### Scenario: Serialize to camelCase for API requests

- **GIVEN** a populated model instance
- **WHEN** `model_dump(by_alias=True)` is called
- **THEN** the output dictionary uses camelCase keys matching the API wire format

#### Scenario: Snake_case output available on demand

- **GIVEN** a populated model instance
- **WHEN** `model_dump(by_alias=False)` is called
- **THEN** the output dictionary uses snake_case keys

### Requirement: Discriminate bookmark content types

The `Bookmark` model SHALL accept content payloads of type `link`, `text`, `asset`, or `unknown`, automatically selecting the correct content model based on the `type` field.

#### Scenario: Link content parsed correctly

- **GIVEN** a bookmark payload with `content.type` equal to `"link"`
- **WHEN** the bookmark is validated
- **THEN** the `content` field is an instance of the link content model with URL and metadata fields

#### Scenario: Asset content parsed correctly

- **GIVEN** a bookmark payload with `content.type` equal to `"asset"`
- **WHEN** the bookmark is validated
- **THEN** the `content` field is an instance of the asset content model with asset type and asset ID

#### Scenario: Unknown content type accepted

- **GIVEN** a bookmark payload with `content.type` equal to `"unknown"`
- **WHEN** the bookmark is validated
- **THEN** the `content` field is an instance of the unknown content model

### Requirement: Support cursor-based pagination models

The system SHALL provide paginated response models with a list of items and an optional next cursor for sequential page retrieval.

#### Scenario: Paginated bookmarks with next page

- **GIVEN** a paginated API response with a non-null `nextCursor`
- **WHEN** the response is validated as `PaginatedBookmarks`
- **THEN** the `next_cursor` field contains the cursor for the next page

#### Scenario: Paginated bookmarks at last page

- **GIVEN** a paginated API response with a null `nextCursor`
- **WHEN** the response is validated as `PaginatedBookmarks`
- **THEN** the `next_cursor` field is `None`

### Requirement: Enforce literal type constraints on enum-like fields

Models SHALL enforce literal type constraints on fields such as `attached_by`, `asset_type`, `color`, `source`, `tagging_status`, and `type`, rejecting invalid values at validation time.

#### Scenario: Valid literal value accepted

- **GIVEN** a payload with a `taggingStatus` value of `"success"`
- **WHEN** the model is validated
- **THEN** the field is set to `"success"`

#### Scenario: Invalid literal value rejected

- **GIVEN** a payload with an `assetType` value not in the allowed set
- **WHEN** the model is validated
- **THEN** a `ValidationError` is raised

### Requirement: Represent PATCH bookmark partial response

The system SHALL provide a `BookmarkUpdateResponse` model matching the partial object returned
by `PATCH /bookmarks/{bookmarkId}`, which includes metadata fields only and does not include
`tags`, `content`, or `assets`.

#### Scenario: PATCH response validates without content or tags

- **GIVEN** a PATCH response payload containing `id`, `createdAt`, `modifiedAt`, `archived`,
  `favourited`, `taggingStatus`, `summarizationStatus`, and `userId` but no `tags`, `content`,
  or `assets` fields
- **WHEN** the payload is validated as `BookmarkUpdateResponse`
- **THEN** the model is populated successfully with all present fields

#### Scenario: PATCH response with only required fields

- **GIVEN** a minimal PATCH response containing only the required fields: `id`, `createdAt`,
  `modifiedAt`, `archived`, `favourited`, `taggingStatus`, `summarizationStatus`, `userId`
- **WHEN** the payload is validated as `BookmarkUpdateResponse`
- **THEN** optional fields (`title`, `note`, `summary`, `source`) default to `None`

### Requirement: Represent tag attach response

The system SHALL provide a `BookmarkTagsAttachResponse` model with an `attached` field
containing the list of tag IDs that were attached.

#### Scenario: Attach response validates

- **GIVEN** a response payload `{"attached": ["id1", "id2"]}`
- **WHEN** the payload is validated as `BookmarkTagsAttachResponse`
- **THEN** the `attached` field contains the list of tag ID strings

### Requirement: Represent tag detach response

The system SHALL provide a `BookmarkTagsDetachResponse` model with a `detached` field
containing the list of tag IDs that were detached.

#### Scenario: Detach response validates

- **GIVEN** a response payload `{"detached": ["id1"]}`
- **WHEN** the payload is validated as `BookmarkTagsDetachResponse`
- **THEN** the `detached` field contains the list of tag ID strings

## Technical Notes

- **Implementation**: `src/karakeep_client/models.py` — `KarakeepBaseModel`, `Bookmark`, `BookmarkUpdateResponse`, `BookmarkTagsAttachResponse`, `BookmarkTagsDetachResponse`, `PaginatedBookmarks`, `ContentTypeLink`, `ContentTypeText`, `ContentTypeAsset`, `ContentTypeUnknown`, `BookmarkAsset`, `Asset`, `Tag`, `TagShort`, `Highlight`, `PaginatedHighlights`, `BookmarkList`
- **Dependencies**: none
- **Schema reference**: karakeep-api.json `components/schemas` — `Bookmark`, `PaginatedBookmarks`, `Tag`, `Highlight`, `BookmarkList`, `Asset`, content type discriminated union via `type` field
