from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_price(value):
    if value <= 0:
        raise ValidationError(
            _("%(value) is not can't be not positive!")
        )