import warnings
from dataclasses import dataclass
from typing import Any, Dict, Optional

from pydantic import BaseModel

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.form import construct_form_data
from aiogram.methods import TelegramMethod
from aiogram.types import InputFile

# TODO: remove in 3.14.0


def _get_fake_bot(default: Optional[DefaultBotProperties] = None) -> Bot:
    if default is None:
        default = DefaultBotProperties()
    return Bot(token="42:Fake", default=default)


@dataclass
class DeserializedTelegramObject:
    """
    Represents a dumped Telegram object.

    :param data: The dumped data of the Telegram object.
    :type data: Dict[str, Any]
    :param files: The dictionary containing the file names as keys
        and the corresponding `InputFile` objects as values.
    :type files: Dict[str, InputFile]
    """

    data: Dict[str, Any]
    files: Dict[str, InputFile]


def deserialize_telegram_object(
    obj: BaseModel,
    default: Optional[DefaultBotProperties] = None,
    include_api_method_name: bool = True,
) -> DeserializedTelegramObject:
    """
    Deserialize Telegram Object to JSON compatible Python object.

    :param obj: The object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized Telegram object.
    """
    warnings.warn(
        "Using `aiogram.utils.serialization` is deprecated. "
        "This util will be removed in 3.14.0 version\n"
        "Use `aiogram.client.form.construct_form_data` or `obj.model_dump()` instead.",
        category=DeprecationWarning,
        stacklevel=2,
    )
    extends = {}
    if include_api_method_name and isinstance(obj, TelegramMethod):
        extends["method"] = obj.__api_method__

    if not isinstance(obj, BaseModel):
        raise TypeError("Cannot deserialize non-tg object")

    # Fake bot is needed to exclude global defaults from the object.
    fake_bot = _get_fake_bot(default=default)

    prepared, files = construct_form_data(obj, bot=fake_bot, dumps=False)
    prepared.update(extends)

    return DeserializedTelegramObject(data=prepared, files=files)


def deserialize_telegram_object_to_python(
    obj: BaseModel,
    default: Optional[DefaultBotProperties] = None,
    include_api_method_name: bool = True,
) -> Dict[str, Any]:
    """
    Deserialize telegram object to JSON compatible Python object excluding files.

    :param obj: The telegram object to be deserialized.
    :param default: Default bot properties
        should be passed only if you want to use custom defaults.
    :param include_api_method_name: Whether to include the API method name in the result.
    :return: The deserialized telegram object.
    """
    return deserialize_telegram_object(
        obj,
        default=default,
        include_api_method_name=include_api_method_name,
    ).data
