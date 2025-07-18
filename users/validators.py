import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(_('Password must be at least 8 characters long.'))
        if not re.search(r'[A-Z]', password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'))
        if not re.search(r'[a-z]', password):
            raise ValidationError(_('Password must contain at least one lowercase letter.'))
        if not re.search(r'\d', password):
            raise ValidationError(_('Password must contain at least one number.'))
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise ValidationError(_('Password must contain at least one special character.'))

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters long and contain at least one uppercase letter, "
            "one lowercase letter, one number, and one special character."
        )