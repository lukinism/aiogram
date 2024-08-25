from __future__ import annotations

import secrets
from typing import Any, Dict, List, Tuple

from pydantic import BaseModel
from pydantic_core import to_json

from aiogram.types import InputFile


def extract_files_from_any(value: Any) -> Tuple[Any, Dict[str, InputFile]]:
    if isinstance(value, InputFile):
        token = secrets.token_urlsafe(10)
        return f"attach://{token}", {token: value}
    if isinstance(value, BaseModel):
        return extract_files_from_model(value)
    if isinstance(value, list):
        return extract_files_from_list(value)
    if isinstance(value, dict):
        return extract_files_from_dict(value)
    return value, {}


def extract_files_from_list(_list: List[Any]) -> Tuple[List[Any], Dict[str, InputFile]]:
    modified_list = []
    list_files = {}
    for item in _list:
        modified_item, item_files = extract_files_from_any(item)
        modified_list.append(modified_item)
        list_files.update(item_files)
    return modified_list, list_files


def extract_files_from_dict(_dict: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, InputFile]]:
    modified_dict = {}
    dict_files = {}
    for key, value in _dict.items():
        modified_value, value_files = extract_files_from_any(value)
        modified_dict[key] = modified_value
        dict_files.update(value_files)
    return modified_dict, dict_files


def extract_files_from_model(model: BaseModel) -> Tuple[BaseModel, Dict[str, InputFile]]:
    model_files = {}
    update = {}
    for field_name, field_value in model:
        modified_value, field_files = extract_files_from_any(field_value)
        if field_files:
            model_files.update(field_files)
            update[field_name] = modified_value
    modified_model = model.model_copy(update=update)
    return modified_model, model_files


def construct_form_data(model: BaseModel) -> Tuple[Dict[str, str], Dict[str, InputFile]]:
    form_data = {}
    model, files = extract_files_from_model(model)
    for key, value in model.model_dump(exclude_none=True).items():
        form_data[key] = serialize_form_value(value)
    return form_data, files


def serialize_form_value(value: Any) -> str:
    """
    Prepare jsonable value to send
    """
    if isinstance(value, str):
        return value
    return to_json(value).decode()
