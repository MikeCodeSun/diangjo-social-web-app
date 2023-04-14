from django.core.exceptions import (
    ValidationError,
)
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import NumericPasswordValidator, CommonPasswordValidator

class CmPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                _("密码太常见了."),
                code='password_too_common',
            )

class NmPasswordValidator(NumericPasswordValidator):
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("密码不能全是数字."),
                code='password_entirely_numeric',
            )