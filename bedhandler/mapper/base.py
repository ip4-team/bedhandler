from typing import Union

from ..domain import BaseList
from ..domain import BaseMultList


class BaseMapper:
    pattern = ''

    def to_string(self, entity: Union[BaseList, BaseMultList]) -> str:
        if entity.is_empty():
            return ''
        return '{}{}'.format(self.pattern, str(entity))
