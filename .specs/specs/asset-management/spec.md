# Asset Management Specification

> Generated from code analysis on 2026-03-29
> Source files: src/karakeep_client/karakeep.py, src/karakeep_client/models.py

## Purpose

Define how assets (files, images, PDFs) are uploaded, retrieved, and associated with bookmarks through the Karakeep API.
Covers standalone asset operations and bookmark-asset association management.

## Requirements

### Requirement: Upload a new asset from a local file

The client SHALL provide a method to upload a file from the local filesystem, detecting MIME type automatically and returning validated asset metadata.

#### Scenario: Successful file upload

- **GIVEN** a valid local file path
- **WHEN** `upload_new_asset(file_path)` is called
- **THEN** an `Asset` object is returned with the asset ID, content type, size, and file name

**Schema reference:** karakeep-api.json `POST /assets` — multipart file upload; response `Asset` (`assetId`, `contentType`, `size`, `fileName`)

#### Scenario: File does not exist

- **GIVEN** a file path that does not exist on the filesystem
- **WHEN** `upload_new_asset(file_path)` is called
- **THEN** a `FileNotFoundError` is raised

### Requirement: Retrieve raw asset content by ID

The client SHALL provide a method to retrieve the raw bytes of an asset by its ID.

#### Scenario: Successful asset retrieval

- **GIVEN** a valid asset ID
- **WHEN** `get_asset(asset_id)` is called
- **THEN** the raw asset content is returned as `bytes`

**Schema reference:** karakeep-api.json `GET /assets/{assetId}` — binary response (`application/octet-stream`)

#### Scenario: Invalid asset ID

- **GIVEN** an empty, blank, or too-short asset ID
- **WHEN** `get_asset(asset_id)` is called
- **THEN** a `ValueError` is raised

### Requirement: Attach an asset to a bookmark

The client SHALL provide a method to attach an existing asset to a bookmark with a specified asset type.

#### Scenario: Successful asset attachment

- **GIVEN** a valid bookmark ID, asset ID, and asset type
- **WHEN** `attach_bookmark_asset(bookmark_id, asset_id, asset_type)` is called
- **THEN** a `BookmarkAsset` object is returned confirming the attachment

**Schema reference:** karakeep-api.json `POST /bookmarks/{bookmarkId}/assets` — request body `{id, assetType}`; response `BookmarkAsset`

### Requirement: Replace a bookmark's asset

The client SHALL provide a method to replace an existing asset on a bookmark with a different asset.

#### Scenario: Successful asset replacement

- **GIVEN** a bookmark with an attached asset
- **WHEN** `update_bookmark_asset(bookmark_id, asset_id, new_asset_id)` is called
- **THEN** the old asset is replaced and `None` is returned on success

**Schema reference:** karakeep-api.json `PUT /bookmarks/{bookmarkId}/assets/{assetId}` — request body `{assetId}`; 204 No Content

### Requirement: Detach an asset from a bookmark

The client SHALL provide a method to detach an asset from a bookmark.

#### Scenario: Successful asset detachment

- **GIVEN** a bookmark with an attached asset
- **WHEN** `delete_bookmark_asset(bookmark_id, asset_id)` is called
- **THEN** the asset is detached and `None` is returned on success

**Schema reference:** karakeep-api.json `DELETE /bookmarks/{bookmarkId}/assets/{assetId}` — 204 No Content

## Technical Notes

- **Implementation**: `src/karakeep_client/karakeep.py` — `upload_new_asset`, `get_asset`, `attach_bookmark_asset`, `update_bookmark_asset`, `delete_bookmark_asset`
- **Dependencies**: client-lifecycle, data-models
