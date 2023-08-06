from abc import abstractmethod, ABC
from typing import (
    TypeVar,
    Optional,
    List,
    Sequence,
    Dict,
    Any,
    Tuple,
    Type,
    cast,
    Generic,
    Mapping,
    Set,
)

import sqlalchemy as sa
import typing_inspect
from pydantic import BaseModel
from sqlalchemy import Table
from sqlalchemy.sql.elements import BinaryExpression

from repka.repositories.queries import (
    SelectQuery,
    Filters,
    Columns,
    InsertQuery,
    UpdateQuery,
    DeleteQuery,
    SqlAlchemyQuery,
    InsertManyQuery,
)
from repka.utils import model_to_primitive, is_field_equal_to_default

Created = bool


class IdModel(BaseModel):
    id: Optional[int]


GenericIdModel = TypeVar("GenericIdModel", bound=IdModel)


class AsyncQueryExecutor:
    @abstractmethod
    async def fetch_one(self, query: SqlAlchemyQuery) -> Optional[Mapping]:
        ...

    @abstractmethod
    async def fetch_all(self, query: SqlAlchemyQuery) -> Sequence[Mapping]:
        ...

    @abstractmethod
    async def fetch_val(self, query: SqlAlchemyQuery) -> Any:
        ...

    @abstractmethod
    async def insert(self, query: SqlAlchemyQuery) -> Mapping:
        ...

    @abstractmethod
    async def insert_many(self, query: SqlAlchemyQuery) -> Sequence[Mapping]:
        ...

    @abstractmethod
    async def update(self, query: SqlAlchemyQuery) -> None:
        ...

    @abstractmethod
    async def delete(self, query: SqlAlchemyQuery) -> None:
        ...

    @abstractmethod
    def execute_in_transaction(self) -> Any:
        ...


