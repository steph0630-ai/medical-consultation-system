import asyncio
from math import ceil
from typing import Any, Callable, Dict, Generic, List, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import Select, func, select
from sqlalchemy.engine.result import Row
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")


class Paginator(Generic[T]):
    def __init__(self, query: Select, db: AsyncSession):
        self.query = query
        self.db = db
        self._items = None
        self._total = None
        self._per_page = 10
        self._page = 1
        self._last_page = None
        self._processors = []
        self._result = None

    async def paginate(self, page: int = 1, per_page: int = 10) -> "Paginator":
        self._page = max(1, page)
        self._per_page = max(1, per_page)
        if self._total is None:
            total_query = select(func.count()).select_from(self.query.subquery())
            self._total = await self.db.scalar(total_query)
        self._last_page = (
            ceil(self._total / self._per_page) if self._per_page > 0 else 0
        )
        paginated_query = self.query.offset(
            (self._page - 1) * self._per_page
        ).limit(self._per_page)
        self._result = await self.db.execute(paginated_query)
        keys = list(self._result.keys())
        if len(keys) == 1:
            self._items = self._result.scalars().all()
        else:
            self._items = self._process_multi_column_result(keys)
        for processor in self._processors:
            if asyncio.iscoroutinefunction(processor):
                self._items = await processor(self._items)
            else:
                self._items = processor(self._items)
        return self

    def _process_multi_column_result(self, keys: List[str]) -> List[Any]:
        if not self._result:
            return []
        rows = self._result.all()
        if not rows:
            return []
        processed_items = []
        for row in rows:
            if isinstance(row, (Row, tuple)):
                main_entity = row[0]
                for index in range(1, len(keys)):
                    setattr(main_entity, keys[index], row[index])
                processed_items.append(main_entity)
            else:
                processed_items.append(row)
        return processed_items

    def process(self, callback: Callable[[List[Any]], List[Any]]) -> "Paginator":
        self._processors.append(callback)
        return self

    def map(self, model_class: Type[BaseModel]) -> "Paginator":
        def mapper(items):
            mapped_items = []
            for item in items:
                item_dict = {
                    key: value
                    for key, value in vars(item).items()
                    if not key.startswith("_")
                }
                for attr_name in dir(item):
                    if attr_name.startswith("_") or attr_name in item_dict:
                        continue
                    try:
                        attr_value = getattr(item, attr_name)
                        if (
                            hasattr(attr_value, "__table__")
                            or attr_name in model_class.__annotations__
                        ):
                            item_dict[attr_name] = attr_value
                    except Exception:
                        pass
                try:
                    mapped_item = model_class.model_validate(item_dict)
                except Exception:
                    mapped_item = model_class.model_construct(**item_dict)
                mapped_items.append(mapped_item)
            return mapped_items

        self._items = mapper(self._items)
        return self

    @property
    def items(self) -> List[Any]:
        return self._items or []

    @property
    def total(self) -> int:
        return self._total or 0

    @property
    def per_page(self) -> int:
        return self._per_page

    @property
    def current_page(self) -> int:
        return self._page

    @property
    def last_page(self) -> int:
        return self._last_page or 0

    @property
    def has_more(self) -> bool:
        return self._page < (self._last_page or 0)

    def to_dict(self) -> Dict:
        return {
            "items": self.items,
            "total": self.total,
            "per_page": self.per_page,
            "current_page": self.current_page,
            "last_page": self.last_page,
            "has_more": self.has_more,
        }

    def to_json(self) -> Dict:
        return jsonable_encoder(self.to_dict())

    def response(
        self, message: str = "Success", code: int = 200, http_code: int = 200
    ) -> JSONResponse:
        return JSONResponse(
            content={"code": code, "message": message, "data": self.to_json()},
            status_code=http_code,
        )
