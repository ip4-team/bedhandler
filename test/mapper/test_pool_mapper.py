from bedhandler.mapper import PoolMapper

pool_mapper = PoolMapper()


def test_mapper_pattern():
    assert pool_mapper.pattern == 'Pool='


def test_mapper_to_entity():
    assert pool_mapper.to_entity('Pool=7,10') == [7, 10]


def test_mapper_to_entity_list():
    assert pool_mapper.to_entity_list('GENE_ID=SAMD11&SAMD11&SAMD11;Pool=4,1&5,2&6,3') == [[4, 1], [5, 2], [6, 3]]
