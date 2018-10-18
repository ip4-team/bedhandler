class BaseList(list):
    def __str__(self) -> str:
        return ','.join(str(p) for p in self)

    def is_empty(self):
        return len(self) == 0


class BaseMultList(list):
    def __str__(self) -> str:
        return '&'.join(str(p) for p in self)

    def flattened(self) -> list:
        return [val for sublist in self for val in sublist]

    def unique_flattened(self) -> list:
        return list(set(self.flattened()))

    def is_empty(self):
        return len(self) == 0
