# Quickstart

This guide provides user-facing, script-friendly examples for `karakeep-client`.

!!! note "Source alignment"
This quickstart is intentionally linked to `notebooks/karakeep_client_demo.py`.
Keep both files aligned when examples are added, removed, or behavior changes.
The quickstart is the canonical user-facing guide; the notebook file is an internal demo/reference.

## Prerequisites

- Python 3.12+
- Karakeep API key
- Karakeep base URL

Set environment variables:

```bash
export KARAKEEP_API_KEY="YOUR_API_KEY"
export KARAKEEP_BASE_URL="https://your.karakeep.instance"
```

Install dependencies:

```bash
uv sync
```

## Basic usage pattern

All client methods are asynchronous. Use `asyncio.run` in scripts.

```python
import asyncio

from karakeep_client.karakeep import KarakeepClient


async def main() -> None:
    async with KarakeepClient(verbose=True) as client:
        page = await client.get_bookmarks_paged(limit=5)
        print(f"Fetched {len(page.bookmarks)} bookmarks")

        search = await client.search_bookmarks(q="python", limit=3)
        print(f"Search returned {len(search.bookmarks)} bookmarks")

        created = await client.create_bookmark(
            bookmark_type="link",
            url="https://example.com",
            title="Example",
        )
        print(f"Created bookmark: {created.id}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Collect all bookmark URLs

```python
import asyncio

from karakeep_client.karakeep import get_all_urls


async def main() -> None:
    urls = await get_all_urls()
    print(f"Collected {len(urls)} unique URLs")


if __name__ == "__main__":
    asyncio.run(main())
```

## Asset upload example

```python
import asyncio

from karakeep_client.karakeep import KarakeepClient


async def main() -> None:
    async with KarakeepClient() as client:
        asset = await client.upload_new_asset("/absolute/path/to/file.pdf")
        bookmark = await client.create_bookmark(
            bookmark_type="asset",
            asset_type="pdf",
            asset_id=asset.asset_id,
            title="Uploaded PDF",
        )
        print(f"Asset bookmark created: {bookmark.id}")


if __name__ == "__main__":
    asyncio.run(main())
```

## Notebook/demo caveats

- `notebooks/karakeep_client_demo.py` uses notebook cell style (`# %%`) and top-level `await`.
- Some values in the demo are placeholders and are not directly runnable without edits.
- For script execution outside notebooks, follow the patterns in this quickstart.
