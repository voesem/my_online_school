import re

from rest_framework.serializers import ValidationError


class URLValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile('https://www.youtube.com/')
        tmp_val = dict(value).get(self.field)

        if not bool(reg.match(tmp_val)):
            raise ValidationError('В поле "Ссылка на видео" допускается размещать только ссылки на видео с YouTube')
