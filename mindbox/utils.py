from mindbox.exceptions import ErrorDetail, ValidationError


def validate_string_length(field_name: str, value: str, *, min_l: int = 0, max_l: int = 10) -> bool:
    _len = len(value)
    if _len < min_l or _len > max_l:
        raise ValidationError([ErrorDetail(f"must be between {min_l} and {max_l} characters long", field_name)])
    return True
