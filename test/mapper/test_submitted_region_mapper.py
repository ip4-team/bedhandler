from bedhandler.mapper import SubmittedRegionMapper

sub_mapper = SubmittedRegionMapper()


def test_mapper_pattern():
    assert sub_mapper.pattern == 'SUBMITTED_REGION='


def test_mapper_to_entity():
    assert sub_mapper.to_entity('SUBMITTED_REGION=') == ['']


def test_mapper_to_entity_list():
    assert sub_mapper.to_entity_list('GENE_ID=SAMD11&SAMD11&SAMD11;SUBMITTED_REGION=&&;Pool=11&12&1') == [[''],
                                                                                                          [''],
                                                                                                          ['']]


def test_mapper_to_entity_list_str_without_pattern():
    assert sub_mapper.to_entity_list('GENE_ID=SAMD11&SAMD11&SAMD11;Pool=4,1&5,2&6,3') == []
    assert sub_mapper.to_entity_list('') == []
