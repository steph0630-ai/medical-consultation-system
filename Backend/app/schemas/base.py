from datetime import datetime
from functools import wraps
from typing import Any, Optional, Type

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseResponseSchema(BaseSchema):
    id: int
    created_at: datetime = Field(default=0)
    updated_at: datetime = Field(default=0)

    def set_padded_id(self, pad_length: int = 4):
        if self.id is not None:
            self.padded_id = str(self.id).zfill(pad_length)
        return self

    def process_nested_padded_ids(self, pad_length: int = 4):
        self.set_padded_id(pad_length)
        for field_name, field_value in self.__dict__.items():
            if field_name.startswith("_"):
                continue
            if isinstance(field_value, BaseResponseSchema):
                field_value.process_nested_padded_ids(pad_length)
            elif isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, BaseResponseSchema):
                        item.process_nested_padded_ids(pad_length)
        return self


def format_datetime(dt: Optional[datetime]) -> str:
    return "" if dt is None else dt.isoformat()


def to_timestamp(value: Any) -> int:
    if isinstance(value, datetime):
        return int(value.timestamp())
    if value is None:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError("time fields must be valid datetime or a number")


def add_padded_id(pad_length: int = 4):
    def decorator(cls: Type):
        if not hasattr(cls, "padded_id"):
            cls.padded_id = Field(default=None, init=False)

        def format_padded_id(identifier: int) -> str:
            return str(identifier).zfill(pad_length)

        setattr(cls, "format_padded_id", staticmethod(format_padded_id))
        original_validate = getattr(cls, "model_validate", None)

        @classmethod
        @wraps(original_validate or (lambda cls, obj: cls.model_construct(**obj.__dict__)))
        def enhanced_validate(cls, obj: Any):
            if original_validate and original_validate != enhanced_validate:
                instance = original_validate(obj)
            else:
                instance = cls.model_construct(**obj.__dict__)
            instance.padded_id = cls.format_padded_id(instance.id)
            return instance

        cls.model_validate = enhanced_validate
        return cls

    return decorator
