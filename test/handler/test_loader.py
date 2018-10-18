import os

from bedhandler.handler import BedFileLoader

mock_dir_path = os.path.join(os.path.dirname(__file__), 'mocks/')


def test_predict_file_type_for_ampliseq_exome():
    assert BedFileLoader(mock_dir_path + 'ampliseq_exome.bed').file_type == 'ampliseq_exome'


def test_len_columns_for_ampliseq_exome():
    bed_file = BedFileLoader(mock_dir_path + 'ampliseq_exome.bed')
    expanded = bed_file.expand_columns()
    assert len(bed_file.columns) == len(expanded[0])


def test_search_map_for_ampliseq_exome():
    bed_file = BedFileLoader(mock_dir_path + 'ampliseq_exome.bed')
    column_map = bed_file.get_map_with_column_indexes()
    assert column_map[bed_file._BedFileLoader__region_id]['search'] is not None
    assert column_map[bed_file._BedFileLoader__attributes]['search'] is not None
    assert column_map[bed_file._BedFileLoader__submitted_region]['search'] is None


def test_predict_file_type_for_general_bed():
    assert BedFileLoader(mock_dir_path + 'general.bed').file_type == 'general_tsv'


def test_len_columns_for_general_bed():
    bed_file = BedFileLoader(mock_dir_path + 'general.bed')
    expanded = bed_file.expand_columns()
    assert len(bed_file.columns) == len(expanded[0])


def test_search_map_for_general_bed():
    bed_file = BedFileLoader(mock_dir_path + 'general.bed')
    column_map = bed_file.get_map_with_column_indexes()
    assert column_map[bed_file._BedFileLoader__region_id]['search'] is None
    assert column_map[bed_file._BedFileLoader__attributes]['search'] is None
    assert column_map[bed_file._BedFileLoader__submitted_region]['search'] is None


def test_predict_file_type_for_effective_regions():
    assert BedFileLoader(mock_dir_path + 'effective_regions.bed').file_type == 'effective_regions'


def test_len_columns_for_effective_regions():
    bed_file = BedFileLoader(mock_dir_path + 'effective_regions.bed')
    expanded = bed_file.expand_columns()
    assert len(bed_file.columns) == len(expanded[0])


def test_search_map_for_effective_regions():
    bed_file = BedFileLoader(mock_dir_path + 'effective_regions.bed')
    column_map = bed_file.get_map_with_column_indexes()
    assert column_map[bed_file._BedFileLoader__region_id]['search'] is not None
    assert column_map[bed_file._BedFileLoader__attributes]['search'] is not None
    assert column_map[bed_file._BedFileLoader__submitted_region]['search'] is not None


def test_predict_file_type_for_amplicon_cov():
    assert BedFileLoader(mock_dir_path + 'amplicon_cov.tsv').file_type == 'amplicon_cov'


def test_len_columns_for_amplicon_cov():
    bed_file = BedFileLoader(mock_dir_path + 'amplicon_cov.tsv')
    expanded = bed_file.expand_columns()
    assert len(bed_file.columns) == len(expanded[0])


def test_search_map_for_amplicon_cov():
    bed_file = BedFileLoader(mock_dir_path + 'amplicon_cov.tsv')
    column_map = bed_file.get_map_with_column_indexes()
    assert column_map[bed_file._BedFileLoader__region_id]['search'] is not None
    assert column_map[bed_file._BedFileLoader__attributes]['search'] is not None
    assert column_map[bed_file._BedFileLoader__submitted_region]['search'] is None


def test_loader_ignores_non_valid_data_lines():
    """
    data lines are those that start with chrom\d* or \d*
    """
    bed_file = BedFileLoader(mock_dir_path + 'mock_for_split.bed')
    #  check headers
    assert len(bed_file.header_lines) == 3
    assert bed_file.header_lines[0] == 'track'
    assert bed_file.header_lines[1] == 'browser'
    assert bed_file.header_lines[2] == 'chromosome\tbut\tignore\tit\tplease'
    #  check data
    assert bed_file.bed_lines[0] == ['chr1', '10000', '100000']
    assert bed_file.bed_lines[1] == ['chr12', '10001', '100000']
    assert bed_file.bed_lines[2] == ['12', '10000', '100000']
    assert bed_file.bed_lines[3] == ['1', '10001', '100000']


def test_loader_expanded_result_is_sorted_by_chrom_start_end():
    """
    test that when bed_lines are expanded the resulting list is sorted by
    chrom, chromStart, and chromEnd (ASC)
    """
    expanded = BedFileLoader(mock_dir_path + 'mock_for_split.bed').expand_columns()
    assert expanded[0] == ['chr1', '10000', '100000']
    assert expanded[1] == ['1', '10001', '100000']
    assert expanded[2] == ['12', '10000', '100000']
    assert expanded[3] == ['chr12', '10001', '100000']

