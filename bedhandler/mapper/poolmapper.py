from ..domain import Pool
from ..domain import Pools
from ..mapper import BaseMapper


class PoolMapper(BaseMapper):
    pattern = 'Pool='

    def to_entity(self, string: str) -> Pool:
        return Pool([int(pool) for pool in string.split(self.pattern)[-1].split(',')])

    def to_entity_list(self, string: str) -> Pools:
        return Pools([self.to_entity(s) for s in string[string.index(self.pattern):].split('&')])
