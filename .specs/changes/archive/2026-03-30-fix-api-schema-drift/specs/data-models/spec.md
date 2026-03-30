# Delta for Data Models

## ADDED Requirements

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
