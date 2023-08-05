# -*- coding: utf-8 -*-
"""Generic errors for immutable data validation."""


class ImmutableDataValidationError(Exception):
    def __init__(self, msg: str = None, append_text: str = None):
        if append_text is not None:
            msg = "%s %s" % (msg, append_text)
        super().__init__(msg)


class ImmutableDataValidationValueError(ImmutableDataValidationError, ValueError):
    pass


class ImmutableDataValidationTypeError(ImmutableDataValidationError, TypeError):
    pass


class WrappedValidationCollectionError(ImmutableDataValidationError):
    pass


class MissingTimezoneError(ImmutableDataValidationValueError):
    pass


class TimezoneNotUtcError(ImmutableDataValidationValueError):
    pass


class MicrosecondsInSqlTimeError(ImmutableDataValidationValueError):
    pass


# wrapped errors for validation_collection


class WrapperValidationCollectionError(ImmutableDataValidationError):
    pass


class ValidationCollectionEmptyValueError(
    ImmutableDataValidationValueError, WrapperValidationCollectionError
):
    pass


class ValidationCollectionMinimumLengthError(
    ImmutableDataValidationValueError, WrapperValidationCollectionError
):
    pass


class ValidationCollectionMaximumLengthError(
    ImmutableDataValidationValueError, WrapperValidationCollectionError
):
    pass


class ValidationCollectionCannotCoerceError(
    ImmutableDataValidationTypeError, WrapperValidationCollectionError
):
    pass


class ValidationCollectionNotAnIntegerError(
    ImmutableDataValidationValueError, WrapperValidationCollectionError
):
    pass


class ValidationCollectionMinimumValueError(
    ImmutableDataValidationValueError, WrapperValidationCollectionError
):
    pass


class ValidationCollectionMaximumValueError(
    ImmutableDataValidationValueError, WrapperValidationCollectionError
):
    pass
