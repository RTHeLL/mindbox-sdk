from typing import List, Union, Sequence, Any, Generator, Optional


class ErrorDetail(str):
    """
    A string-like object that can additionally have a field.
    """
    field = None

    def __new__(cls, string, field=None):
        self = super().__new__(cls, string)
        self.field = field
        return self

    def __eq__(self, other):
        r = super().__eq__(other)
        if r is NotImplemented:
            return NotImplemented
        try:
            return r and self.field == other.field
        except AttributeError:
            return r

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'ErrorDetail(string=%r, field=%r)' % (
            str(self),
            self.field,
        )

    def __hash__(self):
        return hash(str(self))


ErrorList = Union[Sequence[Any], ErrorDetail]


class ValidationError(ValueError):
    __slots__ = 'raw_errors', '_error_cache'

    def __init__(self, errors: Sequence[ErrorList]) -> None:
        self.raw_errors = errors
        self._error_cache: Optional[List['ErrorDetail']] = None

    def errors(self) -> List['ErrorDetail']:
        if self._error_cache is None:
            self._error_cache = list(flatten_errors(self.raw_errors))
        return self._error_cache

    def __str__(self) -> str:
        errors = self.errors()
        no_errors = len(errors)
        return f'{no_errors} validation error{"" if no_errors == 1 else "s"}\n' \
               f'{display_errors(errors)}'


def display_errors(errors: List['ErrorDetail']) -> str:
    return '\n'.join(f'{e.field} -> {e}' for e in errors)


def flatten_errors(errors: Sequence[Any]) -> Generator['ErrorDetail', None, None]:
    for error in errors:
        if isinstance(error, ErrorDetail):
            yield error
        elif isinstance(error, Exception):
            if isinstance(error, ValidationError):
                yield from flatten_errors(error.raw_errors)
            else:
                yield error_detail(error)
        elif isinstance(error, list):
            yield from flatten_errors(error)
        else:
            raise RuntimeError(f'Unknown error object: {error}')


def error_detail(exc: Exception) -> 'ErrorDetail':
    return ErrorDetail(str(exc))
