# Tag Management Specification

> Generated from code analysis on 2026-03-29
> Source files: src/karakeep_client/karakeep.py

## Purpose

Define how tags are attached to and detached from bookmarks via the Karakeep API. Tags can be referenced by ID (existing tags) or by name (creates tag if it does not exist).

## Requirements

### Requirement: Attach tags to a bookmark

The client SHALL provide a method to attach one or more tags to a bookmark, accepting tag IDs, tag names, or both, and SHALL return a `BookmarkTagsAttachResponse` validated against the API response shape.

#### Scenario: Attach tags by ID

- **GIVEN** a valid bookmark ID and a list of tag IDs
- **WHEN** `add_bookmark_tags(bookmark_id, tag_ids=...)` is called
- **THEN** a `BookmarkTagsAttachResponse` is returned with an `attached` field listing the IDs of tags that were attached

**Schema reference:** karakeep-api.json `POST /bookmarks/{bookmarkId}/tags` — request body `{tags: [{tagId}|{tagName}]}`; response `{"attached": [tagId, ...]}`

#### Scenario: Attach tags by name

- **GIVEN** a valid bookmark ID and a list of tag names
- **WHEN** `add_bookmark_tags(bookmark_id, tag_names=...)` is called
- **THEN** a `BookmarkTagsAttachResponse` is returned confirming the tags were attached (creating tags as needed)

### Requirement: Validate tag input before API call

The client SHALL validate that at least one tag source is provided and that tag IDs and names are non-empty strings.

#### Scenario: No tags provided

- **GIVEN** neither `tag_ids` nor `tag_names` is provided
- **WHEN** `add_bookmark_tags()` or `delete_bookmark_tags()` is called
- **THEN** a `ValueError` is raised

#### Scenario: Invalid tag ID type

- **GIVEN** `tag_ids` is not a list
- **WHEN** `add_bookmark_tags()` is called
- **THEN** a `ValueError` is raised

### Requirement: Detach tags from a bookmark

The client SHALL provide a method to detach one or more tags from a bookmark, accepting tag IDs, tag names, or both, and SHALL return a `BookmarkTagsDetachResponse` validated against the API response shape.

#### Scenario: Detach tags by ID

- **GIVEN** a valid bookmark ID and a list of tag IDs
- **WHEN** `delete_bookmark_tags(bookmark_id, tag_ids=...)` is called
- **THEN** a `BookmarkTagsDetachResponse` is returned with a `detached` field listing the IDs of tags that were detached

**Schema reference:** karakeep-api.json `DELETE /bookmarks/{bookmarkId}/tags` — request body `{tags: [{tagId}|{tagName}]}`; response `{"detached": [tagId, ...]}`

## Technical Notes

- **Implementation**: `src/karakeep_client/karakeep.py` — `add_bookmark_tags`, `delete_bookmark_tags`
- **Dependencies**: client-lifecycle
