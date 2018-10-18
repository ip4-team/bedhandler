from bedhandler.mapper import RegionIdMapper

region_mapper = RegionIdMapper()


def test_mapper_pattern():
    assert region_mapper.pattern == ''


def test_mapper_to_entity():
    assert region_mapper.to_entity('OR4F5_1.1.11194') == ['OR4F5_1.1.11194']


def test_mapper_to_entity_list():
    assert region_mapper.to_entity_list('SAMD11_15.3784&SAMD11_15.565&SAMD11_15.2135') == [['SAMD11_15.3784'],
                                                                                           ['SAMD11_15.565'],
                                                                                           ['SAMD11_15.2135']]
