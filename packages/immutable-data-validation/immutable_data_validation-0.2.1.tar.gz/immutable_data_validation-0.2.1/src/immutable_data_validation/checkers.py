# -*- coding: utf-8 -*-
"""Functions for checking type of datas."""
from .errors import ImmutableDataValidationError
from .errors import ValidationCollectionCannotCoerceError
from .errors import ValidationCollectionEmptyValueError
from .validators import validate_utc_datetime
from .wrapped_vc_validators import validate_uuid


def is_utc_datetime(datetime_to_validate: object) -> bool:
    try:
        validate_utc_datetime(datetime_to_validate)
    except ImmutableDataValidationError:
        return False
    return True


def is_uuid(uuid_to_validate: str) -> bool:
    try:
        validate_uuid(uuid_to_validate)
    except (ValidationCollectionEmptyValueError, ValidationCollectionCannotCoerceError):
        return False
    return True
