# Design: Fix API Schema Drift

## Context

The client is a thin async wrapper around the Karakeep HTTP API. All public methods validate
API responses into Pydantic models before returning. The upstream OpenAPI spec is the
authoritative source of truth for response shapes; the client's models must match it exactly.
Four response shapes diverge from the spec, causing either runtime crashes or untyped leakage.

## Decisions

### Decision: BookmarkUpdateResponse as a separate model, not a follow-up GET

**Chosen:** Introduce a new `BookmarkUpdateResponse` model that matches the PATCH endpoint's
actual partial response shape.

**Rationale:** The PATCH response is intentionally a partial record — it contains metadata
fields only, not the full bookmark graph (no `tags`, `content`, `assets`). Callers updating a
bookmark rarely need the full record; if they do, they can call `get_bookmark()` explicitly.
Performing an implicit follow-up GET would double the API calls for every update, add latency,
and introduce a TOCTOU window where the extra GET returns state that has changed since the PATCH.

**Alternatives considered:**

- **Return full `Bookmark` via follow-up GET**: Hidden extra API call; TOCTOU risk; violates principle of least surprise for a method named `update_bookmark`.
- **Return `dict[str, Any]`**: Weakens the public API contract with no validation; callers lose type safety.
- **Make `tags`, `content`, `assets` optional on `Bookmark`**: Pollutes the main `Bookmark` model and breaks every caller that currently assumes those fields are always present on a fetched bookmark.

### Decision: Catch ValueError in get_bookmark_id_by_url, not filter by content type

**Chosen:** Wrap the inner `validate_url` call in a `try/except ValueError` and continue to
the next candidate on failure.

**Rationale:** Filtering by content type (only calling `validate_url` for link bookmarks)
would silently never match text or asset bookmarks that have valid source URLs — which are
legitimate match targets. The existing logic intentionally extracts URLs from all content types.
Catching at the validate call is narrower and preserves the intent of the loop.

**Alternatives considered:**

- **Filter to link bookmarks only**: Breaks matching for text/asset bookmarks with valid source URLs.
- **Pre-validate source_url in the model**: The model field is intentionally `str | None` (it's not a URI field per the API schema); enforcing URL format at the model level would reject valid API responses.

### Decision: Typed response models for tag operations, not TypedDict or bare dict

**Chosen:** Pydantic models `BookmarkTagsAttachResponse` and `BookmarkTagsDetachResponse`.

**Rationale:** Consistent with every other method in the client that validates responses. A
`TypedDict` would type-check statically but provide no runtime validation. A bare `dict` gives
neither. Since the tag response shapes are simple and stable, the overhead of two small models
is trivial.

**Alternatives considered:**

- **TypedDict**: Static typing without runtime validation; inconsistent with the rest of the client.
- **Keep `dict[str, Any]`**: No change — maintains the existing untyped gap.

## Architecture

```text
PATCH /bookmarks/{bookmarkId}
  └─► _call("PATCH", ...)
        └─► BookmarkUpdateResponse.model_validate(response_data)   ← was Bookmark

POST /bookmarks/{bookmarkId}/tags
  └─► _call("POST", ...)
        └─► BookmarkTagsAttachResponse.model_validate(response_data) ← was dict[str, Any]

DELETE /bookmarks/{bookmarkId}/tags
  └─► _call("DELETE", ...)
        └─► BookmarkTagsDetachResponse.model_validate(response_data) ← was dict[str, Any]

get_bookmark_id_by_url(url)
  └─► for bookmark in search_response.bookmarks:
        bookmark_url = extract_url_from_bookmark(bookmark)
        if bookmark_url:
            try:
              if validate_url(bookmark_url) == url: return bookmark.id
            except ValueError:
              log.debug("skipping malformed url"); continue   ← was: propagated to caller
```

## Risks

- **Breaking change for `update_bookmark` callers**: Any code that currently calls
  `update_bookmark` and accesses `.tags`, `.content`, or `.assets` on the result will break.
  Mitigation: the current code already raises a `ValidationError` at runtime on a real server,
  so no working code can be relying on those fields from the PATCH response. The change makes
  the type signature match observable reality.
- **Breaking change for `add_bookmark_tags` / `delete_bookmark_tags` callers**: Callers that
  treat the return value as a plain dict will need to use attribute access instead. Mitigation:
  the new models are simple and the attribute names (`attached`, `detached`) match the existing
  dict keys exactly; Pydantic models support `model.attached` as well as iteration.
