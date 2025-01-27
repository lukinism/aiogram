from __future__ import annotations

import secrets
import typing
from typing import TYPE_CHECKING, Any, Dict, List, Tuple, Union

from pydantic import BaseModel
from pydantic_core import from_json, to_json

from aiogram.client.default import DefaultBotProperties
from aiogram.client.default_annotations import get_default_prop_name, is_default_prop
from aiogram.types import InputFile

if TYPE_CHECKING:
    from aiogram import Bot

M = typing.TypeVar("M", bound=BaseModel)


def extract_files_from_any(value: Any) -> Tuple[Any, Dict[str, InputFile]]:
    if isinstance(value, InputFile):
        token = secrets.token_urlsafe(10)
        return f"attach://{token}", {token: value}
    if isinstance(value, BaseModel):
        return extract_files_from_model(value)
    if isinstance(value, list):
        return extract_files_from_list(value)
    return value, {}


def extract_files_from_list(value: List[Any]) -> Tuple[List[Any], Dict[str, InputFile]]:
    modified_value = []
    files = {}
    for item in value:
        modified_item, item_files = extract_files_from_any(item)
        modified_value.append(modified_item)
        files.update(item_files)
    return modified_value, files


def extract_files_from_model(model: M) -> Tuple[M, Dict[str, InputFile]]:
    files = {}
    update = {}
    for field_name, field_value in model:
        modified_value, field_files = extract_files_from_any(field_value)
        if field_files:
            files.update(field_files)
            update[field_name] = modified_value
    modified_model = model.model_copy(update=update)
    return modified_model, files


def replace_default_props(model: M, *, props: DefaultBotProperties) -> M:
    update = {}
    for field_name, field_info in model.model_fields.items():
        field_value = getattr(model, field_name)
        if is_default_prop(field_info):
            default_name = get_default_prop_name(field_info)
            default_value = props[default_name]
            unset_value = props.model_fields[default_name].default
            replaced_value = default_value if default_value != unset_value else field_value
        elif isinstance(field_value, list):
            replaced_value = [
                (
                    replace_default_props(value, props=props)
                    if isinstance(value, BaseModel)
                    else value
                )
                for value in field_value
            ]
        else:
            replaced_value = field_value
        if field_value != replaced_value:
            update[field_name] = replaced_value
    return model.model_copy(update=update)


def construct_form_data(
    model: BaseModel,
    *,
    bot: Bot,
    dumps: bool = True,  # TODO: remove in 3.14.0
) -> Tuple[Dict[str, Union[str, Any]], Dict[str, InputFile]]:
    form_data = {}
    model, files = extract_files_from_model(model)
    model = replace_default_props(model, props=bot.default)
    for key, value in model.model_dump(mode="json", exclude_none=True).items():
        form_data[key] = json_dumps(value) if dumps else value
    return form_data, files


def json_loads(value: str) -> Any:
    return from_json(value)


def json_dumps(value: Any) -> str:
    if isinstance(value, str):
        return value
    return to_json(value).decode()
