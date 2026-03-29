"""Data models for karakeep client.

Refer to the karakeep openapi spec:
https://raw.githubusercontent.com/karakeep-app/karakeep/refs/heads/main/packages/open-api/karakeep-openapi-spec.json

NOTE: models accept both snake_case and camelCase input. Default serialization
uses camelCase alias; use `<object>.model_dump(by_alias=False)` for snake_case output.
"""

from typing import Literal, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class KarakeepBaseModel(BaseModel):
    """Base model with camelCase alias handling for Karakeep payloads."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_name=True,
        validate_by_alias=True,
        serialize_by_alias=True,
    )


class NumBookmarksByAttachedType(KarakeepBaseModel):
    """Bookmark count split by attachment source."""

    ai: float | None = None
    human: float | None = None


class TagShort(KarakeepBaseModel):
    """Compact tag representation embedded in bookmark payloads."""

    id: str
    name: str
    attached_by: Literal["ai", "human"] = Field(alias="attachedBy")


class Tag(KarakeepBaseModel):
    """Full tag representation with aggregate usage counters."""

    id: str
    name: str
    num_bookmarks: float = Field(alias="numBookmarks")
    num_bookmarks_by_attached_type: NumBookmarksByAttachedType = Field(alias="numBookmarksByAttachedType")


class ContentTypeLink(KarakeepBaseModel):
    """Bookmark content payload for link-type bookmarks."""

    type: Literal["link"] = "link"
    url: str
    title: str | None = None
    description: str | None = None
    image_url: str | None = Field(default=None, alias="imageUrl")
    image_asset_id: str | None = Field(default=None, alias="imageAssetId")
    screenshot_asset_id: str | None = Field(default=None, alias="screenshotAssetId")
    full_page_archive_asset_id: str | None = Field(default=None, alias="fullPageArchiveAssetId")
    precrawled_archive_asset_id: str | None = Field(default=None, alias="precrawledArchiveAssetId")
    video_asset_id: str | None = Field(default=None, alias="videoAssetId")
    favicon: str | None = None
    html_content: str | None = Field(default=None, alias="htmlContent")
    content_asset_id: str | None = Field(default=None, alias="contentAssetId")
    pdf_asset_id: str | None = Field(default=None, alias="pdfAssetId")
    crawl_status: Literal["success", "failure", "pending"] | None = Field(
        default=None, alias="crawlStatus"
    )
    crawled_at: str | None = Field(default=None, alias="crawledAt")
    author: str | None = None
    publisher: str | None = None
    date_published: str | None = Field(default=None, alias="datePublished")
    date_modified: str | None = Field(default=None, alias="dateModified")


class ContentTypeUnknown(KarakeepBaseModel):
    """Fallback content payload for unsupported bookmark content types."""

    type: Literal["unknown"] = "unknown"


class ContentTypeText(KarakeepBaseModel):
    """Bookmark content payload for text-type bookmarks."""

    type: Literal["text"] = "text"
    text: str
    source_url: str | None = Field(default=None, alias="sourceUrl")


class ContentTypeAsset(KarakeepBaseModel):
    """Bookmark content payload for uploaded asset bookmarks."""

    type: Literal["asset"] = "asset"
    asset_type: Literal["image", "pdf"] = Field(alias="assetType")
    asset_id: str = Field(alias="assetId")
    file_name: str | None = Field(default=None, alias="fileName")
    source_url: str | None = Field(default=None, alias="sourceUrl")
    size: float | None = None
    content: str | None = None


class BookmarkAsset(KarakeepBaseModel):
    """Asset metadata attached to a bookmark."""

    id: str
    asset_type: Literal[
        "linkHtmlContent",
        "screenshot",
        "pdf",
        "assetScreenshot",
        "bannerImage",
        "fullPageArchive",
        "video",
        "bookmarkAsset",
        "precrawledArchive",
        "userUploaded",
        "avatar",
        "unknown",
    ] = Field(alias="assetType")
    file_name: str | None = Field(default=None, alias="fileName")


class Asset(KarakeepBaseModel):
    """Metadata for an asset stored in Karakeep."""

    asset_id: str = Field(alias="assetId")
    content_type: str = Field(alias="contentType")
    size: float
    file_name: str = Field(alias="fileName")


class Bookmark(KarakeepBaseModel):
    """Primary bookmark record returned by the Karakeep API."""

    id: str
    created_at: str = Field(alias="createdAt")
    modified_at: str | None = Field(alias="modifiedAt")
    title: str | None = None
    archived: bool
    favourited: bool
    source: Literal["api", "web", "cli", "mobile", "extension", "singlefile", "rss", "import"] | None = None
    user_id: str | None = Field(default=None, alias="userId")
    tagging_status: Literal["success", "failure", "pending"] | None = Field(alias="taggingStatus")
    summarization_status: Literal["success", "failure", "pending"] | None = Field(
        default=None, alias="summarizationStatus"
    )
    note: str | None = None
    summary: str | None = None
    tags: list[TagShort]
    content: Union[ContentTypeLink, ContentTypeText, ContentTypeAsset, ContentTypeUnknown]
    assets: list[BookmarkAsset]


class PaginatedBookmarks(KarakeepBaseModel):
    """Cursor-paginated bookmark response."""

    bookmarks: list[Bookmark]
    next_cursor: str | None = Field(alias="nextCursor")


class Highlight(KarakeepBaseModel):
    """Text highlight metadata associated with a bookmark."""

    bookmark_id: str = Field(alias="bookmarkId")
    start_offset: float = Field(alias="startOffset")
    end_offset: float = Field(alias="endOffset")
    color: Literal["yellow", "red", "green", "blue"] = "yellow"
    text: str | None = None
    note: str | None = None
    id: str
    user_id: str = Field(alias="userId")
    created_at: str = Field(alias="createdAt")


class PaginatedHighlights(KarakeepBaseModel):
    """Cursor-paginated highlight response."""

    highlights: list[Highlight]
    next_cursor: str | None = Field(alias="nextCursor")


class BookmarkList(KarakeepBaseModel):
    """Bookmark list metadata for manual or smart collections."""

    id: str
    name: str
    description: str | None = None
    icon: str
    parent_id: str | None = Field(default=None, alias="parentId")
    type: Literal["manual", "smart"] = "manual"
    query: str | None = None
    public: bool
    has_collaborators: bool = Field(alias="hasCollaborators")
    user_role: Literal["owner", "editor", "viewer", "public"] = Field(alias="userRole")
