# Delta for Tag Management

## MODIFIED Requirements

### Requirement: Attach tags to a bookmark

The client SHALL return a `BookmarkTagsAttachResponse` from `add_bookmark_tags`, validated
against the API response shape `{"attached": [tagId, ...]}`.
(Previously: the method returned `dict[str, Any]` with no response validation, meaning
callers had no typed guarantee about the response structure.)

#### Scenario: Attach tags returns typed response

- **GIVEN** a valid bookmark ID and at least one tag ID or name
- **WHEN** `add_bookmark_tags(bookmark_id, ...)` is called
- **THEN** a `BookmarkTagsAttachResponse` is returned with an `attached` field listing the
  IDs of tags that were attached

### Requirement: Detach tags from a bookmark

The client SHALL return a `BookmarkTagsDetachResponse` from `delete_bookmark_tags`, validated
against the API response shape `{"detached": [tagId, ...]}`.
(Previously: the method returned `dict[str, Any]` with no response validation.)

#### Scenario: Detach tags returns typed response

- **GIVEN** a valid bookmark ID and at least one tag ID or name
- **WHEN** `delete_bookmark_tags(bookmark_id, ...)` is called
- **THEN** a `BookmarkTagsDetachResponse` is returned with a `detached` field listing the
  IDs of tags that were detached
