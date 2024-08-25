from __future__ import annotations

from typing import TYPE_CHECKING, ForwardRef, Optional, cast

from pydantic.fields import FieldInfo
from typing_extensions import Annotated

from aiogram.enums import ParseMode

if TYPE_CHECKING:
    from aiogram.types import LinkPreviewOptions as _LinkPreviewOptions
else:
    _LinkPreviewOptions = ForwardRef("LinkPreviewOptions")  # noqa

DefaultParseMode = Annotated[Optional[ParseMode], "default", "parse_mode"]
DefaultDisableNotification = Annotated[Optional[bool], "default", "disable_notification"]
DefaultProtectContent = Annotated[Optional[bool], "default", "protect_content"]
DefaultAllowSendingWithoutReply = Annotated[
    Optional[bool], "default", "allow_sending_without_reply"
]
DefaultLinkPreviewOptions = Annotated[Optional[_LinkPreviewOptions], "default", "link_preview"]
DefaultShowCaptionAboveMedia = Annotated[Optional[bool], "default", "show_caption_above_media"]


def is_default_prop(info: FieldInfo) -> bool:
    return "default" in info.metadata


def get_default_prop_name(info: FieldInfo) -> str:
    name_index = info.metadata.index("default") + 1
    return cast(str, info.metadata[name_index])
