from django.utils.deconstruct import deconstructible
from django.core import validators
from django.utils.translation import gettext_lazy as _

@deconstructible
class YearValidator(validators.RegexValidator):
    regex = r'^[123456789]\d{3}$'
    message = _(
        '请输入4位数字的合法年份'
    )
    flags = 0