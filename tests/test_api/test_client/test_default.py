from typing import Any, Optional, Type

import pytest
from pydantic import BaseModel

from aiogram.client.default import DefaultBotProperties
from aiogram.client.default_annotations import (
    DefaultDisableNotification,
    DefaultLinkPreviewOptions,
    DefaultParseMode,
    get_default_prop_name,
    is_default_prop,
)
from aiogram.enums import ParseMode
from aiogram.types import LinkPreviewOptions


class TestDefaultAnnotated:
    def test_default_annotated(self):
        class Model(BaseModel):
            parse_mode: DefaultParseMode = None
            disable_notification: DefaultDisableNotification = None
            link_preview_options: DefaultLinkPreviewOptions = None

        def get_field_annotation(name: str) -> Optional[Type[Any]]:
            return Model.model_fields[name].annotation

        assert get_field_annotation("parse_mode") == Optional[ParseMode]
        assert get_field_annotation("disable_notification") == Optional[bool]
        assert get_field_annotation("link_preview_options") == Optional[LinkPreviewOptions]

    def test_is_default_prop(self):
        class Model(BaseModel):
            parse_mode: DefaultParseMode = None
            random_field: str = None

        assert is_default_prop(Model.model_fields["parse_mode"]) is True
        assert is_default_prop(Model.model_fields["random_field"]) is False

    def test_get_default_prop_name(self):
        class Model(BaseModel):
            parse_mode: DefaultParseMode = None
            random_name: DefaultDisableNotification = None

        assert get_default_prop_name(Model.model_fields["parse_mode"]) == "parse_mode"
        assert get_default_prop_name(Model.model_fields["random_name"]) == "disable_notification"


class TestDefaultBotProperties:
    def test_post_init_empty(self):
        default_bot_properties = DefaultBotProperties()

        assert default_bot_properties.link_preview is None

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_post_init_auto_fill_link_preview(self):
        default_bot_properties = DefaultBotProperties(
            link_preview_is_disabled=True,
            link_preview_prefer_small_media=True,
            link_preview_prefer_large_media=True,
            link_preview_show_above_text=True,
        )

        assert default_bot_properties.link_preview == LinkPreviewOptions(
            is_disabled=True,
            prefer_small_media=True,
            prefer_large_media=True,
            show_above_text=True,
        )

    def test_getitem(self):
        default_bot_properties = DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            protect_content=True,
            show_caption_above_media=True,
            link_preview=LinkPreviewOptions(
                prefer_large_media=True,
            ),
        )

        assert default_bot_properties["parse_mode"] == ParseMode.HTML
        assert default_bot_properties["protect_content"] is True
        assert default_bot_properties["show_caption_above_media"] is True
        assert default_bot_properties["link_preview"] == LinkPreviewOptions(
            prefer_large_media=True,
        )
