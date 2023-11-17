from datetime import datetime
from re import search
from typing import Dict, Tuple

from validate_email import validate_email

FIELD_TYPES = {
    'email': 'EMAIL_FIELD',
    'phone': 'PHONE_FIELD',
    'date': 'DATE_FIELD',
    'text': 'TEXT_FIELD',
}


def format_dates(query_parameters: Dict[str, str]) -> Dict[str, str]:
    """Convert dates with dashes to dates with dots.

    Args:
        query_parameters: original values.

    Returns:
        Same dict with replaces dates with dashes.
    """
    result = {}
    for field_name, value in query_parameters.items():
        try:
            date_value = datetime.strptime(value, '%Y-%m-%d')
            result[field_name] = date_value.strftime('%d.%m.%Y')
        except ValueError:
            result[field_name] = value
    return result


def validate_date(value: str) -> Tuple[bool, str]:
    """Validate date.

    Args:
        value: string to validate.

    Returns:
        if value is date: True and formatted value.
        else: False and value.
    """
    try:
        datetime.strptime(value, '%d.%m.%Y')
        return True, value
    except ValueError:
        return False, value


def validate_phone(value: str) -> bool:
    """Validate phone.

    Args:
        value: string to validate.

    Returns:
        if value is phone number: True.
        else: False.
    """
    if search(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', value):
        return True
    return False


def get_field_type(value: str) -> str:
    """Get field type.

    Args:
        value: field value.

    Returns:
        Field type from FIELD_TYPES dict.
    """
    got_date, _ = validate_date(value)
    if got_date:
        return FIELD_TYPES['date']
    if validate_email(value):
        return FIELD_TYPES['email']
    if validate_phone(value):
        return FIELD_TYPES['phone']
    return FIELD_TYPES['text']
