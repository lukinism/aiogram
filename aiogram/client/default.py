from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel

from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions


class DefaultBotProperties(BaseModel):
    """
    Default bot properties.
    """

    parse_mode: Optional[ParseMode] = None
    """Default parse mode for messages."""
    disable_notification: Optional[bool] = None
    """Sends the message silently. Users will receive a notification with no sound."""
    protect_content: Optional[bool] = None
    """Protects content from copying."""
    allow_sending_without_reply: Optional[bool] = None
    """Allows to send messages without reply."""
    link_preview: Optional[LinkPreviewOptions] = None
    """Link preview settings."""
    show_caption_above_media: Optional[bool] = None
    """Show caption above media."""

    @property
    def is_empty(self) -> bool:
        return all(
            getattr(self, field_name) == field_info.default
            for field_name, field_info in self.model_fields.items()
        )

    def __init__(
        self,
        *,
        parse_mode: Optional[ParseMode] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        link_preview: Optional[LinkPreviewOptions] = None,
        link_preview_is_disabled: Optional[bool] = None,
        link_preview_prefer_small_media: Optional[bool] = None,
        link_preview_prefer_large_media: Optional[bool] = None,
        link_preview_show_above_text: Optional[bool] = None,
        show_caption_above_media: Optional[bool] = None,
    ):
        link_preview = link_preview or LinkPreviewOptions()
        link_preview = LinkPreviewOptions(
            is_disabled=link_preview.is_disabled or link_preview_is_disabled,
            url=link_preview.url,
            prefer_small_media=link_preview.prefer_small_media or link_preview_prefer_small_media,
            prefer_large_media=link_preview.prefer_large_media or link_preview_prefer_large_media,
            show_above_text=link_preview.show_above_text or link_preview_show_above_text,
        )
        link_preview = link_preview if link_preview.model_dump(exclude_none=True) else None

        super().__init__(
            parse_mode=parse_mode,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            link_preview=link_preview,
            show_caption_above_media=show_caption_above_media,
        )

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item, None)
