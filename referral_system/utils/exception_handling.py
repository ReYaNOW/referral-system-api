import logging
from typing import Any

from fastapi import HTTPException
from parse import Result, compile
from sqlalchemy import ScalarResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from referral_system.utils.types import ResultType, SQLStatement

NOT_PRESENT_PATTERN = compile(
    'Key ({field})=({input}) is not present in table'
)

ALREADY_EXISTS_PATTERN = compile('Key ({field})=({input}) already exists')

NOT_NULL_PATTERN = compile(
    'null value in column "{column_name}" violates not-null constraint'
)


def handle_integrity_error(e: IntegrityError, table_name: str) -> None:
    original_driver_exception = str(e.orig)

    not_present = NOT_PRESENT_PATTERN.search(original_driver_exception)
    if not_present:
        field, input_ = get_values(not_present, 'field', 'input')
        _, field = field.rsplit('_', maxsplit=1)
        raise HTTPException(
            status_code=409,
            detail=f'{table_name} with ' f'{field}={input_} is not exists',
        ) from None

    already_exists = ALREADY_EXISTS_PATTERN.search(original_driver_exception)
    if already_exists:
        field, input_ = get_values(already_exists, 'field', 'input')
        raise HTTPException(
            status_code=409,
            detail=f'{table_name} with {field}={input_} already exists',
        ) from None

    not_null = NOT_NULL_PATTERN.search(original_driver_exception)
    if not_null:
        column_name = get_values(not_null, 'column_name')[0]
        msg = f'Field {column_name} is required'.replace('"', '')
        raise HTTPException(status_code=409, detail=msg) from None

    logging.error(original_driver_exception)
    raise HTTPException(status_code=500) from None


def get_values(result: Result, *args: str) -> list[str]:
    # Result object doesn't have .get()
    new_values = []
    try:
        for value in args:
            new_values.append(result[value])
    except KeyError:
        new_values.append(None)
    return new_values


async def handle_execution(
    session: AsyncSession,
    execution_statement: SQLStatement,
    result_type: ResultType,
    verbose_name: str,
    *_: Any,
    commit: bool = False,
    raise_on_none: bool = True,
) -> ScalarResult[Any] | Any | None:
    try:
        execution_res = await session.execute(execution_statement)

        if commit:
            await session.commit()

        if result_type == ResultType.ONE:
            result = execution_res.scalar()
        elif result_type == ResultType.MANY:
            result = execution_res.scalars()
        else:
            return None

        if result is None and raise_on_none:
            raise HTTPException(
                status_code=404, detail=f'{verbose_name} is not found'
            )

    except IntegrityError as e:
        handle_integrity_error(e, verbose_name)

    else:
        return result
