import pytest

from bedhandler.domain import BaseList, BaseMultList

# a list
base_list = BaseList()
# a list of lists
base_mult_list = BaseMultList()


@pytest.fixture(autouse=True)
def setup():
    base_list.clear()
    base_mult_list.clear()


def test_base_list_str_single_number():
    """
    test baseList.__str__ with single element
    """
    base_list.append(1)
    assert str(base_list) == '1'


def test_mult_list_str_single_base_list():
    """
    test baseMultList.__str__ with single baseList
    """
    base_list.append(1)
    base_mult_list.append(base_list)
    assert str(base_mult_list) == '1'


def test_base_list_str_multiple_elements():
    """
    test baseList.__str__ with multiple elements
    """
    base_list.extend([1, 2])
    assert str(base_list) == '1,2'


def test_base_mult_list_str_multiple_base_list():
    """
    test baseList.__str__ with multiple baseLists
    """
    base_list.append(1)  # [1]
    base_mult_list.extend([base_list, base_list])
    assert str(base_mult_list) == '1&1'


def test_base_mult_list_str_multiple_base_list_with_multiple_elements():
    """
    test baseMultList.__str__ with multiple baseLists with multiple elements
    """
    base_list.extend([1, 2])
    base_mult_list.extend([base_list, base_list])
    assert str(base_mult_list) == '1,2&1,2'


def test_base_mult_list_flattened_single_base_list_with_single_element():
    """
    test baseMultList.flattened with single baseList with single element
    """
    base_list.append(1)
    base_mult_list.append(base_list)
    assert base_mult_list.flattened() == [1]


def test_base_mult_list_flattened_single_base_list_with_multiple_elements():
    """
    test baseMultList.flattened with single baseList with multiple elements
    """
    base_list.extend([1, 2])
    base_mult_list.append(base_list)
    assert base_mult_list.flattened() == [1, 2]


def test_base_mult_list_flattened_multiple_base_list_without_element_repetitions():
    """
    test baseMultList.flattened with multiple baseList without element repetitions
    """
    base_list.extend([1, 3])
    base_list_2 = BaseList()
    base_list_2.append(2)
    base_mult_list.extend([base_list, base_list_2])
    assert base_mult_list.flattened() == [1, 3, 2]


def test_base_mult_list_flattened_multiple_base_list_with_element_repetitions():
    """
    test baseMultList.flattened with multiple baseList with element repetitions
    """
    base_list.extend([1, 2])
    base_mult_list.extend([base_list, base_list])
    assert base_mult_list.flattened() == [1, 2, 1, 2]


def test_base_mult_list_unique_flattened_base_list_with_single_element():
    """
    test baseMultList.unique_flattened with single baseList with single element
    """
    base_list.append(1)
    base_mult_list.append(base_list)
    assert base_mult_list.unique_flattened() == [1]


def test_base_mult_list_unique_flattened_single_base_list_with_multiple_elements():
    """
    test baseMultList.unique_flattened with single baseList with multiple elements
    """
    base_list.extend([1, 2])
    base_mult_list.append(base_list)
    assert base_mult_list.unique_flattened() == [1, 2]


def test_base_mult_list_unique_flattened_multiple_base_list_without_element_repetitions():
    """
    test baseMultList.unique_flattened with multiple base_list without element repetitions
    """
    base_list.extend([1, 3])
    base_list_2 = BaseList()
    base_list_2.append(2)
    base_mult_list.extend([base_list, base_list_2])
    assert base_mult_list.unique_flattened() == [1, 2, 3]


def test_base_mult_list_unique_flattened_multiple_base_list_with_element_repetitions():
    """
    test baseMultList.unique_flattened with multiple baseList with element repetitions
    """
    base_list.extend([1, 2])
    base_mult_list.extend([base_list, base_list])
    assert base_mult_list.unique_flattened() == [1, 2]


def test_base_list_is_empty_without_elements():
    """
    test baseList.is_empty is True when there are not elements
    """
    assert base_list.is_empty() is True


def test_base_mult_list_is_empty_without_base_lists():
    """
    test baseMultList.is_empty is True when there are no baseLists
    """
    assert base_mult_list.is_empty() is True


def test_base_list_is_empty_containing_elements():
    """
    test baseList.is_empty is False when there are elements
    """
    assert BaseList([1]).is_empty() is False
    assert BaseList([1, 2]).is_empty() is False


def test_base_mult_list_is_empty_containing_base_lists():
    """
    test baseMultList.is_empty is False when there are baseLists
    """
    assert BaseMultList([BaseList([1])]).is_empty() is False
    assert BaseMultList([BaseList([1]), BaseList([2])]).is_empty() is False
