from bedhandler.domain import BaseList
from bedhandler.domain import BaseMultList
from bedhandler.mapper import BaseMapper

base_mapper = BaseMapper()


def test_pattern_is_empty():
    assert base_mapper.pattern == ''


def test_to_string_empty_base_list():
    assert base_mapper.to_string(BaseList([])) == ''


def test_to_string_empty_base_mult_list():
    assert base_mapper.to_string(BaseMultList([])) == ''


def test_to_string_prepends_pattern_to_base_list_str_representation():
    assert base_mapper.to_string(BaseList([1, 2])) == '1,2'


def test_to_string_prepends_pattern_to_base_mult_list_str_representation():
    assert base_mapper.to_string(BaseMultList([BaseList([1, 2]), BaseList([1, 2])])) == '1,2&1,2'
