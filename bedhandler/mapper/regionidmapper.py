from ..domain import RegionId
from ..domain import RegionIdList
from ..mapper import BaseMapper


class RegionIdMapper(BaseMapper):
    pattern = ''

    @staticmethod
    def to_entity(string: str) -> RegionId:
        return RegionId([string])

    def to_entity_list(self, string: str) -> RegionIdList:
        return RegionIdList([self.to_entity(s) for s in string.split('&')])
