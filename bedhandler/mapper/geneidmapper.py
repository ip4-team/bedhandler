from ..domain import GeneId
from ..domain import GeneIdList
from ..mapper import BaseMapper


class GeneIdMapper(BaseMapper):
    pattern = 'GENE_ID='

    def to_entity(self, string: str) -> GeneId:
        return GeneId([gene for gene in string.split(self.pattern)[-1].split(',')])

    def to_entity_list(self, string: str) -> GeneIdList:
        return GeneIdList([self.to_entity(s) for s in string.split(';')[0].split('&')])
