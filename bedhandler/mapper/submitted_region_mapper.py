import re

from ..domain import SubmittedRegion
from ..domain import SubmittedRegionList
from ..mapper import BaseMapper


class SubmittedRegionMapper(BaseMapper):
    pattern = 'SUBMITTED_REGION='

    def to_entity(self, string: str) -> SubmittedRegion:
        return SubmittedRegion([gene for gene in string.split(self.pattern)[-1].split(',')])

    def to_entity_list(self, string: str) -> SubmittedRegionList:
        if re.search(self.pattern, string) is not None:
            return SubmittedRegionList([self.to_entity(s) for s in string.split(';')[1].split('&')])
        return SubmittedRegionList([])
