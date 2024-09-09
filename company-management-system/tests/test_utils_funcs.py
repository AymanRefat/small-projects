from utils.funcs import combine_dicts


def test_combine_dicts_one_dict():
    d = {"a": 1}
    assert d == combine_dicts(d)


def test_combine_dicts_empty():
    ds = [{}, {}, {}]
    assert {} == combine_dicts(*ds)


def test_combine_dicts_mulite_dicts():
    ds = [{"thing": 1}, {1: 2}, {3: 4}]
    assert len(combine_dicts(*ds).items()) == len(ds)