class AsyncBaseRepo(Generic[GenericIdModel], ABC):
    """
    Execute sql-queries, convert sql-row-dicts to/from pydantic models in async way
    """

    # =============
    # CONFIGURATION
    # =============

    @property
    @abstractmethod
    def table(self) -> Table:
        pass

    @property
    def ignore_default(self) -> Sequence[str]:
        """
        Columns will be inserted only if their values are not equal to default values of
        corresponding models' fields
        These columns will be set after insert
        """
        return []

    def serialize(self, entity: GenericIdModel) -> Dict:
        return model_to_primitive(entity, without_id=True)

    def deserialize(self, **kwargs: Any) -> GenericIdModel:
        entity_type = self._get_generic_type()
        return entity_type(**kwargs)

    @property
    @abstractmethod
    def _query_executor(self) -> AsyncQueryExecutor:
        ...

    # ==============
    # SELECT METHODS
    # ==============

    async def first(
        self, *filters: BinaryExpression, orders: Columns = None
    ) -> Optional[GenericIdModel]:
        query = SelectQuery(self.table, filters, orders or [])()
        row = await self._query_executor.fetch_one(query)
        return self.deserialize(**row) if row else None

    async def get_by_id(self, entity_id: int) -> Optional[GenericIdModel]:
        return await self.first(self.table.c.id == entity_id)

    async def get_or_create(
        self, filters: Filters = None, defaults: Dict = None
    ) -> Tuple[GenericIdModel, Created]:
        entity = await self.first(*(filters or []))
        if entity:
            return entity, False

        entity = self.deserialize(**(defaults or {}))
        entity = await self.insert(entity)
        return entity, True

    async def get_all(
        self, filters: Filters = None, orders: Columns = None
    ) -> List[GenericIdModel]:
        query = SelectQuery(self.table, filters or [], orders or [])()
        rows = await self._query_executor.fetch_all(query)
        return [cast(GenericIdModel, self.deserialize(**row)) for row in rows]

    async def get_by_ids(self, entity_ids: Sequence[int]) -> List[GenericIdModel]:
        return await self.get_all(filters=[self.table.c.id.in_(entity_ids)])

    async def get_all_ids(
        self, filters: Sequence[BinaryExpression] = None, orders: Columns = None
    ) -> Sequence[int]:
        """
        Same as get_all() but returns only ids.
        :param filters: List of conditions
        :param orders: List of orders
        :return: List of ids
        """
        query = SelectQuery(
            self.table, filters or [], orders or [], select_columns=[self.table.c.id]
        )()
        rows = await self._query_executor.fetch_all(query)
        return [row["id"] for row in rows]

    async def exists(self, *filters: BinaryExpression) -> bool:
        query = SelectQuery(
            self.table, filters, select_columns=[sa.func.count(self.table.c.id)]
        )()
        result = await self._query_executor.fetch_val(query)
        return bool(result)

    # ==============
    # INSERT METHODS
    # ==============

    async def insert(self, entity: GenericIdModel) -> GenericIdModel:
        serialized = self._serialize_for_insertion(entity)
        returning_columns = self._get_insert_returning_columns()
        query = InsertQuery(self.table, serialized, returning_columns)()

        row = await self._query_executor.insert(query)

        return self._set_ignored_fields(entity, row)

    async def insert_many(self, entities: List[GenericIdModel]) -> List[GenericIdModel]:
        if not entities:
            return entities

        serialized = [self._serialize_for_insertion(entity) for entity in entities]
        returning_columns = self._get_insert_returning_columns()
        query = InsertManyQuery(self.table, serialized, returning_columns)()

        rows = await self._query_executor.insert_many(query)
        for entity, row in zip(entities, rows):
            self._set_ignored_fields(entity, row)

        return entities

    # ==============
    # UPDATE METHODS
    # ==============

    async def update(self, entity: GenericIdModel) -> GenericIdModel:
        assert entity.id
        update_values = self.serialize(entity)
        query = UpdateQuery(self.table, update_values, entity.id)()
        await self._query_executor.update(query)
        return entity

    async def update_partial(
        self, entity: GenericIdModel, **updated_values: Any
    ) -> GenericIdModel:
        assert entity.id

        for field, value in updated_values.items():
            setattr(entity, field, value)

        serialized_entity = self.serialize(entity)
        serialized_values = {key: serialized_entity[key] for key in updated_values.keys()}

        query = UpdateQuery(self.table, serialized_values, entity.id)()
        await self._query_executor.update(query)

        return entity

    async def update_many(self, entities: List[GenericIdModel]) -> List[GenericIdModel]:
        """
        No way to update many in single query:
        https://github.com/aio-libs/aiopg/issues/546

        So update entities sequentially in transaction.
        """
        if not entities:
            return entities

        async with self.execute_in_transaction():
            entities = [await self.update(entity) for entity in entities]

        return entities

    # ==============
    # DELETE METHODS
    # ==============

    async def delete(self, *filters: Optional[BinaryExpression]) -> None:
        query = DeleteQuery(self.table, filters)()
        await self._query_executor.delete(query)

    async def delete_by_id(self, entity_id: int) -> None:
        return await self.delete(self.table.c.id == entity_id)

    async def delete_by_ids(self, entity_ids: Sequence[int]) -> None:
        return await self.delete(self.table.c.id.in_(entity_ids))

    # ==============
    # OTHER METHODS
    # ==============

    def execute_in_transaction(self) -> Any:
        return self._query_executor.execute_in_transaction()

    # ==============
    # PROTECTED & PRIVATE METHODS
    # ==============

    def _get_generic_type(self) -> Type[GenericIdModel]:
        """
        Get generic type of inherited BaseRepository:

        >>> class TransactionRepo(AiopgRepository[Transaction]):
        ...     table = transactions_table
        ... # doctest: +SKIP
        >>> assert TransactionRepo().__get_generic_type() is Transaction # doctest: +SKIP
        """
        return cast(
            Type[GenericIdModel],
            typing_inspect.get_args(typing_inspect.get_generic_bases(self)[-1])[0],
        )

    def _serialize_for_insertion(self, entity: GenericIdModel) -> Dict[str, Any]:
        # key should be removed manually (not in .serialize) due to compatibility
        return {
            key: value
            for key, value in self.serialize(entity).items()
            if key not in self._get_ignored_fields(entity)
        }

    def _get_insert_returning_columns(self) -> Columns:
        return (self.table.c.id, *(getattr(self.table.c, col) for col in self.ignore_default))

    def _set_ignored_fields(self, entity: GenericIdModel, row: Mapping) -> GenericIdModel:
        entity.id = row["id"]
        for col in self._get_ignored_fields(entity):
            setattr(entity, col, row[col])
        return entity

    def _get_ignored_fields(self, entity: GenericIdModel) -> Set[str]:
        return {
            field for field in self.ignore_default if is_field_equal_to_default(entity, field)
        }
