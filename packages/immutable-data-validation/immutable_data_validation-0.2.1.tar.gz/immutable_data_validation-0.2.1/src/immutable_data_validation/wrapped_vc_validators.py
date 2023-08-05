# -*- coding: utf-8 -*-
"""Functions wrapping data type validators."""
import datetime
from typing import Optional
from typing import Union
from uuid import UUID

from validator_collection import validators
from validator_collection.errors import CannotCoerceError
from validator_collection.errors import EmptyValueError
from validator_collection.errors import MaximumLengthError
from validator_collection.errors import MaximumValueError
from validator_collection.errors import MinimumLengthError
from validator_collection.errors import MinimumValueError
from validator_collection.errors import NotAnIntegerError

from .errors import ValidationCollectionCannotCoerceError
from .errors import ValidationCollectionEmptyValueError
from .errors import ValidationCollectionMaximumLengthError
from .errors import ValidationCollectionMaximumValueError
from .errors import ValidationCollectionMinimumLengthError
from .errors import ValidationCollectionMinimumValueError
from .errors import ValidationCollectionNotAnIntegerError


def validate_str(
    value: object,
    allow_null: bool = False,
    minimum_length: Optional[int] = None,
    maximum_length: Optional[int] = None,
    extra_error_msg: str = None,
) -> Union[None, str]:
    """Check that object is a valid string."""
    try:
        validated_value: str = validators.string(
            value,
            allow_empty=allow_null,
            minimum_length=minimum_length,
            maximum_length=maximum_length,
        )
    except EmptyValueError as e:
        raise ValidationCollectionEmptyValueError(e, append_text=extra_error_msg)
    except CannotCoerceError as e:
        raise ValidationCollectionCannotCoerceError(e, append_text=extra_error_msg)
    except MinimumLengthError as e:
        raise ValidationCollectionMinimumLengthError(e, append_text=extra_error_msg)
    except MaximumLengthError as e:
        raise ValidationCollectionMaximumLengthError(e, append_text=extra_error_msg)

    return validated_value


def validate_uuid(
    value: object, allow_null: bool = False, extra_error_msg: str = None
) -> Union[UUID, None]:
    """Check that object is a valid UUID."""
    try:
        validated_value: UUID = validators.uuid(value, allow_empty=allow_null)
    except EmptyValueError as e:
        raise ValidationCollectionEmptyValueError(e, append_text=extra_error_msg)
    except CannotCoerceError as e:
        raise ValidationCollectionCannotCoerceError(e, append_text=extra_error_msg)
    return validated_value


def validate_float(
    value: object,
    allow_null: bool = False,
    minimum: Optional[Union[float, int]] = None,
    maximum: Optional[Union[float, int]] = None,
    extra_error_msg: str = None,
) -> Union[float, None]:
    """Check that object is a valid float."""
    try:
        validated_value: float = validators.float(
            value, allow_empty=allow_null, minimum=minimum, maximum=maximum
        )
    except EmptyValueError as e:
        raise ValidationCollectionEmptyValueError(e, append_text=extra_error_msg)
    except CannotCoerceError as e:
        raise ValidationCollectionCannotCoerceError(e, append_text=extra_error_msg)
    except MinimumValueError as e:
        raise ValidationCollectionMinimumValueError(e, append_text=extra_error_msg)
    except MaximumValueError as e:
        raise ValidationCollectionMaximumValueError(e, append_text=extra_error_msg)

    return validated_value


def validate_int(
    value: object,
    allow_null: bool = False,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
    extra_error_msg: str = None,
) -> Union[int, None]:
    """Check that object is a valid int."""
    try:
        validated_value: int = validators.integer(
            value, allow_empty=allow_null, minimum=minimum, maximum=maximum
        )
    except EmptyValueError as e:
        raise ValidationCollectionEmptyValueError(e, append_text=extra_error_msg)
    except NotAnIntegerError as e:
        raise ValidationCollectionNotAnIntegerError(e, append_text=extra_error_msg)
    except MinimumValueError as e:
        raise ValidationCollectionMinimumValueError(e, append_text=extra_error_msg)
    except MaximumValueError as e:
        raise ValidationCollectionMaximumValueError(e, append_text=extra_error_msg)
    except CannotCoerceError as e:
        raise ValidationCollectionCannotCoerceError(e, append_text=extra_error_msg)

    return validated_value


def validate_datetime(
    value: object,
    allow_null: bool = False,
    minimum: Optional[datetime.datetime] = None,
    maximum: Optional[datetime.datetime] = None,
    extra_error_msg: str = None,
) -> Union[datetime.datetime, None]:
    """Check that object is a valid datetime."""
    try:
        validated_value: datetime.datetime = validators.datetime(
            value, allow_empty=allow_null, minimum=minimum, maximum=maximum
        )
    except EmptyValueError as e:
        raise ValidationCollectionEmptyValueError(e, append_text=extra_error_msg)
    except CannotCoerceError as e:
        raise ValidationCollectionCannotCoerceError(e, append_text=extra_error_msg)
    except MinimumValueError as e:
        raise ValidationCollectionMinimumValueError(e, append_text=extra_error_msg)
    except MaximumValueError as e:
        raise ValidationCollectionMaximumValueError(e, append_text=extra_error_msg)

    return validated_value
