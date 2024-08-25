from __future__ import annotations

import warnings
from typing import Any, Optional

from pydantic import BaseModel

from aiogram.enums import ParseMode

from aiogram.types import LinkPreviewOptions


class Default:
    # TODO: delete
    __slots__ = ("_name",)

    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return f"Default({self._name!r})"

    def __repr__(self) -> str:
        return f"<{self}>"


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
        has_any_link_preview_option = any(
            (
                link_preview_is_disabled,
                link_preview_prefer_small_media,
                link_preview_prefer_large_media,
                link_preview_show_above_text,
            )
        )
        if has_any_link_preview_option:
            warnings.warn(
                "Passing `link_preview_is_disabled`, `link_preview_prefer_small_media`, "
                "`link_preview_prefer_large_media`, and `link_preview_show_above_text` "
                "to DefaultBotProperties initializer is deprecated. "
                "These arguments will be removed in 3.14.0 version\n"
                "Use `link_preview` instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )

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
