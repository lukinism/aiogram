from typing import Any
from unittest import mock

import pytest
from black import datetime
from pydantic import BaseModel

from aiogram.client.default import DefaultBotProperties
from aiogram.client.default_annotations import (
    DefaultLinkPreviewOptions,
    DefaultParseMode,
    DefaultProtectContent,
    DefaultShowCaptionAboveMedia,
)
from aiogram.client.form import (
    construct_form_data,
    extract_files_from_model,
    replace_default_props,
    serialize_form_value,
)
from aiogram.enums import ChatType, ParseMode, TopicIconColor
from aiogram.methods import BanChatMember, SendMediaGroup, SendMessage, SendPhoto
from aiogram.types import (
    BufferedInputFile,
    InputMediaPhoto,
    LinkPreviewOptions,
    MessageId,
)
from tests.mocked_bot import MockedBot


class TestConstructFormData:
    def test_exclude_none(self, bot: MockedBot):
        method = SendMessage(chat_id=1, text="say hello", parse_mode=None)
        form_data, _ = construct_form_data(method, bot=bot)
        assert form_data == {"chat_id": "1", "text": "say hello"}

    def test_mode_json(self, bot: MockedBot):
        method = BanChatMember(
            chat_id=1,
            user_id=2,
            until_date=datetime.fromtimestamp(1234567890),
        )
        form_data, _ = construct_form_data(method, bot=bot)
        assert isinstance(method.until_date, datetime)
        assert form_data == {
            "chat_id": "1",
            "user_id": "2",
            "until_date": "1234567890",
        }

    def test_dumps(self, bot: MockedBot):
        method = SendMessage(chat_id=1, text="say hello")
        form_data, _ = construct_form_data(method, bot=bot, dumps=False)
        assert form_data == {
            "chat_id": 1,
            "text": "say hello",
        }


class TestExtractFiles:
    def test_extract_files(self):
        file = BufferedInputFile(b"123", "file.png")
        method = SendPhoto(
            chat_id=1,
            photo=file,
        )
        with mock.patch("secrets.token_urlsafe", return_value="some_key"):
            modified_method, files = extract_files_from_model(method)
        assert modified_method.photo == "attach://some_key"
        assert files == {
            "some_key": file,
        }

    def test_extract_files_media_group(self):
        file1 = BufferedInputFile(b"123", "file1.png")
        file2 = BufferedInputFile(b"456", "file2.png")
        method = SendMediaGroup(
            chat_id=1,
            media=[
                InputMediaPhoto(media=file1),
                InputMediaPhoto(media=file2),
            ],
        )
        with mock.patch("secrets.token_urlsafe", side_effect=["file1", "file2"]):
            modified_method, files = extract_files_from_model(method)
        assert modified_method.media[0].media == "attach://file1"
        assert modified_method.media[1].media == "attach://file2"
        assert files == {
            "file1": file1,
            "file2": file2,
        }


class TestReplaceDefaultProps:
    def test_replace_default_props(self):
        props = DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            protect_content=True,
            show_caption_above_media=True,
            link_preview_prefer_small_media=True,
        )

        class TestModel(BaseModel):
            parse_mode: DefaultParseMode = None
            protect_content: DefaultProtectContent = None
            show_caption_above_media: DefaultShowCaptionAboveMedia = None
            link_preview_options: DefaultLinkPreviewOptions = None

        model = TestModel()
        assert model.parse_mode is None
        assert model.protect_content is None
        assert model.show_caption_above_media is None
        assert model.link_preview_options is None
        patched_model = replace_default_props(model, props=props)
        assert patched_model.parse_mode == ParseMode.HTML
        assert patched_model.protect_content is True
        assert patched_model.show_caption_above_media is True
        assert patched_model.link_preview_options == LinkPreviewOptions(
            prefer_small_media=True,
        )


class TestSerializeFormValue:
    @pytest.mark.parametrize(
        "value,result",
        [
            ["text", "text"],
            [ChatType.PRIVATE, "private"],
            [TopicIconColor.RED, "16478047"],
            [42, "42"],
            [True, "true"],
            [["test"], '["test"]'],
            [["test", ["test"]], '["test",["test"]]'],
            [[{"test": "pass"}], '[{"test":"pass"}]'],
            [{"test": "pass", "number": 42}, '{"test":"pass","number":42}'],
            [{"foo": {"test": "pass"}}, '{"foo":{"test":"pass"}}'],
            [
                {"message": MessageId(message_id=1337)},
                '{"message":{"message_id":1337}}',
            ],
        ],
    )
    def test_serialize_form_value(self, value: Any, result: str):
        assert serialize_form_value(value) == result
