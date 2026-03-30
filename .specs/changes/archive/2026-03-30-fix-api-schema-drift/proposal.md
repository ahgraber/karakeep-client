# Proposal: Fix API Schema Drift

## Intent

Several client methods produce runtime `ValidationError` or expose incorrect return types because
Pydantic models and method signatures have drifted from the actual API response shapes in the
upstream OpenAPI spec. The most severe case (`update_bookmark`) will raise on every real PATCH
response because the API returns a partial record but the client validates it against the full
`Bookmark` model, which requires `tags`, `content`, and `assets`. A secondary issue
(`get_bookmark_id_by_url`) aborts its search loop when a text or asset result has a non-URL
`source_url`, meaning a valid match later in the results is never examined.

## Scope

**In scope:**

- Introduce `BookmarkUpdateResponse` Pydantic model matching the PATCH `/bookmarks/{bookmarkId}` partial response shape
- Change `update_bookmark` return type from `Bookmark` to `BookmarkUpdateResponse`
- Fix `get_bookmark_id_by_url` to skip candidates whose extracted URL fails `validate_url`, rather than propagating the `ValueError` and aborting
- Add `"userUploaded"` to `BookmarkAsset.asset_type` Literal to match the API schema enum
- Introduce `BookmarkTagsAttachResponse` and `BookmarkTagsDetachResponse` Pydantic models for tag operation responses
- Change `add_bookmark_tags` / `delete_bookmark_tags` return types from `dict[str, Any]` to the typed response models
- Update existing tests whose mocks stub full `Bookmark` payloads for PATCH/tag routes — replace with correct partial shapes
- Add new regression tests for the malformed-source-url abort and the userUploaded enum gap
- Add `hypothesis` to dev dependencies and add property-based tests for `validate_url`

**Out of scope:**

- Implementing missing client endpoints for `Highlight` or `BookmarkList` operations
- Resolving the `userId` optionality mismatch (lenient direction, no crash risk)
- Resolving `Highlight.text`/`note` nullability inconsistency with the API schema
- Adding client-side validation of `update_data` field names against the API schema

## Approach

Introduce three new Pydantic models that mirror the actual API response shapes. The PATCH
bookmark endpoint returns a partial record without `tags`, `content`, or `assets` — model
this explicitly as `BookmarkUpdateResponse` rather than reusing `Bookmark`. The tag
attach/detach endpoints return `{"attached": [tagId, ...]}` / `{"detached": [tagId, ...]}`
where `tagId` is a plain string — model these as lightweight response wrappers.

Fix `get_bookmark_id_by_url` by catching `ValueError` from the inner `validate_url` call,
logging a debug message identifying the malformed candidate, and continuing to the next result.
The outer `validate_url` on the caller-supplied URL is unaffected.

Add `"userUploaded"` to the `BookmarkAsset.asset_type` Literal. Add `hypothesis` to dev
dependencies. Add property-based tests for `validate_url` covering: no unexpected exceptions
(only `ValueError` or a valid `str` result), idempotency on valid inputs, and the empty/whitespace
rejection invariant.

## Schema Impact

No upstream API schema changes — all modifications are to the client's Pydantic models to bring
them into alignment with the existing upstream OpenAPI spec. The `schemas/before/` snapshot was
not captured because the schema generation command requires a network fetch; run
`curl -sL <upstream-url>` manually per `.specs/.sdd/schema-config.yaml` if a baseline snapshot
is needed. No `expected.md` is applicable since the upstream API schema itself is not changing.
