# Tasks: Fix API Schema Drift

## Models

- [x] Add `BookmarkUpdateResponse` to `models.py` — fields: `id`, `created_at`, `modified_at`, `title`, `archived`, `favourited`, `tagging_status`, `summarization_status`, `note`, `summary`, `source`, `user_id`
- [x] Add `BookmarkTagsAttachResponse` to `models.py` — single field `attached: list[str]`
- [x] Add `BookmarkTagsDetachResponse` to `models.py` — single field `detached: list[str]`
- N/A: `"userUploaded"` was already present in `BookmarkAsset.asset_type` before this change

## Client Methods

- [x] Change `update_bookmark` return type annotation from `Bookmark` to `BookmarkUpdateResponse`
- [x] Replace `Bookmark.model_validate(response_data)` with `BookmarkUpdateResponse.model_validate(response_data)` in `update_bookmark`
- [x] Wrap inner `validate_url(bookmark_url.strip())` in `get_bookmark_id_by_url` with `try/except ValueError` — log debug and `continue` on failure
- [x] Change `add_bookmark_tags` return type annotation from `dict[str, Any]` to `BookmarkTagsAttachResponse` and call `BookmarkTagsAttachResponse.model_validate(response_data)`
- [x] Change `delete_bookmark_tags` return type annotation from `dict[str, Any]` to `BookmarkTagsDetachResponse` and call `BookmarkTagsDetachResponse.model_validate(response_data)`

## Tests — Model Unit Tests

- [x] Add `TestBookmarkUpdateResponse` in `test_models.py` — required fields only, optional fields, camelCase aliases
- [x] Add `TestBookmarkTagsResponses` in `test_models.py` — attach/detach validate, empty list, missing field raises
- N/A: `test_bookmark_asset_user_uploaded_accepted` — `userUploaded` was already present

## Tests — Client Regression Tests

- [x] Update `test_update_bookmark_success` mock response — removed `tags`, `content`, `assets`; assert return is `BookmarkUpdateResponse`
- [x] Add `test_update_bookmark_minimal_patch_response` — stub minimal PATCH shape; assert no `ValidationError`
- [x] Add `test_get_bookmark_id_by_url_skips_malformed_source_url`
- [x] Add `test_get_bookmark_id_by_url_all_candidates_malformed`
- [x] Update `test_add_bookmark_tags_*` assertions — `isinstance(result, BookmarkTagsAttachResponse)` and `result.attached`
- [x] Add `test_delete_bookmark_tags_success` — `isinstance(result, BookmarkTagsDetachResponse)` and `result.detached`

## Tests — Hypothesis

- [x] Add `hypothesis` to `[dependency-groups.test]` in `pyproject.toml`
- [x] Add `TestValidateUrlProperties` class in `test_karakeep.py`:
  - `test_no_unexpected_exceptions` — `@given(st.text())`: only `ValueError` or valid `str` result
  - `test_idempotent_on_valid_inputs` — `@given(st.from_regex(...))`: idempotency; `assume(False)` discards non-passing inputs
