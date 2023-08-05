# -*- coding: utf-8 -*-
"""Functions for validating immutable data."""
import datetime
from typing import Optional
from typing import Union

from .errors import MicrosecondsInSqlTimeError
from .errors import MissingTimezoneError
from .errors import TimezoneNotUtcError
from .wrapped_vc_validators import validate_datetime
from .wrapped_vc_validators import validate_str


def validate_utc_datetime(
    datetime_to_validate: object,
    allow_null: bool = False,
    minimum: Optional[datetime.datetime] = None,
    maximum: Optional[datetime.datetime] = None,
    extra_error_msg: str = None,
) -> Union[None, datetime.datetime]:
    """Check that object is a valid UTC Datetime."""
    datetime_to_validate = validate_datetime(
        datetime_to_validate,
        allow_null=allow_null,
        minimum=minimum,
        maximum=maximum,
        extra_error_msg=extra_error_msg,
    )
    if allow_null and datetime_to_validate is None:
        return None
    assert datetime_to_validate is not None  # nosec  needed for mypy
    if datetime_to_validate.tzinfo is None:
        raise MissingTimezoneError(
            "The timezone must be set to UTC for a UTC datetime. But the datetime provided was timezone naive: %s"
            % datetime_to_validate,
            append_text=extra_error_msg,
        )

    a_datetime = datetime.datetime.now()
    if datetime_to_validate.tzinfo.utcoffset(a_datetime) != datetime.timedelta(hours=0):
        raise TimezoneNotUtcError(
            "The timezone must be set to UTC for a UTC datetime. But the datetime provided was in a different timezone: %s"
            % datetime_to_validate,
            append_text=extra_error_msg,
        )

    return datetime_to_validate


def validate_sql_utc_datetime(
    value: object,
    coerce_value: bool = True,
    allow_null: bool = False,
    minimum: Optional[datetime.datetime] = None,
    maximum: Optional[datetime.datetime] = None,
    extra_error_msg: str = None,
) -> Union[None, datetime.datetime]:
    """Check that object is a valid SQL UTC Datetime."""
    value = validate_utc_datetime(
        value,
        allow_null=allow_null,
        minimum=minimum,
        maximum=maximum,
        extra_error_msg=extra_error_msg,
    )
    if allow_null and value is None:
        return None
    assert value is not None  # nosec  needed for mypy
    if coerce_value:
        value = value.replace(microsecond=0)
    if value.microsecond != 0:
        raise MicrosecondsInSqlTimeError(
            "Microseconds are not allowed in time objects in SQL, but this object had microseconds: %s"
            % value,
            append_text=extra_error_msg,
        )
    return value


def validate_crc32(
    value: object, allow_null: bool = False, extra_error_msg: str = None
) -> Union[None, str]:
    """CRC32 checksums are always calculated as an 8 character string."""
    value = validate_str(
        value,
        allow_null=allow_null,
        minimum_length=8,
        maximum_length=8,
        extra_error_msg=extra_error_msg,
    )
    return value
