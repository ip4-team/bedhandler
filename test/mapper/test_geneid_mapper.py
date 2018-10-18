from bedhandler.mapper import GeneIdMapper

gene_mapper = GeneIdMapper()


def test_mapper_pattern():
    assert gene_mapper.pattern == 'GENE_ID='


def test_mapper_to_entity():
    assert gene_mapper.to_entity('GENE_ID=OR4F5') == ['OR4F5']


def test_mapper_to_entity_list():
    assert gene_mapper.to_entity_list('GENE_ID=SAMD11&SAMD11&SAMD11;Pool=4,1&5,2&6,3') == [['SAMD11'],
                                                                                           ['SAMD11'],
                                                                                           ['SAMD11']]
