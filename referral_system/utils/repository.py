from typing import Any, Generic, TypeVar

from sqlalchemy import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Delete

from referral_system.utils.exception_handling import handle_execution
from referral_system.utils.exceptions import TableNameNotProvidedError
from referral_system.utils.types import ResultType, SQLStatement

T = TypeVar('T')


class SQLAlchemyRepository(Generic[T]):
    table_verbose_name: str

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

        if not hasattr(self, 'table_verbose_name'):
            raise TableNameNotProvidedError

    async def execute(
        self,
        execution_statement: SQLStatement,
        result_type: ResultType = ResultType.NONE,
        *_: Any,
        commit: bool = False,
        raise_on_none: bool = True,
    ) -> T | ScalarResult[T] | Any | None:
        if result_type == ResultType.NONE and not isinstance(
            execution_statement, Delete
        ):
            result_type = ResultType.ONE

        return await handle_execution(
            self.db,
            execution_statement,
            result_type,
            self.table_verbose_name,
            commit=commit,
            raise_on_none=raise_on_none,
        )
