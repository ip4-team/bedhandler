import pytest

from bedhandler.domain import RegionId, RegionIdList

# a list of str in the form: NRD1_6882.7839
region_id = RegionId()
# a list of RegionId
region_id_list = RegionIdList()
# ids
samd11 = 'SAMD11_12.1000'
noc2l = 'NOC2L_21.5000'


@pytest.fixture(autouse=True)
def setup():
    region_id.clear()
    region_id_list.clear()


def test_region_id_genes_single_id():
    assert RegionId([samd11]).genes() == ['SAMD11']


def test_region_id_list_flattened_genes_with_single_region_id():
    assert RegionIdList([RegionId([samd11])]).flattened_genes() == ['SAMD11']


def test_region_id_genes_multiple_id():
    assert RegionId([samd11, samd11]).genes() == ['SAMD11', 'SAMD11']


def test_region_id_list_multiple_region_id():
    assert RegionIdList([RegionId([samd11]), RegionId([samd11])]).flattened_genes() == ['SAMD11', 'SAMD11']


def test_region_id_list_flattened_genes_multiple_region_id_with_multiple_id():
    assert RegionIdList([RegionId([samd11, noc2l]), RegionId([samd11, samd11])]).flattened_genes() == ['SAMD11',
                                                                                                       'NOC2L',
                                                                                                       'SAMD11',
                                                                                                       'SAMD11']


def test_region_id_list_multiple_region_id_without_repetitions():
    assert RegionIdList([RegionId([samd11]), RegionId([noc2l])]).flattened_unique_genes() == ['NOC2L', 'SAMD11']


def test_region_id_list_flattened_genes_multiple_region_id_with_multiple_id_with_repetitions():
    assert RegionIdList([RegionId([samd11, noc2l]), RegionId([samd11, samd11])]).flattened_unique_genes() == ['NOC2L',
                                                                                                              'SAMD11']
