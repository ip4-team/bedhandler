from .base import BaseList, BaseMultList


class RegionId(BaseList):
    def genes(self) -> list:
        return [region.split('_')[0] for region in self]


class RegionIdList(BaseMultList):
    def flattened_genes(self) -> list:
        return [val for sublist in self for val in sublist.genes()]

    def flattened_unique_genes(self) -> list:
        return sorted(list(set(self.flattened_genes())))
